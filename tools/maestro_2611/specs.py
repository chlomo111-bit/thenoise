"""Specs compose.py « מאסטרו קול » #6 (26.11 soir) — 440 Hz. Usage : python3 specs.py <dossier_images_10fps> > spec.json
Temps calés sur les mots (scribe)."""
import json, sys
R = sys.argv[1]; D = 18.77
Y = lambda x: f'<span class=y>{x}</span>'
L = lambda x: f'<bdi dir=ltr>{x}</bdi>'
big = lambda x, sz=84: f'<div class=box style="font:900 {sz}px/1.1 H;padding:6px 26px">{x}</div>'
sub = lambda x: f'<div class=box style="font:900 32px/1.2 H">{x}</div>'
O = lambda t0, t1, pos, h, np=0: {'t0': t0, 't1': t1, 'pos': pos, 'html': h, 'np': np}
title = '<div class=pill style="background:#FFC24B;color:#140c04;font:900 28px/1.15 H">מאסטרו קול #6 🎤</div>'
ov = [O(0, D, 'T', title, 1)]
M = [(0,1.0,f'{Y("ידעתם")}?',84),(1.0,2.1,f'{Y("תזמורות")} 🎻',80),(2.1,3.5,f'אותו {Y("צליל")}?',80),(3.5,5.0,f'התו {Y("לה")} 🎼',84),
     (5.0,6.6,f'{Y(L("440 Hz"))}',84),(6.6,8.0,f'{Y("תקן")} 🌍',84),(8.0,9.3,f'{Y("אבל")}...',84),(9.3,10.4,f'{Y("קצת")}',84),(10.4,11.5,f'{Y("יותר גבוה")} 🔼',76),
     (11.5,12.6,f'{Y("שלחו")} 📩',84),(12.6,13.4,f'{Y("למי")}',84),(13.4,14.4,f'{Y("שמכוון")} 👂',80),
     (14.4,15.4,f'{Y("מחר")}:',84),(15.4,16.5,f'{Y("הצעקה")} 📢',80),(16.5,17.6,f'{Y("הכי חזקה")}?',76),(17.6,D,f'{Y("עקבו")} 🎤',84)]
for a_,b_,h,sz in M: ov.append(O(a_,b_,'M',big(h,sz),1 if a_==0 else 0))
B = [(0,3.9,f'ידעתם שכמעט כל התזמורות בעולם מכוונות {Y("לאותו צליל")}?'),
     (3.9,7.9,f'זה התו {Y("לה")}: ארבע מאות וארבעים הרץ, {Y("תקן בינלאומי")}'),
     (7.9,11.4,f'אבל יש תזמורות שמכוונות {Y("קצת יותר גבוה")}'),
     (11.4,14.3,f'שלחו את זה למי שאומר שהוא {Y("מכוון לפי האוזן")} 📩'),
     (14.3,17.5,f'מחר: מה הצעקה {Y("הכי חזקה")} בעולם?'),
     (17.5,D,f'עקבו כדי לדעת! 🎤')]
for a_,b_,h in B: ov.append(O(a_,b_,'B',sub(h),1 if a_<.05 else 0))
spec = {'dur': D, 'fps': 30, 'clips': {'all': {'dir': R, 'fps': 15}}, 'flash': .2, 'novg': 0, 'vgmax': .3,
        'hits': [0.02, 3.9, 8.0, 11.5, 14.4], 'seg': [{'t0': 0, 't1': D, 'clip': 'all', 'off': 0, 'zoom': 0, 'speed': 1.0}], 'ov': ov}
print(json.dumps(spec, ensure_ascii=False))
