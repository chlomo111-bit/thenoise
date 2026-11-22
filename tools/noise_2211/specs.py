"""Specs du reel « המקהלה הכי מזייפת בעולם? » חלק 1 (The Noise 22.11) + story compteur. Usage : python3 specs.py <dossier_clips> <points>"""
import json, sys, re
ISO = lambda d: [o.update(html=re.sub(r'\+(\d+)', r'<span dir=ltr style="unicode-bidi:isolate">+\1</span>', o['html'])) for o in d['ov']]
R = sys.argv[1]; PTS = int(sys.argv[2]) if len(sys.argv) > 2 else 0
C = {'wide': {'dir': f'{R}/wide', 'fps': 10}, 'demo': {'dir': f'{R}/demo', 'fps': 10}, 'end': {'dir': f'{R}/end', 'fps': 10}}
Y = lambda s: f'<span class=y>{s}</span>'
O = lambda t0, t1, pos, h, np=0: {'t0': t0, 't1': t1, 'pos': pos, 'html': h, 'np': np}
big = lambda s, sz=66: f'<div style="font:900 {sz}px/1.12 H">{s}</div>'
cnt = f'{PTS:,}'
TITLE = (f'<div class=box style="font:900 40px/1.15 H">המקהלה הכי {Y("מזייפת")} בעולם?</div><br>'
         f'<div class=pill style="margin-top:10px;background:#FFC24B;color:#140c04;font:900 25px/1.2 H">🎤 {cnt} / 10,000 זמרים</div>'
         f'<div style="margin-top:6px;font:900 16px H;opacity:.85">חלק 1</div>')
BAR = '<div class=pill style="background:rgba(10,8,24,.82);color:#fff;font:900 21px/1.35 H">❤️ לייק +1 · 💬 תגובה +3<br>🔖 שמירה +5 · 🚀 שיתוף +10</div>'
D = 17.5
reel = {'dur': D, 'fps': 30, 'clips': C, 'flash': .4, 'novg': 2.0, 'vgmax': .35,
 'hits': [0.02, 2.68, 5.67, 6.81, 8.72, 9.85, 11.31, 12.69],
 'seg': [{'t0': 0, 't1': 5.67, 'clip': 'wide', 'off': 0, 'zoom': .04},
         {'t0': 5.67, 't1': 11.31, 'clip': 'demo', 'off': 0, 'zoom': .05},
         {'t0': 11.31, 't1': D, 'clip': 'end', 'off': 0, 'zoom': .03}],
 'ov': [O(0, D, 'T', TITLE, 1),
        O(0, 11.31, 'B', BAR, 1),
        O(11.31, 12.69, 'B', '<div class=pill style="background:#2fbf71;color:#fff;font:900 26px/1.3 H">🏆 המקומות פנויים –<br>תהיו הראשונים!</div>'),
        O(12.69, 15.4, 'B', BAR, 1),
        O(15.4, D, 'B', BAR + '<br><div class=pill style="margin-top:8px;background:#C792EA;color:#1a0f2a;font:900 24px H">📩 שלחו לחבר שמזייף</div>', 1),
        O(0, .82, 'M', big(f'אנחנו {Y("בונים")} 🏗️'), 1),
        O(.82, 1.55, 'M', big(f'את {Y("המקהלה")} 🎤')),
        O(1.55, 2.68, 'M', big(f'הכי {Y("מזייפת")}<br>בעולם! 😖')),
        O(2.68, 4.07, 'M', big(f'{Y("10,000")}<br>זמרים', 80)),
        O(4.07, 5.67, 'M', big('ועכשיו<br>יש לנו…', 70)),
        O(5.67, 6.2, 'M', '<div class=box>' + big(f'{Y(cnt)} 😅', 96) + '</div>'),
        O(6.2, 6.81, 'M', big('לייק ❤️', 76)),
        O(6.81, 8.19, 'M', big(f'{Y("+1")} זמר<br>עולה לבמה!', 70)),
        O(8.19, 8.72, 'M', big('תגובה 💬', 76)),
        O(8.72, 9.25, 'M', big(f'{Y("+3")} זמרים!', 76)),
        O(9.25, 9.85, 'M', big('שיתוף 🚀', 76)),
        O(9.85, 11.31, 'M', '<div class=box>' + big(f'{Y("+10")}<br>שורה שלמה!', 80) + '</div>'),
        O(11.31, 12.69, 'M', '<div class=box>' + big(f'כתבו איזה {Y("כלי")}<br>אתם מנגנים 👇', 56) + '<div style="margin-top:10px;font:900 25px/1.4 H">🎸 גיטרה · 🥁 תופים<br>🎺 חצוצרה · 🚿 שירה במקלחת</div></div>'),
        O(12.69, 15.4, 'M', '<div class=box>' + big(f'{Y("5")} התגובות הכי טובות<br>נכנסות לפרק הבא 🏆', 48) + '</div>'),
        O(15.4, D, 'M', '<div class=box>' + big(f'כתבו איזה {Y("כלי")}<br>אתם מנגנים 👇', 56) + '</div>')]}
ISO(reel); json.dump(reel, open(f'{R}/reel.json', 'w'), ensure_ascii=False)
SD = 6.4
story = {'dur': SD, 'fps': 30, 'clips': dict(C, sdemo={'dir': f'{R}/sdemo', 'fps': 10}), 'flash': .35, 'novg': 1.5, 'vgmax': .4, 'hits': [0.02, 2.06, 2.92],
 'seg': [{'t0': 0, 't1': 2.06, 'clip': 'wide', 'off': 1.0, 'zoom': .04}, {'t0': 2.06, 't1': SD, 'clip': 'sdemo', 'off': 0, 'zoom': .05}],
 'ov': [O(0, SD, 'T', TITLE, 1), O(0, SD, 'B', BAR, 1),
        O(0, 2.06, 'M', big(f'🎤 {Y(cnt)}<br>מתוך 10,000', 70), 1),
        O(2.06, 2.92, 'M', big('שתפו את הריל 🚀', 64)),
        O(2.92, SD, 'M', '<div class=box>' + big(f'שיתוף = {Y("+10")}<br>זמרים בבת אחת!', 62) + '</div>')]}
ISO(story); json.dump(story, open(f'{R}/story.json', 'w'), ensure_ascii=False)
print('ok')
