"""Specs The Noise 23.11 matin « המקהלה הכי מזייפת בעולם? » חלק 2 — הדוד שתופס את המיקרופון בחתונה. Usage : python3 specs.py <dossier_clips>"""
import json, sys, re
ISO = lambda d: [o.update(html=re.sub(r'\+(\d+)', r'<span dir=ltr style="unicode-bidi:isolate">+\1</span>', o['html'])) for o in d['ov']]
R = sys.argv[1]
C = {k: {'dir': f'{R}/{k}', 'fps': 10} for k in ('wide', 'cousin', 'demo', 'end')}
Y = lambda s: f'<span class=y>{s}</span>'
O = lambda t0, t1, pos, h, np=0: {'t0': t0, 't1': t1, 'pos': pos, 'html': h, 'np': np}
big = lambda s, sz=66: f'<div style="font:900 {sz}px/1.12 H">{s}</div>'
def title(n): return (f'<div class=box style="font:900 40px/1.15 H">המקהלה הכי {Y("מזייפת")} בעולם?</div><br>'
  f'<div class=pill style="margin-top:10px;background:#FFC24B;color:#140c04;font:900 25px/1.2 H">🎤 {n} / 10,000 זמרים</div>'
  f'<div style="margin-top:6px;font:900 16px H;opacity:.85">חלק 2</div>')
BAR = '<div class=pill style="background:rgba(10,8,24,.82);color:#fff;font:900 21px/1.35 H">❤️ לייק +1 · 💬 תגובה +3<br>🔖 שמירה +5 · 🚀 שיתוף +10</div>'
D = 19.2
reel = {'dur': D, 'fps': 30, 'clips': C, 'flash': .4, 'novg': 2.0, 'vgmax': .35,
 'hits': [0.02, 1.6, 4.3, 7.6, 9.6, 11.0, 12.8, 14.3],
 'seg': [{'t0': 0, 't1': 1.6, 'clip': 'wide', 'off': 0, 'zoom': .03},
         {'t0': 1.6, 't1': 6.2, 'clip': 'cousin', 'off': 0, 'zoom': .04},
         {'t0': 6.2, 't1': 14.3, 'clip': 'demo', 'off': 0, 'zoom': .04},
         {'t0': 14.3, 't1': D, 'clip': 'end', 'off': 0, 'zoom': .03}],
 'ov': [O(0, 7.6, 'T', title(1), 1), O(7.6, D, 'T', title(18), 1),
        O(0, 14.3, 'B', BAR, 1),
        O(13.4, 14.3, 'B', '<div class=pill style="background:#2fbf71;color:#fff;font:900 24px/1.3 H">🏆 המקומות פנויים – תהיו הראשונים!</div>'),
        O(14.3, D, 'B', BAR + '<br><div class=pill style="margin-top:8px;background:#C792EA;color:#1a0f2a;font:900 24px H">📩 תייגו את הדוד שמזייף</div>', 1),
        O(0, .76, 'M', big(f'בכל {Y("משפחה")}')),
        O(.76, 1.6, 'M', big(f'יש {Y("אחד")}! 👆')),
        O(1.6, 2.45, 'M', big(f'{Y("הדוד")} 🤵')),
        O(2.45, 3.55, 'M', big(f'{Y("מיקרופון")}<br>בחתונה 🎤', 62)),
        O(3.55, 4.25, 'M', big('אוי… 😬', 76)),
        O(4.25, 5.0, 'M', big(f'{Y("מזייף")}! 😖', 80)),
        O(5.0, 6.3, 'M', '<div class=box>' + big(f'{Y("תייגו")} אותו 👇', 66) + '</div>'),
        O(6.3, 7.6, 'M', big(f'המקהלה {Y("שלנו")}', 62)),
        O(7.6, 9.45, 'M', '<div class=box>' + big(f'{Y("18")} 🎤<br><span style="font-size:40px">מתוך 10,000</span>', 100) + '</div>'),
        O(9.45, 10.1, 'M', big('לייק ❤️', 76)),
        O(10.1, 11.0, 'M', big(f'{Y("+1")} זמר!', 80)),
        O(11.0, 11.65, 'M', big('תגובה 💬', 76)),
        O(11.65, 12.75, 'M', big(f'{Y("+3")} זמרים!', 76)),
        O(12.75, 13.4, 'M', big('שיתוף 🚀', 76)),
        O(13.4, 14.3, 'M', '<div class=box>' + big(f'{Y("+10")}<br>שורה שלמה!', 76) + '</div>'),
        O(14.3, 17.1, 'M', '<div class=box>' + big(f'כתבו איזה {Y("כלי")}<br>אתם מנגנים 👇', 56) + '<div style="margin-top:10px;font:900 25px/1.4 H">🎸 גיטרה · 🥁 תופים<br>🎺 חצוצרה · 🚿 שירה במקלחת</div></div>'),
        O(17.1, D, 'M', '<div class=box>' + big(f'{Y("5")} התגובות הכי טובות<br>נכנסות לפרק הבא 🏆', 46) + '</div>')]}
ISO(reel); json.dump(reel, open(f'{R}/reel.json', 'w'), ensure_ascii=False)
print('ok')
