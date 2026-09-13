#!/usr/bin/env python3
"""Stitch VEL-STRAWTOTE-MEET-EMILIA-REPL-01: trim segments to the reference
cut lengths, concat, render the serif title overlay (Pillow), burn it over
0:00-11.4s with an alpha fade, output final.mp4 (+ final_clean.mp4, no text).
"""
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
SEG_DIR = os.path.join(BASE, "segments")
# (segment index, trimmed output length seconds) — matches reference cut points
CUTS = [(1, 3.0), (2, 3.5), (3, 4.5), (4, 2.5), (5, 2.0),
        (6, 6.5), (7, 4.5), (8, 3.0), (9, 4.3)]
W, H = 720, 1280
DIDOT = "/System/Library/Fonts/Supplemental/Didot.ttc"
SNELL = "/System/Library/Fonts/Supplemental/SnellRoundhand.ttc"


def tracked(draw, y, text, font, tracking, fill):
    widths = [draw.textlength(c, font=font) for c in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = (W - total) / 2
    for c, w in zip(text, widths):
        draw.text((x, y), c, font=font, fill=fill)
        x += w + tracking
    return total


def render_overlay(path):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    white = (255, 255, 255, 255)
    shadow = (0, 0, 0, 60)

    meet = ImageFont.truetype(DIDOT, 30)
    big = ImageFont.truetype(DIDOT, 96)
    frm = ImageFont.truetype(SNELL, 40, index=1)
    script = ImageFont.truetype(SNELL, 88, index=1)
    foot = ImageFont.truetype(DIDOT, 22)

    tracked(d, 470, "MEET THE", meet, 6, white)
    txt = "STRAW TOTE"
    tw = d.textlength(txt, font=big)
    d.text(((W - tw) / 2 + 2, 522 + 2), txt, font=big, fill=shadow)
    d.text(((W - tw) / 2, 522), txt, font=big, fill=white)
    tw = d.textlength("from", font=frm)
    d.text(((W - tw) / 2, 640), "from", font=frm, fill=white)
    txt = "Velantra"
    tw = d.textlength(txt, font=script)
    d.text(((W - tw) / 2 + 2, 692 + 2), txt, font=script, fill=shadow)
    d.text(((W - tw) / 2, 692), txt, font=script, fill=white)
    tracked(d, 1128, "COASTAL & EFFORTLESS", foot, 10, white)
    img.save(path)


def main():
    os.chdir(BASE)
    trims = []
    for i, length in CUTS:
        src = os.path.join(SEG_DIR, f"seg_{i:02d}.mp4")
        if not os.path.exists(src):
            sys.exit(f"missing {src} - run the seedance manifest first")
        dst = os.path.join(SEG_DIR, f"trim_{i:02d}.mp4")
        subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-i", src, "-t", f"{length}",
             "-vf", f"scale={W}:{H},fps=30,hqdn3d=1.5:1.5:4:4,unsharp=5:5:0.4",
             "-pix_fmt", "yuv420p",
             "-c:v", "libx264", "-crf", "18", "-preset", "medium",
             "-c:a", "aac", "-b:a", "192k", "-ar", "48000", dst], check=True)
        trims.append(dst)

    lst = os.path.join(SEG_DIR, "concat.txt")
    with open(lst, "w") as f:
        for p in trims:
            f.write(f"file '{p}'\n")
    clean = os.path.join(BASE, "final_clean.mp4")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                    "-i", lst, "-c:v", "libx264", "-crf", "18",
                    "-preset", "medium", "-c:a", "aac", "-b:a", "192k", clean],
                   check=True)

    ov = os.path.join(BASE, "title_overlay.png")
    render_overlay(ov)
    final = os.path.join(BASE, "final.mp4")
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", clean, "-i", ov,
         "-filter_complex",
         "[1:v]format=rgba,fade=t=out:st=11.0:d=0.4:alpha=1[ov];"
         "[0:v][ov]overlay=0:0:enable='lte(t,11.4)'",
         "-c:v", "libx264", "-crf", "18", "-preset", "medium",
         "-c:a", "copy", final], check=True)
    print(f"DONE -> {final}")


if __name__ == "__main__":
    main()
