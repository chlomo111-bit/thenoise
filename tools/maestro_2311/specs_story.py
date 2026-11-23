"""Specs story « מאסטרו קול » (teaser fait de demain). Usage : python3 specs_story.py <dossier_images_10fps>"""
import json, sys
R = sys.argv[1]; D = 6.4
Y = lambda s: f'<span class=y>{s}</span>'
big = lambda s, sz=84: f'<div class=box style="font:900 {sz}px/1.1 H;padding:6px 26px">{s}</div>'
sub = lambda s: f'<div class=box style="font:900 32px/1.2 H">{s}</div>'
O = lambda t0, t1, pos, h, np=0: {'t0': t0, 't1': t1, 'pos': pos, 'html': h, 'np': np}
ov = [O(0, D, 'T', '<div class=pill style="background:#FFC24B;color:#140c04;font:900 28px/1.15 H">מאסטרו קול 🎤</div>', 1)]
for a, b, h in [(0, .44, f'{Y("מחר")}'), (.44, 1.33, f'{Y("מאסטרו")} קול'), (1.33, 2.01, 'איפה?'), (2.01, 2.93, f'{Y("העצם")}'), (2.93, 3.78, f'{Y("קטנה")} 🔬'),
                (3.78, 4.52, f'{Y("רמז")}:'), (4.52, 5.11, f'{Y("באוזן")}! 👂'), (5.11, D, f'{Y("עקבו")} 🎤')]: ov.append(O(a, b, 'M', big(h), 1 if a == 0 else 0))
for a, b, h in [(0, 1.33, f'מחר ב{Y("מאסטרו קול")}:'), (1.33, 3.78, f'איפה נמצאת העצם {Y("הכי קטנה")} בגוף?'), (3.78, 5.11, f'רמז: {Y("באוזן")}!'), (5.11, D, 'עקבו כדי לדעת 🎤')]:
    ov.append(O(a, b, 'B', sub(h), 1 if a == 0 else 0))
print(json.dumps({'dur': D, 'fps': 30, 'clips': {'all': {'dir': R, 'fps': 10}}, 'flash': .2, 'novg': 0, 'vgmax': .3, 'hits': [0.02, 4.52],
      'seg': [{'t0': 0, 't1': D, 'clip': 'all', 'off': 0, 'zoom': 0}], 'ov': ov}, ensure_ascii=False))
