# XForward — agency landing page

The landing page for **XForward**, a forward-deployed AI engineering agency
for PME (small and mid-sized businesses): a senior engineer embeds in the
client's operations, finds the costliest repetitive work, and ships AI agents
to production at a fixed price.

Single file, no build step (fonts from Google Fonts, smooth scroll from jsDelivr).
English by default with an EN/FR toggle (French copy lives in the `FR` object
in the page script), plus a light/dark toggle that remembers the choice and
otherwise follows the system setting.

What's on the page, top to bottom:

- **Intro** (once per visit): the two chevrons lock into the X, then the page
  opens like a slit. Any input skips it.
- **Hero**: the topographic map is a live WebGL2 height field. Contour lines
  ripple out from the "bottleneck" on load and bend under the cursor. Scrolling
  tilts it into 3D terrain, a path climbs to the bottleneck (day 4), then a
  chevron sweeps through, flattens it and turns the loops into forward-flowing
  chevrons (day 30). Without WebGL2 it falls back to the 2D canvas version.
  "Watch the film" opens the 20 s brand film (`media/`).
- **Model**: a statement that lights up word by word; stats land on digit reels.
- **Method**: an isometric map of a business, drawn step by step as you scroll:
  the engineer maps the desks, the bottleneck loops get priced, an agent is
  built, agents run the routes through a human-review gate, then handover.
- **Loops → Forward**: 6,500 dots (tasks) break out of their loops and stream
  forward as you scroll.
- **Use cases**: six example agent projects, each with its own animated mini-app
  scene (SMS chat, week calendar, document portal, PDF-to-ERP split view,
  helpdesk, kanban board); content lives in the `CASES` and `SCENES` objects.
- Trust band, **ROI calculator** with a break-even chart against the $12k
  deployment, pricing with hover tilt, founder card, FAQ, and a final call to
  action over flowing chevrons.

A chapter readout (bottom right, desktop) shows where you are. Smooth
scrolling via Lenis (loaded from jsDelivr; the page works without it). Under
`prefers-reduced-motion` the intro is skipped, pinned scenes become static and
all motion stops.

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
- `media/` — the brand film (`xforward-film.mp4`, 12 MB, loaded only when played) and its poster; `media/work/` — product screenshots (Datalith, RealAI)
- `og.jpg` — the 1200×630 image shown when the link is shared
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
