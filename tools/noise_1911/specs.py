"""Specs compose.py du reel tendance « POV: החבר שלך לוקח מיקרופון בקריוקי » (19.11) et de la story vidéo.
Voix : reel_voice.mp3 (1 prise Juniper eleven_v4, coupée + atempo 1,06 → 14,4 s), temps calés sur scribe.
Usage : python3 specs.py <dossier_clips>"""
import json, sys
R = sys.argv[1]
C = {k: {'dir': f'{R}/c_{k}', 'fps': 10} for k in ['grab', 'side', 'flee', 'judge', 'encore', 'end']}
bx = lambda s, sz=30: f'<div class=box style="font:900 {sz}px/1.2 H">{s}</div>'
pill = lambda s, sz=30, bg='#FFC24B', fg='#140c04': f'<div class=pill style="background:{bg};color:{fg};font:900 {sz}px/1.2 H">{s}</div>'
Y = lambda s: f'<span class=y>{s}</span>'
O = lambda t0, t1, pos, h: {'t0': t0, 't1': t1, 'pos': pos, 'html': h}
D = 14.4
reel = {'dur': D, 'fps': 10, 'clips': C, 'flash': .3, 'novg': 2.0, 'vgmax': .4,
 'hits': [2.0, 4.26, 4.98, 6.23, 8.0, 9.25, 10.92],
 'seg': [{'t0': 0, 't1': 2.0, 'clip': 'side', 'off': 0, 'zoom': .08},
         {'t0': 2.0, 't1': 4.26, 'clip': 'grab', 'off': .2, 'zoom': .06},
         {'t0': 4.26, 't1': 4.98, 'clip': 'side', 'off': 1.1, 'zoom': .1},
         {'t0': 4.98, 't1': 6.23, 'clip': 'encore', 'off': .6, 'zoom': .09},
         {'t0': 6.23, 't1': 8.0, 'clip': 'flee', 'off': .5, 'zoom': .05},
         {'t0': 8.0, 't1': 9.25, 'clip': 'judge', 'off': .3, 'zoom': .06},
         {'t0': 9.25, 't1': 10.92, 'clip': 'encore', 'off': 0, 'zoom': .07},
         {'t0': 10.92, 't1': D, 'clip': 'end', 'off': 0, 'zoom': .05}],
 'ov': [dict(O(0, 4.26, 'T', bx(f'<span dir=ltr>POV:</span> 👀<br>החבר שלך לוקח<br>{Y("מיקרופון")} בקריוקי 🎤', 44)), np=1),
        O(4.26, 4.98, 'T', bx(f'ואז…', 56)),
        O(4.98, 6.23, 'T', bx(f'{Y("הזיוף")} 😬🎶❌', 58)),
        O(6.23, 8.0, 'T', bx(f'פתאום כולם הולכים<br>{Y("לשירותים")} 🚽😂', 46)),
        O(8.0, 9.25, 'T', bx(f'גם השופט {Y("לא שורד")} 🙉', 48)),
        O(9.25, 10.92, 'T', bx(f'והוא?<br>{Y("עוד שיר אחד!")} 🎤🔁', 50)),
        O(10.92, D, 'T', bx(f'{Y("תייגו")} את החבר הזה 👇', 50)),
        O(12.53, D, 'B', pill('🎤 כתבו "במה" ותיכנסו<br>📩 שלחו לחבר שמזייף', 40))]}
json.dump(reel, open(f'{R}/reel.json', 'w'), ensure_ascii=False)
SD = 6.9
story = {'dur': SD, 'fps': 10, 'clips': C, 'flash': .3, 'hits': [2.7, 5.2], 'novg': 1.0, 'vgmax': .5,
 'seg': [{'t0': 0, 't1': 2.7, 'clip': 'side', 'off': 0, 'zoom': .06}, {'t0': 2.7, 't1': 5.2, 'clip': 'grab', 'off': 0, 'zoom': .06},
         {'t0': 5.2, 't1': SD, 'clip': 'judge', 'off': .2, 'zoom': .06}],
 'ov': [dict(O(0, 2.7, 'M', bx(f'יש לכם חבר שחוטף<br>את {Y("המיקרופון")} בקריוקי? 🎤', 44)), np=1),
        O(2.7, 5.2, 'M', bx(f'{Y("תייגו אותו")} בריל החדש 😂', 46)),
        O(5.2, SD, 'M', bx(f'ושלחו לנו<br>{Y("הודעה קולית")} 🎙️', 48))]}
json.dump(story, open(f'{R}/story.json', 'w'), ensure_ascii=False)
print('ok')
