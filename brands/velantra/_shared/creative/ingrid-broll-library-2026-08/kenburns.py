#!/usr/bin/env python3
"""SOP fallback: render a 10s handheld-feel push-in from the QA-passed keyframe.
Usage: python3 kenburns.py ING-077 ING-078 ...   (or no args = the default macro list)
"""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
picks = json.load(open(os.path.join(HERE, "state/picks.json")))
DEFAULT = ["ING-077-macro-turnlock", "ING-078-macro-clasp-plate", "ING-079-macro-handle-root",
           "ING-080-macro-stitch-topedge", "ING-081-macro-patina-crease", "ING-085-macro-grain-raking"]
args = sys.argv[1:]
IDS = [next(k for k in picks if k.startswith(a)) for a in args] if args else DEFAULT
for sid in IDS:
    kf = os.path.join(HERE, "keyframes", sid, picks[sid] + ".png")
    out = os.path.join(HERE, "clips", sid + ".mp4")
    # upscale 3x first so zoompan moves subpixel-smooth, then slow 1.00->1.11 push over 300 frames
    vf = ("scale=3240:5760:flags=lanczos,"
          "zoompan=z='1+0.00037*on':x='iw/2-(iw/zoom/2)':y='ih/2.15-(ih/zoom/2)':d=300:s=720x1280:fps=30,"
          "format=yuv420p")
    r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-i", kf,
                        "-vf", vf, "-t", "10", "-r", "30", "-c:v", "libx264", "-preset", "medium",
                        "-crf", "20", out])
    print(sid, "ok" if r.returncode == 0 and os.path.getsize(out) > 100_000 else "FAIL")
