"""The Noise 22.11 « המקהלה הכי מזייפת בעולם? » חלק 1 : filme un plan (wide|demo|end) de l'arène 3D, sans texte, à 10 i/s.
Usage : DSF=1.5 python3 film.py <dossier> <plan> <durée_s> '<json shot extra>'"""
import sys, os, json
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__)); T = '/root/three3/node_modules/three/build/three.min.js'
OUT, SHOT, DUR = sys.argv[1], sys.argv[2], float(sys.argv[3]); X = json.loads(sys.argv[4]) if len(sys.argv) > 4 else {}
os.makedirs(OUT, exist_ok=True); FPS = 10
with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    pg = b.new_page(viewport={'width': 540, 'height': 960}, device_scale_factor=float(os.environ.get('DSF', 1.5)))
    errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    def route(r):
        u = r.request.url
        if u.endswith('three.min.js'): r.fulfill(path=T, content_type='text/javascript')
        elif u.startswith('http://local/'): r.fulfill(path=HERE + '/scene.html', content_type='text/html')
        else: r.abort()
    pg.route('**/*', route); pg.goto('http://local/'); pg.wait_for_timeout(1500)
    sh = dict(name=SHOT, fn=-9, T1=None, T3=None, T10=None); sh.update(X)
    for i in range(int(round(DUR * FPS))):
        pg.evaluate('([s,t])=>pose(s,t)', [sh, i / FPS])
        pg.screenshot(path=f'{OUT}/f{i:04d}.jpg', type='jpeg', quality=90)
    print(SHOT, 'errs', errs[:5]); b.close()
