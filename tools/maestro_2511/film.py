"""The Noise 23.11 « מאסטרו קול » : המאסטרו (chef/juge 3D) parle sur le plateau ; bouche calée sur l'amplitude de la voix (AMP json, 30 valeurs/s).
Usage : AMP=amp.json DUR=18 FPS=15 DSF=1.2 python3 film.py <node_modules> <dossier_sortie>"""
import sys, os, math, json
from playwright.sync_api import sync_playwright
NM, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True); FPS = int(os.environ.get('FPS', 15)); DUR = float(os.environ.get('DUR', 18))
AMP = json.load(open(os.environ['AMP'])) if os.environ.get('AMP') else []
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(f'{D}/carrousel_shofet_1211.py').read(); src = src[:src.rindex('def main')]
g = {'__name__': 'x', '__file__': f'{D}/carrousel_shofet_1211.py'}
sys.argv = sys.argv[:3]; exec(src.replace('os.makedirs(OUT, exist_ok=True)', ''), g)
CHAR_JS, STUDIO_JS, EXTRA, JUDGES, routes, INIT = (g[k] for k in ('CHAR_JS', 'STUDIO_JS', 'EXTRA', 'JUDGES', 'routes', 'INIT'))
def lerp(a, b, k): return [x + (y - x) * k for x, y in zip(a, b)]
def ease(k): k = max(0, min(1, k)); return k * k * (3 - 2 * k)
# plans de caméra (t en s) : [cam, look] ; la caméra bouge en continu
KEYS = [(0, [-.8, 3.0, 3.8], [-1, 2.6, 0]), (2.6, [-1.7, 2.9, 3.4], [-1, 2.7, 0]), (6, [.0, 2.7, 3.9], [-1, 2.6, 0]),
        (10, [-1.5, 3.4, 4.5], [-1, 2.5, 0]), (13, [-1, 2.9, 3.3], [-1, 2.7, 0]), (16, [-.6, 2.9, 3.6], [-1, 2.7, 0]), (60, [-1, 2.9, 3.8], [-1, 2.7, 0])]
def cam(t):
    for (a, ca, la), (b, cb, lb) in zip(KEYS, KEYS[1:]):
        if t <= b:
            k = ease((t - a) / (b - a)); return lerp(ca, cb, k), lerp(la, lb, k)
    return KEYS[-1][1], KEYS[-1][2]
MAESTRO = r'''
{const M=(c,e)=>new THREE.MeshStandardMaterial({color:c,roughness:.5,emissive:e||0,emissiveIntensity:e?.3:0});
 const X=mkChar({shirt:0x15121c,pants:0x0b0b10,hair:0xb8b8c6,long:false,ph:.5});X.g.position.set(-1,.7,0);scene.add(X.g);
 const bow=new THREE.Mesh(new THREE.BoxGeometry(.5,.22,.1),M(0xe01f26,0x600000));bow.position.set(0,1.6,.4);X.body.add(bow);
 const lap1=new THREE.Mesh(new THREE.BoxGeometry(.22,.9,.06),M(0xffc24b,0x6a4500));lap1.position.set(-.3,.9,.42);lap1.rotation.z=.15;X.body.add(lap1);
 const lap2=lap1.clone();lap2.position.x=.3;lap2.rotation.z=-.15;X.body.add(lap2);
 const bat=new THREE.Mesh(new THREE.CylinderGeometry(.03,.03,1.1,8),M(0xffffff,0xffffff));bat.position.set(0,-.7,.1);X.aR.add(bat);bat.rotation.x=1.4;
 const E=['🎙️','🦴','🔊','😖','🎵','👂','📩','🎤'].map(e=>{const s=emojiSprite(e);s.visible=false;scene.add(s);return s});
 window.MAE={X,E};
 try{key.intensity=.9;fill.intensity=.7}catch(e){}
}
'''
POSE = r'''o=>{const T=window.MASK,JD=window.JUDGE,A=window.MAE,X=A.X,t=o.t;
 T.X.g.visible=false;T.ring.visible=false;T.beam.material.opacity=0;T.ENV.visible=false;T.NOTES.forEach(s=>s.visible=false);
 JD.J.forEach(j=>{j.g.visible=false});JD.EM.forEach(s=>s.visible=false);JD.NUM.forEach(s=>s.visible=false);JD.HEARTS.forEach(s=>s.visible=false);
 shot({t:t,cam:o.cam,look:o.look,who:'none',fans:false,screen:''});
 const a=o.amp;
 X.g.visible=true;X.g.position.x=-1;X.g.position.y=.7+Math.abs(Math.sin(t*5))*.05*(a>.15?1:.3);X.g.rotation.y=Math.sin(t*1.3)*.25;
 X.body.rotation.z=Math.sin(t*3.1)*.06;X.head.rotation.z=Math.sin(t*2.3)*.1*(.4+a);X.head.rotation.x=-.05+a*.18;
 X.mo.scale.set(1.2,1+a*10,1);
 const ph=Math.sin(t*4.2);
 X.aR.rotation.set(-1.8+Math.sin(t*6)*.5*(.3+a),0,.5+Math.cos(t*4)*.3);   // baguette
 X.aL.rotation.set(-1.2+ph*.5,0,-.7-a*.8);                               // geste expressif
 if(o.hit){X.aL.rotation.set(0,0,-2.6);X.aR.rotation.set(0,0,2.6)}
 // emojis d'illustration (liste de [index,x,y,z,scale])
 A.E.forEach((s,i)=>{const e=o.em&&o.em.find(q=>q[0]===i);s.visible=!!e;if(e){const w=1+Math.sin(t*9+i)*.06;s.position.set(e[1],e[2]+Math.sin(t*3+i)*.08,e[3]);s.scale.setScalar(e[4]*w)}});
 capHook&&capHook(t)}'''
# illustrations selon le fait : (t0,t1,[[idx,x,y,z,scale]])
EM = [(0, 99, [])]  # 24.11 : plus de sprites 3D (les emojis sont dans le texte, ils chevauchaient les mots)
if os.environ.get('STORY'):
    EM = [(0, 4.3, [[5, 0.1, 3.9, .9, 1.0], [7, -2.1, 3.5, .8, .8]]), (4.3, 99, [[5, 0.1, 3.9, .9, 1.2], [4, -2.1, 3.6, .8, .7]])]
with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    pg = b.new_page(viewport={'width': 540, 'height': 960}, device_scale_factor=float(os.environ.get('DSF', 1.2))); routes(pg); pg.add_init_script(INIT)
    errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto('http://local/index.html?demo', wait_until='domcontentloaded', timeout=90000); pg.wait_for_timeout(4000)
    for js in (CHAR_JS, STUDIO_JS, EXTRA, JUDGES, MAESTRO): pg.evaluate(js + ';0')
    pg.add_style_tag(content='#ov{display:none!important}')
    only = os.environ.get('ONLY'); n = int(round(DUR * FPS))
    for i in range(n):
        if only and str(i) not in only.split(','): continue
        t = i / FPS
        k = min(len(AMP) - 1, int(t * 30)) if AMP else 0
        amp = max(AMP[max(0, k - 1):k + 2]) if AMP else .3
        c, l = cam(t)
        em = next((e for a0, a1, e in EM if a0 <= t < a1), [])
        o = dict(t=t + 1.3, cam=c, look=l, amp=amp, em=em, hit=False)
        pg.evaluate('(o)=>{try{(%s)(o)}catch(e){window.__e=String(e)}}' % POSE.strip(), o)
        pg.evaluate('()=>renderer.render(scene,camera)')
        pg.screenshot(path=f'{OUT}/f{i:04d}.jpg', type='jpeg', quality=88)
    print('images', n, 'erreurs', errs[:5], pg.evaluate('window.__e||null')); b.close()
