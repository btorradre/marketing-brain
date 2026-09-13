#!/usr/bin/env python3
"""Stitch VEL-STRAWTOTE-BEACH-BAG-REPL-01: trim segments to the reference cut
lengths, concat, burn the persistent serif hook line (Pillow overlay) over the
full runtime, output final.mp4 (+ final_clean.mp4, no text)."""
import os
import subprocess

from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
SEG_DIR = os.path.join(BASE, "segments")
# (segment index, trimmed output length seconds) — matches reference cut points
CUTS = [(1, 4.03), (2, 1.37), (3, 1.80), (4, 1.57), (5, 1.01), (6, 1.95)]
W, H = 720, 1280
GEORGIA_B = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"
HOOK = "a beach bag that does it all"


def render_overlay(path):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype(GEORGIA_B, 36)
    tw = d.textlength(HOOK, font=font)
    x = (W - tw) / 2
    y = 218
    d.text((x + 2, y + 2), HOOK, font=font, fill=(0, 0, 0, 70))
    d.text((x, y), HOOK, font=font, fill=(255, 255, 255, 255))
    img.save(path)


def main():
    os.chdir(BASE)
    for idx, ln in CUTS:
        src = os.path.join(SEG_DIR, f"seg_{idx:02d}.mp4")
        dst = os.path.join(SEG_DIR, f"trim_{idx:02d}.mp4")
        subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-i", src, "-t", f"{ln:.2f}",
             "-vf", "scale=720:1280,fps=30", "-c:v", "libx264", "-preset",
             "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac",
             "-b:a", "128k", "-ar", "44100", dst], check=True)
        print(f"trim {idx}: {ln}s")

    concat = os.path.join(SEG_DIR, "concat.txt")
    with open(concat, "w") as f:
        for idx, _ in CUTS:
            f.write(f"file 'trim_{idx:02d}.mp4'\n")
    clean = os.path.join(BASE, "final_clean.mp4")
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
         "-i", concat, "-c", "copy", clean], check=True)
    print("final_clean.mp4 done")

    overlay = os.path.join(BASE, "title_overlay.png")
    render_overlay(overlay)
    final = os.path.join(BASE, "final.mp4")
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", clean, "-i", overlay,
         "-filter_complex", "[0:v][1:v]overlay=0:0",
         "-c:v", "libx264", "-preset", "medium", "-crf", "18",
         "-pix_fmt", "yuv420p", "-c:a", "copy", final], check=True)
    print("final.mp4 done")


if __name__ == "__main__":
    main()
