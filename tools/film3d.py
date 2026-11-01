"""The Noise – épisode filmé en 3D (plateau du jeu + plateau du journal), personnages animés,
bouches pilotées image par image par l'enveloppe des voix de Shlomo (sync exacte)."""
import sys, os, json, math, subprocess, struct, importlib.util
from playwright.sync_api import sync_playwright

E = '/tmp/claude-0/ep'; R = '/home/claude/thenoise'; NM = '/tmp/nm/node_modules'; FPS = 30
spec = importlib.util.spec_from_file_location('build', f'{E}/build.py'); B = importlib.util.module_from_spec(spec); spec.loader.exec_module(B)
SEG, starts, TOTAL, frames = B.SEG, B.starts, B.TOTAL, B.frames
fstart = [sum(frames[:i]) for i in range(len(frames))]
NFR = sum(frames)

# ---------- enveloppes des voix (par image) ----------
def pcm(f):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True).stdout
    return struct.unpack(f'<{len(raw)//2}h', raw)
SRC = {'n': pcm(f'{E}/nimrod.mp3'), 'd': pcm(f'{E}/danit.mp3')}
def rms(src, t):
    a = SRC[src]; i0 = int(t * 16000); w = 16000 // 30
    s = a[max(0, i0 - w // 2): i0 + w // 2]
    return math.sqrt(sum(x * x for x in s) / len(s)) if s else 0
PEAK = {k: sorted(rms(k, i / 60) for i in range(int(len(v) / 16000 * 60)))[-int(len(v) / 16000 * 60) // 20] for k, v in SRC.items()}
def env(fi):
    t = (fi + .5) / FPS; out = {'n': 0., 'd': 0.}
    for (src, a, b), st in zip(SEG, starts):
        if st <= t < st + (b - a):
            out[src] = min(1., rms(src, a + t - st) / PEAK[src])
    return out
ENV = [env(i) for i in range(NFR)]
for k in 'nd':  # léger lissage (attaque rapide, relâche douce)
    p = 0
    for e in ENV:
        v = e[k]; p = v if v > p else p * .55 + v * .45; e[k] = round(p, 3)

# ---------- personnages (JS partagé) ----------
CHAR_JS = r'''
window.mkChar=function(o){
 const M=(c,e,ei)=>new THREE.MeshStandardMaterial({color:c,roughness:.55,emissive:e||0,emissiveIntensity:ei||0});
 const g=new THREE.Group();const Bx=(w,h,d,m,x,y,z,p)=>{const b=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),m);b.position.set(x,y,z);b.castShadow=true;(p||g).add(b);return b};
 const skin=M(o.skin||0xf1c7a2),shirt=M(o.shirt||0x2d6cdf,o.shirt||0x2d6cdf,.08),pants=M(o.pants||0x1b1b24),blk=M(0x0b0b0b),wht=M(0xffffff,0xffffff,.3);
 if(!o.noLegs){Bx(.3,.75,.32,pants,-.18,.375,0);Bx(.3,.75,.32,pants,.18,.375,0);Bx(.32,.12,.42,blk,-.18,.06,.05);Bx(.32,.12,.42,blk,.18,.06,.05)}
 const body=new THREE.Group();body.position.y=.75;g.add(body);
 Bx(.84,.95,.46,shirt,0,.475,0,body);
 const arm=s=>{const a=new THREE.Group();a.position.set(s*.54,.88,0);body.add(a);Bx(.24,.8,.26,shirt,0,-.38,0,a);Bx(.22,.2,.24,skin,0,-.86,0,a);return a};
 const aL=arm(-1),aR=arm(1);
 const head=new THREE.Group();head.position.y=1.0;body.add(head);
 let eL,eR,mo;
 if(o.mic){const grille=new THREE.MeshStandardMaterial({color:0x3a3a42,metalness:.85,roughness:.35});
   Bx(.16,.2,.16,M(0x222228),0,.05,0,head);
   const sp=new THREE.Mesh(new THREE.SphereGeometry(.46,28,22),grille);sp.position.y=.5;head.add(sp);
   const band=new THREE.Mesh(new THREE.TorusGeometry(.465,.04,10,40),new THREE.MeshStandardMaterial({color:0xFFC24B,metalness:.9,roughness:.25,emissive:0x553300}));band.position.y=.42;band.rotation.x=Math.PI/2;head.add(band);
   const ew=new THREE.MeshStandardMaterial({color:0xffffff,emissive:0xffffff,emissiveIntensity:.35});
   const eye=x=>{const e=new THREE.Group();e.position.set(x,.6,.42);head.add(e);const w=new THREE.Mesh(new THREE.BoxGeometry(.16,.18,.04),ew);e.add(w);const p=new THREE.Mesh(new THREE.BoxGeometry(.08,.1,.02),blk);p.position.z=.03;e.add(p);return e};
   eL=eye(-.15);eR=eye(.15);mo=Bx(.22,.05,.04,M(0x6a1020,0x6a1020,.3),0,.36,.43,head);
   Bx(.36,.12,.06,M(0xE01F26,0xE01F26,.3),0,.86,.25,body);Bx(.12,.14,.07,M(0xE01F26),0,.86,.26,body);Bx(.14,.5,.04,wht,0,.62,.235,body);
 }else{
   Bx(.64,.64,.6,skin,0,.33,0,head);
   eL=Bx(.11,.13,.03,blk,-.14,.4,.31,head);eR=Bx(.11,.13,.03,blk,.14,.4,.31,head);
   Bx(.14,.03,.02,blk,-.14,.5,.31,head);Bx(.14,.03,.02,blk,.14,.5,.31,head);
   mo=Bx(.22,.05,.03,M(0x6a1020),0,.18,.31,head);
   if(o.hair){const hm=M(o.hair);Bx(.7,.18,.66,hm,0,.7,-.01,head);Bx(.7,.36,.12,hm,0,.5,-.3,head);
     if(o.long){Bx(.7,.95,.16,hm,0,.25,-.33,head);Bx(.12,.9,.5,hm,-.36,.25,-.05,head);Bx(.12,.9,.5,hm,.36,.25,-.05,head)}
     else{Bx(.1,.3,.5,hm,-.35,.5,-.05,head);Bx(.1,.3,.5,hm,.35,.5,-.05,head)}}
   if(o.ear){const gm=M(0xFFC24B,0xFFC24B,.6);Bx(.06,.1,.06,gm,-.36,.15,.12,head);Bx(.06,.1,.06,gm,.36,.15,.12,head)}
 }
 let mask=null;if(o.mask){mask=new THREE.Group();mask.position.set(0,.42,.33);head.add(mask);
   const gm=new THREE.MeshStandardMaterial({color:0xFFC24B,metalness:.95,roughness:.2,emissive:0x6b4500,emissiveIntensity:.6});
   const m1=new THREE.Mesh(new THREE.BoxGeometry(.72,.36,.06),gm);mask.add(m1);
   const h=new THREE.Mesh(new THREE.BoxGeometry(.14,.1,.02),blk);h.position.set(-.15,0,.035);mask.add(h);const h2=h.clone();h2.position.x=.15;mask.add(h2);
   const f=new THREE.Mesh(new THREE.BoxGeometry(.1,.3,.04),gm);f.position.set(.4,.2,0);f.rotation.z=-.5;mask.add(f);
   const gl=new THREE.Mesh(new THREE.SphereGeometry(.05,10,8),new THREE.MeshBasicMaterial({color:0xff3d6e}));gl.position.set(.42,.37,0);mask.add(gl)}
 if(o.bee){Bx(.86,.16,.48,M(0x111111),0,.3,0,body);Bx(.86,.16,.48,M(0x111111),0,.65,0,body)}
 const c={g,body,head,aL,aR,eL,eR,mo,mask,ph:o.ph||0,o};return c};
window.animChar=function(c,t,talk,mode){
 const ph=c.ph;c.mo.scale.y=1+talk*5.5;c.mo.scale.x=1-talk*.3;
 const bl=((t+ph*1.7)%3.9)<.13;c.eL.scale.y=c.eR.scale.y=bl?.12:1;
 c.body.position.y=.75+Math.sin(t*2.4+ph)*.012;
 if(mode==='sing'){const s=.5+.5*Math.sin(t*5.2+ph);c.mo.scale.y=1+(talk||s*.8)*5;
   c.body.rotation.z=Math.sin(t*2.3+ph)*.07;c.body.rotation.y=Math.sin(t*1.1+ph)*.15;c.head.rotation.x=-.18+Math.sin(t*2.3)*.06;c.head.rotation.z=Math.sin(t*2.3+ph)*.08;
   c.aR.rotation.x=-1.25+Math.sin(t*4.6)*.08;c.aR.rotation.z=-.25;c.aL.rotation.x=-.3-.5*(.5+.5*Math.sin(t*1.7+ph));c.aL.rotation.z=.35+.55*(.5+.5*Math.sin(t*2.3+ph));}
 else if(mode==='cheer'){const j=Math.abs(Math.sin(t*6+ph));c.g.position.y=c.y0+j*.25;c.aL.rotation.z=.4+2.2*j;c.aR.rotation.z=-.4-2.2*j;c.mo.scale.y=4;}
 else if(mode==='desk'){c.head.rotation.x=-.04+Math.sin(t*1.9+ph)*.03-talk*.07;c.head.rotation.y=Math.sin(t*.8+ph)*.1;c.head.rotation.z=Math.sin(t*1.3)*.03;
   c.aL.rotation.x=-1.05-talk*.25*Math.abs(Math.sin(t*3.1));c.aR.rotation.x=-1.0-talk*.45*Math.abs(Math.sin(t*2.2+1));c.aR.rotation.z=-.1-talk*.25*Math.abs(Math.sin(t*1.7));}
 else{c.head.rotation.x=-.05+Math.sin(t*2.1+ph)*.04-talk*.09;c.head.rotation.y=Math.sin(t*.9+ph)*.14;c.head.rotation.z=Math.sin(t*1.4+ph)*.04;
   c.aL.rotation.x=-.25-talk*.9*Math.abs(Math.sin(t*2.9+ph));c.aL.rotation.z=.12+talk*.35*Math.abs(Math.sin(t*1.9));
   c.aR.rotation.x=-.2-talk*.7*Math.abs(Math.sin(t*2.3+1.3));c.aR.rotation.z=-(.12+talk*.55*Math.abs(Math.sin(t*2.6+.5)));
   c.body.rotation.y=Math.sin(t*.7+ph)*.08;}
};
'''

# ---------- plateau du jeu (index.html?demo) ----------
STUDIO_JS = r'''
nameLabels.visible=false;contGroup.visible=false;chairs.forEach(c=>{if(c.label)c.label.visible=false});
document.body.querySelectorAll('*').forEach(e=>{if(e.tagName!=='CANVAS'&&!e.contains(renderer.domElement))e.style.visibility='hidden'});
controls.enabled=true;controls.enableDamping=false;fly=null;
const key=new THREE.SpotLight(0xfff0dd,1.3,40,.42,.6,1);key.position.set(2,11,10);key.target.position.set(0,2,0);scene.add(key,key.target);
const fill=new THREE.PointLight(0xffd0a0,.9,18);fill.position.set(0,4,7);scene.add(fill);
const C={};
C.dudi=mkChar({mic:true,shirt:0x16161c,pants:0x16161c,ph:.3});C.dudi.g.position.set(0,.7,0);
C.harel=mkChar({shirt:0x22aa66,hair:0x1a120c,mask:true,ph:1.1,skin:0xe0ac69});C.harel.g.position.set(0,.7,0);
C.shahar=mkChar({shirt:0xff5fa8,hair:0x3b2314,long:true,ear:true,ph:2.2});C.shahar.g.position.set(0,.7,0);
const sil=figure(rimY);sil.scale.setScalar(1.55);sil.position.set(0,.7,0);scene.add(sil);
Object.values(C).forEach(c=>scene.add(c.g));
const fans=[];for(let i=0;i<9;i++){const f=mkChar({shirt:[0xE01F26,0xFFC24B,0x2d6cdf,0x22aa66,0x9b30ff,0xff7a1a,0x18c3c3,0xffffff,0xff66cc][i],hair:[0x1a120c,0x3b2314,0x8a5a2b][i%3],long:i%2==0,ph:i*.9,skin:[0xf1c27d,0xe0ac69,0xc68642,0xffdbac][i%4]});
  const a=-.5+i*.125,r=4.8+(i%2)*.9;f.g.position.set(Math.sin(a)*r,0,4.5+Math.cos(a)*r*.5);f.y0=0;f.g.rotation.y=Math.PI+a*.6;f.g.scale.setScalar(.9);scene.add(f.g);fans.push(f)}
window.STUDIO={C,sil,fans};
window.shot=function(o){ // o: {t,lt,sc,cam:[x,y,z],look:[x,y,z],who,talk}
  const T=window.STUDIO;['dudi','harel','shahar'].forEach(k=>T.C[k].g.visible=o.who===k);T.sil.visible=o.who==='sil';
  mic.visible=o.who!=='dudi';T.fans.forEach(f=>f.g.visible=!!o.fans);
  camera.position.set(...o.cam);controls.target.set(...o.look);
  if(o.who==='dudi')animChar(T.C.dudi,o.t,o.talk,'talk');
  if(o.who==='harel'){animChar(T.C.harel,o.t,0,'sing');const m=T.C.harel.mask;
    if(o.reveal!=null&&o.reveal>=0){const k=Math.min(1,o.reveal/.55);m.position.set(.9*k,.42+1.6*k,.33+1.2*k);m.rotation.set(-2*k,1.5*k,3*k)}else{m.position.set(0,.42,.33);m.rotation.set(0,0,0)}}
  if(o.who==='shahar')animChar(T.C.shahar,o.t,0,'sing');
  if(o.who==='sil')T.sil.rotation.y=Math.sin(o.t*.6)*.15;
  if(o.fans)T.fans.forEach(f=>animChar(f,o.t,0,'cheer'));
  if(o.chairTurn!=null)chairs[1].g.rotation.y=Math.PI*o.chairTurn;else chairs.forEach(c=>c.g.rotation.y=0);
  screenLine=o.screen||'';
  if(o.jump){for(let i=0;i<14;i++){const si=seatOrder[Math.floor(Math.random()*Math.min(146,MAXS))];JUMP[si]=performance.now()}
    if(Math.random()<.5){const si=seatOrder[Math.floor(Math.random()*120)];const[x,y,z]=SEATS[si];const e=emojiSprite(Math.random()<.5?'👏':'🎟️');e.position.set(x,y+2.4,z);scene.add(e);FLY.push({o:e,t0:performance.now(),type:'em',y0:y+2.4})}}
  capHook(o.t)};
const _cap=window.capHook;window.capHook=function(t){chairs.forEach(c=>{if(c.label)c.label.visible=false});nameLabels.visible=false;contGroup.visible=false;_cap(t)};
'''

# ---------- plateau du journal (dérivé de tools/plateau/plateau.html) ----------
def news_html():
    h = open(f'{R}/tools/plateau/plateau.html', encoding='utf-8').read()
    a = h.index('<div id="ov">'); b = h.index('<script>', a); h = h[:a] + h[b:]
    a = h.index('// presenter (cube style)'); b = h.index('box(0.5,0.05,0.35,shirt'); h = h[:a] + '''// presenter (animée)
const DN=mkChar({shirt:0xc8202a,hair:0x2b1a12,long:true,ear:true,noLegs:true,ph:.7});DN.g.position.set(0,.8,.55);S.add(DN.g);
const skin=M(0xf1c7a2),shirt=M(0xffffff);''' + h[b:]
    h = h.replace('<script src="three.min.js"></script>', '<script src="three.min.js"></script><script>' + CHAR_JS + '</script>')
    h = h.replace("window.ready=true", "window.ready=true;window.nshot=o=>{C.position.set(...o.cam);C.lookAt(...o.look);animChar(DN,o.t,o.talk,'desk');rim.intensity=1.1+.25*Math.sin(o.t*1.7);R.render(S,C)}")
    open(f'{R}/tools/plateau/news_film.html', 'w', encoding='utf-8').write(h)

def lerp(a, b, k): return [x + (y - x) * k for x, y in zip(a, b)]
def ease(k): return k * k * (3 - 2 * k)

# plan de chaque scène : (plateau, fonction(lt, d) -> params)
def S(cam0, cam1, look0, look1, **kw):
    def f(lt, d, t, e):
        k = ease(min(1, lt / d)); o = dict(kw); o.update(cam=lerp(cam0, cam1, k), look=lerp(look0, look1, k), t=t)
        return o
    return f
PLAN = [
    ('studio', S([0, 13, 24], [0, 3.7, 6.0], [0, 2.6, 0], [0, 3.2, 0], who='dudi', screen='The Noise')),          # בפרק הקודם
    ('news',   S([0, 3.4, 8.2], [0, 3.2, 6.6], [0, 3.5, 0], [0, 3.4, 0])),                                       # מבזק
    ('news',   S([2.4, 3.2, 6.4], [1.7, 3.1, 5.4], [0, 3.4, .4], [0, 3.35, .4])),                                  # 56
    ('studio', S([3.2, 3.5, 7.5], [1.2, 3.1, 4.9], [0, 2.6, 0], [0, 2.75, 0], who='harel', screen='🎭 ערב המסכות')),   # מסכות
    ('studio', S([0, 2.9, 4.4], [0, 2.85, 3.7], [0, 2.75, 0], [0, 2.75, 0], who='harel', screen='🎭 הראל!')),         # הראל!
    ('studio', S([0, 3.6, 2.2], [0, 4.6, 1.2], [0, 3.2, 16], [0, 3.8, 16], who='harel', jump=True, fans=True, screen='+30 🎟️')),  # +30
    ('studio', S([0, 4.4, 13.2], [0, 3.3, 5.9], [0, 2.3, 0], [0, 2.95, 0], who='shahar', screen='🎤 אודישן מוקדם')),  # שחר
    ('news',   S([-2.3, 3.3, 7.4], [-1.3, 3.1, 6.0], [0, 3.45, .3], [0, 3.4, .3])),                                # שופטים
    ('studio', S([0, 1.6, 9], [0, 2.3, 5.2], [0, 2.4, 0], [0, 2.6, 0], who='sil', screen='⏩ בפרק הבא…')),           # בפרק הבא
    ('studio', S([1.8, 3.4, 6.2], [0, 3.0, 4.4], [0, 3.2, 0], [0, 3.35, 0], who='dudi', fans=True, screen='?מה יקרה מחר')),  # מה יקרה מחר
]
REVEAL = starts[4]

def routes(pg):
    pg.route('**/three.min.js', lambda r: r.fulfill(path=f'{NM}/three/build/three.min.js'))
    pg.route('**/OrbitControls.js', lambda r: r.fulfill(path=f'{NM}/three/examples/js/controls/OrbitControls.js'))
    pg.route('**/supabase.min.js', lambda r: r.fulfill(body='window.supabase=null', content_type='text/javascript'))
    css = ''.join(f"@font-face{{font-family:Heebo;src:url(http://local/__f/heebo-{s}-{w}-normal.woff2);font-weight:{w}}}" for s in ('hebrew', 'latin') for w in (400, 900))
    pg.route('https://fonts.googleapis.com/**', lambda r: r.fulfill(body=css, content_type='text/css'))
    def loc(r):
        p = r.request.url.split('http://local/')[1].split('?')[0]
        if p.startswith('__f/'): return r.fulfill(path=f'{NM}/@fontsource/heebo/files/{p[4:]}')
        if p.endswith('.woff2'): return r.fulfill(path=f'{NM}/@fontsource/heebo/files/{p.split("/")[-1]}')
        if p.endswith('three.min.js'): return r.fulfill(path=f'{NM}/three/build/three.min.js')
        if p.endswith('logo_t.png'): return r.fulfill(path=f'{R}/logo_t.png')
        return r.fulfill(path=f'{R}/{p}')
    pg.route('http://local/**', loc)

INIT = "window.CAP=true;window.__T=0;performance.now=()=>window.__T*1000;Math.random=(()=>{let s=12345;return()=>{s=(s*16807)%2147483647;return(s-1)/2147483646}})();"

def main(only=None, preview=None):
    news_html()
    with sync_playwright() as p:
        b = p.chromium.launch(args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
        st = b.new_page(viewport={'width': 540, 'height': 960}, device_scale_factor=2); routes(st); st.add_init_script(INIT)
        st.goto('http://local/index.html?demo'); st.wait_for_timeout(3000)
        st.evaluate(CHAR_JS + ";0"); st.evaluate(STUDIO_JS + ";0"); st.evaluate(f'window.REV={REVEAL}')
        nw = b.new_page(viewport={'width': 1080, 'height': 1920}); routes(nw); nw.add_init_script(INIT)
        nw.goto('http://local/tools/plateau/news_film.html'); nw.wait_for_function('window.ready===true', timeout=20000)
        for i, (where, fn) in enumerate(PLAN):
            if only is not None and i not in only: continue
            n = frames[i]; d = n / FPS
            pts = preview if preview else None
            ff = None
            if not pts:
                tmp = f'{E}/v{i}.tmp.mp4'
                vf = "[0:v]format=yuv420p[bg];[1:v]format=rgba,fade=t=in:st=0:d=0.22:alpha=1[o];[bg][o]overlay=0:0:format=auto,format=yuv420p[v]"
                ff = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'image2pipe', '-framerate', str(FPS), '-c:v', 'mjpeg', '-i', '-',
                                       '-loop', '1', '-framerate', str(FPS), '-i', f'{E}/ov3d{i}.png', '-filter_complex', vf, '-map', '[v]', '-frames:v', str(n),
                                       '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p', '-r', str(FPS), tmp], stdin=subprocess.PIPE)
            rng = [int(x * n) for x in pts] if pts else range(n)
            for j in rng:
                gi = fstart[i] + j; t = gi / FPS; lt = j / FPS; e = ENV[gi]
                o = fn(lt, d, t, e)
                if where == 'news':
                    o['talk'] = e['d']; nw.evaluate('o=>{window.__T=o.t;nshot(o)}', o); img = nw.screenshot(type='jpeg', quality=90)
                else:
                    o['talk'] = e['n']
                    if i in (3, 4): o['reveal'] = t - REVEAL - .08
                    st.evaluate("o=>{window.__T=o.t;show=o.showAt!=null?{t0:o.showAt*1000}:(o.t>REV?{t0:(REV-1.25)*1000}:null);window.REV2=0;shot(o)}", dict(o, showAt=(REVEAL + .05 - 1.3) if (i in (3, 4) and t >= REVEAL + .05 - 1.3) else None))
                    img = st.screenshot(type='jpeg', quality=90)
                if ff: ff.stdin.write(img)
                else: open(f'{E}/pv{i}_{j}.jpg', 'wb').write(img)
            if ff:
                ff.stdin.close(); ff.wait()
                if ff.returncode: raise SystemExit(f'ffmpeg scene {i}')
                os.replace(f'{E}/v{i}.tmp.mp4', f'{E}/v{i}.mp4')
            print('scene', i, 'ok', flush=True)
        b.close()

if __name__ == '__main__':
    a = sys.argv[1:]
    if a and a[0] == 'preview': main(preview=[.15, .85])
    elif a and a[0] == 'scenes': main(only=[int(x) for x in a[1:]])
    else: main()
