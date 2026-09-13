#!/usr/bin/env python3
"""Remove dead space from a VO track and rewrite its word timings to match.

Cuts any inter-word gap longer than KEEP down to KEEP seconds, plus any lead-in
and tail silence. Emits <stem>-tight.mp3 and <stem>-tight-words.json so the
picture edit can be cut to the tightened track.
Usage: tighten.py <words.json> <out-stem> [keep_seconds]
"""
import json, os, subprocess, sys

src_words = sys.argv[1]
out_stem = sys.argv[2]
KEEP = float(sys.argv[3]) if len(sys.argv) > 3 else 0.12
src_mp3 = src_words.replace("-words.json", ".mp3")

W = json.load(open(src_mp3.replace(".mp3", "-words.json")))
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                            "-of", "csv=p=0", src_mp3], capture_output=True, text=True).stdout.strip())

# Build keep-segments: everything except the slack inside oversized gaps.
cuts = []               # (start, end) of audio to REMOVE
if W[0]["s"] > KEEP:
    cuts.append((0.0, W[0]["s"] - KEEP))
for i in range(len(W) - 1):
    gap = W[i+1]["s"] - W[i]["e"]
    if gap > KEEP:
        cuts.append((W[i]["e"] + KEEP, W[i+1]["s"]))
tail = dur - W[-1]["e"]
if tail > KEEP:
    cuts.append((W[-1]["e"] + KEEP, dur))

removed = sum(e - s for s, e in cuts)
if not cuts:
    subprocess.run(["cp", src_mp3, out_stem + ".mp3"], check=True)
    json.dump(W, open(out_stem + "-words.json", "w"), indent=1)
    print(f"{os.path.basename(out_stem)}: nothing to remove ({dur:.2f}s)")
    raise SystemExit

# keep-ranges = complement of cuts
keeps, pos = [], 0.0
for s, e in cuts:
    if s > pos:
        keeps.append((pos, s))
    pos = e
if pos < dur:
    keeps.append((pos, dur))

sel = "+".join(f"between(t,{s:.4f},{e:.4f})" for s, e in keeps)
subprocess.run(["ffmpeg", "-v", "error", "-i", src_mp3,
                "-af", f"aselect='{sel}',asetpts=N/SR/TB",
                "-b:a", "192k", out_stem + ".mp3", "-y"], check=True)

# shift word timings by cumulative removal before each timestamp
def shift(t):
    return t - sum(min(e, t) - s for s, e in cuts if s < t)

NW = [{"w": x["w"], "s": round(shift(x["s"]), 3), "e": round(shift(x["e"]), 3)} for x in W]
json.dump(NW, open(out_stem + "-words.json", "w"), indent=1)

newdur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                               "-of", "csv=p=0", out_stem + ".mp3"], capture_output=True, text=True).stdout.strip())
print(f"{os.path.basename(out_stem):<18} {dur:5.2f}s -> {newdur:5.2f}s   removed {removed:.2f}s across {len(cuts)} gaps")
