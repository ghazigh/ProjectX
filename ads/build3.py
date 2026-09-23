"""Round 3: recognition-first ("that's me") concepts, premium craft.

GSAP-only compositions with a synthesized soundtrack (pings, whooshes, hits)
timed to the same event lists the visuals use.
"""
import os, shutil, sys
from build import FONTS, XLOGO, HELPERS
import synth

HERE = os.path.dirname(os.path.abspath(__file__))
DRAFT = "--final" not in sys.argv

CSS0 = """
html,body{margin:0;background:#000}
#root{position:relative;width:100%;height:100%;overflow:hidden;background:#000}
.stage{position:absolute;left:0;top:0;overflow:hidden;color:#fff;font-family:'Archivo',sans-serif}
.clip{position:absolute;inset:0}
.xl{display:block;overflow:visible}
.xl path{fill:none;stroke-width:2.3;stroke-linecap:round;stroke-linejoin:round}
.xl .m1{stroke:#fff}.xl .m2{stroke:#8C96FF}
.wm{font-weight:750;font-stretch:118%;letter-spacing:-.04em}.wm b{color:#8C96FF}
.tag{font-weight:450;color:rgba(255,255,255,.72)}
.mono{font-family:'IBM Plex Mono',monospace;letter-spacing:.14em;text-transform:uppercase}
.endcard{position:absolute;inset:0;background:#000;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}
"""


def page(cid, W, H, zoom, dur, css, body, js):
    w, h = round(W * zoom), round(H * zoom)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width={w}, height={h}">
<title>XForward ad · {cid}</title>
<script src="gsap.min.js"></script>
<style>
{FONTS}
{CSS0}
.stage{{width:{W}px;height:{H}px;zoom:{zoom}}}
{css}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-width="{w}" data-height="{h}" data-duration="{dur}">
<div class="stage">
{body}
</div>
<audio id="music" src="music.wav" data-start="0" data-duration="{dur}" data-track-index="9"></audio>
</div>
<script>
{HELPERS}
const tl = gsap.timeline({{ paused: true }});
{js}
window.__timelines["main"] = tl;
</script>
</body>
</html>
"""


C = {}

# ======================================================================= 1 · 11:47 PM notifications (9:16)
CARDS = [
    ("#EA4335", "M", "Gmail", "New quote request", "Hi, could you send a price for 40 units by tomorrow?"),
    ("#34C759", "✆", "Phone", "Missed calls (2)", "(514) 555-0142 · 9:12 PM, 10:40 PM"),
    ("#2CA01C", "qb", "QuickBooks", "3 invoices overdue", "Total outstanding: $8,420"),
    ("#0A84FF", "O", "Outlook", "RE: RE: RE: Order #4471", "Sorry, which delivery date did we agree on?"),
    ("#FF9F0A", "31", "Calendar", "Reschedule request", "Marc Roy can't make 9:00 tomorrow"),
    ("#34C759", "✉", "Messages", "Are you open Saturday?", "Also, do you do free estimates?"),
    ("#95BF47", "S", "Shopify", "Where is my order?", "Order #10432 · customer asked twice"),
    ("#EA4335", "M", "Gmail", "Documents for 2025", "Here are some of them, rest next week"),
    ("#5B5FC7", "T", "Teams", "Did you update the CRM?", "Need the numbers for Monday"),
    ("#0A84FF", "O", "Outlook", "Purchase order PO-4471.pdf", "Please enter and confirm"),
    ("#8E8E93", "▶", "Voicemail", "New voicemail · 0:48", "“Hi, it's about the leak…”"),
    ("#34C759", "✉", "Messages", "Can you confirm my booking?", "Still waiting on a reply"),
]
CARD_T = [round(0.35 + i * 0.36, 2) for i in range(len(CARDS))]
SWIPE_T = [round(5.7 + k * 0.26, 2) for k in range(4)]

cards_html = "".join(
    f'<div class="nc" id="n{i}"><span class="ap" style="background:{c}">{g}</span><div class="nb"><div class="nh"><b>{a}</b><span>now</span></div>'
    f'<p class="nt">{t}</p><p class="nx">{x}</p></div><span class="ok">✓ Handled</span></div>'
    for i, (c, g, a, t, x) in enumerate(CARDS))

C["r3-1-1147pm"] = dict(W=1080, H=1920, zoom=1/3, dur=15,
    music=lambda p: synth.notif(p, CARD_T, SWIPE_T), css="""
.wall{position:absolute;inset:0;background:
  radial-gradient(600px 600px at 20% 25%,rgba(64,78,255,.55),transparent 70%),
  radial-gradient(700px 700px at 85% 60%,rgba(140,70,255,.45),transparent 70%),
  radial-gradient(800px 600px at 40% 95%,rgba(0,150,170,.35),transparent 70%),#07080C}
.dim{position:absolute;inset:0;background:rgba(0,0,0,.25)}
.clock{position:absolute;left:0;right:0;top:170px;text-align:center}
.clock .t{font-weight:200;font-stretch:100%;font-size:270px;letter-spacing:-8px;line-height:1}
.clock .d{font-size:44px;font-weight:500;opacity:.85;margin-top:10px}
.say{position:absolute;left:0;right:0;top:600px;text-align:center;font-weight:750;font-stretch:112%;font-size:84px;letter-spacing:-3px;opacity:0}
.say.b{color:#fff}
.nc{position:absolute;left:54px;right:54px;bottom:260px;height:178px;box-sizing:border-box;padding:26px 30px;border-radius:44px;display:flex;gap:26px;align-items:flex-start;
  background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.18);-webkit-backdrop-filter:blur(30px);backdrop-filter:blur(30px);opacity:0;overflow:hidden}
.ap{flex:none;width:76px;height:76px;border-radius:20px;display:grid;place-items:center;font-weight:800;font-size:34px;color:#fff}
.nb{flex:1;min-width:0}
.nh{display:flex;justify-content:space-between;font-size:28px;opacity:.75}
.nh b{font-weight:600}
.nt{margin:6px 0 0;font-size:36px;font-weight:650;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.nx{margin:4px 0 0;font-size:31px;opacity:.8;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.ok{position:absolute;right:26px;top:24px;padding:8px 16px;border-radius:999px;background:#8C96FF;color:#07080C;font-weight:700;font-size:26px;opacity:0}
.sum{position:absolute;left:54px;right:54px;bottom:260px;padding:34px 36px;border-radius:44px;background:rgba(140,150,255,.22);border:1px solid rgba(140,150,255,.5);
  -webkit-backdrop-filter:blur(30px);backdrop-filter:blur(30px);opacity:0}
.sum .nh{opacity:.85}
.sum .nt{font-size:44px;white-space:normal}
.sum .nx{white-space:normal}
.endcard{gap:36px;padding:0 90px}
.endcard .xl{width:230px;height:230px}
.endcard .wm{font-size:120px}.endcard .tag{font-size:46px}
""", body=f"""
<div class="wall"></div><div class="dim"></div>
<div class="clock"><div class="t" id="tm">11:47</div><div class="d">Tuesday, March 11</div></div>
<p class="say" id="s1">Still doing admin.</p>
<p class="say b" id="s2">Go to bed.</p>
{cards_html}
<div class="sum" id="sum"><div class="nh"><b><span style="color:#8C96FF">X</span>Forward agents</b><span>now</span></div>
  <p class="nt">Tonight: 23 tasks done.</p><p class="nx">Quotes sent · 2 bookings confirmed · invoices chased · 0 need you</p></div>
<section id="end1" class="clip" data-start="10.4" data-duration="4.6"><div class="endcard">
  <div id="lg">{XLOGO}</div><div class="wm" id="wm"><b>X</b>Forward</div><div class="tag" id="tg">AI agents that do the admin.</div></div></section>
""", js=f"""
const CT={CARD_T}, SW={SWIPE_T}, N=CT.length, STEP=200;
const vis=d=>d>=4?0:(d>=3?.45:1);
tl.fromTo('#s1',{{opacity:0,y:20}},{{opacity:1,y:0,duration:.5,ease:'power3.out'}},1.7);
for(let k=0;k<N;k++){{
  tl.fromTo('#n'+k,{{opacity:0,y:140,scale:.96}},{{opacity:1,y:0,scale:1,duration:.32,ease:'back.out(1.4)',immediateRender:false}},CT[k]);
  for(let j=0;j<k;j++){{const d=k-j;
    tl.fromTo('#n'+j,{{y:-(d-1)*STEP,opacity:vis(d-1),scale:1-(d-1)*.015}},{{y:-d*STEP,opacity:vis(d),scale:1-d*.015,duration:.3,ease:'power3.out',immediateRender:false}},CT[k]);}}
}}
// agent sweeps: visible cards (newest first) get handled and fly out
const visible=[N-1,N-2,N-3,N-4];
visible.forEach((j,i)=>{{
  tl.fromTo('#n'+j+' .ok',{{opacity:0,scale:.6}},{{opacity:1,scale:1,duration:.18,ease:'back.out(2)',immediateRender:false}},5.35+i*.05);
  tl.to('#n'+j,{{x:1200,opacity:0,duration:.34,ease:'power3.in'}},SW[i]);}});
tl.to('#s1',{{opacity:0,y:-20,duration:.3}},6.6);
tl.fromTo('#sum',{{opacity:0,y:120,scale:.96}},{{opacity:1,y:0,scale:1,duration:.5,ease:'back.out(1.4)'}},7.4);
tl.set('#tm',{{textContent:'11:48'}},7.4);
tl.fromTo('#s2',{{opacity:0,scale:1.2}},{{opacity:1,scale:1,duration:.35,ease:'power4.out'}},8.4);
xMorph(tl,'#lg',10.5);
tl.fromTo('#wm',{{opacity:0,y:30}},{{opacity:1,y:0,duration:.5,ease:'power3.out'}},11.0);
tl.fromTo('#tg',{{opacity:0}},{{opacity:1,duration:.5}},11.5);
""")

# ======================================================================= 2 · Starring: You (16:9, cinematic)
ROLES = [("Starring", "You"), ("Receptionist", "You"), ("Accountant", "You"), ("Dispatcher", "You"),
         ("Customer service", "You"), ("Data entry", "You"), ("Night shift", "You"), ("Weekends", "Also you")]
HITS = [1.2, 2.3, 3.2, 4.0, 4.7, 5.3, 5.8, 6.3]
RECAST = [("Receptionist", 8.6), ("Accounting", 9.15), ("Dispatch", 9.7), ("Night shift", 10.25)]
FINAL = 11.0

credits_html = "".join(f'<div class="cr" id="r{i}"><p class="role mono">{r}</p><p class="nm">{n}</p></div>' for i, (r, n) in enumerate(ROLES))
recast_html = "".join(f'<div class="cr" id="q{i}"><p class="role mono">{r}</p><div class="roll"><div class="rl" id="ql{i}"><p class="nm">You</p><p class="nm ag">Agent</p></div></div></div>' for i, (r, _) in enumerate(RECAST))

C["r3-2-starring-you"] = dict(W=1920, H=1080, zoom=1/3, dur=15,
    music=lambda p: synth.credits(p, HITS, [t for _, t in RECAST], FINAL), css="""
.bgc{position:absolute;inset:0;background:radial-gradient(1200px 700px at 50% 55%,#14161d,#050507 70%)}
.grain{position:absolute;inset:-100px;background:radial-gradient(ellipse at center,transparent 45%,rgba(0,0,0,.65) 100%)}
.bar{position:absolute;left:0;right:0;height:120px;background:#000;z-index:5}
.bar.t{top:0}.bar.b{bottom:0}
.cr{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;opacity:0}
.role{margin:0;font-size:30px;color:rgba(255,255,255,.62)}
.nm{margin:14px 0 0;font-family:'Instrument Serif',serif;font-size:190px;line-height:1;letter-spacing:-2px}
.roll{height:204px;overflow:hidden}
.rl .nm{height:190px;margin:14px 0 0}
.ag{color:#8C96FF;font-style:italic}
.intro{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;opacity:0}
.intro p{font-size:28px;color:rgba(255,255,255,.7)}
.recast{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;opacity:0}
.recast p{font-family:'Instrument Serif',serif;font-style:italic;font-size:160px;margin:0}
.ceo .nm{font-style:normal}
.endcard{gap:26px;background:transparent}
.endcard .xl{width:150px;height:150px}
.endcard .prod{font-size:26px;color:rgba(255,255,255,.6)}
.endcard .wm{font-size:120px}.endcard .tag{font-size:40px}
""", body=f"""
<div class="bgc"></div><div class="grain" id="gr"></div>
<div class="intro" id="in"><p class="mono">A small business production</p></div>
{credits_html}
<div class="recast" id="rc"><p>Time to recast.</p></div>
{recast_html}
<div class="cr ceo" id="ceo"><p class="role mono">CEO</p><p class="nm">You.</p></div>
<section id="endS" class="clip" data-start="12.2" data-duration="2.8"><div class="endcard">
  <div id="lg">{XLOGO}</div><p class="prod mono" id="pr">An XForward production</p>
  <div class="wm" id="wm"><b>X</b>Forward</div><div class="tag" id="tg">AI agents, built into your business.</div></div></section>
<div class="bar t"></div><div class="bar b"></div>
""", js=f"""
const H={HITS}, RC={[t for _, t in RECAST]}, FIN={FINAL};
tl.fromTo('#gr',{{x:0,y:0}},{{x:60,y:-40,duration:15,ease:'steps(90)'}},0);
tl.fromTo('#in',{{opacity:0}},{{opacity:1,duration:.3}},.15); tl.to('#in',{{opacity:0,duration:.2}},.95);
H.forEach((t,i)=>{{const end=i<H.length-1?H[i+1]:7.0;
  tl.fromTo('#r'+i,{{opacity:0,scale:1.04}},{{opacity:1,scale:1,duration:.16,ease:'power2.out',immediateRender:false}},t);
  tl.to('#r'+i,{{opacity:0,duration:.1}},end-.1);}});
tl.fromTo('#rc',{{opacity:0,scale:.96}},{{opacity:1,scale:1,duration:.4,ease:'power3.out'}},7.4);
tl.to('#rc',{{opacity:0,duration:.2}},8.4);
RC.forEach((t,i)=>{{const end=i<RC.length-1?RC[i+1]:FIN;
  tl.fromTo('#q'+i,{{opacity:0}},{{opacity:1,duration:.1,immediateRender:false}},t-.1);
  tl.fromTo('#ql'+i,{{y:0}},{{y:-204,duration:.28,ease:'power3.inOut',immediateRender:false}},t+.12);
  tl.to('#q'+i,{{opacity:0,duration:.08}},end-.1);}});
tl.fromTo('#ceo',{{opacity:0,scale:1.08}},{{opacity:1,scale:1,duration:.45,ease:'power3.out'}},FIN);
tl.to('#ceo',{{opacity:0,duration:.3}},12.0);
xMorph(tl,'#lg',12.3);
tl.fromTo('#pr',{{opacity:0}},{{opacity:1,duration:.4}},12.6);
tl.fromTo('#wm',{{opacity:0,y:30}},{{opacity:1,y:0,duration:.5,ease:'power3.out'}},12.9);
tl.fromTo('#tg',{{opacity:0}},{{opacity:1,duration:.5}},13.3);
""")

# ======================================================================= 3 · Sunday (1:1)
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
# (day, startHour, hours, title) — admin that eats evenings and the weekend
ADMIN = [(0, 19, 2, "Invoices"), (1, 20, 2, "Quotes"), (2, 19, 3, "Emails"), (3, 20, 2, "Follow-ups"), (4, 18, 3, "Payroll"),
         (5, 10, 2, "Orders"), (5, 14, 3, "Scheduling"), (6, 9, 2, "Catch-up"), (6, 11, 2, "Taxes"), (6, 13, 2, "CRM update"),
         (6, 15, 2, "Supplier calls"), (6, 17, 2, "Reminders"), (0, 21, 1, "Quotes"), (2, 22, 1, "Admin"), (4, 21, 1, "Emails"), (6, 19, 2, "Next week prep")]
DROP_T = [round(0.4 + i * 0.3, 2) for i in range(len(ADMIN))]
FLY_T = [round(6.5 + i * 0.16, 2) for i in range(len(ADMIN))]

C["r3-3-sunday"] = dict(W=1080, H=1080, zoom=4/9, dur=15,
    music=lambda p: synth.sunday(p, DROP_T, FLY_T), css="""
.bg{position:absolute;inset:0;background:radial-gradient(900px 700px at 50% 30%,#141824,#06070A 75%)}
.q{position:absolute;left:70px;right:70px;top:60px;font-weight:750;font-stretch:112%;font-size:62px;letter-spacing:-2px;line-height:1.02;opacity:0}
.q span{color:#8C96FF}
.cal{position:absolute;left:70px;right:70px;top:250px;bottom:150px;border-radius:26px;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.1);overflow:hidden}
.dh{position:absolute;top:14px;font:600 22px 'IBM Plex Mono',monospace;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,.6);text-align:center}
.dh.sun{color:#fff}
.hl{position:absolute;left:14px;font:500 17px 'IBM Plex Mono',monospace;color:rgba(255,255,255,.35)}
.gl{position:absolute;left:90px;right:0;height:1px;background:rgba(255,255,255,.06)}
.blk{position:absolute;border-radius:10px;padding:6px 8px;box-sizing:border-box;font-size:17px;font-weight:600;line-height:1.1;overflow:hidden}
.work{background:rgba(255,255,255,.07);color:rgba(255,255,255,.35)}
.adm{background:#3A3F4B;color:#fff;border:1px solid rgba(255,255,255,.18);opacity:0}
.adm.ag{background:#8C96FF;color:#07080C}
.lane{position:absolute;left:70px;right:70px;bottom:40px;height:84px;border-radius:22px;border:2px solid #8C96FF;display:flex;align-items:center;gap:18px;padding:0 26px;opacity:0;background:rgba(140,150,255,.12)}
.lane b{font:700 24px 'IBM Plex Mono',monospace;letter-spacing:2px;color:#8C96FF}
.lane span{font-size:26px;color:rgba(255,255,255,.8)}
.free{position:absolute;border-radius:12px;border:2px dashed rgba(140,150,255,.8);display:grid;place-items:center;text-align:center;font-family:'Instrument Serif',serif;font-style:italic;font-size:44px;color:#fff;opacity:0}
.endcard{gap:30px;padding:0 90px}
.endcard .xl{width:190px;height:190px}.endcard .wm{font-size:110px}.endcard .tag{font-size:40px}
""", body=f"""
<div class="bg"></div>
<p class="q" id="q1">When was your last <span>free Sunday?</span></p>
<p class="q" id="q2">Your Sundays. <span>Back.</span></p>
<div class="cal" id="cal"></div>
<div class="lane" id="lane"><b>AGENTS · 24/7</b><span>handling it while you're off</span></div>
<section id="endS" class="clip" data-start="10.6" data-duration="4.4"><div class="endcard">
  <div id="lg">{XLOGO}</div><div class="wm" id="wm"><b>X</b>Forward</div><div class="tag" id="tg">AI agents, built into your business.</div></div></section>
""", js=f"""
const DAYS={DAYS}, ADMIN={[list(a) for a in ADMIN]}, DROP={DROP_T}, FLY={FLY_T};
const cal=document.getElementById('cal'), CW=940, CH=680, X0=90, Y0=60, H0=8, HN=15, colW=(CW-X0)/7, rowH=(CH-Y0-10)/HN;
const pos=(d,h,n)=>({{left:X0+d*colW+4,top:Y0+(h-H0)*rowH+2,width:colW-8,height:n*rowH-4}});
DAYS.forEach((d,i)=>{{const e=document.createElement('div');e.className='dh'+(i===6?' sun':'');e.textContent=d;Object.assign(e.style,{{left:(X0+i*colW)+'px',width:colW+'px'}});cal.appendChild(e);}});
for(let h=0;h<HN;h+=2){{const e=document.createElement('div');e.className='hl';e.style.top=(Y0+h*rowH-8)+'px';e.textContent=((H0+h-1)%12+1)+(H0+h<12?'a':'p');cal.appendChild(e);
  const g=document.createElement('div');g.className='gl';g.style.top=(Y0+h*rowH)+'px';cal.appendChild(g);}}
for(let d=0;d<5;d++){{const p=pos(d,9,8);const e=document.createElement('div');e.className='blk work';e.textContent='Work';Object.assign(e.style,{{left:p.left+'px',top:p.top+'px',width:p.width+'px',height:p.height+'px'}});cal.appendChild(e);}}
const free=document.createElement('div');free.className='free';free.id='free';const fp=pos(6,9,12);Object.assign(free.style,{{left:fp.left+'px',top:fp.top+'px',width:fp.width+'px',height:fp.height+'px'}});free.textContent='free';cal.appendChild(free);
ADMIN.forEach((a,i)=>{{const p=pos(a[0],a[1],a[2]);const e=document.createElement('div');e.className='blk adm';e.id='a'+i;e.textContent=a[3];
  Object.assign(e.style,{{left:p.left+'px',top:p.top+'px',width:p.width+'px',height:p.height+'px'}});cal.appendChild(e);
  tl.fromTo(e,{{opacity:0,y:-40,scale:1.08}},{{opacity:1,y:0,scale:1,duration:.28,ease:'back.out(1.8)',immediateRender:false}},DROP[i]);
  const dy=CH-p.top+60, dx=(40+i*52)-p.left;
  tl.to(e,{{backgroundColor:'#8C96FF',color:'#07080C',duration:.15}},FLY[i]-.15);
  tl.to(e,{{x:dx,y:dy,scale:.45,opacity:0,duration:.5,ease:'power3.in'}},FLY[i]);}});
tl.fromTo('#q1',{{opacity:0,y:20}},{{opacity:1,y:0,duration:.5,ease:'power3.out'}},1.6);
tl.to('#cal',{{scale:1.02,duration:4.5,ease:'none'}},1.5);
tl.fromTo('#lane',{{opacity:0,y:30}},{{opacity:1,y:0,duration:.45,ease:'power3.out'}},6.2);
tl.to('#q1',{{opacity:0,duration:.3}},8.6);
tl.fromTo('#free',{{opacity:0,scale:.9}},{{opacity:1,scale:1,duration:.5,ease:'back.out(1.6)'}},9.4);
tl.fromTo('#q2',{{opacity:0,y:20}},{{opacity:1,y:0,duration:.45,ease:'power3.out'}},9.0);
xMorph(tl,'#lg',10.7);
tl.fromTo('#wm',{{opacity:0,y:30}},{{opacity:1,y:0,duration:.5,ease:'power3.out'}},11.2);
tl.fromTo('#tg',{{opacity:0}},{{opacity:1,duration:.5}},11.7);
""")


def build():
    out = os.path.join(HERE, "projects")
    for cid, c in C.items():
        d = os.path.join(out, cid)
        os.makedirs(os.path.join(d, "fonts"), exist_ok=True)
        for f in os.listdir(os.path.join(HERE, "fonts")):
            if f.endswith(".woff2"):
                shutil.copy(os.path.join(HERE, "fonts", f), os.path.join(d, "fonts", f))
        shutil.copy(os.path.join(HERE, "gsap.min.js"), d)
        c["music"](os.path.join(d, "music.wav"))
        zoom = c["zoom"] if DRAFT else 1
        with open(os.path.join(d, "index.html"), "w") as fh:
            fh.write(page(cid, c["W"], c["H"], zoom, c["dur"], c["css"], c["body"], c["js"]))
        print("built", cid, round(c["W"] * zoom), "x", round(c["H"] * zoom))


if __name__ == "__main__":
    build()
