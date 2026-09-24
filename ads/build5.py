"""Round 5: same clear message, four distinct visual styles and formats.

Bauhaus poster (4:5) · Whiteboard sketch (16:9) · Warm & human (9:16) ·
Neo-brutalist (1:1). GSAP + synthesized tracks.
"""
import json, os, shutil, sys
from build3 import page
import synth

HERE = os.path.dirname(os.path.abspath(__file__))
DRAFT = "--final" not in sys.argv
C = {}


def mark(stroke1, stroke2, cls="xl", idn=""):
    return (f'<svg class="{cls}" {f"id={chr(34)}{idn}{chr(34)}" if idn else ""} viewBox="0 0 24 24" aria-hidden="true">'
            f'<path class="m1" d="M5 5l7 7-7 7" style="stroke:{stroke1}"/><path class="m2" d="M12 5l7 7-7 7" style="stroke:{stroke2}"/></svg>')


# ======================================================================= 1 · Bauhaus poster (4:5)
TASKS = ["EMAILS", "QUOTES", "INVOICES", "CALLS", "ORDERS", "FOLLOW-UPS", "BOOKINGS", "REMINDERS", "DATA ENTRY"]
SCATTER = [(140, 520), (610, 470), (880, 640), (300, 760), (720, 830), (120, 930), (520, 990), (860, 1030), (360, 610)]
GRID = [(150 + (i % 3) * 300, 520 + (i // 3) * 190) for i in range(9)]
dots = "".join(f'<div class="dot" id="d{i}"><span>{t}</span></div>' for i, t in enumerate(TASKS))
agents = "".join(f'<div class="agt" id="g{i}"><span>AGENT</span></div>' for i in range(9))

C["r5-1-bauhaus"] = dict(W=1080, H=1350, zoom=4/9, dur=16,
    music=lambda p: synth.explainer(p, 16, [2.5, 5.0, 9.0, 12.2], 5.0, 12.2, bpm=118), css="""
.stage{background:#F2EEE3;color:#111}
.hd{position:absolute;left:70px;right:70px;top:70px;font-family:'Archivo';font-weight:900;font-stretch:62%;font-size:150px;line-height:.86;letter-spacing:-2px;text-transform:uppercase;margin:0;opacity:0}
.hd .r{color:#E63B2E}.hd .b{color:#2334E0}
.circ{position:absolute;width:420px;height:420px;border-radius:50%;background:#E63B2E;left:620px;top:900px}
.sq{position:absolute;width:260px;height:260px;background:#F5C518;left:-60px;top:1120px}
.bar{position:absolute;left:0;right:0;top:420px;height:14px;background:#111;transform-origin:left center}
.dot{position:absolute;left:0;top:0;width:150px;height:150px;margin:-75px 0 0 -75px;border-radius:50%;background:#E63B2E;display:grid;place-items:center;opacity:0}
.dot span{font:700 17px 'IBM Plex Mono',monospace;color:#F2EEE3;letter-spacing:.06em}
.agt{position:absolute;left:0;top:0;width:170px;height:170px;margin:-85px 0 0 -85px;background:#2334E0;display:grid;place-items:center;opacity:0}
.agt span{font:700 18px 'IBM Plex Mono',monospace;color:#F2EEE3;letter-spacing:.1em}
.res{position:absolute;left:70px;right:70px;top:470px;display:flex;flex-direction:column;gap:18px}
.res p{margin:0;font-family:'Archivo';font-weight:900;font-stretch:62%;font-size:132px;line-height:.9;text-transform:uppercase;opacity:0;letter-spacing:-1px}
.res p:nth-child(1){color:#2334E0}.res p:nth-child(2){color:#E63B2E}.res p:nth-child(3){color:#111}
.res small{font:600 20px 'IBM Plex Mono',monospace;opacity:0;color:#555}
.end{position:absolute;inset:0;background:#2334E0;display:flex;flex-direction:column;justify-content:flex-end;padding:70px;opacity:0;color:#F2EEE3}
.end .xl{width:260px;height:260px;margin-bottom:40px}
.end .xl path{fill:none;stroke-width:2.6;stroke-linecap:square;stroke-linejoin:miter}
.end h2{margin:0;font-family:'Archivo';font-weight:900;font-stretch:62%;font-size:230px;line-height:.82;text-transform:uppercase}
.end p{margin:26px 0 0;font:600 34px 'IBM Plex Mono',monospace}
.end .ball{position:absolute;right:-120px;top:-120px;width:520px;height:520px;border-radius:50%;background:#F5C518}
""", body=f"""
<div class="circ" id="ci"></div><div class="sq" id="sq"></div><i class="bar" id="br"></i>
<p class="hd" id="h1">Your team is busy.</p>
<p class="hd" id="h2">With the <span class="r">wrong</span> work.</p>
<p class="hd" id="h3">We build <span class="b">AI agents</span></p>
<p class="hd" id="h4">that do it <span class="b">for them.</span></p>
{dots}{agents}
<div class="res" id="rs"><p>27 h / week back</p><p>Replies &lt; 60 s</p><p>6 weeks. Fixed price.</p><small>Typical targets, confirmed in your diagnostic.</small></div>
<div class="end" id="en"><div class="ball"></div>{mark('#F2EEE3', '#F5C518', idn='lgB')}<h2>XForward</h2><p>AI agents, built into your business. · Book a free call</p></div>
""", js=f"""
const SC={json.dumps(SCATTER)}, GR={json.dumps(GRID)};
tl.fromTo('#ci',{{x:700,rotation:0}},{{x:0,duration:1,ease:'power3.out'}},0);
tl.fromTo('#sq',{{y:400}},{{y:0,duration:.9,ease:'power3.out'}},.2);
tl.fromTo('#br',{{scaleX:0}},{{scaleX:1,duration:.7,ease:'power3.inOut'}},.3);
const hd=(s,a,b)=>{{tl.fromTo(s,{{opacity:0,y:60}},{{opacity:1,y:0,duration:.35,ease:'power4.out'}},a); if(b) tl.to(s,{{opacity:0,duration:.15}},b)}};
hd('#h1',.4,2.35); hd('#h2',2.5,4.85); hd('#h3',5.0,8.85); hd('#h4',9.0,11.9);
// tasks: chaos
SC.forEach((p,i)=>{{
  tl.fromTo('#d'+i,{{x:p[0],y:p[1]-500,opacity:0,scale:.5}},{{y:p[1],opacity:1,scale:1,duration:.5,ease:'bounce.out',immediateRender:false}},2.6+i*.12);
  tl.to('#d'+i,{{x:p[0]+((i%2)?40:-40),y:p[1]+((i%3)?-30:30),duration:.6,yoyo:true,repeat:2,ease:'sine.inOut'}},3.8);}});
tl.to('#ci',{{scale:.6,x:120,y:120,duration:1,ease:'power2.inOut'}},2.6);
// agents arrive, snap to grid, cover tasks
GR.forEach((g,i)=>{{
  tl.to('#d'+i,{{x:g[0],y:g[1],duration:.45,ease:'power3.inOut'}},5.4+i*.08);
  tl.fromTo('#g'+i,{{x:g[0]+900,y:g[1],opacity:1}},{{x:g[0],duration:.5,ease:'power3.out',immediateRender:false}},6.2+i*.14);
  tl.to('#d'+i,{{opacity:0,duration:.1}},6.65+i*.14);}});
tl.to(['.agt','#ci','#sq'],{{opacity:0,duration:.3}},8.8);
tl.fromTo('#rs p',{{opacity:0,x:-80}},{{opacity:1,x:0,duration:.4,stagger:.55,ease:'power4.out'}},9.5);
tl.fromTo('#rs small',{{opacity:0}},{{opacity:1,duration:.3}},11.2);
tl.to(['#rs','#br'],{{opacity:0,duration:.2}},12.0);
tl.fromTo('#en',{{opacity:0,yPercent:100}},{{opacity:1,yPercent:0,duration:.5,ease:'power4.out'}},12.2);
xMorph(tl,'#lgB',12.7);
""")

# ======================================================================= 2 · Whiteboard (16:9)
C["r5-2-whiteboard"] = dict(W=1920, H=1080, zoom=1/3, dur=20,
    music=lambda p: synth.explainer(p, 20, [5.0, 8.2, 12.3, 16.2], 12.3, 16.2, bpm=96, ticks_to=0.0,
                                    chords=[[196, 246.9, 293.7], [220, 277.2, 329.6], [174.6, 220, 261.6], [196, 246.9, 293.7, 392]]), css="""
.stage{background:#FBFBF8;color:#1d1d1f;font-family:'Caveat',cursive}
.board{position:absolute;inset:0;background:radial-gradient(ellipse at 30% 20%,#fff,#F1F1EC 80%)}
.hw{position:absolute;margin:0;font-weight:700;line-height:1;white-space:nowrap}
svg.ink{position:absolute;left:0;top:0;width:1920px;height:1080px;overflow:visible}
svg.ink path,svg.ink circle,svg.ink rect,svg.ink ellipse{fill:none;stroke-linecap:round;stroke-linejoin:round}
.k{stroke:#1d1d1f;stroke-width:6}.bl{stroke:#1f4bd8;stroke-width:6}.rd{stroke:#d93025;stroke-width:7}.gr{stroke:#188038;stroke-width:8}
.list{position:absolute;left:1260px;top:300px;display:flex;flex-direction:column;gap:26px}
.list p{margin:0;font-size:74px;font-weight:700;white-space:nowrap}
.list b{color:#188038}
.brand{position:absolute;left:1260px;top:830px;display:flex;align-items:center;gap:24px}
.brand .xl{width:90px;height:90px}
.brand .xl path{fill:none;stroke-width:2.6;stroke-linecap:round;stroke-linejoin:round}
.brand span{font-family:'Archivo';font-weight:750;font-stretch:118%;font-size:80px;letter-spacing:-3px}
.brand span b{color:#1f4bd8}
.cta{position:absolute;left:1260px;top:950px;font-size:58px;font-weight:700;color:#1f4bd8}
""", body=f"""
<div class="board"></div>
<p class="hw" id="t0" style="left:110px;top:60px;font-size:96px">How XForward works</p>
<svg class="ink" viewBox="0 0 1920 1080">
  <path id="u0" class="bl" d="M112 170 Q400 162 700 176 T860 168"/>
  <path id="house" class="k" d="M150 420 L520 250 L890 420 M190 400 L188 900 L852 902 L850 400"/>
  <rect id="b1" class="k" x="240" y="470" width="260" height="150" rx="14"/>
  <rect id="b2" class="k" x="540" y="470" width="260" height="150" rx="14"/>
  <rect id="b3" class="k" x="240" y="680" width="260" height="150" rx="14"/>
  <rect id="b4" class="k" x="540" y="680" width="260" height="150" rx="14"/>
  <ellipse id="c1" class="rd" cx="370" cy="545" rx="160" ry="100"/>
  <ellipse id="c2" class="rd" cx="670" cy="545" rx="160" ry="100"/>
  <ellipse id="c3" class="rd" cx="370" cy="755" rx="160" ry="100"/>
  <ellipse id="c4" class="rd" cx="670" cy="755" rx="160" ry="100"/>
  <path id="eng" class="bl" d="M1010 520 a30 30 0 1 0 0.1 0 M1010 580 L1010 690 M1010 610 L960 650 M1010 610 L1060 650 M1010 690 L975 770 M1010 690 L1045 770"/>
  <path id="bot" class="bl" d="M950 820 h120 v90 h-120 z M985 855 h0 M1035 855 h0 M1010 820 v-30 M995 885 q15 10 30 0"/>
  <path id="ar1" class="bl" d="M960 860 Q880 820 810 760"/><path id="ar2" class="bl" d="M960 850 Q880 700 810 560"/>
  <path id="k1" class="gr" d="M270 520 l25 25 l45 -55"/><path id="k2" class="gr" d="M570 520 l25 25 l45 -55"/>
  <path id="k3" class="gr" d="M270 730 l25 25 l45 -55"/><path id="k4" class="gr" d="M570 730 l25 25 l45 -55"/>
  <path id="ul" class="bl" d="M1255 1030 Q1500 1020 1780 1034"/>
</svg>
<p class="hw" id="lb" style="left:380px;top:925px;font-size:56px">your business</p>
<p class="hw" id="w1" style="left:285px;top:515px;font-size:50px">emails</p>
<p class="hw" id="w2" style="left:585px;top:515px;font-size:50px">quotes</p>
<p class="hw" id="w3" style="left:280px;top:725px;font-size:50px">invoices</p>
<p class="hw" id="w4" style="left:585px;top:725px;font-size:50px">calls</p>
<p class="hw" id="w5" style="left:880px;top:190px;font-size:84px;color:#d93025;transform:rotate(-6deg)">27 h / week lost!</p>
<p class="hw" id="w6" style="left:1070px;top:520px;font-size:54px;color:#1f4bd8">our engineer</p>
<p class="hw" id="w7" style="left:1090px;top:850px;font-size:54px;color:#1f4bd8">AI agents</p>
<div class="list"><p id="l1"><b>✓</b> 27 h / week back</p><p id="l2"><b>✓</b> replies in &lt; 60 s</p><p id="l3"><b>✓</b> live in 6 weeks</p><p id="l4"><b>✓</b> fixed price</p></div>
<div class="brand" id="bd">{mark('#1d1d1f', '#1f4bd8', idn='lgW')}<span><b>X</b>Forward</span></div>
<p class="hw cta" id="ct">Book a free call →</p>
""", js="""
const draw=(sel,a,d)=>{const el=document.querySelector(sel);const L=el.getTotalLength();tl.fromTo(el,{strokeDasharray:L,strokeDashoffset:L},{strokeDashoffset:0,duration:d,ease:'power1.inOut'},a)};
const write=(sel,a,d)=>tl.fromTo(sel,{clipPath:'inset(-20% 100% -20% -2%)'},{clipPath:'inset(-20% -2% -20% -2%)',duration:d,ease:'none'},a);
write('#t0',.2,1.1); draw('#u0',1.2,.4);
draw('#house',1.6,1.1); write('#lb',2.6,.6);
['#b1','#b2','#b3','#b4'].forEach((s,i)=>draw(s,2.9+i*.3,.35));
['#w1','#w2','#w3','#w4'].forEach((s,i)=>write(s,3.2+i*.3,.4));
['#c1','#c2','#c3','#c4'].forEach((s,i)=>draw(s,5.0+i*.35,.4));
write('#w5',6.5,.9);
draw('#eng',8.2,1.0); write('#w6',9.1,.6);
draw('#bot',9.9,.8); write('#w7',10.6,.5);
draw('#ar1',11.1,.4); draw('#ar2',11.4,.4);
['#k1','#k2','#k3','#k4'].forEach((s,i)=>draw(s,11.9+i*.2,.25));
tl.to(['#c1','#c2','#c3','#c4','#w5'],{opacity:.18,duration:.4},12.3);
['#l1','#l2','#l3','#l4'].forEach((s,i)=>write(s,12.6+i*.8,.6));
tl.fromTo('#bd',{opacity:0,y:20},{opacity:1,y:0,duration:.4},16.2);
xMorph(tl,'#lgW',16.3);
write('#ct',17.2,.8); draw('#ul',18.0,.5);
""")

# ======================================================================= 3 · Warm & human (9:16)
C["r5-3-warm"] = dict(W=1080, H=1920, zoom=1/3, dur=16,
    music=lambda p: synth.explainer(p, 16, [5.5, 12.6], 99, 99, bpm=80,
                                    chords=[[146.8, 220, 293.7], [130.8, 196, 261.6, 329.6], [146.8, 220, 293.7, 370]]), css="""
.stage{background:#F6EFE6;color:#1F3B2F;font-family:'DM Sans',sans-serif}
.blob{position:absolute;border-radius:50%;filter:blur(40px)}
.b1{width:900px;height:900px;left:-200px;top:-150px;background:#F4BFA6}
.b2{width:800px;height:800px;left:400px;top:900px;background:#B9CDB3}
.b3{width:600px;height:600px;left:500px;top:200px;background:#F7D9A8}
.big{position:absolute;left:90px;right:90px;margin:0;font-family:'Instrument Serif',serif;line-height:.98;letter-spacing:-1px;opacity:0}
.card{position:absolute;left:120px;right:120px;padding:38px 42px;border-radius:40px;background:rgba(255,255,255,.72);box-shadow:0 30px 60px -30px rgba(31,59,47,.35);
  display:flex;align-items:center;gap:26px;font-size:42px;font-weight:600;opacity:0}
.card i{flex:none;width:64px;height:64px;border-radius:50%;background:#F4BFA6;display:grid;place-items:center;font-style:normal;font-size:34px}
.card .done{margin-left:auto;padding:10px 20px;border-radius:999px;background:#1F3B2F;color:#F6EFE6;font-size:28px;opacity:0}
.win{position:absolute;left:90px;right:90px;top:620px;display:flex;flex-direction:column;gap:40px}
.win p{margin:0;font-family:'Instrument Serif',serif;font-size:120px;line-height:1;opacity:0}
.win p span{font-style:italic;color:#C0674A}
.end{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:34px;text-align:center;padding:0 110px;opacity:0}
.end .xl{width:190px;height:190px}.end .xl path{fill:none;stroke-width:2.3;stroke-linecap:round;stroke-linejoin:round}
.end .wm{font-family:'Instrument Serif',serif;font-size:150px;line-height:1}
.end .tg{font-size:44px;opacity:.8}
.end .cta{margin-top:20px;padding:28px 46px;border-radius:999px;background:#1F3B2F;color:#F6EFE6;font-size:40px;font-weight:600}
""", body=f"""
<div class="blob b1" id="bl1"></div><div class="blob b2" id="bl2"></div><div class="blob b3" id="bl3"></div>
<p class="big" id="a1" style="top:260px;font-size:230px">5:00 PM.</p>
<p class="big" id="a2" style="top:520px;font-size:96px">The shop is closed.</p>
<p class="big" id="a3" style="top:260px;font-size:120px"><i>But the work isn’t.</i></p>
<div class="card" id="c0" style="top:640px"><i>✉</i>12 emails to answer<span class="done">Done</span></div>
<div class="card" id="c1" style="top:830px"><i>$</i>3 quotes to send<span class="done">Done</span></div>
<div class="card" id="c2" style="top:1020px"><i>⏱</i>Invoices to chase<span class="done">Done</span></div>
<div class="card" id="c3" style="top:1210px"><i>☎</i>2 calls to return<span class="done">Done</span></div>
<p class="big" id="a4" style="top:1450px;font-size:84px">Our AI agents take it from here.</p>
<div class="win"><p id="v1">Dinner <span>at home.</span></p><p id="v2">Weekends <span>off.</span></p><p id="v3">Every customer <span>answered.</span></p></div>
<div class="end" id="en">{mark('#1F3B2F', '#C0674A', idn='lgH')}<div class="wm">XForward</div><div class="tg">AI agents, built into your business.</div><div class="cta">Book a free call</div></div>
""", js="""
tl.fromTo('#bl1',{x:0,y:0},{x:160,y:120,duration:16,ease:'sine.inOut'},0);
tl.fromTo('#bl2',{x:0,y:0},{x:-180,y:-160,duration:16,ease:'sine.inOut'},0);
tl.fromTo('#bl3',{x:0,y:0},{x:-120,y:200,duration:16,ease:'sine.inOut'},0);
const soft=(s,a,b)=>{tl.fromTo(s,{opacity:0,y:40},{opacity:1,y:0,duration:.9,ease:'power2.out'},a);if(b)tl.to(s,{opacity:0,y:-20,duration:.5},b)};
soft('#a1',.2,2.5); soft('#a2',.9,2.5); soft('#a3',2.8,8.6);
for(let i=0;i<4;i++){ soft('#c'+i,3.3+i*.45,0);
  tl.to('#c'+i+' .done',{opacity:1,duration:.3},6.2+i*.35);
  tl.to('#c'+i,{y:-500-i*60,opacity:0,duration:1.2,ease:'power2.in'},7.2+i*.25);}
soft('#a4',5.5,8.6);
['#v1','#v2','#v3'].forEach((s,i)=>soft(s,9.0+i*1.1,12.4));
tl.fromTo('#en',{opacity:0},{opacity:1,duration:.8},12.6);
xMorph(tl,'#lgH',12.9);
""")

# ======================================================================= 4 · Neo-brutalist (1:1)
C["r5-4-brutalist"] = dict(W=1080, H=1080, zoom=4/9, dur=15,
    music=lambda p: synth.explainer(p, 15, [2.2, 4.8, 8.2, 11.2], 2.2, 11.2, bpm=128), css="""
.stage{background:#FFE14D;color:#111;font-family:'Bricolage Grotesque',sans-serif}
.box{position:absolute;border:6px solid #111;box-shadow:12px 12px 0 #111;border-radius:22px;background:#fff;box-sizing:border-box}
.ttl{left:70px;top:90px;right:70px;padding:30px 40px;background:#B6F36A;opacity:0}
.ttl h1{margin:0;font-size:150px;font-weight:800;letter-spacing:-5px;line-height:.9}
.ttl p{margin:10px 0 0;font-size:48px;font-weight:600}
.stk{position:absolute;padding:14px 26px;border:5px solid #111;border-radius:999px;background:#FF8FD8;font-weight:800;font-size:40px;opacity:0;box-shadow:6px 6px 0 #111}
.lbl{position:absolute;left:70px;top:90px;font-size:64px;font-weight:800;opacity:0;margin:0}
.do{width:450px;height:250px;padding:28px;display:flex;align-items:flex-end;font-size:50px;font-weight:800;line-height:1;opacity:0}
.win{left:70px;right:70px;height:210px;display:flex;align-items:center;justify-content:space-between;padding:0 44px;opacity:0}
.win b{font-size:120px;font-weight:800;letter-spacing:-5px}
.win span{font-size:42px;font-weight:700;text-align:right;max-width:9em;line-height:1.05}
.steps{position:absolute;left:70px;right:70px;top:320px;display:flex;flex-direction:column;gap:30px}
.stp{position:relative;height:150px;display:flex;align-items:center;gap:28px;padding:0 34px;font-size:56px;font-weight:800;opacity:0}
.stp i{font-style:normal;width:90px;height:90px;border-radius:50%;border:5px solid #111;display:grid;place-items:center;background:#FFE14D;font-size:50px}
.end{position:absolute;inset:0;background:#111;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:34px;opacity:0}
.end .xl{width:170px;height:170px}.end .xl path{fill:none;stroke-width:2.8;stroke-linecap:round;stroke-linejoin:round}
.end .wm{font-size:140px;font-weight:800;color:#FFE14D;letter-spacing:-5px}
.btn{position:relative;padding:30px 50px;border:6px solid #FFE14D;border-radius:24px;background:#B6F36A;color:#111;font-size:52px;font-weight:800;box-shadow:12px 12px 0 #FFE14D}
""", body=f"""
<div class="box ttl" id="tt"><h1>AI agents</h1><p>for your business. Built by us.</p></div>
<div class="stk" id="sk1" style="left:640px;top:420px">no code needed</div>
<p class="lbl" id="lb1">What they do:</p>
<div class="box do" id="o1" style="left:70px;top:210px;background:#B6F36A">Answer every lead in 60 s</div>
<div class="box do" id="o2" style="left:560px;top:210px;background:#FF8FD8">Send your quotes</div>
<div class="box do" id="o3" style="left:70px;top:520px;background:#6C8CFF">Chase your invoices</div>
<div class="box do" id="o4" style="left:560px;top:520px;background:#FF7A45">Enter your orders</div>
<p class="lbl" id="lb2">What you win:</p>
<div class="box win" id="v1" style="top:210px;background:#B6F36A"><b>27 h</b><span>back every week</span></div>
<div class="box win" id="v2" style="top:470px;background:#FF8FD8"><b>2×</b><span>more jobs booked</span></div>
<div class="box win" id="v3" style="top:730px;background:#6C8CFF"><b>0</b><span>missed calls</span></div>
<p class="lbl" id="lb3">How:</p>
<div class="steps"><div class="box stp" id="p1"><i>1</i>We find the work</div><div class="box stp" id="p2"><i>2</i>We build the agents</div><div class="box stp" id="p3"><i>3</i>You keep the hours</div></div>
<div class="stk" id="sk2" style="left:600px;top:880px;background:#B6F36A">fixed price</div>
<div class="end" id="en">{mark('#FFE14D', '#B6F36A', idn='lgN')}<div class="wm">XForward</div><div class="btn" id="bt">Book a free call →</div></div>
""", js="""
const pop=(s,a)=>tl.fromTo(s,{opacity:0,scale:.6,y:40},{opacity:1,scale:1,y:0,duration:.4,ease:'back.out(2.2)',immediateRender:false},a);
const out=(s,a)=>tl.to(s,{opacity:0,duration:.15},a);
const stk=(s,a,r)=>tl.fromTo(s,{opacity:0,scale:1.8,rotation:r*2},{opacity:1,scale:1,rotation:r,duration:.3,ease:'power4.in',immediateRender:false},a);
pop('#tt',.1); stk('#sk1',1.0,-8); out(['#tt','#sk1'],2.05);
pop('#lb1',2.2); ['#o1','#o2','#o3','#o4'].forEach((s,i)=>pop(s,2.5+i*.35)); out(['#lb1','#o1','#o2','#o3','#o4'],4.65);
pop('#lb2',4.8); ['#v1','#v2','#v3'].forEach((s,i)=>{pop(s,5.1+i*.6);tl.fromTo(s,{x:0},{x:10,duration:.05,yoyo:true,repeat:3,immediateRender:false},5.5+i*.6)});
out(['#lb2','#v1','#v2','#v3'],8.05);
pop('#lb3',8.2); ['#p1','#p2','#p3'].forEach((s,i)=>pop(s,8.5+i*.45)); stk('#sk2',10.0,6); out(['#lb3','#p1','#p2','#p3','#sk2'],11.05);
tl.fromTo('#en',{opacity:0},{opacity:1,duration:.2},11.2);
xMorph(tl,'#lgN',11.3);
pop('#bt',12.2);
tl.to('#bt',{x:10,y:10,boxShadow:'2px 2px 0 #FFE14D',duration:.12,yoyo:true,repeat:1},13.4);
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
