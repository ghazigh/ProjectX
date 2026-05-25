# SEO content plan — the inbound engine

Organic search is your "they find me and reach out" channel. It compounds: each
article keeps pulling buyers for years. Two cornerstone pieces are already live
in `website/insights/`. This is the backlog to expand it.

Target **buyer-intent** queries (people evaluating a build), not generic
"what is an AI agent" traffic. Aim for ~1 quality article every 1-2 weeks.

## Backlog (buyer-intent topics)

1. "How to hire an agentic AI developer (and what to look for)"
2. "Agentic AI for financial services: where it pays off and where it doesn't"
3. "Build vs. buy: when to use an off-the-shelf AI tool vs. a custom agent"
4. "How to evaluate an AI agent before you trust it in production"
5. "AI agent security: what to lock down before you ship"
6. "Signs your AI proof-of-concept will never make it to production"
7. "What a good agentic AI audit actually delivers"
8. "RAG vs. agents: which does your problem actually need?"
9. "How much does it cost to run an AI agent per month?"
10. "Agentic AI for operations teams: the highest-ROI first projects"

## Generate drafts with the content engine (in this repo)

The `content_engine` produces an SEO-structured draft + scorecard:

```bash
export ANTHROPIC_API_KEY=sk-ant-...
python -m content_engine.cli "How to hire an agentic AI developer" \
    --keyword "hire agentic AI developer" \
    --secondary "AI agent development,agentic AI consultant" \
    --words 1400 --tone "authoritative, plain-English, senior" \
    --audience "founders and ops leaders evaluating an AI build"
```

Then: edit and **fact-check** the draft (it's a starting point, never publish
raw), and paste the body into a copy of one of the existing article HTML files
in `website/insights/` (they're your template — update title, meta, canonical,
the JSON-LD `headline`, and add the new post to `insights/index.html`).

## Rules that keep it working

- **Edit everything.** AI drafts get you 70% there; your expertise and real
  examples are what make it rank and convert. Add specifics only you know.
- **One clear CTA per article** → the booking link (already in the template).
- **Link articles to each other** and to `work-with-me.html`.
- **Submit your sitemap** to Google Search Console once (`website/sitemap.xml`)
  so indexing starts; then it's hands-off.
- Be patient: organic takes weeks-to-months to rank. That's the tradeoff you
  chose by going free + no-soliciting. It compounds — keep shipping.
