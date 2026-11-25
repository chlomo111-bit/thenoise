"""Specs compose.py « מאסטרו קול » #4 (25.11 matin) — l'ouïe 20 Hz–20 kHz. Usage : python3 specs.py <dossier_images_10fps> > spec.json
Temps calés sur les mots (scribe)."""
import json, sys
R = sys.argv[1]; D = 18.05
Y = lambda x: f'<span class=y>{x}</span>'
L = lambda x: f'<bdi dir=ltr>{x}</bdi>'
big = lambda x, sz=84: f'<div class=box style="font:900 {sz}px/1.1 H;padding:6px 26px">{x}</div>'
sub = lambda x: f'<div class=box style="font:900 32px/1.2 H">{x}</div>'
O = lambda t0, t1, pos, h, np=0: {'t0': t0, 't1': t1, 'pos': pos, 'html': h, 'np': np}
title = '<div class=pill style="background:#FFC24B;color:#140c04;font:900 28px/1.15 H">מאסטרו קול #5 🎤</div>'
ov = [O(0, D, 'T', title, 1)]
M = [(0,.9,f'{Y("ידעתם")}?',84),(.9,1.9,f'{Y("הכלים")} 🎼',84),(1.9,3.0,f'הכי {Y("עתיקים")}',80),(3.0,4.0,f'{Y("חליל")} 🎶',84),(4.0,4.8,f'{Y("מעצם")} 🦴',84),
     (4.8,5.9,f'בן {Y("בערך")}',84),(5.9,7.0,f'{Y(L("35-40"))}',84),(7.0,8.0,f'אלף {Y("שנה")}!',84),(8.0,9.0,f'כבר {Y("אז")}',84),(9.0,10.1,f'{Y("מוזיקה")} 🎵',84),
     (10.1,11.0,f'{Y("שלחו")} 📩',84),(11.0,12.0,f'למי {Y("שחושב")}',80),(12.0,13.0,f'{Y("הראשון")}? 🤔',84),
     (13.0,14.2,f'{Y("מחר")}:',84),(14.2,15.4,f'{Y("תזמורות")} 🎻',80),(15.4,16.6,f'אותו {Y("צליל")}?',80),(16.6,D,f'{Y("עקבו")} 🎤',84)]
for a_,b_,h,sz in M: ov.append(O(a_,b_,'M',big(h,sz),1 if a_==0 else 0))
B = [(0,4.8,f'ידעתם שאחד הכלים המוזיקליים הכי עתיקים שנמצאו הוא {Y("חליל מעצם של נשר")}?'),
     (4.8,8.0,f'הוא בן בערך {Y(L("35"))} עד {Y(L("40"))} אלף שנה!'),
     (8.0,10.1,f'כבר אז אנשים עשו {Y("מוזיקה")}'),
     (10.1,13.0,f'שלחו את זה למי שחושב שהוא {Y("הראשון")} שהמציא מוזיקה! 📩'),
     (13.0,16.6,f'מחר: למה כל התזמורות מכוונות {Y("לאותו צליל")}?'),
     (16.6,D,f'עקבו כדי לדעת! 🎤')]
for a_,b_,h in B: ov.append(O(a_,b_,'B',sub(h),1 if a_<.05 else 0))
spec = {'dur': D, 'fps': 30, 'clips': {'all': {'dir': R, 'fps': 10}}, 'flash': .2, 'novg': 0, 'vgmax': .3,
        'hits': [0.02, 4.8, 8.0, 10.1, 13.0], 'seg': [{'t0': 0, 't1': D, 'clip': 'all', 'off': 0, 'zoom': 0, 'speed': 1.0}], 'ov': ov}
print(json.dumps(spec, ensure_ascii=False))
