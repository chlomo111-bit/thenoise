"""The Noise 18.11 (format A, jour principal) « תו אחד… בום! » : filme un plan du plateau 3D, sans texte.
Plans : boom (gros plan du candidat masqué : son faux pète le micro, gerbe 💥 dès l'image 0) |
        judge (UN juge en gros plan qui se bouche les oreilles puis bascule en arrière hors du fauteuil) |
        end (candidat qui continue à chanter, fier, plan qui tourne).
Plateau éclairé normalement (pas de lumière baissée : image 1 lumineuse).
Usage : DSF=1.5 FPS=10 python3 film.py <node_modules> <dossier_sortie> <plan> <durée_s>  (START=s pour décaler)"""
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
    if SHOT == 'boom':
        sh = math.exp(-t * 2.5) * .14
        k = ease(t / max(DUR, 2.4))
        cam = lerp([.45, 3.0, 3.7], [.8, 3.15, 4.6], k); cam = [cam[0] + math.sin(t * 41) * sh, cam[1] + math.cos(t * 37) * sh, cam[2]]
        return dict(singer=True, notes=True, cam=cam, look=[0, 2.8, 0], turn=[0] * 4, screen='💥❌'), 'boom'
    if SHOT == 'judge':
        k = ease(t / 3.0)
        cam = lerp([XJ + .3, 2.7, 12.2], [XJ + .4, 2.5, 13.2], k)
        fk = max(0, t - FALL)
        sh = math.exp(-fk * 4) * .1 if fk > .45 else 0
        cam = [cam[0] + math.sin(t * 43) * sh, cam[1] + math.cos(t * 39) * sh, cam[2]]
        return dict(cam=cam, look=[XJ, 1.8, 8.9], turn=[1, 1, 1, 1], em=[2]), 'judge'
    a = .25 + t * .09
    return dict(singer=True, notes=True, fans=True, cam=[math.sin(a) * 5.2, 3.4, math.cos(a) * 5.2 + .5], look=[0, 2.6, 0], turn=[0] * 4, screen='🎤 במה'), 'end'

EXTRA_POSE = r'''o=>{const T=window.MASK,JD=window.JUDGE;
 if(!window.__B){window.__B=[];for(let i=0;i<14;i++){const s=emojiSprite(i%3==0?'💥':(i%3==1?'✨':'❌'));s.visible=false;scene.add(s);window.__B.push(s)}
   window.__S=[];for(let i=0;i<5;i++){const s=emojiSprite('💫');s.visible=false;scene.add(s);window.__S.push(s)}}
 const mic=[0.0,3.05,.75];
 window.__B.forEach((s,i)=>{s.visible=false});window.__S.forEach(s=>s.visible=false);
 if(o.singer){T.X.body.rotation.z=Math.sin(o.t*9)*.14;T.X.head.rotation.z=Math.sin(o.t*7)*.18;T.X.head.rotation.x=-.3+Math.sin(o.t*5)*.08;T.X.aR.rotation.set(-2.6+Math.sin(o.t*6)*.3,0,.3);T.X.aL.rotation.set(0,0,-2.5+Math.sin(o.t*8)*.3);
   T.NOTES.forEach((s,i)=>{s.visible=true;const a=o.t*1.4+i*.63,r=1.0+(i%3)*.35;s.position.set(Math.sin(a)*r,2.5+((o.t*1.4+i*.37)%2.0),Math.cos(a)*r*.6+.7)})}
 if(o.mode==='boom'){const bt=o.lt+.45; // gerbe déjà partie à l'image 0
   if(!window.__BIG){window.__BIG=emojiSprite('💥');scene.add(window.__BIG)}
   const B=window.__BIG;B.visible=o.lt<.9;B.position.set(mic[0]+.1,mic[1]+.1,mic[2]+.6);B.scale.setScalar(1.1*(1-Math.min(1,o.lt/.9))+.4);
   window.__B.forEach((s,i)=>{const a=i*2.399,el=(i%5-2)*.35,sp=1.0+(i%4)*.35,r=Math.min(2.8,bt*sp*1.5);
     s.visible=bt<2.0;s.position.set(mic[0]+Math.cos(a)*r,mic[1]+Math.sin(a)*r*.75+el*.2,mic[2]+.4+Math.sin(a*1.7)*.3);
     s.scale.setScalar((i%3==0?.7:.4))})}
 else if(window.__BIG)window.__BIG.visible=false;
 if(o.mode==='judge'){const j=JD.J[2];const fk=Math.max(0,o.lt-o.fall);const f=Math.min(1,fk/.45);
   j.head.rotation.z=Math.sin(o.t*16)*.18*(1-f);j.mo.scale.set(1,7+Math.sin(o.t*20)*1.5,1);
   // éjecté du fauteuil : il saute, tourne sur lui-même et retombe assis par terre devant le fauteuil, sonné
   const sp=Math.min(1,fk/1.1);
   const up=Math.min(1,sp/.55),dn=Math.max(0,(sp-.55)/.45);j.g.position.y=.3+1.1*Math.sin(up*Math.PI/2)-dn*dn*1.8; const zz=dn*dn*(3-2*dn);j.g.position.z=-.1-zz*JZ; j.g.rotation.y=Math.PI+up*Math.PI*2;j.g.rotation.z=Math.sin(up*Math.PI)*.5; j.g.rotation.x=0;
   j.aL.rotation.set(0,0,-3.25*(1-f)-f*2.2);j.aR.rotation.set(0,0,3.25*(1-f)+f*2.2);
   const e=JD.EM[2];e.position.set(XJ-.75,3.9,8.9);e.scale.setScalar(.8);
   window.__S.forEach((s,i)=>{s.visible=fk>1.1;const a=o.t*4+i*1.25;s.position.set(XJ+Math.cos(a)*.7,1.45+Math.sin(a*1.3)*.15,8.6+1.3+Math.sin(a)*.3);s.scale.setScalar(.45)})}
}'''.replace('XJ', str(XJ)).replace('JZ', os.environ.get('JZ','1.3'))

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
