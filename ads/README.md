# XForward ad campaign: HyperFrames concepts

Ad concepts, each a [HyperFrames](https://github.com/heygen-com/hyperframes)
composition (HTML + GSAP, rendered to MP4).

| | Concept | Format | Idea |
|---|---|---|---|
| A | 9:42 PM | 9:16 · 15 s | Night lead nobody answers, then the agent books it in 38 s |
| B | Hours | 1:1 · 13 s | Kinetic type: wasted hours count up, tasks crossed out |
| C | Terrain | 16:9 · 15 s | The site's topographic map rises into a 3D mountain, then flattens |
| D | Help Wanted | 9:16 · 14 s | Newspaper classified for an impossible hire, stamped "It's an AI agent" |
| E | The Receipt | 1:1 · 13 s | A receipt totals the week's wasted time in dollars, stamped "Recovered" |

Round 1 (above) was rejected as too literal. Low-res silent drafts: `drafts/round1/`.

## Round 2: premium (Apple / Stripe) x manifesto (Nike), awe-first hook

| | Concept | Format | Idea |
|---|---|---|---|
| 1 | Chrome X | 16:9 · 15 s | Glossy 3D arrows in studio light lock into the X; 4-beat manifesto |
| 2 | Tunnel | 9:16 · 14 s | Fly through a tunnel of busywork words; beat cuts; "Your people deserve better work" |
| 3 | Hours | 1:1 · 15 s | 20,000 particle "hours" trapped in circles, then streaming forward into the X |

Source: `build2.py` (Three.js scenes driven by HyperFrames `hf-seek` time, GSAP for
type) and `synth.py` (placeholder beat tracks, pure Python). Drafts with sound:
`drafts/round2/`.

## Round 3: recognition hook ("that's me"), premium craft

| | Concept | Format | Idea |
|---|---|---|---|
| 1 | 11:47 PM | 9:16 · 15 s | Night lock screen flooded with admin notifications; the agent clears them: "Go to bed." |
| 2 | Starring: You | 16:9 · 15 s | Movie credits: Receptionist: You, Night shift: You… "Time to recast." → Agent. CEO: You. |
| 3 | Sunday | 1:1 · 15 s | Admin fills every evening and Sunday; blocks fly to "Agents · 24/7": "Your Sundays. Back." |

Source: `build3.py` (GSAP + synthesized pings/whooshes/hits). Drafts: `drafts/round3/`.

## Build and render

Needs Node 22+, FFmpeg, and the HyperFrames CLI (`npm i -g hyperframes`,
then `hyperframes browser ensure`).

```bash
python3 build.py            # round 1 low-res drafts -> projects/<concept>/
python3 build2.py           # round 2 low-res drafts (Three.js + audio)
python3 build3.py           # round 3 low-res drafts (recognition hooks + audio)
python3 build.py --final    # full resolution (1080x1920, 1080x1080, 1920x1080)
cd projects/a-942pm && hyperframes render -q draft -f 24 -o ../../a.mp4
```

Each concept is authored at full design size inside a `.stage` scaled with
CSS `zoom`, so the same source renders drafts and finals. Fonts and GSAP are
bundled locally because the renderer cannot fetch from CDNs.
