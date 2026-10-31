"""Stories 1080×1920 The Noise.
Usage : python3 tools/story_soon.py <mode> <abonnés> <sortie.jpg> [objectif=50]
  mode = teaser  -> « הערב ב־19:00 עולה הפרק הראשון »
  mode = soon    -> « חסרים לנו עוד X כדי להתחיל » + barre de progression
Fond = cover_collab.jpg (ou post du jour) assombri/flouté, Heebo embarqué, blanc + #FFC24B.
"""
import asyncio, base64, sys, pathlib
from playwright.async_api import async_playwright

mode = sys.argv[1]; n = int(sys.argv[2]); out = sys.argv[3]; goal = int(sys.argv[4]) if len(sys.argv) > 4 else 50
left = max(0, goal - n); pct = max(4, round(n / goal * 100))
root = pathlib.Path(__file__).resolve().parent.parent
font = base64.b64encode((root / "tools/fonts/Heebo.ttf").read_bytes()).decode()
bgp = root / "media/2026-10-31/cover_collab.jpg"
if not bgp.exists(): bgp = root / "media/2026-10-30/post_du_jour.jpg"
bg = base64.b64encode(bgp.read_bytes()).decode()

if mode == "launch":
    body = """<div class="pill">🔴 עכשיו בפרופיל</div>
<h1>The Noise<br><span class="k">התחיל!</span> 🎤</h1>
<div class="row">🐝 הדבורה &nbsp;·&nbsp; ⚓ הקפטן &nbsp;·&nbsp; 👵 סבתא מזל</div>
<div class="sub2">כבר באולם… ואתם? 🪑</div>
<div class="cta">הפרק החדש בפרופיל 👆</div>
<div class="sub2" style="direction:ltr;margin-top:50px">@the_noise_2026</div>"""
elif mode == "teaser":
    body = """<div class="pill">🎤 The Noise</div>
<h1>הערב<br>ב־<span class="k">19:00</span></h1>
<div class="sub">עולה הפרק הראשון של<br>התוכנית הכי מזייפת באינסטגרם 😂</div>
<div class="row">🐝 הדבורה &nbsp;·&nbsp; ⚓ הקפטן &nbsp;·&nbsp; 👵 סבתא מזל</div>
<div class="sub2">כבר יושבים באולם… ואתם? 🪑</div>
<div class="cta">הפעילו התראות 🔔</div>"""
else:
    body = f"""<div class="pill">🎤 The Noise · בקרוב</div>
<h1>חסרים לנו<br>עוד <span class="k">{left}</span>!</h1>
<div class="sub">כשהאולם מתמלא – בוחרים שופטים<br>ונפתחים האודישנים 🎶</div>
<div class="cnt">{n} <small>/ {goal}</small></div>
<div class="bar"><i></i></div>
<div class="row">1️⃣ עקבו אחרי <span>@the_noise_2026</span></div>
<div class="row">2️⃣ שתפו בסטורי ותייגו חבר שמזייף 🎤</div>
<div class="cta">עזרו לנו למלא את האולם 🙏</div>"""

html = f"""<!doctype html><html dir="rtl" lang="he"><head><meta charset="utf-8"><style>
@font-face{{font-family:Heebo;src:url(data:font/ttf;base64,{font}) format("truetype");font-weight:100 900}}
*{{box-sizing:border-box}}body{{margin:0;width:1080px;height:1920px;font-family:Heebo,sans-serif;color:#fff;overflow:hidden;position:relative;background:#05030a}}
.bg{{position:absolute;inset:-60px;background:url(data:image/jpeg;base64,{bg}) center/cover;filter:blur(16px) brightness(.42) saturate(1.2)}}
.wrap>*{{flex-shrink:0}}.wrap{{position:relative;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:260px 90px 300px;text-align:center}}
.pill{{background:#e0242b;border-radius:999px;padding:16px 46px;font-weight:900;font-size:46px;box-shadow:0 0 40px rgba(224,36,43,.55)}}
h1{{font-weight:900;font-size:150px;line-height:1.02;margin:50px 0 24px;letter-spacing:-2px}}.k{{color:#FFC24B}}
.sub{{font-weight:800;font-size:52px;line-height:1.3;margin:0 0 50px}}.sub2{{font-weight:800;font-size:54px;margin:10px 0 60px}}
.cnt{{font-weight:900;font-size:150px;line-height:1;direction:ltr}}.cnt small{{font-size:80px;opacity:.85}}
.bar{{width:100%;height:56px;border-radius:999px;background:rgba(255,255,255,.12);border:2px solid rgba(255,194,75,.5);margin:26px 0 56px;overflow:hidden;display:flex}}
.bar i{{display:block;height:100%;width:{pct}%;background:linear-gradient(270deg,#FFC24B,#ff5a5a);border-radius:999px}}
.row{{width:100%;border:3px solid rgba(255,194,75,.75);border-radius:34px;background:rgba(10,6,16,.6);font-weight:900;font-size:44px;padding:28px 24px;margin-bottom:26px;white-space:nowrap}}
.row span{{direction:ltr;unicode-bidi:isolate}}
.cta{{margin-top:30px;background:#FFC24B;color:#111;border-radius:999px;padding:26px 64px;font-weight:900;font-size:60px}}
</style></head><body><div class="bg"></div><div class="wrap">{body}</div></body></html>"""

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        await pg.set_content(html); await pg.wait_for_timeout(1200)
        await pg.screenshot(path=out, type="jpeg", quality=92); await b.close()

asyncio.run(main())
