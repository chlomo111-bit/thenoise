"""Reel crossover « L'ENVELOPPE » The Noise (07/11, lettre ר 3/5)."""
import sys, os, math, subprocess, struct, importlib.util, json
sys.path.insert(0, '/tmp/claude-0/ep4'); sys.path.insert(0, '/tmp/claude-0/ep')
from playwright.sync_api import sync_playwright
import film as F
import film4 as M          # EXTRA_JS, STUDIO_JS, S, lerp, ease
E = '/tmp/claude-0/ep5'; FPS = 30
spec = importlib.util.spec_from_file_location('b1', '/tmp/claude-0/ep/build.py'); B1 = importlib.util.module_from_spec(spec); spec.loader.exec_module(B1)

# ---- timeline (s) ----
CUT = [0, 3.6, 8.0, 12.4, 20.75, 23.6, 28.9, 31.4, 34.9]
VO = [('n1', 0.5), ('n2', 3.75), ('d1', 12.55), ('n3', 20.95)]
TOTAL = CUT[-1]; NF = [round(CUT[i+1]*FPS) - round(CUT[i]*FPS) for i in range(len(CUT)-1)]
FST = [round(c*FPS) for c in CUT[:-1]]
BURSTS = [CUT[2] + 0.8]

def pcm(f):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True).stdout
    return struct.unpack(f'<{len(raw)//2}h', raw)
SRC = {k: pcm(f'{E}/{k}.mp3') for k, _ in VO}
def rms(a, t):
    i0 = int(t*16000); w = 16000//30; s = a[max(0, i0-w//2): i0+w//2]
    return math.sqrt(sum(x*x for x in s)/len(s)) if s else 0
PEAK = {k: sorted(rms(v, i/60) for i in range(int(len(v)/16000*60)))[-max(1, int(len(v)/16000*60)//20)] for k, v in SRC.items()}
def talk(t, who):
    for k, st in VO:
        if (k[0] == who) and st <= t < st + len(SRC[k])/16000: return min(1., rms(SRC[k], t-st)/PEAK[k])
    return 0.
NFR = sum(NF); ENV = []
pn = pd = 0
for i in range(NFR):
    t = (i+.5)/FPS; vn, vd = talk(t, 'n'), talk(t, 'd')
    pn = vn if vn > pn else pn*.55 + vn*.45; pd = vd if vd > pd else pd*.55 + vd*.45
    ENV.append({'n': round(pn, 3), 'd': round(pd, 3)})

EXTRA5 = r'''
{const T=window.ST;const SM=(c,e,ei,o)=>new THREE.MeshStandardMaterial(Object.assign({color:c,roughness:.6,emissive:e||0,emissiveIntensity:ei||0},o||{}));
 // table du jury
 const DESK=new THREE.Group();const top=new THREE.Mesh(new THREE.BoxGeometry(12.5,.12,1.1),SM(0x1b1b22,0,0,{metalness:.4,roughness:.35}));top.position.y=1.15;DESK.add(top);
 const fr=new THREE.Mesh(new THREE.BoxGeometry(12.5,1.05,.08),SM(0xb3121a,0xb3121a,.25));fr.position.set(0,.6,-.5);DESK.add(fr);
 const st=new THREE.Mesh(new THREE.BoxGeometry(12.5,.05,.1),new THREE.MeshBasicMaterial({color:0xFFC24B}));st.position.set(0,1.05,-.56);DESK.add(st);
 DESK.position.set(0,0,7.5);scene.add(DESK);
 // enveloppe crème + cachet rouge
 const ENV=new THREE.Group();const paper=SM(0xf3e6c8,0xf3e6c8,.12,{roughness:.8});
 const pb=new THREE.Mesh(new THREE.BoxGeometry(1.0,.04,.66),paper);ENV.add(pb);
 const fl=new THREE.Mesh(new THREE.CylinderGeometry(.6,.6,.02,3),SM(0xe9d9b4,0xe9d9b4,.1,{roughness:.8}));fl.scale.set(.83,1,.55);fl.rotation.y=Math.PI/6+Math.PI;fl.position.set(0,.031,-.08);ENV.add(fl);
 const seal=new THREE.Mesh(new THREE.CylinderGeometry(.11,.12,.045,24),SM(0xa50f17,0x5a0006,.4,{roughness:.35,metalness:.2}));seal.position.set(0,.06,.02);ENV.add(seal);
 const sr=new THREE.Mesh(new THREE.TorusGeometry(.085,.012,6,20),SM(0xd0303a));sr.rotation.x=Math.PI/2;sr.position.set(0,.085,.02);ENV.add(sr);
 const glow=new THREE.PointLight(0xffe2a8,0,4);glow.position.set(0,.6,0);ENV.add(glow);
 scene.add(ENV);ENV.visible=false;
 // portail + lapin blanc (silhouette)
 const POR=new THREE.Group();const ring=new THREE.Mesh(new THREE.TorusGeometry(1.5,.12,16,64),new THREE.MeshBasicMaterial({color:0xb26bff}));POR.add(ring);
 const ring2=new THREE.Mesh(new THREE.TorusGeometry(1.32,.05,8,64),new THREE.MeshBasicMaterial({color:0x5fe3ff}));POR.add(ring2);
 const disc=new THREE.Mesh(new THREE.CircleGeometry(1.42,48),new THREE.MeshBasicMaterial({color:0x2a0b4a,transparent:true,opacity:.92}));POR.add(disc);
 const sw=[];for(let i=0;i<5;i++){const r=new THREE.Mesh(new THREE.RingGeometry(.25+i*.22,.3+i*.22,40,1,0,Math.PI*1.3),new THREE.MeshBasicMaterial({color:i%2?0x8a4dff:0x41c9ff,transparent:true,opacity:.6,side:THREE.DoubleSide}));r.position.z=.01+i*.002;POR.add(r);sw.push(r)}
 const plight=new THREE.PointLight(0xa070ff,0,9);plight.position.set(0,0,1);POR.add(plight);
 POR.position.set(0,2.4,-.6);scene.add(POR);POR.visible=false;
 const RB=new THREE.Group();const wm=new THREE.MeshBasicMaterial({color:0xffffff});
 const sp=(r,sx,sy,sz,x,y,z,rz)=>{const m=new THREE.Mesh(new THREE.SphereGeometry(r,20,16),wm);m.scale.set(sx,sy,sz);m.position.set(x,y,z);m.rotation.z=rz||0;RB.add(m);return m};
 sp(.42,1.3,.8,.8,0,0,0);            // corps (le long de x)
 sp(.25,1.15,1,1,.55,.36,0);         // tête
 sp(.07,.75,4.2,.5,.47,.86,.07,.32); sp(.07,.75,4.0,.5,.56,.84,-.07,.18);   // longues oreilles
 sp(.13,1,1,1,-.6,.18,0);            // queue
 sp(.16,1.9,.7,.8,-.25,-.32,0,-.2);  // patte arrière
 sp(.08,1.6,.6,.7,.42,-.3,0);        // patte avant
 scene.add(RB);RB.visible=false;
 Object.assign(T,{DESK,ENV,glow,POR,ring,ring2,sw,plight,RB});
 const _shot=window.shot;
 window.shot=function(o){
  T.ENV.visible=!!o.env;if(o.env){const e=o.env;T.ENV.position.set(e[0],e[1],e[2]);T.ENV.rotation.set(e[3]||0,e[4]||0,e[5]||0);T.ENV.scale.setScalar(e[6]||1);T.glow.intensity=o.envGlow||0}
  T.POR.visible=!!o.portal;T.RB.visible=o.rabbit!=null;
  if(o.portal){const k=o.portal;T.POR.scale.setScalar(Math.max(.01,k));T.sw.forEach((r,i)=>r.rotation.z=-o.t*(2+i*.7));T.ring.material.color.setHSL(.75+.05*Math.sin(o.t*3),1,.62);T.plight.intensity=2.2*k}
  if(o.rabbit!=null){const k=o.rabbit;           // 0..1 : saut du lapin vers le portail
    const x=-1.9+1.9*k, y=1.2+1.6*Math.sin(Math.PI*k)+1.2*k, z=2.4-3.0*k;
    T.RB.position.set(x,y,z);T.RB.rotation.set(0,0,.55-1.1*k);T.RB.scale.setScalar(1.7*(k>.85?Math.max(.01,1-(k-.85)/.15):1))}
  _shot(o)}
}
'''

S = M.S
H = lambda a, b, k: [x+(y-x)*k for x, y in zip(a, b)]
def fall(lt, d):     # l'enveloppe tombe en tournoyant sur la table du jury
    k = min(1, lt/1.1); y = 1.24 + 3.6*(1-k)**2
    return {'env': [0.2, y, 7.35, .6*(1-k), lt*4*(1-k), .4*(1-k)], 'envGlow': 1.2}
def held(lt, d):     # Dudi tient la lettre
    return {'env': [0.62, 2.55, .85, -1.1, .2, .1, .55], 'envGlow': .8}
def outro(lt, d):
    p = min(1, lt/.6); k = min(1, max(0, (lt-.6)/1.8))
    return {'portal': p, 'rabbit': k if lt < 2.5 else None}
PLAN = [
    ('studio', S([0.5, 2.25, 8.2], [0.25, 1.95, 7.85], [0.2, 1.24, 7.35], [0.2, 1.24, 7.35], extra=lambda lt, d: {'env': [0.2, 1.24, 7.35, 0, lt*.15, 0], 'envGlow': 1.4}, screen='✉️')),
    ('studio', S([1.2, 3.3, 5.4], [0, 3.05, 3.8], [0, 3.1, 0], [0, 3.2, 0], pos={'dudi': [0, 0.3]}, screen='🎤')),
    ('studio', S([0, 3.4, 2.4], [0, 4.4, 1.4], [0, 3.0, 16], [0, 4.2, 16], fans=True, jump=True, screen='79 👥')),
    ('news',   S([0, 3.4, 8.2], [0, 3.2, 6.6], [0, 3.5, 0], [0, 3.4, 0])),
    ('studio', S([0, 2.7, 10.6], [0, 2.25, 9.6], [0, 2.3, 2], [0, 1.9, 3], pos={'liav': [0, 0]}, mic=True, extra=fall, screen='🎤 ליאב')),
    ('studio', S([0.9, 3.25, 4.6], [0.2, 3.1, 3.6], [0.3, 3.0, 0], [0.3, 3.1, 0], pos={'dudi': [0, 0.3]}, extra=held, screen='✉️?!')),
    ('studio', S([0, 2.6, 9.0], [0, 2.5, 8.3], [0, 2.4, 0], [0, 2.4, 0], extra=outro, screen='🔎')),
    ('studio', S([0, 2.5, 8.3], [0, 2.45, 7.4], [0, 2.4, 0], [0, 2.4, 0], extra=lambda lt, d: {'portal': 1}, screen='🔎')),
]

NEWS = '<div class="flash">⚡ מבזק</div><div class="live"><i></i>LIVE · קומה 24</div>'
TICK = '<div class="tick">✉️ מכתב מסתורי הגיע לאולפן · 👑 הזוכה: hayley645726 · ✅ ליאב בפנים · 🔎 5 עולמות, 5 אותיות ·</div>'
LOW = lambda b: f'<div class="low"><span class="n">דנית · החדשות של The Noise</span><div class="b">{b}</div></div>'
OV = [
 '''<div class="c card" style="top:1180px"><div class="big" style="font-size:96px">המכתב הגיע<br><span class="k">גם אלינו…</span> ✉️</div></div>''',
 '''<div class="c" style="top:280px"><div class="pill">🎤 The Noise</div></div>
    <div class="c card" style="top:1330px"><div class="mid" style="font-size:64px">אתם המתמודדים –<br><span class="k">ואתם השופטים!</span></div></div>''',
 '''<div class="c big" style="top:330px;font-size:100px">אתמול 71<br>היום <span class="k">79</span> 👥</div>''',
 NEWS + '''<div class="c card" style="top:330px"><div class="mid">👑 זוכת ההגרלה</div><div class="big k" style="font-size:84px"><bdi dir="ltr">@hayley645726</bdi></div><div class="mid" style="font-size:56px;margin-top:16px">✅ ליאב עובר את האודישן!</div></div>''' + LOW('+300 🎟️ והכתר! 👑') + TICK,
 '''<div class="c card" style="top:300px"><div class="big" style="font-size:88px">רגע… מה <span class="k">נפל</span><br>על השולחן?! ✉️</div></div>''',
 '''<div class="c card" style="top:300px"><div class="mid" style="font-size:66px">״מועמד סודי יגיע לבמה –<br><span class="k">מעולם אחר</span>״</div></div>
    <div class="c big" style="top:1450px;font-size:96px">מי שלח את זה?! 😱</div>''',
 '''<div></div>''',
 '''<div class="c card" style="top:330px"><div class="mid" style="font-size:58px">אות 3 מתוך 5:</div><div class="big k" style="font-size:230px;line-height:1">״ר״</div></div>
    <div class="c mid" style="top:1080px;font-size:54px">מי שולח את המכתבים?<br>5 עולמות, 5 אותיות 🔎</div>
    <div class="c mid" style="top:1290px;font-size:50px">האות הבאה אצל <span class="k"><bdi dir="ltr">@hasavta.shelanu</bdi></span></div>
    <div class="c" style="top:1430px"><div class="cta" style="font-size:52px">שלחו לחבר שיעזור לכם לפתור 📩</div></div>''',
]
COVER = '''<div style="position:absolute;inset:0;background:linear-gradient(180deg,#0000 20%,#0009 45%,#0000 62%,#000a 100%)"></div>
 <div class="c" style="top:440px"><div class="pill" style="font-size:58px">✉️ פרק מיוחד</div></div>
 <div class="c card" style="top:560px"><div class="big" style="font-size:104px">המכתב הגיע<br><span class="k">גם אלינו…</span></div></div>
 <div class="c" style="top:1180px"><div class="cta" style="font-size:54px">אות 3 מתוך 5 🔎</div></div>'''

def overlays():
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
        for i, h in enumerate(OV):
            pg.set_content(f'<html><head><meta charset="utf-8"><style>{B1.CSS}</style></head><body>{h}</body></html>'); pg.wait_for_timeout(250)
            pg.screenshot(path=f'{E}/ov{i}.png', omit_background=True)
        b.close()
def cover(bg):
    import base64
    d = base64.b64encode(open(bg, 'rb').read()).decode()
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
        pg.set_content(f'<html><head><meta charset="utf-8"><style>{B1.CSS} body{{background:url(data:image/jpeg;base64,{d}) center/cover}}</style></head><body>{COVER}</body></html>'); pg.wait_for_timeout(300)
        pg.screenshot(path=f'{E}/cover.jpg', type='jpeg', quality=92); b.close()
def audio():
    H = '/tmp/claude-0/hymne_v2.mp3'; o = CUT[-2]        # outro
    sp = [(st, st+len(SRC[k])/16000) for k, st in VO]
    duck = '+'.join(f'between(t,{a-0.25:.2f},{b+0.2:.2f})' for a, b in sp)
    fl = [f"[0:a]atrim=0:{o:.2f},asetpts=PTS-STARTPTS,volume='if({duck},0.16,0.55)':eval=frame,afade=t=out:st={o-0.4:.2f}:d=0.4[h1]",
          f"[1:a]atrim=50:{50+TOTAL-o:.2f},asetpts=PTS-STARTPTS,volume=1.5,afade=t=in:d=0.25,afade=t=out:st={TOTAL-o-0.8:.2f}:d=0.8,adelay={int(o*1000)}|{int(o*1000)}[h2]"]
    ins = ['-i', H, '-i', H]; mix = '[h1][h2]'
    for j, (k, st) in enumerate(VO):
        ins += ['-i', f'{E}/{k}.mp3']; fl.append(f"[{j+2}:a]volume=1.2,adelay={int(st*1000)}|{int(st*1000)}[v{j}]"); mix += f'[v{j}]'
    fl.append(f"{mix}amix=inputs={len(VO)+2}:normalize=0,alimiter=limit=0.95,aresample=44100[out]")
    subprocess.run(['ffmpeg', '-y', '-v', 'error', *ins, '-filter_complex', ';'.join(fl), '-map', '[out]', '-t', f'{TOTAL:.2f}', '-c:a', 'aac', '-b:a', '192k', f'{E}/audio.m4a'], check=True)

def main(only=None, preview=None):
    F.news_html()
    with sync_playwright() as p:
        b = p.chromium.launch(args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
        st = b.new_page(viewport={'width': 540, 'height': 960}, device_scale_factor=2); F.routes(st); st.add_init_script(F.INIT)
        st.goto('http://local/index.html?demo'); st.wait_for_timeout(3000)
        st.evaluate(F.CHAR_JS + ";0"); st.evaluate(M.EXTRA_JS + ";0"); st.evaluate(M.STUDIO_JS + ";0"); st.evaluate(EXTRA5 + ";0")
        nw = b.new_page(viewport={'width': 1080, 'height': 1920}); F.routes(nw); nw.add_init_script(F.INIT)
        nw.goto('http://local/tools/plateau/news_film.html'); nw.wait_for_function('window.ready===true', timeout=20000)
        for i, (where, fn) in enumerate(PLAN):
            if only is not None and i not in only: continue
            n = NF[i]; d = n/FPS; ff = None
            if not preview:
                tmp = f'{E}/v{i}.tmp.mp4'
                vf = "[0:v]format=yuv420p[bg];[1:v]format=rgba,fade=t=in:st=0:d=0.22:alpha=1[o];[bg][o]overlay=0:0:format=auto,format=yuv420p[v]"
                ff = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'image2pipe', '-framerate', str(FPS), '-c:v', 'mjpeg', '-i', '-',
                     '-loop', '1', '-framerate', str(FPS), '-i', f'{E}/ov{i}.png', '-filter_complex', vf, '-map', '[v]', '-frames:v', str(n),
                     '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p', '-r', str(FPS), tmp], stdin=subprocess.PIPE)
            rng = [min(n-1, int(x*n)) for x in preview] if preview else range(n)
            for j in rng:
                gi = FST[i]+j; t = gi/FPS; lt = j/FPS; e = ENV[gi]; o = fn(lt, d, t)
                if where == 'news':
                    o['talk'] = e['d']; nw.evaluate('o=>{window.__T=o.t;nshot(o)}', o); img = nw.screenshot(type='jpeg', quality=90)
                else:
                    o['talk'] = e['n']; bs = [x for x in BURSTS if x <= t]
                    o['showAt'] = (bs[-1]-1.3) if bs and t-bs[-1] < 6.5 else None
                    st.evaluate("o=>{window.__T=o.t;show=o.showAt!=null?{t0:o.showAt*1000}:null;shot(o)}", o); img = st.screenshot(type='jpeg', quality=90)
                if ff: ff.stdin.write(img)
                else: open(f'{E}/pv{i}_{j}.jpg', 'wb').write(img)
            if ff:
                ff.stdin.close(); ff.wait()
                if ff.returncode: raise SystemExit(f'ffmpeg scene {i}')
                os.replace(f'{E}/v{i}.tmp.mp4', f'{E}/v{i}.mp4')
            print('scene', i, 'ok', flush=True)
        b.close()
    if only is None and not preview:
        open(f'{E}/l.txt', 'w').write(''.join(f'file v{i}.mp4\n' for i in range(len(PLAN))))
        subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-i', f'{E}/l.txt', '-i', f'{E}/audio.m4a', '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'copy', '-shortest', '-movflags', '+faststart', f'{E}/final.mp4'], check=True)
        print('final ok', flush=True)

if __name__ == '__main__':
    a = sys.argv[1:]
    if a and a[0] == 'prep': overlays(); audio(); print(json.dumps({'total': TOTAL, 'nf': NF}))
    elif a and a[0] == 'preview': main(preview=[.15, .85])
    elif a and a[0] == 'scenes': main(only=[int(x) for x in a[1:]])
    else: main()
