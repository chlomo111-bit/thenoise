"""The Noise – carrousel 12.11 « איזה שופט אתם? » : 7 slides 1080×1350 tirées du plateau 3D (index.html?demo)
avec le candidat masqué de film_masque_1011.py et 4 juges assis dans les fauteuils rouges retournés.
Usage : python3 tools/carrousel_shofet_1211.py <node_modules> <dossier_sortie>   (ONLY=1,3 pour quelques slides)"""
import sys, os, re
from playwright.sync_api import sync_playwright
NM, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'film_masque_1011.py')).read()
src = src[:src.index('def main')]
g = {'__name__': 'x', 'sys': sys}
exec(src, g)
CHAR_JS, STUDIO_JS, EXTRA, routes, INIT = g['CHAR_JS'], g['STUDIO_JS'], g['EXTRA'], g['routes'], g['INIT']

JUDGES = r'''
{const J=[];const cfg=[
  {shirt:0xff7ab6,hair:0x2b1a12,ph:.2},                  // 1 le gentil
  {shirt:0x111116,hair:0x0b0b0b,long:true,ear:true,ph:1}, // 2 la dure
  {shirt:0x2d6cdf,hair:0x8a5a2b,ph:2},                   // 3 le choqué
  {shirt:0xFFC24B,hair:0x3b2314,long:true,ph:3}];        // 4 celle qui se retourne quand même
 cfg.forEach((c,i)=>{const j=mkChar(Object.assign({noLegs:true},c));j.g.position.set(0,.3,-.1);j.g.rotation.y=Math.PI;chairs[i].g.add(j.g);J.push(j)});
 const EM=['😇','❌','😱','🔄'].map(e=>{const s=emojiSprite(e);s.visible=false;scene.add(s);return s});
 const NUM=['1','2','3','4'].map(e=>{const s=emojiSprite(e+'️⃣');s.visible=false;scene.add(s);return s});
 const HEARTS=[];for(let i=0;i<6;i++){const s=emojiSprite('💖');s.visible=false;scene.add(s);HEARTS.push(s)}
 window.JUDGE={J,EM,NUM,HEARTS};
 try{key.intensity=1.8;fill.intensity=1.6}catch(e){}
 const jl=new THREE.PointLight(0xfff2e0,1.6,16);jl.position.set(0,5,13);scene.add(jl);
 const amb=new THREE.HemisphereLight(0xdfe4ff,0x403040,.9);scene.add(amb);
}
'''

POSE = r'''o=>{window.__T=o.t;const T=window.MASK,JD=window.JUDGE;
 T.X.g.visible=!!o.singer;T.X.g.position.y=.7;T.X.g.rotation.y=0;if(o.singer){animChar(T.X,o.t,0,'sing');T.X.body.rotation.z=.12;T.X.head.rotation.z=-.15}
 T.aura.intensity=.3;T.ring.visible=!!o.singer;T.beam.material.opacity=0;T.ENV.visible=false;
 T.NOTES.forEach((s,i)=>{s.visible=!!o.notes&&i<6;const a=i*1.05+.5,r=2.0+(i%2)*.5;s.position.set(Math.sin(a)*r,2.6+((i*.37)%2.2),Math.cos(a)*r*.6+.6)});
 shot({t:o.t,cam:o.cam,look:o.look,who:'none',fans:!!o.fans,screen:o.screen||''});
 chairs.forEach((c,i)=>{c.g.rotation.y=o.turn[i]*Math.PI});
 JD.J.forEach((j,i)=>{animChar(j,o.t+i,0,'talk')});
 const [j1,j2,j3,j4]=JD.J;
 // 1 : sourire, bras ouverts
 j1.aL.rotation.set(-1.45,0,-.75);j1.aR.rotation.set(-1.35,0,.75);j1.mo.scale.set(1.6,2.5,1);
 // 2 : bras croisés, bouche fermée
 j2.aL.rotation.set(-.6,0,.9);j2.aR.rotation.set(-.6,0,-.9);j2.mo.scale.set(1.2,.6,1);j2.head.rotation.set(.12,0,0);
 // 3 : mains sur les oreilles, bouche grande ouverte
 j3.aL.rotation.set(0,0,-3.25);j3.aR.rotation.set(0,0,3.25);j3.mo.scale.set(.9,7,1);j3.head.rotation.set(-.1,0,0);
 // 4 : bras en l'air, euphorique
 j4.aL.rotation.set(0,0,-2.4);j4.aR.rotation.set(0,0,2.4);j4.mo.scale.set(1.3,5,1);
 JD.EM.forEach((s,i)=>{s.visible=!!o.em&&o.em.includes(i);const c=chairs[i].g.position;s.position.set(c.x+.85,4.0,c.z+.3);s.scale.setScalar(.95)});
 JD.NUM.forEach((s,i)=>{s.visible=!!o.num;const c=chairs[i].g.position;s.position.set(c.x,4.15,c.z+.3);s.scale.setScalar(1.3)});
 JD.HEARTS.forEach((s,i)=>{s.visible=!!o.hearts;const c=chairs[0].g.position;s.position.set(c.x-1+(i%3)*1,3.2+Math.floor(i/3)*.8+(i%2)*.2,c.z+.6);s.scale.setScalar(.55)});
 capHook(o.t)}'''

Y = lambda s: f'<span style="color:#FFC24B">{s}</span>'
CSS = """#my{position:fixed;inset:0;pointer-events:none;font-family:Heebo;direction:rtl;color:#fff;visibility:visible;z-index:120}
#my *{visibility:visible}
#my .t{position:absolute;left:0;right:0;text-align:center;padding:0 22px;text-shadow:0 3px 14px rgba(0,0,0,.95),0 0 4px rgba(0,0,0,.8)}
#my .h{font:900 46px/1.12 Heebo}#my .s{font:900 30px/1.2 Heebo}
#my .tag{display:inline-block;background:#FFC24B;color:#1a0f2a;border-radius:999px;padding:6px 20px;font:900 24px Heebo;text-shadow:none}
#my .band{position:absolute;left:0;right:0;height:30%}
#my .num{position:absolute;bottom:2.5%;left:4%;font:900 18px Heebo;opacity:.85;text-shadow:0 2px 6px #000}
#my .brand{position:absolute;top:2.5%;right:4%;background:rgba(10,6,20,.75);border:2px solid #E01F26;border-radius:999px;padding:3px 12px;font:900 15px Heebo}
#my .q{display:inline-block;background:rgba(10,6,20,.72);border-radius:20px;padding:8px 22px;font:900 32px/1.2 Heebo}
"""
TOP = '<div class=band style="top:0;background:linear-gradient(rgba(10,6,20,.78),rgba(10,6,20,0))"></div>'
BOT = '<div class=band style="bottom:0;background:linear-gradient(rgba(10,6,20,0),rgba(10,6,20,.82))"></div>'

X = [-5.1, -1.7, 1.7, 5.1]
def judge(i):  # gros plan sur le juge i (fauteuil retourné)
    return dict(cam=[X[i] + .35, 2.75, 12.0], look=[X[i], 2.05, 8.6], turn=[1, 1, 1, 1], em=[i], hearts=(i == 0))

SLIDES = [
    (dict(singer=True, notes=True, cam=[.7, 3.0, 4.6], look=[0, 2.6, 0], turn=[0, 0, 0, 0], screen='🎶❌'),
     TOP + BOT + f'<div class="t h" style="top:8%">הוא {Y("זייף")} כל תו 🎤😂</div>'
     + f'<div class="t h" style="bottom:13%">4 שופטים. 4 תגובות.<br>{Y("איזה שופט אתם?")}</div>'
     + '<div class="t s" style="bottom:5%">החליקו ←</div>'),
    (judge(0), TOP + BOT + '<div class="t" style="top:7%"><span class=tag>שופט 1</span></div>'
     + f'<div class="t h" style="top:13%">{Y("הנחמד")} 😇</div>'
     + '<div class="t" style="bottom:12%"><span class=q>״היה מושלם! ממש!״</span></div>'
     + '<div class="t s" style="bottom:5%">(הוא זייף כל תו)</div>'),
    (judge(1), TOP + BOT + '<div class="t" style="top:7%"><span class=tag>שופטת 2</span></div>'
     + f'<div class="t h" style="top:13%">{Y("הקשוחה")} ❌</div>'
     + '<div class="t" style="bottom:12%"><span class=q>״לא. פשוט לא.״</span></div>'
     + '<div class="t s" style="bottom:5%">שתי מילים. בלי רחמים.</div>'),
    (judge(2), TOP + BOT + '<div class="t" style="top:7%"><span class=tag>שופט 3</span></div>'
     + f'<div class="t h" style="top:13%">{Y("בהלם")} 😱</div>'
     + '<div class="t" style="bottom:12%"><span class=q>סותם אוזניים</span></div>'
     + '<div class="t s" style="bottom:5%">מהתו הראשון…</div>'),
    (judge(3), TOP + BOT + '<div class="t" style="top:7%"><span class=tag>שופטת 4</span></div>'
     + f'<div class="t h" style="top:13%">{Y("מסתובבת בכל מקרה")} 🔄</div>'
     + '<div class="t" style="bottom:12%"><span class=q>״אני רוצה אותו בקבוצה שלי!״</span></div>'
     + '<div class="t s" style="bottom:5%">כי זיוף זה סגנון 😎</div>'),
    (dict(cam=[0, 7.2, 22], look=[0, 2.2, 8.6], turn=[1, 1, 1, 1], num=True),
     TOP + BOT + f'<div class="t h" style="top:8%">{Y("איזה שופט אתם?")} 🤔</div>'
     + '<div class="t h" style="bottom:12%">כתבו 1, 2, 3 או 4 👇</div>'
     + f'<div class="t s" style="bottom:5%">ותייגו את {Y("השופט")} שבחבורה</div>'),
    (dict(singer=True, fans=True, cam=[0, 3.9, 8.5], look=[0, 2.5, 0.5], turn=[0, 0, 0, 0], screen='🎤 במה'),
     TOP + BOT + f'<div class="t h" style="top:8%">רוצים לעלות<br>{Y("לבמה")}? 🎤</div>'
     + f'<div class="t h" style="bottom:14%">כתבו {Y("במה")} ותיכנסו 👇</div>'
     + '<div class="t s" style="bottom:5%">📩 שלחו לחבר שמזייף</div>'),
]

def main():
    with sync_playwright() as p:
        b = p.chromium.launch(args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
        pg = b.new_page(viewport={'width': 540, 'height': int(os.environ.get('H', 675))}, device_scale_factor=2); routes(pg); pg.add_init_script(INIT)
        errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto('http://local/index.html?demo'); pg.wait_for_timeout(4000)
        pg.evaluate(CHAR_JS + ";0"); pg.evaluate(STUDIO_JS + ";0"); pg.evaluate(EXTRA + ";0"); pg.evaluate(JUDGES + ";0")
        pg.add_style_tag(content='#ov{display:none!important}' + CSS)
        pg.evaluate("()=>{const d=document.createElement('div');d.id='my';document.body.appendChild(d)}")
        only = os.environ.get('ONLY')
        for i, (cfg, html) in enumerate(SLIDES, 1):
            if only and str(i) not in only.split(','): continue
            o = dict(t=1.3); o.update(cfg)
            pg.evaluate(POSE, o)
            if os.environ.get('NOTXT'): html = ''
            pg.evaluate('h=>{document.getElementById("my").innerHTML=h}', (html + f'<div class=brand>🎤 THE NOISE</div><div class=num>{i}/{len(SLIDES)}</div>') if not os.environ.get('NOTXT') else '')
            pg.wait_for_timeout(400)
            pg.screenshot(path=f'{OUT}/slide{i}.jpg', type='jpeg', quality=92)
        print('slides', len(SLIDES), 'erreurs', errs[:5]); b.close()

main()
