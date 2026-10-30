"""Visuels The Noise (post du jour 4:5, stories 9:16).
Usage: python3 tools/visuel.py <post|story> <out.jpg> '<json>'
json: {"pill":"...","title":"...","hl":"mot du titre en jaune","lines":["..."],"cta":"...","bg":"chemin png optionnel"}
Fond : capture du site (?demo) si bg absent. Police Heebo (npm i @fontsource/heebo dans NM)."""
import sys, json, os, base64
from playwright.sync_api import sync_playwright
NM = os.environ.get('NM', '/tmp/nm/node_modules')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
kind, out, spec = sys.argv[1], sys.argv[2], json.loads(sys.argv[3])
W, H = (1080, 1350) if kind == 'post' else (1080, 1920)
def font(n): return base64.b64encode(open(f'{NM}/@fontsource/heebo/files/{n}', 'rb').read()).decode()
def shot_bg(pg):
    pg.set_viewport_size({'width': W // 2, 'height': H // 2})
    pg.route('**/three.min.js', lambda r: r.fulfill(path=f'{NM}/three/build/three.min.js'))
    pg.route('**/OrbitControls.js', lambda r: r.fulfill(path=f'{NM}/three/examples/js/controls/OrbitControls.js'))
    pg.route('**/supabase.min.js', lambda r: r.fulfill(body='window.supabase=null', content_type='text/javascript'))
    pg.route('https://fonts.googleapis.com/**', lambda r: r.fulfill(body='', content_type='text/css'))
    pg.route('http://local/**', lambda r: r.fulfill(path=ROOT + '/' + r.request.url.split('http://local/')[1].split('?')[0]))
    pg.goto('http://local/index.html?demo'); pg.wait_for_timeout(2500); pg.click('#enter'); pg.wait_for_timeout(6500)
    pg.evaluate("try{nameLabels.visible=false;chairs.forEach(c=>{if(c.label)c.label.visible=false})}catch(e){}");pg.wait_for_timeout(300)
    pg.evaluate("document.querySelectorAll('#hud,#search,#bar,#intro,.panel,#toast,#mdone,#nw').forEach(e=>e.style.display='none')")
    return base64.b64encode(pg.screenshot()).decode()
with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    pg = b.new_page()
    bg = base64.b64encode(open(spec['bg'], 'rb').read()).decode() if spec.get('bg') else shot_bg(pg)
    t = spec['title']
    if spec.get('hl'): t = t.replace(spec['hl'], f'<span class=y>{spec["hl"]}</span>')
    lines = ''.join(f'<div class=l>{x}</div>' for x in spec.get('lines', []))
    html = f'''<html dir=rtl><style>
@font-face{{font-family:H;font-weight:900;src:url(data:font/woff2;base64,{font('heebo-hebrew-900-normal.woff2')})}}
@font-face{{font-family:H;font-weight:900;src:url(data:font/woff2;base64,{font('heebo-latin-900-normal.woff2')});unicode-range:U+0000-00FF}}
@font-face{{font-family:H;font-weight:700;src:url(data:font/woff2;base64,{font('heebo-hebrew-700-normal.woff2')})}}
@font-face{{font-family:H;font-weight:700;src:url(data:font/woff2;base64,{font('heebo-latin-700-normal.woff2')});unicode-range:U+0000-00FF}}
body{{margin:0;width:{W}px;height:{H}px;font-family:H,'Noto Color Emoji',sans-serif;color:#fff;background:#0b0507 url(data:image/png;base64,{bg}) center/cover;overflow:hidden}}
.bgb{{position:absolute;inset:-20px;background:inherit;filter:blur(3px)}}
.o{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,3,5,.82) 0%,rgba(10,3,5,.35) 42%,rgba(10,3,5,.88) 78%)}}
.c{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;text-align:center;padding:{'90px 70px' if kind=='post' else '230px 80px'}}}
.p{{background:#E01F26;font-weight:900;font-size:46px;padding:12px 34px;border-radius:60px;box-shadow:0 8px 30px rgba(224,31,38,.5)}}
h1{{font-weight:900;font-size:{100 if kind=='post' else 112}px;line-height:1.05;margin:34px 0 0;text-shadow:0 6px 30px #000}}
.y{{color:#FFC24B}} .sp{{flex:1}}
.l{{font-weight:900;font-size:50px;background:rgba(0,0,0,.6);border:3px solid rgba(255,194,75,.7);border-radius:26px;padding:16px 30px;margin:12px 0;width:88%}}
.cta{{margin-top:26px;background:#FFC24B;color:#111;font-weight:900;font-size:62px;padding:16px 48px;border-radius:70px}}
.f{{margin-top:22px;font-weight:700;font-size:30px;opacity:.85}}
</style><body><div class=bgb></div><div class=o></div><div class=c><div class=p>{spec.get('pill','')}</div><h1>{t}</h1><div class=sp></div>{lines}
{f'<div class=cta>{spec["cta"]}</div>' if spec.get('cta') else ''}<div class=f dir=ltr>@the_noise_2026 · thenoise.hakaveret.online</div></div></body></html>'''
    pg.set_viewport_size({'width': W, 'height': H}); pg.set_content(html); pg.wait_for_timeout(600)
    pg.screenshot(path=out, type='jpeg', quality=90); b.close()
print(out)
