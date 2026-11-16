"""The Noise 16.11 (format A) « זיוף בשידור חי » : filme un plan du plateau 3D, sans texte, à 10 i/s.
Plans : sing (candidat masqué qui chante faux, gros plan) | judge (UN juge qui se bouche les oreilles puis se retourne) | end (candidat + public).
Réutilise film_masque_1011.py + JUDGES/POSE de carrousel_shofet_1211.py.
Usage : DSF=1.5 python3 film.py <node_modules> <dossier_sortie> <plan> <durée_s>"""
import sys, os, math
from playwright.sync_api import sync_playwright
NM, OUT, SHOT, DUR = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4])
os.makedirs(OUT, exist_ok=True); FPS = int(os.environ.get('FPS', 10))
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(f'{D}/carrousel_shofet_1211.py').read(); src = src[:src.rindex('def main')]
g = {'__name__': 'x', '__file__': f'{D}/carrousel_shofet_1211.py'}
sys.argv = sys.argv[:3]; exec(src.replace('os.makedirs(OUT, exist_ok=True)', ''), g)
CHAR_JS, STUDIO_JS, EXTRA, JUDGES, POSE, routes, INIT = (g[k] for k in ('CHAR_JS', 'STUDIO_JS', 'EXTRA', 'JUDGES', 'POSE', 'routes', 'INIT'))
def lerp(a, b, k): return [x + (y - x) * k for x, y in zip(a, b)]
def ease(k): k = max(0, min(1, k)); return k * k * (3 - 2 * k)
XJ = 1.7  # juge 3 (le choqué), fauteuil n°3

def plan(t):
    if SHOT == 'sing':
        sh = math.exp(-t * 3) * .12  # secousse dès l'image 0
        k = ease(t / DUR)
        cam = lerp([.5, 3.1, 4.0], [.9, 3.2, 5.0], k); cam = [cam[0] + math.sin(t * 41) * sh, cam[1] + math.cos(t * 37) * sh, cam[2]]
        return dict(singer=True, notes=True, cam=cam, look=[0, 2.75, 0], turn=[0] * 4, screen='🎶❌'), 'sing'
    if SHOT == 'judge':
        turn = 1 - ease((t - float(os.environ.get('TURN', 1.1))) / .6)  # le fauteuil lui tourne le dos
        k = ease(t / DUR)
        cam = lerp([XJ + .3, 2.7, 11.3], [XJ + .45, 2.85, 12.2], k)
        return dict(cam=cam, look=[XJ, 2.1, 8.6], turn=[1, 1, turn, 1], em=[2] if turn > .6 else []), 'judge'
    a = .18 + t * .08
    return dict(singer=True, notes=True, cam=[math.sin(a) * 4.8, 3.3, math.cos(a) * 4.8 + .4], look=[0, 2.5, 0], turn=[0] * 4, screen='🎤 במה'), 'end'

EXTRA_POSE = r'''o=>{const T=window.MASK,JD=window.JUDGE;
 if(!window.__L){window.__L=[];scene.traverse(n=>{if(n.isHemisphereLight||(n.isPointLight&&n.intensity==1.6))window.__L.push([n,n.intensity])})}
 window.__L.forEach(([n,v])=>n.intensity=o.singer?v*.35:v);
 if(o.singer){T.X.body.rotation.z=Math.sin(o.t*9)*.14;T.X.head.rotation.z=Math.sin(o.t*7)*.18;T.X.head.rotation.x=-.25+Math.sin(o.t*5)*.08;T.X.aR.rotation.set(-2.6+Math.sin(o.t*6)*.3,0,.3);
   T.NOTES.forEach((s,i)=>{s.visible=true;const a=o.t*1.4+i*.63,r=1.0+(i%3)*.35;s.position.set(Math.sin(a)*r,2.5+((o.t*1.4+i*.37)%2.0),Math.cos(a)*r*.6+.7)})}
 if(o.mode==='judge'){const j=JD.J[2];j.head.rotation.z=Math.sin(o.t*16)*.18;j.head.rotation.x=-.1;j.mo.scale.set(.9,6+Math.sin(o.t*20)*1.5,1)}
}'''

with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    pg = b.new_page(viewport={'width': 540, 'height': 960}, device_scale_factor=float(os.environ.get('DSF', 1.5))); routes(pg); pg.add_init_script(INIT)
    errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto('http://local/index.html?demo'); pg.wait_for_timeout(4000)
    for js in (CHAR_JS, STUDIO_JS, EXTRA, JUDGES): pg.evaluate(js + ";0")
    pg.add_style_tag(content='#ov{display:none!important}')
    for i in range(int(round(DUR * FPS))):
        t = i / FPS; o, mode = plan(t); o['t'] = t + 1.3; o['mode'] = mode
        pg.evaluate(POSE, o); pg.evaluate(EXTRA_POSE, o)
        pg.screenshot(path=f'{OUT}/f{i:04d}.jpg', type='jpeg', quality=90)
    print(SHOT, 'images', i + 1, 'erreurs', errs[:5]); b.close()
