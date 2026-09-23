"""Round 2: premium (Apple/Stripe) x manifesto (Nike) concepts, awe-first hooks.

Three.js for the hero visuals (driven by HyperFrames `hf-seek` time), GSAP for
type, and a synthesized beat track per concept. Draft = low-res; `--final`
renders full resolution from the same source.
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
#gl{position:absolute;left:0;top:0;display:block}
.clip{position:absolute;inset:0}
.xl{display:block;overflow:visible}
.xl path{fill:none;stroke-width:2.3;stroke-linecap:round;stroke-linejoin:round}
.xl .m1{stroke:#fff}.xl .m2{stroke:#8C96FF}
.big{font-weight:800;font-stretch:125%;letter-spacing:-.045em;line-height:.9;margin:0}
.lineup{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;text-align:center}
.wm{font-weight:750;font-stretch:118%;letter-spacing:-.04em}.wm b{color:#8C96FF}
.tag{font-weight:450;color:rgba(255,255,255,.72)}
.mono{font-family:'IBM Plex Mono',monospace;letter-spacing:.14em;text-transform:uppercase}
"""


def page(cid, W, H, zoom, dur, css, body, js, module):
    w, h = round(W * zoom), round(H * zoom)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width={w}, height={h}">
<title>XForward ad · {cid}</title>
<script src="gsap.min.js"></script>
<script type="importmap">{{"imports":{{"three":"./three/three.module.js"}}}}</script>
<style>
{FONTS}
{CSS0}
.stage{{width:{W}px;height:{H}px;zoom:{zoom}}}
#gl{{width:{W}px;height:{H}px}}
{css}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-width="{w}" data-height="{h}" data-duration="{dur}">
<div class="stage">
<canvas id="gl"></canvas>
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
<script type="module">
import * as THREE from 'three';
const W={W}, H={H}, Z={zoom};
const PXW=Math.round(W*Z), PXH=Math.round(H*Z);
const ss=(a,b,x)=>{{const t=Math.min(1,Math.max(0,(x-a)/(b-a)));return t*t*(3-2*t)}};
const lerp=(a,b,k)=>a+(b-a)*k;
function rng(seed){{let s=seed>>>0;return()=>((s=Math.imul(s^(s>>>15),2246822507)^Math.imul(s^(s>>>13),3266489909),(s^=s>>>16)>>>0)/4294967296)}}
window.__hf=window.__hf||{{}};window.__hf.buildReady=window.__hf.buildReady||{{}};
let resolveReady;window.__hf.buildReady['{cid}']=new Promise(r=>resolveReady=r);
{module}
</script>
</body>
</html>
"""


C = {}

# ======================================================================= 1 · Chrome X (16:9)
C["r2-1-chrome-x"] = dict(W=1920, H=1080, zoom=1/3, dur=15, music=synth.chrome_x, css="""
.sweep{position:absolute;left:0;top:50%;width:1920px;height:2px;margin-top:-1px;background:linear-gradient(90deg,transparent,#fff 45%,#8C96FF 55%,transparent);transform-origin:left center}
.veil{position:absolute;inset:0;background:#000;opacity:0}
.m{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;text-align:center;opacity:0}
.m .big{font-size:150px}
.m .acc{color:#8C96FF}
.end{position:absolute;left:0;right:0;bottom:170px;display:flex;flex-direction:column;align-items:center;gap:22px;text-align:center}
.end .wm{font-size:110px}.end .tag{font-size:40px}
""", body="""
<div class="sweep" id="sw"></div>
<div class="veil" id="vl"></div>
<div class="m" id="m1"><p class="big">The work that repeats.</p></div>
<div class="m" id="m2"><p class="big acc">Automated.</p></div>
<div class="m" id="m3"><p class="big">The work that matters.</p></div>
<div class="m" id="m4"><p class="big acc">Yours again.</p></div>
<div class="end"><div class="wm" id="wm"><b>X</b>Forward</div><div class="tag" id="tg">AI agents, built into your business.</div></div>
""", js="""
tl.fromTo('#sw',{scaleX:0,opacity:1},{scaleX:1,duration:.7,ease:'power3.inOut'},0);
tl.to('#sw',{opacity:0,duration:.5},.7);
const cut=(s,t,d)=>{tl.fromTo(s,{opacity:0,scale:1.06},{opacity:1,scale:1,duration:.12,ease:'power2.out'},t);tl.to(s,{opacity:0,duration:.1},t+d)};
tl.fromTo('#vl',{opacity:0},{opacity:.55,duration:.3},4.9);
cut('#m1',5.0,1.4); cut('#m2',6.5,1.4); cut('#m3',8.0,1.4); cut('#m4',9.5,1.35);
tl.to('#vl',{opacity:0,duration:.4},10.9);
tl.fromTo('#wm',{opacity:0,y:40},{opacity:1,y:0,duration:.7,ease:'power3.out'},11.3);
tl.fromTo('#tg',{opacity:0,y:20},{opacity:1,y:0,duration:.6,ease:'power3.out'},11.8);
""", module="""
import { RoomEnvironment } from './three/addons/RoomEnvironment.js';
const canvas=document.getElementById('gl');
const renderer=new THREE.WebGLRenderer({canvas,antialias:true,preserveDrawingBuffer:true});
renderer.setPixelRatio(1);renderer.setSize(PXW,PXH,false);
renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.outputColorSpace=THREE.SRGBColorSpace;
const scene=new THREE.Scene();scene.background=new THREE.Color(0x030305);
const pmrem=new THREE.PMREMGenerator(renderer);scene.environment=pmrem.fromScene(new RoomEnvironment(),0.04).texture;
const cam=new THREE.PerspectiveCamera(28,W/H,0.1,100);
const w=0.36,s=new THREE.Shape();
s.moveTo(-0.6,1);s.lineTo(-0.6+w,1);s.lineTo(0.4+w,0);s.lineTo(-0.6+w,-1);s.lineTo(-0.6,-1);s.lineTo(0.4,0);s.closePath();
const geo=new THREE.ExtrudeGeometry(s,{depth:0.32,bevelEnabled:true,bevelThickness:0.07,bevelSize:0.05,bevelSegments:6,curveSegments:4});
geo.translate(0,0,-0.16);
const chrome=new THREE.MeshPhysicalMaterial({color:0xe9edf5,metalness:1,roughness:0.14,clearcoat:1,clearcoatRoughness:0.05});
const cobalt=new THREE.MeshPhysicalMaterial({color:0x4a5cff,metalness:0.55,roughness:0.12,clearcoat:1,clearcoatRoughness:0.04,iridescence:1,iridescenceIOR:1.7,iridescenceThicknessRange:[200,700]});
const c1=new THREE.Mesh(geo,chrome),c2=new THREE.Mesh(geo,cobalt);
const g=new THREE.Group();g.add(c1,c2);scene.add(g);
const key=new THREE.PointLight(0xffffff,40,20);scene.add(key);
const rim=new THREE.PointLight(0x8c96ff,30,20);scene.add(rim);
const floorGlow=new THREE.Mesh(new THREE.CircleGeometry(3.2,64),new THREE.MeshBasicMaterial({color:0x2334e0,transparent:true,opacity:0.0}));
floorGlow.rotation.x=-Math.PI/2;floorGlow.position.y=-1.5;scene.add(floorGlow);
function renderAt(t){
  const lock=ss(3.6,4.5,t), endk=ss(11,12.2,t);
  c1.position.x=lerp(-0.95,-0.58,lock); c2.position.x=lerp(0.3,0.58,lock); c2.rotation.y=Math.PI*lock;
  c2.position.z=Math.sin(lock*Math.PI)*0.6;
  g.rotation.y=t<4.5? -1.0+0.14*t : lerp(-0.37+0.1*(t-4.5)*0+Math.sin((t-4.5)*0.55)*0.35,0,endk);
  g.rotation.x=0.08*Math.sin(t*0.4);
  g.position.y=lerp(0,0.62,endk); g.scale.setScalar(lerp(1,0.62,endk));
  const push=ss(0.3,4.4,t);
  cam.position.set(lerp(1.3,0,push)+Math.sin(t*0.3)*0.25,lerp(0.55,0.12,push),lerp(3.3,6.6,push)-ss(4.5,11,t)*0.8+endk*0.8);
  cam.lookAt(0,g.position.y*0.6,0);
  key.position.set(Math.cos(t*0.9)*3,1.8,Math.sin(t*0.9)*3+1);
  rim.position.set(-Math.cos(t*0.6)*3,-1,-2);
  renderer.toneMappingExposure=ss(0.4,2.4,t)*1.15 + 0.35*Math.exp(-Math.pow((t-4.5)/0.18,2)) + 0.25*Math.exp(-Math.pow((t-11)/0.2,2));
  floorGlow.material.opacity=0.18*ss(4.4,5.2,t);
  renderer.render(scene,cam);
}
window.addEventListener('hf-seek',e=>renderAt(e.detail.time));
renderAt(window.__hfThreeTime||0); resolveReady();
""")

# ======================================================================= 2 · Tunnel (9:16)
C["r2-2-tunnel"] = dict(W=1080, H=1920, zoom=1/3, dur=14, music=synth.tunnel, css="""
.bg{position:absolute;inset:0;opacity:0}
.k{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;opacity:0}
.k .big{font-size:220px}
.ph{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;text-align:center;opacity:0;padding:0 60px}
.ph .big{font-size:150px;text-shadow:0 0 60px rgba(0,0,0,.8)}
.flash{position:absolute;inset:0;background:#fff;opacity:0}
.endbg{position:absolute;inset:0;background:#000}
.end{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:40px;text-align:center;padding:0 90px}
.end .xl{width:240px;height:240px}
.end .say{font-size:86px}
.end .wm{font-size:120px}.end .tag{font-size:44px}
""", body="""
<div class="bg" id="bg"></div>
<div class="k" id="k0"><p class="big">COPY.</p></div><div class="k" id="k1"><p class="big">PASTE.</p></div>
<div class="k" id="k2"><p class="big">REPEAT.</p></div><div class="k" id="k3"><p class="big">COPY.</p></div>
<div class="k" id="k4"><p class="big">PASTE.</p></div><div class="k" id="k5"><p class="big">REPEAT.</p></div>
<div class="k" id="k6"><p class="big">COPY.</p></div><div class="k" id="k7"><p class="big">PAS—</p></div>
<div class="ph" id="p1"><p class="big">Your people</p></div>
<div class="ph" id="p2"><p class="big">deserve</p></div>
<div class="ph" id="p3"><p class="big" style="color:#8C96FF">better work.</p></div>
<section id="endS" class="clip" data-start="9.9" data-duration="4.1">
  <div class="endbg"></div>
  <div class="end">
    <div id="lg">""" + XLOGO + """</div>
    <p class="big say" id="sy">Agents do the rest.</p>
    <div class="wm" id="wm"><b>X</b>Forward</div>
    <div class="tag" id="tg">AI agents, built into your business.</div>
  </div>
</section>
<div class="flash" id="fl"></div>
""", js="""
const b=60/128, cols=['#ffffff','#000000','#2334E0','#000000','#ffffff','#2334E0','#000000','#ffffff'], ink=['#000','#fff','#fff','#fff','#000','#fff','#fff','#000'];
tl.set('#bg',{opacity:1},3.3);
for(let i=0;i<8;i++){const t=3.3+i*b;
  tl.set('#bg',{backgroundColor:cols[i]},t);
  tl.set('#k'+i+' .big',{color:ink[i]},t);
  tl.fromTo('#k'+i,{opacity:1,scale:1.18},{opacity:1,scale:1,duration:b*.9,ease:'power4.out',immediateRender:false},t);
  tl.set('#k'+i,{opacity:0},t+b);}
tl.set('#bg',{opacity:0},3.3+8*b);
const ph=(s,t,d)=>{tl.fromTo(s,{opacity:0,y:30},{opacity:1,y:0,duration:.25,ease:'power3.out'},t);tl.to(s,{opacity:0,duration:.15},t+d)};
ph('#p1',7.35,.8); ph('#p2',8.2,.75); ph('#p3',9.0,.85);
tl.fromTo('#fl',{opacity:0},{opacity:1,duration:.12},9.8);
tl.to('#fl',{opacity:0,duration:.6,ease:'power2.out'},9.95);
xMorph(tl,'#lg',10.0);
tl.fromTo('#sy',{opacity:0,y:30},{opacity:1,y:0,duration:.4,ease:'power3.out'},10.5);
tl.to('#sy',{opacity:0,duration:.25},11.7);
tl.fromTo('#wm',{opacity:0,y:30},{opacity:1,y:0,duration:.5,ease:'power3.out'},11.9);
tl.fromTo('#tg',{opacity:0},{opacity:1,duration:.5},12.3);
""", module="""
const canvas=document.getElementById('gl');
const renderer=new THREE.WebGLRenderer({canvas,antialias:true,preserveDrawingBuffer:true});
renderer.setPixelRatio(1);renderer.setSize(PXW,PXH,false);renderer.outputColorSpace=THREE.SRGBColorSpace;
const scene=new THREE.Scene();scene.background=new THREE.Color(0x000000);scene.fog=new THREE.Fog(0x000000,3,34);
const cam=new THREE.PerspectiveCamera(70,W/H,0.1,200);
const words=['COPY','PASTE','RE-TYPE','FOLLOW UP','INVOICE','RESCHEDULE','CHASE','REMIND','UPDATE CRM','SORT EMAIL','DATA ENTRY','CALL BACK','QUOTE','REPEAT'];
const tc=document.createElement('canvas');tc.width=2048;tc.height=1024;const x=tc.getContext('2d');
let tex=null, tube=null, glow=null, ready=false;
async function build(){
  await document.fonts.load("800 96px Archivo");
  const r=rng(42);x.fillStyle='#000';x.fillRect(0,0,2048,1024);x.textBaseline='middle';
  for(let row=0;row<8;row++){let px=-r()*400;const y=64+row*128;
    x.font="800 92px Archivo";
    while(px<2048){const wd=words[Math.floor(r()*words.length)];const a=r();
      x.fillStyle=a>.86?'#8C96FF':(a>.45?'rgba(255,255,255,.92)':'rgba(255,255,255,.28)');
      x.fillText(wd,px,y);px+=x.measureText(wd).width+70;}}
  tex=new THREE.CanvasTexture(tc);tex.wrapS=tex.wrapT=THREE.RepeatWrapping;tex.repeat.set(-2,5);tex.colorSpace=THREE.SRGBColorSpace;tex.anisotropy=8;
  const mat=new THREE.MeshBasicMaterial({map:tex,side:THREE.BackSide,color:0xffffff});
  tube=new THREE.Mesh(new THREE.CylinderGeometry(2.4,2.4,80,64,1,true),mat);tube.rotation.x=Math.PI/2;
  const grp=new THREE.Group();grp.add(tube);scene.add(grp);tube.userData.grp=grp;
  const gc=document.createElement('canvas');gc.width=gc.height=256;const gx=gc.getContext('2d');
  const gr=gx.createRadialGradient(128,128,0,128,128,128);gr.addColorStop(0,'rgba(255,255,255,1)');gr.addColorStop(.25,'rgba(140,150,255,.9)');gr.addColorStop(1,'rgba(35,52,224,0)');
  gx.fillStyle=gr;gx.fillRect(0,0,256,256);
  glow=new THREE.Sprite(new THREE.SpriteMaterial({map:new THREE.CanvasTexture(gc),transparent:true,depthWrite:false,fog:false}));
  glow.position.set(0,0,-38);scene.add(glow);
  cam.position.set(0,0,30);cam.lookAt(0,0,-40);
  ready=true;
}
const white=new THREE.Color(0xffffff),blue=new THREE.Color(0x8c96ff);
function renderAt(t){
  if(!ready)return;
  const travel=0.45*t+0.09*t*t+ss(7.1,9.9,t)*2.2*(t-7.1);
  tex.offset.y=-travel*0.35;
  tube.userData.grp.rotation.z=0.12*t+0.05*t*t*0.1;
  tube.material.color.copy(white).lerp(blue,ss(7.1,8.4,t));
  const g=ss(6.8,9.9,t);glow.scale.setScalar(6+g*60);glow.material.opacity=0.35+0.65*g;
  cam.fov=70+ss(7.5,9.9,t)*25;cam.updateProjectionMatrix();
  renderer.render(scene,cam);
}
window.addEventListener('hf-seek',e=>renderAt(e.detail.time));
build().then(()=>{renderAt(window.__hfThreeTime||0);resolveReady();});
""")

# ======================================================================= 3 · Hours (1:1)
C["r2-3-hours"] = dict(W=1080, H=1080, zoom=4/9, dur=15, music=synth.hours, css="""
.cap{position:absolute;left:0;right:0;text-align:center;opacity:0}
.cap .mono{font-size:26px;color:rgba(255,255,255,.7)}
.num{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;opacity:0}
.num .big{font-size:230px;font-variant-numeric:tabular-nums}
.num .mono{font-size:28px;color:rgba(255,255,255,.75);margin-top:18px}
.say{position:absolute;left:0;right:0;bottom:130px;text-align:center;opacity:0}
.say .big{font-size:96px}
.end{position:absolute;left:0;right:0;bottom:120px;display:flex;flex-direction:column;align-items:center;gap:18px}
.end .wm{font-size:100px}.end .tag{font-size:36px}
""", body="""
<div class="cap" id="c0" style="top:150px"><p class="mono">A 10-person team gives you</p></div>
<div class="num" id="n0"><p class="big"><span id="nn">0</span></p><p class="mono">hours a year</p></div>
<div class="say" id="s1"><p class="big">Thousands go in circles.</p></div>
<div class="say" id="s2"><p class="big">We send them <span style="color:#8C96FF">forward.</span></p></div>
<div class="end"><div class="wm" id="wm"><b>X</b>Forward</div><div class="tag" id="tg">AI agents, built into your business.</div></div>
""", js="""
tl.fromTo('#c0',{opacity:0,y:20},{opacity:1,y:0,duration:.6,ease:'power3.out'},.5);
tl.fromTo('#n0',{opacity:0,scale:.92},{opacity:1,scale:1,duration:.7,ease:'power3.out'},.8);
const o={v:0};tl.to(o,{v:20000,duration:1.6,ease:'power3.out',onUpdate:()=>{document.getElementById('nn').textContent=Math.round(o.v/10)*10>=1000?(Math.round(o.v/10)*10).toLocaleString('en-US'):Math.round(o.v)}},.8);
tl.to(['#c0','#n0'],{opacity:0,duration:.4},2.8);
tl.fromTo('#s1',{opacity:0,y:30},{opacity:1,y:0,duration:.6,ease:'power3.out'},3.6);
tl.to('#s1',{opacity:0,duration:.3},6.6);
tl.fromTo('#s2',{opacity:0,y:30},{opacity:1,y:0,duration:.5,ease:'power3.out'},7.2);
tl.to('#s2',{opacity:0,duration:.3},9.8);
tl.fromTo('#wm',{opacity:0,y:30},{opacity:1,y:0,duration:.6,ease:'power3.out'},11.0);
tl.fromTo('#tg',{opacity:0},{opacity:1,duration:.5},11.5);
""", module="""
const canvas=document.getElementById('gl');
const renderer=new THREE.WebGLRenderer({canvas,antialias:true,preserveDrawingBuffer:true});
renderer.setPixelRatio(1);renderer.setSize(PXW,PXH,false);
const scene=new THREE.Scene();scene.background=new THREE.Color(0x020207);
const cam=new THREE.PerspectiveCamera(42,1,0.1,100);
const N=3600,r=rng(2026),P=new Float32Array(N*3),CO=new Float32Array(N*3);
const home=[],loop=[],lane=[],xt=[];
for(let i=0;i<N;i++){
  const u=r()*2-1,a=r()*Math.PI*2,rad=Math.cbrt(r())*4.2;
  home.push([rad*Math.sqrt(1-u*u)*Math.cos(a),rad*u*0.7,rad*Math.sqrt(1-u*u)*Math.sin(a)]);
  const ring=i%48, rr=rng(ring*977+13); const cx=(rr()*2-1)*3.3,cy=(rr()*2-1)*2.3,cz=(rr()*2-1)*1.2,lr=0.28+rr()*0.5,th=rr()*Math.PI,om=(1.4+rr()*1.4)*(rr()<.5?-1:1);
  loop.push([cx,cy,cz,lr,Math.cos(th),Math.sin(th),(i/48)*Math.PI*2*0.37+r()*0.08,om]);
  lane.push([r()*14,(Math.floor(r()*18)-8.5)*0.3+(r()-.5)*0.05,(r()-.5)*1.2,2.2+r()*2.4]);
  const s=r()*2-1,side=r()<.5,ww=(r()-.5)*0.22,dd=(r()-.5)*0.3;
  xt.push(side?[s*1.55+ww,s*1.55+0.55,dd]:[s*1.55+ww,-s*1.55+0.55,dd]);
}
const geo=new THREE.BufferGeometry();geo.setAttribute('position',new THREE.BufferAttribute(P,3));geo.setAttribute('aColor',new THREE.BufferAttribute(CO,3));
const mat=new THREE.ShaderMaterial({transparent:true,depthWrite:false,blending:THREE.AdditiveBlending,
  uniforms:{uSize:{value:95*PXH/480}},
  vertexShader:`attribute vec3 aColor;varying vec3 vC;uniform float uSize;void main(){vec4 mv=modelViewMatrix*vec4(position,1.);gl_PointSize=uSize/-mv.z;gl_Position=projectionMatrix*mv;vC=aColor;}`,
  fragmentShader:`varying vec3 vC;void main(){float d=length(gl_PointCoord-.5);float a=smoothstep(.5,.0,d);a*=a;gl_FragColor=vec4(vC*a,a);}`});
const pts=new THREE.Points(geo,mat);scene.add(pts);
const cDrift=[.55,.62,.85],cLoop=[.62,.42,1.0],cStream=[.45,.55,1.0],cWhite=[1,1,1],cBlue=[.42,.48,1.0];
function renderAt(t){
  const a=ss(3.0,4.2,t),b=ss(6.8,7.7,t),c=ss(9.6,10.8,t),rot=0.06*t;
  for(let i=0;i<N;i++){
    const h=home[i],cr=Math.cos(rot),sr=Math.sin(rot);
    let x=h[0]*cr-h[2]*sr,y=h[1]+0.08*Math.sin(t*0.7+i),z=h[0]*sr+h[2]*cr;
    const L=loop[i],ang=L[6]+L[7]*t;
    const lx=L[0]+L[3]*Math.cos(ang),ly=L[1]+L[3]*Math.sin(ang)*L[4],lz=L[2]+L[3]*Math.sin(ang)*L[5];
    x=lerp(x,lx,a);y=lerp(y,ly,a);z=lerp(z,lz,a);
    const ln=lane[i],sx=((ln[0]+ln[3]*t*1.6)%14)-7;
    x=lerp(x,sx,b);y=lerp(y,ln[1],b);z=lerp(z,ln[2],b);
    const X=xt[i],pulse=1+0.02*Math.sin(t*3+i);
    x=lerp(x,X[0]*pulse,c);y=lerp(y,X[1]*pulse,c);z=lerp(z,X[2],c);
    P[i*3]=x;P[i*3+1]=y;P[i*3+2]=z;
    const endc=X[0]<0?cWhite:cBlue;
    for(let k=0;k<3;k++){let v=lerp(cDrift[k],cLoop[k],a);v=lerp(v,cStream[k],b);v=lerp(v,endc[k],c);CO[i*3+k]=v*(0.85-0.5*c);}
  }
  geo.attributes.position.needsUpdate=true;geo.attributes.aColor.needsUpdate=true;
  cam.position.set(Math.sin(t*0.12)*0.8,0.2,lerp(9.5,7.6,ss(0,6,t))+ss(9.6,11,t)*0.6);cam.lookAt(0,0.1+ss(9.6,11,t)*0.35,0);
  renderer.render(scene,cam);
}
window.addEventListener('hf-seek',e=>renderAt(e.detail.time));
renderAt(window.__hfThreeTime||0); resolveReady();
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
        if os.path.exists(os.path.join(d, "three")):
            shutil.rmtree(os.path.join(d, "three"))
        shutil.copytree(os.path.join(HERE, "three"), os.path.join(d, "three"))
        wav = os.path.join(d, "music.wav")
        if not os.path.exists(wav):
            c["music"](wav)
        zoom = c["zoom"] if DRAFT else 1
        with open(os.path.join(d, "index.html"), "w") as fh:
            fh.write(page(cid, c["W"], c["H"], zoom, c["dur"], c["css"], c["body"], c["js"], c["module"]))
        print("built", cid, round(c["W"] * zoom), "x", round(c["H"] * zoom))


if __name__ == "__main__":
    build()
