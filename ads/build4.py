"""Round 4: clear message — what XForward does and what the business wins.

GSAP compositions + synthesized tracks (synth.explainer). Numbers are
illustrative targets and are labelled as such on screen.
"""
import os, shutil, sys
from build import FONTS, XLOGO
from build3 import page
import synth

HERE = os.path.dirname(os.path.abspath(__file__))
DRAFT = "--final" not in sys.argv
ARROW = '<svg viewBox="0 0 16 16" width="34" height="34"><path d="M3 8h10M9 4l4 4-4 4" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
C = {}

# ======================================================================= 1 · How it works (16:9, 20 s)
ROOMS = [  # id, label, x, y, w, h, pain tag, hours, tool
    ("fd", "Front desk", 600, 190, 520, 300, "Missed calls · 9 / wk", "Calls & texts"),
    ("ib", "Inbox", 1150, 190, 300, 300, "Emails · 7 h / wk", "Gmail"),
    ("sq", "Sales & quotes", 1480, 190, 320, 300, "Quotes · 6 h / wk", "CRM"),
    ("ac", "Accounting", 600, 520, 420, 320, "Invoices · 4 h / wk", "QuickBooks"),
    ("op", "Operations", 1050, 520, 750, 320, "Order entry · 5 h / wk", "ERP"),
]
rooms_html = "".join(
    f'<div class="room" id="rm-{i}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px"><span class="rl mono">{lab}</span>'
    f'<div class="pain" id="pn-{i}"><span class="pt">{pain}</span><span class="ag">✓ Agent · {tool}</span></div></div>'
    for i, (_, lab, x, y, w, h, pain, tool) in enumerate(ROOMS))
IMP1 = [1.2, 4.8, 9.3, 13.8, 17.0]

C["r4-1-how-it-works"] = dict(W=1920, H=1080, zoom=1/3, dur=20,
    music=lambda p: synth.explainer(p, 20, IMP1, 9.3, 17.0, bpm=112), css="""
.bgp{position:absolute;inset:0;background:#06080D;background-image:linear-gradient(rgba(140,150,255,.07) 1px,transparent 1px),linear-gradient(90deg,rgba(140,150,255,.07) 1px,transparent 1px);background-size:60px 60px}
.kick{position:absolute;left:120px;top:120px;font:500 24px 'IBM Plex Mono',monospace;letter-spacing:.16em;color:#8C96FF;opacity:0}
.step{position:absolute;left:120px;top:250px;width:420px;opacity:0}
.step .n{font:600 26px 'IBM Plex Mono',monospace;color:#8C96FF;letter-spacing:.1em}
.step p{margin:16px 0 0;font-weight:700;font-stretch:110%;font-size:64px;line-height:1.02;letter-spacing:-2.5px}
.step small{display:block;margin-top:22px;font-size:30px;color:rgba(255,255,255,.62);line-height:1.3}
.room{position:absolute;border:2px solid rgba(140,150,255,.35);border-radius:18px;background:rgba(140,150,255,.03)}
.rl{position:absolute;left:20px;top:16px;font-size:20px;color:rgba(255,255,255,.55)}
.pain{position:absolute;left:20px;bottom:20px;opacity:0}
.pt,.ag{display:inline-block;padding:10px 16px;border-radius:999px;font-weight:650;font-size:26px}
.pt{background:#F2A33A;color:#1A1204}
.ag{background:#8C96FF;color:#06080D;position:absolute;left:0;bottom:0;white-space:nowrap;opacity:0}
.eng{position:absolute;left:0;top:0;width:0;height:0}
.eng i{position:absolute;left:-16px;top:-16px;width:32px;height:32px;border-radius:50%;background:#8C96FF;box-shadow:0 0 0 8px rgba(140,150,255,.25),0 0 40px #8C96FF}
.eng b{position:absolute;left:26px;top:-16px;font:600 20px 'IBM Plex Mono',monospace;color:#8C96FF;white-space:nowrap;letter-spacing:.08em}
.total{position:absolute;left:600px;top:870px;font-weight:700;font-size:44px;opacity:0}
.total span{color:#F2A33A}
.tools{position:absolute;left:600px;top:880px;display:flex;gap:14px;opacity:0}
.tools span{font:600 22px 'IBM Plex Mono',monospace;padding:10px 16px;border-radius:999px;border:2px solid #8C96FF;color:#8C96FF}
.res{position:absolute;inset:0;background:#06080D;display:grid;grid-template-columns:repeat(3,1fr);align-items:center;padding:0 110px;gap:60px;opacity:0}
.res div{border-top:3px solid #8C96FF;padding-top:30px}
.res b{display:block;font-weight:800;font-stretch:120%;font-size:120px;letter-spacing:-5px;line-height:1}
.res span{display:block;margin-top:18px;font-size:34px;color:rgba(255,255,255,.72)}
.disc{position:absolute;left:110px;bottom:70px;font:500 18px 'IBM Plex Mono',monospace;color:rgba(255,255,255,.4);opacity:0}
.endcard{gap:26px}
.endcard .xl{width:150px;height:150px}.endcard .wm{font-size:120px}.endcard .tag{font-size:40px}
.cta{margin-top:18px;display:inline-flex;align-items:center;gap:14px;padding:22px 36px;border-radius:999px;background:#8C96FF;color:#06080D;font-weight:750;font-size:36px}
""", body=f"""
<div class="bgp"></div>
<p class="kick" id="kk">HOW XFORWARD WORKS</p>
<div class="step" id="st1"><span class="n">01</span><p>We embed a senior AI engineer in your business.</p><small>On site with your team, from week one.</small></div>
<div class="step" id="st2"><span class="n">02</span><p>We find the work that eats your hours.</p><small>Every repetitive task, priced in hours.</small></div>
<div class="step" id="st3"><span class="n">03</span><p>We build AI agents that do it for you.</p><small>On your own tools. Your data stays yours.</small></div>
{rooms_html}
<div class="eng" id="eng"><i></i><b>ENGINEER</b></div>
<p class="total" id="tot">= <span>27 hours a week</span> of repetitive work</p>
<div class="tools" id="tls"><span>Gmail</span><span>Calendar</span><span>QuickBooks</span><span>CRM</span><span>ERP</span></div>
<div class="res" id="res"><div><b>27 h</b><span>back every week</span></div><div><b>&lt; 60 s</b><span>reply to every lead, 24/7</span></div><div><b>6 wks</b><span>to live, at a fixed price</span></div></div>
<p class="disc" id="dsc">Illustrative targets for a 10-person business. Confirmed in your free diagnostic.</p>
<section id="endS" class="clip" data-start="17" data-duration="3"><div class="endcard">
  <div id="lg">{XLOGO}</div><div class="wm" id="wm"><b>X</b>Forward</div><div class="tag" id="tg">AI agents, built into your business.</div>
  <div class="cta" id="ct">Book a free call {ARROW}</div></div></section>
""", js="""
tl.fromTo('#kk',{opacity:0},{opacity:1,duration:.5},.3);
tl.fromTo('.room',{opacity:0,scale:.94},{opacity:1,scale:1,duration:.5,stagger:.12,ease:'power3.out'},.4);
const step=(s,a,b)=>{tl.fromTo(s,{opacity:0,y:30},{opacity:1,y:0,duration:.5,ease:'power3.out'},a);tl.to(s,{opacity:0,y:-20,duration:.3},b)};
step('#st1',1.2,4.5); step('#st2',4.8,9.0); step('#st3',9.3,13.5);
// engineer walks the rooms
const path=[[560,660],[860,340],[1300,340],[1640,340],[1420,680],[810,680]];
tl.fromTo('#eng',{x:path[0][0],y:path[0][1],opacity:0},{opacity:1,duration:.3,immediateRender:false},1.3);
for(let i=1;i<path.length;i++) tl.to('#eng',{x:path[i][0],y:path[i][1],duration:.55,ease:'power2.inOut'},1.4+i*.6);
// pain points appear with hours
for(let i=0;i<5;i++) tl.fromTo('#pn-'+i,{opacity:0,y:16,scale:.9},{opacity:1,y:0,scale:1,duration:.3,ease:'back.out(2)'},5.2+i*.45);
tl.fromTo('.room',{borderColor:'rgba(140,150,255,.35)'},{borderColor:'rgba(242,163,58,.7)',duration:.4,immediateRender:false},5.2);
tl.fromTo('#tot',{opacity:0,y:20},{opacity:1,y:0,duration:.45,ease:'power3.out'},7.6);
tl.to('#tot',{opacity:0,duration:.3},9.2);
// agents replace them
for(let i=0;i<5;i++){ tl.to('#pn-'+i+' .ag',{opacity:1,duration:.25},9.8+i*.4); tl.to('#pn-'+i+' .pt',{opacity:0,duration:.2},9.8+i*.4); }
tl.to('.room',{borderColor:'rgba(140,150,255,.9)',backgroundColor:'rgba(140,150,255,.08)',duration:.6},9.8);
tl.fromTo('#tls',{opacity:0,y:20},{opacity:1,y:0,duration:.45,ease:'power3.out'},11.2);
tl.to('#eng',{opacity:0,duration:.3},12.6);
tl.fromTo('#res',{opacity:0},{opacity:1,duration:.4},13.8);
tl.fromTo('#res div',{opacity:0,y:40},{opacity:1,y:0,duration:.5,stagger:.35,ease:'power3.out',immediateRender:false},13.9);
tl.fromTo('#dsc',{opacity:0},{opacity:1,duration:.4},14.8);
xMorph(tl,'#lg',17.1);
tl.fromTo('#wm',{opacity:0,y:30},{opacity:1,y:0,duration:.5,ease:'power3.out'},17.5);
tl.fromTo('#tg',{opacity:0},{opacity:1,duration:.4},17.9);
tl.fromTo('#ct',{opacity:0,scale:.9},{opacity:1,scale:1,duration:.4,ease:'back.out(1.8)'},18.2);
""")

# ======================================================================= 2 · Same day (9:16, 18 s)
EVENTS = [(3.0, "New lead", "8:14", "Reply at 4:52 PM · lost", "Replied in 42 s · booked"),
          (5.0, "Quote request", "9:30", "Sent 2 days later", "Sent in 5 minutes"),
          (7.0, "Purchase order PDF", "11:05", "Typed by hand · 25 min", "In the ERP in 90 s"),
          (9.0, "Missed call", "12:40", "No callback", "Texted back · rescheduled"),
          (11.0, "Invoice 30 days late", "15:00", "Forgot to chase", "Reminder sent · paid")]
def feed(side):
    rows = []
    for i, (t, ev, tm, bad, good) in enumerate(EVENTS):
        out = bad if side == "w" else good
        rows.append(f'<div class="ev" id="{side}{i}"><span class="tm mono">{tm}</span><span class="en">{ev}</span><span class="oc {"bad" if side == "w" else "good"}">{out}</span></div>')
    return "".join(rows)

C["r4-2-same-day"] = dict(W=1080, H=1920, zoom=1/3, dur=18,
    music=lambda p: synth.explainer(p, 18, [3.0, 13.4, 15.6], 3.0, 13.4, bpm=120, pings=[e[0] for e in EVENTS], ticks_to=3.0), css="""
.half{position:absolute;left:0;right:0;height:900px;padding:40px 60px;box-sizing:border-box}
.half.w{top:0;background:linear-gradient(180deg,#15120E,#0B0A09)}
.half.x{bottom:0;background:linear-gradient(180deg,#0B0D1C,#070812)}
.hd{display:flex;justify-content:space-between;align-items:center;font:600 26px 'IBM Plex Mono',monospace;letter-spacing:.14em}
.w .hd{color:#F2A33A}.x .hd{color:#8C96FF}
.ev{display:grid;grid-template-columns:120px 1fr;gap:4px 20px;align-items:baseline;padding:20px 0;border-bottom:1px solid rgba(255,255,255,.08);opacity:0}
.tm{font-size:24px;color:rgba(255,255,255,.5);grid-row:span 2}
.en{font-size:34px;font-weight:650}
.oc{font-size:30px;font-weight:600}
.oc.bad{color:#F2A33A}.oc.good{color:#8C96FF}
.score{position:absolute;left:60px;right:60px;bottom:40px;display:flex;justify-content:space-between;font-size:30px;color:rgba(255,255,255,.72)}
.score b{color:#fff;font-size:44px;font-weight:800;margin-left:8px;font-variant-numeric:tabular-nums}
.mid{position:absolute;left:0;right:0;top:900px;height:120px;margin-top:-60px;display:flex;align-items:center;justify-content:center;z-index:3}
.clk{padding:18px 36px;border-radius:999px;background:#fff;color:#000;font:700 48px 'IBM Plex Mono',monospace;font-variant-numeric:tabular-nums;box-shadow:0 10px 40px rgba(0,0,0,.6)}
.intro{position:absolute;inset:0;background:#000;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:0 90px;z-index:4}
.intro p{margin:0;font-weight:750;font-stretch:112%;font-size:96px;letter-spacing:-3px;line-height:1}
.intro small{margin-top:30px;font-size:40px;color:rgba(255,255,255,.7)}
.res{position:absolute;inset:0;background:#000;display:flex;flex-direction:column;justify-content:center;padding:0 90px;gap:40px;opacity:0;z-index:4}
.res p{margin:0;font-weight:750;font-stretch:112%;font-size:92px;letter-spacing:-3px;line-height:1}
.res p span{color:#8C96FF}
.res small{font:500 22px 'IBM Plex Mono',monospace;color:rgba(255,255,255,.45)}
.endcard{gap:34px;z-index:5;padding:0 90px}
.endcard .xl{width:200px;height:200px}.endcard .wm{font-size:120px}.endcard .tag{font-size:46px}
.cta{display:inline-flex;align-items:center;gap:14px;padding:26px 44px;border-radius:999px;background:#8C96FF;color:#06080D;font-weight:750;font-size:42px}
""", body=f"""
<div class="half w"><div class="hd"><span>WITHOUT AGENTS</span><span>Same business</span></div>{feed("w")}
  <div class="score"><span>Jobs booked<b id="sw1">0</b></span><span>Hours at the desk<b id="sw2">0</b></span></div></div>
<div class="half x"><div class="hd"><span>WITH XFORWARD AGENTS</span><span>Same day</span></div>{feed("x")}
  <div class="score"><span>Jobs booked<b id="sx1">0</b></span><span>Hours at the desk<b id="sx2">0</b></span></div></div>
<div class="mid"><div class="clk" id="clk">08:00</div></div>
<div class="intro" id="in"><p>Same business. Same day.</p><small>Two ways to run it.</small></div>
<div class="res" id="res"><p>Same team.</p><p><span>2× the jobs booked.</span></p><p><span>4 hours</span> back. Every day.</p><small>Illustrative day for a small service business.</small></div>
<section id="endS" class="clip" data-start="15.6" data-duration="2.4"><div class="endcard">
  <div id="lg">{XLOGO}</div><div class="wm" id="wm"><b>X</b>Forward</div><div class="tag" id="tg">We build the agents. You get the day back.</div>
  <div class="cta" id="ct">Book a free call {ARROW}</div></div></section>
""", js=f"""
const EV={[e[0] for e in EVENTS]};
tl.fromTo('#in p',{{opacity:0,y:30}},{{opacity:1,y:0,duration:.5,ease:'power3.out'}},.2);
tl.fromTo('#in small',{{opacity:0}},{{opacity:1,duration:.4}},.9);
tl.to('#in',{{opacity:0,duration:.35}},2.6);
const clk={{m:8*60}};
tl.to(clk,{{m:18*60,duration:10.4,ease:'none',onUpdate:()=>{{const h=Math.floor(clk.m/60),m=Math.floor(clk.m%60);document.getElementById('clk').textContent=String(h).padStart(2,'0')+':'+String(m).padStart(2,'0')}}}},3.0);
EV.forEach((t,i)=>{{
  tl.fromTo('#w'+i,{{opacity:0,x:-40}},{{opacity:1,x:0,duration:.35,ease:'power3.out'}},t);
  tl.fromTo('#x'+i,{{opacity:0,x:40}},{{opacity:1,x:0,duration:.35,ease:'power3.out'}},t+.12);}});
const cnt=(sel,to,a,d)=>{{const o={{v:0}};tl.to(o,{{v:to,duration:d,ease:'none',onUpdate:()=>{{document.querySelector(sel).textContent=Math.round(o.v)}}}},a)}};
cnt('#sw1',3,3,10.4); cnt('#sx1',6,3,10.4); cnt('#sw2',11,3,10.4); cnt('#sx2',7,3,10.4);
tl.fromTo('#res',{{opacity:0}},{{opacity:1,duration:.3}},13.4);
tl.fromTo('#res p',{{opacity:0,y:40}},{{opacity:1,y:0,duration:.45,stagger:.5,ease:'power3.out',immediateRender:false}},13.5);
tl.fromTo('#res small',{{opacity:0}},{{opacity:1,duration:.4,immediateRender:false}},14.9);
xMorph(tl,'#lg',15.7);
tl.fromTo('#wm',{{opacity:0,y:30}},{{opacity:1,y:0,duration:.45,ease:'power3.out'}},16.1);
tl.fromTo('#tg',{{opacity:0}},{{opacity:1,duration:.4}},16.4);
tl.fromTo('#ct',{{opacity:0,scale:.9}},{{opacity:1,scale:1,duration:.35,ease:'back.out(1.8)'}},16.7);
""")

# ======================================================================= 3 · The offer (1:1, 15 s)
STATS = [(2.6, "6 weeks", "From first call to agents live."),
         (4.7, "< 60 s", "Every lead answered. Day and night."),
         (6.8, "27 h", "Back to your team. Every week."),
         (8.9, "1 fixed price", "Agreed upfront. No surprises.")]
stats_html = "".join(f'<div class="st" id="s{i}"><b>{n}</b><span>{d}</span></div>' for i, (_, n, d) in enumerate(STATS))

C["r4-3-the-offer"] = dict(W=1080, H=1080, zoom=4/9, dur=15,
    music=lambda p: synth.explainer(p, 15, [2.6, 4.7, 6.8, 8.9, 11.2], 2.6, 11.2, bpm=112), css="""
.bgo{position:absolute;inset:0;background:#05060A}
.orb{position:absolute;width:1000px;height:1000px;left:40px;top:40px;border-radius:50%;background:radial-gradient(circle,rgba(35,52,224,.55),transparent 65%)}
.hl{position:absolute;left:90px;right:90px;top:0;bottom:0;display:flex;flex-direction:column;justify-content:center}
.hl p{margin:0;font-weight:800;font-stretch:120%;font-size:104px;letter-spacing:-4px;line-height:.98}
.hl p .acc{color:#8C96FF}
.hl .w{display:inline-block;opacity:0}
.st{position:absolute;left:90px;right:90px;top:0;bottom:0;display:flex;flex-direction:column;justify-content:center;opacity:0}
.st b{font-weight:850;font-stretch:118%;font-size:150px;white-space:nowrap;letter-spacing:-9px;line-height:.9;color:#fff}
.st span{margin-top:30px;font-size:52px;color:rgba(255,255,255,.8);font-weight:550;letter-spacing:-1px}
.idx{position:absolute;left:90px;bottom:80px;display:flex;gap:10px}
.idx i{display:block;width:60px;height:5px;border-radius:5px;background:rgba(255,255,255,.18)}
.disc{position:absolute;right:90px;bottom:70px;font:500 18px 'IBM Plex Mono',monospace;color:rgba(255,255,255,.4);opacity:0}
.keep{position:absolute;left:90px;right:90px;top:0;bottom:0;display:flex;flex-direction:column;justify-content:center;opacity:0}
.keep p{margin:0;font-weight:800;font-stretch:118%;font-size:96px;letter-spacing:-3.5px;line-height:1}
.keep p span{color:#8C96FF}
.endcard{gap:30px;padding:0 80px;background:#05060A}
.endcard .xl{width:170px;height:170px}.endcard .wm{font-size:110px}
.cta{display:inline-flex;align-items:center;gap:14px;padding:26px 40px;border-radius:999px;background:#8C96FF;color:#06080D;font-weight:750;font-size:40px}
.sub{font-size:34px;color:rgba(255,255,255,.7)}
""", body=f"""
<div class="bgo"></div><div class="orb" id="orb"></div>
<div class="hl" id="hl"><p><span class="w">We</span> <span class="w">put</span> <span class="w acc">AI</span> <span class="w acc">agents</span></p><p><span class="w">to</span> <span class="w">work</span> <span class="w">in</span> <span class="w">your</span> <span class="w">business.</span></p></div>
{stats_html}
<div class="idx" id="idx"><i></i><i></i><i></i><i></i></div>
<p class="disc" id="dsc">Typical targets</p>
<div class="keep" id="kp"><p>You keep the agents.</p><p><span>And the hours.</span></p></div>
<section id="endS" class="clip" data-start="12.2" data-duration="2.8"><div class="endcard">
  <div id="lg">{XLOGO}</div><div class="wm" id="wm"><b>X</b>Forward</div>
  <div class="cta" id="ct">Book a free 20-min call {ARROW}</div><div class="sub" id="sb">We'll find your first agent.</div></div></section>
""", js=f"""
const ST={[s[0] for s in STATS]};
tl.fromTo('#hl .w',{{opacity:0,y:50}},{{opacity:1,y:0,duration:.28,stagger:.15,ease:'power4.out'}},.15);
tl.to('#hl',{{opacity:0,duration:.25}},2.4);
ST.forEach((t,i)=>{{const end=i<ST.length-1?ST[i+1]:11.0;
  tl.fromTo('#s'+i,{{opacity:0,scale:1.12}},{{opacity:1,scale:1,duration:.35,ease:'power4.out',immediateRender:false}},t);
  tl.fromTo('#s'+i+' span',{{opacity:0,y:20}},{{opacity:1,y:0,duration:.35,ease:'power3.out',immediateRender:false}},t+.25);
  tl.to('#s'+i,{{opacity:0,duration:.2}},end-.2);
  tl.to('#idx i:nth-child('+(i+1)+')',{{backgroundColor:'#8C96FF',duration:.2}},t);
  tl.fromTo('#orb',{{x:[0,420,-240,300][i]-150,y:[0,-200,260,-120][i]-100}},{{x:[420,-240,300,0][i]-150,y:[-200,260,-120,0][i]-100,duration:2.1,ease:'power2.inOut',immediateRender:false}},t);}});
tl.fromTo('#dsc',{{opacity:0}},{{opacity:1,duration:.3}},2.8); tl.to(['#dsc','#idx'],{{opacity:0,duration:.2}},10.9);
tl.fromTo('#kp p',{{opacity:0,y:40}},{{opacity:1,y:0,duration:.45,stagger:.4,ease:'power3.out'}},11.2);
tl.to('#kp',{{opacity:0,duration:.2}},12.1);
xMorph(tl,'#lg',12.3);
tl.fromTo('#wm',{{opacity:0,y:30}},{{opacity:1,y:0,duration:.45,ease:'power3.out'}},12.7);
tl.fromTo('#ct',{{opacity:0,scale:.9}},{{opacity:1,scale:1,duration:.35,ease:'back.out(1.8)'}},13.1);
tl.fromTo('#sb',{{opacity:0}},{{opacity:1,duration:.4}},13.5);
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
