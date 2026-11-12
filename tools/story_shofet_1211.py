"""The Noise – story vidéo 12.11 (≈7,5 s, 1080×1920) qui renvoie au carrousel « איזה שופט אתם? ».
Plateau 3D filmé : le candidat masqué chante faux, les 4 fauteuils se retournent un à un, plan large des juges.
Réutilise JUDGES/POSE de carrousel_shofet_1211.py. Usage : python3 tools/story_shofet_1211.py <node_modules> <dossier_images> <durée>"""
import sys, os, math
from playwright.sync_api import sync_playwright
NM, OUT, TOTAL = sys.argv[1], sys.argv[2], float(sys.argv[3])
os.makedirs(OUT, exist_ok=True); FPS = 30
D = os.path.dirname(os.path.abspath(__file__))
src = open(f'{D}/carrousel_shofet_1211.py').read(); src = src[:src.rindex('def main')]
g = {'__name__': 'x', '__file__': f'{D}/carrousel_shofet_1211.py'}
sys.argv = sys.argv[:3]; exec(src.replace('os.makedirs(OUT, exist_ok=True)', ''), g)
for k in ('CHAR_JS', 'STUDIO_JS', 'EXTRA', 'JUDGES', 'POSE', 'routes', 'INIT', 'CSS', 'TOP', 'BOT', 'Y'): globals()[k] = g[k]

def lerp(a, b, k): return [x + (y - x) * k for x, y in zip(a, b)]
def ease(k): k = max(0, min(1, k)); return k * k * (3 - 2 * k)

def plan(t):
    if t < 2.2:  # gros plan candidat qui chante faux
        k = ease(t / 2.2); o = dict(singer=True, notes=True, cam=lerp([.6, 3.0, 4.2], [.9, 3.1, 5.6], k), look=[0, 2.6, 0], turn=[0] * 4, screen='🎶❌')
        h = f'<div class="t h" style="top:12%">4 שופטים 🪑<br>{Y("זיוף אחד")} 😂</div>'
    elif t < 4.6:  # les fauteuils se retournent un par un
        lt = t - 2.2; turn = [ease((lt - i * .45) / .5) for i in range(4)]
        o = dict(cam=lerp([0, 5.5, 20], [0, 6.8, 22], ease(lt / 2.4)), look=[0, 2.2, 8.6], turn=turn, em=[i for i in range(4) if turn[i] > .9])
        h = f'<div class="t h" style="top:12%">{Y("כולם")} מסתובבים… 🔄</div>'
    else:
        lt = t - 4.6; o = dict(cam=[math.sin(lt * .15) * 1.2, 7.2, 22], look=[0, 2.2, 8.6], turn=[1] * 4, num=True)
        h = (f'<div class="t h" style="top:12%">{Y("איזה שופט אתם?")} 🤔</div>'
             + '<div class="t" style="bottom:20%"><span class=q style="font-size:40px">👆 בפוסט החדש</span></div>'
             + '<div class="t s" style="bottom:12%">🎙️ שלחו לנו הודעה קולית</div>')
    o['t'] = t
    return o, TOP + BOT + h

def main():
    with sync_playwright() as p:
        b = p.chromium.launch(args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
        pg = b.new_page(viewport={'width': 540, 'height': 960}, device_scale_factor=2); routes(pg); pg.add_init_script(INIT)
        errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto('http://local/index.html?demo'); pg.wait_for_timeout(4000)
        for js in (CHAR_JS, STUDIO_JS, EXTRA, JUDGES): pg.evaluate(js + ";0")
        pg.add_style_tag(content='#ov{display:none!important}' + CSS)
        pg.evaluate("()=>{const d=document.createElement('div');d.id='my';document.body.appendChild(d)}")
        last = None
        for i in range(int(TOTAL * FPS)):
            if os.path.exists(f'{OUT}/f{i:04d}.jpg') and os.environ.get('RESUME'): continue
            o, html = plan(i / FPS)
            pg.evaluate(POSE, o)
            if html != last:
                pg.evaluate('h=>{document.getElementById("my").innerHTML=h}', html + '<div class=brand style="top:8%">🎤 THE NOISE</div>'); last = html
            pg.screenshot(path=f'{OUT}/f{i:04d}.jpg', type='jpeg', quality=88)
        print('images', i + 1, 'erreurs', errs[:5]); b.close()

main()
