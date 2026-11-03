"""Épisode 02/11 « החייזר על היען » : timeline des voix (découpe aux silences), overlays, audio."""
import importlib.util, subprocess, sys, json
from playwright.sync_api import sync_playwright
E = '/tmp/claude-0/ep3'; FPS = 30
spec = importlib.util.spec_from_file_location('b1', '/tmp/claude-0/ep/build.py'); B1 = importlib.util.module_from_spec(spec); spec.loader.exec_module(B1)
CSS = B1.CSS

# (source, début, fin) dans l'ordre de lecture
SEG = [
    ('n', 0.00, 8.27),    # 0 ברוכים הבאים – המתמודדים והשופטים = העוקבים
    ('n', 8.68, 12.86),   # 1 אתמול 65 – היום 69
    ('n', 13.10, 19.73),  # 2 שני מתמודדים עברו… ארבעה מועמדים לשופטים
    ('d', 0.00, 5.39),    # 3 מבזק: התגובה של היום – חד משמעית דודי זוכה
    ('d', 5.84, 10.00),   # 4 החייזר מתאמן לקרב חוזר
    ('n', 20.13, 26.44),  # 5 NissoC – מי אני – 3 וי
    ('n', 26.90, 32.11),  # 6 קרב הריקודים – אני ניצחתי… החייזר
    ('n', 32.61, 35.18),  # 7 הגרלה – אף אחד – הכתר מחכה
    ('n', 35.49, 39.41),  # 8 הערב ליאב – אמינם – נשאר או הולך
    ('n', 40.09, 46.06),  # 9 עוד עוקב אחד – 50 כרטיסים – מי יהיה ה־70
]
GAP = [0.30, 0.30, 0.30, 0.30, 0.30, 0.30, 0.30, 0.40, 0.30, 0.90]
LEAD = 0.25
starts = []; t = LEAD
for (s, a, b), g in zip(SEG, GAP):
    starts.append(t); t += (b - a) + g
TOTAL = t
bounds = [0.0] + starts[1:] + [TOTAL]
frames = [round(bounds[i + 1] * FPS) - round(bounds[i] * FPS) for i in range(len(SEG))]
BURSTS = [starts[5] + (24.10 - 20.13), starts[6] + 1.2]

NEWS = '<div class="flash">⚡ מבזק</div><div class="live"><i></i>LIVE · קומה 24</div>'
TICK = '<div class="tick">🎤 הערב: ליאב עם Eminem · 👨‍⚖️ 4 מועמדים לשופטים · 🎁 הגרלה ב־20:00 · 🎉 70 עוקבים = 50 🎟️ לכולם ·</div>'
LOW = lambda b: f'<div class="low"><span class="n">דנית · החדשות של The Noise</span><div class="b">{b}</div></div>'
SC = [
    """<div class="c" style="top:260px"><div class="pill" style="font-size:58px">🎤 The Noise</div></div>
       <div class="c card" style="top:1330px"><div class="mid">המתמודדים <span class="k">וגם</span> השופטים</div><div class="big" style="font-size:100px">= <span class="k">העוקבים!</span></div></div>""",
    """<div class="c" style="top:260px"><div class="pill">📈 אתמול → היום</div></div>
       <div class="c card" style="top:1330px"><div class="big ltr" style="font-size:150px">65 → <span class="k">69</span></div><div class="mid">עוקבים באולם 👥</div></div>""",
    """<div class="c card" style="top:260px"><div class="mid" style="font-size:68px">✅ <span class="k">2</span> עברו את האודישן</div><div class="mid" style="font-size:68px">👨‍⚖️ <span class="k">4</span> מועמדים לשופטים</div></div>""",
    NEWS + """<div class="c card" style="top:330px"><div class="mid" style="font-size:46px">💬 התגובה של היום</div><div class="big" style="font-size:92px">״חד משמעית,<br><span class="k">דודי זוכה!</span>״</div><div class="mid ltr" style="font-size:42px">@habama.hamerkazit</div></div>""" + LOW('התגובה של היום – כמו שהבטחנו!') + TICK,
    NEWS + """<div class="c card" style="top:330px"><div class="big" style="font-size:96px">👽 החייזר<br><span class="k">מתאמן…</span></div><div class="mid">לקרב חוזר! 🕺</div></div>""" + LOW('מקורות באולפן: קרב חוזר בקרוב') + TICK,
    """<div class="c" style="top:260px"><div class="pill">⏪ אתמול</div></div>
       <div class="c card" style="top:1330px"><div class="mid ltr k" style="font-size:66px">NissoC · ״מי אני״</div><div class="big ltr" style="font-size:110px">✅3 · ❌0</div><div class="mid">עבר את האודישן! 🎉</div></div>""",
    """<div class="c" style="top:260px"><div class="pill" style="font-size:60px">🏆 דודי ניצח!</div></div>
       <div class="c mid" style="top:1500px">אבל החייזר… <span class="k">עוד לא סיים</span> 👽</div>""",
    """<div class="c card" style="top:300px"><div class="mid">🎁 ההגרלה של אתמול</div><div class="big" style="font-size:96px">אף אחד<br><span class="k">לא נכנס!</span></div><div class="mid">הכתר 👑 עדיין מחכה</div></div>""",
    """<div class="c" style="top:260px"><div class="pill">🎤 הערב באודישן</div></div>
       <div class="c card" style="top:1330px"><div class="big k" style="font-size:110px">ליאב</div><div class="mid ltr">Eminem – Till I Collapse</div><div class="big" style="font-size:80px">✅ נשאר? ❌ הולך?</div></div>""",
    """<div class="c card" style="top:280px"><div class="mid">עוד עוקב <span class="k">אחד</span> =</div><div class="big" style="font-size:110px">50 🎟️ <span class="k">לכולם!</span></div></div>
       <div class="c" style="top:1560px"><div class="cta" style="font-size:50px">מי יהיה העוקב ה־70? 👇<br>כתבו בתגובות</div></div>""",
]
COVER = '''<div style="position:absolute;inset:0;background:linear-gradient(180deg,#0000 20%,#0008 45%,#0000 60%,#000a 100%)"></div>
 <div class="c" style="top:440px"><div class="pill" style="font-size:58px">🎤 פרק חדש</div></div>
 <div class="c big" style="top:560px;font-size:108px">ליאב <span class="k">על הבמה!</span></div>
 <div class="c mid" style="top:1300px;font-size:54px">🏆 דודי ניצח · 🎁 הכתר מחכה</div>'''

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
    d0, d1 = starts[6], starts[7]   # beat pendant la danse de victoire
    fl.append(f"aevalsrc='0.05*sin(2*PI*110*t)+0.035*sin(2*PI*164.8*t)+0.03*sin(2*PI*220*t)*(0.6+0.4*sin(2*PI*0.5*t))':s=44100:d={TOTAL:.3f},afade=t=in:d=1,afade=t=out:st={TOTAL-1.2:.3f}:d=1.2[pad]")
    fl.append(f"aevalsrc='0.55*sin(2*PI*55*t)*exp(-14*mod(t,0.5))+0.12*(random(0)*2-1)*exp(-40*mod(t+0.25,0.5))':s=44100:d={d1-d0:.3f},afade=t=out:st={d1-d0-0.4:.3f}:d=0.4,adelay={int(d0*1000)}|{int(d0*1000)}[beat]")
    fl.append(f"aevalsrc='0.3*sin(2*PI*(300+900*t)*t)*exp(-3*t)':s=44100:d=1.2,adelay={int(BURSTS[0]*1000)}|{int(BURSTS[0]*1000)}[ufo]")
    fl.append(f"{mix}amix=inputs={len(SEG)}:normalize=0[vo];[vo][pad][beat][ufo]amix=inputs=4:normalize=0,alimiter=limit=0.95,aresample=44100[out]")
    run(['ffmpeg', '-y', '-v', 'error', '-i', f'{E}/nimrod.mp3', '-i', f'{E}/danit.mp3', '-filter_complex', ';'.join(fl), '-map', '[out]', '-t', f'{TOTAL:.3f}', '-c:a', 'aac', '-b:a', '192k', f'{E}/audio.m4a'])

if __name__ == '__main__':
    print(json.dumps({'total': round(TOTAL, 3), 'starts': [round(s, 3) for s in starts], 'frames': frames}))
    if 'ov' in sys.argv: overlays()
    if 'audio' in sys.argv: audio()
