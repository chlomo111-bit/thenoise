"""Story VIDÉO The Noise (1080×1920, ~8 s) : plateau 3D du jeu qui bouge (caméra en mouvement, lumières,
public qui saute) + texte en haut/bas + musique synthétique (jamais de voix).
Usage : python3 tools/story_video.py out.mp4 '<titre (html, .k = jaune)>' '<texte>' '<cta>' [secondes=8]
Dépendances : npm i three@0.128.0 @fontsource/heebo dans /tmp/nm (NM=/tmp/nm/node_modules).
"""
import sys, os, base64, subprocess, pathlib, tempfile
from playwright.sync_api import sync_playwright
out, title, text, cta = sys.argv[1:5]; SEC = float(sys.argv[5]) if len(sys.argv) > 5 else 8.0
FPS = 30; N = int(SEC * FPS)
R = pathlib.Path(__file__).resolve().parent.parent; NM = os.environ.get('NM', '/tmp/nm/node_modules')
font = base64.b64encode((R / 'tools/fonts/Heebo.ttf').read_bytes()).decode()
tmp = pathlib.Path(tempfile.mkdtemp())

OV = f'''<!doctype html><html dir="rtl"><head><meta charset="utf-8"><style>
@font-face{{font-family:Heebo;src:url(data:font/ttf;base64,{font}) format("truetype");font-weight:100 900}}
html,body{{margin:0;width:1080px;height:1920px;background:transparent;font-family:Heebo,sans-serif;color:#fff;overflow:hidden}}
.top{{position:absolute;top:230px;left:70px;right:70px;text-align:center}}
.pill{{display:inline-block;background:#e0242b;border-radius:999px;padding:14px 44px;font-weight:900;font-size:46px;box-shadow:0 0 40px rgba(224,36,43,.55)}}
h1{{font-weight:900;font-size:118px;line-height:1.04;margin:30px 0 0;text-shadow:0 8px 40px #000d}}.k{{color:#FFC24B}}
.bot{{position:absolute;bottom:300px;left:70px;right:70px;text-align:center}}
.sub{{font-weight:800;font-size:50px;line-height:1.3;margin:0 0 34px;text-shadow:0 6px 30px #000e}}
.cta{{display:inline-block;background:#FFC24B;color:#111;border-radius:999px;padding:24px 60px;font-weight:900;font-size:56px}}
.ltr{{direction:ltr;unicode-bidi:isolate}}
</style></head><body><div class="top"><div class="pill">🎤 The Noise</div><h1>{title}</h1></div>
<div class="bot"><div class="sub">{text}</div><div class="cta">{cta}</div></div></body></html>'''

def routes(pg):
    pg.route('**/three.min.js', lambda r: r.fulfill(path=f'{NM}/three/build/three.min.js'))
    pg.route('**/OrbitControls.js', lambda r: r.fulfill(path=f'{NM}/three/examples/js/controls/OrbitControls.js'))
    pg.route('**/supabase.min.js', lambda r: r.fulfill(body='window.supabase=null', content_type='text/javascript'))
    css = ''.join(f"@font-face{{font-family:Heebo;src:url(http://local/__f/heebo-{s}-{w}-normal.woff2);font-weight:{w}}}" for s in ('hebrew', 'latin') for w in (400, 900))
    pg.route('https://fonts.googleapis.com/**', lambda r: r.fulfill(body=css, content_type='text/css'))
    def loc(r):
        p = r.request.url.split('http://local/')[1].split('?')[0]
        if p.startswith('__f/'): return r.fulfill(path=f'{NM}/@fontsource/heebo/files/{p[4:]}')
        if p.endswith('three.min.js'): return r.fulfill(path=f'{NM}/three/build/three.min.js')
        return r.fulfill(path=str(R / p))
    pg.route('http://local/**', loc)

INIT = "window.CAP=true;window.__T=0;performance.now=()=>window.__T*1000;Math.random=(()=>{let s=777;return()=>{s=(s*16807)%2147483647;return(s-1)/2147483646}})();"
SETUP = r'''
nameLabels.visible=false;contGroup.visible=false;
document.body.querySelectorAll('*').forEach(e=>{if(e.tagName!=='CANVAS'&&!e.contains(renderer.domElement))e.style.visibility='hidden'});
controls.enabled=true;controls.enableDamping=false;fly=null;
const key=new THREE.SpotLight(0xfff0dd,1.3,40,.42,.6,1);key.position.set(2,11,10);key.target.position.set(0,2,0);scene.add(key,key.target);
window.vshot=function(t,k){const a=-0.9+1.8*k;camera.position.set(Math.sin(a)*14,5.5-1.5*k,-1+Math.cos(a)*14);controls.target.set(0,2.6,0);
  chairs.forEach(c=>{if(c.label)c.label.visible=false});nameLabels.visible=false;
  if(Math.floor(t*4)!==Math.floor((t-1/30)*4)){for(let i=0;i<10;i++){const si=seatOrder[Math.floor(Math.random()*140)];JUMP[si]=performance.now()}
    const si=seatOrder[Math.floor(Math.random()*120)];const[x,y,z]=SEATS[si];const e=emojiSprite(['👏','🎤','🔥','🎟️'][Math.floor(Math.random()*4)]);e.position.set(x,y+2.4,z);scene.add(e);FLY.push({o:e,t0:performance.now(),type:'em',y0:y+2.4})}
  screenLine='';capHook(t)};0
'''

with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    ov = b.new_page(viewport={'width': 1080, 'height': 1920}); ov.set_content(OV); ov.wait_for_timeout(400)
    ov.screenshot(path=str(tmp / 'ov.png'), omit_background=True)
    pg = b.new_page(viewport={'width': 540, 'height': 960}, device_scale_factor=1); routes(pg); pg.add_init_script(INIT)
    pg.goto('http://local/index.html?demo'); pg.wait_for_timeout(3000); pg.evaluate(SETUP)
    vf = "[0:v]scale=1080:1920:flags=lanczos,format=yuv420p,eq=brightness=-0.06[bg];[1:v]format=rgba,fade=t=in:st=0.1:d=0.35:alpha=1[o];[bg][o]overlay=0:0:format=auto,format=yuv420p[v]"
    ff = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'image2pipe', '-framerate', str(FPS), '-c:v', 'mjpeg', '-i', '-',
                           '-loop', '1', '-framerate', str(FPS), '-i', str(tmp / 'ov.png'), '-filter_complex', vf, '-map', '[v]', '-frames:v', str(N),
                           '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', '-r', str(FPS), str(tmp / 'v.mp4')], stdin=subprocess.PIPE)
    for j in range(N):
        t = j / FPS; k = j / max(1, N - 1); k = k * k * (3 - 2 * k)
        pg.evaluate(f'window.__T={t};vshot({t},{k})'); ff.stdin.write(pg.screenshot(type='jpeg', quality=88))
    ff.stdin.close(); ff.wait(); b.close()

# musique : kick 4/4 + hi-hat + basse en arpège (120 bpm), fondu en fin
mus = (f"aevalsrc='0.6*sin(2*PI*52*t)*exp(-16*mod(t,0.5))"
       f"+0.08*(random(0)*2-1)*exp(-60*mod(t+0.25,0.5))"
       f"+0.16*sin(2*PI*110*(1+0.5*eq(floor(mod(t,2)/0.5),1)+0.25*eq(floor(mod(t,2)/0.5),2)+0.333*eq(floor(mod(t,2)/0.5),3))*t)*exp(-3*mod(t,0.25))"
       f"+0.05*sin(2*PI*440*t)*eq(mod(floor(t*4),8),0)*exp(-8*mod(t,0.25))':s=44100:d={SEC}")
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(tmp / 'v.mp4'), '-f', 'lavfi', '-i', mus,
                '-filter_complex', f'[1:a]afade=t=in:d=0.3,afade=t=out:st={SEC-0.8}:d=0.8,alimiter=limit=0.9[a]',
                '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', out], check=True)
print('ok', out)
