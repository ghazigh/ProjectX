# XForward ad campaign: HyperFrames concepts

Five ad concepts, each a [HyperFrames](https://github.com/heygen-com/hyperframes)
composition (HTML + GSAP, rendered to MP4).

| | Concept | Format | Idea |
|---|---|---|---|
| A | 9:42 PM | 9:16 · 15 s | Night lead nobody answers, then the agent books it in 38 s |
| B | Hours | 1:1 · 13 s | Kinetic type: wasted hours count up, tasks crossed out |
| C | Terrain | 16:9 · 15 s | The site's topographic map rises into a 3D mountain, then flattens |
| D | Help Wanted | 9:16 · 14 s | Newspaper classified for an impossible hire, stamped "It's an AI agent" |
| E | The Receipt | 1:1 · 13 s | A receipt totals the week's wasted time in dollars, stamped "Recovered" |

Low-res silent drafts of round 1 are in `drafts/`.

## Build and render

Needs Node 22+, FFmpeg, and the HyperFrames CLI (`npm i -g hyperframes`,
then `hyperframes browser ensure`).

```bash
python3 build.py            # low-res drafts  -> projects/<concept>/
python3 build.py --final    # full resolution (1080x1920, 1080x1080, 1920x1080)
cd projects/a-942pm && hyperframes render -q draft -f 24 -o ../../a.mp4
```

Each concept is authored at full design size inside a `.stage` scaled with
CSS `zoom`, so the same source renders drafts and finals. Fonts and GSAP are
bundled locally because the renderer cannot fetch from CDNs.
