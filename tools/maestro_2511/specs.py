"""Specs compose.py « מאסטרו קול » #4 (25.11 matin) — l'ouïe 20 Hz–20 kHz. Usage : python3 specs.py <dossier_images_10fps> > spec.json
Temps calés sur les mots (scribe)."""
import json, sys
R = sys.argv[1]; D = 18.0
Y = lambda x: f'<span class=y>{x}</span>'
L = lambda x: f'<bdi dir=ltr>{x}</bdi>'
big = lambda x, sz=84: f'<div class=box style="font:900 {sz}px/1.1 H;padding:6px 26px">{x}</div>'
sub = lambda x: f'<div class=box style="font:900 32px/1.2 H">{x}</div>'
O = lambda t0, t1, pos, h, np=0: {'t0': t0, 't1': t1, 'pos': pos, 'html': h, 'np': np}
title = '<div class=pill style="background:#FFC24B;color:#140c04;font:900 28px/1.15 H">מאסטרו קול #4 🎤</div>'
ov = [O(0, D, 'T', title, 1)]
M = [(0, .85, f'{Y("ידעתם")}?', 84), (.85, 1.6, f'{Y("האוזן")} 👂', 84), (1.6, 2.35, f'{Y("שומעת")}', 84),
     (2.35, 3.25, f'מ-{Y(L("20"))}', 84), (3.25, 4.3, f'עד {Y(L("20,000"))}', 84), (4.3, 5.35, f'{Y("הרץ")}! 🎵', 84),
     (5.35, 6.4, f'אצל {Y("צעירים")}', 84), (6.4, 7.3, f'{Y("בריאים")} 💪', 84),
     (7.3, 8.4, f'עם {Y("השנים")} ⏳', 84), (8.4, 9.6, f'{Y("הכי גבוהים")}', 76), (9.6, 10.9, f'{Y("נעלמים")} 🔇', 84),
     (10.9, 12.4, f'מי {Y("שאומר")}?', 84), (12.4, 13.6, f'״{Y("שומע הכל")}״ 🙉', 70),
     (13.6, 14.5, f'{Y("שלחו")} 📩', 84), (14.5, 15.4, f'{Y("מחר")}:', 84), (15.4, 17.2, f'הכלי {Y("העתיק")} 🎺', 76),
     (17.2, 18.0, f'{Y("עקבו")} 🎤', 84)]
for a, b, h, sz in M: ov.append(O(a, b, 'M', big(h, sz), 1 if a == 0 else 0))
B = [(0, 4.8, f'ידעתם שהאוזן שלנו שומעת בערך מ-{Y(L("20"))} עד {Y(L("20,000"))} הרץ?'),
     (4.8, 7.3, f'ככה אצל {Y("צעירים בריאים")}'),
     (7.3, 10.9, f'ועם השנים הצלילים הכי גבוהים {Y("נעלמים")} לאט לאט'),
     (10.9, 14.5, f'מי שאומר ״אני שומע הכל״? {Y("שלחו לו את זה")}! 📩'),
     (14.5, 17.2, f'מחר: הכלי המוזיקלי הכי {Y("עתיק")} בעולם'),
     (17.2, 18.0, f'עקבו! 🎤')]
for a, b, h in B: ov.append(O(a, b, 'B', sub(h), 1 if a < .05 else 0))
spec = {'dur': D, 'fps': 30, 'clips': {'all': {'dir': R, 'fps': 10}}, 'flash': .2, 'novg': 0, 'vgmax': .3,
        'hits': [0.02, 3.25, 8.4, 10.9], 'seg': [{'t0': 0, 't1': D, 'clip': 'all', 'off': 0, 'zoom': 0, 'speed': 1.0}], 'ov': ov}
print(json.dumps(spec, ensure_ascii=False))
