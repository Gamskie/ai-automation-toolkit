# AI Automation Toolkit

Production-ready building blocks for AI workflow automation — the kind that actually save SMBs and exporters real hours every week.

Maintained by [Gamma Wira](https://linkedin.com/in/gammawira) · AI Automation Engineer · Bandung, Indonesia.

> 🔧 Real code from real production systems, sanitized into reusable starters.
> Not tutorials. Not "hello world." Pieces I keep reaching for.

---

## What's inside

```
ai-automation-toolkit/
├── python/
│   ├── claude_outreach_agent.py     # Multi-step prospect research + cold email drafting (Claude API)
│   ├── document_parser.py            # Parse Excel/Word/PDF templates with prefer_below logic for IPL workflows
│   ├── reply_classifier.py           # Classify inbound replies: interested / objection / not now / unsubscribe
│   └── requirements.txt
├── n8n-workflows/
│   ├── lead-research-agent.json      # End-to-end lead enrichment via Firecrawl + Claude
│   └── email-classifier.json         # Inbound reply classification + routing
├── examples/
│   └── shipment_date_compute.py      # Holiday-aware shipment date logic (real exporter use case)
├── .env.example
└── README.md
```

## Why this exists

I'm building in public as I pivot from Marketing & Export Specialist to AI Automation Engineer. Most "AI automation" code online is either toy demos or locked behind agencies. This repo is what I'd hand a junior engineer if I needed them to ship a real workflow on day one.

If something here saves you an afternoon, that's the goal.

## Quick start

```bash
git clone https://github.com/Gamskie/ai-automation-toolkit.git
cd ai-automation-toolkit/python
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # fill in your keys
python3 claude_outreach_agent.py --prospect "John Doe @ Acme Logistics"
```

## Hire me

I build this stuff for clients full-time:

- **Shipment & ops automation** for exporters / importers (saving 4 hrs → 10 min per booking is my benchmark)
- **AI sales outreach agents** (lead research, hyper-personalized email, reply handling)
- **Custom n8n / Mastra / Python orchestrators** for SMBs drowning in copy-paste

📧 gammawirawibowo@gmail.com
🔗 linkedin.com/in/gammawira

## License

MIT — use it, modify it, ship with it. A link back is appreciated but not required.
