#!/usr/bin/env python3
"""SOP fallback: render a 10s handheld-feel push-in from the QA-passed keyframe."""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
picks = json.load(open(os.path.join(HERE, "state/picks.json")))
IDS = ["COL-050-home-radiator-window","COL-083-macro-corner-base","COL-085-macro-side-gusset",
       "COL-086-macro-interior-shadow","MAR-008-commute-taxi-exit","MAR-011-commute-bike-lane-wait",
       "MAR-031-cafe-bench-seat","MAR-038-car-seat-golden","MAR-077-macro-turnlock",
       "MAR-080-macro-keeper-strap","MAR-088-setdown-bench-lobby"]
for sid in IDS:
    kf = os.path.join(HERE, "keyframes", sid, picks[sid] + ".png")
    out = os.path.join(HERE, "clips", sid + ".mp4")
    # upscale 3x first so zoompan moves subpixel-smooth, then slow 1.00->1.11 push over 300 frames
    vf = ("scale=3240:5760:flags=lanczos,"
          "zoompan=z='1+0.00037*on':x='iw/2-(iw/zoom/2)':y='ih/2.15-(ih/zoom/2)':d=300:s=720x1280:fps=30,"
          "format=yuv420p")
    r = subprocess.run(["ffmpeg","-y","-loglevel","error","-loop","1","-i",kf,
                        "-vf",vf,"-t","10","-r","30","-c:v","libx264","-preset","medium","-crf","20",out])
    print(sid, "ok" if r.returncode==0 and os.path.getsize(out)>100_000 else "FAIL")
