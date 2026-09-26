"""XForward — "Loops → Forward": a 20 s brand film at showreel level (HyperFrames).

Busywork is drawn as loops (the site's topographic contour lines); the XForward
chevron cuts through them, maps the business, spawns AI agents, turns loops into
forward flow, climbs the ROI summit and locks into the X logo.

10 bars at 128 BPM + a 1.25 s tail. DOM/GSAP for type and cards; one Three.js
canvas (contours, isometric 3D map, particles, terrain) with a hand-written
bloom/tonemap pass, driven by HyperFrames' `hf-seek` time.

  python3 xf_build.py              draft (zoom 0.5 -> 960x540)
  python3 xf_build.py --zoom 1     full HD
  python3 xf_build.py --measure    zoom-1 layout pass -> measure.json
"""
import json, os, random, shutil, struct, subprocess, sys, zlib

HERE = os.path.dirname(os.path.abspath(__file__))
ADS = os.path.dirname(HERE)
DIST = os.path.join(ADS, "vendor", "gsap")
MB_SNIPPET = os.path.join(ADS, "vendor", "motion-blur.html")
MEASURE = "--measure" in sys.argv
ZOOM = 1.0 if MEASURE else float(sys.argv[sys.argv.index("--zoom") + 1]) if "--zoom" in sys.argv else 0.5
OUT = os.path.join(ADS, "projects", "xforward-reel-measure" if MEASURE else "xforward-reel")
W, H, DUR = 1920, 1080, 20.0
PLUGINS = ["CustomEase", "CustomWiggle", "DrawSVGPlugin"]
FONTS = open(os.path.join(ADS, "fonts", "fonts.css")).read().replace("../fonts/", "fonts/")
CHEV = "M5 5l7 7-7 7"


def png_noise(path, n=256, seed=7):
    r = random.Random(seed)
    raw = b"".join(b"\x00" + bytes(r.randrange(256) for _ in range(n)) for _ in range(n))

    def chunk(t, d):
        return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)

    with open(path, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", n, n, 8, 0, 0, 0, 0))
                + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))


def words(text, cls="wd"):
    out = []
    for w in text.split(" "):
        if w.startswith("*") and w.endswith("*"):
            out.append(f'<span class="mw"><span class="{cls} acc">{w[1:-1]}</span></span>')
        else:
            out.append(f'<span class="mw"><span class="{cls}">{w}</span></span>')
    return " ".join(out)


def ring_text(r, text, reps):
    return (f'<path id="rp{r}" d="M960,540 m-{r},0 a{r},{r} 0 1,1 {2 * r},0 a{r},{r} 0 1,1 -{2 * r},0"/>',
            f'<text><textPath href="#rp{r}">{text * reps}</textPath></text>')


def s1_html():
    defs, texts = [], []
    for r, t, n in ((440, "COPY · PASTE · CHASE · REMIND · RE-TYPE · RESCHEDULE · FOLLOW UP · ", 2),
                    (340, "INVOICES · QUOTES · INBOX · DATA ENTRY · CALLBACKS · REPORTS · ", 2),
                    (250, "SAME TASKS · EVERY DAY · ", 4)):
        d, x = ring_text(r, t, n)
        defs.append(d)
        texts.append(f'<svg class="ring" id="ring{r}" viewBox="0 0 1920 1080"><defs>{d}</defs>{x}</svg>')
    wordsC = "".join(f'<div class="cw" id="cw{i}">{w}</div>' for i, w in enumerate(["Copy.", "Paste.", "Chase.", "Repeat."]))
    return f"""
<section id="s1" class="clip shot" data-start="0" data-duration="1.9">
  <div id="rings">{''.join(texts)}</div>
  {wordsC}
</section>"""


def s2_html():
    reel = "".join(f"<b>{d % 10}</b>" for d in range(20))
    ticks = "".join(f'<i class="tk" style="transform:rotate({a}deg)"></i>' for a in range(0, 360, 15))
    return f"""
<section id="s2" class="clip shot" data-start="1.875" data-duration="1.875">
  <div id="cost">
    <svg id="dial" viewBox="0 0 800 800"><circle id="dialc" cx="400" cy="400" r="330"/></svg>
    <div id="ticks">{ticks}</div>
    <div id="num"><div class="dg"><div class="reel" id="ra">{reel}</div></div><div class="dg"><div class="reel" id="rb">{reel}</div></div><span class="unit">h</span></div>
    <div id="perwk" class="mono">per week, per team</div>
    <div id="lost" class="hl">{words("lost to *busywork.*")}</div>
  </div>
</section>"""


def s3_html():
    return f"""
<section id="s3" class="clip shot" data-start="3.75" data-duration="1.9">
  <div id="eng" class="hl">{words("We send an")} <span class="mw"><span class="wd em" id="engw">engineer.</span></span></div>
  <div id="notdeck" class="hl2">Not a <span id="sd">slide deck.</span></div>
  <i id="strike"></i>
  <div id="engcap" class="mono">Senior · forward-deployed · inside your team</div>
</section>
<div id="chev3" class="clip" data-start="3.6" data-duration="2.05" data-hf-motion-blur='{{"samplesPerFrame":24}}'><svg viewBox="0 0 24 24"><path d="{CHEV}"/></svg></div>
<div id="wipe" class="clip" data-start="5.3" data-duration="0.35"></div>"""


def heads_html():
    return f"""
<section id="h4" class="clip shot hls" data-start="5.625" data-duration="1.875">
  <div class="tag mono">Step 1 — Map</div>
  <div class="hl">{words("We map how the work")}<br>{words("*really* flows.")}</div>
</section>
<section id="h5" class="clip shot hls" data-start="7.5" data-duration="1.875">
  <div class="tag mono">Step 2 — Build</div>
  <div class="hl">{words("We build *AI* *agents*")}<br>{words("that do the work.")}</div>
</section>
<section id="h6" class="clip shot hls dark" data-start="9.375" data-duration="1.875">
  <div class="tag mono">Step 3 — Run</div>
  <div class="hl">{words("They work *24/7.*")}</div>
  <div class="hl sub">{words("Your team gets its *week* back.")}</div>
</section>
<section id="h7" class="clip shot hls dark" data-start="11.25" data-duration="1.875">
  <div class="tag mono">Step 4 — Stay</div>
  <div class="hl">{words("We stay until the agents do the job")}</div>
  <div class="hl sub">{words("and you see the *ROI.*")}</div>
  <div id="roipin" class="mono"><i></i>ROI</div>
</section>"""


PROOF = [
    ("var(--co)", "var(--paper)", "&lt; 60 s", "First reply to every lead.", "Home services · Lead-to-booking agent", "sms"),
    ("var(--paper)", "var(--ink)", "0", "Orders typed by hand.", "Distribution · Order-entry agent", "erp"),
    ("var(--ink)", "var(--paper)", "24/7", "Patients book themselves.", "Clinics · Front-desk agent", "cal"),
    ("var(--peri)", "var(--ink)", "&lt; 2 min", "Support response time.", "E-commerce · Support agent", "tix"),
]


def proof_ui(kind):
    if kind == "sms":
        return ('<div class="ui sms"><div class="bub in">New lead · AC not cooling, can someone come today?</div>'
                '<div class="bub out">Yes! Booked for 4:30 PM. A tech will text on the way. ✓</div></div>')
    if kind == "erp":
        rows = "".join(f'<div class="row"><span>{a}</span><span>{b}</span><span class="ok">✓</span></div>'
                       for a, b in (("SKU-4471", "× 120"), ("SKU-2208", "× 36"), ("SKU-9310", "× 8")))
        return f'<div class="ui erp"><div class="pdf">PO-10482.pdf</div><div class="tbl">{rows}</div></div>'
    if kind == "cal":
        cells = "".join(f'<i class="c{(i * 7) % 5}"></i>' for i in range(20))
        return f'<div class="ui cal"><div class="cg">{cells}</div></div>'
    return ('<div class="ui tix"><div class="tk1">“Where is my order #5812?”</div>'
            '<div class="tk2">Resolved · tracking link sent ✓</div></div>')


def s8_html():
    t0, beat = 13.125, 0.46875
    out = []
    for i, (bg, fg, big, lab, tag, ui) in enumerate(PROOF):
        out.append(f"""<section id="pc{i}" class="clip shot pcard" data-start="{t0 + i * beat:.6f}" data-duration="{beat:.6f}" style="background:{bg};color:{fg}">
  <div class="pin"><div class="ptag mono">{tag}</div><div class="pbig">{big}</div><div class="plab">{lab}</div></div>
  {proof_ui(ui)}
  <div class="pnote mono">Target outcomes · example projects</div>
</section>""")
    return "\n".join(out)


def end_html():
    return f"""
<section id="s9" class="clip shot" data-start="15" data-duration="5">
  <div id="lockup"><svg id="mk" viewBox="0 0 24 24"><path class="m1" d="{CHEV}"/><path class="m2" d="{CHEV}"/></svg><span id="fwd">Forward</span></div>
  <div id="tagl">AI agents, built into your business.</div>
  <div id="cta"><span>Book a free call</span><i>→</i></div>
  <div id="url" class="mono">xforward.ca</div>
  <i id="ring9"></i>
</section>
<div id="lgpair" class="clip" data-start="14.6" data-duration="5.4">
  <div id="lg1" data-hf-motion-blur='{{"samplesPerFrame":24}}'><svg viewBox="0 0 24 24"><path d="{CHEV}"/></svg></div>
  <div id="lg2" data-hf-motion-blur='{{"samplesPerFrame":24}}'><svg viewBox="0 0 24 24" style="transform:scaleX(-1)"><path d="{CHEV}"/></svg></div>
</div>"""


HUD = """
<div id="hud" class="mono">
  <div class="h tl"><svg class="hm" viewBox="0 0 24 24"><path class="m1" d="M5 5l7 7-7 7"/><path class="m2" d="M5 5l7 7-7 7"/></svg>XForward</div>
  <div class="h tr"><i class="rec"></i><span id="st">MON 08:02</span></div>
  <div class="h bl"><span id="chn">01</span><span class="dim">/10</span><span id="chl">THE LOOP</span></div>
  <div class="h br">""" + "".join('<i class="seg"><i></i></i>' for _ in range(10)) + """</div>
</div>"""

CSS = r"""
:root{--ink:#0A0B0D;--ink2:#0E1210;--paper:#F1F2EE;--raise:#FFFFFF;--co:#2334E0;--peri:#8C96FF;--muted:#5B645F;--muted2:#868D98;--line:#D7DBD4}
html,body{margin:0;background:#000}
#root{position:relative;width:100%;height:100%;overflow:hidden;background:#0A0B0D}
.stage{position:absolute;left:0;top:0;width:1920px;height:1080px;overflow:hidden;font-family:'Archivo',sans-serif;color:var(--paper)}
#gl{position:absolute;left:0;top:0;width:1920px;height:1080px;display:block;z-index:1}
.shot{position:absolute;left:0;top:0;width:1920px;height:1080px;overflow:hidden}
.mono{font-family:'IBM Plex Mono',monospace;text-transform:uppercase;letter-spacing:.18em}
.hl{font-weight:800;letter-spacing:-.025em;line-height:1.02;font-variation-settings:'wdth' 100}
.mw{display:inline-block;overflow:hidden;vertical-align:top;padding:0 .02em .08em;margin:0 -.02em -.08em}
.wd{display:inline-block}
.acc{color:var(--peri)}
/* 01 loop */
#s1{z-index:5}
.ring{position:absolute;left:0;top:0;width:1920px;height:1080px;transform-origin:960px 540px;overflow:visible}
.ring text{font:500 25px 'IBM Plex Mono',monospace;letter-spacing:.2em;fill:#7E8591}
#ring340 text{font-size:23px;fill:#5E6571}
#ring250 text{font-size:21px;fill:#A7AEB9}
.cw{position:absolute;left:0;right:0;top:452px;text-align:center;font:800 170px/1 'Archivo';letter-spacing:-.03em;color:var(--paper);opacity:0}
#cw0{opacity:1}
/* 02 cost */
#s2{z-index:5}
#cost{position:absolute;inset:0;transform-origin:960px 500px}
#dial{position:absolute;left:560px;top:100px;width:800px;height:800px;overflow:visible}
#dialc{fill:none;stroke:rgba(236,238,242,.55);stroke-width:2;transform:rotate(-90deg);transform-origin:400px 400px}
#ticks{position:absolute;left:960px;top:500px;width:0;height:0}
.tk{position:absolute;left:-1px;top:-352px;width:2px;height:14px;background:rgba(236,238,242,.35);transform-origin:1px 352px}
#num{position:absolute;left:0;right:0;top:300px;display:flex;justify-content:center;align-items:flex-end;gap:6px}
.dg{width:250px;height:360px;overflow:hidden}
.reel b{display:block;height:360px;font:900 440px/360px 'Archivo';font-variation-settings:'wdth' 88;text-align:center;color:var(--paper)}
.unit{font:800 150px/1 'Archivo';color:var(--peri);margin:0 0 20px 16px}
#perwk{position:absolute;left:0;right:0;top:688px;text-align:center;font-size:18px;color:#868D98;opacity:0}
#lost{position:absolute;left:0;right:0;top:740px;text-align:center;font-size:84px;color:var(--paper)}
/* 03 engineer */
#s3{z-index:5}
#eng{position:absolute;left:640px;top:370px;font-size:112px;color:var(--paper);white-space:nowrap}
#eng .em{position:relative;color:var(--peri)}
#engw::after{content:'';position:absolute;left:0;right:0;bottom:.04em;height:.07em;background:var(--peri);transform:scaleX(var(--u,0));transform-origin:0 50%}
#notdeck{position:absolute;left:644px;top:520px;font:500 64px/1.1 'Archivo';color:#868D98;opacity:0}
#strike{position:absolute;height:5px;background:var(--peri);transform-origin:0 50%;transform:scaleX(0)}
#engcap{position:absolute;left:648px;top:644px;font-size:17px;color:var(--peri);clip-path:inset(0 100% 0 0)}
#chev3{position:absolute;left:-150px;top:390px;width:300px;height:300px;z-index:9}
#chev3 svg,#lg1 svg,#lg2 svg{width:100%;height:100%;overflow:visible}
#chev3 path{fill:none;stroke:var(--peri);stroke-width:2.6;stroke-linecap:round;stroke-linejoin:round}
#wipe{position:absolute;inset:0;background:var(--paper);z-index:8;clip-path:inset(0 100% 0 0)}
/* headlines over GL */
.hls{z-index:6;pointer-events:none}
.hls .tag{position:absolute;left:112px;top:110px;font-size:16px;color:var(--co)}
.hls .hl{position:absolute;left:108px;top:146px;font-size:76px;color:var(--ink2);white-space:nowrap}
.hls .hl .acc{color:var(--co)}
.hls.dark .tag{color:var(--peri)}
.hls.dark .hl{color:var(--paper)}
.hls.dark .hl .acc{color:var(--peri)}
.hls .hl.sub{top:236px;font-size:60px;font-weight:700;color:#868D98}
.hls.dark .hl.sub{color:#A7AEB9}
#roipin{position:absolute;left:0;top:0;padding:10px 18px 10px 14px;border-radius:40px;background:var(--peri);color:var(--ink);font-size:20px;font-weight:600;letter-spacing:.14em;transform-origin:0 100%;opacity:0;white-space:nowrap}
#roipin i{display:inline-block;width:10px;height:10px;border-radius:50%;background:var(--ink);margin-right:10px;vertical-align:1px}
/* 08 proof */
.pcard{z-index:8}
.pin{position:absolute;left:150px;top:250px}
.ptag{font-size:18px;opacity:.75;margin-bottom:26px}
.pbig{font:900 300px/0.92 'Archivo';letter-spacing:-.04em;font-variation-settings:'wdth' 100}
.plab{font:700 62px/1.1 'Archivo';letter-spacing:-.02em;margin-top:26px}
.pnote{position:absolute;left:150px;bottom:112px;font-size:14px;opacity:.55}
.ui{position:absolute;right:150px;top:330px;width:560px}
.sms .bub{font:500 28px/1.3 'Archivo';padding:22px 28px;border-radius:28px;margin-bottom:22px;max-width:470px}
.sms .in{background:rgba(241,242,238,.16);color:var(--paper);border-bottom-left-radius:8px}
.sms .out{background:var(--paper);color:var(--ink2);margin-left:auto;border-bottom-right-radius:8px}
.erp .pdf{font:600 26px 'IBM Plex Mono';padding:22px 26px;border:2px solid var(--ink2);border-radius:12px;width:300px;margin-bottom:28px;color:var(--ink2)}
.erp .row{display:flex;justify-content:space-between;font:500 28px 'IBM Plex Mono';padding:16px 20px;border-bottom:2px solid var(--line);color:var(--ink2)}
.erp .ok{color:var(--co);font-weight:700}
.cal .cg{display:grid;grid-template-columns:repeat(5,1fr);gap:12px}
.cal .cg i{display:block;height:70px;border-radius:10px;background:rgba(241,242,238,.1)}
.cal .cg i.c0,.cal .cg i.c3{background:var(--peri)}
.tix .tk1,.tix .tk2{font:500 30px/1.3 'Archivo';padding:26px 30px;border-radius:18px;margin-bottom:22px}
.tix .tk1{background:rgba(10,11,13,.1);color:var(--ink2)}
.tix .tk2{background:var(--ink2);color:var(--paper)}
/* 09 end */
#s9{z-index:7}
#lockup{position:absolute;left:0;right:0;top:330px;display:flex;justify-content:center;align-items:flex-end;white-space:nowrap}
#mk{width:236px;height:236px;margin:0 -30px -25px -58px;opacity:0;overflow:visible}
#mk path,.hm path{fill:none;stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round}
#mk .m1,.hm .m1{stroke:var(--ink2)}
#mk .m2,.hm .m2{stroke:var(--co);transform-box:fill-box;transform-origin:center;transform:scaleX(-1)}
#fwd{font:800 196px/1 'Archivo';letter-spacing:-.035em;color:var(--ink2);font-variation-settings:'wdth' var(--wd,100);clip-path:inset(-10% 100% -10% 0)}
#tagl{position:absolute;left:0;right:0;top:600px;text-align:center;font:500 52px/1.2 'Archivo';letter-spacing:-.01em;color:var(--muted);opacity:0}
#cta{position:absolute;left:50%;top:720px;height:92px;padding:0 44px 0 48px;margin-left:-262px;border-radius:60px;background:var(--co);color:#fff;display:flex;align-items:center;gap:22px;font:700 38px 'Archivo';letter-spacing:-.01em;transform:scale(0)}
#cta i{font-style:normal;display:inline-block}
#url{position:absolute;left:0;right:0;top:846px;text-align:center;font-size:20px;color:var(--muted);opacity:0}
#ring9{position:absolute;left:910px;top:420px;width:100px;height:100px;border-radius:50%;border:3px solid var(--co);box-sizing:border-box;opacity:0}
#lgpair{position:absolute;left:0;top:0;width:1920px;height:1080px;z-index:9;pointer-events:none}
#lg1,#lg2{position:absolute;left:810px;top:320px;width:300px;height:300px}
#lg1 path,#lg2 path{fill:none;stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round}
#lg1 path{stroke:var(--ink2)}
#lg2 path{stroke:var(--co)}
/* finishing */
#flash{position:absolute;inset:0;background:#fff;opacity:0;z-index:20}
#vig{position:absolute;inset:0;background:radial-gradient(ellipse 72% 72% at 50% 50%,transparent 60%,rgba(0,0,0,.3) 100%);opacity:0;z-index:21}
#grain{position:absolute;inset:0;background:url(noise.png);background-size:512px 512px;image-rendering:pixelated;mix-blend-mode:overlay;opacity:0;z-index:22}
#hud{position:absolute;inset:0;z-index:30;color:var(--paper);font-size:15px;font-weight:500;letter-spacing:.2em}
#hud .h{position:absolute;white-space:nowrap;display:flex;align-items:center}
#hud .tl{left:56px;top:40px}#hud .tr{right:56px;top:44px}#hud .bl{left:56px;bottom:44px}#hud .br{right:56px;bottom:50px;gap:6px}
#hud .hm{width:26px;height:26px;margin-right:10px}
#hud .hm .m1{stroke:currentColor}
#hud .dim{opacity:.45;margin:0 .5em}
#hud #chl{margin-left:.9em}
#hud .rec{display:inline-block;width:9px;height:9px;border-radius:50%;background:var(--peri);margin-right:12px}
#hud .seg{display:block;width:30px;height:3px;position:relative}
#hud .seg::before{content:'';position:absolute;inset:0;background:currentColor;opacity:.25}
#hud .seg i{position:absolute;left:0;top:0;width:100%;height:100%;background:currentColor;transform-origin:0 50%;transform:scaleX(0)}
"""

TL_JS = r"""
gsap.registerPlugin(CustomEase, CustomWiggle, DrawSVGPlugin);
CustomWiggle.create('shake6', { wiggles: 6, type: 'easeOut' });
const MEASURE = /measure/.test(location.search);
const B = 60 / 128, BAR = 4 * B, bt = n => n * B;
const M = %%MEASURE%%;
const PAPER = '#F1F2EE', INK = '#0E1210', CO = '#2334E0', PERI = '#8C96FF';
function rng(seed){let s=seed>>>0;return()=>((s=Math.imul(s^(s>>>15),2246822507)^Math.imul(s^(s>>>13),3266489909),(s^=s>>>16)>>>0)/4294967296)}
const $ = s => document.querySelector(s), $$ = s => gsap.utils.toArray(s);
const tl = gsap.timeline({ paused: true });
const rise = (sel, t, st = 0.05, d = 0.55) => tl.fromTo(sel, { yPercent: 110 }, { yPercent: 0, duration: d, ease: 'expo.out', stagger: st }, t);
if (!MEASURE) {
// ======================================================== 01 THE LOOP  0 – 1.875
[['#ring440', 70, 0.8], ['#ring340', -95, 0.86], ['#ring250', 140, 0.9]].forEach(([s, rot, sc]) => {
  tl.fromTo(s, { scale: sc, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.6, ease: 'expo.out' }, 0.001);
  tl.fromTo(s, { rotation: 0 }, { rotation: rot, duration: bt(3.6), ease: 'power1.in', immediateRender: false }, 0.001);
  tl.fromTo(s, { scale: 1 }, { scale: 0.02, rotation: `+=${rot * 2.2}`, duration: 0.3, ease: 'expo.in', immediateRender: false }, bt(4) - 0.3);
});
$$('.cw').forEach((w, i) => {
  if (i) tl.set(w, { opacity: 1 }, bt(i));
  tl.fromTo(w, { scale: 1.3 }, { scale: 1, duration: 0.34, ease: 'expo.out', immediateRender: !i }, i ? bt(i) : 0);
  tl.set(w, { opacity: 0 }, bt(i + 1) - 0.001);
});

// ======================================================== 02 THE COST  1.875 – 3.75
tl.fromTo('#dialc', { drawSVG: '0% 0%' }, { drawSVG: '0% 100%', duration: bt(3), ease: 'power2.inOut' }, bt(4));
tl.fromTo('.tk', { opacity: 0 }, { opacity: 1, duration: 0.01, stagger: bt(3) / 24 }, bt(4));
tl.fromTo('#ra', { y: 0 }, { y: -360 * 12, duration: 0.62, ease: 'expo.out' }, bt(4));
tl.fromTo('#rb', { y: 0 }, { y: -360 * 17, duration: 0.74, ease: 'expo.out' }, bt(4));
tl.fromTo('#num', { scale: 1.25 }, { scale: 1, duration: 0.5, ease: 'expo.out' }, bt(4));
tl.fromTo('.unit', { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 0.4, ease: 'expo.out' }, bt(4) + 0.3);
tl.to('#perwk', { opacity: 1, duration: 0.3 }, bt(5));
rise('#lost .wd', bt(6), 0.06);
tl.fromTo('#cost', { scale: 1 }, { scale: 1.06, duration: bt(3.2), ease: 'sine.inOut', immediateRender: false }, bt(4.2));
tl.fromTo('#cost', { scale: 1.06, opacity: 1 }, { scale: 0.02, opacity: 0.4, duration: 0.24, ease: 'expo.in', immediateRender: false }, bt(7.5));

// ======================================================== 03 THE ENGINEER  3.75 – 5.625
const T3 = bt(8);
gsap.set('#chev3', { x: -400 });
tl.fromTo('#chev3', { x: -400 }, { x: 530, duration: 0.3, ease: 'expo.out', immediateRender: false }, T3);
tl.fromTo('#chev3', { y: 0 }, { y: -8, duration: 0.7, ease: 'sine.inOut', yoyo: true, repeat: 1, immediateRender: false }, T3 + 0.3);
tl.fromTo('#chev3', { x: 530 }, { x: 2300, duration: 0.24, ease: 'expo.in', immediateRender: false }, bt(12) - 0.24);
rise('#eng .wd', T3 + 0.12, 0.06, 0.6);
tl.fromTo('#engw', { '--u': 0 }, { '--u': 1, duration: 0.5, ease: 'expo.inOut', immediateRender: false }, T3 + 0.55);
tl.fromTo('#notdeck', { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.4, ease: 'expo.out' }, bt(10));
gsap.set('#strike', { left: M.sd[0], top: M.sd[1] + M.sd[3] * 0.55, width: M.sd[2] });
tl.fromTo('#strike', { scaleX: 0 }, { scaleX: 1, duration: 0.22, ease: 'power3.out', immediateRender: false }, bt(10.5));
tl.to('#engcap', { clipPath: 'inset(0% 0% 0% 0%)', duration: 0.4, ease: 'power2.out' }, bt(11));
tl.fromTo('#wipe', { clipPath: 'inset(0% 100% 0% 0%)' }, { clipPath: 'inset(0% 0% 0% 0%)', duration: 0.24, ease: 'expo.in', immediateRender: false }, bt(12) - 0.24);

// ======================================================== 04–07 headlines over WebGL
[['#h4', bt(12)], ['#h5', bt(16)], ['#h6', bt(20)], ['#h7', bt(24)]].forEach(([h, t]) => {
  tl.fromTo(`${h} .tag`, { clipPath: 'inset(0% 100% 0% 0%)' }, { clipPath: 'inset(0% 0% 0% 0%)', duration: 0.35, ease: 'power2.out' }, t + 0.05);
  rise(`${h} .hl:not(.sub) .wd`, t + 0.1, 0.045);
});
rise('#h6 .sub .wd', bt(22), 0.05);
rise('#h7 .sub .wd', bt(26), 0.06);

// ======================================================== 08 THE PROOF  13.125 – 15
$$('.pcard').forEach((c, i) => {
  const t = bt(28 + i);
  tl.fromTo(c.querySelector('.pin'), { x: i % 2 ? 120 : -120 }, { x: 0, duration: 0.3, ease: 'expo.out' }, t);
  tl.fromTo(c.querySelector('.pbig'), { scale: 1.2, transformOrigin: '0% 80%' }, { scale: 1, duration: 0.3, ease: 'expo.out' }, t);
  tl.fromTo(c.querySelector('.ui'), { y: 80, opacity: 0 }, { y: 0, opacity: 1, duration: 0.3, ease: 'expo.out' }, t + 0.06);
  const ui = c.querySelectorAll('.ui > *, .ui .row, .ui .cg i');
  tl.fromTo(ui, { scale: 0.85, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.18, ease: 'back.out(2)', stagger: { amount: 0.16 } }, t + 0.06);
});

// ======================================================== 09–10 XFORWARD  15 – 20
const T9 = bt(32);
tl.fromTo('#lg1', { x: -1400 }, { x: 0, duration: 0.3, ease: 'power2.in', immediateRender: false }, T9 - 0.3);
tl.fromTo('#lg2', { x: 1400 }, { x: 0, duration: 0.3, ease: 'power2.in', immediateRender: false }, T9 - 0.3);
gsap.set(['#lg1', '#lg2'], { x: (i) => i ? 1400 : -1400 });
tl.fromTo('#lgpair', { scale: 1.12 }, { scale: 1, duration: 0.5, ease: 'elastic.out(1,0.45)', transformOrigin: '960px 470px', immediateRender: false }, T9);
tl.fromTo('#ring9', { scale: 0.6, opacity: 1 }, { scale: 6, opacity: 0, duration: 0.7, ease: 'expo.out', immediateRender: false }, T9);
tl.fromTo('#flash', { opacity: 0.4 }, { opacity: 0, duration: 0.3, ease: 'expo.out', immediateRender: false }, T9);
// the pair becomes the X of the lockup
const pk = M.mk, s = pk[2] / 300;
tl.fromTo('#lgpair', { x: 0, y: 0 }, { x: (pk[0] + pk[2] / 2) - 960 - (1 - s) * 0, y: (pk[1] + pk[3] / 2) - 470, duration: 0.55, ease: 'expo.inOut', immediateRender: false }, T9 + 0.36);
tl.fromTo(['#lg1', '#lg2'], { scale: 1 }, { scale: s, duration: 0.55, ease: 'expo.inOut', immediateRender: false }, T9 + 0.36);
tl.fromTo('#fwd', { clipPath: 'inset(-10% 100% -10% 0%)', '--wd': 62 }, { clipPath: 'inset(-10% 0% -10% 0%)', '--wd': 100, duration: 0.7, ease: 'expo.out', immediateRender: false }, T9 + 0.62);
tl.fromTo('#tagl', { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.6, ease: 'expo.out', immediateRender: false }, bt(34));
tl.fromTo('#cta', { scale: 0 }, { scale: 1, duration: 0.5, ease: 'back.out(2.2)', immediateRender: false }, bt(36));
tl.fromTo('#url', { opacity: 0 }, { opacity: 1, duration: 0.5, immediateRender: false }, bt(36) + 0.2);
[37, 38, 39, 40, 41].forEach(b => tl.fromTo('#cta i', { x: 0 }, { x: 9, duration: B / 2, ease: 'power2.out', yoyo: true, repeat: 1, immediateRender: false }, bt(b)));
tl.fromTo('#cta', { scale: 1 }, { scale: 1.05, duration: 0.12, ease: 'power2.out', immediateRender: false }, bt(40));
tl.fromTo('#cta', { scale: 1.05 }, { scale: 1, duration: 0.5, ease: 'elastic.out(1,0.4)', immediateRender: false }, bt(40) + 0.12);

// ======================================================== drop flashes
tl.fromTo('#flash', { opacity: 0.35 }, { opacity: 0, duration: 0.3, ease: 'expo.out', immediateRender: false }, T3);

// ======================================================== HUD + finishing
tl.set(['#vig', '#grain'], { opacity: (i) => [1, 0.075][i] }, 0.001);
[[bt(12), 0.3], [bt(20), 1], [bt(28), 0.5], [bt(32), 0.12]].forEach(([t, o]) => tl.set('#vig', { opacity: o }, t));
[[0, PAPER], [bt(12), INK], [bt(20), PAPER], [bt(28), PAPER]].forEach(([t, c]) => tl.set('#hud', { color: c }, t || 0.001));
tl.set('#hud', { mixBlendMode: 'difference', color: PAPER }, bt(28));
tl.to('#hud', { opacity: 0, duration: 0.2 }, T9 - 0.1);
$$('#hud .seg i').forEach((s, k) => tl.fromTo(s, { scaleX: 0 }, { scaleX: 1, duration: BAR, ease: 'none', immediateRender: false }, k * BAR + 0.001));
const CH = ['THE LOOP', 'THE COST', 'THE ENGINEER', 'THE MAP', 'THE AGENTS', 'THE WORK', 'THE ROI', 'THE PROOF', 'XFORWARD', 'XFORWARD'];
const GLY = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/#+=';
function scr(txt, p, seed) { const r = rng(seed); let o = ''; for (let i = 0; i < txt.length; i++) { const c = txt[i]; o += (i < p * txt.length || c === ' ') ? c : GLY[Math.floor(r() * GLY.length)]; } return o; }
const DAYS = ['MON', 'TUE', 'WED', 'THU', 'FRI'];
const stEl = $('#st'), chnEl = $('#chn'), chlEl = $('#chl'), grEl = $('#grain');
function status(t) {
  if (t < bt(8)) { const p = Math.min(1, Math.pow(t / 3.6, 1.6)), m = Math.round(2 + p * 6364), d = Math.min(4, Math.floor((m + 480) / 1440)), mm = (m + 480) % 1440;
    return `${DAYS[d]} ${String(Math.floor(mm / 60)).padStart(2, '0')}:${String(mm % 60).padStart(2, '0')}`; }
  if (t < bt(16)) return 'ENGINEER ON SITE';
  if (t < bt(20)) return `AGENTS ONLINE · ${String(Math.round(24 * Math.min(1, Math.max(0, (t - bt(16) - 0.1) / 0.9)))).padStart(2, '0')}`;
  if (t < bt(24)) return `HOURS BACK / WEEK · ${String(Math.round(27 * Math.min(1, Math.max(0, (t - bt(20) - 0.2) / 1.4)))).padStart(2, '0')}`;
  if (t < bt(28)) return 'MEASURING ROI';
  return 'TARGET OUTCOMES';
}
function tick() {
  const t = tl.time(), f = Math.floor(t * 30 + 1e-6);
  stEl.textContent = status(t);
  const k = Math.min(9, Math.floor(t / BAR + 1e-6)), dt = t - k * BAR;
  chnEl.textContent = String(k + 1).padStart(2, '0');
  chlEl.textContent = scr(CH[k], Math.min(1, dt / 0.24), f * 7 + 3);
  const g = rng(f * 13 + 5); grEl.style.backgroundPosition = `${Math.floor(g() * 256) * 2}px ${Math.floor(g() * 256) * 2}px`;
}
tl.to({ p: 0 }, { p: 1, duration: %%DUR%%, ease: 'none', onUpdate: tick }, 0);
}
window.__timelines = window.__timelines || {};
window.__timelines["main"] = tl;
"""

GL_JS = r"""
import * as THREE from 'three';
import { RoomEnvironment } from './three/addons/RoomEnvironment.js';
const MEASURE = /measure/.test(location.search);
const Z = %%ZOOM%%, W = 1920, H = 1080, PXW = Math.round(W * Z), PXH = Math.round(H * Z), ASP = W / H;
const B = 60 / 128, bt = n => n * B;
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const seg = (t, a, b) => clamp((t - a) / (b - a));
const ss = (a, b, t) => { const x = seg(t, a, b); return x * x * (3 - 2 * x); };
const lerp = (a, b, k) => a + (b - a) * k;
const E = {
  expoOut: p => p >= 1 ? 1 : 1 - Math.pow(2, -10 * p), expoIn: p => p <= 0 ? 0 : Math.pow(2, 10 * p - 10),
  cubicOut: p => 1 - Math.pow(1 - p, 3), cubicInOut: p => p < .5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2,
  backOut: (p, s = 1.70158) => 1 + (s + 1) * Math.pow(p - 1, 3) + s * Math.pow(p - 1, 2),
};
function rng(seed){let s=seed>>>0;return()=>((s=Math.imul(s^(s>>>15),2246822507)^Math.imul(s^(s>>>13),3266489909),(s^=s>>>16)>>>0)/4294967296)}
window.__hf = window.__hf || {}; window.__hf.buildReady = window.__hf.buildReady || {};
let resolveReady; window.__hf.buildReady.main = new Promise(r => resolveReady = r);
const lin = hex => new THREE.Color(hex);   // THREE.Color converts sRGB hex to linear working space

// -------------------------------------------------------------- renderer + post
const canvas = document.getElementById('gl');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: false, preserveDrawingBuffer: true, alpha: false });
renderer.setPixelRatio(1); renderer.setSize(PXW, PXH, false);
renderer.outputColorSpace = THREE.LinearSRGBColorSpace; renderer.toneMapping = THREE.NoToneMapping;
renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
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
const compM = fsMat(`uniform sampler2D tS, tB1, tB2, tB3, tB4; uniform float uBloom, uExp, uCA, uVig, uFlash, uTone; varying vec2 vUv;
  vec3 neutral(vec3 c){ float x = min(c.r, min(c.g, c.b)); float o = x < .08 ? x - 6.25 * x * x : .04; c -= o;
    float pk = max(c.r, max(c.g, c.b)); if (pk < .76) return c; float d = .24; float np = 1. - d * d / (pk + d - .76);
    c *= np / pk; float g = 1. - 1. / (.15 * (pk - np) + 1.); return mix(c, vec3(np), g); }
  vec3 srgb(vec3 c){ c = clamp(c, 0., 1.); return mix(c * 12.92, 1.055 * pow(c, vec3(1. / 2.4)) - .055, step(.0031308, c)); }
  void main(){ vec2 d = vUv - .5; float r2 = dot(d, d); vec2 o = d * uCA * r2;
    vec3 c = vec3(texture2D(tS, vUv - o).r, texture2D(tS, vUv).g, texture2D(tS, vUv + o).b);
    if (any(isnan(c)) || any(isinf(c))) c = vec3(0.); c = min(c, vec3(64.));
    c += (texture2D(tB1, vUv).rgb * .5 + texture2D(tB2, vUv).rgb * .7 + texture2D(tB3, vUv).rgb * .9 + texture2D(tB4, vUv).rgb * 1.1) * uBloom;
    c *= uExp; c = uTone > .5 ? neutral(c) : c;
    c = srgb(c); c *= mix(1., smoothstep(1.05, .3, sqrt(r2) * 1.3), uVig); c = mix(c, vec3(1.), uFlash);
    gl_FragColor = vec4(c, 1.); }`,
  { tS: { value: rtS.texture }, tB1: { value: LV[0].a.texture }, tB2: { value: LV[1].a.texture }, tB3: { value: LV[2].a.texture }, tB4: { value: LV[3].a.texture },
    uBloom: { value: .5 }, uExp: { value: 1 }, uCA: { value: 0 }, uVig: { value: .6 }, uFlash: { value: 0 }, uTone: { value: 1 } });
function post(p) {
  if (p.bloom > 0) {
    brightM.uniforms.tIn.value = rtS.texture; brightM.uniforms.uTh.value = p.th; pass(brightM, LV[0].a);
    LV.forEach((L, i) => {
      if (i) { copyM.uniforms.tIn.value = LV[i - 1].a.texture; pass(copyM, L.a); }
      blurM.uniforms.tIn.value = L.a.texture; blurM.uniforms.uDir.value.set(1 / L.w, 0); pass(blurM, L.b);
      blurM.uniforms.tIn.value = L.b.texture; blurM.uniforms.uDir.value.set(0, 1 / L.h); pass(blurM, L.a);
    });
  }
  const u = compM.uniforms; u.uBloom.value = p.bloom; u.uExp.value = p.exp ?? 1; u.uCA.value = p.ca ?? 0; u.uVig.value = p.vig ?? .5;
  u.uFlash.value = p.flash ?? 0; u.uTone.value = p.tone ?? 1;
  pass(compM, null);
}

// -------------------------------------------------------------- A · contour loops (bars 1-3, end card)
const sC = new THREE.Scene();
const mC = new THREE.ShaderMaterial({ depthTest: false, depthWrite: false, vertexShader: VS,
  uniforms: { uT: { value: 0 }, uAsp: { value: ASP }, uLight: { value: 0 }, uWake: { value: 0 }, uAX: { value: -3 }, uDim: { value: 0 }, uTight: { value: 0 },
    uN: { value: 11 }, uP: { value: new THREE.Vector4(0, B, 2 * B, 3 * B) }, uPx: { value: PXH / 1080 } },
  fragmentShader: `uniform float uT, uAsp, uLight, uWake, uAX, uDim, uTight, uN, uPx; uniform vec4 uP; varying vec2 vUv;
    float h21(vec2 p){ p = fract(p * vec2(123.34, 456.21)); p += dot(p, p + 45.32); return fract(p.x * p.y); }
    float vn(vec2 p){ vec2 i = floor(p), f = fract(p); vec2 u = f * f * (3. - 2. * f);
      return mix(mix(h21(i), h21(i + vec2(1., 0.)), u.x), mix(h21(i + vec2(0., 1.)), h21(i + vec2(1., 1.)), u.x), u.y); }
    float fbm(vec2 p){ float s = 0., a = .5; mat2 m = mat2(1.6, 1.2, -1.2, 1.6); for (int i = 0; i < 4; i++){ s += a * vn(p); p = m * p; a *= .5; } return s; }
    void main(){
      vec2 p = (vUv - .5) * vec2(uAsp, 1.);
      float r = length(p), a = uT * .38 / (.55 + r * 1.6);
      vec2 ps = mat2(cos(a), -sin(a), sin(a), cos(a)) * p;
      float h = fbm(ps * 1.3 + vec2(3.1, 1.7)) + .1 * sin(r * 9. - uT * 2.4) * exp(-r * 1.5);
      for (int i = 0; i < 4; i++){ float dt = uT - uP[i]; if (dt > 0.) h += .045 * exp(-pow((r - dt * 1.7) * 7., 2.)) * exp(-dt * 2.2); }
      float wk = uWake * smoothstep(uAX + .02, uAX - .6, p.x);
      float hf = p.y * .78 + .012 * sin(p.x * 4. - uT * 5.) + 3.;
      float v = h * uN * (1. + uTight), vf = hf * uN;
      float dd = abs(fract(v - .5) - .5) / max(fwidth(v), 1e-5), df = abs(fract(vf - .5) - .5) / max(fwidth(vf), 1e-5);
      float maj = mix(1. - step(.5, mod(floor(v + .5), 5.)), 1. - step(.5, mod(floor(vf + .5), 5.)), step(.5, wk));
      float lw = mix(1.0, 1.7, maj) * uPx;
      float line = mix(1. - smoothstep(lw * .5, lw * .5 + 1., dd), 1. - smoothstep(lw * .5, lw * .5 + 1., df), wk);
      vec3 bg = mix(vec3(.003, .0034, .004), vec3(.879, .888, .855), uLight);
      vec3 lc = mix(mix(vec3(.02, .024, .03), vec3(.045, .05, .062), maj), mix(vec3(.73, .75, .71), vec3(.62, .65, .6), maj), uLight);
      vec3 wc = mix(vec3(.26, .30, 1.) * mix(.45, .9, maj), mix(vec3(.62, .65, .6), vec3(.017, .034, .745), .25 * maj), uLight);
      lc = mix(lc, wc, wk);
      gl_FragColor = vec4(mix(bg, lc, line * (1. - uDim)), 1.);
    }` });
const qC = new THREE.Mesh(new THREE.PlaneGeometry(2, 2), mC); qC.frustumCulled = false; sC.add(qC);
const T3 = bt(8), T12 = bt(12);
function arrowX(t) {
  if (t < T3) return -400;
  if (t < T3 + 0.3) return lerp(-400, 530, E.expoOut((t - T3) / 0.3));
  if (t < T12 - 0.24) return 530;
  return lerp(530, 2300, E.expoIn(seg(t, T12 - 0.24, T12)));
}
function renderC(t, light) {
  const u = mC.uniforms; u.uT.value = t; u.uLight.value = light ? 1 : 0;
  if (light) { u.uWake.value = 1; u.uAX.value = 4; u.uDim.value = 0; u.uTight.value = 0; u.uN.value = 9; }
  else {
    u.uN.value = 11;
    u.uWake.value = t >= T3 ? 1 : 0; u.uAX.value = (arrowX(t) / 1920 - 0.5) * ASP;
    u.uDim.value = t < bt(4) ? 0 : t < T3 ? lerp(0.45, 1, ss(bt(7.3), bt(7.9), t)) : 0;
    u.uTight.value = t < T3 ? 1.1 * E.expoIn(seg(t, bt(7), bt(8))) : 0;
  }
  renderer.render(sC, fsCam);
  if (light) return { bloom: 0, tone: 0, vig: 0, ca: 0 };
  const hit = Math.exp(-Math.max(0, t - T3) * 5) * (t >= T3 ? 1 : 0);
  return { bloom: 0.55 + 0.6 * hit, th: 0.25, exp: 1, ca: 0.02 + 0.25 * hit, vig: 0.65, tone: 1 };
}

// -------------------------------------------------------------- shared: capsule chevron geometry (the logo's round-cap stroke, in 3D)
function mergeGeos(geos) {
  const parts = geos.map(g => g.index ? g.toNonIndexed() : g);
  const n = parts.reduce((s, g) => s + g.attributes.position.count, 0);
  const pos = new Float32Array(n * 3), nor = new Float32Array(n * 3); let o = 0;
  parts.forEach(g => { pos.set(g.attributes.position.array, o * 3); nor.set(g.attributes.normal.array, o * 3); o += g.attributes.position.count; });
  const m = new THREE.BufferGeometry(); m.setAttribute('position', new THREE.BufferAttribute(pos, 3)); m.setAttribute('normal', new THREE.BufferAttribute(nor, 3)); return m;
}
function chevronGeo(r = 0.14, vertical = false) {
  const arms = [-45, 45].map((deg, i) => {
    const g = new THREE.CapsuleGeometry(r, 0.99, 6, 14); g.rotateZ(Math.PI / 2); g.rotateY(deg * Math.PI / 180);
    g.translate(0, 0, i ? 0.35 : -0.35); return g;
  });
  const m = mergeGeos(arms); if (vertical) m.rotateX(Math.PI / 2); return m;
}

// -------------------------------------------------------------- B · the isometric map (bars 4-5)
const sM = new THREE.Scene(); sM.background = lin('#F1F2EE');
const camM = new THREE.OrthographicCamera(-1, 1, 1, -1, 0.1, 200);
const EL0 = Math.atan(1 / Math.sqrt(2)), AZ0 = Math.PI / 4, F0 = 11.5;
function setIso(az, el, F, tx, tz) {
  const d = 50; camM.position.set(tx + d * Math.cos(el) * Math.sin(az), d * Math.sin(el), tz + d * Math.cos(el) * Math.cos(az));
  camM.up.set(0, 1, 0); camM.lookAt(tx, 0, tz);
  camM.left = -F / 2 * ASP; camM.right = F / 2 * ASP; camM.top = F / 2; camM.bottom = -F / 2; camM.updateProjectionMatrix();
}
const kpx = 1080 / F0;
const iso2w = (sx, sy) => { const a = sx / (0.70711 * kpx), b = sy / (0.40825 * kpx); return [(a + b) / 2, (b - a) / 2]; };
const NODES = [['INBOX', '62 emails / day', -330, 110], ['QUOTES', '18 requests / week', -40, -120], ['CRM', '1 200 contacts', 250, 150],
  ['INVOICES', '340 / month', 590, -70], ['CALENDAR', '45 bookings / week', 610, 300]].map(([n, s, x, y]) => { const [wx, wz] = iso2w(x, y); return { n, s, x: wx, z: wz }; });
const NT = NODES.map((_, i) => bt(12 + 0.5 * i));
const HL = new THREE.HemisphereLight(0xffffff, 0xd9dbd4, 1.5); sM.add(HL);
const key = new THREE.DirectionalLight(0xffffff, 2.4); key.position.set(-6, 16, 10); key.castShadow = true;
key.shadow.mapSize.set(2048, 2048); Object.assign(key.shadow.camera, { left: -14, right: 14, top: 14, bottom: -14, near: 1, far: 60 });
key.shadow.bias = -0.0006; key.shadow.radius = 4; sM.add(key); sM.add(key.target);
const ground = new THREE.Mesh(new THREE.PlaneGeometry(80, 80), new THREE.ShaderMaterial({
  uniforms: { uPx: { value: PXH / 1080 } },
  vertexShader: 'varying vec3 vW; void main(){ vec4 w = modelMatrix * vec4(position, 1.); vW = w.xyz; gl_Position = projectionMatrix * viewMatrix * w; }',
  fragmentShader: `varying vec3 vW; uniform float uPx;
    float gl(vec2 p, float s, float wpx){ vec2 q = p / s; vec2 g = abs(fract(q - .5) - .5) / max(fwidth(q), vec2(1e-5)); return 1. - clamp((min(g.x, g.y) - wpx * .5) / 1., 0., 1.); }
    void main(){ vec3 c = vec3(.879, .888, .855); float f = 1. - smoothstep(9., 20., length(vW.xz));
      c = mix(c, vec3(.79, .80, .765), gl(vW.xz, 1., 1. * uPx) * .7 * f); c = mix(c, vec3(.70, .72, .68), gl(vW.xz, 5., 1.4 * uPx) * f);
      gl_FragColor = vec4(c, 1.); }` }));
ground.rotation.x = -Math.PI / 2; sM.add(ground);
const shadowPlane = new THREE.Mesh(new THREE.PlaneGeometry(80, 80), new THREE.ShadowMaterial({ opacity: 0.16 }));
shadowPlane.rotation.x = -Math.PI / 2; shadowPlane.position.y = 0.002; shadowPlane.receiveShadow = true; sM.add(shadowPlane);
function rrShape(w, d, r) { const s = new THREE.Shape(), x = -w / 2, y = -d / 2;
  s.moveTo(x + r, y); s.lineTo(x + w - r, y); s.quadraticCurveTo(x + w, y, x + w, y + r); s.lineTo(x + w, y + d - r); s.quadraticCurveTo(x + w, y + d, x + w - r, y + d);
  s.lineTo(x + r, y + d); s.quadraticCurveTo(x, y + d, x, y + d - r); s.lineTo(x, y + r); s.quadraticCurveTo(x, y, x + r, y); return s; }
const tileGeo = new THREE.ExtrudeGeometry(rrShape(2.3, 1.5, 0.28), { depth: 1, bevelEnabled: true, bevelThickness: 0.03, bevelSize: 0.03, bevelSegments: 3, curveSegments: 8 });
tileGeo.rotateX(-Math.PI / 2);
const tileMat = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.62 });
const coMat = new THREE.MeshPhysicalMaterial({ color: lin('#2334E0'), roughness: 0.22, metalness: 0.05, clearcoat: 1, clearcoatRoughness: 0.06 });
const tiles = NODES.map(n => { const m = new THREE.Mesh(tileGeo, tileMat); m.position.set(n.x, 0, n.z); m.castShadow = true; m.receiveShadow = true; sM.add(m); return m; });
const leds = NODES.map(n => { const m = new THREE.Mesh(new THREE.SphereGeometry(0.1, 16, 8), new THREE.MeshStandardMaterial({ color: 0x9aa0a8, roughness: 0.4 })); sM.add(m); return m; });
function labelTex(title, sub, color = '#0E1210', subColor = '#5B645F') {
  const c = document.createElement('canvas'); c.width = 720; c.height = 220; const x = c.getContext('2d');
  x.font = '800 88px Archivo'; x.fillStyle = color; x.textBaseline = 'alphabetic'; x.fillText(title, 8, 100);
  x.font = '500 36px "IBM Plex Mono"'; x.fillStyle = subColor; x.fillText(sub.toUpperCase(), 10, 170);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4; return t;
}
const labels = [];
const pillM = new THREE.MeshBasicMaterial({ color: 0xffffff });
function sprite(tex, w, h) { const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: tex, transparent: true, depthTest: false, depthWrite: false })); s.scale.set(w, h, 1); s.renderOrder = 10; sM.add(s); return s; }
// routes: orthogonal traces with rounded corners
const ROUTES = [[0, 1], [1, 2], [2, 3], [2, 4]];
const routeCurves = ROUTES.map(([a, b]) => {
  const A = new THREE.Vector3(NODES[a].x, 0.03, NODES[a].z), Bv = new THREE.Vector3(NODES[b].x, 0.03, NODES[b].z);
  const C = new THREE.Vector3(Bv.x, 0.03, A.z), r = 0.6;
  const d1 = new THREE.Vector3().subVectors(C, A).normalize(), d2 = new THREE.Vector3().subVectors(Bv, C).normalize();
  const C1 = C.clone().addScaledVector(d1, -r), C2 = C.clone().addScaledVector(d2, r);
  const cp = new THREE.CurvePath(); cp.add(new THREE.LineCurve3(A, C1)); cp.add(new THREE.QuadraticBezierCurve3(C1, C, C2)); cp.add(new THREE.LineCurve3(C2, Bv));
  return cp;
});
const routeMat = new THREE.MeshStandardMaterial({ color: lin('#0E1210'), roughness: 0.5 });
const RSEG = 160, RRAD = 10;
const tubes = routeCurves.map(c => { const m = new THREE.Mesh(new THREE.TubeGeometry(c, RSEG, 0.05, RRAD, false), routeMat); m.castShadow = true; sM.add(m); return m; });
const RT = ROUTES.map(([a]) => NT[a] + 0.12);
// bottleneck loops: dashed rings that keep turning
const loopMat = new THREE.ShaderMaterial({ transparent: true, depthWrite: false, uniforms: { uT: { value: 0 }, uA: { value: 1 } },
  vertexShader: 'varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.); }',
  fragmentShader: 'varying vec2 vUv; uniform float uT, uA; void main(){ if (fract(vUv.x * 30. - uT * 1.6) > .55) discard; gl_FragColor = vec4(vec3(.34, .37, .35), uA); }' });
const LOOPN = [1, 3];
const loops = LOOPN.map(i => { const m = new THREE.Mesh(new THREE.TorusGeometry(1.75, 0.035, 8, 160), loopMat); m.rotation.x = -Math.PI / 2; m.position.set(NODES[i].x, 0.06, NODES[i].z); sM.add(m); return m; });
const loopLab = [], loopDone = [];
// the engineer (cursor) and the agents
const chevG = chevronGeo(0.14, true);
const cursor = new THREE.Mesh(chevG, coMat); cursor.castShadow = true; sM.add(cursor);
const NA = 24, agents = new THREE.InstancedMesh(chevG, coMat, NA); agents.castShadow = true; agents.frustumCulled = false; sM.add(agents);
const rA = rng(71), AG = Array.from({ length: NA }, (_, i) => ({ route: i % 4, off: (i / NA) * 3.7 % 1, spd: 0.34 + rA() * 0.12, del: rA() * 0.25 }));
const envM = (() => { const pm = new THREE.PMREMGenerator(renderer); const t = pm.fromScene(new RoomEnvironment(), 0.04).texture; pm.dispose(); return t; })();
sM.environment = envM;
const dM = new THREE.Object3D();
function cursorPos(t) {
  const pts = NODES.map(n => new THREE.Vector3(n.x, 1.25, n.z));
  if (t < NT[0]) { const p = E.cubicOut(seg(t, NT[0] - 0.35, NT[0])); return new THREE.Vector3(lerp(pts[0].x - 7, pts[0].x, p), 1.25, lerp(pts[0].z + 7, pts[0].z, p)); }
  for (let i = 0; i < 4; i++) if (t < NT[i + 1]) return pts[i].clone().lerp(pts[i + 1], E.cubicInOut(seg(t, NT[i] + 0.05, NT[i + 1])));
  const home = new THREE.Vector3((NODES[2].x + NODES[3].x) / 2, 1.6, (NODES[2].z + NODES[4].z) / 2);
  return pts[4].clone().lerp(home, E.cubicInOut(seg(t, NT[4] + 0.1, NT[4] + 0.6)));
}
function renderM(t) {
  const t4 = bt(12), t5 = bt(16);
  // camera: gentle drift on bar 4, orbit + push on bar 5
  const k5 = E.cubicInOut(seg(t, t5, t5 + 1.8));
  setIso(AZ0 + 0.05 * seg(t, t4, t5) + 0.22 * k5, EL0 - 0.06 * k5, F0 - 0.4 * seg(t, t4, t5) - 0.9 * k5, -0.9 * k5, -0.5 * k5);
  NODES.forEach((n, i) => {
    const p = E.backOut(seg(t, NT[i], NT[i] + 0.34), 2.2), ex = E.backOut(seg(t, t5 + 0.05 * i, t5 + 0.05 * i + 0.4), 1.8);
    const hgt = lerp(0.12, 0.85, ex);
    tiles[i].scale.set(Math.max(1e-3, p), hgt, Math.max(1e-3, p)); tiles[i].visible = p > 0.001;
    leds[i].position.set(n.x + 0.8, hgt + 0.1, n.z - 0.45); leds[i].visible = p > 0.5;
    leds[i].material.color.set(t > t5 + 0.5 + 0.12 * i ? '#2334E0' : '#9AA0A8');
    const L = labels[i]; if (L) { L.position.set(n.x - 0.15, hgt + 0.85, n.z + 0.1); L.material.opacity = seg(t, NT[i] + 0.08, NT[i] + 0.25); L.visible = p > 0.01; }
  });
  tubes.forEach((m, i) => { const p = E.cubicInOut(seg(t, RT[i], RT[i] + 0.45)); m.geometry.setDrawRange(0, Math.floor(p * RSEG) * RRAD * 6); m.visible = p > 0; });
  routeMat.color.copy(lin('#0E1210')).lerp(lin('#2334E0'), ss(t5 + 0.1, t5 + 0.5, t));
  loopMat.uniforms.uT.value = t;
  loops.forEach((m, i) => { const a = E.backOut(seg(t, NT[LOOPN[i]] + 0.2, NT[LOOPN[i]] + 0.55), 1.6), g = 1 - E.cubicInOut(seg(t, t5 + 0.55 + 0.1 * i, t5 + 1.0 + 0.1 * i));
    m.scale.setScalar(Math.max(1e-3, a * lerp(0.35, 1, g))); m.visible = a * g > 0.01; m.rotation.z = -t * 0.9 * (i ? -1 : 1); });
  loopMat.uniforms.uA.value = 1;
  loopLab.forEach((s, i) => { const a = seg(t, NT[LOOPN[i]] + 0.35, NT[LOOPN[i]] + 0.55), g = 1 - seg(t, t5 + 0.6 + 0.1 * i, t5 + 0.8 + 0.1 * i);
    s.material.opacity = a * g; s.visible = a * g > 0.01; loopDone[i].material.opacity = seg(t, t5 + 0.7 + 0.1 * i, t5 + 0.9 + 0.1 * i); loopDone[i].visible = t > t5 + 0.7; });
  // cursor → splits into agents on the downbeat of bar 5
  const cp = cursorPos(t), bob = 0.08 * Math.sin(t * 5);
  cursor.position.set(cp.x, cp.y + bob, cp.z); cursor.rotation.set(0, AZ0, 0); cursor.scale.setScalar(0.95 * (1 - seg(t, t5, t5 + 0.12)));
  cursor.visible = t < t5 + 0.12 && t > NT[0] - 0.4;
  const on = t >= t5;
  agents.visible = on;
  if (on) {
    for (let i = 0; i < NA; i++) {
      const a = AG[i], c = routeCurves[a.route], k = E.cubicOut(seg(t, t5 + a.del * 0.4, t5 + a.del * 0.4 + 0.45));
      const s = (a.off + (t - t5) * a.spd) % 1, p = c.getPointAt(s), tg = c.getTangentAt(s);
      const x = lerp(cp.x, p.x, k), y = lerp(cp.y, 0.52, k), z = lerp(cp.z, p.z, k);
      dM.position.set(x, y + 0.03 * Math.sin(t * 9 + i), z); dM.rotation.set(0, Math.atan2(-tg.z, tg.x), 0); dM.scale.setScalar(0.56 * Math.min(1, k * 2)); dM.updateMatrix();
      agents.setMatrixAt(i, dM.matrix);
    }
    agents.instanceMatrix.needsUpdate = true;
  }
  renderer.render(sM, camM);
  return { bloom: 0, tone: 0, vig: 0.28, ca: 0 };
}

// -------------------------------------------------------------- C · the work: loops → forward flow (bar 6)
const sF = new THREE.Scene();
const camF = new THREE.OrthographicCamera(-ASP, ASP, 1, -1, -1, 1);
const NF = 24000, rF = rng(606);
const fLoop = new Float32Array(NF * 4), fMove = new Float32Array(NF * 4), fSeed = new Float32Array(NF);
const LOOPS = []; for (let gy = 0; gy < 8; gy++) for (let gx = 0; gx < 14; gx++) LOOPS.push([(gx + 0.5 + (rF() - 0.5) * 0.7) / 14 * 2 * ASP - ASP, (gy + 0.5 + (rF() - 0.5) * 0.7) / 8 * 1.9 - 0.95, 0.04 + rF() * 0.1, (rF() < 0.5 ? -1 : 1) * (2 + rF() * 3)]);
for (let i = 0; i < NF; i++) {
  const L = LOOPS[i % LOOPS.length], rr = L[2] * (0.75 + rF() * 0.5);
  fLoop.set([L[0], L[1], rr, rF() * 6.2832], i * 4);
  const tc = 0.08 + (L[0] + ASP + 0.2) / (2 * ASP + 0.4) * 0.85 + (rF() - 0.5) * 0.08;
  const lane = (Math.floor(rF() * 44) + 0.5) / 44 * 1.9 - 0.95 + (rF() - 0.5) * 0.006;
  fMove.set([L[3] * (0.9 + rF() * 0.2), lane, 0.8 + Math.pow(rF(), 1.5) * 4.2, tc], i * 4); fSeed[i] = rF();
}
const FLOW_GLSL = `uniform float uT; attribute vec4 aLoop, aMove; attribute float aSeed;
  vec2 posAt(float t){
    vec2 c = aLoop.xy; float r = aLoop.z; float ph = aLoop.w + aMove.x * t;
    vec2 lp = c + r * vec2(cos(ph), sin(ph) * .72);
    float tc = aMove.w, dt = t - tc;
    if (dt <= 0.) return lp;
    float phc = aLoop.w + aMove.x * tc; vec2 pc = c + r * vec2(cos(phc), sin(phc) * .72);
    float x = pc.x + aMove.z * dt * smoothstep(0., .22, dt) + (1. + 3. * aSeed) * dt * dt, W = ${ASP.toFixed(4)} + .35;
    x = mod(x + W, 2. * W) - W;
    return vec2(x, mix(pc.y, aMove.y, smoothstep(0., .2, dt)));
  }`;
const gP = new THREE.BufferGeometry();
gP.setAttribute('position', new THREE.BufferAttribute(new Float32Array(NF * 3), 3));
gP.setAttribute('aLoop', new THREE.BufferAttribute(fLoop, 4)); gP.setAttribute('aMove', new THREE.BufferAttribute(fMove, 4)); gP.setAttribute('aSeed', new THREE.BufferAttribute(fSeed, 1));
const mP = new THREE.ShaderMaterial({ transparent: true, depthTest: false, depthWrite: false, blending: THREE.AdditiveBlending,
  uniforms: { uT: { value: 0 }, uPx: { value: PXH / 1080 } },
  vertexShader: FLOW_GLSL + `uniform float uPx; varying vec3 vC;
    void main(){ vec2 p = posAt(uT); gl_Position = projectionMatrix * modelViewMatrix * vec4(p, 0., 1.);
      float cap = smoothstep(0., .25, uT - aMove.w);
      gl_PointSize = mix(1.6, 2.6, aSeed) * uPx * mix(1., 1.35, cap);
      vC = mix(vec3(.13, .14, .16) * (.55 + aSeed), mix(vec3(.26, .30, 1.), vec3(1.), .3 * aSeed) * .8, cap); }`,
  fragmentShader: 'varying vec3 vC; void main(){ float d = length(gl_PointCoord - .5); gl_FragColor = vec4(vC, smoothstep(.5, .1, d)); }' });
const ptsF = new THREE.Points(gP, mP); ptsF.frustumCulled = false; sF.add(ptsF);
const NL = 5000, lLoop = new Float32Array(NL * 8), lMove = new Float32Array(NL * 8), lSeed = new Float32Array(NL * 2), lEnd = new Float32Array(NL * 2);
for (let i = 0; i < NL; i++) for (let e = 0; e < 2; e++) {
  lLoop.set(fLoop.subarray(i * 4, i * 4 + 4), (i * 2 + e) * 4); lMove.set(fMove.subarray(i * 4, i * 4 + 4), (i * 2 + e) * 4); lSeed[i * 2 + e] = fSeed[i]; lEnd[i * 2 + e] = e;
}
const gL = new THREE.BufferGeometry();
gL.setAttribute('position', new THREE.BufferAttribute(new Float32Array(NL * 6), 3));
gL.setAttribute('aLoop', new THREE.BufferAttribute(lLoop, 4)); gL.setAttribute('aMove', new THREE.BufferAttribute(lMove, 4));
gL.setAttribute('aSeed', new THREE.BufferAttribute(lSeed, 1)); gL.setAttribute('aEnd', new THREE.BufferAttribute(lEnd, 1));
const mL = new THREE.ShaderMaterial({ transparent: true, depthTest: false, depthWrite: false, blending: THREE.AdditiveBlending, uniforms: { uT: { value: 0 } },
  vertexShader: FLOW_GLSL + `attribute float aEnd; varying float vA; varying float vCap;
    void main(){ vec2 h = posAt(uT), tl = posAt(uT - .07); vec2 p = aEnd > .5 ? (abs(tl.x - h.x) > .6 ? h : tl) : h;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(p, 0., 1.); vCap = smoothstep(0., .25, uT - aMove.w); vA = aEnd > .5 ? 0. : 1.; }`,
  fragmentShader: 'varying float vA, vCap; void main(){ gl_FragColor = vec4(vec3(.26, .30, 1.) * (.3 * vA + .02) * vCap, 1.); }' });
const linesF = new THREE.LineSegments(gL, mL); linesF.frustumCulled = false; sF.add(linesF);
// the agents sweeping through: bright comets riding the capture front
const NCM = 9, cG = new THREE.BufferGeometry(), cPos = new Float32Array(NCM * 3);
cG.setAttribute('position', new THREE.BufferAttribute(cPos, 3));
const cM = new THREE.PointsMaterial({ size: 26 * PXH / 1080, sizeAttenuation: false, color: new THREE.Color(2.2, 2.3, 3.2), transparent: true, blending: THREE.AdditiveBlending, depthTest: false,
  map: (() => { const c = document.createElement('canvas'); c.width = c.height = 64; const x = c.getContext('2d'); const g = x.createRadialGradient(32, 32, 0, 32, 32, 32);
    g.addColorStop(0, 'rgba(255,255,255,1)'); g.addColorStop(.25, 'rgba(190,200,255,.8)'); g.addColorStop(1, 'rgba(140,150,255,0)'); x.fillStyle = g; x.fillRect(0, 0, 64, 64); return new THREE.CanvasTexture(c); })() });
const comets = new THREE.Points(cG, cM); comets.frustumCulled = false; sF.add(comets);
function renderF(tt) {
  mP.uniforms.uT.value = tt; mL.uniforms.uT.value = tt;
  const fx = -ASP - 0.2 + (tt - 0.08) / 0.85 * (2 * ASP + 0.4);
  for (let i = 0; i < NCM; i++) { cPos[i * 3] = fx + 0.05 * Math.sin(i * 7.1); cPos[i * 3 + 1] = -0.85 + i * 0.21 + 0.03 * Math.sin(tt * 6 + i); }
  cG.attributes.position.needsUpdate = true; comets.visible = tt > 0.02 && tt < 1.05;
  renderer.render(sF, camF);
  const hit = Math.exp(-tt * 6);
  return { bloom: 0.55 + 0.4 * hit, th: 0.45, exp: 1, ca: 0.02 + 0.15 * hit, vig: 0.7, tone: 1 };
}

// -------------------------------------------------------------- D · the ROI summit (bar 7)
const HILLS = [[0, -6, 3.3, 2.5], [-5, -2.5, 1.5, 1.8], [4.6, -1.5, 1.7, 2.0], [-2.8, 2.6, 0.9, 1.5], [3.2, 3.6, 0.8, 1.4], [-7.5, -8, 1.9, 2.5], [7, -8.5, 1.6, 2.2], [-9, 1, 1.2, 2], [9, 1.5, 1.1, 2]];
const hJS = (x, z) => HILLS.reduce((s, [cx, cz, a, sg]) => s + a * Math.exp(-((x - cx) ** 2 + (z - cz) ** 2) / (sg * sg)), 0) + 0.18 * Math.sin(0.55 * x + 0.8) * Math.sin(0.45 * z - 0.3);
const H_GLSL = `float hf(vec2 p){ float s = 0.; ${HILLS.map(([cx, cz, a, sg]) => `s += ${a.toFixed(3)} * exp(-dot(p - vec2(${cx.toFixed(2)}, ${cz.toFixed(2)}), p - vec2(${cx.toFixed(2)}, ${cz.toFixed(2)})) / ${(sg * sg).toFixed(3)});`).join(' ')}
  return s + .18 * sin(.55 * p.x + .8) * sin(.45 * p.y - .3); }`;
const sT = new THREE.Scene(); sT.background = lin('#0A0B0D');
const camT = new THREE.PerspectiveCamera(38, ASP, 0.1, 200);
const mT = new THREE.ShaderMaterial({ uniforms: { uRise: { value: 0 }, uPx: { value: PXH / 1080 }, uT: { value: 0 }, uFog: { value: 8 } },
  vertexShader: H_GLSL + `uniform float uRise; varying vec3 vW; varying float vH;
    void main(){ vec3 p = position; float h = hf(vec2(p.x, -p.y)); vH = h; p.z = h * uRise; vec4 w = modelMatrix * vec4(p, 1.); vW = w.xyz; gl_Position = projectionMatrix * viewMatrix * w; }`,
  fragmentShader: `uniform float uPx, uT, uFog; varying vec3 vW; varying float vH;
    void main(){ float v = vH * 5.2; float fw = max(fwidth(v), 1e-5); float d = abs(fract(v - .5) - .5) / fw;
      float maj = 1. - step(.5, mod(floor(v + .5), 5.)); float lw = mix(1., 1.8, maj) * uPx;
      float line = 1. - smoothstep(lw * .5, lw * .5 + 1., d);
      vec3 n = normalize(cross(dFdx(vW), dFdy(vW))); float sh = clamp(dot(n, normalize(vec3(-.4, .8, .3))), 0., 1.);
      vec3 base = vec3(.004, .0045, .006) + vec3(.012, .014, .03) * sh;
      vec3 lc = vec3(.26, .30, 1.) * mix(.32, 1.0, maj) * (.55 + .45 * sh);
      float fog = exp(-max(0., length(vW - cameraPosition) - uFog) * .09);
      gl_FragColor = vec4(mix(vec3(.003, .0034, .004), mix(base, lc, line), fog), 1.); }` });
const terr = new THREE.Mesh(new THREE.PlaneGeometry(40, 40, 300, 300), mT); terr.rotation.x = -Math.PI / 2; sT.add(terr);
const PATHXZ = [[-1.6, 7.5], [1.4, 4.4], [-0.9, 1.6], [1.1, -1.4], [-0.5, -3.8], [0.15, -5.4], [0, -6]];
const pathCurve = new THREE.CatmullRomCurve3(PATHXZ.map(([x, z]) => new THREE.Vector3(x, hJS(x, z) + 0.09, z)), false, 'centripetal');
const PSEG = 260, PRAD = 8;
const pathMesh = new THREE.Mesh(new THREE.TubeGeometry(pathCurve, PSEG, 0.045, PRAD, false), new THREE.MeshBasicMaterial({ color: new THREE.Color(1.3, 1.45, 3.4) }));
sT.add(pathMesh);
const headT = new THREE.Mesh(chevronGeo(0.12, true), new THREE.MeshBasicMaterial({ color: new THREE.Color(2.2, 2.3, 3.4) })); sT.add(headT);
const summit = new THREE.Vector3(0, hJS(0, -6), -6);
const pinM = new THREE.Mesh(new THREE.SphereGeometry(0.12, 24, 12), new THREE.MeshBasicMaterial({ color: new THREE.Color(2.6, 2.7, 3.6) })); pinM.position.copy(summit).add(new THREE.Vector3(0, 0.12, 0)); sT.add(pinM);
const beam = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, 0.9, 8), new THREE.MeshBasicMaterial({ color: new THREE.Color(1.2, 1.3, 3) })); beam.position.copy(summit).add(new THREE.Vector3(0, 0.55, 0)); sT.add(beam);
const roiEl = document.getElementById('roipin'), tmpV = new THREE.Vector3(), upV = new THREE.Vector3(0, 1, 0);
function renderT(tt) {
  const rise = E.cubicInOut(seg(tt, 0.1, 0.95)); mT.uniforms.uRise.value = rise;
  const k = E.cubicInOut(seg(tt, 0.06, 1.0)), push = E.cubicInOut(seg(tt, 0.95, 1.875));
  camT.position.set(lerp(0.2, 0.9, k), lerp(27, 3.3, k) + 0.5 * push, lerp(-0.6, 11.5, k) - 1.8 * push);
  const look = new THREE.Vector3(0, lerp(0, 2.6, k), lerp(-1.4, -4.2, k));
  camT.up.set(0, 1, 0); if (k < 0.02) camT.up.set(0, 0, -1); camT.lookAt(look); mT.uniforms.uFog.value = camT.position.distanceTo(look) + 1.5;
  const pd = E.cubicInOut(seg(tt, 0.95, 1.6)); pathMesh.geometry.setDrawRange(0, Math.floor(pd * PSEG) * PRAD * 6); pathMesh.visible = pd > 0;
  const hp = pathCurve.getPointAt(Math.max(0.001, pd)), tg = pathCurve.getTangentAt(Math.max(0.001, pd));
  headT.visible = pd > 0.001 && pd < 0.999; headT.position.copy(hp).addScaledVector(upV, 0.1);
  const zA = new THREE.Vector3().crossVectors(tg, upV).normalize(), yA = new THREE.Vector3().crossVectors(zA, tg).normalize();
  headT.quaternion.setFromRotationMatrix(new THREE.Matrix4().makeBasis(tg, yA, zA)); headT.scale.setScalar(0.9);
  const pin = seg(tt, 1.55, 1.75); pinM.visible = beam.visible = pin > 0; pinM.scale.setScalar(Math.max(1e-3, E.backOut(pin, 2.5))); beam.scale.y = Math.max(1e-3, pin);
  tmpV.copy(summit).add(new THREE.Vector3(0, 1.0, 0)).project(camT);
  const sx = (tmpV.x * 0.5 + 0.5) * 1920, sy = (-tmpV.y * 0.5 + 0.5) * 1080;
  roiEl.style.transform = `translate(${sx - 8}px, ${sy - 44}px) scale(${E.backOut(seg(tt, 1.6, 1.8), 2)})`; roiEl.style.opacity = seg(tt, 1.6, 1.7);
  renderer.render(sT, camT);
  return { bloom: 0.75, th: 0.35, exp: 1, ca: 0.02, vig: 0.7, tone: 1 };
}

// -------------------------------------------------------------- dispatch
let ready = false, cleared = false;
function clearGL() { if (!cleared) { renderer.setRenderTarget(null); renderer.setClearColor(0x000000, 1); renderer.clear(); cleared = true; } }
function renderAt(t) {
  if (!ready) return;
  if (t >= bt(28) && t < bt(32) - 0.03) { clearGL(); return; }
  cleared = false;
  renderer.setRenderTarget(rtS); renderer.setClearColor(0x000000, 1); renderer.clear();
  let p;
  if (t < bt(12)) p = renderC(t, false);
  else if (t < bt(20)) p = renderM(t);
  else if (t < bt(24)) p = renderF(t - bt(20));
  else if (t < bt(28)) p = renderT(t - bt(24));
  else p = renderC(t, true);
  post(p);
}
window.addEventListener('hf-seek', e => renderAt(e.detail.time));
async function build() {
  if (MEASURE) return;
  await new Promise(r => setTimeout(r, 0));
  await Promise.all([document.fonts.load('800 88px Archivo'), document.fonts.load('500 36px "IBM Plex Mono"')]);
  NODES.forEach((n, i) => { labels[i] = sprite(labelTex(n.n, n.s), 3.3, 1.01); });
  LOOPN.forEach((ni, i) => {
    const mk = (txt, col) => { const c = document.createElement('canvas'); c.width = 520; c.height = 96; const x = c.getContext('2d');
      x.font = '600 44px "IBM Plex Mono"'; x.fillStyle = col; x.fillText(txt, 6, 64); const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace; return tx; };
    loopLab[i] = sprite(mk(i ? '2 DAYS LATE' : '3 H / DAY', '#5B645F'), 2.4, 0.44);
    loopDone[i] = sprite(mk('AUTOMATED ✓', '#2334E0'), 2.4, 0.44);
    [loopLab[i], loopDone[i]].forEach(s => s.position.set(NODES[ni].x + 1.35, 0.9, NODES[ni].z + 1.55));
  });
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
  await p.evaluate(async () => { await document.fonts.ready; await Promise.all(['800 196px Archivo', '500 64px Archivo'].map(f => document.fonts.load(f))); });
  await p.waitForTimeout(300);
  const m = await p.evaluate(() => {
    const r = el => { const b = document.querySelector(el).getBoundingClientRect(); return [b.left, b.top, b.width, b.height]; };
    return { mk: r('#mk'), sd: r('#sd'), fwd: r('#fwd') };
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
    body = s1_html() + s2_html() + s3_html() + heads_html() + s8_html() + end_html()
    tl_js = TL_JS.replace("%%MEASURE%%", json.dumps(measure)).replace("%%DUR%%", str(DUR))
    gl_js = GL_JS.replace("%%ZOOM%%", repr(zoom))
    plugin_tags = "\n".join(f'<script src="{p}.min.js"></script>' for p in PLUGINS)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width={pw}, height={ph}">
<title>XForward — Loops to Forward</title>
<script src="gsap.min.js"></script>
{plugin_tags}
<script type="importmap">{{"imports":{{"three":"./three/three.module.js"}}}}</script>
<style>
{FONTS}
{CSS}
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
        measure = {"mk": [700, 330, 236, 236], "sd": [900, 520, 330, 70], "fwd": [900, 330, 800, 196]}
    else:
        measure = json.load(open(mfile))
        src = os.path.join(HERE, "out", "music.wav")
        if not os.path.exists(src):
            subprocess.run([sys.executable, os.path.join(HERE, "xf_synth.py"), os.path.join(HERE, "out")], check=True)
        shutil.copy(src, os.path.join(OUT, "music.wav"))
    with open(os.path.join(OUT, "index.html"), "w") as fh:
        fh.write(page(measure))
    if MEASURE:
        js = os.path.join(HERE, "measure.js")
        open(js, "w").write(MEASURE_JS)
        scratch = os.path.dirname(ADS)
        res = subprocess.run(["node", js, os.path.join(OUT, "index.html")], check=True, capture_output=True, text=True, cwd=scratch)
        m = json.loads(res.stdout.strip().splitlines()[-1])
        json.dump(m, open(mfile, "w"), indent=1)
        print("measured", m)
    else:
        print("built", OUT, round(W * ZOOM), "x", round(H * ZOOM))


if __name__ == "__main__":
    build()
