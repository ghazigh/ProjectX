# Content Engine (secondary asset)

A working SEO-article generator: topic + keyword → publish-ready draft (title,
meta, slug, body, FAQ, link ideas) plus a local on-page SEO scorecard. Built on
Claude with structured output.

It's kept here as a reusable asset / smaller revenue stream. The repo's primary
project is the **lead-response & booking agent** (see the root `README.md`).

## Run

```bash
pip install -r ../requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...   # or use the repo .env
python -m content_engine.cli "How to compost at home" \
    --keyword "home composting" \
    --secondary "compost bin,kitchen scraps" \
    --words 1500 --tone "friendly, practical" --audience "beginner gardeners"
```

Output lands in `output/<slug>.md`. **Always edit and fact-check before
delivering** — AI drafts are a starting point; verify every claim and insert
real sources. The tool flags where to cite; it never fabricates citations.

## Files

- `prompts.py` — cached system prompt, JSON response schema, brief builder
- `pipeline.py` — Anthropic SDK call (streamed), cost estimation
- `seo.py` — local on-page SEO scorecard (no API calls)
- `cli.py` — command-line entry + markdown rendering
