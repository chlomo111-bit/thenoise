import json, sys
R = sys.argv[1]; D = 6.6
Y = lambda x: f'<span class=y>{x}</span>'
big = lambda x, sz=84: f'<div class=box style="font:900 {sz}px/1.1 H;padding:6px 26px">{x}</div>'
sub = lambda x: f'<div class=box style="font:900 32px/1.2 H">{x}</div>'
O = lambda t0, t1, pos, h, np=0: {'t0': t0, 't1': t1, 'pos': pos, 'html': h, 'np': np}
title = '<div class=pill style="background:#FFC24B;color:#140c04;font:900 28px/1.15 H">מאסטרו קול 🎤 מחר</div>'
ov = [O(0, D, 'T', title, 1)]
M = [(0, .8, Y('מחר')), (.8, 1.9, f'עד איזה {Y("גובה")}'), (1.9, 2.8, f'{Y("האוזן")} שלנו'), (2.8, 3.85, f'{Y("שומעת")}? 👂'),
     (3.85, 5.2, f'יש {Y("הפתעה")}! 😮'), (5.2, 6.6, f'{Y("עקבו")} 🎤')]
for a, b, h in M: ov.append(O(a, b, 'M', big(h, 76), 1 if a == 0 else 0))
ov.append(O(0, D, 'B', sub(f'מחר ב-{Y("מאסטרו קול")}: עד איזה גובה האוזן שומעת?'), 1))
print(json.dumps({'dur': D, 'fps': 30, 'clips': {'all': {'dir': R, 'fps': 10}}, 'flash': .2, 'novg': 0, 'vgmax': .3,
  'hits': [0.02, 3.85], 'seg': [{'t0': 0, 't1': D, 'clip': 'all', 'off': 0, 'zoom': 0, 'speed': 1.0}], 'ov': ov}, ensure_ascii=False))
