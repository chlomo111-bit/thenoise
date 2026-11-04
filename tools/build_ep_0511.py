"""Épisode 02/11 « החייזר על היען » : timeline des voix (découpe aux silences), overlays, audio."""
import importlib.util, subprocess, sys, json
from playwright.sync_api import sync_playwright
E = '/tmp/claude-0/ep4'; FPS = 30
spec = importlib.util.spec_from_file_location('b1', '/tmp/claude-0/ep/build.py'); B1 = importlib.util.module_from_spec(spec); spec.loader.exec_module(B1)
CSS = B1.CSS

# (source, début, fin) dans l'ordre de lecture
SEG = [
    ('n', 0.00, 4.26),    # 0 עצרו! חבר שמזייף במקלחת?
    ('n', 4.71, 8.70),    # 1 המתמודדים והשופטים = העוקבים
    ('n', 9.13, 14.87),   # 2 65 → 71, 50 כרטיסים לכולם
    ('d', 0.00, 4.38),    # 3 מבזק: 70 עוקבים – בונוס
    ('d', 4.77, 9.17),    # 4 החייזר מתאמן עם היען
    ('n', 15.41, 18.54),  # 5 ליאב בסכנה
    ('n', 19.13, 23.01),  # 6 האתגר: שלחו לחבר הכי מזייף
    ('n', 23.34, 28.39),  # 7 "אני מזייף" → אודישן + 50 לשניכם
    ('n', 28.72, 31.81),  # 8 למי אתם שולחים? תייגו
]
GAP = [0.20, 0.20, 0.25, 0.25, 0.25, 0.25, 0.20, 0.25, 1.0]
LEAD = 0.15
starts = []; t = LEAD
for (s, a, b), g in zip(SEG, GAP):
    starts.append(t); t += (b - a) + g
TOTAL = t
bounds = [0.0] + starts[1:] + [TOTAL]
frames = [round(bounds[i + 1] * FPS) - round(bounds[i] * FPS) for i in range(len(SEG))]
BURSTS = [starts[2] + 2.0, starts[7] + 2.5]

NEWS = '<div class="flash">⚡ מבזק</div><div class="live"><i></i>LIVE · קומה 24</div>'
TICK = '<div class="tick">📲 שלחו לחבר הכי מזייף · "אני מזייף" = אודישן + 50 🎟️ · 🎁 הגרלה ב־20:00 · 👨‍⚖️ מחפשים שופטים ·</div>'
LOW = lambda b: f'<div class="low"><span class="n">דנית · החדשות של The Noise</span><div class="b">{b}</div></div>'
SC = [
    """<div class="c" style="top:250px"><div class="pill" style="font-size:66px">✋ עצרו!</div></div>
       <div class="c card" style="top:1300px"><div class="big" style="font-size:96px">יש לכם חבר<br>ש<span class="k">מזייף</span> במקלחת? 🚿</div></div>""",
    """<div class="c card" style="top:280px"><div class="mid">המתמודדים + השופטים</div><div class="big" style="font-size:120px">= <span class="k">אתם!</span> 🫵</div></div>""",
    """<div class="c" style="top:260px"><div class="pill">📈 אתמול → היום</div></div>
       <div class="c card" style="top:1330px"><div class="big ltr" style="font-size:140px">65 → <span class="k">71</span></div><div class="mid">+50 🎟️ מתנה לכל השחקנים 🎉</div></div>""",
    NEWS + """<div class="c card" style="top:330px"><div class="big" style="font-size:100px">🎉 <span class="ltr">70</span> עוקבים</div><div class="mid">בונוס לכל השחקנים!</div></div>""" + LOW('70 עוקבים באולפן – כולם קיבלו 50 🎟️') + TICK,
    NEWS + """<div class="c card" style="top:330px"><div class="big" style="font-size:96px">👽 החייזר<br><span class="k">מתאמן…</span></div><div class="mid">עם היען 🦤</div></div>""" + LOW('מאחורי הקלעים: הכנות לקרב חוזר') + TICK,
    """<div class="c" style="top:260px"><div class="pill" style="font-size:60px">😬 ליאב בסכנה</div></div>
       <div class="c mid" style="top:1500px">כמעט אף אחד <span class="k">לא הצביע…</span></div>""",
    """<div class="c card" style="top:1300px"><div class="mid">📲 האתגר:</div><div class="big" style="font-size:92px">שלחו לחבר<br>ה<span class="k">הכי מזייף</span> שלכם</div></div>""",
    """<div class="c card" style="top:270px"><div class="mid">הוא כותב בתגובות</div><div class="big k" style="font-size:110px">״אני מזייף״</div><div class="mid">🎤 אודישן + 50 🎟️ לשניכם!</div></div>""",
    """<div class="c card" style="top:280px"><div class="big" style="font-size:100px">למי אתם<br><span class="k">שולחים?</span> 📲</div></div>
       <div class="c" style="top:1560px"><div class="cta" style="font-size:52px">👇 תייגו אותו עכשיו</div></div>""",
]
COVER = '''<div style="position:absolute;inset:0;background:linear-gradient(180deg,#0000 20%,#0008 45%,#0000 60%,#000a 100%)"></div>
 <div class="c" style="top:440px"><div class="pill" style="font-size:58px">🚿 אתגר חדש</div></div>
 <div class="c card" style="top:560px"><div class="big" style="font-size:104px">שלחו לחבר<br>ה<span class="k">הכי מזייף!</span></div></div>
 <div class="c" style="top:1240px"><div class="cta" style="font-size:52px">״אני מזייף״ = אודישן + 50 🎟️</div></div>'''

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
    d0, d1 = starts[7], starts[8]   # beat sur le défi
    fl.append(f"aevalsrc='0.05*sin(2*PI*110*t)+0.035*sin(2*PI*164.8*t)+0.03*sin(2*PI*220*t)*(0.6+0.4*sin(2*PI*0.5*t))':s=44100:d={TOTAL:.3f},afade=t=in:d=1,afade=t=out:st={TOTAL-1.2:.3f}:d=1.2[pad]")
    fl.append(f"aevalsrc='0.55*sin(2*PI*55*t)*exp(-14*mod(t,0.5))+0.12*(random(0)*2-1)*exp(-40*mod(t+0.25,0.5))':s=44100:d={d1-d0:.3f},afade=t=out:st={d1-d0-0.4:.3f}:d=0.4,adelay={int(d0*1000)}|{int(d0*1000)}[beat]")
    fl.append(f"aevalsrc='0.3*sin(2*PI*(300+900*t)*t)*exp(-3*t)':s=44100:d=1.2,adelay={int(BURSTS[0]*1000)}|{int(BURSTS[0]*1000)}[ufo]")
    fl.append(f"{mix}amix=inputs={len(SEG)}:normalize=0[vo];[vo][pad][beat][ufo]amix=inputs=4:normalize=0,alimiter=limit=0.95,aresample=44100[out]")
    run(['ffmpeg', '-y', '-v', 'error', '-i', f'{E}/nimrod.mp3', '-i', f'{E}/danit.mp3', '-filter_complex', ';'.join(fl), '-map', '[out]', '-t', f'{TOTAL:.3f}', '-c:a', 'aac', '-b:a', '192k', f'{E}/audio.m4a'])

if __name__ == '__main__':
    print(json.dumps({'total': round(TOTAL, 3), 'starts': [round(s, 3) for s in starts], 'frames': frames}))
    if 'ov' in sys.argv: overlays()
    if 'audio' in sys.argv: audio()
