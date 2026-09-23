# Forward — agency landing page

The landing page for **Forward**, a forward-deployed AI engineering agency
for PME (small and mid-sized businesses): a senior engineer embeds in the
client's operations, finds the costliest repetitive work, and ships AI agents
to production at a fixed price.

Single file, no build step, no dependencies (fonts load from Google Fonts).
French by default with an FR/EN toggle (English copy lives in the `EN` object
in the page script). Light and dark themes follow the visitor's system setting.

What's on the page: a live topographic "field map" hero with a sample mission
log, a comparison table (SaaS vs. consulting vs. hiring vs. forward-deployed),
the 5-step method with a scroll-driven progress rail, six mission types, an ROI
calculator, the three fixed-price offers, reliability commitments, founder
card, FAQ and a final call to action. Motion respects `prefers-reduced-motion`.

"Forward" is a working name. To rename, search-and-replace it in
`index.html` (title, meta, JSON-LD, header, copy and footer).

## Fill in before publishing

Open `index.html` and replace:

- `https://calendly.com/gharsallahghazi` — your Calendly / Cal.com link
- `gharsallahghazi@gmail.com` — your contact email

Then verify the founder card (`#equipe`) against what you're comfortable stating
publicly (exact PhD status, role title, and how much of your current employer to
name — see the conflict-of-interest note in `sales/agentic-ai-offer.md`).

## Deploy (GitHub Pages)

`.github/workflows/pages.yml` publishes this `website/` folder on every push to
`main` that touches it. Live at **https://ghazigh.github.io/ProjectX/**.

One-time setup: repo **Settings → Pages → Build and deployment → Source:
GitHub Actions**. Then re-run the workflow (Actions tab → "Deploy website to
GitHub Pages" → Run workflow) or push any change to `website/`.

## Preview locally

```bash
cd website && python3 -m http.server 8000   # then open http://localhost:8000
# landing page: http://localhost:8000/index.html
# insights:     http://localhost:8000/insights/
```

## Files in this folder

- `index.html` — the Forward agency landing page (served at the site root)
- `insights/` — the SEO blog: `index.html` + two cornerstone articles + `article.css`
- `sitemap.xml`, `robots.txt` — copy to your site **root** for indexing

## SEO / getting found (the inbound engine)

1. Deploy the landing page + `insights/` + `sitemap.xml` + `robots.txt`.
2. Replace `https://calendly.com/gharsallahghazi` in **every** file (landing page + all insights pages).
3. Add the site to **Google Search Console** and submit `sitemap.xml` once.
4. Expand the blog over time — see `sales/seo-content-plan.md` for the topic
   backlog and how to generate drafts with the `content_engine` in this repo.

Organic search compounds slowly (weeks-to-months) — that's the tradeoff for a
free, no-soliciting channel. Keep shipping articles; each one keeps working.

## Quick placeholder replace

```bash
# from the website/ folder, after setting your real values:
grep -rl 'https://calendly.com/gharsallahghazi' . | xargs sed -i 's|https://calendly.com/gharsallahghazi|https://cal.com/you/intro|g'
grep -rl 'gharsallahghazi@gmail.com' . | xargs sed -i 's|gharsallahghazi@gmail.com|you@example.com|g'
```
