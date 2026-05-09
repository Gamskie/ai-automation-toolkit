# ai-automation-toolkit

A small open-source kit of starters I'm building from as I learn AI / LLM workflow automation.

Maintained by [Gamma Wira](https://linkedin.com/in/gammawira) — marketing & export ops by day, Python on the side, Bandung, Indonesia.

> Honest scope: these are starter scripts I've built to learn patterns, not battle-tested production systems running for clients. They're the foundation I'll be forking from when I take on automation work. Forks and PRs welcome.

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

I'm pivoting from Marketing & Export Specialist into AI / automation work. Most public AI-automation code is either toy demos or locked behind agencies. This repo is what I wished I'd found when I started — small, readable, and meant to be forked.

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

I'd like to do automation work for SMBs and exporters who have a workflow that lives in Excel + email + a vendor portal. If that sounds like your team, message me on LinkedIn or email.

📧 gammawirawibowo@gmail.com  
🔗 [linkedin.com/in/gammawira](https://linkedin.com/in/gammawira)  
🌐 [gamskie.github.io/gammawira-portfolio](https://gamskie.github.io/gammawira-portfolio/)

## License

MIT — use it, modify it, ship with it. A link back is appreciated but not required.
