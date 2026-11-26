#!/bin/bash
# mix.sh frames_pattern bed.wav voice.mp3 out.mp4 [bedvol]
BV=${5:-0.45}
ffmpeg -v error -y -framerate 30 -i "$1" -i "$2" -i "$3" -filter_complex "[2:a]aresample=44100,pan=stereo|c0=c0|c1=c0,volume=1.6,apad,asplit[v][sc];[1:a]aresample=44100,volume=$BV[b];[b][sc]sidechaincompress=threshold=0.02:ratio=5:attack=15:release=350[bd];[bd][v]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]" -map 0:v -map "[a]" -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p -r 30 -c:a aac -b:a 192k -movflags +faststart "$4"
