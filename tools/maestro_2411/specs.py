"""Specs compose.py « מאסטרו קול » #2 (24.11 matin) — l'étrier. Usage : python3 specs.py <dossier_images_10fps> > spec.json
Temps ci-dessous = temps de la prise brute ; tout est divisé par TEMPO (atempo 1,08)."""
import json, sys
R = sys.argv[1]; TEMPO = 1.08; D = 19.15
s = lambda t: round(t / TEMPO, 3)
Y = lambda x: f'<span class=y>{x}</span>'
big = lambda x, sz=84: f'<div class=box style="font:900 {sz}px/1.1 H;padding:6px 26px">{x}</div>'
sub = lambda x: f'<div class=box style="font:900 32px/1.2 H">{x}</div>'
O = lambda t0, t1, pos, h, np=0: {'t0': t0, 't1': t1, 'pos': pos, 'html': h, 'np': np}
title = '<div class=pill style="background:#FFC24B;color:#140c04;font:900 28px/1.15 H">מאסטרו קול #2 🎤</div>'
ov = [O(0, D, 'T', title, 1)]
M = [(0, .95, f'{Y("ידעתם")}?'), (.95, 1.9, f'העצם {Y("הכי קטנה")} 🦴'), (1.9, 2.9, 'בגוף? 🤔'), (2.9, 3.8, f'{Y("באוזן")}! 👂'),
     (3.8, 5.3, f'{Y("ארכוף")}!'), (5.3, 6.4, 'הקול 🔊'), (6.4, 7.6, f'שלוש {Y("עצמות")}'), (7.6, 8.8, f'{Y("קטנטנות")} 🔬'),
     (8.8, 9.7, 'והארכוף'), (9.7, 11.0, f'{Y("הכי קטן")}! 🏆'), (11.0, 12.2, f'{Y("שלחו")} 📩'), (12.2, 13.3, 'למי שאומר'),
     (13.3, 14.4, f'{Y("מה?")} 🤷'), (14.4, 15.1, 'מחר'), (15.1, 16.5, f'{Y("מהר יותר")}? 💨'), (16.5, 18.1, f'אוויר או {Y("מים")}'),
     (18.1, 19.1, f'{Y("עקבו")} 🎤'), (19.1, 21, f'{Y("כתבו שם")} ✍️')]
for a, b, h in M: ov.append(O(s(a), s(b), 'M', big(h), 1 if a == 0 else 0))
B = [(0, 2.9, f'ידעתם איפה נמצאת העצם {Y("הכי קטנה")} בגוף?'), (2.9, 5.3, f'{Y("באוזן")}! קוראים לה {Y("ארכוף")}'),
     (5.3, 8.8, f'הקול עובר דרך שלוש {Y("עצמות")} קטנטנות באוזן'), (8.8, 11.0, f'והארכוף הוא האחרון והקטן מכולן'),
     (11.0, 14.4, f'שלחו את זה למי שכל הזמן אומר: {Y("מה?")} לא שמעתי!'), (14.4, 18.1, f'מחר: איפה הקול נע {Y("מהר יותר")} — באוויר או במים?'),
     (18.1, 21, f'עקבו וכתבו שם — ואני אקרא לכם! 🎤')]
for a, b, h in B: ov.append(O(s(a), s(b), 'B', sub(h), 1 if a < .05 else 0))
spec = {'dur': D, 'fps': 30, 'clips': {'all': {'dir': R, 'fps': 10}}, 'flash': .2, 'novg': 0, 'vgmax': .3,
        'hits': [0.02, s(2.9), s(9.7), s(14.4)], 'seg': [{'t0': 0, 't1': D, 'clip': 'all', 'off': 0, 'zoom': 0, 'speed': .97}], 'ov': ov}
print(json.dumps(spec, ensure_ascii=False))
