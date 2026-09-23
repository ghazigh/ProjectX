"""Builds the five XForward ad concept drafts as HyperFrames projects.

Each concept is authored at full design size inside a `.stage` that is scaled
with CSS `zoom`, so the same file renders low-res drafts now (ZOOM < 1) and
full-resolution finals later (ZOOM = 1).
"""
import os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = open(os.path.join(HERE, "fonts", "fonts.css")).read().replace("../fonts/", "fonts/")
DRAFT = "--final" not in sys.argv

XLOGO = '<svg class="xl" viewBox="0 0 24 24" aria-hidden="true"><path class="m1" d="M5 5l7 7-7 7"/><path class="m2" d="M12 5l7 7-7 7"/></svg>'

BASE_CSS = """
html,body{margin:0;background:#000}
#root{position:relative;width:100%;height:100%;overflow:hidden}
.stage{position:absolute;left:0;top:0;overflow:hidden}
.clip{position:absolute;inset:0}
.xl{display:block;overflow:visible}
.xl path{fill:none;stroke-width:2.3;stroke-linecap:round;stroke-linejoin:round}
.mono{font-family:'IBM Plex Mono',monospace}
"""

# helper JS shared by every concept: the brand mark morph (two arrows -> X)
HELPERS = """
function xMorph(tl, sel, t){
  const m1 = document.querySelector(sel + ' .m1'), m2 = document.querySelector(sel + ' .m2');
  tl.fromTo(sel, {opacity:0, scale:.6}, {opacity:1, scale:1, duration:.6, ease:'back.out(1.6)'}, t);
  tl.fromTo(m1, {x:-6}, {x:0, duration:.6, ease:'power3.out'}, t);
  tl.fromTo(m2, {x:6, scaleX:1}, {x:0, duration:.6, ease:'power3.out'}, t);
  tl.to(m2, {scaleX:-1, transformOrigin:'50% 50%', duration:.9, ease:'power3.inOut'}, t + .7);
}
"""


def page(cid, design_w, design_h, zoom, duration, css, body, js):
    w, h = round(design_w * zoom), round(design_h * zoom)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width={w}, height={h}">
<title>XForward ad · {cid}</title>
<script src="gsap.min.js"></script>
<style>
{FONTS}
{BASE_CSS}
.stage{{width:{design_w}px;height:{design_h}px;zoom:{zoom}}}
{css}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-width="{w}" data-height="{h}" data-duration="{duration}">
<div class="stage">
{body}
</div>
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


CONCEPTS = {}

# ---------------------------------------------------------------- A · 9:42 PM (9:16)
CONCEPTS["a-942pm"] = dict(w=1080, h=1920, zoom=1/3, dur=15, css="""
.stage{background:#0A0B0D;color:#ECEEF2;font-family:'Archivo',sans-serif}
.center{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;padding:0 90px}
.clock{margin-top:250px;position:relative;height:250px;width:100%}
.clock div{position:absolute;inset:0;text-align:center;white-space:nowrap;font-weight:300;font-stretch:100%;font-size:190px;letter-spacing:-7px;line-height:250px;font-variant-numeric:tabular-nums}
.day{font:500 34px 'IBM Plex Mono',monospace;letter-spacing:6px;text-transform:uppercase;color:#868D98;margin-top:10px}
.notif{margin-top:120px;width:100%;box-sizing:border-box;padding:34px 38px;border-radius:44px;background:rgba(236,238,242,.1);display:flex;gap:28px}
.notif .ic{flex:none;width:84px;height:84px;border-radius:22px;background:#2E343C;display:grid;place-items:center;font-size:44px}
.notif b{display:block;font-size:34px;margin-bottom:6px}
.notif small{font:500 26px 'IBM Plex Mono',monospace;color:#868D98}
.notif p{margin:10px 0 0;font-size:40px;line-height:1.3}
.strike{position:absolute;left:60px;right:60px;height:8px;background:#FF5A4E;top:50%;transform-origin:left center}
.cap{position:absolute;left:90px;right:90px;bottom:260px;font-weight:650;font-stretch:112%;font-size:76px;line-height:1.05;letter-spacing:-2px}
.cap span{color:#868D98}
.cap.red span{color:#FF5A4E}
.rew{opacity:0;position:absolute;inset:0;display:grid;place-items:center;font-weight:800;font-stretch:125%;font-size:170px;letter-spacing:-6px;color:#0A0B0D;background:#8C96FF}
.thread{position:absolute;left:70px;right:70px;top:430px;display:flex;flex-direction:column;gap:26px}
.bub{max-width:80%;padding:30px 36px;border-radius:40px;font-size:42px;line-height:1.3}
.bub small{display:block;font:500 24px 'IBM Plex Mono',monospace;opacity:.6;margin-bottom:8px}
.in{align-self:flex-start;background:rgba(236,238,242,.12);border-bottom-left-radius:12px}
.out{align-self:flex-end;background:#8C96FF;color:#0A0B0D;border-bottom-right-radius:12px}
.typing{align-self:flex-end;display:flex;gap:12px;padding:30px 36px;border-radius:40px;background:rgba(140,150,255,.25)}
.typing i{width:18px;height:18px;border-radius:50%;background:#8C96FF;display:block}
.booked{border:3px solid #8C96FF;border-radius:34px;padding:30px 36px;font-size:44px;font-weight:650}
.booked small{display:block;font:500 28px 'IBM Plex Mono',monospace;color:#868D98;margin-top:8px;font-weight:500}
.stat{align-self:center;margin-top:30px;font:600 34px 'IBM Plex Mono',monospace;letter-spacing:2px;color:#8C96FF;text-transform:uppercase;text-align:center}
.top{position:absolute;left:0;right:0;top:170px;text-align:center;font-weight:300;font-stretch:112%;font-size:110px;letter-spacing:-4px}
.end{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:40px;text-align:center;padding:0 110px}
.end .xl{width:230px;height:230px}
.end .xl .m1{stroke:#ECEEF2}.end .xl .m2{stroke:#8C96FF}
.wm{font-weight:750;font-stretch:118%;font-size:110px;letter-spacing:-4px}
.wm b{color:#8C96FF}
.tag{font-size:48px;line-height:1.25;color:#C3C8D0;max-width:18ch}
.cta{margin-top:30px;padding:30px 54px;border-radius:999px;background:#8C96FF;color:#0A0B0D;font-weight:700;font-size:42px}
""", body=f"""
<section id="a1" class="clip" data-start="0" data-duration="5.6"><div class="center">
  <div class="clock"><div id="c0">9:42 PM</div><div id="c1">11:58 PM</div><div id="c2">2:13 AM</div><div id="c3">8:17 AM</div></div>
  <div class="day" id="day">Tuesday night</div>
  <div class="notif" id="notif" style="position:relative"><span class="ic">💬</span><span><b>(514) 555-0142</b><small id="unread">NEW MESSAGE</small><p>Water is leaking everywhere. Can someone come tonight?</p></span><i class="strike" id="strike"></i></div>
</div>
<p class="cap" id="capA">A customer needs you. <span>Right now.</span></p>
<p class="cap red" id="capB">Nobody answered. <span>They booked someone else.</span></p>
</section>
<section id="a2" class="clip" data-start="5.6" data-duration="0.9"><div class="rew" id="rew">Rewind.</div></section>
<section id="a3" class="clip" data-start="6.5" data-duration="5.1">
  <div class="top" id="top">9:42 PM</div>
  <div class="thread">
    <p class="bub in" id="b1"><small>NEW LEAD · 9:42 PM</small>Water is leaking everywhere. Can someone come tonight?</p>
    <div class="typing" id="typ"><i></i><i></i><i></i></div>
    <p class="bub out" id="b2"><small>AI AGENT · 9:42:38 PM</small>Sorry! Shut the main valve. A plumber can be there at 7:30 AM or 9:00. Which works?</p>
    <p class="bub in" id="b3">7:30 please 🙏</p>
    <div class="booked" id="bk">✓ Booked · Tomorrow 7:30 AM<small>Marc, plumber · SMS confirmation sent</small></div>
    <p class="stat" id="st">Answered in 38 seconds. While you slept.</p>
  </div>
</section>
<section id="a4" class="clip" data-start="11.6" data-duration="3.4"><div class="end">
  <div id="lgA">{XLOGO}</div>
  <div class="wm" id="wmA"><b>X</b>Forward</div>
  <p class="tag" id="tgA">AI agents that answer, book and follow up. Built into your business.</p>
  <div class="cta" id="ctA">Book a free call · xforward.ca</div>
</div></section>
""", js="""
tl.fromTo('#c0',{opacity:0,y:40},{opacity:1,y:0,duration:.6,ease:'power3.out'},.1);
tl.fromTo('#day',{opacity:0},{opacity:1,duration:.5},.4);
tl.fromTo('#notif',{opacity:0,y:-80,scale:.96},{opacity:1,y:0,scale:1,duration:.7,ease:'back.out(1.4)'},.8);
tl.fromTo('#capA',{opacity:0,y:30},{opacity:1,y:0,duration:.5,ease:'power3.out'},1.5);
tl.to('#capA',{opacity:0,y:-20,duration:.3},2.9);
const clocks=['#c0','#c1','#c2','#c3'];
for(let i=1;i<4;i++){const t=2.8+i*.42;
  tl.to(clocks[i-1],{opacity:0,y:-90,duration:.25,ease:'power2.in'},t);
  tl.fromTo(clocks[i],{opacity:0,y:90},{opacity:1,y:0,duration:.3,ease:'power2.out'},t+.12);}
tl.to('#day',{opacity:0,duration:.2},3.2);
tl.to('#notif',{opacity:.45,duration:.6},3.4);
tl.fromTo('#strike',{scaleX:0},{scaleX:1,duration:.45,ease:'power2.inOut'},4.25);
tl.fromTo('#capB',{opacity:0,y:30},{opacity:1,y:0,duration:.5,ease:'power3.out'},4.3);
tl.fromTo('#rew',{opacity:0,scale:1.3},{opacity:1,scale:1,duration:.35,ease:'power3.out'},5.6);
tl.to('#rew',{scale:.85,opacity:0,duration:.3,ease:'power2.in'},6.2);
tl.fromTo('#top',{opacity:0,y:-30},{opacity:1,y:0,duration:.5},6.5);
tl.fromTo('#b1',{opacity:0,y:40},{opacity:1,y:0,duration:.5,ease:'power3.out'},6.8);
tl.fromTo('#typ',{opacity:0,y:20},{opacity:1,y:0,duration:.3},7.4);
tl.fromTo('#typ i',{y:0},{y:-12,duration:.25,stagger:.1,yoyo:true,repeat:3,ease:'sine.inOut'},7.5);
tl.to('#typ',{opacity:0,duration:.15},8.3);
tl.fromTo('#b2',{opacity:0,y:40,scale:.96},{opacity:1,y:0,scale:1,duration:.5,ease:'back.out(1.5)'},8.35);
tl.fromTo('#b3',{opacity:0,y:40},{opacity:1,y:0,duration:.45,ease:'power3.out'},9.3);
tl.fromTo('#bk',{opacity:0,y:40,scale:.95},{opacity:1,y:0,scale:1,duration:.55,ease:'back.out(1.6)'},9.9);
tl.fromTo('#st',{opacity:0},{opacity:1,duration:.5},10.6);
xMorph(tl,'#lgA',11.7);
tl.fromTo('#wmA',{opacity:0,y:30},{opacity:1,y:0,duration:.5,ease:'power3.out'},12.1);
tl.fromTo('#tgA',{opacity:0,y:20},{opacity:1,y:0,duration:.5},12.5);
tl.fromTo('#ctA',{opacity:0,scale:.9},{opacity:1,scale:1,duration:.5,ease:'back.out(1.7)'},13.0);
""")

# ---------------------------------------------------------------- B · Hours (1:1)
CONCEPTS["b-hours"] = dict(w=1080, h=1080, zoom=4/9, dur=13, css="""
.stage{background:#0A0B0D;color:#F1F2EE;font-family:'Archivo',sans-serif}
.full{position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;padding:0 90px}
.w{display:block;font-weight:800;font-stretch:125%;font-size:150px;line-height:.92;letter-spacing:-7px}
.w.sm{font-size:70px;letter-spacing:-2px;font-weight:600;color:#868D98;margin-bottom:12px}
.big{font-weight:800;font-stretch:125%;font-size:430px;line-height:.8;letter-spacing:-24px;color:#8C96FF;font-variant-numeric:tabular-nums}
.task{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;text-align:center;padding:0 70px}
.task span{position:relative;display:block;font-weight:800;font-stretch:118%;font-size:118px;line-height:.95;letter-spacing:-5px}
.task i{position:absolute;left:-10px;right:-10px;top:52%;height:14px;background:#FF5A4E;transform-origin:left center;display:block}
.blue{position:absolute;inset:0;background:#2334E0}
.give{position:absolute;inset:0;display:flex;align-items:center;padding:0 90px;font-weight:800;font-stretch:125%;font-size:150px;line-height:.9;letter-spacing:-7px;color:#fff}
.end{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:34px;text-align:center}
.end .xl{width:190px;height:190px}.end .xl .m1{stroke:#F1F2EE}.end .xl .m2{stroke:#8C96FF}
.wm{font-weight:750;font-stretch:118%;font-size:100px;letter-spacing:-4px}.wm b{color:#8C96FF}
.tag{font:500 34px 'IBM Plex Mono',monospace;letter-spacing:4px;text-transform:uppercase;color:#868D98}
""", body=f"""
<section id="b1" class="clip" data-start="0" data-duration="3.4"><div class="full">
  <span class="w sm" id="w1">Your team spends</span>
  <span class="big" id="n1">0</span>
  <span class="w" id="w2">hours a week</span>
  <span class="w" id="w3" style="color:#868D98">copy-pasting.</span>
</div></section>
<section id="b2" class="clip" data-start="3.4" data-duration="3">
  <div class="task" id="t1"><span>Re-typing orders<i></i></span></div>
  <div class="task" id="t2"><span>Chasing documents<i></i></span></div>
  <div class="task" id="t3"><span>The same email, again<i></i></span></div>
  <div class="task" id="t4"><span>Booking every call<i></i></span></div>
</section>
<section id="b3" class="clip" data-start="6.4" data-duration="2.6"><div class="full">
  <span class="w sm" id="w4">That's</span>
  <span class="big" id="n2">0</span>
  <span class="w" id="w5">hours a year.</span>
</div></section>
<section id="b4" class="clip" data-start="9" data-duration="1.9">
  <div class="blue" id="bl"></div>
  <div class="give" id="gv">Give them to an agent.</div>
</section>
<section id="b5" class="clip" data-start="10.9" data-duration="2.1"><div class="end">
  <div id="lgB">{XLOGO}</div>
  <div class="wm" id="wmB"><b>X</b>Forward</div>
  <div class="tag" id="tgB">AI agents for small businesses</div>
</div></section>
""", js="""
const stomp=(s,t)=>tl.fromTo(s,{opacity:0,scale:1.35},{opacity:1,scale:1,duration:.28,ease:'power4.out'},t);
stomp('#w1',.15);
const c1={v:0};tl.fromTo('#n1',{opacity:0,y:60},{opacity:1,y:0,duration:.3,ease:'power3.out'},.5);
tl.to(c1,{v:11,duration:1.1,ease:'power2.out',onUpdate:()=>{document.querySelector('#n1').textContent=Math.round(c1.v)}},.55);
stomp('#w2',1.2); stomp('#w3',2.1);
['#t1','#t2','#t3','#t4'].forEach((s,i)=>{const t=3.4+i*.62;
  tl.fromTo(s+' span',{opacity:0,scale:1.5},{opacity:1,scale:1,duration:.22,ease:'power4.out'},t);
  tl.fromTo(s+' i',{scaleX:0},{scaleX:1,duration:.22,ease:'power2.out'},t+.3);
  if(i<3) tl.to(s+' span',{opacity:0,duration:.08},t+.6);});
stomp('#w4',6.5);
const c2={v:0};tl.fromTo('#n2',{opacity:0},{opacity:1,duration:.2},6.8);
tl.to(c2,{v:506,duration:1.2,ease:'power3.out',onUpdate:()=>{document.querySelector('#n2').textContent=Math.round(c2.v)}},6.8);
stomp('#w5',7.9);
tl.fromTo('#bl',{yPercent:100},{yPercent:0,duration:.45,ease:'power4.inOut'},9);
tl.fromTo('#gv',{opacity:0,y:60},{opacity:1,y:0,duration:.45,ease:'power3.out'},9.3);
xMorph(tl,'#lgB',11);
tl.fromTo('#wmB',{opacity:0,y:30},{opacity:1,y:0,duration:.45,ease:'power3.out'},11.4);
tl.fromTo('#tgB',{opacity:0},{opacity:1,duration:.5},11.9);
""")

# ---------------------------------------------------------------- C · Terrain (16:9)
CONCEPTS["c-terrain"] = dict(w=1920, h=1080, zoom=1/3, dur=15, css="""
.stage{background:#0A0B0D;color:#ECEEF2;font-family:'Archivo',sans-serif}
#cv{position:absolute;left:0;top:0;width:1920px;height:1080px}
.veil{position:absolute;inset:0;background:linear-gradient(90deg,rgba(10,11,13,.92) 0%,rgba(10,11,13,.55) 36%,rgba(10,11,13,0) 62%)}
.line{position:absolute;left:140px;bottom:170px;max-width:900px;font-weight:650;font-stretch:112%;font-size:96px;line-height:1;letter-spacing:-4px}
.line b{display:block;font:500 26px 'IBM Plex Mono',monospace;letter-spacing:6px;text-transform:uppercase;color:#8C96FF;margin-bottom:26px;font-weight:500}
.line span{color:#868D98}
.pin{position:absolute;left:0;top:0;width:0;height:0}
.pin i{position:absolute;left:-12px;top:-12px;width:24px;height:24px;border-radius:50%;background:#8C96FF;box-shadow:0 0 0 7px #0A0B0D}
.pin .lb{position:absolute;left:0;bottom:36px;white-space:nowrap;padding:18px 24px;border-radius:20px;background:#16191E;border:2px solid #2E343C;font-size:30px;transform:translateX(-50%)}
.pin .lb b{display:block;font:600 20px 'IBM Plex Mono',monospace;letter-spacing:3px;color:#8C96FF;margin-bottom:6px}
.hud{position:absolute;left:140px;top:90px;font:500 22px 'IBM Plex Mono',monospace;letter-spacing:4px;color:#868D98;text-transform:uppercase}
.endv{position:absolute;inset:0;background:#0A0B0D}
.end{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:34px;text-align:center}
.end .xl{width:180px;height:180px}.end .xl .m1{stroke:#ECEEF2}.end .xl .m2{stroke:#8C96FF}
.wm{font-weight:750;font-stretch:118%;font-size:110px;letter-spacing:-4px}.wm b{color:#8C96FF}
.tag{font-size:40px;color:#C3C8D0}
""", body=f"""
<canvas id="cv"></canvas>
<div class="veil"></div>
<div class="hud" id="hud">Contours = hours lost per week</div>
<div class="pin" id="pin"><i></i><div class="lb" id="plb"><b>BOTTLENECK · DAY 4</b>Quotes typed by hand · 4 h/day</div></div>
<p class="line" id="l1"><b>Your business</b>Every business has a hidden mountain.</p>
<p class="line" id="l2"><b>Day 4</b>Hours lost to work <span>a machine could do.</span></p>
<p class="line" id="l3"><b>Weeks 2–6</b>We send an engineer to flatten it.</p>
<p class="line" id="l4"><b>Day 30</b>80 hours back. <span>Every month.</span></p>
<section id="c5" class="clip" data-start="12" data-duration="3">
  <div class="endv" id="ev"></div>
  <div class="end">
    <div id="lgC">{XLOGO}</div>
    <div class="wm" id="wmC"><b>X</b>Forward</div>
    <p class="tag" id="tgC">AI agents, built into your business.</p>
  </div>
</section>
""", js="""
const ZOOM = parseFloat(getComputedStyle(document.querySelector('.stage')).zoom) || 1;
const W=1920,H=1080, cv=document.getElementById('cv'), ctx=cv.getContext('2d');
cv.width=Math.round(W*ZOOM); cv.height=Math.round(H*ZOOM);
const perm=new Uint8Array(512);(()=>{let s=20260923;const r=()=>(s=(s*16807)%2147483647)/2147483647;const b=[...Array(256).keys()];for(let i=255;i>0;i--){const j=Math.floor(r()*(i+1));[b[i],b[j]]=[b[j],b[i]]}for(let i=0;i<512;i++)perm[i]=b[i&255]})();
const fade=t=>t*t*t*(t*(t*6-15)+10), grad=(h,x,y)=>{switch(h&7){case 0:return x+y;case 1:return -x+y;case 2:return x-y;case 3:return -x-y;case 4:return x;case 5:return -x;case 6:return y;default:return -y}};
function noise(x,y){const fx=Math.floor(x),fy=Math.floor(y),X=fx&255,Y=fy&255;x-=fx;y-=fy;const u=fade(x),v=fade(y),a=perm[X]+Y,b=perm[X+1]+Y;const l1=grad(perm[a],x,y)+u*(grad(perm[b],x-1,y)-grad(perm[a],x,y));const l2=grad(perm[a+1],x,y-1)+u*(grad(perm[b+1],x-1,y-1)-grad(perm[a+1],x,y-1));return l1+v*(l2-l1)}
const S={t:0,rise:0,col:0,draw:0}, PX=W*.68, PY=H*.52, R2=Math.pow(H*.16,2), cell=12, cols=Math.ceil(W/cell), rows=Math.ceil(H/cell), vals=new Float32Array((cols+1)*(rows+1));
const field=(x,y)=>{const nx=x/460,ny=y/460;let v=noise(nx+S.t*.03,ny-S.t*.02)*.85+noise(nx*1.8-S.t*.04+20,ny*1.8+7)*.3;const dx=x-PX,dy=y-PY;return v+1.25*(1-.9*S.col)*Math.exp(-(dx*dx+dy*dy)/R2)};
function proj(x,y,L,o){const r=S.rise;if(r<1e-3){o[0]=x;o[1]=y;return}const th=r*56*Math.PI/180,ph=(-r*12-S.col*10)*Math.PI/180,k=1+.3*r,hs=r*H*.17,F=W*1.15;
 const x0=(x-W/2)*k,y0=(y-H*.56)*k,z=(L+1.1)*hs,xr=x0*Math.cos(ph)-y0*Math.sin(ph),yr=x0*Math.sin(ph)+y0*Math.cos(ph);
 const ys=yr*Math.cos(th)-z*Math.sin(th),zc=z*Math.cos(th)+yr*Math.sin(th),sc=F/Math.max(F*.2,F-zc);o[0]=W/2+xr*sc;o[1]=H*.56+r*H*.05+ys*sc}
function draw(){
 const C=cols+1,s=cell,step=.1,lo=-3,E=2*C*(rows+1);
 for(let j=0;j<=rows;j++)for(let i=0;i<=cols;i++)vals[j*C+i]=field(i*s,j*s);
 const pts=new Map(),adj=new Map(),link=(a,b)=>{(adj.get(a)||adj.set(a,[]).get(a)).push(b);(adj.get(b)||adj.set(b,[]).get(b)).push(a)};
 for(let j=0;j<rows;j++)for(let i=0;i<cols;i++){const a=vals[j*C+i],b=vals[j*C+i+1],c=vals[(j+1)*C+i+1],d=vals[(j+1)*C+i],mn=Math.min(a,b,c,d),mx=Math.max(a,b,c,d);
  for(let k=Math.ceil((mn-lo)/step);k<=Math.floor((mx-lo)/step);k++){const L=lo+k*step,code=(a>L?8:0)|(b>L?4:0)|(c>L?2:0)|(d>L?1:0);if(!code||code===15)continue;
   const base=k*E,x0=i*s,y0=j*s,T=base+2*(j*C+i),B=base+2*((j+1)*C+i),Lk=T+1,R=base+2*(j*C+i+1)+1;
   if(!pts.has(T))pts.set(T,[x0+s*(L-a)/(b-a),y0]);if(!pts.has(B))pts.set(B,[x0+s*(L-d)/(c-d),y0+s]);if(!pts.has(Lk))pts.set(Lk,[x0,y0+s*(L-a)/(d-a)]);if(!pts.has(R))pts.set(R,[x0+s,y0+s*(L-b)/(c-b)]);
   switch(code){case 1:case 14:link(Lk,B);break;case 2:case 13:link(B,R);break;case 3:case 12:link(Lk,R);break;case 4:case 11:link(T,R);break;case 5:link(T,Lk);link(B,R);break;case 6:case 9:link(T,B);break;case 7:case 8:link(T,Lk);break;case 10:link(T,R);link(Lk,B);break}}}
 const thin=new Path2D(),idx=new Path2D(),hot=new Path2D(),seen=new Set(),o=[0,0];
 const trace=st=>{const line=[st];seen.add(st);let pv=-1,cu=st,closed=false;for(;;){const nb=adj.get(cu);let nx=-1;for(const m of nb)if(m!==pv&&!seen.has(m)){nx=m;break}if(nx<0){closed=line.length>2&&nb.includes(st);break}line.push(nx);seen.add(nx);pv=cu;cu=nx}
  const n=line.length;if(n<2)return;const k=Math.floor(st/E),L=lo+k*step,p=L>=1.02?hot:(k%5===0?idx:thin),q=[];for(const key of line){const pt=pts.get(key);proj(pt[0],pt[1],L,o);q.push(o[0],o[1])}
  if(closed){p.moveTo((q[2*n-2]+q[0])/2,(q[2*n-1]+q[1])/2);for(let m=0;m<n;m++){const m2=(m+1)%n;p.quadraticCurveTo(q[2*m],q[2*m+1],(q[2*m]+q[2*m2])/2,(q[2*m+1]+q[2*m2+1])/2)}}
  else{p.moveTo(q[0],q[1]);for(let m=1;m<n-1;m++)p.quadraticCurveTo(q[2*m],q[2*m+1],(q[2*m]+q[2*m+2])/2,(q[2*m+1]+q[2*m+3])/2);p.lineTo(q[2*n-2],q[2*n-1])}};
 for(const [key,nb] of adj)if(nb.length===1&&!seen.has(key))trace(key);for(const key of adj.keys())if(!seen.has(key))trace(key);
 ctx.setTransform(ZOOM,0,0,ZOOM,0,0);ctx.clearRect(0,0,W,H);ctx.lineCap='round';ctx.lineJoin='round';ctx.globalAlpha=S.draw;
 ctx.strokeStyle='rgba(236,238,242,.22)';ctx.lineWidth=1.6;ctx.stroke(thin);ctx.strokeStyle='rgba(236,238,242,.46)';ctx.lineWidth=2.2;ctx.stroke(idx);ctx.strokeStyle='#8C96FF';ctx.lineWidth=2.6;ctx.stroke(hot);ctx.globalAlpha=1;
 proj(PX,PY,field(PX,PY),o);document.getElementById('pin').style.transform=`translate(${o[0]}px,${o[1]}px)`;
}
tl.to(S,{t:15,duration:15,ease:'none',onUpdate:draw},0);
tl.fromTo(S,{draw:0},{draw:1,duration:1.4,ease:'power2.out',immediateRender:false},0);
tl.fromTo(S,{rise:0},{rise:1,duration:2.6,ease:'power2.inOut',immediateRender:false},2.6);
tl.fromTo(S,{col:0},{col:1,duration:2.2,ease:'power2.inOut',immediateRender:false},7.6);
tl.fromTo('#hud',{opacity:0},{opacity:1,duration:.6},.6);
const line=(s,a,b)=>{tl.fromTo(s,{opacity:0,y:40},{opacity:1,y:0,duration:.6,ease:'power3.out'},a);tl.to(s,{opacity:0,y:-30,duration:.4,ease:'power2.in'},b)};
line('#l1',.5,2.4); line('#l2',3.2,6.6); line('#l3',7,9.4); line('#l4',9.9,11.9);
tl.fromTo('#pin i',{scale:0},{scale:1,duration:.4,ease:'back.out(2)'},4.4);
tl.fromTo('#plb',{opacity:0},{opacity:1,duration:.4},4.6);
tl.to('#plb',{opacity:0,duration:.3},8.4);
tl.fromTo('#ev',{opacity:0},{opacity:1,duration:.6},12);
xMorph(tl,'#lgC',12.4);
tl.fromTo('#wmC',{opacity:0,y:30},{opacity:1,y:0,duration:.5,ease:'power3.out'},12.8);
tl.fromTo('#tgC',{opacity:0},{opacity:1,duration:.5},13.2);
draw();
""")

# ---------------------------------------------------------------- D · Help Wanted (9:16)
CONCEPTS["d-help-wanted"] = dict(w=1080, h=1920, zoom=1/3, dur=14, css="""
.stage{background:#2A2622}
.paper{position:absolute;inset:0;background:#EFE9DC;color:#1E1B17;font-family:'Instrument Serif',serif;
  background-image:repeating-linear-gradient(0deg,rgba(0,0,0,.018) 0 2px,transparent 2px 5px),radial-gradient(circle at 30% 20%,rgba(255,255,255,.5),transparent 60%)}
.mast{position:absolute;left:70px;right:70px;top:80px;text-align:center;border-bottom:6px double #1E1B17;padding-bottom:22px}
.mast h1{margin:0;font-weight:400;font-size:150px;letter-spacing:-2px;line-height:1}
.mast p{margin:14px 0 0;font:400 30px 'Special Elite',monospace;letter-spacing:3px;display:flex;justify-content:space-between}
.cols{position:absolute;left:70px;right:70px;top:380px;bottom:120px;display:grid;grid-template-columns:1fr 1fr 1fr;gap:34px}
.col i{display:block;height:16px;background:rgba(30,27,23,.16);margin-bottom:18px;border-radius:2px}
.col b{display:block;font:400 34px 'Special Elite',monospace;margin:30px 0 18px;opacity:.55}
.ad{position:absolute;left:150px;right:150px;top:560px;padding:50px 54px;border:5px solid #1E1B17;background:#F4EFE3}
.ad h2{margin:0 0 24px;font-weight:400;font-size:120px;line-height:.95;text-align:center;letter-spacing:-2px}
.ad .ln{display:block;font:400 42px/1.35 'Special Elite',monospace;margin:0 0 16px;overflow:hidden;white-space:nowrap}
.ad .ln span{display:inline-block}
.pen{position:absolute;left:90px;top:500px;width:900px;height:1080px;overflow:visible}
.pen ellipse{fill:none;stroke:#C8261C;stroke-width:9;stroke-linecap:round}
.note{position:absolute;left:520px;top:1620px;font-style:italic;font-size:84px;color:#C8261C;white-space:nowrap}
.stamp{position:absolute;left:120px;right:120px;top:1030px;text-align:center;padding:30px 20px;border:12px solid #2334E0;color:#2334E0;font:400 96px/1 'Special Elite',monospace;letter-spacing:2px;background:rgba(239,233,220,.55)}
.end{position:absolute;inset:0;background:#EFE9DC;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:40px;text-align:center;padding:0 110px;color:#1E1B17}
.end .xl{width:210px;height:210px}.end .xl .m1{stroke:#1E1B17}.end .xl .m2{stroke:#2334E0}
.wm{font:750 110px 'Archivo',sans-serif;font-stretch:118%;letter-spacing:-4px}.wm b{color:#2334E0}
.tag{font-size:66px;line-height:1.1;font-style:italic}
.url{font:400 44px 'Special Elite',monospace}
""", body=f"""
<div class="paper" id="paper">
  <div class="mast"><h1>The Daily Ledger</h1><p><span>Classifieds</span><span>Tuesday</span><span>50¢</span></p></div>
  <div class="cols">
    <div class="col"><b>FOR SALE</b><i></i><i style="width:80%"></i><i></i><i style="width:60%"></i><b>RENTALS</b><i></i><i style="width:70%"></i></div>
    <div class="col"><b>SERVICES</b><i></i><i></i><i style="width:75%"></i></div>
    <div class="col"><b>AUTOS</b><i></i><i style="width:85%"></i><i></i><i style="width:50%"></i></div>
  </div>
  <div class="ad" id="ad">
    <h2 id="hw">Help Wanted</h2>
    <p class="ln"><span id="d1">Front desk, local business.</span></p>
    <p class="ln"><span id="d2">Answers every customer</span></p>
    <p class="ln"><span id="d3">in under 60 seconds.</span></p>
    <p class="ln"><span id="d4">Nights, weekends, holidays.</span></p>
    <p class="ln"><span id="d5">Never mistypes an order.</span></p>
    <p class="ln"><span id="d6">Never forgets a follow-up.</span></p>
    <p class="ln"><span id="d7">Starts in 6 weeks.</span></p>
  </div>
  <svg class="pen" viewBox="0 0 900 1080"><ellipse id="circ" cx="450" cy="470" rx="420" ry="520" transform="rotate(-3 450 470)"/></svg>
  <p class="note" id="note">a person?!</p>
  <div class="stamp" id="stamp">IT'S AN AI AGENT.</div>
</div>
<section id="d9" class="clip" data-start="11.4" data-duration="2.6"><div class="end">
  <div id="lgD">{XLOGO}</div>
  <div class="wm" id="wmD"><b>X</b>Forward</div>
  <p class="tag" id="tgD">We build it into your business.</p>
  <p class="url" id="urD">xforward.ca</p>
</div></section>
""", js="""
tl.fromTo('#paper',{scale:1.12,y:120},{scale:1,y:0,duration:1.6,ease:'power3.out'},0);
tl.to('#paper',{scale:1.06,duration:9,ease:'none'},1.6);
tl.fromTo('#hw',{opacity:0,scale:1.4},{opacity:1,scale:1,duration:.4,ease:'power4.out'},.9);
['#d1','#d2','#d3','#d4','#d5','#d6','#d7'].forEach((s,i)=>{
  tl.fromTo(s,{clipPath:'inset(0 100% 0 0)'},{clipPath:'inset(0 0% 0 0)',duration:.6,ease:'steps(22)'},1.5+i*.72);});
const circ=document.getElementById('circ'), len=circ.getTotalLength();
tl.fromTo(circ,{strokeDasharray:len,strokeDashoffset:len},{strokeDashoffset:0,duration:.9,ease:'power2.inOut'},6.9);
tl.fromTo('#note',{opacity:0,x:-30,rotation:-8},{opacity:1,x:0,rotation:-6,duration:.4,ease:'power2.out'},7.8);
tl.fromTo('#stamp',{opacity:0,scale:2.4,rotation:-18},{opacity:1,scale:1,rotation:-8,duration:.32,ease:'power4.in'},9.1);
tl.fromTo('#paper',{x:0},{x:10,duration:.05,yoyo:true,repeat:3,immediateRender:false},9.42);
xMorph(tl,'#lgD',11.5);
tl.fromTo('#wmD',{opacity:0,y:30},{opacity:1,y:0,duration:.5,ease:'power3.out'},11.9);
tl.fromTo('#tgD',{opacity:0},{opacity:1,duration:.5},12.3);
tl.fromTo('#urD',{opacity:0},{opacity:1,duration:.5},12.7);
""")

# ---------------------------------------------------------------- E · The Receipt (1:1)
CONCEPTS["e-receipt"] = dict(w=1080, h=1080, zoom=4/9, dur=13, css="""
.stage{background:#0A0B0D;font-family:'IBM Plex Mono',monospace}
.slot{position:absolute;left:220px;right:220px;top:40px;height:26px;border-radius:13px;background:#1F2329;z-index:3}
.rcpt{position:absolute;left:250px;width:580px;top:60px;background:#FAF8F3;color:#1B1B1B;padding:46px 40px 60px;
  -webkit-mask:linear-gradient(#000,#000) top/100% calc(100% - 16px) no-repeat,conic-gradient(from -45deg at bottom,#0000,#000 1deg 89deg,#0000 90deg) bottom/24px 16px repeat-x;
  box-shadow:0 30px 60px -20px rgba(0,0,0,.7)}
.rcpt .c{text-align:center}
.rcpt h3{margin:0;font-size:40px;font-weight:600;letter-spacing:4px}
.rcpt .s{font-size:22px;color:#555;margin:8px 0 0}
.rcpt hr{border:0;border-top:3px dashed #999;margin:26px 0}
.row{display:flex;gap:10px;font-size:25px;line-height:1.3;margin:0 0 16px}
.row .d{flex:1;border-bottom:3px dotted #aaa;transform:translateY(-8px)}
.row.tot{font-weight:600;font-size:30px}
.row.big{font-weight:600;font-size:40px;margin-top:10px}
.bar{height:90px;margin:34px 10px 10px;background:repeating-linear-gradient(90deg,#1B1B1B 0 4px,transparent 4px 7px,#1B1B1B 7px 13px,transparent 13px 16px,#1B1B1B 16px 18px,transparent 18px 23px)}
.stamp{position:absolute;left:170px;right:170px;top:470px;text-align:center;padding:26px 10px;border:12px solid #2334E0;color:#2334E0;font:600 70px/1 'IBM Plex Mono',monospace;letter-spacing:2px;z-index:4;background:rgba(250,248,243,.5)}
.end{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:34px;text-align:center;color:#ECEEF2}
.end .xl{width:190px;height:190px}.end .xl .m1{stroke:#ECEEF2}.end .xl .m2{stroke:#8C96FF}
.wm{font:750 100px 'Archivo',sans-serif;font-stretch:118%;letter-spacing:-4px}.wm b{color:#8C96FF}
.tag{font:650 60px 'Archivo',sans-serif;font-stretch:110%;letter-spacing:-2px}
.url{font-size:34px;color:#868D98}
""", body=f"""
<section id="e1" class="clip" data-start="0" data-duration="10.4">
<div class="rcpt" id="rc">
  <div class="c rl"><h3>YOUR BUSINESS</h3><p class="s">WEEK 37 · TIME SPENT ON REPETITIVE WORK</p></div>
  <hr class="rl">
  <p class="row rl">Re-typing orders<span class="d"></span>6.0 h</p>
  <p class="row rl">Chasing documents<span class="d"></span>4.5 h</p>
  <p class="row rl">Same email, again<span class="d"></span>3.0 h</p>
  <p class="row rl">Rebooking calls<span class="d"></span>2.5 h</p>
  <p class="row rl">Missed night leads<span class="d"></span>7</p>
  <hr class="rl">
  <p class="row tot rl">TOTAL<span class="d"></span>16.0 h</p>
  <p class="row rl">× $45/h<span class="d"></span>$720</p>
  <p class="row big rl">PER YEAR<span class="d"></span>$37,440</p>
  <div class="bar rl"></div>
  <p class="c s rl">THANK YOU FOR YOUR TIME</p>
</div>
<div class="slot"></div>
<div class="stamp" id="stE">RECOVERED BY AI AGENTS</div>
</section>
<section id="e2" class="clip" data-start="10.4" data-duration="2.6"><div class="end">
  <div id="lgE">{XLOGO}</div>
  <div class="wm" id="wmE"><b>X</b>Forward</div>
  <p class="tag" id="tgE">Get your hours back.</p>
  <p class="url" id="urE">xforward.ca</p>
</div></section>
""", js="""
const rows=[...document.querySelectorAll('.rl')];
tl.fromTo('#rc',{y:-900},{y:-620,duration:.7,ease:'power2.out'},.1);
rows.forEach((r,i)=>{const t=.5+i*.42; tl.fromTo(r,{opacity:0},{opacity:1,duration:.12},t);});
tl.to('#rc',{y:40,duration:rows.length*.42,ease:'none'},.6);
tl.fromTo('#stE',{opacity:0,scale:2.6,rotation:-20},{opacity:1,scale:1,rotation:-9,duration:.32,ease:'power4.in'},7.8);
tl.fromTo('#rc',{x:0},{x:12,duration:.05,yoyo:true,repeat:3,immediateRender:false},8.12);
tl.to(['#rc','#stE'],{y:'+=1200',duration:.7,ease:'power3.in'},9.7);
xMorph(tl,'#lgE',10.5);
tl.fromTo('#wmE',{opacity:0,y:30},{opacity:1,y:0,duration:.45,ease:'power3.out'},10.9);
tl.fromTo('#tgE',{opacity:0,y:20},{opacity:1,y:0,duration:.45},11.3);
tl.fromTo('#urE',{opacity:0},{opacity:1,duration:.45},11.7);
""")


def build():
    out = os.path.join(HERE, "projects")
    for cid, c in CONCEPTS.items():
        d = os.path.join(out, cid)
        os.makedirs(os.path.join(d, "fonts"), exist_ok=True)
        for f in os.listdir(os.path.join(HERE, "fonts")):
            if f.endswith(".woff2"):
                shutil.copy(os.path.join(HERE, "fonts", f), os.path.join(d, "fonts", f))
        shutil.copy(os.path.join(HERE, "gsap.min.js"), os.path.join(d, "gsap.min.js"))
        zoom = c["zoom"] if DRAFT else 1
        with open(os.path.join(d, "index.html"), "w") as fh:
            fh.write(page(cid, c["w"], c["h"], zoom, c["dur"], c["css"], c["body"], c["js"]))
        print("built", cid, round(c["w"] * zoom), "x", round(c["h"] * zoom), c["dur"], "s")


if __name__ == "__main__":
    build()
