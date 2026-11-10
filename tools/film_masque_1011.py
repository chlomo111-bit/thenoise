"""The Noise – reel 10.11 « המועמד במסכה » : un candidat masqué venu d'un autre monde atterrit sur la scène et chante faux.
Voix Juniper (eleven_v4, 25,6 s), découpage mot à mot. Filmé sur le vrai plateau 3D (index.html?demo) avec les personnages cubes de film3d.py.
Les textes (sous-titres) sont dessinés dans la page, au-dessus du canvas.
Usage : python3 tools/film_masque_1011.py <node_modules> <dossier_images> [échantillon]"""
import sys, os, re, math
from playwright.sync_api import sync_playwright
NM, OUT = sys.argv[1], sys.argv[2]; SAMPLE = int(sys.argv[3]) if len(sys.argv) > 3 else 1
R = '/home/claude/thenoise'; FPS = 30; TOTAL = 26.4
os.makedirs(OUT, exist_ok=True)
src = open(f'{R}/tools/film3d.py').read()
CHAR_JS = re.search(r"CHAR_JS = r'''(.*?)'''", src, re.S).group(1)
STUDIO_JS = re.search(r"STUDIO_JS = r'''(.*?)'''", src, re.S).group(1)

EXTRA = r'''
{const M=(c,e,ei)=>new THREE.MeshStandardMaterial({color:c,roughness:.5,emissive:e||0,emissiveIntensity:ei||0});
 const X=mkChar({shirt:0x7b2cff,pants:0x2a0b4a,hair:0x111111,mask:true,ph:.7,skin:0xbfe8ff});X.g.position.set(0,.7,0);scene.add(X.g);
 const aura=new THREE.PointLight(0xa070ff,0,8);aura.position.set(0,2.6,1.2);scene.add(aura);
 const ring=new THREE.Mesh(new THREE.TorusGeometry(1.4,.09,10,48),new THREE.MeshBasicMaterial({color:0xb26bff,transparent:true,opacity:.9}));ring.rotation.x=Math.PI/2;ring.position.set(0,.78,0);scene.add(ring);
 const beam=new THREE.Mesh(new THREE.CylinderGeometry(1.2,1.6,14,32,1,true),new THREE.MeshBasicMaterial({color:0xb26bff,transparent:true,opacity:.0,side:THREE.DoubleSide,depthWrite:false}));beam.position.set(0,7.5,0);scene.add(beam);
 const ENV=new THREE.Group();const pb=new THREE.Mesh(new THREE.BoxGeometry(1.0,.04,.66),M(0xf3e6c8,0xf3e6c8,.15));ENV.add(pb);
 const seal=new THREE.Mesh(new THREE.CylinderGeometry(.12,.12,.05,20),M(0xa50f17,0x5a0006,.4));seal.position.set(0,.05,0);ENV.add(seal);ENV.scale.setScalar(1.6);scene.add(ENV);ENV.visible=false;
 const NOTES=[];for(let i=0;i<10;i++){const s=emojiSprite(i%3?'🎵':'❌');s.visible=false;scene.add(s);NOTES.push(s)}
 window.MASK={X,aura,ring,beam,ENV,NOTES};
 const ov=document.createElement('div');ov.id='ov';ov.style.cssText='position:fixed;inset:0;z-index:99;pointer-events:none;font-family:Heebo;direction:rtl;visibility:visible';document.body.appendChild(ov);
 const css=document.createElement('style');css.textContent='#ov *{visibility:visible}#ov .t{position:absolute;left:0;right:0;text-align:center;color:#fff;text-shadow:0 4px 18px rgba(0,0,0,.9);padding:0 16px}#ov .y{color:#FFC24B}#ov .p{color:#C9A8FF}@keyframes pop{0%{transform:scale(.4);opacity:0}55%{transform:scale(1.15);opacity:1}100%{transform:scale(1)}}#ov .pop{animation:pop .26s ease-out both}#ov .box{display:inline-block;background:rgba(10,6,20,.78);border-radius:24px;padding:10px 24px}';document.head.appendChild(css);
 ov.innerHTML='<div class=t id=oT style="top:9%"></div><div class=t id=oM style="top:36%"></div><div class=t id=oB style="bottom:13%"></div><div id=oF style="position:absolute;inset:0;background:#fff;opacity:0"></div><div id=oV style="position:absolute;inset:0;background:radial-gradient(ellipse at center,rgba(120,40,255,0) 40%,rgba(90,20,200,.55) 100%);opacity:0"></div><div style="position:absolute;top:3%;right:4%;background:rgba(10,6,20,.75);border:2px solid #E01F26;border-radius:999px;padding:4px 14px;font:900 14px Heebo;color:#fff">🎤 THE NOISE · מועמד סודי</div>';
 window.OVL={last:''};
 window.ovl=function(key,top,mid,bot,flash,vio){const O=window.OVL;if(key!==O.last){O.last=key;document.getElementById('oT').innerHTML=top;document.getElementById('oM').innerHTML=mid;document.getElementById('oB').innerHTML=bot}
   document.getElementById('oF').style.opacity=flash;document.getElementById('oV').style.opacity=vio};
}
'''

HITS = [0.16, 1.84, 3.39, 6.0, 7.28, 9.01, 10.84, 11.65, 12.56, 14.08, 15.28, 17.35, 19.04, 21.2, 23.16]
BIG = {0.16, 1.84, 11.65, 15.28, 17.35}

def lerp(a, b, k): return [x + (y - x) * k for x, y in zip(a, b)]
def ease(k): k = max(0, min(1, k)); return k * k * (3 - 2 * k)
Y = lambda s: f'<span class=y>{s}</span>'
P = lambda s: f'<span class=p>{s}</span>'
box = lambda s, sz=46: f'<div class="box pop" style="font:900 {sz}px/1.18 Heebo">{s}</div>'
pill = lambda s, sz=38: f'<div class="pop" style="display:inline-block;background:#FFC24B;color:#1a1108;border-radius:24px;padding:12px 28px;font:900 {sz}px/1.2 Heebo;text-shadow:none">{s}</div>'

def plan(t):
    """renvoie (o pour shot(), key, top, mid, bot, vio, extras)"""
    o = dict(t=t, who='none', fans=False, screen='')
    x = {'xmode': 'idle', 'beam': 0, 'env': None, 'notes': 0, 'land': 1}
    if t < 2.88:  # arrivée du candidat : il descend dans un faisceau violet
        k = ease(t / 2.6); o.update(cam=lerp([0, 6.5, 13], [0, 3.6, 6.2], k), look=[0, 2.6, 0], screen='👽 ???')
        x.update(beam=1, land=min(1, t / 1.7), xmode='idle')
        key = 'a' + ('1' if t >= 1.84 else '0')
        top = box(f'מועמד {P("מעולם אחר")}… 👽', 54)
        bot = box(f'{Y("נחת")} על הבמה! 🎤', 58) if t >= 1.84 else ''
        return o, x, key, top, '', bot, .55
    if t < 5.9:
        a = (t - 2.88) * .18 + 0.6; o.update(cam=[math.sin(a) * 15, 7.5, math.cos(a) * 15 + 3], look=[0, 2.5, 3], fans=True, screen='The Noise')
        key = 'b'; top = pill('🎤 THE NOISE', 34)
        mid = box(f'העוקבים = {Y("הזמרים")}<br>ו{Y("השופטים")} 🪑', 48)
        return o, x, key, top, mid, '', 0
    if t < 8.91:
        k = ease((t - 5.9) / 3); o.update(cam=lerp([4, 3.6, 9], [1.5, 3.2, 6.5], k), look=[0, 2.6, 0], who='dudi', screen='82 🎤')
        key = 'c' + ('1' if t >= 7.28 else '0'); top = box(f'אתמול: {Y("81")}', 50) + (f'<div style="margin-top:12px">{box("היום: " + Y("82") + " 🎉", 60)}</div>' if t >= 7.28 else '')
        return o, x, key, top, '', '', 0
    if t < 10.84:  # la lettre
        lt = t - 8.91; x['env'] = lt; o.update(cam=[0.7, 2.9, 5.2 - lt * .5], look=[0, 2.3, 1.6], screen='✉️')
        key = 'd'; bot = box(f'✉️ במכתב נכתב:<br>{Y("“הוא יגיע”")}', 46)
        return o, x, key, '', '', bot, .2
    if t < 13.44:  # il est là, masqué
        k = ease((t - 10.84) / 2.4); o.update(cam=lerp([0, 3.6, 7.0], [0, 3.15, 3.4], k), look=[0, 2.75, 0], screen='🎭 ???')
        key = 'e' + ('1' if t >= 12.4 else '0'); top = box(f'והערב — {Y("הוא פה")}.', 52); bot = box(f'עם {P("מסכה")} 🎭', 58) if t >= 12.4 else ''
        return o, x, key, top, '', bot, .3
    if t < 17.28:  # il chante faux
        lt = t - 13.44; x.update(xmode='sing', notes=1); a = .4 + lt * .25
        o.update(cam=[math.sin(a) * 6, 3.4, math.cos(a) * 6 + 1], look=[0, 2.7, 0], fans=True, screen='🎶❌')
        key = 'f' + ('1' if t >= 15.28 else '0'); top = box('🎤 הוא פתח את הפה…', 46)
        bot = box(f'😂 ו{Y("זייף")} את כל השיר!', 56) if t >= 15.28 else ''
        return o, x, key, top, '', bot, 0
    if t < 18.96:  # le jury en état de choc
        lt = t - 17.28; o.update(cam=[0, 4.2, 15.5], look=[0, 1.8, 8.6], chairTurn=min(1, lt / .6), screen='😱')
        x['xmode'] = 'sing'; key = 'g'; mid = box(f'😱 השופטים {Y("בהלם")}!', 60)
        return o, x, key, '', mid, '', 0
    if t < 21.12:  # qui est sous le masque ?
        k = ease((t - 18.96) / 2.1); o.update(cam=lerp([.6, 3.2, 3.2], [0, 3.15, 2.1], k), look=[0, 3.1, 0], screen='❓')
        key = 'h'; top = box(f'מי מסתתר<br>מאחורי {P("המסכה")}? 🤔', 56)
        return o, x, key, top, '', '', .45
    a = (t - 21.12) * .12 - .25; o.update(cam=[math.sin(a) * 10, 5, math.cos(a) * 10 + 3], look=[0, 2.6, 1], fans=True, screen='❓🎭❓')
    key = 'i' + ('1' if t >= 23.16 else '0'); top = box(f'כתבו את {Y("הניחוש")} שלכם 👇', 48)
    bot = pill('🏷️ תייגו חבר<br>שמזייף בדיוק ככה! 😂', 44) if t >= 23.16 else ''
    return o, x, key, top, '', bot, .2

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
        return r.fulfill(path=f'{R}/{p}')
    pg.route('http://local/**', loc)
    pg.route('https://**', lambda r: r.abort())

INIT = "window.CAP=true;window.__T=0;performance.now=()=>window.__T*1000;Math.random=(()=>{let s=12345;return()=>{s=(s*16807)%2147483647;return(s-1)/2147483646}})();"

STEP = r'''o=>{window.__T=o.t;const T=window.MASK,x=o.x;
 const X=T.X;X.g.visible=true;
 X.g.position.y=.7+(1-x.land)*9;X.g.rotation.y=x.land<1?(1-x.land)*6:Math.sin(o.t*.7)*.2;
 animChar(X,o.t,0,x.xmode==='sing'?'sing':'talk');
 if(x.xmode==='sing'){X.body.rotation.z=Math.sin(o.t*9)*.12;X.head.rotation.z=Math.sin(o.t*7)*.15}
 T.aura.intensity=x.beam?2.5:1.2;T.ring.rotation.z=o.t*2;T.ring.material.opacity=.5+.4*Math.sin(o.t*5);
 T.beam.material.opacity=x.beam?.28*(1-Math.max(0,(o.t-2.2)/.6)):0;
 T.ENV.visible=x.env!=null;if(x.env!=null){const k=Math.min(1,x.env/.9);T.ENV.position.set(.1,2.2+(1-k)*3,1.6);T.ENV.rotation.set(1.2+(1-k)*3,o.t*.5,0)}
 T.NOTES.forEach((s,i)=>{s.visible=!!x.notes;if(x.notes){const a=o.t*1.3+i*.63,r=1.2+(i%3)*.4;s.position.set(Math.sin(a)*r,2.6+((o.t*1.2+i*.37)%2.2),Math.cos(a)*r*.6+.6)}});
 ovl(o.key,o.top,o.mid,o.bot,o.flash,o.vio);
 shot(o)}'''

def main():
    with sync_playwright() as p:
        b = p.chromium.launch(args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
        st = b.new_page(viewport={'width': 540, 'height': 960}, device_scale_factor=2); routes(st); st.add_init_script(INIT)
        errs = []; st.on('pageerror', lambda e: errs.append(str(e)))
        st.goto('http://local/index.html?demo'); st.wait_for_timeout(4000)
        st.evaluate(CHAR_JS + ";0"); st.evaluate(STUDIO_JS + ";0"); st.evaluate(EXTRA + ";0")
        n = int(round(TOTAL * FPS))
        for i in range(n):
            if i % SAMPLE: continue
            t = i / FPS
            o, x, key, top, mid, bot, vio = plan(t)
            h = max([z for z in HITS if z <= t], default=-9); dt = t - h
            kick = math.exp(-dt * (5 if h in BIG else 9)) if dt < .4 else 0
            if kick and t >= 0.1:
                o['cam'] = [o['cam'][0] + math.sin(i * 7.1) * kick * .25, o['cam'][1] + math.cos(i * 5.3) * kick * .25, o['cam'][2]]
            o.update(x=x, key=key, top=top, mid=mid, bot=bot, vio=vio, flash=kick * (.5 if h in BIG else .2))
            st.evaluate(STEP, o)
            st.screenshot(path=f'{OUT}/f{i:04d}.jpg', type='jpeg', quality=90)
        print('images', n, 'erreurs', errs[:5]); b.close()

main()
