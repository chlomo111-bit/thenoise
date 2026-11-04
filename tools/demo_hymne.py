"""Démo 10 s : hymne The Noise + Dudi (ducking)."""
import sys, os, math, subprocess, importlib.util
sys.path.insert(0, '/tmp/claude-0/ep4'); sys.path.insert(0, '/tmp/claude-0/ep')
from playwright.sync_api import sync_playwright
import film4 as M; import film as F
D = '/tmp/claude-0/demo'; FPS = 30
CUT = [0, 3.2, 7.4, 10.0]; NF = [round(CUT[i+1]*FPS) - round(CUT[i]*FPS) for i in range(3)]
V0 = 3.35   # début de la voix de Dudi (dans la scène B)
spec = importlib.util.spec_from_file_location('b1', '/tmp/claude-0/ep/build.py'); B1 = importlib.util.module_from_spec(spec); spec.loader.exec_module(B1)
OV = [
 '''<div class="c" style="top:300px"><div class="pill" style="font-size:58px">🎤 ההמנון של The Noise</div></div>
    <div class="c card" style="top:1300px"><div class="big" style="font-size:92px">אני <span class="k">מזייף</span>,<br>ואני גאה בזה!</div></div>''',
 '''<div class="c" style="top:300px"><div class="pill" style="font-size:64px">✋ עצרו!</div></div>
    <div class="c card" style="top:1330px"><div class="big" style="font-size:84px">יש לכם חבר<br><span class="k">שמזייף</span> במקלחת? 🚿</div></div>''',
 '''<div class="c card" style="top:300px"><div class="big" style="font-size:88px">תייגו חבר<br><span class="k">שמזייף כמוני</span> 👇</div></div>
    <div class="c" style="top:1500px"><div class="cta" style="font-size:54px">״אני מזייף״ = אודישן + 50 🎟️</div></div>''']
def overlays():
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
        for i, h in enumerate(OV):
            pg.set_content(f'<html><head><meta charset="utf-8"><style>{B1.CSS}</style></head><body>{h}</body></html>'); pg.wait_for_timeout(250)
            pg.screenshot(path=f'{D}/ov{i}.png', omit_background=True)
        b.close()
def talk(t):   # enveloppe de la voix de Dudi (nimrod 0–4.26)
    lt = t - V0
    if lt < 0 or lt > 4.26: return 0
    return min(1., M.rms('n', lt) / M.PEAK['n'])
S = M.S
PLAN = [S([-5, 6.5, 16], [3, 4.5, 11], [0, 2.4, 0], [0, 2.8, 0], pos={'dudi': [-1.2, .3, .4], 'nisso': [1.2, 0, -.4]}, dudiMode='dance', fans=True, jump=True, screen='🎤🎶'),
        S([1.2, 3.3, 5.4], [0, 3.05, 3.7], [0, 3.1, 0], [0, 3.2, 0], pos={'dudi': [0, 0.3]}, screen='🚿?!'),
        S([0, 3.0, 4.0], [0, 4.6, 12.5], [0, 3.0, 0], [0, 2.6, 0], pos={'dudi': [-1.2, .3, .4], 'nisso': [1.2, 0, -.4]}, dudiMode='dance', fans=True, jump=True, screen='👇')]
def video():
    with sync_playwright() as p:
        b = p.chromium.launch(args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
        st = b.new_page(viewport={'width': 540, 'height': 960}, device_scale_factor=2); F.routes(st); st.add_init_script(F.INIT)
        st.goto('http://local/index.html?demo'); st.wait_for_timeout(3000)
        st.evaluate(F.CHAR_JS + ";0"); st.evaluate(M.EXTRA_JS + ";0"); st.evaluate(M.STUDIO_JS + ";0")
        f0 = 0
        for i, fn in enumerate(PLAN):
            n = NF[i]; d = n / FPS; tmp = f'{D}/s{i}.tmp.mp4'
            vf = "[0:v]format=yuv420p[bg];[1:v]format=rgba,fade=t=in:st=0:d=0.2:alpha=1[o];[bg][o]overlay=0:0:format=auto,format=yuv420p[v]"
            ff = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'image2pipe', '-framerate', str(FPS), '-c:v', 'mjpeg', '-i', '-', '-loop', '1', '-framerate', str(FPS), '-i', f'{D}/ov{i}.png',
                '-filter_complex', vf, '-map', '[v]', '-frames:v', str(n), '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p', '-r', str(FPS), tmp], stdin=subprocess.PIPE)
            for j in range(n):
                t = (f0 + j) / FPS; o = fn(j / FPS, d, t); o['talk'] = talk(t)
                o['showAt'] = (CUT[2] - 1.3) if t >= CUT[2] else None
                st.evaluate("o=>{window.__T=o.t;show=o.showAt!=null?{t0:o.showAt*1000}:null;shot(o)}", o)
                ff.stdin.write(st.screenshot(type='jpeg', quality=90))
            ff.stdin.close(); ff.wait(); os.replace(tmp, f'{D}/s{i}.mp4'); f0 += n; print('scene', i, flush=True)
        b.close()
def audio():
    # hymne : +4 dB, baissé à 18 % pendant la voix de Dudi (V0 → V0+4.26), fondu final
    a, z = V0 - 0.25, V0 + 4.26 + 0.15
    vol = f"volume='1.6*if(between(t,{a},{z}),0.18,1)':eval=frame"
    fl = (f"[0:a]atrim=0:10,asetpts=PTS-STARTPTS,{vol},afade=t=out:st=9.3:d=0.7[m];"
          f"[1:a]atrim=0:4.26,asetpts=PTS-STARTPTS,volume=1.15,adelay={int(V0*1000)}|{int(V0*1000)}[v];"
          f"[m][v]amix=inputs=2:normalize=0,alimiter=limit=0.95,aresample=44100[out]")
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', '/tmp/claude-0/hymne_v2.mp3', '-i', '/tmp/claude-0/ep4/nimrod.mp3', '-filter_complex', fl, '-map', '[out]', '-t', '10', '-c:a', 'aac', '-b:a', '192k', f'{D}/audio.m4a'], check=True)
if __name__ == '__main__':
    overlays(); audio(); video()
    open(f'{D}/l.txt', 'w').write(''.join(f'file s{i}.mp4\n' for i in range(3)))
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-i', f'{D}/l.txt', '-i', f'{D}/audio.m4a', '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'copy', '-shortest', '-movflags', '+faststart', f'{D}/demo.mp4'], check=True)
    print('ok')
