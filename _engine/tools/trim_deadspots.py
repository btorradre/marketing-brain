#!/usr/bin/env python3
"""
trim_deadspots.py — find dead air in generated clips and cut it so a chain stitches seamlessly.

Every fixed-container engine (Omni ~10s, Flow's omni.edit 9.685s) returns the same clip
length no matter how long the speech actually runs, so each segment arrives padded with
silence at the tail and often a beat of nothing at the head. Concatenated raw, that reads
as a stuttering pause at every seam.

Length gets corrected by TRIMMING, never by changing playback speed — speed changes shift
formants and the voice stops matching the anchor.

    python3 trim_deadspots.py <clips_dir> [--out <dir>] [--concat final.mp4]
    python3 trim_deadspots.py <clips_dir> --report        # analyse only, cut nothing

Head/tail silence is trimmed by default. Internal gaps are only REPORTED, because cutting
mid-clip in a locked-off talking head produces a visible jump; pass --collapse-internal to
cut them anyway (best paired with a short crossfade in the NLE).
"""
import argparse
import json
import pathlib
import re
import subprocess
import sys

SILENCE_START = re.compile(r"silence_start:\s*(-?[\d.]+)")
SILENCE_END = re.compile(r"silence_end:\s*([\d.]+)\s*\|\s*silence_duration:\s*([\d.]+)")


def run(cmd: list[str]) -> str:
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.stdout + p.stderr


def duration(path: pathlib.Path) -> float:
    out = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
               "-of", "default=nw=1:nk=1", str(path)]).strip()
    try:
        return float(out.splitlines()[0])
    except (ValueError, IndexError):
        return 0.0


def silences(path: pathlib.Path, noise_db: int, min_dur: float) -> list[tuple[float, float]]:
    """Return [(start, end)] of every detected silent run."""
    out = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
               "-af", f"silencedetect=noise={noise_db}dB:d={min_dur}", "-f", "null", "-"])
    spans, start = [], None
    for line in out.splitlines():
        if (m := SILENCE_START.search(line)):
            start = max(0.0, float(m.group(1)))
        if (m := SILENCE_END.search(line)) and start is not None:
            spans.append((start, float(m.group(1))))
            start = None
    if start is not None:                       # silence ran to end of file
        spans.append((start, duration(path)))
    return spans


def analyse(path: pathlib.Path, noise_db: int, min_dur: float, pad: float) -> dict:
    dur = duration(path)
    spans = silences(path, noise_db, min_dur)
    head = next((e for s, e in spans if s <= 0.05), 0.0)
    tail = next((s for s, e in spans if e >= dur - 0.05), dur)
    internal = [(s, e) for s, e in spans if s > 0.05 and e < dur - 0.05]

    speech_in = max(0.0, head - pad)
    speech_out = min(dur, tail + pad)
    return {
        "file": path.name,
        "duration": round(dur, 3),
        "speech_in": round(speech_in, 3),
        "speech_out": round(speech_out, 3),
        "speech_length": round(speech_out - speech_in, 3),
        "trimmed_head": round(speech_in, 3),
        "trimmed_tail": round(dur - speech_out, 3),
        "internal_gaps": [{"start": round(s, 3), "end": round(e, 3), "len": round(e - s, 3)}
                          for s, e in internal],
        "all_silent": speech_out - speech_in < 0.4,
    }


def cut(src: pathlib.Path, dst: pathlib.Path, start: float, end: float,
        drops: list[tuple[float, float]]) -> None:
    """Re-encode the kept span. Frame-accurate cuts need a re-encode, not a stream copy."""
    if drops:
        keep, cursor = [], start
        for s, e in drops:
            if s > cursor:
                keep.append((cursor, s))
            cursor = e
        if cursor < end:
            keep.append((cursor, end))
        v = "".join(f"[0:v]trim={s}:{e},setpts=PTS-STARTPTS[v{i}];" for i, (s, e) in enumerate(keep))
        a = "".join(f"[0:a]atrim={s}:{e},asetpts=PTS-STARTPTS[a{i}];" for i, (s, e) in enumerate(keep))
        legs = "".join(f"[v{i}][a{i}]" for i in range(len(keep)))
        fc = f"{v}{a}{legs}concat=n={len(keep)}:v=1:a=1[v][a]"
        cmd = ["ffmpeg", "-y", "-i", str(src), "-filter_complex", fc, "-map", "[v]", "-map", "[a]"]
    else:
        cmd = ["ffmpeg", "-y", "-ss", str(start), "-to", str(end), "-i", str(src)]
    cmd += ["-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", str(dst)]
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        sys.exit(f"ffmpeg failed on {src.name}:\n{p.stderr[-1500:]}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("clips_dir")
    ap.add_argument("--out")
    ap.add_argument("--concat")
    ap.add_argument("--report", action="store_true", help="analyse only, write nothing")
    ap.add_argument("--noise-db", type=int, default=-35, help="dB floor counted as silence")
    ap.add_argument("--min-silence", type=float, default=0.35, help="shortest run counted, seconds")
    ap.add_argument("--pad", type=float, default=0.08, help="breath kept either side of speech")
    ap.add_argument("--collapse-internal", action="store_true",
                    help="also cut internal gaps (visible jump in a locked-off shot)")
    ap.add_argument("--internal-threshold", type=float, default=0.7)
    ap.add_argument("--prefix", default="seg", help="clip basename before the number")
    args = ap.parse_args()

    src_dir = pathlib.Path(args.clips_dir)
    # Match seg-<n>.mp4 ONLY, and order by that number. A bare *.mp4 glob also picks up
    # take files and the voice anchor, and lexicographic sort puts seg-10 before seg-2,
    # which silently concatenates the script out of order.
    numbered = []
    for p in src_dir.glob("*.mp4"):
        m = re.fullmatch(rf"{re.escape(args.prefix)}-(\d+)\.mp4", p.name)
        if m:
            numbered.append((int(m.group(1)), p))
    clips = [p for _, p in sorted(numbered)]
    if not clips:
        sys.exit(f"no {args.prefix}-<n>.mp4 clips in {src_dir}")
    missing = set(range(1, max(n for n, _ in numbered) + 1)) - {n for n, _ in numbered}
    if missing:
        print(f"WARNING: gap in sequence, missing {sorted(missing)}", file=sys.stderr)

    out_dir = pathlib.Path(args.out or src_dir / "trimmed")
    if not args.report:
        out_dir.mkdir(parents=True, exist_ok=True)

    reports, kept_total, raw_total = [], 0.0, 0.0
    for clip in clips:
        r = analyse(clip, args.noise_db, args.min_silence, args.pad)
        raw_total += r["duration"]
        kept_total += r["speech_length"]
        reports.append(r)

        flags = []
        if r["all_silent"]:
            flags.append("ALL SILENT — regenerate")
        big = [g for g in r["internal_gaps"] if g["len"] >= args.internal_threshold]
        if big:
            flags.append(f"{len(big)} internal gap(s) >= {args.internal_threshold}s")
        print(f"{r['file']:<28} {r['duration']:>6.2f}s -> {r['speech_length']:>6.2f}s   "
              f"head -{r['trimmed_head']:.2f}  tail -{r['trimmed_tail']:.2f}"
              f"{'   [' + '; '.join(flags) + ']' if flags else ''}")
        for g in big:
            print(f"{'':<28}   gap {g['start']:.2f}-{g['end']:.2f} ({g['len']:.2f}s)")

        if not args.report and not r["all_silent"]:
            drops = [(g["start"], g["end"]) for g in big] if args.collapse_internal else []
            cut(clip, out_dir / clip.name, r["speech_in"], r["speech_out"], drops)

    print(f"\n{len(clips)} clips: {raw_total:.1f}s raw -> {kept_total:.1f}s speech "
          f"({raw_total - kept_total:.1f}s dead air removed)")

    if not args.report:
        (out_dir / "trim_report.json").write_text(json.dumps(reports, indent=2))
        print(f"-> {out_dir}")

    if args.concat and not args.report:
        listing = out_dir / "concat.txt"
        # Reuse the numerically-ordered input list. Re-globbing here would sort
        # lexicographically and silently emit seg-1, seg-10, seg-11 ... seg-2 — a
        # scrambled script that still reports the correct total duration.
        ordered = [c.name for c in clips if (out_dir / c.name).exists()]
        listing.write_text("".join(f"file '{n}'\n" for n in ordered))
        final = pathlib.Path(args.concat)

        # Decode and re-encode through the concat FILTER rather than stream-copying with
        # the demuxer. Every AAC file carries encoder priming samples at its head; a
        # stream copy re-inserts those at each join, which punches a ~80ms hole into the
        # audio at every seam. On a chain whose beats split mid-sentence, that reads as
        # dropped words. Decoding to PCM first and encoding once at the end makes the
        # audio genuinely continuous.
        cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"]
        for name in ordered:
            cmd += ["-i", str(out_dir / name)]
        n = len(ordered)
        legs = "".join(f"[{i}:v:0][{i}:a:0]" for i in range(n))
        cmd += ["-filter_complex", f"{legs}concat=n={n}:v=1:a=1[v][a]",
                "-map", "[v]", "-map", "[a]",
                "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart",
                str(final)]
        p = subprocess.run(cmd, capture_output=True, text=True)
        if p.returncode != 0:
            sys.exit(f"concat failed:\n{p.stderr[-1500:]}")
        print(f"-> {final}  ({duration(final):.1f}s)")


if __name__ == "__main__":
    main()
