# XForward — agency landing page

The landing page for **XForward**, a forward-deployed AI engineering agency
for PME (small and mid-sized businesses): a senior engineer embeds in the
client's operations, finds the costliest repetitive work, and ships AI agents
to production at a fixed price.

Single file, no build step (fonts from Google Fonts, smooth scroll from jsDelivr).
English by default with an EN/FR toggle (French copy lives in the `FR` object
in the page script), plus a light/dark toggle that remembers the choice and
otherwise follows the system setting.

What's on the page: a full-bleed topographic hero pinned to the scroll: the
terrain tilts into 3D, the "bottleneck" peak rises, then flattens as the sample
mission reaches day 30. Then a statement that lights up word by word, a
horizontally-scrolling 5-step method, an industry use-case explorer (six
example agent projects, each with an animated agent-run trace; content lives in
the `CASES` object in the script), a trust band, an ROI calculator, pricing
with hover tilt, founder card, FAQ and a final call to action. Smooth scrolling
via Lenis (loaded from jsDelivr; the page works without it). All motion is
disabled under `prefers-reduced-motion`.

The logo is two forward arrows that connect into an X on load and open back
to `>>` on hover. To rename the agency, search-and-replace the name in
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
GitHub Actions**. `main` must also be the repo's default branch (Settings →
General), because the `github-pages` environment only accepts deploys from it. Then re-run the workflow (Actions tab → "Deploy website to
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
