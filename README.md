# ai-automation-toolkit

Open-source building blocks for AI lead & revenue automation — prospect research, AI-drafted replies, inbound reply classification, follow-up logic.

Maintained by [Gamma Wira](https://linkedin.com/in/gammawira) — I build AI systems that stop businesses from losing leads. Bandung, Indonesia.

> Honest scope: these are starter scripts that show the patterns, not a finished product. They're the same building blocks I assemble into a full AI Lead Rescue System for clients. Forks and PRs welcome.

---

## What's inside

```
ai-automation-toolkit/
├── python/
│   ├── claude_outreach_agent.py     # Multi-step prospect research + cold email drafting (Claude API)
│   ├── document_parser.py            # Parse Excel/Word templates with prefer_below logic for IPL-style workflows
│   ├── reply_classifier.py           # Classify inbound replies: interested / objection / not now / unsubscribe
│   ├── holiday_aware_dates.py        # Holiday-aware shipment date math across multi-port routes
│   ├── claude_email_composer.py      # Carrier-routing-aware email drafting with schema validation
│   └── requirements.txt
├── typescript/
│   ├── mastra_outreach_agent.ts      # Mastra + Claude SDK outreach agent
│   └── package.json
├── n8n-workflows/
│   ├── lead-research-agent.json      # Lead enrichment via Firecrawl + Claude
│   ├── email-classifier.json         # Inbound reply classification + routing
│   └── inbound-reply-classifier.json # Gmail trigger → Claude Haiku → Slack routing
├── examples/
│   └── shipment_date_compute.py      # Holiday-aware shipment date logic
├── .env.example
└── README.md
```

## Why this exists

I build AI Lead Rescue Systems for service businesses — the systems that make sure no inquiry gets answered too slowly or dropped before it closes. Most public AI-automation code is either toy demos or locked behind agencies. This repo is what I wished I'd found when I started — small, readable, and meant to be forked.

If something here saves you an hour, that's the point.

## Quick start

```bash
git clone https://github.com/Gamskie/ai-automation-toolkit.git
cd ai-automation-toolkit/python
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp ../.env.example ../.env  # fill in your keys
python3 claude_outreach_agent.py --prospect "Jane Doe @ Acme Logistics"
```

## Working with me

I build AI Lead Rescue Systems for service businesses — agencies, consultants, contractors, clinics, studios. If your team loses leads to slow replies or dropped follow-up, message me on LinkedIn or email.

📧 gammawirawibowo@gmail.com
🔗 [linkedin.com/in/gammawira](https://linkedin.com/in/gammawira)
🌐 [gamskie.github.io/gammawira-portfolio](https://gamskie.github.io/gammawira-portfolio/)

## License

MIT — use it, modify it, ship with it. A link back is appreciated but not required.
