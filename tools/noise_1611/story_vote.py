"""Story image The Noise 16.11 : question « תענו 1 או 2 » + prénoms des joueurs, sur une image du plateau 3D.
Usage : python3 story_vote.py <image_fond> <sortie.jpg>"""
import sys, base64
from playwright.sync_api import sync_playwright
bg, out = sys.argv[1:3]
F = '/root/three3/node_modules/@fontsource/heebo/files/'
b = lambda p: base64.b64encode(open(p, 'rb').read()).decode()
H = f"""<html><head><meta charset=utf-8><style>@font-face{{font-family:H;font-weight:900;src:url(data:font/woff2;base64,{b(F+'heebo-hebrew-900-normal.woff2')})}}
@font-face{{font-family:H;font-weight:900;src:url(data:font/woff2;base64,{b(F+'heebo-latin-900-normal.woff2')});unicode-range:U+0000-00FF}}
body{{margin:0;width:540px;height:960px;position:relative;overflow:hidden;font-family:H;direction:rtl;color:#fff;background:#120a1c}}
img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:brightness(.8)}}
.c{{position:absolute;left:0;right:0;text-align:center;padding:0 24px;text-shadow:0 3px 14px rgba(0,0,0,.95)}}
.box{{display:inline-block;background:rgba(10,6,20,.8);border-radius:22px;padding:10px 22px}}
.btn{{display:inline-block;width:40%;margin:0 8px;border-radius:24px;padding:14px 0;font:900 34px/1.2 H;text-shadow:none}}
.y{{color:#FFC24B}}.tag{{display:inline-block;background:#FFC24B;color:#140c04;border-radius:999px;padding:6px 18px;font:900 22px H;text-shadow:none}}
</style></head><body><img src="data:image/jpeg;base64,{b(bg)}">
<div class=c style="top:7%"><span class=tag>🎤 THE NOISE · השאלה של היום</span></div>
<div class=c style="top:15%"><div class=box style="font:900 44px/1.2 H">איפה אתם <span class=y>מזייפים</span><br>הכי חזק? 🎶😂</div></div>
<div class=c style="top:47%"><span class=btn style="background:#2d6cdf">1️⃣<br>במקלחת 🚿</span><span class=btn style="background:#E01F26">2️⃣<br>באוטו 🚗</span></div>
<div class=c style="top:66%"><div class=box style="font:900 30px/1.3 H">תענו <span class=y>1 או 2</span> 👇<br>🎙️ או שלחו לנו הודעה קולית</div></div>
<div class=c style="bottom:8%"><div class=box style="font:900 22px/1.4 H">על הבמה: <span dir=ltr>@bdvy214</span> 🎤<br>הצביעו: <span dir=ltr>@gili.lev29 · @jewels_by_girlz</span></div></div>
</body></html>"""
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page(viewport={'width': 540, 'height': 960}, device_scale_factor=2)
    pg.set_content(H); pg.wait_for_timeout(500); pg.screenshot(path=out, type='jpeg', quality=92); br.close()
