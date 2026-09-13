#!/usr/bin/env python3
"""
detect_cuts.py — cut-aware segmentation for the seedance-prompt-architect skill.

Given a reference video, find where the hard cuts happen (ffmpeg scene
detection), then slice the video into segments where:

  * a segment ENDS at a cut, and
  * no segment is longer than --max seconds (default 15). A continuous shot
    longer than max is split into equal sub-segments so nothing exceeds the cap.
  * fragments shorter than --min seconds (default 1.0) are merged forward into
    the next segment (kills transition flashes / 2-frame blips).

This gives Claude a precise timeline to hang per-segment prompts on. Claude
still visually confirms/annotates each cut from the /watch frames — this script
only supplies the timestamps.

Output: segments.json
{
  "video": "...", "duration": 41.8, "scene_threshold": 0.3,
  "raw_cuts": [3.1, 7.4, 12.0, ...],
  "segments": [
    {"seg": 1, "start": 0.0, "end": 3.1, "duration": 3.1, "capped": false},
    ...
  ]
}
Also prints a human-readable table to stderr.
"""
import argparse, json, math, pathlib, re, subprocess, sys


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def probe_duration(video):
    r = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", video])
    try:
        return float(r.stdout.strip())
    except ValueError:
        print(f"[detect_cuts] could not probe duration of {video}", file=sys.stderr)
        sys.exit(2)


def detect_cuts(video, threshold):
    """Return sorted list of cut timestamps (seconds) via ffmpeg scene score."""
    r = run(["ffmpeg", "-i", video, "-filter:v",
             f"select='gt(scene,{threshold})',showinfo", "-f", "null", "-"])
    # showinfo lines look like: ... pts_time:3.12 ...
    times = [float(m) for m in re.findall(r"pts_time:([0-9.]+)", r.stderr)]
    return sorted(set(round(t, 3) for t in times))


def build_segments(duration, cuts, min_s, max_s):
    boundaries = [0.0] + [c for c in cuts if 0.0 < c < duration] + [duration]
    # merge sub-min fragments forward
    merged = [boundaries[0]]
    for b in boundaries[1:]:
        if b - merged[-1] < min_s and b != duration:
            continue  # skip this boundary → fragment folds into next
        merged.append(b)
    if merged[-1] != duration:
        merged[-1] = duration

    segs = []
    for a, b in zip(merged, merged[1:]):
        span = b - a
        if span <= max_s + 1e-6:
            segs.append((a, b, False))
        else:
            n = math.ceil(span / max_s)
            step = span / n
            for i in range(n):
                s = a + i * step
                e = a + (i + 1) * step if i < n - 1 else b
                segs.append((s, e, True))
    return [
        {"seg": i + 1, "start": round(s, 2), "end": round(e, 2),
         "duration": round(e - s, 2), "capped": capped}
        for i, (s, e, capped) in enumerate(segs)
    ]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--video", required=True, help="path to the reference video (local file)")
    p.add_argument("--max", type=float, default=15.0, help="max segment length seconds (default 15)")
    p.add_argument("--min", type=float, default=1.0, help="merge fragments shorter than this (default 1.0)")
    p.add_argument("--threshold", type=float, default=0.3,
                   help="ffmpeg scene-change sensitivity 0-1, lower = more cuts (default 0.3)")
    p.add_argument("--output", required=True, help="segments.json output path")
    a = p.parse_args()

    if not pathlib.Path(a.video).exists():
        print(f"[detect_cuts] video not found: {a.video}", file=sys.stderr)
        sys.exit(2)

    duration = probe_duration(a.video)
    cuts = detect_cuts(a.video, a.threshold)
    segments = build_segments(duration, cuts, a.min, a.max)

    out = {
        "video": a.video, "duration": round(duration, 2),
        "scene_threshold": a.threshold, "max_segment_s": a.max, "min_fragment_s": a.min,
        "raw_cuts": cuts, "segments": segments,
    }
    pathlib.Path(a.output).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.output).write_text(json.dumps(out, indent=2))

    print(f"[detect_cuts] {duration:.1f}s video · {len(cuts)} cuts · "
          f"{len(segments)} segments (max {a.max}s)", file=sys.stderr)
    for s in segments:
        flag = "  [split@max]" if s["capped"] else ""
        print(f"  SEG {s['seg']:02d}  {s['start']:6.2f}–{s['end']:6.2f}  "
              f"({s['duration']:4.1f}s){flag}", file=sys.stderr)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
