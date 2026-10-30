"""Post « ça commence bientôt » (1080×1350) avec le vrai nombre d'abonnés.
Usage : python3 tools/post_soon.py <abonnés> <sortie.jpg> [objectif=50]
Fond = post_du_jour du 30/10 (assombri/flouté), style Heebo très gras blanc + #FFC24B.
"""
import asyncio, base64, sys, pathlib
from playwright.async_api import async_playwright

n = int(sys.argv[1]); out = sys.argv[2]; goal = int(sys.argv[3]) if len(sys.argv) > 3 else 50
left = max(0, goal - n); pct = max(4, round(n / goal * 100))
root = pathlib.Path(__file__).resolve().parent.parent
font = base64.b64encode((root / "tools/fonts/Heebo.ttf").read_bytes()).decode()
bg = base64.b64encode((root / "media/2026-10-30/post_du_jour.jpg").read_bytes()).decode()

html = f"""<!doctype html><html dir="rtl" lang="he"><head><meta charset="utf-8">
<style>
@font-face{{font-family:Heebo;src:url(data:font/ttf;base64,{font}) format("truetype");font-weight:100 900}}
*{{box-sizing:border-box}}body{{margin:0;width:1080px;height:1350px;font-family:Heebo,sans-serif;color:#fff;overflow:hidden;position:relative;background:#05030a}}
.bg{{position:absolute;inset:-40px;background:url(data:image/jpeg;base64,{bg}) center/cover;filter:blur(18px) brightness(.45) saturate(1.2)}}
.wrap>*{{flex-shrink:0}}.wrap{{position:relative;height:100%;display:flex;flex-direction:column;align-items:center;padding:86px 90px 60px;text-align:center}}
.pill{{background:#e0242b;border-radius:999px;padding:14px 40px;font-weight:900;font-size:40px;box-shadow:0 0 40px rgba(224,36,43,.55)}}
h1{{font-weight:900;font-size:96px;line-height:1.05;margin:46px 0 8px;letter-spacing:-1px}}h1 .k,.k{{color:#FFC24B}}
.sub{{font-weight:800;font-size:44px;opacity:.95;margin:0 0 40px}}
.cnt{{font-weight:900;font-size:120px;line-height:1;direction:ltr}}.cnt small{{font-size:64px;opacity:.85}}
.bar{{width:100%;height:46px;border-radius:999px;background:rgba(255,255,255,.12);border:2px solid rgba(255,194,75,.5);margin:22px 0 46px;overflow:hidden;display:flex;justify-content:flex-start}}
.bar i{{display:block;height:100%;width:{pct}%;background:linear-gradient(270deg,#FFC24B,#ff5a5a);border-radius:999px}}
.row{{width:100%;border:3px solid rgba(255,194,75,.75);border-radius:30px;background:rgba(10,6,16,.55);font-weight:900;font-size:46px;padding:24px 30px;margin-bottom:22px}}
.row span{{direction:ltr;unicode-bidi:isolate}}
.cta{{margin-top:auto;background:#FFC24B;color:#111;border-radius:999px;padding:22px 60px;font-weight:900;font-size:54px}}
.ft{{margin-top:26px;font-weight:500;font-size:32px;opacity:.85;direction:ltr}}
</style></head><body><div class="bg"></div><div class="wrap">
<div class="pill">🎤 The Noise · בקרוב</div>
<h1>חסרים לנו עוד <span class="k">{left}</span><br>כדי להתחיל!</h1>
<div class="sub">כשהאולם מתמלא – בוחרים שופטים ונפתחים האודישנים 🎶</div>
<div class="cnt">{n} <small>/ {goal}</small></div>
<div class="bar"><i></i></div>
<div class="row">1️⃣ עקבו אחרי <span>@the_noise_2026</span></div>
<div class="row">2️⃣ שתפו בסטורי ותייגו חבר שמזייף 🎤</div>
<div class="cta">עזרו לנו למלא את האולם 🙏</div>
<div class="ft">@the_noise_2026 · thenoise.hakaveret.online</div>
</div></body></html>"""

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1080, "height": 1350})
        await pg.set_content(html); await pg.wait_for_timeout(1500)
        await pg.screenshot(path=out, type="jpeg", quality=92); await b.close()

asyncio.run(main())
