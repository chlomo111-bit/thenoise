import asyncio, base64, json, os, subprocess, math
from playwright.async_api import async_playwright
E = '/tmp/claude-0/ep'
R = '/home/claude/thenoise'
FPS = 30
font = base64.b64encode(open(f'{R}/tools/fonts/Heebo.ttf', 'rb').read()).decode()

# ---- audio segments (source, start, end) in play order ----
SEG = [
    ('n', 0.00, 5.28),   # 1 בפרק הקודם
    ('d', 0.00, 6.38),   # 2 מבזק
    ('d', 6.70, 13.98),  # 3 עברנו את החמישים
    ('n', 5.73, 11.97),  # 4a ערב המסכות … היה…
    ('n', 11.97, 12.55), # 4b הראל!
    ('n', 12.75, 15.60), # 5 שלושים כרטיסים
    ('n', 15.88, 21.63), # 6 שחר סטארבקס
    ('d', 14.19, 18.61), # 7 מחפשים שופטים
    ('n', 22.11, 26.47), # 8 בפרק הבא
    ('n', 26.84, 29.72), # 9 מה יקרה מחר
]
GAP = [0.25, 0.25, 0.30, 0.0, 0.70, 0.25, 0.30, 0.30, 0.30, 0.9]  # pause after each segment
LEAD = 0.30
starts = []; t = LEAD
for (src, a, b), g in zip(SEG, GAP):
    starts.append(t); t += (b - a) + g
TOTAL = t
# scene boundaries = segment starts (scene 0 begins at 0)
bounds = [0.0] + starts[1:] + [TOTAL]
frames = [round(bounds[i + 1] * FPS) - round(bounds[i] * FPS) for i in range(len(SEG))]

BG = {'studio': f'{E}/bg_chars.jpg', 'blur': f'{E}/bg_blur.jpg', 'news': f'{E}/plateau_bg.png'}
CSS = f'''@font-face{{font-family:Heebo;src:url(data:font/ttf;base64,{font}) format("truetype");font-weight:100 900}}
*{{box-sizing:border-box}}html,body{{margin:0;width:1080px;height:1920px;background:transparent;font-family:Heebo,sans-serif;color:#fff;overflow:hidden}}body>*{{direction:rtl}}
.k{{color:#FFC24B}}.c{{position:absolute;left:70px;right:70px;text-align:center}}
.pill{{display:inline-block;background:#e1252d;color:#fff;font-weight:900;font-size:52px;padding:12px 40px;border-radius:999px;box-shadow:0 8px 34px #e1252d99}}
.big{{font-weight:900;font-size:118px;line-height:1.05;text-shadow:0 8px 40px #000c}}
.mid{{font-weight:900;font-size:62px;line-height:1.25;text-shadow:0 6px 30px #000c}}
.card{{background:rgba(10,6,16,.82);border:4px solid #FFC24B;border-radius:40px;padding:40px 36px;box-shadow:0 20px 70px #000c}}
.ltr{{direction:ltr;unicode-bidi:isolate}}
.flash{{position:absolute;top:150px;right:60px;background:#e1252d;font-weight:900;font-size:58px;padding:10px 34px;border-radius:10px}}
.live{{position:absolute;top:166px;left:60px;font-weight:900;font-size:40px;direction:ltr}}.live i{{display:inline-block;width:24px;height:24px;border-radius:50%;background:#e1252d;margin-right:12px;vertical-align:middle}}
.low{{position:absolute;bottom:250px;left:0;right:0}}.low .n{{display:inline-block;margin-right:60px;background:#fff;color:#111;font-weight:900;font-size:44px;padding:10px 28px;border-radius:10px 10px 0 0}}
.low .b{{background:#e1252d;font-weight:900;font-size:56px;padding:20px 60px}}
.tick{{position:absolute;bottom:170px;left:0;right:0;background:#111;color:#FFC24B;font-weight:900;font-size:36px;padding:16px 60px;white-space:nowrap;overflow:hidden}}
.cta{{display:inline-block;background:#FFC24B;color:#111;font-weight:900;font-size:60px;padding:24px 56px;border-radius:999px}}
'''
NEWS_HUD = '<div class="flash">⚡ מבזק</div><div class="live"><i></i>LIVE · קומה 24</div>'
TICK = '<div class="tick">🎤 אודישנים מוקדמים · 🎭 ערב המסכות · 🎁 הגרלה ב־20:00 – הזוכה מחליט מה יקרה מחר · 👨‍⚖️ מחפשים שופטים ·</div>'
SC = [
    ('studio', .45, '''<div class="c" style="top:300px"><div class="pill">⏪ בפרק הקודם…</div></div>
     <div class="c card" style="top:440px"><div class="big">האולם היה<br><span class="k">חצי ריק</span> 🪑</div></div>'''),
    ('news', 1, NEWS_HUD + '''<div class="c card" style="top:330px"><div class="mid">משהו שלא קרה</div><div class="big k" style="font-size:104px">באף עונה!</div></div>
     <div class="low"><span class="n">דנית · החדשות של The Noise</span><div class="b">התוכנית מתחילה לפני שהאולם מלא!</div></div>''' + TICK),
    ('news', 1, NEWS_HUD + '''<div class="c card" style="top:330px"><div class="big" style="font-size:190px">56 <span class="k">🎉</span></div><div class="mid">עוקבים – <span class="k">עברנו את ה־50!</span></div></div>
     <div class="low"><span class="n">דנית · החדשות של The Noise</span><div class="b">האולם מתמלא 🪑</div></div>''' + TICK),
    ('blur', 1, '''<div class="c" style="top:280px"><div class="pill">🎭 ערב המסכות</div></div>
     <div class="c" style="top:560px;font-size:330px">🎭</div>
     <div class="c big" style="top:1080px">מי מתחת<br>ל<span class="k">מסכת הזהב?</span></div>
     <div class="c mid" style="top:1430px;font-size:44px">רעיון של <span class="ltr">@shahar_b.y</span> 💡</div>'''),
    ('blur', 1, '''<div class="c" style="top:280px"><div class="pill">🎭 הוסרה המסכה!</div></div>
     <div class="c big" style="top:700px;font-size:150px">זה <span class="k">הראל!</span></div>
     <div class="c mid" style="top:960px"><span class="ltr k">@harel.2002</span></div>'''),
    ('blur', 1, '''<div class="c card" style="top:700px"><div class="big" style="font-size:170px"><span class="ltr">+30</span> 🎟️</div><div class="mid">לכל מי שניחש נכון!</div></div>'''),
    ('studio', .6, '''<div class="c" style="top:260px"><div class="pill">🎤 אודישן מוקדם</div></div>
     <div class="c card" style="top:1150px"><div class="mid ltr k" style="font-size:72px">@shahar_b.y</div><div class="mid">🎵 סטארבקס – עדן גולן ושרק</div>
     <div class="big" style="font-size:96px;margin-top:14px">✅ נשארת?<br>❌ הולכת?</div><div class="mid" style="font-size:42px;margin-top:12px">הצביעו באולפן – הקישור בביו</div></div>'''),
    ('news', 1, NEWS_HUD + '''<div class="c card" style="top:330px"><div class="big" style="font-size:96px">👨‍⚖️ מחפשים<br><span class="k">שופטים!</span></div><div class="mid" style="font-size:52px">כתבו "שופט" בתגובות 👇<br>8 הכי אהובים → הצבעה</div></div>
     <div class="low"><span class="n">דנית · החדשות של The Noise</span><div class="b">ההרשמה לשופטים נפתחה!</div></div>''' + TICK),
    ('blur', .7, '''<div class="c" style="top:300px"><div class="pill" style="background:#222;box-shadow:none">⏩ בפרק הבא…</div></div>
     <div class="c big" style="top:720px">זמר <span class="k">אמיתי</span> 🎤</div>
     <div class="c mid" style="top:900px">שיר מקורי משלו:</div>
     <div class="c big k" style="top:1000px;font-size:140px">״מי אני״</div>
     <div class="c mid" style="top:1210px;font-size:46px">NissoC · <span class="ltr">@habama.hamerkazit</span></div>'''),
    ('studio', .4, '''<div class="c card" style="top:300px"><div class="big">מה יקרה<br><span class="k">מחר?</span></div></div>
     <div class="c" style="top:1560px"><div class="cta" style="font-size:52px">התגובה עם הכי הרבה<br>לייקים קובעת 👇</div></div>'''),
]
COVER = '''<div style="position:absolute;inset:0;background:linear-gradient(180deg,#0009 0%,#0000 35%,#0000 55%,#000c 100%)"></div>
 <div class="c" style="top:200px"><div class="pill" style="font-size:64px">⚡ מבזק</div></div>
 <div class="c big" style="top:360px">משהו שלא קרה<br><span class="k">באף עונה!</span></div>
 <div class="c mid" style="top:1500px;font-size:58px">🎭 ערב המסכות · 🎤 אודישנים · 👨‍⚖️ שופטים</div>'''

async def render():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': 1080, 'height': 1920})
        for i, (_, _, html) in enumerate(SC):
            await pg.set_content(f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{html}</body></html>')
            await pg.wait_for_timeout(300)
            await pg.screenshot(path=f'{E}/ov{i}.png', omit_background=True)
        bgd = base64.b64encode(open(BG['studio'], 'rb').read()).decode()
        await pg.set_content(f'<html><head><meta charset="utf-8"><style>{CSS} body{{background:url(data:image/jpeg;base64,{bgd}) center/cover}}</style></head><body>{COVER}</body></html>')
        await pg.wait_for_timeout(300)
        await pg.screenshot(path=f'{E}/cover.jpg', type='jpeg', quality=92)
        await b.close()

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: raise SystemExit(r.stderr[-2000:])

def scenes():
    lst = []
    for i, ((bgk, dim, _), n) in enumerate(zip(SC, frames)):
        d = n / FPS
        zf = 'min(1+0.0009*on,1.15)'
        vf = (f"[0:v]scale=1188:2112,zoompan=z='{zf}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps={FPS},"
              f"eq=brightness={-0.5*(1-dim):.2f},trim=end_frame={n},setpts=PTS-STARTPTS[bg];"
              f"[1:v]format=rgba,fade=t=in:st=0:d=0.22:alpha=1[o];[bg][o]overlay=0:0:format=auto,format=yuv420p[v]")
        out = f'{E}/s{i}.mp4'; tmp = f'{E}/s{i}.tmp.mp4'
        run(['ffmpeg', '-y', '-v', 'error', '-loop', '1', '-framerate', str(FPS), '-i', BG[bgk], '-loop', '1', '-framerate', str(FPS), '-i', f'{E}/ov{i}.png',
             '-filter_complex', vf, '-map', '[v]', '-frames:v', str(n), '-r', str(FPS), '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', tmp])
        os.replace(tmp, out); lst.append(out)
    open(f'{E}/list.txt', 'w').write(''.join(f"file '{x}'\n" for x in lst))
    run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', f'{E}/list.txt', '-c', 'copy', f'{E}/video.mp4'])

def audio():
    parts = []; fl = []
    for k, ((src, a, b), st) in enumerate(zip(SEG, starts)):
        fl.append(f"[{0 if src=='n' else 1}:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={b-a-0.03:.3f}:d=0.03,adelay={int(st*1000)}|{int(st*1000)}[a{k}]")
    mix = ''.join(f'[a{k}]' for k in range(len(SEG)))
    # light music bed (pad) + sting at the mask reveal
    rev = starts[4]
    fl.append(f"aevalsrc='0.05*sin(2*PI*110*t)+0.035*sin(2*PI*164.8*t)+0.03*sin(2*PI*220*t)*(0.6+0.4*sin(2*PI*0.5*t))':s=44100:d={TOTAL:.3f},afade=t=in:d=1,afade=t=out:st={TOTAL-1.2:.3f}:d=1.2[pad]")
    fl.append(f"aevalsrc='0.35*sin(2*PI*(880+600*t)*t)*exp(-4*t)':s=44100:d=0.8,adelay={int(rev*1000)}|{int(rev*1000)}[st]")
    fl.append(f"{mix}amix=inputs={len(SEG)}:normalize=0[vo];[vo][pad][st]amix=inputs=3:normalize=0,alimiter=limit=0.95,aresample=44100[out]")
    run(['ffmpeg', '-y', '-v', 'error', '-i', f'{E}/nimrod.mp3', '-i', f'{E}/danit.mp3', '-filter_complex', ';'.join(fl), '-map', '[out]', '-t', f'{TOTAL:.3f}', '-c:a', 'aac', '-b:a', '192k', f'{E}/audio.m4a'])

if __name__ == '__main__':
    import sys
    print(json.dumps({'total': TOTAL, 'starts': [round(s, 3) for s in starts], 'frames': frames}))
    asyncio.run(render())
    if 'render' in sys.argv: raise SystemExit
    scenes(); audio()
    run(['ffmpeg', '-y', '-v', 'error', '-i', f'{E}/video.mp4', '-i', f'{E}/audio.m4a', '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'copy', '-shortest', '-movflags', '+faststart', f'{E}/final.mp4'])
    print('ok')
