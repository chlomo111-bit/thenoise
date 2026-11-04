"""Épisode 02/11 filmé en 3D : chevauchée de l'extraterrestre sur l'autruche, battle de danse, NissoC."""
import sys, os, math, subprocess, struct, importlib.util
from playwright.sync_api import sync_playwright
sys.path.insert(0, '/tmp/claude-0/ep')
import film as F                      # personnages, routes, plateau du journal
E = '/tmp/claude-0/ep4'; FPS = 30
spec = importlib.util.spec_from_file_location('b2', f'{E}/build4.py'); B = importlib.util.module_from_spec(spec); spec.loader.exec_module(B)
SEG, starts, frames, TOTAL = B.SEG, B.starts, B.frames, B.TOTAL
fstart = [sum(frames[:i]) for i in range(len(frames))]; NFR = sum(frames)

def pcm(f):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True).stdout
    return struct.unpack(f'<{len(raw)//2}h', raw)
SRC = {'n': pcm(f'{E}/nimrod.mp3'), 'd': pcm(f'{E}/danit.mp3')}
def rms(src, t):
    a = SRC[src]; i0 = int(t * 16000); w = 16000 // 30; s = a[max(0, i0 - w // 2): i0 + w // 2]
    return math.sqrt(sum(x * x for x in s) / len(s)) if s else 0
PEAK = {k: sorted(rms(k, i / 60) for i in range(int(len(v) / 16000 * 60)))[-int(len(v) / 16000 * 60) // 20] for k, v in SRC.items()}
def env(fi):
    t = (fi + .5) / FPS; out = {'n': 0., 'd': 0.}
    for (src, a, b), st in zip(SEG, starts):
        if st <= t < st + (b - a): out[src] = min(1., rms(src, a + t - st) / PEAK[src])
    return out
ENV = [env(i) for i in range(NFR)]
for k in 'nd':
    p = 0
    for e in ENV:
        v = e[k]; p = v if v > p else p * .55 + v * .45; e[k] = round(p, 3)

EXTRA_JS = r'''
const _anim=window.animChar;
window.animChar=function(c,t,talk,mode){
 if(mode!=='dance')return _anim(c,t,talk,mode);
 const b=t*Math.PI*4, ph=c.ph;               // 120 bpm
 c.body.position.y=.75+Math.abs(Math.sin(b/2))*.12; c.body.rotation.y=Math.sin(b/4+ph)*.5; c.body.rotation.z=Math.sin(b/2+ph)*.12;
 c.aL.rotation.z=.3+1.6*(.5+.5*Math.sin(b/2+ph)); c.aR.rotation.z=-.3-1.6*(.5+.5*Math.sin(b/2+ph+Math.PI));
 c.aL.rotation.x=-.4*Math.sin(b/2); c.aR.rotation.x=.4*Math.sin(b/2);
 c.head.rotation.x=-.1+Math.sin(b)*.08; c.head.rotation.z=Math.sin(b/2+ph)*.12;
 c.mo.scale.y=talk?1+talk*5.5:2.5; const bl=((t+ph)%3.9)<.13; c.eL.scale.y=c.eR.scale.y=bl?.12:1;
};
'''

STUDIO_JS = r'''
nameLabels.visible=false;contGroup.visible=false;chairs.forEach(c=>{if(c.label)c.label.visible=false});
document.body.querySelectorAll('*').forEach(e=>{if(e.tagName!=='CANVAS'&&!e.contains(renderer.domElement))e.style.visibility='hidden'});
controls.enabled=true;controls.enableDamping=false;fly=null;
const key=new THREE.SpotLight(0xfff0dd,1.3,40,.42,.6,1);key.position.set(2,11,10);key.target.position.set(0,2,0);scene.add(key,key.target);
const fill=new THREE.PointLight(0xffd0a0,.9,18);fill.position.set(0,4,7);scene.add(fill);
const SM=(c,e,ei,o)=>new THREE.MeshStandardMaterial(Object.assign({color:c,roughness:.5,emissive:e||0,emissiveIntensity:ei||0},o||{}));
const C={};
C.dudi=mkChar({mic:true,shirt:0x16161c,pants:0x16161c,ph:.3});
C.harel=mkChar({shirt:0x22aa66,hair:0x1a120c,mask:true,ph:1.1,skin:0xe0ac69});
C.shahar=mkChar({shirt:0xff5fa8,hair:0x3b2314,long:true,ear:true,ph:2.2});
C.nisso=mkChar({shirt:0xff7a1a,hair:0x120c08,ph:.8,skin:0xe0ac69});
C.liav=mkChar({shirt:0x2b2f8f,pants:0x222222,hair:0x3b2314,ph:1.4,skin:0xf1c27d});
{const cap=new THREE.Mesh(new THREE.BoxGeometry(.7,.14,.7),SM(0xE01F26));cap.position.set(0,.72,0);C.liav.head.add(cap);const br=new THREE.Mesh(new THREE.BoxGeometry(.6,.05,.32),SM(0xE01F26));br.position.set(0,.66,-.45);C.liav.head.add(br);const hood=new THREE.Mesh(new THREE.BoxGeometry(.7,.3,.25),SM(0x23277a));hood.position.set(0,.95,-.25);C.liav.body.add(hood)}
{const g=new THREE.Mesh(new THREE.BoxGeometry(.6,.13,.04),SM(0x050505,0,0,{metalness:.8,roughness:.2}));g.position.set(0,.42,.33);C.nisso.head.add(g);
 const cap=new THREE.Mesh(new THREE.BoxGeometry(.7,.14,.7),SM(0x111111));cap.position.set(0,.72,0);C.nisso.head.add(cap);
 const br=new THREE.Mesh(new THREE.BoxGeometry(.6,.05,.32),SM(0x111111));br.position.set(0,.66,.45);C.nisso.head.add(br);
 const ch=new THREE.Mesh(new THREE.TorusGeometry(.22,.03,6,20),SM(0xFFC24B,0xFFC24B,.5,{metalness:.9}));ch.position.set(0,.72,.24);ch.rotation.x=.3;C.nisso.body.add(ch)}
Object.values(C).forEach(c=>{c.g.position.set(0,.7,0);scene.add(c.g)});
// ---- extraterrestre ----
const AL=mkChar({skin:0x7be36a,shirt:0xc3ccd6,pants:0x8a96a6,noLegs:true,ph:1.7});
AL.eL.geometry=new THREE.BoxGeometry(.22,.26,.03);AL.eR.geometry=new THREE.BoxGeometry(.22,.26,.03);AL.eL.position.x=-.15;AL.eR.position.x=.15;
[-.18,.18].forEach(x=>{const a=new THREE.Mesh(new THREE.CylinderGeometry(.02,.02,.45,6),SM(0x5fbf50));a.position.set(x,.85,0);a.rotation.z=x*1.2;AL.head.add(a);
 const bl=new THREE.Mesh(new THREE.SphereGeometry(.07,12,10),new THREE.MeshBasicMaterial({color:0xfff35a}));bl.position.set(x*1.6,1.07,0);AL.head.add(bl)});
// ---- autruche ----
const OS=new THREE.Group();const fe=SM(0x2a2420),sk=SM(0xe7b49c),wh=SM(0xf4f1ea);
const bod=new THREE.Mesh(new THREE.SphereGeometry(.62,20,16),fe);bod.scale.set(1,.72,1.35);bod.position.y=1.55;OS.add(bod);
const tail=new THREE.Mesh(new THREE.SphereGeometry(.32,12,10),wh);tail.position.set(0,1.75,-.85);OS.add(tail);
const wingL=new THREE.Mesh(new THREE.SphereGeometry(.35,12,10),fe);wingL.scale.set(.35,.7,1.1);wingL.position.set(-.58,1.6,0);OS.add(wingL);const wingR=wingL.clone();wingR.position.x=.58;OS.add(wingR);
const neck=new THREE.Group();neck.position.set(0,1.8,.65);OS.add(neck);
const nk=new THREE.Mesh(new THREE.CylinderGeometry(.07,.1,1.25,10),sk);nk.position.y=.6;neck.add(nk);neck.rotation.x=.18;
const hd=new THREE.Mesh(new THREE.SphereGeometry(.16,14,12),sk);hd.position.set(0,1.3,.05);neck.add(hd);
const bk=new THREE.Mesh(new THREE.ConeGeometry(.07,.26,10),SM(0xf2a33a));bk.rotation.x=Math.PI/2;bk.position.set(0,1.27,.27);neck.add(bk);
[-.1,.1].forEach(x=>{const e=new THREE.Mesh(new THREE.SphereGeometry(.035,8,6),SM(0x050505));e.position.set(x,1.36,.13);neck.add(e)});
const legs=[];[-.22,.22].forEach(x=>{const l=new THREE.Group();l.position.set(x,1.25,0);OS.add(l);const c=new THREE.Mesh(new THREE.CylinderGeometry(.05,.07,1.2,8),sk);c.position.y=-.6;l.add(c);
 const f=new THREE.Mesh(new THREE.BoxGeometry(.16,.06,.3),sk);f.position.set(0,-1.2,.08);l.add(f);legs.push(l)});
// rider + speaker
const RIDER=new THREE.Group();RIDER.add(OS);AL.g.position.set(0,1.32,-.1);AL.g.scale.setScalar(.85);RIDER.add(AL.g);
const spk=new THREE.Group();const sb=new THREE.Mesh(new THREE.BoxGeometry(.5,.7,.45),SM(0x151515));spk.add(sb);
const cone=new THREE.Mesh(new THREE.CircleGeometry(.18,20),SM(0x333333,0x23d5ff,.6));cone.position.z=.231;spk.add(cone);const tw=new THREE.Mesh(new THREE.CircleGeometry(.07,16),SM(0x333333,0xff3df2,.8));tw.position.set(0,.24,.231);spk.add(tw);
spk.position.set(.75,1.55,.1);RIDER.add(spk);
RIDER.scale.setScalar(.95);scene.add(RIDER);
// ---- soucoupe + faisceau ----
const UFO=new THREE.Group();const disc=new THREE.Mesh(new THREE.SphereGeometry(2.2,32,12),SM(0xb8c0cc,0,0,{metalness:.9,roughness:.25}));disc.scale.set(1,.22,1);UFO.add(disc);
const dome=new THREE.Mesh(new THREE.SphereGeometry(.9,24,12,0,Math.PI*2,0,Math.PI/2),new THREE.MeshStandardMaterial({color:0x8af7ff,transparent:true,opacity:.7,emissive:0x2ad3ff,emissiveIntensity:.5}));dome.position.y=.3;UFO.add(dome);
const ul=[];for(let i=0;i<12;i++){const s=new THREE.Mesh(new THREE.SphereGeometry(.12,8,6),new THREE.MeshBasicMaterial({color:0x7CFF5A}));const a=i/12*Math.PI*2;s.position.set(Math.sin(a)*2.05,-.05,Math.cos(a)*2.05);UFO.add(s);ul.push(s)}
scene.add(UFO);
const bh=10;const bgeo=new THREE.ConeGeometry(2.6,bh,32,1,true);bgeo.translate(0,-bh/2,0);const BEAM=new THREE.Mesh(bgeo,coneMat(0x7CFF5A));scene.add(BEAM);
const fans=[];for(let i=0;i<9;i++){const f=mkChar({shirt:[0xE01F26,0xFFC24B,0x2d6cdf,0x22aa66,0x9b30ff,0xff7a1a,0x18c3c3,0xffffff,0xff66cc][i],hair:[0x1a120c,0x3b2314,0x8a5a2b][i%3],long:i%2==0,ph:i*.9,skin:[0xf1c27d,0xe0ac69,0xc68642,0xffdbac][i%4]});
  const a=-.5+i*.125,r=4.8+(i%2)*.9;f.g.position.set(Math.sin(a)*r,0,4.5+Math.cos(a)*r*.5);f.y0=0;f.g.rotation.y=Math.PI+a*.6;f.g.scale.setScalar(.9);scene.add(f.g);fans.push(f)}
window.ST={C,AL,OS,RIDER,UFO,BEAM,ul,legs,neck,wingL,wingR,spk,cone,fans};
window.shot=function(o){
  const T=window.ST, P=o.pos||{};
  ['dudi','harel','shahar','nisso','liav'].forEach(k=>{const c=T.C[k];c.g.visible=k in P;if(P[k]){c.g.position.set(P[k][0],.7,P[k][1]);c.g.rotation.y=P[k][2]||0}});
  T.RIDER.visible='rider' in P;T.fans.forEach(f=>f.g.visible=!!o.fans);mic.visible=!!o.mic;
  T.UFO.visible=o.ufo!=null;T.BEAM.visible=o.beam>0;
  camera.position.set(...o.cam);controls.target.set(...o.look);
  const t=o.t;
  if(P.dudi)animChar(T.C.dudi,t,o.talk,o.dudiMode||'talk');
  if(P.shahar)animChar(T.C.shahar,t,0,o.shaharMode||'sing');
  if(P.nisso)animChar(T.C.nisso,t,0,o.nissoMode||'sing');
  if(P.liav)animChar(T.C.liav,t,0,'sing');
  if(P.harel){animChar(T.C.harel,t,0,'sing');const m=T.C.harel.mask;
    if(o.reveal!=null&&o.reveal>=0){const k=Math.min(1,o.reveal/.55);m.position.set(.9*k,.42+1.6*k,.33+1.2*k);m.rotation.set(-2*k,1.5*k,3*k)}else{m.position.set(0,.42,.33);m.rotation.set(0,0,0)}}
  if(P.rider){const r=P.rider;T.RIDER.position.set(r[0],.7+(o.riderY||0),r[1]);T.RIDER.rotation.y=r[2]||0;
    const dance=o.alienMode==='dance', walk=o.riderY>0.05?0:1;
    const hop=dance?Math.abs(Math.sin(t*Math.PI*2))*.25:0;T.OS.position.y=hop;
    T.legs[0].rotation.x=(dance?.6:.15)*Math.sin(t*(dance?12.6:3));T.legs[1].rotation.x=-T.legs[0].rotation.x;
    T.neck.rotation.x=.18+Math.sin(t*(dance?12.6:2.2))*(dance?.25:.08);T.neck.rotation.z=dance?Math.sin(t*6.3)*.2:0;
    T.wingL.rotation.z=dance?.6*Math.abs(Math.sin(t*6.3)):.05*Math.sin(t*2);T.wingR.rotation.z=-T.wingL.rotation.z;
    T.AL.g.position.y=1.32+hop;animChar(T.AL,t,o.alienTalk||0,o.alienMode||'talk');
    const pulse=.5+.5*Math.abs(Math.sin(t*(dance?12.6:4)));T.cone.scale.setScalar(.9+.25*pulse);T.cone.material.emissiveIntensity=.4+pulse;}
  if(o.ufo!=null){T.UFO.position.set(0,o.ufo,0);T.UFO.rotation.y=t*1.2;T.ul.forEach((s,i)=>s.material.color.setHSL(((t*2+i/12)%1),1,.6))}
  if(o.beam>0){T.BEAM.position.set(0,o.ufo!=null?o.ufo:10,0);T.BEAM.material.uniforms.k.value=.35*o.beam}
  if(o.fans)T.fans.forEach(f=>animChar(f,t,0,'cheer'));
  screenLine=o.screen||'';
  if(o.jump){for(let i=0;i<14;i++){const si=seatOrder[Math.floor(Math.random()*Math.min(146,MAXS))];JUMP[si]=performance.now()}
    if(Math.random()<.5){const si=seatOrder[Math.floor(Math.random()*120)];const[x,y,z]=SEATS[si];const e=emojiSprite(['👏','🕺','👽','🔥'][Math.floor(Math.random()*4)]);e.position.set(x,y+2.4,z);scene.add(e);FLY.push({o:e,t0:performance.now(),type:'em',y0:y+2.4})}}
  chairs.forEach(c=>{if(c.label)c.label.visible=false});nameLabels.visible=false;contGroup.visible=false;
  capHook(t)};
'''

def lerp(a, b, k): return [x + (y - x) * k for x, y in zip(a, b)]
def ease(k): return k * k * (3 - 2 * k)
def S(cam0, cam1, look0, look1, extra=None, **kw):
    def f(lt, d, t):
        k = ease(min(1, lt / d)); o = dict(kw); o.update(cam=lerp(cam0, cam1, k), look=lerp(look0, look1, k), t=t)
        if extra: o.update(extra(lt, d))
        return o
    return f
def descend(lt, d):       # l'autruche descend de la soucoupe
    k = min(1, lt / 1.7); y = 7.5 * (1 - ease(k))
    return {'riderY': y, 'beam': 1 if lt < 2.2 else max(0, 1 - (lt - 2.2) / .6), 'ufo': 9.5}
PLAN = [
    ('studio', S([0, 6, 14], [0, 3.1, 3.9], [0, 2.8, 0], [0, 3.15, 0], pos={'dudi': [0, 0.3]}, screen='🚿?!')),
    ('studio', S([0, 3.4, 2.4], [0, 4.4, 1.4], [0, 3.0, 16], [0, 4.2, 16], fans=True, jump=True, screen='= אתם!')),
    ('studio', S([-4, 6, 16], [4, 5, 14], [0, 2.4, 0], [0, 2.6, 0], pos={'dudi': [0, 0.3]}, dudiMode='dance', fans=True, jump=True, screen='71 👥')),
    ('news',   S([0, 3.4, 8.2], [0, 3.2, 6.6], [0, 3.5, 0], [0, 3.4, 0])),
    ('news',   S([2.4, 3.2, 6.4], [1.7, 3.1, 5.4], [0, 3.4, .4], [0, 3.35, .4])),
    ('studio', S([0, 2.0, 9.5], [0, 2.8, 5.0], [0, 2.4, 0], [0, 2.9, 0], pos={'liav': [0, 0]}, mic=True, screen='😬 ליאב')),
    ('studio', S([1.4, 3.3, 5.6], [0, 3.0, 4.0], [0, 3.1, 0], [0, 3.15, 0], pos={'dudi': [0, 0.3]}, screen='📲')),
    ('studio', S([0, 4.4, 12.5], [0, 3.4, 6.4], [0, 2.6, 0], [0, 2.9, 0], pos={'dudi': [-1.2, .3, .4], 'nisso': [1.2, 0, -.4]}, dudiMode='dance', mic=False, fans=True, jump=True, screen='״אני מזייף״')),
    ('studio', S([0.8, 3.3, 5.0], [0, 3.05, 3.8], [0, 3.1, 0], [0, 3.2, 0], pos={'dudi': [0, 0.3]}, fans=True, screen='👇')),
]

def main(only=None, preview=None):
    F.news_html()
    with sync_playwright() as p:
        b = p.chromium.launch(args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
        st = b.new_page(viewport={'width': 540, 'height': 960}, device_scale_factor=2); F.routes(st); st.add_init_script(F.INIT)
        st.goto('http://local/index.html?demo'); st.wait_for_timeout(3000)
        st.evaluate(F.CHAR_JS + ";0"); st.evaluate(EXTRA_JS + ";0"); st.evaluate(STUDIO_JS + ";0")
        nw = b.new_page(viewport={'width': 1080, 'height': 1920}); F.routes(nw); nw.add_init_script(F.INIT)
        nw.goto('http://local/tools/plateau/news_film.html'); nw.wait_for_function('window.ready===true', timeout=20000)
        for i, (where, fn) in enumerate(PLAN):
            if only is not None and i not in only: continue
            n = frames[i]; d = n / FPS; ff = None
            if not preview:
                tmp = f'{E}/v{i}.tmp.mp4'
                vf = "[0:v]format=yuv420p[bg];[1:v]format=rgba,fade=t=in:st=0:d=0.22:alpha=1[o];[bg][o]overlay=0:0:format=auto,format=yuv420p[v]"
                ff = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'image2pipe', '-framerate', str(FPS), '-c:v', 'mjpeg', '-i', '-',
                                       '-loop', '1', '-framerate', str(FPS), '-i', f'{E}/ov3d{i}.png', '-filter_complex', vf, '-map', '[v]', '-frames:v', str(n),
                                       '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p', '-r', str(FPS), tmp], stdin=subprocess.PIPE)
            rng = [min(n - 1, int(x * n)) for x in preview] if preview else range(n)
            for j in rng:
                gi = fstart[i] + j; t = gi / FPS; lt = j / FPS; e = ENV[gi]
                o = fn(lt, d, t)
                if where == 'news':
                    o['talk'] = e['d']; nw.evaluate('o=>{window.__T=o.t;nshot(o)}', o); img = nw.screenshot(type='jpeg', quality=90)
                else:
                    o['talk'] = e['n']
                    bs = [x for x in B.BURSTS if x <= t]
                    o['showAt'] = (bs[-1] - 1.3) if bs and t - bs[-1] < 6.5 else None
                    st.evaluate("o=>{window.__T=o.t;show=o.showAt!=null?{t0:o.showAt*1000}:null;shot(o)}", o)
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
    if a and a[0] == 'preview': main(preview=[.2, .9])
    elif a and a[0] == 'scenes': main(only=[int(x) for x in a[1:]])
    else: main()
