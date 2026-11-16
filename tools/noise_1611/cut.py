"""Noise 16.11 : coupe les silences de la voix (reel + story) et donne le minutage après coupe. À lancer dans le dossier des mp3."""
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
mr=build('reel_raw.mp3','reel_voice.mp3',[(.30,.46),(2.20,2.58),(3.31,3.62),(4.48,4.90),(6.06,6.55)],9.0,.08,1.1)
ms=build('story_raw.mp3','story_voice.mp3',[(3.73,4.06),(5.58,5.98)],8.45,.08,1.12)
print({k:round(mr(t),2) for k,t in [('a',.46),('shofet',2.58),('sotem',3.62),('mistovev',4.90),('kitvu',6.55),('end',9.0)]})
print({k:round(ms(t),2) for k,t in [('uv',4.06),('kitvu',5.98),('end',8.45)]})
