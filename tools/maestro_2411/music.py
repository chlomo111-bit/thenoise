"""Musique de fond synthétisée pour les reels 10.11.
Usage : python3 music.py <mood: show|tender|suspense> out.wav duree [evenements "boom:1.2,sour:14,whoosh:3"]"""
import numpy as np, wave, sys
SR = 44100
mood, out, D = sys.argv[1], sys.argv[2], float(sys.argv[3])
EV = [(k, float(v)) for k, v in (e.split(':') for e in sys.argv[4].split(','))] if len(sys.argv) > 4 and sys.argv[4] else []
N = int(SR * D); L = np.zeros(N); R = np.zeros(N); rng = np.random.default_rng(3)
def env(n, a, d):
    t = np.arange(n) / SR; return np.clip(t / a, 0, 1) * np.exp(-t / d)
def add(s, at, g=1., pan=0.):
    i = int(at * SR)
    if i >= N or i < 0: return
    j = min(N, i + len(s)); L[i:j] += g * s[:j - i] * (1 - pan) ; R[i:j] += g * s[:j - i] * (1 + pan)
def tone(f, dur, a=.01, d=.4, kind='sine'):
    n = int(dur * SR); t = np.arange(n) / SR
    if kind == 'piano': s = np.sin(2*np.pi*f*t) + .45*np.sin(2*np.pi*2*f*t)*np.exp(-t*3) + .2*np.sin(2*np.pi*3*f*t)*np.exp(-t*5)
    elif kind == 'saw': s = 2*((f*t) % 1) - 1; s = np.convolve(s, np.ones(6)/6, 'same')
    elif kind == 'pad': s = np.sin(2*np.pi*f*t) + .5*np.sin(2*np.pi*f*1.003*t) + .3*np.sin(2*np.pi*f*2*t)
    else: s = np.sin(2*np.pi*f*t)
    return s * env(n, a, d)
hz = lambda m: 440 * 2 ** ((m - 69) / 12)
def kick():
    n = int(.3*SR); t = np.arange(n)/SR; return np.sin(2*np.pi*(50+90*np.exp(-t*35))*t) * env(n, .002, .09)
def snare():
    n = int(.2*SR); return rng.standard_normal(n) * env(n, .001, .05) * .6
def hat():
    n = int(.05*SR); s = rng.standard_normal(n); s = s - np.convolve(s, np.ones(4)/4, 'same'); return s * env(n, .001, .015)
if mood == 'show':  # groove « plateau télé » 118 BPM, sol majeur
    b = 60 / 118; prog = [[55, 59, 62], [52, 55, 59], [48, 52, 55], [50, 54, 57]]
    k = 0; t = 0
    while t < D:
        ch = prog[(k // 4) % 4]
        add(kick(), t, .9); add(hat(), t + b/2, .5, .3)
        if k % 2: add(snare(), t, .7)
        if k % 2 == 0:
            for m in ch: add(tone(hz(m), b*1.9, .01, .5, 'saw'), t, .05, -.2)
        add(tone(hz(ch[0] - 24), b*.9, .005, .25), t, .35)
        t += b; k += 1
elif mood == 'tender':  # piano doux 72 BPM, la mineur → do majeur
    b = 60 / 72; prog = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]
    k = 0; t = 0
    while t < D:
        ch = prog[(k // 4) % 4]
        add(tone(hz(ch[k % 3] + 12), b*3, .005, 1.2, 'piano'), t, .16, .2)
        if k % 4 == 0:
            add(tone(hz(ch[0] - 12), b*4.2, .01, 2.2, 'piano'), t, .2, -.2)
            for m in ch: add(tone(hz(m), b*4.2, .6, 3.0, 'pad'), t, .035)
        t += b; k += 1
else:  # suspense : drone grave + battement de cœur + notes de piano isolées
    t = np.arange(N) / SR
    dr = (np.sin(2*np.pi*55*t) + .6*np.sin(2*np.pi*55.4*t) + .3*np.sin(2*np.pi*82.4*t)) * .12 * np.clip(t/1.5, 0, 1)
    L += dr; R += dr
    bt = 0.2
    while bt < D:
        add(kick(), bt, .55); add(kick(), bt + .22, .35); bt += 1.15
    for i, m in enumerate([76, 75, 79, 76, 72, 75, 76, 81, 79, 75]):
        add(tone(hz(m), 2.5, .005, 1.3, 'piano'), 0.6 + i * 2.9, .1, .3 if i % 2 else -.3)
for kd, at in EV:
    if kd == 'boom':
        n = int(1.5*SR); x = np.arange(n)/SR; s = np.sin(2*np.pi*np.cumsum(30+60*np.exp(-x*6))/SR)*env(n, .002, .45); add(np.tanh(1.5*s), at, .9)
    elif kd == 'whoosh':
        n = int(.6*SR); s = np.convolve(rng.standard_normal(n), np.ones(25)/25, 'same') * np.sin(np.linspace(0, np.pi, n)) * .7; add(s, at - .45)
    elif kd == 'ding':
        add(tone(1567, 1.2, .002, .35) + .4*tone(2349, 1.2, .002, .3), at, .25)
    elif kd == 'sour':  # notes fausses (le candidat chante faux)
        for i, f in enumerate([392, 415, 370, 440, 349, 466]):
            add(tone(f * (1 + .03*np.sin(i)), .42, .01, .3, 'saw'), at + i * .4, .12)
    elif kd == 'knock':
        for i in range(3):
            n = int(.12*SR); s = np.sin(2*np.pi*120*np.arange(n)/SR)*env(n, .001, .03) + rng.standard_normal(n)*env(n, .001, .01)*.5; add(s, at + i * .38, .9)
    elif kd == 'stop':  # coupe la musique (pause dramatique)
        i = int(at*SR); j = min(N, i + int(.9*SR)); L[i:j] *= np.linspace(1, .15, j - i); R[i:j] *= np.linspace(1, .15, j - i)
m = max(1e-9, np.abs(np.concatenate([L, R])).max()); L, R = L / m * .8, R / m * .8
fade = np.clip((D - np.arange(N)/SR) / 1.2, 0, 1); L *= fade; R *= fade
w = wave.open(out, 'w'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((np.stack([L, R], 1) * 32767).astype(np.int16).tobytes()); w.close(); print('ok', D)
