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
# landing page: http://localhost:8000/index.html
# insights:     http://localhost:8000/insights/
```

## Files in this folder

- `index.html` — the service landing page (deploy as `work-with-me.html`)
- `insights/` — the SEO blog: `index.html` + two cornerstone articles + `article.css`
- `sitemap.xml`, `robots.txt` — copy to your site **root** for indexing

## SEO / getting found (the inbound engine)

1. Deploy the landing page + `insights/` + `sitemap.xml` + `robots.txt`.
2. Replace `{{BOOKING_LINK}}` in **every** file (landing page + all insights pages).
3. Add the site to **Google Search Console** and submit `sitemap.xml` once.
4. Expand the blog over time — see `sales/seo-content-plan.md` for the topic
   backlog and how to generate drafts with the `content_engine` in this repo.

Organic search compounds slowly (weeks-to-months) — that's the tradeoff for a
free, no-soliciting channel. Keep shipping articles; each one keeps working.

## Quick placeholder replace

```bash
# from the website/ folder, after setting your real values:
grep -rl '{{BOOKING_LINK}}' . | xargs sed -i 's|{{BOOKING_LINK}}|https://cal.com/you/intro|g'
grep -rl '{{EMAIL}}' . | xargs sed -i 's|{{EMAIL}}|you@example.com|g'
```
