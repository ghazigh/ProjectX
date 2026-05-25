# ProjectX — agentic AI revenue engine

A cold-start play for turning senior agentic-AI skill into revenue with $0
capital and no audience. The bottleneck at this stage is **demand, not build** —
so the strategy front-loads proof and distribution, and the flagship build
doubles as the proof.

**Flagship: a lead-response & booking agent** for local service businesses. It's
three things at once:

1. **Proof** — a working demo you can re-skin to any prospect's business in
   minutes (you have no references yet, so you manufacture them).
2. **Delivery template** — each paying client is one config file, so per-build
   effort stays small.
3. **Product seed** — after a few bespoke installs, the config + onboarding
   becomes a self-serve product. Services fund it; the product compounds it.

## What the agent does

Replies to an inbound lead in seconds, qualifies them, captures their details,
and **books the appointment** — using real tools, not scripted replies:

- `get_availability` — real open slots from the business's hours/calendar
- `save_lead` — capture + qualify the lead so the business can follow up
- `book_appointment` — confirm a real booking (with double-book protection)
- `escalate_to_human` — hand off emergencies, out-of-scope, or "get me a person"

Everything specific to a business lives in one JSON config (`configs/`), which is
the multi-tenant / re-skin seam. The booking backend is JSON-backed for the demo
and swappable for Google Calendar / Calendly / a CRM behind the same interface.

## Quickstart

```bash
pip install -r requirements.txt
cp .env.example .env          # paste your ANTHROPIC_API_KEY
export $(grep -v '^#' .env | xargs)

# Interactive — you play the inbound lead:
python -m lead_agent.cli --config configs/sample_home_services.json

# Deterministic replay — great for recording an outbound demo video:
python -m lead_agent.cli \
    --config configs/sample_home_services.json \
    --scenario configs/sample_scenario.json \
    --fixed-date 2026-05-25
```

Get an API key at https://console.anthropic.com. For this real-time, high-volume
use case, `claude-sonnet-4-6` or `claude-haiku-4-5` is the sensible production
model (faster + cheaper) — set `LEAD_AGENT_MODEL` to switch. Default is
`claude-opus-4-7`.

## Go to market (you're starting cold)

| Doc | What |
|-----|------|
| `sales/wedge-offer.md` | The named offer, ROI math, pricing tiers, the path to $9k |
| `sales/cold-outreach.md` | The demo-led outreach motion: target → re-skin → record → send → close |

The motion in one line: re-skin the agent to a prospect's business, record a
90-second video of it booking a lead, send it as your first touch. The demo is
your credibility when you have no reviews yet.

## Project layout

```
lead_agent/
  config.py     # BusinessConfig — the per-tenant re-skin layer
  backend.py    # availability + bookings + leads store (swappable seam)
  tools.py      # tool schemas + dispatch (booking is a real side effect)
  prompts.py    # system prompt assembled from the business config
  agent.py      # manual agentic loop over the Anthropic SDK
  cli.py        # interactive + scenario-replay demo runner
configs/        # per-business configs + a demo scenario
sales/          # the wedge offer + cold-outreach playbook
content_engine/ # secondary asset: an SEO-article generator (see its README)
```

## Honest notes

- The demo runs end-to-end locally; only the live model call needs your API key.
- The booking backend is intentionally simple (JSON files). Wiring it to a real
  calendar/CRM/lead source is the first thing a paying client needs — that work
  is the seam in `backend.py`, not a rewrite.
- No tool acquires clients for you from cold. The first 1-2 take real outreach
  effort; after that, delivery is the cheap, repeatable part. That's the leverage.
- Don't mass-blast outreach — it's illegal (CAN-SPAM/CASL) and ineffective from a
  no-reputation sender. Low-volume, personalized, demo-led wins.
