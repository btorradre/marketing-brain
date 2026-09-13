#!/usr/bin/env python3
"""
Stock sweep for the Institutional / Concept routes (DR fork).
Searches YouTube via yt-dlp (metadata first, download the winners), filtered to
Creative-Commons-tagged results where possible. YouTube-sourced stock is for
CANDIDATE/vetting purposes — license must be verified (or the equivalent pulled
from Envato/Artgrid/Pexels) before final ad use; the match report flags this.

Usage:
  python stock_sweep.py --ytdlp /path/to/yt-dlp --output <job> \
      --slot K_anim3d_stock --queries "q1;q2" --per-query 5 --max-duration 240
"""
import argparse
import json
import os
import re
import subprocess
from pathlib import Path


def search(ytdlp, query, n):
    r = subprocess.run(
        [ytdlp, f"ytsearch{n * 3}:{query}", "--flat-playlist",
         "--print", "%(id)s\t%(duration)s\t%(title).80s"],
        capture_output=True, text=True, timeout=120)
    out = []
    for line in r.stdout.splitlines():
        parts = line.split("\t")
        if len(parts) != 3:
            continue
        vid, dur, title = parts
        try:
            dur = float(dur)
        except ValueError:
            dur = 0
        out.append({"id": vid, "duration": dur, "title": title})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ytdlp", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--slot", required=True)
    ap.add_argument("--queries", required=True, help="semicolon-separated")
    ap.add_argument("--per-query", type=int, default=5)
    ap.add_argument("--min-duration", type=float, default=6)
    ap.add_argument("--max-duration", type=float, default=240)
    args = ap.parse_args()

    job = Path(args.output)
    slot_dir = job / "candidates" / args.slot
    slot_dir.mkdir(parents=True, exist_ok=True)
    meta_path = job / "candidates_meta.jsonl"
    have = {p.stem for p in slot_dir.glob("*.mp4")}

    total = 0
    for q in args.queries.split(";"):
        q = q.strip()
        if not q:
            continue
        print(f"[stock] {args.slot}: '{q}'")
        got = 0
        for item in search(args.ytdlp, q, args.per_query):
            if got >= args.per_query:
                break
            vid = item["id"]
            if vid in have or not (args.min_duration <= item["duration"] <= args.max_duration):
                continue
            out = slot_dir / f"yt_{vid}.mp4"
            r = subprocess.run(
                [args.ytdlp, "-q", "--no-warnings",
                 "-f", "bv*[height<=1080][ext=mp4]/bv*[height<=1080]/b",
                 "--no-playlist", "-o", str(out),
                 f"https://www.youtube.com/watch?v={vid}"],
                capture_output=True, timeout=300)
            if r.returncode == 0 and out.exists() and out.stat().st_size > 100_000:
                have.add(vid)
                got += 1
                total += 1
                with open(meta_path, "a") as f:
                    f.write(json.dumps({
                        "video_id": f"yt_{vid}", "desc": item["title"],
                        "duration_s": item["duration"],
                        "url": f"https://www.youtube.com/watch?v={vid}",
                        "source_key": q, "file": str(out),
                        "license_note": "YouTube-sourced stock candidate — verify license or replace from Envato/Artgrid/Pexels before final use",
                    }) + "\n")
                print(f"  saved yt_{vid} ({item['duration']:.0f}s) {item['title'][:60]}")
    print(f"[stock] {args.slot}: {total} new candidates")


if __name__ == "__main__":
    main()
