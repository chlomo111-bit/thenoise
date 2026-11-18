"""The Noise 18.11 soir — « הזיופים הכי גרועים » פרק 1 : le candidat masqué en oncle de mariage qui chante faux.
Plans : uncle (gros plan, décor de mariage 💍🥂, invités derrière) | flee (plan large, les invités fuient) |
        judge (UN juge se bouche les oreilles, sans chute) | button (gros plan : sa main descend vers le gros bouton rouge, s'arrête juste avant) | end.
Usage : DSF=1.4 FPS=10 python3 film.py <node_modules> <dossier_sortie> <plan> <durée_s>"""
import sys, os, math
from playwright.sync_api import sync_playwright
NM, OUT, SHOT, DUR = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4])
os.makedirs(OUT, exist_ok=True); FPS = int(os.environ.get('FPS', 10)); START = float(os.environ.get('START', 0))
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(f'{D}/carrousel_shofet_1211.py').read(); src = src[:src.rindex('def main')]
g = {'__name__': 'x', '__file__': f'{D}/carrousel_shofet_1211.py'}
sys.argv = sys.argv[:3]; exec(src.replace('os.makedirs(OUT, exist_ok=True)', ''), g)
CHAR_JS, STUDIO_JS, EXTRA, JUDGES, POSE, routes, INIT = (g[k] for k in ('CHAR_JS', 'STUDIO_JS', 'EXTRA', 'JUDGES', 'POSE', 'routes', 'INIT'))
def lerp(a, b, k): return [x + (y - x) * k for x, y in zip(a, b)]
def ease(k): k = max(0, min(1, k)); return k * k * (3 - 2 * k)
XJ = 1.7
FALL = float(os.environ.get('FALL', 1.0))

def plan(t):
    if SHOT == 'uncle':
        k = ease(t / max(DUR, 2.5))
        cam = lerp([.35, 3.0, 4.0], [.75, 3.2, 5.6], k)
        return dict(singer=True, notes=True, fans=True, cam=cam, look=[0, 2.75, 0], turn=[0] * 4, screen='💍 מזל טוב'), 'uncle'
    if SHOT == 'flee':
        k = ease(t / max(DUR, 2.4))
        return dict(singer=True, notes=True, fans=True, cam=lerp([-.4, 6.2, 11.0], [.4, 5.4, 10.2], k), look=[0, 1.6, 3.6], turn=[0] * 4, screen='💍 מזל טוב'), 'flee'
    if SHOT == 'judge':
        k = ease(t / 3.0)
        cam = lerp([XJ + .3, 2.7, 12.4], [XJ + .35, 2.55, 13.4], k)
        return dict(cam=cam, look=[XJ, 1.8, 8.9], turn=[1, 1, 1, 1], em=[2]), 'judge'
    if SHOT == 'button':
        k = ease(t / max(DUR, 3))
        cam = lerp([XJ + .9, 2.6, 11.6], [XJ + .35, 2.15, 10.6], k)
        return dict(cam=cam, look=lerp([XJ, 1.7, 9.4], [XJ - .2, 1.35, 9.75], k), turn=[1, 1, 1, 1]), 'button'
    a = .25 + t * .09
    return dict(singer=True, notes=True, cam=[math.sin(a) * 5.2, 3.4, math.cos(a) * 5.2 + .5], look=[0, 2.6, 0], turn=[0] * 4, screen='💍 מזל טוב'), 'end'

EXTRA_POSE = r'''o=>{const T=window.MASK,JD=window.JUDGE,ST=window.STUDIO;
 if(!window.__W){window.__W=[];['💍','🥂','💐','🎉','🥂','💍','🎊','💐'].forEach(e=>{const s=emojiSprite(e);scene.add(s);window.__W.push(s)});
   const M=(c,e)=>new THREE.MeshStandardMaterial({color:c,roughness:.35,emissive:e||0,emissiveIntensity:.5});
   const btn=new THREE.Group();const base=new THREE.Mesh(new THREE.CylinderGeometry(.42,.48,.22,32),M(0x222228));btn.add(base);
   const cap=new THREE.Mesh(new THREE.CylinderGeometry(.32,.34,.2,32),M(0xe01f26,0x900008));cap.position.y=.2;btn.add(cap);
   const ped=new THREE.Mesh(new THREE.BoxGeometry(.8,1.3,.8),M(0x1a1030));ped.position.y=-.75;btn.add(ped);
   btn.position.set(XJ-.15,1.45,10.0);scene.add(btn);window.__BTN=btn;
   const tie=new THREE.Mesh(new THREE.BoxGeometry(.5,.18,.12),M(0xe01f26,0x600004));window.__TIE=tie;T.X.g.add(tie);tie.position.set(0,2.05,.42);}
 // décor de mariage qui flotte autour du chanteur
 window.__W.forEach((s,i)=>{const a=o.t*.5+i*.785,r=2.6+(i%2)*.6;s.visible=o.mode!=='judge'&&o.mode!=='button';s.position.set(Math.sin(a)*r,3.4+Math.sin(o.t*1.3+i)*.35+(i%3)*.4,Math.cos(a)*r*.5-.8);s.scale.setScalar(.6)});
 window.__BTN.visible=o.mode==='button'||o.mode==='judge';
 if(o.singer){T.X.body.rotation.z=Math.sin(o.t*9)*.14;T.X.head.rotation.z=Math.sin(o.t*7)*.18;T.X.head.rotation.x=-.3+Math.sin(o.t*5)*.08;T.X.aR.rotation.set(-2.6+Math.sin(o.t*6)*.3,0,.3);T.X.aL.rotation.set(0,0,-2.5+Math.sin(o.t*8)*.3);
   T.NOTES.forEach((s,i)=>{s.visible=true;const a=o.t*1.4+i*.63,r=1.0+(i%3)*.35;s.position.set(Math.sin(a)*r,2.5+((o.t*1.4+i*.37)%2.0),Math.cos(a)*r*.6+.7)})}
 // invités : dansent (uncle), puis s'enfuient vers les côtés en courant (flee), partis (end)
 if(ST&&ST.fans){ST.fans.forEach((f,i)=>{if(!f.p0)f.p0=f.g.position.clone();const side=(f.p0.x>=0?1:-1);
   let k=o.mode==='flee'?Math.max(0,o.lt-.3-(i%4)*.12)/1.6:(o.mode==='end'?9:0);k=Math.min(k,4);
   f.g.visible=o.mode==='uncle'||o.mode==='flee';
   f.g.position.set(f.p0.x+side*k*k*2.2,f.p0.y+(k>0?Math.abs(Math.sin(o.t*14+i))*.25:0),f.p0.z+k*1.5);
   if(k>0){f.g.rotation.y=side*Math.PI/2;f.aL.rotation.set(Math.sin(o.t*14+i)*1.1,0,-2.9);f.aR.rotation.set(-Math.sin(o.t*14+i)*1.1,0,2.9);f.mo&&f.mo.scale.set(1,6,1)}})}
 const j=JD.J[2];
 if(o.mode==='judge'||o.mode==='button'){j.head.rotation.z=Math.sin(o.t*16)*.15;j.mo.scale.set(1,6+Math.sin(o.t*20)*1.5,1);
   j.aL.rotation.set(0,0,-3.25);j.aR.rotation.set(0,0,3.25);
   const e=JD.EM[2];e.visible=o.mode==='judge';e.position.set(XJ-.8,3.45,9.1);e.scale.setScalar(.8)}
 if(o.mode==='button'){const k=Math.min(1,o.lt/2.6);const kk=k*k*(3-2*k);const tr=Math.sin(o.t*38)*.04*kk;
   // la main droite quitte l'oreille et descend vers le bouton, puis tremble juste au-dessus
   j.aR.rotation.set(-1.25*kk+tr,0,3.25*(1-kk)+.15*kk);j.mo.scale.set(1.2,2+kk*3,1);j.head.rotation.x=.35*kk;
   window.__BTN.children[1].material.emissiveIntensity=.4+.5*Math.abs(Math.sin(o.t*6))}
}'''.replace('XJ', str(XJ))

with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    pg = b.new_page(viewport={'width': 540, 'height': 960}, device_scale_factor=float(os.environ.get('DSF', 1.5))); routes(pg); pg.add_init_script(INIT)
    errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto('http://local/index.html?demo'); pg.wait_for_timeout(4000)
    for js in (CHAR_JS, STUDIO_JS, EXTRA, JUDGES): pg.evaluate(js + ";0")
    pg.add_style_tag(content='#ov{display:none!important}')
    only = os.environ.get('ONLY')
    n = int(round(DUR * FPS)); i0 = int(round(START * FPS))
    for i in range(i0, n):
        if only and str(i) not in only.split(','): continue
        t = i / FPS; o, mode = plan(t); o['t'] = t + 1.3; o['lt'] = t; o['mode'] = mode; o['fall'] = FALL
        pg.evaluate(POSE, o); pg.evaluate(EXTRA_POSE, o); pg.evaluate('()=>renderer.render(scene,camera)')
        pg.screenshot(path=f'{OUT}/f{i:04d}.jpg', type='jpeg', quality=90)
    print(SHOT, 'images', n, 'erreurs', errs[:5]); b.close()
