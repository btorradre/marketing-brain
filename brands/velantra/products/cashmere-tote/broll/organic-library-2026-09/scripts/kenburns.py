#!/usr/bin/env python3
"""SOP fallback for macro / hardware-heavy shots: 8s handheld-feel push-in from the approved keyframe."""
import os, subprocess, sys
from common import *
def render(cid, kf, out, secs=8, drift="in"):
    frames = secs * 30
    z = f"1+{0.10/frames:.6f}*on" if drift == "in" else f"1.10-{0.10/frames:.6f}*on"
    vf = ("scale=3240:5760:flags=lanczos,"
          f"zoompan=z='{z}':x='iw/2-(iw/zoom/2)+sin(on/37)*6':y='ih/2.1-(ih/zoom/2)+cos(on/29)*5':d={frames}:s=720x1280:fps=30,"
          "noise=alls=6:allf=t,format=yuv420p")
    r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-i", kf, "-vf", vf, "-t", str(secs),
                        "-r", "30", "-c:v", "libx264", "-preset", "medium", "-crf", "20", out])
    return r.returncode == 0 and os.path.getsize(out) > 100_000
if __name__ == "__main__":
    picks = load(os.path.join(STATE, "picks.json"), {})
    for cid in sys.argv[1:]:
        out = os.path.join(CLIPS, f"{cid}.mp4")
        print(cid, "ok" if render(cid, os.path.join(ROOT, picks[cid]["kf"]), out) else "FAIL")
