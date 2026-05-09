"""
Claude-powered cold outreach agent.

Pipeline (per prospect):
    1. Web research — pull recent signals from public sources
    2. Compose — draft a hyper-personalized cold email with Claude
    3. Validate — guardrail pass to catch hallucinated facts before send
    4. Output — JSON that downstream sender (Salesforge / lemwarm) can ingest

Usage:
    python3 claude_outreach_agent.py --prospect "Jane Doe @ Acme Logistics"
    python3 claude_outreach_agent.py --batch prospects.csv --out drafts.jsonl

Author: Gamma Wira <gammawirawibowo@gmail.com>
License: MIT
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
from dataclasses import dataclass, asdict
from typing import Iterable

import anthropic  # pip install anthropic
import httpx      # pip install httpx


# ---- config ----------------------------------------------------------

CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-6")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")  # optional

# Sender persona — change to match your client's voice
SENDER_NAME = os.getenv("SENDER_NAME", "Gamma Wira")
SENDER_TITLE = os.getenv("SENDER_TITLE", "AI Automation Engineer")
SENDER_OFFER = os.getenv(
    "SENDER_OFFER",
    "I help exporters and SMBs automate their ops workflows — usually a 4 hr → 10 min reduction per task.",
)


# ---- data ------------------------------------------------------------

@dataclass
class Prospect:
    name: str
    company: str
    title: str = ""
    email: str = ""
    linkedin_url: str = ""

    @classmethod
    def parse(cls, raw: str) -> "Prospect":
        # Accepts "Name @ Company" shorthand
        if "@" in raw:
            name, company = (s.strip() for s in raw.split("@", 1))
        else:
            name, company = raw.strip(), ""
        return cls(name=name, company=company)


@dataclass
class Draft:
    prospect: Prospect
    research_notes: str
    subject: str
    body: str
    confidence: float
    flags: list[str]


# ---- step 1: research ------------------------------------------------

def research_prospect(p: Prospect) -> str:
    """Gather public signals. Stub here — wire up Firecrawl, Apollo, or LinkedIn scraper.

    Returns a short notes string for Claude to ground on.
    """
    notes = []
    notes.append(f"Prospect: {p.name}")
    if p.company:
        notes.append(f"Company: {p.company}")
    if p.title:
        notes.append(f"Title: {p.title}")
    if p.linkedin_url:
        notes.append(f"LinkedIn: {p.linkedin_url}")

    # Optional: enrich with Firecrawl (search + scrape)
    if FIRECRAWL_API_KEY and p.company:
        try:
            r = httpx.post(
                "https://api.firecrawl.dev/v1/search",
                headers={"Authorization": f"Bearer {FIRECRAWL_API_KEY}"},
                json={"query": f"{p.name} {p.company}", "limit": 3},
                timeout=30,
            )
            if r.status_code == 200:
                hits = r.json().get("data", [])
                for h in hits[:3]:
                    title = h.get("title", "").strip()
                    snippet = h.get("description", "").strip()[:200]
                    if title:
                        notes.append(f"- {title}: {snippet}")
        except Exception as exc:
            notes.append(f"(research failed: {exc})")

    return "\n".join(notes)


# ---- step 2: compose -------------------------------------------------

SYSTEM_PROMPT = """You are a senior B2B copywriter writing cold emails on behalf of a freelance AI Automation Engineer.

Rules:
- Email must be UNDER 100 words. Cold inboxes don't read past that.
- Open with a SPECIFIC observation about the prospect or their company. Never "I came across your profile".
- One concrete value claim. Not a list of services.
- One soft CTA — a question, not a demo booking.
- Tone: confident, peer-to-peer, mildly self-deprecating. Not salesy. Not formal.
- Never invent facts. If research is thin, write a more general (but still specific to industry) email.
- Output ONLY valid JSON: {"subject": "...", "body": "...", "confidence": 0-1, "flags": []}
- "flags" lists any concerns: ["thin_research", "possible_hallucination", "industry_mismatch"]
"""


def compose_email(notes: str, sender_name: str, sender_offer: str) -> dict:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    user_msg = f"""Research notes:
{notes}

Sender: {sender_name}
Offer: {sender_offer}

Draft the cold email as JSON only."""

    resp = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=600,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_msg}],
    )
    text = resp.content[0].text.strip()
    # Strip markdown fences if Claude added them
    if text.startswith("```"):
        text = text.split("```", 2)[1].lstrip("json").strip()
    return json.loads(text)


# ---- step 3: validate ------------------------------------------------

def validate_draft(draft: dict, notes: str) -> list[str]:
    """Cheap heuristic guardrail. Catches the obvious mistakes before send."""
    flags = list(draft.get("flags", []))
    body = draft.get("body", "")

    if len(body.split()) > 110:
        flags.append("too_long")
    if not draft.get("subject"):
        flags.append("missing_subject")
    if "{{" in body or "}}" in body:
        flags.append("unfilled_template")
    if "I came across" in body or "I noticed your profile" in body:
        flags.append("generic_opener")

    # Anti-hallucination: check that any quoted fact in body appears in notes
    for sentence in body.split("."):
        if "$" in sentence or "%" in sentence:
            tokens = [t.strip("$%,. ") for t in sentence.split() if "$" in t or "%" in t]
            for tok in tokens:
                if tok and tok not in notes:
                    flags.append("possible_hallucination")
                    break
    return list(dict.fromkeys(flags))


# ---- pipeline --------------------------------------------------------

def run(prospect: Prospect) -> Draft:
    notes = research_prospect(prospect)
    raw = compose_email(notes, SENDER_NAME, SENDER_OFFER)
    flags = validate_draft(raw, notes)
    return Draft(
        prospect=prospect,
        research_notes=notes,
        subject=raw["subject"],
        body=raw["body"],
        confidence=float(raw.get("confidence", 0.5)),
        flags=flags,
    )


def run_batch(prospects: Iterable[Prospect], out_path: str) -> None:
    with open(out_path, "w", encoding="utf-8") as fh:
        for p in prospects:
            try:
                draft = run(p)
                fh.write(json.dumps(asdict(draft), ensure_ascii=False) + "\n")
                print(f"[ok]  {p.name} @ {p.company}  ({draft.confidence:.2f})", file=sys.stderr)
            except Exception as exc:
                print(f"[err] {p.name}: {exc}", file=sys.stderr)
            time.sleep(1.0)  # be nice to the API


# ---- CLI -------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--prospect", help='Single prospect, e.g. "Jane Doe @ Acme"')
    ap.add_argument("--batch", help="CSV with columns name,company,title,email,linkedin_url")
    ap.add_argument("--out", default="drafts.jsonl", help="Output JSONL path for batch mode")
    args = ap.parse_args()

    if not ANTHROPIC_API_KEY:
        sys.exit("Set ANTHROPIC_API_KEY in env (or copy .env.example to .env).")

    if args.prospect:
        draft = run(Prospect.parse(args.prospect))
        print(json.dumps(asdict(draft), ensure_ascii=False, indent=2))
    elif args.batch:
        with open(args.batch, encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            prospects = [Prospect(**{k: r.get(k, "") for k in Prospect.__annotations__}) for r in reader]
        run_batch(prospects, args.out)
        print(f"Wrote {args.out}")
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
