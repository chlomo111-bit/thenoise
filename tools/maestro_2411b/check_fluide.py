"""Contrôle anti-gel AVANT publication (15.11.2026).
Usage : python3 check_fluide.py final.mp4   -> code 0 si fluide, 1 sinon.
Mesure, sur l'image réduite, la part d'images identiques à la précédente (image répétée = petit gel)."""
import sys, subprocess, numpy as np
f = sys.argv[1]; W, H = 135, 240
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-vf', f'scale={W}:{H},format=gray', '-f', 'rawvideo', '-'], capture_output=True).stdout
a = np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(np.int16)
d = np.abs(a[1:] - a[:-1]).mean(axis=(1, 2))
rep = float((d < 0.15).mean()); jumps = int((d > 12).sum())
# plus longue suite d'images figées
run = best = 0
for x in d:
    run = run + 1 if x < 0.15 else 0; best = max(best, run)
ok = rep < 0.10 and best < 8
print(f'{f}: images répétées {rep:.0%}, plus long gel {best} images ({best/30:.2f} s), sauts brusques {jumps} -> {"OK" if ok else "SACCADÉ : interpoler à 30 i/s avant de publier"}')
sys.exit(0 if ok else 1)
