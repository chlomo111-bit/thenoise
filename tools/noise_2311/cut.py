"""The Noise 22.11 — Coupe les silences de la voix (1 prise) + atempo, et donne les instants des phrases dans la voix montée. Usage : cd <dossier>; python3 cut.py"""
import subprocess,json
def build(src,out,sil,total,keep,tempo,lead=0):
    segs=[];cur=lead
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
SIL=[(2.83,3.14),(4.55,4.81),(6.45,6.89),(7.35,7.96),(8.51,8.70),(10.10,10.49),(10.95,11.19),(11.65,12.04),(12.58,12.84),(14.33,14.81),(16.21,16.44)]
mr=build('reel_raw.mp3','reel_voice.mp3',SIL,19.36,.12,1.1)
W={"bonim":0,"makhela":.9,"mezayefet":1.7,"10000":3.14,"laugh":4.81,"veakhshav":5.07,"efes":6.89,"like":7.96,"zamar":8.70,"tguva":10.49,"shlosha":11.19,"shituf":12.04,"shura":12.84,"kitvu":14.81,"chamesh":16.44,"nichnasot":18.0,"END":19.3}
print(json.dumps({k:round(mr(v),2) for k,v in W.items()}))
ms=build('story_raw.mp3','story_voice.mp3',[(2.06,2.38),(3.19,3.39)],6.15,.1,1.05)
print(json.dumps({k:round(ms(v),2) for k,v in {"efes":0,"shatfu":2.38,"eser":3.39,"END":6.1}.items()}))
