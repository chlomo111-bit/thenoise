"""Specs compose.py « מאסטרו קול » #3 (24.11 soir) — le son dans l'eau. Usage : python3 specs.py <dossier_images_10fps> > spec.json
Temps = temps de la prise brute (aucun atempo), calés sur les silences de la voix."""
import json, sys
R = sys.argv[1]; D = 17.1
Y = lambda x: f'<span class=y>{x}</span>'
L = lambda x: f'<bdi dir=ltr>{x}</bdi>'
big = lambda x, sz=84: f'<div class=box style="font:900 {sz}px/1.1 H;padding:6px 26px">{x}</div>'
sub = lambda x: f'<div class=box style="font:900 32px/1.2 H">{x}</div>'
O = lambda t0, t1, pos, h, np=0: {'t0': t0, 't1': t1, 'pos': pos, 'html': h, 'np': np}
title = '<div class=pill style="background:#FFC24B;color:#140c04;font:900 28px/1.15 H">מאסטרו קול #3 🎤</div>'
ov = [O(0, D, 'T', title, 1)]
M = [(0, .9, f'{Y("ידעתם")}?'), (.9, 1.8, f'{Y("במים")} 🌊'), (1.8, 2.7, f'הקול {Y("נע מהר")}'), (2.7, 3.5, f'פי {Y("ארבעה")}!'),
     (3.5, 4.5, f'מאשר {Y("באוויר")} 💨'),
     (4.5, 5.35, f'{Y("באוויר")} 💨'), (5.35, 6.2, Y(L('340'))), (6.2, 7.3, 'מטר בשנייה'),
     (7.3, 8.25, f'{Y("ובמים")}?! 🌊'), (8.25, 9.0, f'{Y("יותר מ")}'), (9.0, 10.25, Y(L('1,400')) + '!'),
     (10.25, 11.1, f'{Y("שלחו")} 📩'), (11.1, 12.2, 'למי ש'+Y('צועק')), (12.2, 13.45, f'מתוך {Y("הבריכה")} 🏊'),
     (13.45, 14.2, f'{Y("מחר")}'), (14.2, 15.0, f'עד איזה {Y("גובה")}?'), (15.0, 15.85, f'{Y("האוזן")} 👂'),
     (15.85, 17.1, f'{Y("עקבו")} 🎤')]
for a, b, h in M: ov.append(O(a, b, 'M', big(h, 66 if a == 1.8 else 84), 1 if a == 0 else 0))
B = [(0, 4.5, f'ידעתם שבמים הקול נע מהר בערך פי {Y("ארבעה")} מאשר באוויר?'),
     (4.5, 7.3, f'באוויר: בערך {Y(L("340"))} מטר בשנייה'),
     (7.3, 10.25, f'ובמים? יותר מ-{Y(L("1,400"))} מטר בשנייה!'),
     (10.25, 13.45, f'שלחו את זה למי שצועק לכם {Y("מתוך הבריכה")}'),
     (13.45, 15.85, f'מחר: עד איזה {Y("גובה")} האוזן שלנו שומעת?'),
     (15.85, 17.1, f'עקבו כדי לדעת! 🎤')]
for a, b, h in B: ov.append(O(a, b, 'B', sub(h), 1 if a < .05 else 0))
spec = {'dur': D, 'fps': 30, 'clips': {'all': {'dir': R, 'fps': 10}}, 'flash': .2, 'novg': 0, 'vgmax': .3,
        'hits': [0.02, 7.3, 9.0, 13.45], 'seg': [{'t0': 0, 't1': D, 'clip': 'all', 'off': 0, 'zoom': 0, 'speed': 1.0}], 'ov': ov}
print(json.dumps(spec, ensure_ascii=False))
