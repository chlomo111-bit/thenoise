"""Noise 18.11 : coupe les silences de la voix (reel + story) et donne le minutage après coupe. À lancer dans le dossier des mp3."""
import subprocess
def build(src,out,sil,total,keep,tempo,start=0):
    segs=[];cur=start
    for a,b in sil: segs.append((cur,a+keep/2));cur=b-keep/2
    segs.append((cur,total))
    f=''.join(f'[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS[s{i}];' for i,(a,b) in enumerate(segs))
    f+=''.join(f'[s{i}]' for i in range(len(segs)))+f'concat=n={len(segs)}:v=0:a=1,atempo={tempo}[o]'
    subprocess.run(['ffmpeg','-v','error','-y','-i',src,'-filter_complex',f,'-map','[o]','-ar','44100',out],check=True)
    def m(t):
        acc=0
        for a,b in segs:
            if t<=b: return (acc+max(0,t-a))/tempo
            acc+=b-a
        return acc/tempo
    return m
mr=build('reel_raw.mp3','reel_voice.mp3',[(.63,.91),(3.72,4.16),(5.55,5.78)],7.30,.08,1.08,start=.1)
ms=build('story_raw.mp3','story_voice.mp3',[(.66,1.0),(2.51,2.76),(4.16,4.47)],6.78,.08,1.08,start=.1)
print('reel', {k: round(mr(t), 2) for k, t in [('boum', .91), ('rire', 1.92), ('shofet', 2.82), ('kitvu', 4.16), ('vshilchu', 5.78), ('end', 7.3)]})
print('story', {k: round(ms(t), 2) for k, t in [('hashofet', 1.0), ('bareel', 2.76), ('kitvu', 4.47), ('end', 6.78)]})
