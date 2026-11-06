"""Post du jour 1080×1350 The Noise (loterie sans argent).
Usage : python3 tools/post_jour.py <sortie.jpg> "<ligne événement du jour>"
"""
import asyncio, base64, sys, pathlib, os
from playwright.async_api import async_playwright
out = sys.argv[1]; event = sys.argv[2] if len(sys.argv) > 2 else ""; credit = sys.argv[3] if len(sys.argv) > 3 else ""
PILL = os.environ.get("PILL", "🎁 ההגרלה של הערב · 20:00")
root = pathlib.Path(__file__).resolve().parent.parent
font = base64.b64encode((root / "tools/fonts/Heebo.ttf").read_bytes()).decode()
bg = base64.b64encode((root / "media/2026-10-31/cover_collab.jpg").read_bytes()).decode()
ev = (f'<div class="ev">{event}' + (f'<small>רעיון של <span>@{credit}</span> 💡</small>' if credit else '') + '</div>') if event else ""
html = f"""<!doctype html><html dir="rtl" lang="he"><head><meta charset="utf-8"><style>
@font-face{{font-family:Heebo;src:url(data:font/ttf;base64,{font}) format("truetype");font-weight:100 900}}
*{{box-sizing:border-box}}body{{margin:0;width:1080px;height:1350px;font-family:Heebo,sans-serif;color:#fff;overflow:hidden;position:relative;background:#05030a}}
.clip{{position:absolute;inset:0;overflow:hidden}}.bg{{position:absolute;inset:-40px;background:url(data:image/jpeg;base64,{bg}) center/cover;filter:blur(14px) brightness(.42) saturate(1.2)}}
.wrap>*{{flex-shrink:0}}.wrap{{position:relative;height:100%;display:flex;flex-direction:column;align-items:center;padding:80px 80px 56px;text-align:center}}
.pill{{background:#e0242b;border-radius:999px;padding:14px 40px;font-weight:900;font-size:40px;box-shadow:0 0 40px rgba(224,36,43,.55)}}
h1{{font-weight:900;font-size:104px;line-height:1.04;margin:40px 0 26px;letter-spacing:-1px}}.k{{color:#FFC24B}}
.ev small{{display:block;font-size:32px;font-weight:700;opacity:.9;margin-top:6px}}.ev small span{{direction:ltr;unicode-bidi:isolate}}.ev{{background:rgba(255,194,75,.16);border:3px dashed #FFC24B;border-radius:28px;padding:20px 26px;font-weight:900;font-size:44px;margin-bottom:34px}}
.row{{width:100%;border:3px solid rgba(255,194,75,.75);border-radius:30px;background:rgba(10,6,16,.6);font-weight:900;font-size:38px;padding:22px 18px;margin-bottom:20px;white-space:nowrap;overflow:hidden}}
.cta{{margin-top:auto;background:#FFC24B;color:#111;border-radius:999px;padding:22px 70px;font-weight:900;font-size:58px}}
.ft{{margin-top:22px;font-weight:500;font-size:30px;opacity:.85;direction:ltr}}
</style></head><body><div class="clip"><div class="bg"></div></div><div class="wrap">
<div class="pill">{PILL}</div>
<h1>מי יחליט מה<br>יקרה <span class="k">מחר</span> באולפן?</h1>
{ev}
<div class="row">✅ חדש: מספיק להגיב על הפוסט כדי להיכנס!</div>
<div class="row">🎟️ 100 כרטיסים באולפן = כפול סיכוי</div>
<div class="row">🏆 הזוכה: <span dir="ltr">+300 🎟️</span> · כתר 👑 · מחליט מה יקרה מחר</div>
<div class="cta">הגיבו כאן 👇</div>
<div class="ft">@the_noise_2026 · thenoise.hakaveret.online</div>
</div></body></html>"""
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1080, "height": 1350})
        await pg.set_content(html); await pg.wait_for_timeout(1200)
        await pg.screenshot(path=out, type="jpeg", quality=92); await b.close()
asyncio.run(main())
