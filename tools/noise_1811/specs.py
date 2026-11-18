"""Specs de montage (compose.py) du reel et de la story The Noise 18.11 (format A : action dès l'image 0, petit texte en haut, centre libre).
Usage : python3 specs.py <dossier_clips>"""
import json, sys
R = sys.argv[1]
C = {k: {'dir': f'{R}/c_{k}', 'fps': 30 if k == 'judge' else 10} for k in ['boom', 'judge', 'end']}
bx = lambda s, sz=30: f'<div class=box style="font:900 {sz}px/1.2 H">{s}</div>'
pill = lambda s, sz=30, bg='#FFC24B', fg='#140c04': f'<div class=pill style="background:{bg};color:{fg};font:900 {sz}px/1.2 H">{s}</div>'
Y = lambda s: f'<span class=y>{s}</span>'
O = lambda t0, t1, pos, h: {'t0': t0, 't1': t1, 'pos': pos, 'html': h}
D = 7.0
reel = {'dur': D, 'fps': 10, 'clips': C, 'flash': .4, 'novg': 2.0, 'vgmax': .4,
 'hits': [0.56, 1.5, 2.1, 3.5],
 'seg': [{'t0': 0, 't1': 1.5, 'clip': 'boom', 'off': 0, 'zoom': .06},
         {'t0': 1.5, 't1': 3.5, 'clip': 'judge', 'off': .4, 'zoom': .06},
         {'t0': 3.5, 't1': D, 'clip': 'end', 'off': 0, 'zoom': .05}],
 'ov': [dict(O(0, .56, 'T', bx(f'תו {Y("אחד")}… 🎤', 50)), np=1),
        O(.56, 1.5, 'T', bx(f'{Y("בום!")} 💥', 58)),
        O(1.5, 3.5, 'T', bx(f'השופט {Y("עף מהכיסא")}! 😂', 46)),
        O(3.5, 4.6, 'B', pill('כתבו "במה"<br>ותיכנסו 🎤', 56)),
        O(4.6, D, 'B', pill('📩 שלחו לחבר<br>שמזייף', 56, '#fff'))]}
json.dump(reel, open(f'{R}/reel.json', 'w'), ensure_ascii=False)
SD = 6.4
story = {'dur': SD, 'fps': 10, 'clips': C, 'flash': .3, 'hits': [2.06, 3.44], 'novg': 1.0, 'vgmax': .5,
 'seg': [{'t0': 0, 't1': 2.06, 'clip': 'judge', 'off': .55, 'zoom': .05}, {'t0': 2.06, 't1': 3.44, 'clip': 'boom', 'off': 0, 'zoom': .06},
         {'t0': 3.44, 't1': SD, 'clip': 'end', 'off': .3, 'zoom': .05}],
 'ov': [dict(O(0, SD, 'T', pill('🎤 THE NOISE · ראיתם?!', 28)), np=1),
        O(0, 2.06, 'B', bx(f'השופט {Y("עף מהכיסא")}! 😂', 46)),
        O(2.06, 3.44, 'B', bx('בריל החדש… 👀', 50)),
        O(3.44, SD, 'B', bx(f'כתבו {Y("במה")} 🎤<br>🎙️ ושלחו לנו הודעה קולית!', 42))]}
json.dump(story, open(f'{R}/story.json', 'w'), ensure_ascii=False)
print('ok')
