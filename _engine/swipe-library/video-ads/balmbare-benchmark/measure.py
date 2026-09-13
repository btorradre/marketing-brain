#!/usr/bin/env python3
"""Measure the Balmbare benchmark: real cut timestamps, shot lengths, frames.

Pacing claims in a rubric are worthless unless they come from measurement, so
this pulls the actual scene-change timestamps out of ffmpeg rather than eyeballing.
"""
import json, re, subprocess, sys, urllib.request
from pathlib import Path

OUT = Path(__file__).parent / "benchmark"
OUT.mkdir(exist_ok=True)

ADS = [
    ("a01_md_hook",        "24336111476058299", 203, 20852),
    ("a02_podcast_doctor", "815587837523468",   104, 21459),
    ("a03_why_didnt_work", "2037141337152097",   48, 31726),
    ("a04_top_reach",      "1648124513139196",   43, 43034),
    ("a05_not_just_hair",  "989783990151240",    54, 18566),
    ("a06_dht_block",      "3366050580226978",   95, 13609),
    ("a07_longest_240d",   "1761655691900219",  240,   461),
    ("a08_nurse_science",  "2473457769677120",  223,   987),
    ("a09_chewies",        "1250384376495449",  182,  3699),
    ("a10_dht_ie",         "799794902527296",    95, 10847),
]
BASE = "https://medias.trendtrack.io/video/facebook/{}.mp4"


def sh(cmd, timeout=600):
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    return p.returncode, p.stdout, p.stderr


def duration(path):
    _, out, _ = sh(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                    "-of", "default=nw=1:nk=1", str(path)])
    try:
        return round(float(out.strip()), 2)
    except ValueError:
        return 0.0


def cut_times(path, thresh=0.28):
    """Real scene-change timestamps via showinfo on the select filter."""
    _, _, err = sh(["ffmpeg", "-v", "info", "-i", str(path),
                    "-vf", f"select='gt(scene,{thresh})',showinfo",
                    "-f", "null", "-"], timeout=900)
    return [round(float(m), 2) for m in re.findall(r"pts_time:([0-9.]+)", err)]


results = []
for name, vid, days, reach in ADS:
    dest = OUT / name
    dest.mkdir(exist_ok=True)
    mp4 = dest / "ad.mp4"
    if not mp4.exists():
        # curl, not urllib: python's cert store is not wired up in this vault
        rc, _, err = sh(["curl", "-fsSL", "--max-time", "300",
                         "-o", str(mp4), BASE.format(vid)], timeout=360)
        if rc != 0 or not mp4.exists() or mp4.stat().st_size < 10000:
            print(f"{name}: download failed {err[:150]}", file=sys.stderr)
            mp4.unlink(missing_ok=True)
            continue
    dur = duration(mp4)
    cuts = cut_times(mp4)
    # shot lengths = gaps between consecutive cuts, bookended by 0 and duration
    marks = [0.0] + cuts + [dur]
    shots = [round(marks[i + 1] - marks[i], 2) for i in range(len(marks) - 1)]
    shots = [s for s in shots if s > 0.05]

    fdir = dest / "frames"
    fdir.mkdir(exist_ok=True)
    # hook: first 4s at 4fps
    sh(["ffmpeg", "-y", "-v", "error", "-i", str(mp4), "-t", "4",
        "-vf", "fps=4,scale=560:-2", "-frames:v", "16",
        str(fdir / "hook_%02d.jpg")], timeout=300)
    # body: one frame per detected cut
    sh(["ffmpeg", "-y", "-v", "error", "-i", str(mp4),
        "-vf", f"select='gt(scene,0.28)',scale=560:-2", "-fps_mode", "vfr",
        "-frames:v", "30", str(fdir / "cut_%02d.jpg")], timeout=900)

    r = {
        "name": name, "video_id": vid, "days_running": days, "reach": reach,
        "duration": dur, "cuts": len(cuts), "cut_times": cuts,
        "shot_lengths": shots,
        "avg_shot": round(sum(shots) / len(shots), 2) if shots else None,
        "median_shot": round(sorted(shots)[len(shots) // 2], 2) if shots else None,
        "cuts_in_first_5s": len([c for c in cuts if c <= 5]),
        "first_cut_at": cuts[0] if cuts else None,
        "cuts_per_sec": round(len(cuts) / dur, 2) if dur else None,
    }
    results.append(r)
    print(f"{name:22} {dur:6.1f}s  {len(cuts):3d} cuts  avg shot {r['avg_shot']}s  "
          f"first cut {r['first_cut_at']}s  {r['cuts_in_first_5s']} cuts in first 5s",
          flush=True)

(OUT / "measurements.json").write_text(json.dumps(results, indent=2))
if results:
    durs = [r["duration"] for r in results]
    avgs = [r["avg_shot"] for r in results if r["avg_shot"]]
    firsts = [r["first_cut_at"] for r in results if r["first_cut_at"] is not None]
    print("\n=== AGGREGATE ===")
    print(f"n={len(results)}  duration {min(durs):.0f}-{max(durs):.0f}s "
          f"(median {sorted(durs)[len(durs)//2]:.0f}s)")
    print(f"avg shot length across ads: {sum(avgs)/len(avgs):.2f}s "
          f"(range {min(avgs):.2f}-{max(avgs):.2f})")
    print(f"first cut lands at: median {sorted(firsts)[len(firsts)//2]:.2f}s, "
          f"range {min(firsts):.2f}-{max(firsts):.2f}")
