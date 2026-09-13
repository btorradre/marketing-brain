#!/usr/bin/env python3
"""Stage 4 — trim every Omni clip to its scene target and concat into the finished reel.

Omni returns ~8s per clip. We take each one FROM THE START: the keyframe is frame one
and construction drift grows with time, so the head of the clip is always the cleanest
part of it. That is also why the scene targets are short.

  python3 assemble.py            # build the cut
  python3 assemble.py --check    # just report what is present and how long it would be
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from scenes import SCENES

CLIPS = os.path.join(ROOT, "clips")
WORK = os.path.join(HERE, "_assemble")
OUT = os.path.join(ROOT, "VEL-WEEKENDER-BLKCARRYON-01-final.mp4")
PICKS = json.load(open(os.path.join(HERE, "picks.json")))

# 9:16 at 1080p, the format both IG Reels and TikTok want.
W, H, FPS = 1080, 1920, 30


def dur(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=nw=1:nk=1", path], capture_output=True, text=True)
    return float(r.stdout.strip())


def main():
    check = "--check" in sys.argv
    os.makedirs(WORK, exist_ok=True)
    order = [s for s in SCENES if s["id"] in PICKS]
    parts, total, missing = [], 0.0, []

    for s in order:
        src = os.path.join(CLIPS, f"{s['id']}.mp4")
        if not os.path.exists(src):
            missing.append(s["id"])
            continue
        have = dur(src)
        take = min(s["target"], have)
        total += take
        print(f"  {s['id']}  clip {have:5.2f}s  ->  take {take:4.2f}s")
        if check:
            continue
        dst = os.path.join(WORK, f"{s['id']}.mp4")
        subprocess.run([
            "ffmpeg", "-y", "-v", "error", "-i", src, "-t", f"{take:.3f}",
            "-vf", (f"scale={W}:{H}:force_original_aspect_ratio=increase,"
                    f"crop={W}:{H},fps={FPS},format=yuv420p"),
            "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "18", dst,
        ], check=True)
        parts.append(dst)

    if missing:
        print(f"\n  MISSING CLIPS: {' '.join(missing)}")
    print(f"\n  {len(order)-len(missing)} scenes, {total:.1f}s")
    if check or not parts:
        return

    lst = os.path.join(WORK, "concat.txt")
    with open(lst, "w") as f:
        for p in parts:
            f.write(f"file '{p}'\n")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                    "-i", lst, "-c", "copy", OUT], check=True)
    print(f"\n  -> {OUT}  ({dur(OUT):.1f}s)")
    print("  Silent by design: drop a trending audio track on it in the IG/TikTok editor,")
    print("  the way the reference reel is cut.")


if __name__ == "__main__":
    main()
