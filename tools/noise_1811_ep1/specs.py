"""Specs de montage (compose.py) du reel « הזיופים הכי גרועים · פרק 1 » et de la story du 18.11 soir.
Usage : python3 specs.py <dossier_clips>"""
import json, sys
R = sys.argv[1]
C = {k: {'dir': f'{R}/c_{k}', 'fps': 10} for k in ['uncle', 'flee', 'judge', 'button', 'end']}
bx = lambda s, sz=30: f'<div class=box style="font:900 {sz}px/1.2 H">{s}</div>'
pill = lambda s, sz=30, bg='#FFC24B', fg='#140c04': f'<div class=pill style="background:{bg};color:{fg};font:900 {sz}px/1.2 H">{s}</div>'
Y = lambda s: f'<span class=y>{s}</span>'
O = lambda t0, t1, pos, h: {'t0': t0, 't1': t1, 'pos': pos, 'html': h}
D = 14.8
VOTE = pill('1 🔴 לוחץ – הדוד יורד<br>2 🎤 נותן לו לסיים', 40, '#fff')
reel = {'dur': D, 'fps': 10, 'clips': C, 'flash': .35, 'novg': 2.0, 'vgmax': .4, 'badge': 'פרק 1 · הזיופים הכי גרועים',
 'hits': [2.0, 3.0, 5.2, 7.4, 9.9, 11.9],
 'seg': [{'t0': 0, 't1': 3.0, 'clip': 'uncle', 'off': 0, 'zoom': .06},
         {'t0': 3.0, 't1': 5.2, 'clip': 'flee', 'off': 0, 'zoom': .05},
         {'t0': 5.2, 't1': 7.4, 'clip': 'judge', 'off': 0, 'zoom': .06},
         {'t0': 7.4, 't1': 11.9, 'clip': 'button', 'off': 0, 'zoom': .07},
         {'t0': 11.9, 't1': D, 'clip': 'end', 'off': 0, 'zoom': .05}],
 'ov': [dict(O(0, 2.0, 'T', bx(f'כשהדוד לוקח<br>{Y("מיקרופון")} בחתונה… 🎤', 46)), np=1),
        O(2.0, 3.0, 'T', bx(f'ואז… {Y("הזיוף")} 😬', 52)),
        O(3.0, 3.9, 'T', bx(f'{Y("אוי לא!")} 😱', 56)),
        O(3.9, 5.2, 'T', bx(f'האורחים {Y("בורחים")}! 🏃‍♀️', 50)),
        O(5.2, 7.4, 'T', bx(f'גם השופט<br>{Y("סותם אוזניים")} 🙉', 48)),
        O(7.4, 8.7, 'T', bx(f'והיד שלו… {Y("לכפתור")} 🔴', 48)),
        O(8.7, 9.9, 'T', bx(f'הוא {Y("לוחץ")}…?! 😳', 54)),
        O(9.9, 11.9, 'T', bx(f'{Y("אתם מחליטים")} 👇', 52)),
        O(9.9, 11.9, 'B', VOTE),
        O(11.9, D, 'T', bx(f'1 או 2? {Y("בתגובות")} 👇', 50)),
        O(11.9, 12.25, 'B', VOTE),
        O(12.25, D, 'B', pill('🏷️ תייגו את מי<br>שמזייף בחתונות', 50))]}
json.dump(reel, open(f'{R}/reel.json', 'w'), ensure_ascii=False)
SD = 7.0
story = {'dur': SD, 'fps': 10, 'clips': C, 'flash': .3, 'hits': [2.64, 4.0], 'novg': 1.0, 'vgmax': .5, 'badge': 'פרק 1',
 'seg': [{'t0': 0, 't1': 2.64, 'clip': 'button', 'off': 2.0, 'zoom': .05}, {'t0': 2.64, 't1': 4.0, 'clip': 'uncle', 'off': .5, 'zoom': .06},
         {'t0': 4.0, 't1': SD, 'clip': 'judge', 'off': 0, 'zoom': .05}],
 'ov': [dict(O(0, 2.64, 'M', bx(f'היד של השופט<br>{Y("כבר על הכפתור")}… 🔴', 46)), np=1),
        O(2.64, 4.0, 'M', bx(f'הוא {Y("לוחץ")} או לא? 😳', 50)),
        O(4.0, SD, 'M', bx(f'{Y("תצביעו בריל")} 👇<br>1 🔴 לוחץ · 2 🎤 לא', 46))]}
json.dump(story, open(f'{R}/story.json', 'w'), ensure_ascii=False)
print('ok')
