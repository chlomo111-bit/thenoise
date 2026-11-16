"""Specs de montage (compose.py) du reel et de la story The Noise 16.11 (format A : action dès l'image 0, petit texte en haut, centre libre).
Usage : python3 specs.py <dossier_clips>"""
import json, sys
R = sys.argv[1]
C = {k: {'dir': f'{R}/c_{k}', 'fps': 30 if k == 'judge' else 10} for k in ['sing', 'judge', 'end']}
bx = lambda s, sz=30: f'<div class=box style="font:900 {sz}px/1.2 H">{s}</div>'
pill = lambda s, sz=30, bg='#FFC24B', fg='#140c04': f'<div class=pill style="background:{bg};color:{fg};font:900 {sz}px/1.2 H">{s}</div>'
Y = lambda s: f'<span class=y>{s}</span>'
O = lambda t0, t1, pos, h: {'t0': t0, 't1': t1, 'pos': pos, 'html': h}
D = 7.4
reel = {'dur': D, 'fps': 10, 'clips': C, 'flash': .4, 'novg': 2.0, 'vgmax': .45,
 'hits': [0.05, 2.0, 3.6, 4.7],
 'seg': [{'t0': 0, 't1': 2.0, 'clip': 'sing', 'off': .2, 'zoom': .06},
         {'t0': 2.0, 't1': 4.7, 'clip': 'judge', 'off': 0, 'zoom': .07},
         {'t0': 4.7, 't1': D, 'clip': 'end', 'off': 0, 'zoom': .05}],
 'ov': [dict(O(0, 2.0, 'T', bx(f'{Y("זיוף")} בשידור חי 🎤', 46)), np=1),
        O(2.0, 3.55, 'T', bx(f'השופט: {Y("סותם אוזניים")} 🙉', 44)),
        O(3.55, 4.7, 'T', bx(f'…ו{Y("מסתובב בחזרה")}! 🔄😂', 46)),
        O(4.7, 5.9, 'M', pill('כתבו "במה"<br>ותיכנסו 🎤', 56)),
        O(5.9, D, 'M', pill('📩 שלחו לחבר<br>שמזייף', 56, '#fff'))]}
json.dump(reel, open(f'{R}/reel.json', 'w'), ensure_ascii=False)
SD = 7.3
story = {'dur': SD, 'fps': 10, 'clips': C, 'flash': .3, 'hits': [0.05, 1.8, 3.4, 4.83], 'novg': 1.0, 'vgmax': .5,
 'seg': [{'t0': 0, 't1': 1.8, 'clip': 'end', 'off': 1.2, 'zoom': .05}, {'t0': 1.8, 't1': 3.4, 'clip': 'sing', 'off': 1.0, 'zoom': .06},
         {'t0': 3.4, 't1': 4.83, 'clip': 'judge', 'off': .9, 'zoom': .06}, {'t0': 4.83, 't1': SD, 'clip': 'end', 'off': 0, 'zoom': .05}],
 'ov': [dict(O(0, SD, 'T', pill('🎤 THE NOISE · עולים לבמה', 28)), np=1),
        dict(O(0, 1.8, 'M', bx(f'שחקן חדש {Y("עלה לבמה")}! 🎉<br><span dir=ltr>@bdvy214</span>', 46)), np=1),
        O(1.8, 3.4, 'M', bx('ובריל החדש… 👀', 50)),
        O(3.4, 4.83, 'M', bx(f'השופט {Y("סותם אוזניים")} 🙉', 46)),
        O(4.83, SD, 'M', bx(f'כתבו {Y("במה")} 🎤<br>והשם שלכם בסטורי הבא!', 44)),
        O(4.83, SD, 'B', pill('👈 בריל החדש', 44, '#fff'))]}
json.dump(story, open(f'{R}/story.json', 'w'), ensure_ascii=False)
print('ok')
