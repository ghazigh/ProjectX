# Service landing page

A self-contained, buyer-facing landing page for the agentic-AI service offering.
Matches your existing site's editorial brand (Fraunces / Newsreader / JetBrains
Mono) but is positioned to convert clients, not impress academics.

Single file, no build step, no dependencies (fonts load from Google Fonts).

## Fill in before publishing

Open `index.html` and replace:

- `{{BOOKING_LINK}}` — your Calendly / Cal.com link
- `{{EMAIL}}` — your contact email

Then verify the `§ 03 — Why me` section against what you're comfortable stating
publicly (exact PhD status, role title, and how much of your current employer to
name — see the conflict-of-interest note in `sales/agentic-ai-offer.md`).

## Deploy options

**A. As a page on your existing site** (recommended — keeps your research site intact):

```bash
# from a clone of your github.io repo:
cp /path/to/ProjectX/website/index.html ./work-with-me.html
git add work-with-me.html && git commit -m "Add agentic AI services page" && git push
# live at https://ghazigh.github.io/work-with-me.html
```

Then link to it from your main site's nav ("Work with me") and from your
LinkedIn profile + posts.

**B. As its own domain** — drop `index.html` on Netlify/Cloudflare Pages/Vercel
and point a domain at it (e.g. an `agentic-` subdomain). Cleaner separation
between "researcher" and "vendor" identities.

## Preview locally

```bash
cd website && python3 -m http.server 8000   # then open http://localhost:8000
```
