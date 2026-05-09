"""
Classify inbound cold email replies into actionable buckets.

Buckets:
    interested     — wants to talk, asks a follow-up question, says "yes"
    objection      — has a specific concern (price, timing, scope) but isn't a no
    not_now        — soft no, "maybe later", "circle back in Q3"
    hard_no        — clear rejection
    unsubscribe    — wants off the list (LEGAL: must be honored immediately)
    auto_reply     — out-of-office, vacation auto-responder
    referral       — "talk to my colleague X"
    other          — fallback

Usage:
    python3 reply_classifier.py --thread thread.txt
    python3 reply_classifier.py --batch replies.jsonl --out classified.jsonl

Author: Gamma Wira <gammawirawibowo@gmail.com>
License: MIT
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass

import anthropic


CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001")  # cheap+fast for classification
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")


SYSTEM = """You classify cold email replies into ONE of these buckets:
- interested
- objection
- not_now
- hard_no
- unsubscribe
- auto_reply
- referral
- other

Output ONLY valid JSON: {"bucket": "...", "confidence": 0-1, "next_action": "..."}

next_action is a one-line instruction for the human/system, e.g.:
  "Reply with calendar link, mention Tuesday."
  "REMOVE FROM LIST IMMEDIATELY."
  "Forward to colleague Sarah at sarah@..."
  "Follow up in Q3 2026 (date suggested by prospect)."
  "Drop politely. Don't follow up again."
"""


@dataclass
class Classification:
    bucket: str
    confidence: float
    next_action: str


def classify(reply_text: str) -> Classification:
    if not ANTHROPIC_API_KEY:
        raise RuntimeError("ANTHROPIC_API_KEY not set")
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    resp = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=300,
        system=SYSTEM,
        messages=[{"role": "user", "content": f"Reply to classify:\n\n{reply_text}"}],
    )
    text = resp.content[0].text.strip()
    if text.startswith("```"):
        text = text.split("```", 2)[1].lstrip("json").strip()
    data = json.loads(text)
    return Classification(
        bucket=data["bucket"],
        confidence=float(data.get("confidence", 0.5)),
        next_action=data.get("next_action", ""),
    )


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--thread", help="Plain text file with the reply body")
    ap.add_argument("--batch", help="JSONL file with one {id, body} per line")
    ap.add_argument("--out", default="classified.jsonl")
    args = ap.parse_args()

    if args.thread:
        with open(args.thread, encoding="utf-8") as fh:
            body = fh.read()
        result = classify(body)
        print(json.dumps(result.__dict__, indent=2, ensure_ascii=False))
    elif args.batch:
        with open(args.batch, encoding="utf-8") as fin, open(args.out, "w", encoding="utf-8") as fout:
            for line in fin:
                row = json.loads(line)
                try:
                    c = classify(row["body"])
                    row["classification"] = c.__dict__
                except Exception as exc:
                    row["error"] = str(exc)
                fout.write(json.dumps(row, ensure_ascii=False) + "\n")
        print(f"Wrote {args.out}")
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
