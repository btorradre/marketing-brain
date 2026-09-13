#!/usr/bin/env python3
"""
Per-slot contact sheets for the human pick.
==========================================
Adopted from b-roll-finder's law: the agent never picks the final b-roll —
the user does, from a contact sheet. For every clip in matched/<slot>/,
extracts N frames evenly across the (already-trimmed) clip and tiles all
clips into one labeled grid PNG per slot: contact_sheets/<slot>.png.

Each row = one clip: rank, confidence, video id, duration, frames.

Usage:
  venv/bin/python contact_sheet.py --output <job-dir> [--frames 5] [--slot S01]
"""

import argparse
import json
import os
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

THUMB_H = 210
LABEL_W = 128
PAD = 6


def clip_duration(path):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


def extract_frames(path, n, tmpdir):
    dur = clip_duration(path)
    if dur <= 0:
        return [], 0
    frames = []
    for i in range(n):
        t = dur * (i + 0.5) / n
        out = os.path.join(tmpdir, f"f{i}.jpg")
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t:.2f}",
             "-i", str(path), "-vframes", "1",
             "-vf", f"scale=-2:{THUMB_H}", out],
            capture_output=True)
        if os.path.exists(out):
            frames.append(Image.open(out).copy())
    return frames, dur


def font(size=15):
    for p in ("/System/Library/Fonts/Helvetica.ttc",
              "/System/Library/Fonts/Supplemental/Arial.ttf"):
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


def build_sheet(slot_dir, out_png, n_frames):
    clips = sorted(Path(slot_dir).glob("*.mp4"))
    if not clips:
        return 0
    rows = []
    with tempfile.TemporaryDirectory() as tmp:
        for c in clips:
            frames, dur = extract_frames(c, n_frames, tmp)
            if frames:
                rows.append((c.name, dur, frames))
    if not rows:
        return 0

    row_w = LABEL_W + sum(f.width + PAD for _, _, fr in rows[:1] for f in fr)
    max_w = max(LABEL_W + sum(f.width + PAD for f in fr) for _, _, fr in rows)
    total_h = PAD + len(rows) * (THUMB_H + PAD)
    sheet = Image.new("RGB", (max_w + PAD, total_h), (18, 18, 18))
    draw = ImageDraw.Draw(sheet)
    f_big, f_small = font(16), font(12)

    y = PAD
    for name, dur, frames in rows:
        parts = name.replace(".mp4", "").split("_")
        rank = parts[0] if parts else ""
        conf = parts[1] if len(parts) > 1 else ""
        vid = parts[-1] if parts else ""
        draw.text((8, y + 8), rank.upper(), fill=(255, 255, 255), font=f_big)
        draw.text((8, y + 34), conf, fill=(180, 220, 120), font=f_small)
        draw.text((8, y + 54), f"{dur:.0f}s", fill=(160, 160, 160), font=f_small)
        draw.text((8, y + 74), vid[-10:], fill=(120, 120, 120), font=f_small)
        x = LABEL_W
        for fr in frames:
            sheet.paste(fr, (x, y))
            x += fr.width + PAD
        y += THUMB_H + PAD

    sheet.save(out_png, quality=88)
    return len(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", required=True, help="job dir")
    ap.add_argument("--frames", type=int, default=5)
    ap.add_argument("--slot", help="only this slot")
    args = ap.parse_args()

    job = Path(args.output)
    sheets_dir = job / "contact_sheets"
    sheets_dir.mkdir(exist_ok=True)
    matched = job / "matched"
    slots = [d for d in sorted(matched.iterdir()) if d.is_dir()] if matched.exists() else []
    if args.slot:
        slots = [d for d in slots if d.name == args.slot]
    for d in slots:
        n = build_sheet(d, sheets_dir / f"{d.name}.png", args.frames)
        print(f"{d.name}: {n} clips -> {sheets_dir / (d.name + '.png')}")


if __name__ == "__main__":
    main()
