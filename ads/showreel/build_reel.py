"""CLAUDE — Showreel 2026: a 15 s motion-design reel for HyperFrames.

One orange dot travels through eight disciplines, one bar of 128 BPM each:
principles, typography, geometry, 3D, particles, shaders, editing, title.
DOM shots are GSAP; 3D/particles/shaders are one Three.js canvas with a
hand-written bloom/tonemap pass, driven by HyperFrames' `hf-seek` time.

  python3 build_reel.py            draft (zoom 0.5 -> 960x540)
  python3 build_reel.py --zoom 1   full HD
  python3 build_reel.py --measure  zoom-1 layout pass -> measure.json
"""
import json, math, os, random, shutil, struct, subprocess, sys, zlib

HERE = os.path.dirname(os.path.abspath(__file__))
ADS = os.path.dirname(HERE)
SCRATCH = os.path.dirname(ADS)
DIST = os.path.join(ADS, "vendor", "gsap")                     # GSAP 3.14.2 bonus plugins
MB_SNIPPET = os.path.join(ADS, "vendor", "motion-blur.html")   # HyperFrames registry: motion-blur
MEASURE = "--measure" in sys.argv
ZOOM = 1.0 if MEASURE else float(sys.argv[sys.argv.index("--zoom") + 1]) if "--zoom" in sys.argv else 0.5
OUT = os.path.join(ADS, "projects", "showreel-measure" if MEASURE else "showreel")

W, H, DUR = 1920, 1080, 15.0
PLUGINS = ["CustomEase", "CustomWiggle", "DrawSVGPlugin"]
FONTS = open(os.path.join(ADS, "fonts", "fonts.css")).read().replace("../fonts/", "fonts/")


# ---------------------------------------------------------------- assets
def png_noise(path, n=256, seed=7):
    r = random.Random(seed)
    raw = b"".join(b"\x00" + bytes(r.randrange(256) for _ in range(n)) for _ in range(n))

    def chunk(t, d):
        return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)

    with open(path, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", n, n, 8, 0, 0, 0, 0))
                + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))


# ---------------------------------------------------------------- shape morph targets
NS = 48  # samples every 7.5 deg: every corner below sits exactly on a sample


def ray(poly, th):
    dx, dy, best = math.cos(th), math.sin(th), 0.0
    for (x1, y1), (x2, y2) in zip(poly, poly[1:] + poly[:1]):
        ex, ey = x2 - x1, y2 - y1
        det = -dx * ey + ex * dy
        if abs(det) < 1e-12:
            continue
        s = (-x1 * ey + ex * y1) / det
        u = (dx * y1 - dy * x1) / det
        if s > 0 and -1e-9 <= u <= 1 + 1e-9:
            best = max(best, s)
    return best


def num(v):
    """Compact number: GSAP reads the trailing zeros of '50.00%' as part of the unit."""
    t = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if t in ("-0", "") else t


def polar(rf):
    pts = []
    for k in range(NS):
        th = 2 * math.pi * k / NS - math.pi / 2
        r = rf(th)
        pts.append(f"{num(50 + r * math.cos(th))}% {num(50 + r * math.sin(th))}%")
    return "polygon(" + ", ".join(pts) + ")"


def reg(n, R, a0):
    return [(R * math.cos(math.radians(a0 + 360 * i / n)), R * math.sin(math.radians(a0 + 360 * i / n))) for i in range(n)]


def star(n, ro, ri, a0):
    return [((ro if i % 2 == 0 else ri) * math.cos(math.radians(a0 + 180 * i / n)),
             (ro if i % 2 == 0 else ri) * math.sin(math.radians(a0 + 180 * i / n))) for i in range(2 * n)]


L_, w_ = 43.0, 43.0 * math.tan(math.radians(22.5))
PLUS = [(L_, w_), (w_, w_), (w_, L_), (-w_, L_), (-w_, w_), (-L_, w_), (-L_, -w_), (-w_, -w_), (-w_, -L_), (w_, -L_), (w_, -w_), (L_, -w_)]
SHAPES = {
    "circle": polar(lambda th: 36.0),
    "square": polar(lambda th: ray(reg(4, 44.5, 45), th)),
    "tri": polar(lambda th: ray(reg(3, 47.0, -90), th)),
    "star": polar(lambda th: ray(star(4, 49.0, 14.0, -90), th)),
    "plus": polar(lambda th: ray(PLUS, th)),
    "dot": polar(lambda th: 6.0),
}


# ---------------------------------------------------------------- DOM
def s1_html():
    ticks = "".join(f'<i class="tick" style="left:{x}px"></i>' for x in range(280, 1650, 40))
    ghosts = "".join('<i class="gh"></i>' for _ in range(15))
    drops = "".join(f'<i class="drop" style="width:{s}px;height:{s}px;margin:-{s/2}px 0 0 -{s/2}px"></i>'
                    for s in (14, 10, 18, 8, 12, 16, 9, 11))
    labs = [("01", "ANTICIPATION", 470, 752), ("02", "ARC", 640, 150), ("03", "SQUASH", 905, 752),
            ("04", "STRETCH", 1195, 330), ("05", "FOLLOW-THROUGH", 1290, 752)]
    lab = "".join(f'<div class="lab" id="lab{i}" style="left:{x}px;top:{y}px"><b>{n}</b>{t}</div>' for i, (n, t, x, y) in enumerate(labs))
    return f"""
<section id="s1" class="clip shot" data-start="0" data-duration="1.875">
  <div id="floor"></div>{ticks}
  {ghosts}
  <i class="ring" id="ring1"></i>
  <div id="ball" class="ball" data-hf-motion-blur='{{"samplesPerFrame":12}}'></div>
  {drops}
  {lab}
  <div id="bar"></div>
</section>"""


def s2_html():
    def chars(word, cls="c"):
        return "".join(f'<span class="{cls}">{ch}</span>' for ch in word)
    return f"""
<section id="s2" class="clip shot" data-start="1.875" data-duration="1.875">
  <div id="s2z">
    <div id="field" style="--hr:-2px"></div>
    <div class="ln" id="l1" style="--wd:125"><span class="mk">{chars('TYPE')}</span></div>
    <div class="ln" id="l2"><span class="w">Time</span><span class="w e e3">Time</span><span class="w e e2">Time</span><span class="w e e1">Time</span></div>
    <div class="ln" id="l3"><span class="mk">{chars('RHYTHM')}</span></div>
    <div class="ln" id="l4"><span class="f">F</span><span class="oslot"><svg id="ring4" viewBox="0 0 182 182"><circle id="ringc" cx="91" cy="91" r="69"/></svg></span><span class="rm">RM</span></div>
    <i class="rule" style="top:272px"></i><i class="rule" style="top:512px"></i><i class="rule" style="top:752px"></i><i class="rule" style="top:992px"></i>
    <div class="cap" style="top:236px">01 · Variable axis — wdth <span id="wdv">125</span></div>
    <div class="cap" style="top:476px">02 · Echo — 3 × 45 ms</div>
    <div class="cap" style="top:716px">03 · Stagger — 30 ms</div>
    <div class="cap" style="top:956px">04 · Geometry — ⌀ 182</div>
  </div>
</section>"""


def s3_html():
    cells = "".join(f'<i class="sh" style="left:{(i % 16) * 120}px;top:{(i // 16) * 120}px"></i>' for i in range(144))
    return f"""
<section id="s3" class="clip shot" data-start="3.28" data-duration="2.345">
  <div id="grid">{cells}</div>
</section>
<div id="bigc" class="clip" data-start="5.2" data-duration="0.6"></div>"""


def spiral_path(cx, cy, turns=5.5, r0=6, r1=470, n=420):
    pts = []
    for i in range(n + 1):
        p = i / n
        th = p * turns * 2 * math.pi
        r = r0 + (r1 - r0) * p
        pts.append(f"{cx + r * math.cos(th):.1f},{cy + r * math.sin(th):.1f}")
    return "M" + " L".join(pts)


def s7_html():
    h = 0.234375
    t0 = 11.25
    reel = "".join(f"<b>{d % 10}</b>" for d in range(20))
    tiles = "".join(f'<div class="tile" style="left:{(i % 8) * 240}px;top:{(i // 8) * 270}px"><i class="fa"></i><i class="fb"></i></div>'
                    for i in range(32))
    glitch_slices = "".join(f'<div class="sl" style="clip-path:inset({k * 100 / 7:.2f}% 0 {100 - (k + 1) * 100 / 7:.2f}% 0)">GLITCH</div>'
                            for k in range(7))
    ring_txt = "MOTION DESIGN · MOTION DESIGN · MOTION DESIGN · "
    ring2 = "IN CODE · IN CODE · IN CODE · IN CODE · "
    return f"""
<section id="s7a" class="clip shot" data-start="{t0}" data-duration="{h:.6f}">
  <div class="strip" data-hf-motion-blur='{{"samplesPerFrame":48,"shutterAngle":360,"shutterPhase":-180}}' style="left:0;background:var(--or);color:var(--ink)"><span>E</span></div>
  <div class="strip" data-hf-motion-blur='{{"samplesPerFrame":48,"shutterAngle":360,"shutterPhase":-180}}' style="left:480px;background:var(--bone);color:var(--ink)"><span>D</span></div>
  <div class="strip" data-hf-motion-blur='{{"samplesPerFrame":48,"shutterAngle":360,"shutterPhase":-180}}' style="left:960px;background:var(--co);color:var(--bone)"><span>I</span></div>
  <div class="strip" data-hf-motion-blur='{{"samplesPerFrame":48,"shutterAngle":360,"shutterPhase":-180}}' style="left:1440px;background:var(--ink);color:var(--or)"><span>T</span></div>
</section>
<section id="s7b" class="clip shot" data-start="{t0 + h:.6f}" data-duration="{h:.6f}">
  <svg id="spsvg" viewBox="0 0 1920 1080"><path id="sp1" d="{spiral_path(960, 540)}"/><path id="sp2" d="{spiral_path(960, 540, 5.5, 6, 470, 420)}" transform="rotate(180 960 540)"/></svg>
  <i class="cdot"></i>
</section>
<section id="s7c" class="clip shot" data-start="{t0 + 2 * h:.6f}" data-duration="{h:.6f}">
  <div class="digits"><div class="dg"><div class="reel" id="r1">{reel}</div></div><div class="dg"><div class="reel" id="r2">{reel}</div></div><div class="dg"><div class="reel" id="r3">{reel}</div></div></div>
  <div class="bpm mono">BPM</div>
</section>
<section id="s7d" class="clip shot" data-start="{t0 + 3 * h:.6f}" data-duration="{h:.6f}">
  <div class="gw"><div class="sl rgbR">GLITCH</div><div class="sl rgbB">GLITCH</div>{glitch_slices}</div>
</section>
<section id="s7e" class="clip shot" data-start="{t0 + 4 * h:.6f}" data-duration="{h:.6f}">
  <div class="tiles">{tiles}</div>
</section>
<section id="s7f" class="clip shot" data-start="{t0 + 5 * h:.6f}" data-duration="{h:.6f}">
  <svg id="ct1" class="ct" viewBox="0 0 1000 1000"><defs><path id="c1p" d="M500,500 m-380,0 a380,380 0 1,1 760,0 a380,380 0 1,1 -760,0"/></defs><text><textPath href="#c1p">{ring_txt}</textPath></text></svg>
  <svg id="ct2" class="ct ct2" viewBox="0 0 1000 1000"><defs><path id="c2p" d="M500,500 m-250,0 a250,250 0 1,1 500,0 a250,250 0 1,1 -500,0"/></defs><text><textPath href="#c2p">{ring2}</textPath></text></svg>
  <i class="cdot"></i>
</section>
<section id="s7g" class="clip shot num" data-start="12.65625" data-duration="0.1171875" style="background:var(--ink);color:var(--bone)"><span id="n3">3</span></section>
<section id="s7h" class="clip shot num" data-start="12.7734375" data-duration="0.1171875" style="background:var(--bone);color:var(--ink)"><span id="n2">2</span></section>
<section id="s7i" class="clip shot num" data-start="12.890625" data-duration="0.1171875" style="background:var(--or);color:var(--ink)"><span id="n1">1</span></section>
<section id="s7j" class="clip shot" data-start="13.0078125" data-duration="0.1171875" style="background:#000"></section>"""


def s8_html():
    letters = "".join(f'<span class="nl">{c}</span>' for c in "CLAUDE")
    plain = "".join(f'<span class="nl">{c}</span>' for c in "CLAUDE")
    return f"""
<section id="s8" class="clip shot" data-start="13.125" data-duration="1.875">
  <div id="s8in">
    <div id="name" style="--wd:112">{letters}<span id="pslot"></span></div>
    <div id="shine" style="--wd:112">{plain}<span class="pslot"></span></div>
    <div id="role"><span>Motion Designer</span></div>
    <i id="rule8"></i>
    <div id="skills" class="mono">Showreel 2026 — Type · Shape · 3D · Particles · Shaders · Edit</div>
    <div id="credit" class="mono">Every frame made in code · HyperFrames · GSAP · Three.js · GLSL</div>
    <i id="ring8"></i>
    <div id="dot8"></div>
  </div>
</section>"""


HUD = """
<div id="hud" class="mono">
  <div class="h tl">Claude <span class="dim">—</span> Showreel ’26</div>
  <div class="h tr"><i class="rec"></i><span id="tc">00:00:00:00</span></div>
  <div class="h bl"><span id="shotn">01</span><span class="dim">/08</span><span id="shotl">PRINCIPLES</span></div>
  <div class="h br">""" + "".join('<i class="seg"><i></i></i>' for _ in range(8)) + """</div>
</div>"""

CSS = r"""
:root{--ink:#0A0A0C;--bone:#EFEBE3;--or:#FF5A1F;--co:#2B3BFF}
html,body{margin:0;background:#000}
#root{position:relative;width:100%;height:100%;overflow:hidden;background:#0A0A0C}
.stage{position:absolute;left:0;top:0;width:1920px;height:1080px;overflow:hidden;font-family:'Archivo',sans-serif;color:var(--bone)}
#gl{position:absolute;left:0;top:0;width:1920px;height:1080px;display:block;z-index:1}
.shot{position:absolute;left:0;top:0;width:1920px;height:1080px;overflow:hidden}
.mono{font-family:'IBM Plex Mono',monospace;text-transform:uppercase;letter-spacing:.16em}
/* 01 principles */
#s1{background:var(--ink);z-index:5}
#floor{position:absolute;left:260px;top:699px;width:1400px;height:2px;background:var(--bone)}
.tick{position:absolute;top:714px;width:1px;height:10px;background:rgba(239,235,227,.4);transform-origin:50% 0}
.gh{position:absolute;left:-55px;top:-55px;width:110px;height:110px;border-radius:50%;border:1.5px solid rgba(239,235,227,.7);box-sizing:border-box;opacity:0}
.ball{position:absolute;left:-55px;top:-55px;width:110px;height:110px;border-radius:50%;background:var(--or)}
.ring{position:absolute;left:505px;top:590px;width:110px;height:110px;border-radius:50%;border:2px solid var(--bone);box-sizing:border-box;opacity:0}
.drop{position:absolute;left:0;top:0;border-radius:50%;background:var(--or);opacity:0}
.lab{position:absolute;font:500 15px/1 'IBM Plex Mono',monospace;letter-spacing:.2em;color:rgba(239,235,227,.8);white-space:nowrap;clip-path:inset(0 100% 0 0)}
.lab b{color:var(--or);font-weight:600;margin-right:12px}
#bar{position:absolute;left:0;top:693px;width:1920px;height:14px;background:var(--or);transform-origin:1360px 50%;transform:scaleX(0)}
/* 02 typography */
#s2{z-index:6}
#s2z{position:absolute;left:0;top:0;width:1920px;height:1080px}
#field{position:absolute;left:0;top:0;width:1920px;height:1080px;background:var(--or);
  -webkit-mask-image:radial-gradient(circle at var(--ox) var(--oy),transparent var(--hr),#000 calc(var(--hr) + 1.5px));
  mask-image:radial-gradient(circle at var(--ox) var(--oy),transparent var(--hr),#000 calc(var(--hr) + 1.5px))}
.ln{position:absolute;left:104px;line-height:1;white-space:nowrap;color:var(--ink)}
.mk{display:inline-block;overflow:hidden;vertical-align:top}
.mk .c{display:inline-block}
#l1{top:44px;font-size:250px;font-weight:900;font-variation-settings:'wdth' var(--wd)}
#l2{top:262px;font:italic 400 300px/1 'Instrument Serif',serif;letter-spacing:-.01em}
#l2 .w{display:inline-block}
#l2 .e{position:absolute;left:0;top:0;color:transparent;-webkit-text-stroke:2px var(--ink)}
#l3{top:524px;font-size:250px;font-weight:900;font-variation-settings:'wdth' 72}
#l3 .c{--w:900;font-variation-settings:'wdth' 72,'wght' var(--w)}
#l4{top:764px;font-size:250px;font-weight:900;font-variation-settings:'wdth' 100}
#l4 .f,#l4 .rm{display:inline-block}
.oslot{display:inline-block;width:182px;height:182px;margin:0 10px -3px 14px;position:relative}
#ring4{position:absolute;left:0;top:0;width:182px;height:182px;overflow:visible}
#ringc{fill:none;stroke:var(--ink);stroke-width:44;transform:rotate(-90deg);transform-origin:91px 91px}
.rule{position:absolute;left:104px;width:1712px;height:2px;background:var(--ink);transform-origin:0 50%;transform:scaleX(0)}
.cap{position:absolute;right:104px;font:500 15px/1 'IBM Plex Mono',monospace;letter-spacing:.16em;text-transform:uppercase;color:var(--ink);clip-path:inset(0 100% 0 0)}
/* 03 geometry */
#s3{background:var(--bone);z-index:4}
#grid{position:absolute;left:0;top:0;width:1920px;height:1080px;transform-origin:50% 50%}
.sh{position:absolute;width:120px;height:120px;background:var(--ink);clip-path:%%CIRCLE%%}
#bigc{position:absolute;left:710px;top:290px;width:500px;height:500px;border-radius:50%;background:var(--or);z-index:7}
/* 07 edit */
#s7a,#s7b,#s7c,#s7d,#s7e,#s7f,#s7g,#s7h,#s7i,#s7j{z-index:8}
.strip{position:absolute;top:0;width:480px;height:1080px;overflow:hidden;display:flex;align-items:center;justify-content:center}
.strip span{font:900 860px/1 'Archivo';font-variation-settings:'wdth' 62;display:block;margin-top:-40px}
#s7b{background:var(--ink)}
#spsvg{position:absolute;left:0;top:0;width:1920px;height:1080px}
#sp1{fill:none;stroke:var(--or);stroke-width:16;stroke-linecap:round}
#sp2{fill:none;stroke:var(--bone);stroke-width:5;stroke-linecap:round}
.cdot{position:absolute;left:930px;top:510px;width:60px;height:60px;border-radius:50%;background:var(--or)}
#s7c{background:var(--bone);color:var(--ink)}
.digits{position:absolute;left:330px;top:300px;display:flex;gap:10px}
.dg{width:390px;height:480px;overflow:hidden}
.reel b{display:block;height:480px;font:900 600px/480px 'Archivo';font-variation-settings:'wdth' 80;text-align:center}
.bpm{position:absolute;left:1560px;top:650px;font-size:48px;font-weight:600;letter-spacing:.3em}
#s7d{background:var(--ink)}
.gw{position:absolute;left:0;top:340px;width:1920px;height:400px}
.gw .sl{position:absolute;left:0;top:0;width:1920px;text-align:center;font:900 330px/400px 'Archivo';font-variation-settings:'wdth' 118;color:var(--bone);letter-spacing:-.02em}
.gw .rgbR{color:#ff2a2a;mix-blend-mode:screen;opacity:.9}
.gw .rgbB{color:#2a6bff;mix-blend-mode:screen;opacity:.9}
#s7e{background:var(--ink)}
.tiles{position:absolute;inset:0;perspective:1400px}
.tile{position:absolute;width:240px;height:270px;transform-style:preserve-3d}
.tile i{position:absolute;inset:6px;backface-visibility:hidden}
.tile .fa{background:var(--co)}
.tile .fb{background:var(--or);transform:rotateY(180deg)}
#s7f{background:var(--bone)}
.ct{position:absolute;left:460px;top:40px;width:1000px;height:1000px}
.ct text{font:800 66px 'Archivo';font-variation-settings:'wdth' 100;fill:var(--ink);letter-spacing:.06em}
.ct2 text{font-size:52px;fill:var(--or)}
.num{display:flex;align-items:center;justify-content:center}
.num span{display:block;font:900 900px/1 'Archivo';font-variation-settings:'wdth' 90;margin-top:-60px}
/* 08 title */
#s8{background:var(--ink);z-index:8}
#s8in{position:absolute;inset:0}
#name{position:absolute;left:0;right:0;top:300px;text-align:center;font-size:232px;font-weight:800;line-height:1;letter-spacing:-.015em;white-space:nowrap;font-variation-settings:'wdth' var(--wd)}
#name .nl{display:inline-block}
#pslot,.pslot{display:inline-block;width:62px;height:10px;margin-left:10px}
#shine{position:absolute;left:0;right:0;top:300px;text-align:center;font-size:232px;font-weight:800;line-height:1;letter-spacing:-.015em;white-space:nowrap;font-variation-settings:'wdth' var(--wd);color:transparent;background:linear-gradient(104deg,transparent 42%,rgba(255,244,230,.95) 50%,transparent 58%);background-size:320% 100%;background-position:100% 0;-webkit-background-clip:text;background-clip:text;opacity:0}
#shine .nl{display:inline-block}
#dot8{position:absolute;left:931px;top:511px;width:58px;height:58px;border-radius:50%;background:var(--or)}
#ring8{position:absolute;left:910px;top:490px;width:100px;height:100px;border-radius:50%;border:2px solid var(--bone);box-sizing:border-box;opacity:0}
#role{position:absolute;left:0;right:0;top:596px;text-align:center;font:italic 400 84px/1.1 'Instrument Serif',serif;color:var(--bone);overflow:hidden}
#role span{display:inline-block}
#rule8{position:absolute;left:660px;top:742px;width:600px;height:1px;background:rgba(239,235,227,.5);transform:scaleX(0)}
#skills{position:absolute;left:0;right:0;top:776px;text-align:center;font-size:19px;font-weight:600;color:var(--bone)}
#credit{position:absolute;left:0;right:0;top:822px;text-align:center;font-size:14px;color:rgba(239,235,227,.6);opacity:0}
/* finishing */
#flash{position:absolute;inset:0;background:#fff;opacity:0;z-index:20}
#vig{position:absolute;inset:0;background:radial-gradient(ellipse 72% 72% at 50% 50%,transparent 58%,rgba(0,0,0,.34) 100%);opacity:0;z-index:21}
#grain{position:absolute;inset:0;background:url(noise.png);background-size:512px 512px;image-rendering:pixelated;mix-blend-mode:overlay;opacity:0;z-index:22}
#hud{position:absolute;inset:0;z-index:30;color:var(--bone);font-size:15px;font-weight:500;letter-spacing:.2em}
#hud .h{position:absolute;white-space:nowrap}
#hud .tl{left:56px;top:44px}#hud .tr{right:56px;top:44px}#hud .bl{left:56px;bottom:44px}#hud .br{right:56px;bottom:48px;display:flex;gap:6px}
#hud .dim{opacity:.45;margin:0 .5em}
#hud #shotl{margin-left:.9em}
#hud .rec{display:inline-block;width:9px;height:9px;border-radius:50%;background:var(--or);margin-right:12px;vertical-align:1px}
#hud .seg{display:block;width:34px;height:3px;background:currentColor;opacity:.9;position:relative}
#hud .seg::before{content:'';position:absolute;inset:0;background:currentColor;opacity:.25}
#hud .seg{background:transparent}
#hud .seg i{position:absolute;left:0;top:0;width:100%;height:100%;background:currentColor;transform-origin:0 50%;transform:scaleX(0)}
"""

TL_JS = r"""
gsap.registerPlugin(CustomEase, CustomWiggle, DrawSVGPlugin);
CustomWiggle.create('shake7', { wiggles: 7, type: 'easeOut' });
const MEASURE = /measure/.test(location.search);
const B = 60 / 128, BAR = 4 * B, bt = n => n * B;
const M = %%MEASURE%%;
const SH = %%SHAPES%%;
const OR = '#FF5A1F', INK = '#0A0A0C', BONE = '#EFEBE3', CO = '#2B3BFF';
function rng(seed){let s=seed>>>0;return()=>((s=Math.imul(s^(s>>>15),2246822507)^Math.imul(s^(s>>>13),3266489909),(s^=s>>>16)>>>0)/4294967296)}
const $ = s => document.querySelector(s), $$ = s => gsap.utils.toArray(s);
const tl = gsap.timeline({ paused: true });
if (!MEASURE) {
// ======================================================== 01 PRINCIPLES  0 – 1.875
const FLOOR = 700, R = 55, TL0 = bt(1), TC1 = bt(2), TC2 = bt(3);
function hop(t, ta, tb, xa, xb, h) {
  const D = tb - ta, s = (t - ta) / D;
  const x = xa + (xb - xa) * s, vx = (xb - xa) / D, vy = -4 * h * (1 - 2 * s) / D;
  const st = 1 + Math.min(0.55, Math.hypot(vx, vy) * 0.00016);
  const rot = Math.atan2(vy, vx) * 180 / Math.PI, th = rot * Math.PI / 180;
  const ext = Math.sqrt((R * st * Math.sin(th)) ** 2 + (R / Math.sqrt(st) * Math.cos(th)) ** 2);
  return [x, Math.min(FLOOR - R - 4 * h * s * (1 - s), FLOOR - ext), rot, st, 1 / Math.sqrt(st)];
}
function ballAt(t) {
  if (t < 0.2) return [560, FLOOR - R, 0, 1, 1];
  if (t < TL0) { const p = (t - 0.2) / (TL0 - 0.2), e = p * p * (3 - 2 * p), sy = 1 - 0.36 * e, sx = 1 + 0.3 * e; return [560 - 12 * e, FLOOR - R * sy, 0, sx, sy]; }
  if (t < TC1) return hop(t, TL0, TC1, 548, 960, 400);
  if (t < TC1 + 0.05) { const p = (t - TC1) / 0.05, sy = 0.6 + 0.3 * p, sx = 1.42 - 0.3 * p; return [960, FLOOR - R * sy, 0, sx, sy]; }
  if (t < TC2) return hop(t, TC1 + 0.05, TC2, 960, 1360, 220);
  const p = Math.min(1, (t - TC2) / 0.1), e = 1 - Math.pow(1 - p, 3), sy = 1 - 0.84 * e, sx = 1 + 1.7 * e;
  return [1360, FLOOR - R * sy, 0, sx, sy];
}
const ball = $('#ball');
gsap.set(ball, { x: 560, y: FLOOR - R, scale: 0 });
tl.fromTo(ball, { scale: 0 }, { scale: 1, duration: 0.2, ease: 'back.out(3.2)', immediateRender: false }, 0.001);
const DT = 1 / 120, NK = Math.ceil((TC2 + 0.14 - 0.2) / DT);
for (let k = 0; k < NK; k++) {
  const t = 0.2 + k * DT, a = ballAt(t), b = ballAt(t + DT);
  tl.fromTo(ball, { x: a[0], y: a[1], rotation: a[2], scaleX: a[3], scaleY: a[4] },
    { x: b[0], y: b[1], rotation: b[2], scaleX: b[3], scaleY: b[4], duration: DT, ease: 'none', immediateRender: false }, t);
}
tl.fromTo('#ring1', { scale: 0.5, opacity: 0.9 }, { scale: 3.2, opacity: 0, duration: 0.5, ease: 'expo.out', immediateRender: false }, 0.001);
const GH = []; for (let t = 0.515; t < TC2 - 0.02; t += 1 / 15) if (Math.abs(t - TC1) > 0.03) GH.push(t);
$$('.gh').forEach((g, i) => {
  const tg = GH[i]; if (tg === undefined) return;
  const s = ballAt(tg);
  gsap.set(g, { x: s[0], y: s[1], rotation: s[2], scaleX: s[3], scaleY: s[4] });
  tl.fromTo(g, { opacity: 0.55 }, { opacity: 0, duration: 0.6, ease: 'power2.in', immediateRender: false }, tg);
});
tl.fromTo('#floor', { scaleX: 0 }, { scaleX: 1, duration: 0.55, ease: 'expo.out' }, 0.001);
tl.fromTo('.tick', { scaleY: 0 }, { scaleY: 1, duration: 0.3, ease: 'expo.out', stagger: { each: 0.006, from: 'center' } }, 0.08);
[0.2, 0.6, 0.95, 1.18, 1.43].forEach((t, i) => tl.to(`#lab${i}`, { clipPath: 'inset(0% 0% 0% 0%)', duration: 0.22, ease: 'power2.out' }, t));
tl.to('.lab', { opacity: 0, duration: 0.1, stagger: 0.02 }, 1.62);
const rd = rng(11);
$$('.drop').forEach((d, i) => {
  const vx = (rd() * 2 - 1) * 560, vy = 420 + rd() * 640, g = 3600, ta = vy / g, h = vy * vy / (2 * g), T = 2 * ta;
  const x0 = 1360 + (rd() * 2 - 1) * 50, y0 = FLOOR - 5;
  tl.set(d, { x: x0, y: y0, opacity: 1 }, TC2 + 0.01);
  tl.fromTo(d, { x: x0 }, { x: x0 + vx * T, duration: T, ease: 'none', immediateRender: false }, TC2 + 0.01);
  tl.fromTo(d, { y: y0 }, { y: y0 - h, duration: ta, ease: 'power2.out', immediateRender: false }, TC2 + 0.01);
  tl.fromTo(d, { y: y0 - h }, { y: y0, duration: ta, ease: 'power2.in', immediateRender: false }, TC2 + 0.01 + ta);
  tl.to(d, { scale: 0, duration: 0.08 }, TC2 + 0.01 + T);
});
tl.fromTo('#bar', { scaleX: 0 }, { scaleX: 1, duration: 0.34, ease: 'expo.out', immediateRender: false }, TC2 + 0.03);
tl.fromTo('#bar', { scaleY: 1 }, { scaleY: 84, duration: 0.2, ease: 'power4.in', immediateRender: false }, bt(4) - 0.2);

// ======================================================== 02 TYPOGRAPHY  1.875 – 3.75
gsap.set('#field', { '--ox': M.ring[0] + 'px', '--oy': M.ring[1] + 'px' });
gsap.set('#s2z', { transformOrigin: `${M.ring[0]}px ${M.ring[1]}px` });
$$('#s2 .rule').forEach((r, i) => tl.to(r, { scaleX: 1, duration: 0.55, ease: 'expo.out' }, bt(4 + i) + 0.02));
$$('#s2 .cap').forEach((c, i) => tl.to(c, { clipPath: 'inset(0% 0% 0% 0%)', duration: 0.3, ease: 'power2.out' }, bt(4 + i) + 0.1));
tl.fromTo('#l1 .c', { yPercent: 105 }, { yPercent: 0, duration: 0.42, ease: 'expo.out', stagger: 0.035 }, bt(4));
tl.fromTo('#l1', { '--wd': 125 }, { '--wd': 62, duration: 0.13, ease: 'power3.in', immediateRender: false }, bt(4) + 0.24);
tl.fromTo('#l1', { '--wd': 62 }, { '--wd': 100, duration: 0.6, ease: 'elastic.out(1,0.32)', immediateRender: false }, bt(4) + 0.37);
tl.fromTo('#l2 .w:not(.e)', { x: 460, skewX: -16, opacity: 0 }, { x: 0, skewX: 0, opacity: 1, duration: 0.45, ease: 'expo.out' }, bt(5));
[1, 2, 3].forEach(k => tl.fromTo(`#l2 .e${k}`, { x: 460, opacity: 0 }, { x: 64 * k, opacity: 0.8 - 0.2 * k, duration: 0.45, ease: 'expo.out' }, bt(5) + 0.045 * k));
tl.fromTo('#l3 .c', { yPercent: -105 }, { yPercent: 0, duration: 0.3, ease: 'bounce.out', stagger: 0.025 }, bt(6));
const re = rng(5);
$$('#l3 .c').forEach((c, i) => {
  for (let k = 0; k < 3; k++) {
    const t = bt(6) + 0.46 + k * B / 4, a = 16 + re() * 46;
    const wl = 380 + re() * 200;
    tl.fromTo(c, { y: 0, '--w': 900 }, { y: -a, '--w': wl, duration: B / 8, ease: 'power2.out', immediateRender: false }, t + i * 0.012);
    tl.fromTo(c, { y: -a, '--w': wl }, { y: 0, '--w': 900, duration: B / 8, ease: 'power2.in', immediateRender: false }, t + i * 0.012 + B / 8);
  }
});
tl.fromTo('#l4 .f', { x: -170, opacity: 0 }, { x: 0, opacity: 1, duration: 0.3, ease: 'expo.out' }, bt(7));
tl.fromTo('#l4 .rm', { x: 170, opacity: 0 }, { x: 0, opacity: 1, duration: 0.3, ease: 'expo.out' }, bt(7) + 0.02);
tl.fromTo('#ringc', { drawSVG: '0% 0%' }, { drawSVG: '0% 100%', duration: 0.22, ease: 'power3.inOut' }, bt(7));
tl.fromTo('#field', { '--hr': '-2px' }, { '--hr': '54px', duration: 0.06, ease: 'none', immediateRender: false }, bt(7) + 0.18);
tl.fromTo('#s2z', { scale: 1, x: 0, y: 0 }, { scale: 26, x: 960 - M.ring[0], y: 540 - M.ring[1], duration: 0.36, ease: 'expo.in', immediateRender: false }, bt(8) - 0.36);

// ======================================================== 03 GEOMETRY  3.75 – 5.625
const shapes = $$('#grid .sh'), GRID = [9, 16];
const cxy = i => [(i % 16) * 120 + 60, Math.floor(i / 16) * 120 + 60];
gsap.set(shapes, { scale: 0.42 });
tl.fromTo('#grid', { scale: 0.5 }, { scale: 1, duration: 0.8, ease: 'expo.out' }, 3.4);
tl.fromTo('#grid', { rotation: 0 }, { rotation: -7, duration: 1.6, ease: 'sine.inOut' }, 3.75);
tl.to(shapes, { scale: 1, duration: 0.45, ease: 'back.out(2.4)', stagger: { grid: GRID, from: 'center', amount: 0.3 } }, bt(8));
tl.to(shapes, { backgroundColor: i => { const [c, r] = [i % 16, Math.floor(i / 16)]; return Math.floor(Math.hypot(c - 7.5, r - 4)) % 3 === 0 ? OR : INK; }, duration: 0, stagger: { grid: GRID, from: 'center', amount: 0.3 } }, bt(8));
tl.to(shapes, { clipPath: SH.square, rotation: 90, duration: 0.42, ease: 'expo.out', stagger: { grid: GRID, from: [0, 0], amount: 0.24 } }, bt(9));
tl.to(shapes, { backgroundColor: i => ((i % 16) + Math.floor(i / 16)) % 2 ? CO : INK, duration: 0, stagger: { grid: GRID, from: [0, 0], amount: 0.24 } }, bt(9));
tl.to(shapes, { clipPath: SH.tri, rotation: i => ((i % 16) + Math.floor(i / 16)) % 2 ? 180 : 360, duration: 0.42, ease: 'back.out(1.8)', stagger: { grid: GRID, from: 'end', amount: 0.24 } }, bt(10));
tl.to(shapes, { backgroundColor: i => (((i % 16) - Math.floor(i / 16)) % 4 + 4) % 4 === 0 ? OR : INK, duration: 0, stagger: { grid: GRID, from: 'end', amount: 0.24 } }, bt(10));
const rs = rng(3);
const starCol = shapes.map(() => rs() < 0.14 ? OR : INK);
tl.to(shapes, { clipPath: SH.star, rotation: '+=45', duration: 0.36, ease: 'expo.out', stagger: { grid: GRID, from: 'center', amount: 0.18 } }, bt(11));
tl.to(shapes, { backgroundColor: i => starCol[i], duration: 0, stagger: { grid: GRID, from: 'center', amount: 0.18 } }, bt(11));
tl.to(shapes, { x: i => 960 - cxy(i)[0], y: i => 540 - cxy(i)[1], scale: 0.2, rotation: '+=180', duration: 0.2, ease: 'power3.in', stagger: { grid: GRID, from: 'edges', amount: 0.1 } }, 5.2);
tl.set(shapes, { opacity: 0 }, 5.52);
tl.set('#s3', { backgroundColor: INK }, 5.36);
gsap.set('#bigc', { scale: 0 });
tl.fromTo('#bigc', { scale: 0 }, { scale: 1, duration: 0.16, ease: 'back.out(2.2)', immediateRender: false }, 5.33);
tl.fromTo('#bigc', { scale: 1 }, { scale: 0.94, duration: 0.14, ease: 'power2.in', immediateRender: false }, bt(12) - 0.14);
tl.fromTo('#bigc', { opacity: 1 }, { opacity: 0, duration: 0.09, ease: 'none', immediateRender: false }, bt(12));

// ======================================================== 04–06 are WebGL; DOM adds the drop flash
tl.fromTo('#flash', { opacity: 0.32 }, { opacity: 0, duration: 0.26, ease: 'expo.out', immediateRender: false }, bt(12));
tl.fromTo('#flash', { opacity: 0.35 }, { opacity: 0, duration: 0.35, ease: 'expo.out', immediateRender: false }, bt(16));

// ======================================================== 07 EDITING  11.25 – 13.125
const S7 = bt(24), hb = B / 2;
$$('#s7a .strip').forEach((s, i) => tl.fromTo(s, { yPercent: i % 2 ? 100 : -100 }, { yPercent: 0, duration: 0.17, ease: 'expo.out' }, S7 + i * 0.022));
tl.fromTo('#sp1', { drawSVG: '0% 0%' }, { drawSVG: '0% 100%', duration: 0.21, ease: 'power2.out' }, S7 + hb);
tl.fromTo('#sp2', { drawSVG: '0% 0%' }, { drawSVG: '0% 100%', duration: 0.23, ease: 'power2.out' }, S7 + hb + 0.01);
tl.fromTo('#spsvg', { rotation: -60, scale: 0.85 }, { rotation: 40, scale: 1.1, duration: hb, ease: 'none', transformOrigin: '50% 50%' }, S7 + hb);
[['#r1', 11], ['#r2', 12], ['#r3', 18]].forEach(([r, n], i) => tl.fromTo(r, { y: 0 }, { y: -480 * n, duration: 0.19 + 0.02 * i, ease: 'expo.out' }, S7 + 2 * hb + 0.005));
const gr8 = rng(99);
for (let f = 0; f < 8; f++) {
  const t = S7 + 3 * hb + f / 30;
  $$('#s7d .sl:not(.rgbR):not(.rgbB)').forEach(s => tl.set(s, { x: (gr8() - 0.5) * (gr8() < 0.35 ? 260 : 36) }, t));
  tl.set('#s7d .rgbR', { x: -10 - gr8() * 26, y: (gr8() - 0.5) * 10 }, t);
  tl.set('#s7d .rgbB', { x: 10 + gr8() * 26, y: (gr8() - 0.5) * 10 }, t);
}
tl.fromTo('#s7e .tile', { rotationY: 0 }, { rotationY: 180, duration: 0.15, ease: 'power3.inOut', stagger: { grid: [4, 8], from: [0, 0], amount: 0.08 } }, S7 + 4 * hb);
tl.fromTo('#ct1', { rotation: 30 }, { rotation: -80, duration: hb, ease: 'power1.out', transformOrigin: '50% 50%' }, S7 + 5 * hb);
tl.fromTo('#ct2', { rotation: -20 }, { rotation: 110, duration: hb, ease: 'power1.out', transformOrigin: '50% 50%' }, S7 + 5 * hb);
[['#n3', bt(27)], ['#n2', bt(27.25)], ['#n1', bt(27.5)]].forEach(([n, t]) => tl.fromTo(n, { scale: 1.4 }, { scale: 1, duration: 0.11, ease: 'expo.out' }, t));

// ======================================================== 08 TITLE  13.125 – 15
const T8 = bt(28);
gsap.set('#dot8', { scale: 0 });
tl.fromTo('#dot8', { scale: 0 }, { scale: 1, duration: 0.26, ease: 'back.out(4)', immediateRender: false }, T8);
tl.fromTo('#ring8', { scale: 0.4, opacity: 1 }, { scale: 5.5, opacity: 0, duration: 0.6, ease: 'expo.out', immediateRender: false }, T8);
tl.fromTo('#flash', { opacity: 0.45 }, { opacity: 0, duration: 0.4, ease: 'expo.out', immediateRender: false }, T8);
tl.fromTo('#dot8', { x: 0, y: 0 }, { x: M.pslot[0] - 960, y: M.pslot[1] - 540, duration: 0.55, ease: 'expo.inOut', immediateRender: false }, T8 + 0.1);
$$('#name .nl').forEach((l, i) => {
  tl.fromTo(l, { x: 960 - M.letters[i][0], y: 540 - M.letters[i][1], scale: 0.15, opacity: 0 },
    { x: 0, y: 0, scale: 1, opacity: 1, duration: 0.62, ease: 'expo.out' }, T8 + 0.2 + Math.abs(i - 2.5) * 0.03);
});
tl.fromTo('#name', { '--wd': 62 }, { '--wd': 112, duration: 0.7, ease: 'expo.out' }, T8 + 0.2);
tl.fromTo('#s8in', { x: 0 }, { x: 16, duration: 0.4, ease: 'shake7', immediateRender: false }, T8);
tl.fromTo('#role span', { yPercent: 115 }, { yPercent: 0, duration: 0.55, ease: 'expo.out' }, T8 + 0.5);
tl.to('#rule8', { scaleX: 1, duration: 0.6, ease: 'expo.inOut' }, T8 + 0.58);
tl.fromTo('#credit', { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: 0.45, ease: 'power2.out' }, T8 + 1.0);
tl.set('#shine', { opacity: 1 }, T8 + 0.98);
tl.fromTo('#shine', { backgroundPosition: '100% 0%' }, { backgroundPosition: '0% 0%', duration: 0.75, ease: 'power2.inOut', immediateRender: false }, T8 + 0.98);
tl.fromTo('#s8', { scale: 1 }, { scale: 1.035, duration: 1.875, ease: 'sine.out', immediateRender: false, transformOrigin: '50% 45%' }, T8);
tl.fromTo('#dot8', { scale: 1 }, { scale: 1.3, duration: 0.09, ease: 'power2.out', immediateRender: false }, bt(31));
tl.fromTo('#dot8', { scale: 1.3 }, { scale: 1, duration: 0.4, ease: 'elastic.out(1,0.4)', immediateRender: false }, bt(31) + 0.09);

// ======================================================== HUD + finishing
tl.set(['#vig', '#grain'], { opacity: (i) => [1, 0.085][i] }, 0.001);
const hudC = [[0, BONE], [bt(4), INK], [5.36, BONE], [S7, BONE], [T8, BONE]];
hudC.forEach(([t, c]) => tl.set('#hud', { color: c }, t === 0 ? 0.001 : t));
tl.set('#hud', { mixBlendMode: 'difference' }, S7);
tl.set('#hud', { mixBlendMode: 'normal' }, T8);
$$('#hud .seg i').forEach((s, k) => tl.fromTo(s, { scaleX: 0 }, { scaleX: 1, duration: BAR, ease: 'none', immediateRender: false }, k * BAR + 0.001));
for (let b = 0; b < 32; b++) tl.fromTo('#hud .rec', { opacity: 1 }, { opacity: 0.25, duration: B * 0.9, ease: 'power2.in', immediateRender: false }, bt(b) + 0.001);
const LABELS = ['PRINCIPLES', 'TYPOGRAPHY', 'GEOMETRY', '3D', 'PARTICLES', 'SHADERS', 'EDITING', 'CREDITS'];
const GLY = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/#+=';
function scr(txt, p, seed) { const r = rng(seed); let o = ''; for (let i = 0; i < txt.length; i++) { const c = txt[i]; o += (i < p * txt.length || c === ' ') ? c : GLY[Math.floor(r() * GLY.length)]; } return o; }
const tcEl = $('#tc'), snEl = $('#shotn'), slEl = $('#shotl'), grEl = $('#grain'), wdv = $('#wdv'), l1 = $('#l1'), skEl = $('#skills');
const SK = skEl.textContent.toUpperCase();
function tick() {
  const t = tl.time(), f = Math.floor(t * 30 + 1e-6);
  tcEl.textContent = `00:00:${String(Math.floor(f / 30)).padStart(2, '0')}:${String(f % 30).padStart(2, '0')}`;
  const k = Math.min(7, Math.floor(t / BAR + 1e-6)), dt = t - k * BAR;
  snEl.textContent = '0' + (k + 1);
  slEl.textContent = scr(LABELS[k], Math.min(1, dt / 0.24), f * 7 + 3);
  const g = rng(f * 13 + 5); grEl.style.backgroundPosition = `${Math.floor(g() * 256) * 2}px ${Math.floor(g() * 256) * 2}px`;
  wdv.textContent = Math.round(parseFloat(gsap.getProperty(l1, '--wd')) || 125);
  const p8 = (t - (T8 + 0.66)) / 0.42;
  skEl.textContent = p8 < 0 ? '' : scr(SK, Math.min(1, p8), f * 3 + 1);
}
tl.to({ p: 0 }, { p: 1, duration: %%DUR%%, ease: 'none', onUpdate: tick }, 0);
tl.to({}, { duration: 0.001 }, %%DUR%% - 0.001);
}
window.__timelines = window.__timelines || {};
window.__timelines["main"] = tl;
"""

GL_JS = r"""
import * as THREE from 'three';
const MEASURE = /measure/.test(location.search);
const Z = %%ZOOM%%, W = 1920, H = 1080, PXW = Math.round(W * Z), PXH = Math.round(H * Z);
const B = 60 / 128, bt = n => n * B;
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const seg = (t, a, b) => clamp((t - a) / (b - a));
const ss = (a, b, t) => { const x = seg(t, a, b); return x * x * (3 - 2 * x); };
const lerp = (a, b, k) => a + (b - a) * k;
const E = {
  expoOut: p => p >= 1 ? 1 : 1 - Math.pow(2, -10 * p),
  expoIn: p => p <= 0 ? 0 : Math.pow(2, 10 * p - 10),
  cubicOut: p => 1 - Math.pow(1 - p, 3),
  cubicInOut: p => p < .5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2,
  backOut: (p, s = 1.70158) => 1 + (s + 1) * Math.pow(p - 1, 3) + s * Math.pow(p - 1, 2),
};
function rng(seed){let s=seed>>>0;return()=>((s=Math.imul(s^(s>>>15),2246822507)^Math.imul(s^(s>>>13),3266489909),(s^=s>>>16)>>>0)/4294967296)}
window.__hf = window.__hf || {}; window.__hf.buildReady = window.__hf.buildReady || {};
let resolveReady; window.__hf.buildReady.main = new Promise(r => resolveReady = r);

const canvas = document.getElementById('gl');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: false, preserveDrawingBuffer: true, alpha: false });
renderer.setPixelRatio(1); renderer.setSize(PXW, PXH, false);
renderer.outputColorSpace = THREE.LinearSRGBColorSpace;
renderer.toneMapping = THREE.NoToneMapping;
const HF = THREE.HalfFloatType;
const rtS = new THREE.WebGLRenderTarget(PXW, PXH, { type: HF, samples: 4 });
const LV = [4, 8, 16, 32].map(d => { const w = Math.max(2, Math.round(PXW / d)), h = Math.max(2, Math.round(PXH / d));
  return { w, h, a: new THREE.WebGLRenderTarget(w, h, { type: HF }), b: new THREE.WebGLRenderTarget(w, h, { type: HF }) }; });
const VS = `varying vec2 vUv; void main(){ vUv = uv; gl_Position = vec4(position.xy, 0.0, 1.0); }`;
const fsScene = new THREE.Scene(), fsCam = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);
const fsQuad = new THREE.Mesh(new THREE.PlaneGeometry(2, 2)); fsQuad.frustumCulled = false; fsScene.add(fsQuad);
const fsMat = (fs, uniforms) => new THREE.ShaderMaterial({ vertexShader: VS, fragmentShader: fs, uniforms, depthTest: false, depthWrite: false });
function pass(mat, target) { fsQuad.material = mat; renderer.setRenderTarget(target); renderer.render(fsScene, fsCam); }
const brightM = fsMat(`uniform sampler2D tIn; uniform float uTh; uniform vec2 uPx; varying vec2 vUv;
  void main(){ vec3 c = (texture2D(tIn, vUv + uPx*vec2(-1.,-1.)).rgb + texture2D(tIn, vUv + uPx*vec2(1.,-1.)).rgb + texture2D(tIn, vUv + uPx*vec2(-1.,1.)).rgb + texture2D(tIn, vUv + uPx*vec2(1.,1.)).rgb) * .25;
  if (any(isnan(c)) || any(isinf(c))) c = vec3(0.); c = min(c, vec3(24.));
  float l = max(c.r, max(c.g, c.b)); gl_FragColor = vec4(c * smoothstep(uTh, uTh * 1.6 + .15, l), 1.); }`,
  { tIn: { value: null }, uTh: { value: 1 }, uPx: { value: new THREE.Vector2(1 / PXW, 1 / PXH) } });
const blurM = fsMat(`uniform sampler2D tIn; uniform vec2 uDir; varying vec2 vUv;
  void main(){ vec3 s = texture2D(tIn, vUv).rgb * .227027;
  s += (texture2D(tIn, vUv + uDir * 1.3846153846).rgb + texture2D(tIn, vUv - uDir * 1.3846153846).rgb) * .3162162162;
  s += (texture2D(tIn, vUv + uDir * 3.2307692308).rgb + texture2D(tIn, vUv - uDir * 3.2307692308).rgb) * .0702702703;
  gl_FragColor = vec4(s, 1.); }`, { tIn: { value: null }, uDir: { value: new THREE.Vector2() } });
const copyM = fsMat(`uniform sampler2D tIn; varying vec2 vUv; void main(){ gl_FragColor = vec4(texture2D(tIn, vUv).rgb, 1.); }`, { tIn: { value: null } });
const compM = fsMat(`uniform sampler2D tS, tB1, tB2, tB3, tB4; uniform float uBloom, uExp, uCA, uVig, uFlash, uSat; varying vec2 vUv;
  vec3 neutral(vec3 c){ float x = min(c.r, min(c.g, c.b)); float o = x < .08 ? x - 6.25 * x * x : .04; c -= o;
    float pk = max(c.r, max(c.g, c.b)); if (pk < .76) return c; float d = .24; float np = 1. - d * d / (pk + d - .76);
    c *= np / pk; float g = 1. - 1. / (.15 * (pk - np) + 1.); return mix(c, vec3(np), g); }
  vec3 srgb(vec3 c){ c = clamp(c, 0., 1.); return mix(c * 12.92, 1.055 * pow(c, vec3(1. / 2.4)) - .055, step(.0031308, c)); }
  void main(){ vec2 d = vUv - .5; float r2 = dot(d, d); vec2 o = d * uCA * r2;
    vec3 c = vec3(texture2D(tS, vUv - o).r, texture2D(tS, vUv).g, texture2D(tS, vUv + o).b);
    if (any(isnan(c)) || any(isinf(c))) c = vec3(0.); c = min(c, vec3(64.));
    c += (texture2D(tB1, vUv).rgb * .5 + texture2D(tB2, vUv).rgb * .7 + texture2D(tB3, vUv).rgb * .9 + texture2D(tB4, vUv).rgb * 1.1) * uBloom;
    c = neutral(c * uExp); float l = dot(c, vec3(.2126, .7152, .0722)); c = mix(vec3(l), c, uSat);
    c = srgb(c); c *= mix(1., smoothstep(1.05, .3, sqrt(r2) * 1.3), uVig); c = mix(c, vec3(1.), uFlash);
    gl_FragColor = vec4(c, 1.); }`,
  { tS: { value: rtS.texture }, tB1: { value: LV[0].a.texture }, tB2: { value: LV[1].a.texture }, tB3: { value: LV[2].a.texture }, tB4: { value: LV[3].a.texture }, uBloom: { value: .5 }, uExp: { value: 1 },
    uCA: { value: 0 }, uVig: { value: .6 }, uFlash: { value: 0 }, uSat: { value: 1 } });
function post(p) {
  brightM.uniforms.tIn.value = rtS.texture; brightM.uniforms.uTh.value = p.th; pass(brightM, LV[0].a);
  LV.forEach((L, i) => {
    if (i) { copyM.uniforms.tIn.value = LV[i - 1].a.texture; pass(copyM, L.a); }
    blurM.uniforms.tIn.value = L.a.texture; blurM.uniforms.uDir.value.set(1 / L.w, 0); pass(blurM, L.b);
    blurM.uniforms.tIn.value = L.b.texture; blurM.uniforms.uDir.value.set(0, 1 / L.h); pass(blurM, L.a);
  });
  const u = compM.uniforms; u.uBloom.value = p.bloom; u.uExp.value = p.exp; u.uCA.value = p.ca; u.uVig.value = p.vig; u.uFlash.value = p.flash; u.uSat.value = p.sat;
  pass(compM, null);
}
const NOISE = `
vec3 mod289(vec3 x){return x-floor(x*(1./289.))*289.;} vec4 mod289(vec4 x){return x-floor(x*(1./289.))*289.;}
vec4 permute(vec4 x){return mod289(((x*34.)+1.)*x);} vec4 taylorInvSqrt(vec4 r){return 1.79284291400159-.85373472095314*r;}
float snoise(vec3 v){const vec2 C=vec2(1./6.,1./3.);const vec4 D=vec4(0.,.5,1.,2.);vec3 i=floor(v+dot(v,C.yyy));vec3 x0=v-i+dot(i,C.xxx);
vec3 g=step(x0.yzx,x0.xyz);vec3 l=1.-g;vec3 i1=min(g.xyz,l.zxy);vec3 i2=max(g.xyz,l.zxy);vec3 x1=x0-i1+C.xxx;vec3 x2=x0-i2+C.yyy;vec3 x3=x0-D.yyy;
i=mod289(i);vec4 p=permute(permute(permute(i.z+vec4(0.,i1.z,i2.z,1.))+i.y+vec4(0.,i1.y,i2.y,1.))+i.x+vec4(0.,i1.x,i2.x,1.));
float n_=.142857142857;vec3 ns=n_*D.wyz-D.xzx;vec4 j=p-49.*floor(p*ns.z*ns.z);vec4 x_=floor(j*ns.z);vec4 y_=floor(j-7.*x_);
vec4 x=x_*ns.x+ns.yyyy;vec4 y=y_*ns.x+ns.yyyy;vec4 h=1.-abs(x)-abs(y);vec4 b0=vec4(x.xy,y.xy);vec4 b1=vec4(x.zw,y.zw);
vec4 s0=floor(b0)*2.+1.;vec4 s1=floor(b1)*2.+1.;vec4 sh=-step(h,vec4(0.));vec4 a0=b0.xzyw+s0.xzyw*sh.xxyy;vec4 a1=b1.xzyw+s1.xzyw*sh.zzww;
vec3 p0=vec3(a0.xy,h.x);vec3 p1=vec3(a0.zw,h.y);vec3 p2=vec3(a1.xy,h.z);vec3 p3=vec3(a1.zw,h.w);
vec4 norm=taylorInvSqrt(vec4(dot(p0,p0),dot(p1,p1),dot(p2,p2),dot(p3,p3)));p0*=norm.x;p1*=norm.y;p2*=norm.z;p3*=norm.w;
vec4 m=max(.6-vec4(dot(x0,x0),dot(x1,x1),dot(x2,x2),dot(x3,x3)),0.);m=m*m;return 42.*dot(m*m,vec4(dot(p0,x0),dot(p1,x1),dot(p2,x2),dot(p3,x3)));}`;

// -------------------------------------------------------------- 04 · 3D
const cOR = new THREE.Color('#FF5A1F'), cWH = new THREE.Color('#F4F4F6');
function studio() {
  const s = new THREE.Scene(); s.background = new THREE.Color(0x0c0c10);
  const dome = new THREE.Mesh(new THREE.SphereGeometry(30, 32, 16), new THREE.ShaderMaterial({ side: THREE.BackSide, vertexShader: 'varying vec3 vP; void main(){ vP = position; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.); }', fragmentShader: 'varying vec3 vP; void main(){ float h = normalize(vP).y; gl_FragColor = vec4(mix(vec3(.02,.02,.025), vec3(.22,.22,.26), smoothstep(-.2, .9, h)), 1.); }' })); s.add(dome);
  const add = (w, h, hex, k, p) => { const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ color: new THREE.Color(hex).multiplyScalar(k), side: THREE.DoubleSide })); m.position.set(...p); m.lookAt(0, 0, 0); s.add(m); };
  add(11, 1.5, 0xffffff, 6, [0, 7.5, 2.5]); add(1.3, 11, 0xffffff, 3.6, [-8, 0.5, 3]); add(1.0, 9, 0xffffff, 2.4, [7.5, 0, -3]);
  add(6, 5, 0xff5a1f, 2.6, [4.5, -4, 6]); add(8, 6, 0x2b3bff, 2.6, [-6, 3, -7]); add(5, 3, 0xffffff, 1.0, [0, -6, -4]);
  const pm = new THREE.PMREMGenerator(renderer); const tex = pm.fromScene(s, 0.02).texture; pm.dispose(); return tex;
}
const s4 = new THREE.Scene(); s4.background = new THREE.Color(0x050507);
const cam4 = new THREE.PerspectiveCamera(30, W / H, 0.1, 100);
const U4 = { uAmp: { value: 0 }, uT: { value: 0 }, uFreq: { value: 0.95 } };
const blobM = new THREE.MeshPhysicalMaterial({ color: cOR.clone(), roughness: 0.3, metalness: 0, clearcoat: 1, clearcoatRoughness: 0.06,
  iridescence: 0.001, iridescenceIOR: 1.8, iridescenceThicknessRange: [120, 640], emissive: cOR.clone(), emissiveIntensity: 1 });
blobM.onBeforeCompile = sh => {
  Object.assign(sh.uniforms, U4);
  sh.vertexShader = sh.vertexShader
    .replace('#include <common>', `#include <common>\nuniform float uAmp, uT, uFreq;\n${NOISE}\nvec3 dsp(vec3 p){ vec3 n = normalize(p); float d = snoise(n * uFreq + vec3(0., uT * .7, uT * .4)) * .8 + snoise(n * uFreq * 2.1 - vec3(uT * .5)) * .2; return n * (1. + uAmp * d); }`)
    .replace('#include <beginnormal_vertex>', `vec3 _n = normalize(position); vec3 _t = normalize(abs(_n.y) < .99 ? cross(_n, vec3(0., 1., 0.)) : cross(_n, vec3(1., 0., 0.)));
      vec3 _b = normalize(cross(_n, _t)); vec3 _p0 = dsp(position); vec3 _p1 = dsp(position + _t * .01); vec3 _p2 = dsp(position + _b * .01);
      vec3 objectNormal = normalize(cross(_p1 - _p0, _p2 - _p0));`)
    .replace('#include <begin_vertex>', 'vec3 transformed = _p0;');
};
const blob = new THREE.Mesh(new THREE.SphereGeometry(1, 256, 160), blobM); s4.add(blob);
const NI = 150, gold = Math.PI * (3 - Math.sqrt(5)), r4 = rng(404), D4 = [];
for (let i = 0; i < NI; i++) {
  const y = 1 - 2 * (i + 0.5) / NI, rr = Math.sqrt(1 - y * y), ph = i * gold;
  const ux = Math.cos(ph) * rr, uz = Math.sin(ph) * rr, R2 = 2.25 + (r4() - 0.5) * 0.35;
  D4.push({ s: [ux, y, uz], p: [ux * R2, y * R2, uz * R2], k: i / (NI - 1), strand: i % 2, size: 0.075 + r4() * 0.085, del: r4() * 0.07, orange: i % 4 === 1 });
}
const sphG = new THREE.SphereGeometry(1, 32, 16);
const chromeM = new THREE.MeshPhysicalMaterial({ color: 0xffffff, metalness: 1, roughness: 0.06, iridescence: 0.7, iridescenceIOR: 1.8, iridescenceThicknessRange: [150, 600], clearcoat: 0.001 });
const lacqM = new THREE.MeshPhysicalMaterial({ color: cOR.clone(), roughness: 0.25, clearcoat: 1, clearcoatRoughness: 0.05, iridescence: 0.001 });
const nO = D4.filter(d => d.orange).length;
const imC = new THREE.InstancedMesh(sphG, chromeM, NI - nO), imO = new THREE.InstancedMesh(sphG, lacqM, nO);
imC.frustumCulled = imO.frustumCulled = false;
const grp = new THREE.Group(); grp.add(imC, imO); s4.add(grp);
const key = new THREE.DirectionalLight(0xffffff, 2.0); key.position.set(-3, 4, 5); s4.add(key);
const rim = new THREE.PointLight(0x4a5cff, 40, 30, 2); rim.position.set(3.5, 1.5, -4); s4.add(rim);
const glowTex = (() => { const c = document.createElement('canvas'); c.width = c.height = 256; const x = c.getContext('2d'); const g = x.createRadialGradient(128, 128, 0, 128, 128, 128);
  g.addColorStop(0, 'rgba(255,255,255,1)'); g.addColorStop(0.2, 'rgba(255,190,150,.8)'); g.addColorStop(1, 'rgba(255,90,31,0)'); x.fillStyle = g; x.fillRect(0, 0, 256, 256); return new THREE.CanvasTexture(c); })();
const core = new THREE.Sprite(new THREE.SpriteMaterial({ map: glowTex, blending: THREE.AdditiveBlending, depthWrite: false, depthTest: false, transparent: true }));
core.material.color.setRGB(6, 4, 3); s4.add(core);
const dmy = new THREE.Object3D();
function renderS4(t) {
  U4.uT.value = t;
  U4.uAmp.value = 0.21 * ss(0.05, 0.5, t) + 0.1 * Math.exp(-Math.pow((t - 0.47) / 0.07, 2));
  const chr = ss(0.44, 0.6, t);
  blobM.color.copy(cOR).lerp(cWH, chr); blobM.metalness = chr; blobM.roughness = lerp(0.3, 0.05, chr);
  blobM.iridescence = lerp(0.001, 1, chr); blobM.emissiveIntensity = 0.5 * (1 - ss(0.0, 0.22, t)); blobM.envMapIntensity = lerp(0.3, 1.1, ss(0, 0.35, t));
  const pop = 1 - 0.06 * Math.exp(-t * 7) * Math.cos(t * 30), burst = ss(0.92, 1.0, t);
  blob.scale.setScalar(pop * (1 - burst)); blob.visible = burst < 1;
  blob.rotation.set(0.25 * t, 0.7 * t, 0);
  const vis = t >= 0.9; imC.visible = imO.visible = vis;
  if (vis) {
    let ic = 0, io = 0;
    for (let i = 0; i < NI; i++) {
      const d = D4[i];
      const a = E.backOut(seg(t, 0.93 + d.del, 1.3 + d.del), 1.5);
      const b = E.cubicInOut(seg(t, 1.36 + d.del * 1.6, 1.62 + d.del * 1.6));
      const c = E.expoIn(seg(t, 1.62 + d.del * 0.7, 1.86));
      const ang = d.k * Math.PI * 4.5 + d.strand * Math.PI + t * 2.4;
      const hx = Math.cos(ang) * 1.05, hz = Math.sin(ang) * 1.05, hy = (d.k - 0.5) * 4.4;
      let x = lerp(d.s[0], d.p[0], a), y = lerp(d.s[1], d.p[1], a), z = lerp(d.s[2], d.p[2], a);
      x = lerp(x, hx, b); y = lerp(y, hy, b); z = lerp(z, hz, b);
      const sc = d.size * clamp((t - 0.9) / 0.06) * (1 - c);
      dmy.position.set(x * (1 - c), y * (1 - c), z * (1 - c)); dmy.scale.setScalar(Math.max(1e-4, sc)); dmy.updateMatrix();
      if (d.orange) imO.setMatrixAt(io++, dmy.matrix); else imC.setMatrixAt(ic++, dmy.matrix);
    }
    imC.instanceMatrix.needsUpdate = imO.instanceMatrix.needsUpdate = true;
  }
  grp.rotation.set(0.1 + 0.3 * ss(1.36, 1.62, t), 0.9 * t + 1.1 * ss(0.93, 1.5, t), 0.35 * ss(1.36, 1.62, t));
  const cs = E.expoIn(seg(t, 1.66, 1.875)); core.scale.setScalar(0.05 + 1.4 * cs); core.material.opacity = cs;
  const az = 0.5 * E.cubicInOut(seg(t, 0, 0.92)) + 1.0 * E.cubicInOut(seg(t, 0.92, 1.875));
  const el = 0.15 * ss(0, 0.9, t) - 0.12 * ss(1.3, 1.8, t);
  const dist = 8.123 - 2.1 * E.cubicInOut(seg(t, 0.04, 0.9)) + 3.6 * E.expoOut(seg(t, 0.93, 1.35)) - 4.6 * E.expoIn(seg(t, 1.6, 1.875));
  let sx = 0, sy = 0;
  for (const [tb, am] of [[0, 0.07], [0.469, 0.04], [0.9375, 0.06], [1.406, 0.03]]) { const dt = t - tb; if (dt >= 0) { const e = Math.exp(-dt * 13) * am; sx += Math.sin(dt * 71 + tb * 9) * e; sy += Math.cos(dt * 53 + tb * 5) * e; } }
  cam4.position.set(Math.sin(az) * Math.cos(el) * dist, Math.sin(el) * dist, Math.cos(az) * Math.cos(el) * dist);
  cam4.lookAt(0, 0, 0); cam4.position.x += sx; cam4.position.y += sy;
  key.position.set(-3 + 4 * ss(0, 0.5, t), 4, 5);
  const burstFlash = Math.exp(-Math.pow((t - 0.95) / 0.05, 2));
  return { bloom: 0.32 + 0.5 * burstFlash + 1.6 * cs, th: 1.1, exp: 1.0 + 0.3 * Math.exp(-Math.pow((t - 0.47) / 0.05, 2)) + 0.4 * burstFlash, ca: 0.03 + 0.35 * burstFlash + 0.5 * cs, vig: 0.7, flash: Math.pow(cs, 5), sat: 1 };
}

// -------------------------------------------------------------- 05 · particles
const NP = 40000, r5 = rng(505);
const s5 = new THREE.Scene();
const cam5 = new THREE.PerspectiveCamera(30, W / H, 0.1, 100);
const g5 = new THREE.BufferGeometry();
const aDir = new Float32Array(NP * 3), aSeed = new Float32Array(NP * 4), aGal = new Float32Array(NP * 4), aText = new Float32Array(NP * 3);
for (let i = 0; i < NP; i++) {
  const u = r5() * 2 - 1, ph = r5() * Math.PI * 2, s = Math.sqrt(1 - u * u);
  aDir.set([s * Math.cos(ph), u * 0.85, s * Math.sin(ph)], i * 3);
  aSeed.set([r5(), r5(), r5(), r5()], i * 4);
  const arm = Math.floor(r5() * 3), rr = 0.12 + 4.3 * Math.pow(r5(), 1.7);
  aGal.set([rr, arm * 2 * Math.PI / 3 + rr * 1.15 + (r5() - 0.5) * 0.55 / (0.4 + rr * 0.35), (r5() - 0.5) * 0.4 * Math.exp(-rr * 0.45), arm], i * 4);
}
g5.setAttribute('position', new THREE.BufferAttribute(new Float32Array(NP * 3), 3));
g5.setAttribute('aDir', new THREE.BufferAttribute(aDir, 3)); g5.setAttribute('aSeed', new THREE.BufferAttribute(aSeed, 4));
g5.setAttribute('aGal', new THREE.BufferAttribute(aGal, 4)); g5.setAttribute('aText', new THREE.BufferAttribute(aText, 3));
const m5 = new THREE.ShaderMaterial({ transparent: true, depthWrite: false, depthTest: false, blending: THREE.AdditiveBlending,
  uniforms: { uT: { value: 0 }, uPx: { value: PXH / 1080 } },
  vertexShader: `uniform float uT, uPx; attribute vec3 aDir, aText; attribute vec4 aSeed, aGal; varying vec3 vC; varying float vA;
    mat3 rX(float a){ float c = cos(a), s = sin(a); return mat3(1., 0., 0., 0., c, s, 0., -s, c); }
    mat3 rY(float a){ float c = cos(a), s = sin(a); return mat3(c, 0., -s, 0., 1., 0., s, 0., c); }
    void main(){
      float t = uT;
      float sp = mix(3.0, 12.0, pow(aSeed.x, 1.6)), k = 4.2;
      vec3 pE = rY(t * 1.4 * (aSeed.y - .5)) * (aDir * sp * (1. - exp(-k * t)) / k);
      float r = aGal.x, th = aGal.y + t * 1.9 / (.3 + r);
      vec3 pG = rX(-1.08) * rY(.35) * vec3(cos(th) * r, aGal.z, sin(th) * r);
      vec3 pT = aText + .018 * vec3(sin(t * 7. + aSeed.y * 40.), cos(t * 6. + aSeed.z * 40.), 0.);
      float g = smoothstep(.2 + aSeed.y * .25, .72 + aSeed.y * .22, t);
      float x = smoothstep(1.0 + aSeed.z * .24, 1.4 + aSeed.z * .12, t);
      float w = smoothstep(1.62 + aSeed.w * .12, 1.95, t);
      vec3 p = mix(mix(pE, pG, g), pT, x);
      p += vec3(7. + 7. * aSeed.x, 1.2 * (aSeed.y - .5), 3. * (aSeed.z - .5)) * w * w + .7 * w * vec3(sin(p.y * 3. + t * 5.), cos(p.x * 2.5 + t * 4.), sin(p.x * 2.));
      vec4 mv = modelViewMatrix * vec4(p, 1.);
      gl_Position = projectionMatrix * mv;
      gl_PointSize = mix(1.7, 3.3, aSeed.w) * (1. + 1.8 * exp(-t * 5.)) * uPx * (10. / -mv.z) * mix(1., 1.45, x);
      vec3 hot = vec3(1., .82, .62), orn = vec3(1., .1, .014), cob = vec3(.03, .05, 1.), bone = vec3(.86, .83, .77);
      vec3 cE = mix(hot * 2.8, orn * 2.4, smoothstep(0., .45, t) * aSeed.y);
      vec3 cG = mix(mix(hot * 2.4, orn * 2.0, smoothstep(.1, 1.0, r)), cob * 2.2, smoothstep(1.0, 3.0, r) * step(.3, aSeed.z));
      vec3 cT = aSeed.x > .93 ? orn * 2.6 : vec3(1., .97, .93) * 1.6;
      vC = mix(mix(cE, cG, g), cT, x); vA = (1. - w) * mix(.95, .75, x);
    }`,
  fragmentShader: `varying vec3 vC; varying float vA; void main(){ float d = length(gl_PointCoord - .5); float a = smoothstep(.5, .05, d); gl_FragColor = vec4(vC * vA, a * a); }` });
const pts5 = new THREE.Points(g5, m5); pts5.frustumCulled = false; s5.add(pts5);
const shock = new THREE.Mesh(new THREE.RingGeometry(0.985, 1.0, 160), new THREE.MeshBasicMaterial({ color: new THREE.Color(2.2, 1.7, 1.3), transparent: true, blending: THREE.AdditiveBlending, depthWrite: false, depthTest: false }));
const shock2 = new THREE.Mesh(new THREE.RingGeometry(0.97, 1.0, 160), new THREE.MeshBasicMaterial({ color: new THREE.Color(2.0, 0.25, 0.04), transparent: true, blending: THREE.AdditiveBlending, depthWrite: false, depthTest: false }));
s5.add(shock, shock2);
async function sampleText(word, n) {
  const cw_ = 2200, ch_ = 560, c = document.createElement('canvas'); c.width = cw_; c.height = ch_;
  const x = c.getContext('2d', { willReadFrequently: true }); x.fillStyle = '#000'; x.fillRect(0, 0, cw_, ch_);
  x.font = '900 380px Archivo'; x.fontStretch = 'expanded'; x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillStyle = '#fff';
  x.fillText(word, cw_ / 2, ch_ / 2 + 14);
  const d = x.getImageData(0, 0, cw_, ch_).data, px = [];
  let minX = 1e9, maxX = -1e9;
  for (let yy = 0; yy < ch_; yy += 2) for (let xx = 0; xx < cw_; xx += 2) if (d[(yy * cw_ + xx) * 4] > 140) { px.push(xx, yy); minX = Math.min(minX, xx); maxX = Math.max(maxX, xx); }
  const r = rng(77), worldW = 7.4, sc = worldW / (maxX - minX), cx = (minX + maxX) / 2;
  for (let i = 0; i < n; i++) {
    const j = Math.floor(r() * (px.length / 2)) * 2;
    aText[i * 3] = (px[j] + (r() - .5) * 2 - cx) * sc; aText[i * 3 + 1] = -(px[j + 1] + (r() - .5) * 2 - ch_ / 2) * sc; aText[i * 3 + 2] = (r() - .5) * 0.12;
  }
  g5.attributes.aText.needsUpdate = true;
}
function renderS5(t) {
  m5.uniforms.uT.value = t;
  const k1 = E.cubicOut(seg(t, 0, 0.55)), k2 = E.cubicOut(seg(t, 0.04, 0.7));
  shock.scale.setScalar(0.05 + 5.6 * k1); shock.material.opacity = Math.pow(1 - seg(t, 0.0, 0.42), 2) * 0.8;
  shock2.scale.setScalar(0.05 + 4.2 * k2); shock2.material.opacity = Math.pow(1 - seg(t, 0.04, 0.55), 2) * 0.6;
  shock.rotation.x = -1.08; shock2.rotation.x = -1.08; shock.rotation.y = shock2.rotation.y = 0.35;
  const az = 0.32 * Math.sin(Math.PI * seg(t, 0.2, 1.1)) ;
  cam5.position.set(Math.sin(az) * 10, 0.15 * Math.sin(Math.PI * seg(t, 0.2, 1.1)), Math.cos(az) * 10); cam5.lookAt(0, 0, 0);
  const boom = Math.exp(-t * 7);
  return { bloom: 0.7 + 0.35 * boom, th: 0.7 + 1.5 * boom, exp: 1.0, ca: 0.015 + 0.2 * boom, vig: 0.75, flash: 0.85 * Math.exp(-t * 26), sat: 1 };
}

// -------------------------------------------------------------- 06 · shaders
const tt = document.createElement('canvas'); tt.width = 2048; tt.height = 1152;
const tTex = new THREE.CanvasTexture(tt); tTex.colorSpace = THREE.NoColorSpace;
const IC = new THREE.Vector2(0.5, 0.5);
function drawFluid() {
  const x = tt.getContext('2d'); x.fillStyle = '#000'; x.fillRect(0, 0, 2048, 1152);
  x.font = '900 440px Archivo'; x.fontStretch = 'expanded'; x.textBaseline = 'alphabetic'; x.fillStyle = '#fff'; x.textAlign = 'left';
  const w = x.measureText('FLUID').width, left = 1024 - w / 2, base = 576 + 154;
  x.fillText('FLUID', left, base);
  const wFLUI = x.measureText('FLUI').width, wI = x.measureText('I').width;
  IC.set((left + wFLUI - wI / 2) / 2048, 1 - (base - 154) / 1152);
  tTex.needsUpdate = true;
}
const s6 = new THREE.Scene();
const m6 = new THREE.ShaderMaterial({ depthTest: false, depthWrite: false,
  uniforms: { uT: { value: 0 }, uZ: { value: 40 }, uC: { value: IC }, tText: { value: tTex }, uFade: { value: 1 }, uG: { value: 0.22 * PXH }, uBeats: { value: new THREE.Vector4(0, B, 2 * B, 3 * B) } },
  vertexShader: VS,
  fragmentShader: `uniform float uT, uZ, uFade, uG; uniform vec2 uC; uniform sampler2D tText; uniform vec4 uBeats; varying vec2 vUv;
    float h21(vec2 p){ p = fract(p * vec2(123.34, 456.21)); p += dot(p, p + 45.32); return fract(p.x * p.y); }
    float vn(vec2 p){ vec2 i = floor(p), f = fract(p); vec2 u = f * f * (3. - 2. * f);
      return mix(mix(h21(i), h21(i + vec2(1., 0.)), u.x), mix(h21(i + vec2(0., 1.)), h21(i + vec2(1., 1.)), u.x), u.y); }
    float fbm(vec2 p){ float s = 0., a = .5; mat2 m = mat2(1.6, 1.2, -1.2, 1.6); for (int i = 0; i < 5; i++){ s += a * vn(p); p = m * p; a *= .5; } return s; }
    void main(){
      vec2 p = (vUv - .5) * vec2(1.7778, 1.);
      vec2 rp = vec2(0.);
      for (int i = 0; i < 4; i++){ float dt = uT - uBeats[i]; if (dt > 0.){ float d = length(p), ring = dt * 1.5;
        float w = exp(-pow((d - ring) * 7., 2.)) * exp(-dt * 2.2); rp += normalize(p + 1e-5) * w * .06 * sin((d - ring) * 34.); } }
      vec2 q = p * 1.5 + rp; float t = uT * .42;
      vec2 a = vec2(fbm(q + vec2(0., t)), fbm(q + vec2(5.2, 1.3) - t * .6));
      vec2 b = vec2(fbm(q + 3.6 * a + vec2(1.7, 9.2) + t * .9), fbm(q + 3.6 * a + vec2(8.3, 2.8) - t * .7));
      float f = fbm(q + 3.3 * b);
      vec3 ink = vec3(.003, .003, .006), cob = vec3(.03, .05, 1.), orn = vec3(1., .1, .014), bon = vec3(.86, .83, .77);
      float bO = smoothstep(.36, .42, f) * (1. - smoothstep(.5, .55, f));
      float bB = smoothstep(.57, .61, f) * (1. - smoothstep(.66, .72, f));
      vec3 col = ink + orn * 1.1 * bO + cob * .9 * bB;
      col = mix(col, bon, smoothstep(.74, .84, f + .15 * a.y));
      vec2 gr = vec2(dFdx(f), dFdy(f)) * uG; vec3 n = normalize(vec3(-gr, 1.));
      float spec = pow(max(dot(reflect(vec3(0., 0., -1.), n), normalize(vec3(-.35, .45, .82))), 0.), 22.);
      col += spec * vec3(1., .95, .9) * 1.6;
      float zz = uZ; float wgt = (1. - 1. / zz) / (1. - 1. / 40.);
      vec2 tuv = mix(vec2(.5), uC, wgt) + (vUv - .5) / zz;
      float m = texture2D(tText, tuv).r;
      col *= 1. + .9 * (1. - wgt) + .5 * (1. - smoothstep(.25, .75, m));
      gl_FragColor = vec4(col * m * uFade, 1.);
    }` });
const q6 = new THREE.Mesh(new THREE.PlaneGeometry(2, 2), m6); q6.frustumCulled = false; s6.add(q6);
function renderS6(t) {
  m6.uniforms.uT.value = t;
  m6.uniforms.uZ.value = Math.exp(lerp(Math.log(40), 0, E.cubicInOut(seg(t, 1.08, 1.7))));
  m6.uniforms.uFade.value = ss(-0.09, 0.08, t);
  const rip = [0, 1, 2, 3].reduce((s, i) => s + Math.exp(-Math.max(0, t - i * B) * 9) * (t >= i * B ? 1 : 0), 0);
  return { bloom: 0.4 + 0.25 * rip, th: 0.85, exp: 1.0 + 0.12 * rip, ca: 0.018 + 0.12 * rip, vig: 0.75, flash: 0, sat: 1.05 };
}

// -------------------------------------------------------------- dispatch
let ready = false, cleared = false;
function renderAt(time) {
  if (!ready) return;
  if (time < 5.6 || time >= 11.3) {
    if (!cleared) { renderer.setRenderTarget(null); renderer.setClearColor(0x000000, 1); renderer.clear(); cleared = true; }
    return;
  }
  cleared = false;
  renderer.setRenderTarget(rtS); renderer.setClearColor(0x000000, 1); renderer.clear();
  let p;
  if (time < 7.5) { p = renderS4(Math.max(0, time - bt(12))); renderer.render(s4, cam4); }
  else if (time < bt(20) - 0.09) { p = renderS5(time - bt(16)); renderer.render(s5, cam5); }
  else {
    p = renderS6(time - bt(20)); renderer.render(s6, fsCam);
    if (time < bt(20) + 0.2) { renderS5(time - bt(16)); renderer.autoClear = false; renderer.render(s5, cam5); renderer.autoClear = true; }
  }
  post(p);
}
window.addEventListener('hf-seek', e => renderAt(e.detail.time));
async function build() {
  if (MEASURE) return;
  await new Promise(r => setTimeout(r, 0));
  await Promise.all([document.fonts.load('900 380px Archivo'), document.fonts.load('900 400px Archivo')]);
  s4.environment = studio();
  await sampleText('MOTION', NP);
  drawFluid();
  ready = true;
}
build().then(() => { renderAt(window.__hfThreeTime || 0); resolveReady(); });
"""

MEASURE_JS = r"""
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.addInitScript(() => { window.__timelines = {}; });
  await p.goto('file://' + process.argv[2] + '?measure');
  await p.evaluate(async () => { await document.fonts.ready; await Promise.all(['900 250px Archivo', '800 232px Archivo', 'italic 400 84px "Instrument Serif"'].map(f => document.fonts.load(f))); });
  await p.waitForTimeout(300);
  const m = await p.evaluate(() => {
    const c = el => { const r = el.getBoundingClientRect(); return [r.left + r.width / 2, r.top + r.height / 2]; };
    const r4 = document.getElementById('ring4').getBoundingClientRect();
    const ps = document.getElementById('pslot').getBoundingClientRect();
    const nm = document.querySelector('#name .nl').getBoundingClientRect();
    return { ring: [r4.left + r4.width / 2, r4.top + r4.height / 2], letters: [...document.querySelectorAll('#name .nl')].map(c),
      pslot: [ps.left + ps.width / 2 - 2, nm.top + nm.height * 0.832 - 29], nameBox: [nm.top, nm.height] };
  });
  console.log(JSON.stringify(m));
  await b.close();
})();
"""


def page(measure):
    zoom = ZOOM
    pw, ph = round(W * zoom), round(H * zoom)
    mb = open(MB_SNIPPET).read()
    mb = mb[mb.index("<script>"):]
    body = s1_html() + s3_html() + s2_html() + s7_html() + s8_html()
    tl_js = (TL_JS.replace("%%MEASURE%%", json.dumps(measure)).replace("%%SHAPES%%", json.dumps(SHAPES))
             .replace("%%DUR%%", str(DUR)))
    gl_js = GL_JS.replace("%%ZOOM%%", repr(zoom))
    css = CSS.replace("%%CIRCLE%%", SHAPES["circle"])
    plugin_tags = "\n".join(f'<script src="{p}.min.js"></script>' for p in PLUGINS)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width={pw}, height={ph}">
<title>Claude — Showreel 2026</title>
<script src="gsap.min.js"></script>
{plugin_tags}
<script type="importmap">{{"imports":{{"three":"./three/three.module.js"}}}}</script>
<style>
{FONTS}
{css}
.stage{{zoom:{zoom}}}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-width="{pw}" data-height="{ph}" data-duration="{DUR}">
<div class="stage">
<canvas id="gl"></canvas>
{body}
<div id="flash"></div>
<div id="vig"></div>
<div id="grain"></div>
{HUD}
</div>
<audio id="music" src="music.wav" data-start="0" data-duration="{DUR}" data-track-index="9"></audio>
</div>
{mb}
<script>
{tl_js}
</script>
<script type="module">
{gl_js}
</script>
</body>
</html>
"""


def build():
    os.makedirs(os.path.join(OUT, "fonts"), exist_ok=True)
    for f in os.listdir(os.path.join(ADS, "fonts")):
        if f.endswith(".woff2"):
            shutil.copy(os.path.join(ADS, "fonts", f), os.path.join(OUT, "fonts", f))
    shutil.copy(os.path.join(ADS, "gsap.min.js"), OUT)
    for p in PLUGINS:
        shutil.copy(os.path.join(DIST, p + ".min.js"), OUT)
    if not os.path.exists(os.path.join(OUT, "three")):
        shutil.copytree(os.path.join(ADS, "three"), os.path.join(OUT, "three"))
    png_noise(os.path.join(OUT, "noise.png"))
    mfile = os.path.join(HERE, "measure.json")
    if MEASURE:
        measure = {"ring": [560, 870], "letters": [[960, 540]] * 6, "pslot": [1500, 520]}
    else:
        measure = json.load(open(mfile))
        wav = os.path.join(OUT, "music.wav")
        src = os.path.join(HERE, "out", "music.wav")
        if not os.path.exists(src):
            subprocess.run([sys.executable, os.path.join(HERE, "reel_synth.py"), os.path.join(HERE, "out")], check=True)
        shutil.copy(src, wav)
    with open(os.path.join(OUT, "index.html"), "w") as fh:
        fh.write(page(measure))
    if MEASURE:
        js = os.path.join(HERE, "measure.js")
        open(js, "w").write(MEASURE_JS)
        res = subprocess.run(["node", js, os.path.join(OUT, "index.html")], check=True, capture_output=True, text=True,
                             cwd=SCRATCH)
        m = json.loads(res.stdout.strip().splitlines()[-1])
        json.dump(m, open(mfile, "w"), indent=1)
        print("measured", m)
    else:
        print("built", OUT, round(W * ZOOM), "x", round(H * ZOOM))


if __name__ == "__main__":
    build()
