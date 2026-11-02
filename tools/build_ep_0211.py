"""Épisode 02/11 « החייזר על היען » : timeline des voix (découpe aux silences), overlays, audio."""
import importlib.util, subprocess, sys, json
from playwright.sync_api import sync_playwright
E = '/tmp/claude-0/ep2'; FPS = 30
spec = importlib.util.spec_from_file_location('b1', '/tmp/claude-0/ep/build.py'); B1 = importlib.util.module_from_spec(spec); spec.loader.exec_module(B1)
CSS = B1.CSS

# (source, début, fin) dans l'ordre de lecture
SEG = [
    ('n', 0.00, 4.92),    # 0 בפרק הקודם… הראל נחשף
    ('n', 5.31, 9.18),    # 1 שחר עוברת
    ('n', 9.63, 12.21),   # 2 אבל הלילה… משהו נחת
    ('n', 12.61, 15.71),  # 3 חייזר! רכוב על יען!
    ('d', 0.00, 4.38),    # 4 מבזק! חייזר נחת
    ('d', 4.88, 8.90),    # 5 ההחלטה של NissoC
    ('n', 16.08, 20.00),  # 6 המלך של הכרוביות… קרב ריקודים
    ('n', 20.41, 22.36),  # 7 יאללה חייזר
    ('d', 9.43, 17.10),   # 8 מועמדים לשופטים
    ('n', 22.87, 27.46),  # 9 אודישן NissoC מי אני
    ('n', 27.99, 34.90),  # 10 מי ניצח? כתבו בתגובות
]
GAP = [0.30, 0.30, 0.15, 0.30, 0.30, 0.30, 0.25, 1.80, 0.30, 0.30, 0.90]
LEAD = 0.30
starts = []; t = LEAD
for (s, a, b), g in zip(SEG, GAP):
    starts.append(t); t += (b - a) + g
TOTAL = t
bounds = [0.0] + starts[1:] + [TOTAL]
frames = [round(bounds[i + 1] * FPS) - round(bounds[i] * FPS) for i in range(len(SEG))]
BURSTS = [starts[1] + 1.6, starts[7]]          # confettis : « שחר עוברת » et début du קרב ריקודים

NEWS = '<div class="flash">⚡ מבזק</div><div class="live"><i></i>LIVE · קומה 24</div>'
TICK = '<div class="tick">🎤 אודישן מוקדם: NissoC · 👽 חייזר באולפן · 🎁 הגרלה ב־20:00 · 👨‍⚖️ מחפשים שופטים ·</div>'
LOW = lambda b: f'<div class="low"><span class="n">דנית · החדשות של The Noise</span><div class="b">{b}</div></div>'
SC = [
    '''<div class="c" style="top:280px"><div class="pill">⏪ בפרק הקודם…</div></div>
       <div class="c big" style="top:1420px;font-size:96px">מתחת למסכה: <span class="k">הראל!</span></div>''',
    '''<div class="c" style="top:280px"><div class="pill">🎤 אודישן מוקדם</div></div>
       <div class="c big" style="top:1380px;font-size:110px">✅ שחר <span class="k">עוברת!</span></div>
       <div class="c mid" style="top:1540px;font-size:46px"><span class="ltr">@shahar_b.y</span> · 2 ✅ מול 0 ❌</div>''',
    '''<div class="c big" style="top:300px;font-size:120px">אבל הלילה…</div>''',
    '''<div class="c" style="top:260px"><div class="pill" style="font-size:64px">👽 חייזר!!</div></div>
       <div class="c mid" style="top:1520px">רכוב על <span class="k">יען</span> 🦤 · עם רמקול ענק 🔊</div>''',
    NEWS + '''<div class="c card" style="top:330px"><div class="big" style="font-size:96px">👽 חייזר<br><span class="k">נחת באולפן!</span></div></div>''' + LOW('רכוב על יען – ועם רמקול ענק!') + TICK,
    NEWS + '''<div class="c card" style="top:330px"><div class="mid">ההחלטה של</div><div class="big k" style="font-size:110px">NissoC 👑</div><div class="mid" style="font-size:44px">הזוכה בהגרלה + המגיב של היום</div></div>''' + LOW('<span class="ltr">@habama.hamerkazit</span> החליט – וזה קרה!') + TICK,
    '''<div class="c card" style="top:280px"><div class="big" style="font-size:92px">👑 המלך החדש<br>של <span class="k">הכרוביות</span> 🥦</div></div>
       <div class="c mid" style="top:1520px">מזמין את דודי <span class="k">לקרב ריקודים?!</span></div>''',
    '''<div class="c" style="top:260px"><div class="pill" style="font-size:64px">🕺 קרב ריקודים!</div></div>
       <div class="c big" style="top:1460px;font-size:100px">דודי 🆚 <span class="k">החייזר</span></div>''',
    NEWS + '''<div class="c card" style="top:330px"><div class="big" style="font-size:96px">👨‍⚖️ מחפשים<br><span class="k">שופטים!</span></div><div class="mid" style="font-size:50px">כבר 3 מועמדים · כתבו "שופט" 👇</div></div>''' + LOW('הכי אהובים עולים להצבעה!') + TICK,
    '''<div class="c" style="top:260px"><div class="pill">🎤 אודישן מוקדם</div></div>
       <div class="c card" style="top:1330px"><div class="mid ltr k" style="font-size:64px">NissoC</div><div class="mid">שיר מקורי משלו:</div>
       <div class="big k" style="font-size:110px">״מי אני״</div><div class="mid" style="font-size:42px">✅/❌ הצביעו באולפן – הקישור בביו</div></div>''',
    '''<div class="c card" style="top:280px"><div class="big" style="font-size:110px">מי <span class="k">ניצח?</span></div><div class="mid">דודי 🕺 או החייזר 👽</div></div>
       <div class="c" style="top:1560px"><div class="cta" style="font-size:50px">כתבו בתגובות 👇<br>הכי הרבה לייקים קובע את מחר</div></div>''',
]
COVER = '''<div style="position:absolute;inset:0;background:linear-gradient(180deg,#0000 20%,#0008 45%,#0000 60%,#000a 100%)"></div>
 <div class="c" style="top:440px"><div class="pill" style="font-size:58px">👽 פרק חדש</div></div>
 <div class="c big" style="top:560px;font-size:112px">חייזר <span class="k">באולפן!</span></div>
 <div class="c mid" style="top:1300px;font-size:56px">🕺 קרב ריקודים · 🎤 NissoC</div>'''

def overlays():
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
        for i, h in enumerate(SC):
            pg.set_content(f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{h}</body></html>'); pg.wait_for_timeout(250)
            pg.screenshot(path=f'{E}/ov3d{i}.png', omit_background=True)
        b.close()

def cover(bgjpg):
    import base64
    bg = base64.b64encode(open(bgjpg, 'rb').read()).decode()
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
        pg.set_content(f'<html><head><meta charset="utf-8"><style>{CSS} body{{background:url(data:image/jpeg;base64,{bg}) center/cover}}</style></head><body>{COVER}</body></html>'); pg.wait_for_timeout(300)
        pg.screenshot(path=f'{E}/cover.jpg', type='jpeg', quality=92); b.close()

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: raise SystemExit(r.stderr[-2000:])

def audio():
    fl = []
    for k, ((src, a, b), st) in enumerate(zip(SEG, starts)):
        fl.append(f"[{0 if src=='n' else 1}:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={b-a-0.03:.3f}:d=0.03,adelay={int(st*1000)}|{int(st*1000)}[a{k}]")
    mix = ''.join(f'[a{k}]' for k in range(len(SEG)))
    d0, d1 = starts[7], starts[8]   # beat de danse pendant le קרב
    fl.append(f"aevalsrc='0.05*sin(2*PI*110*t)+0.035*sin(2*PI*164.8*t)+0.03*sin(2*PI*220*t)*(0.6+0.4*sin(2*PI*0.5*t))':s=44100:d={TOTAL:.3f},afade=t=in:d=1,afade=t=out:st={TOTAL-1.2:.3f}:d=1.2[pad]")
    fl.append(f"aevalsrc='0.55*sin(2*PI*55*t)*exp(-14*mod(t,0.5))+0.12*(random(0)*2-1)*exp(-40*mod(t+0.25,0.5))':s=44100:d={d1-d0:.3f},afade=t=out:st={d1-d0-0.4:.3f}:d=0.4,adelay={int(d0*1000)}|{int(d0*1000)}[beat]")
    fl.append(f"aevalsrc='0.3*sin(2*PI*(300+900*t)*t)*exp(-3*t)':s=44100:d=1.2,adelay={int(starts[3]*1000)}|{int(starts[3]*1000)}[ufo]")
    fl.append(f"{mix}amix=inputs={len(SEG)}:normalize=0[vo];[vo][pad][beat][ufo]amix=inputs=4:normalize=0,alimiter=limit=0.95,aresample=44100[out]")
    run(['ffmpeg', '-y', '-v', 'error', '-i', f'{E}/nimrod.mp3', '-i', f'{E}/danit.mp3', '-filter_complex', ';'.join(fl), '-map', '[out]', '-t', f'{TOTAL:.3f}', '-c:a', 'aac', '-b:a', '192k', f'{E}/audio.m4a'])

if __name__ == '__main__':
    print(json.dumps({'total': round(TOTAL, 3), 'starts': [round(s, 3) for s in starts], 'frames': frames}))
    if 'ov' in sys.argv: overlays()
    if 'audio' in sys.argv: audio()
