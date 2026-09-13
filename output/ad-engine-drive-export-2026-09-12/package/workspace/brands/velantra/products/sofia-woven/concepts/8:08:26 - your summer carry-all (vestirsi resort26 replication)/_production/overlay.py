#!/usr/bin/env python3
"""Burns the VEL-SOFIA-CARRYALL-01 text plate onto the assembled cut.

The scene_replicator's built-in overlay is a bold, black-stroked UGC caption at
13% height. This ad's plate is the opposite: Helvetica Neue Light, all caps,
wide tracking, no stroke, slightly transparent, centred at mid frame — matching
the Vestirsi reference's treatment exactly.

The reference's second line is an influencer credit ("as seen on @..."). We do
not have that creator, so line 2 is the product name instead. Never invent a
handle.

usage: python3 overlay.py <in.mp4> <out.mp4>
"""
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

FONT = "/System/Library/Fonts/HelveticaNeue.ttc"
LIGHT, REGULAR = 7, 0

LINE1 = "YOUR SUMMER CARRY-ALL"
LINE2 = "the sofia woven tote"

# Proportions measured off the reference frame at 720x1280.
L1_SIZE = 0.0335      # of frame width
L1_TRACK = 0.30       # letter spacing, as a fraction of font size
L1_Y = 0.478          # top of line 1, as a fraction of frame height
L1_ALPHA = 236
L2_SIZE = 0.0225
L2_TRACK = 0.055
L2_GAP = 0.017        # gap below line 1, as a fraction of frame height
L2_ALPHA = 205


def tracked(draw, text, font, track_px):
    """Width of `text` rendered with `track_px` between glyphs."""
    return sum(draw.textlength(c, font=font) for c in text) + track_px * (len(text) - 1)


def draw_tracked(draw, text, font, track_px, cx, y, alpha):
    w = tracked(draw, text, font, track_px)
    x = cx - w / 2
    for c in text:
        draw.text((x, y), c, font=font, fill=(255, 255, 255, alpha))
        x += draw.textlength(c, font=font) + track_px


def render_plate(width, height, dest):
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx = width / 2

    f1 = ImageFont.truetype(FONT, int(width * L1_SIZE), index=LIGHT)
    f2 = ImageFont.truetype(FONT, int(width * L2_SIZE), index=REGULAR)

    y1 = height * L1_Y
    draw_tracked(draw, LINE1, f1, f1.size * L1_TRACK, cx, y1, L1_ALPHA)

    y2 = y1 + f1.size + height * L2_GAP
    draw_tracked(draw, LINE2, f2, f2.size * L2_TRACK, cx, y2, L2_ALPHA)

    img.save(dest)
    return dest


def probe(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height", "-of", "csv=p=0:s=x", path],
        capture_output=True, text=True, check=True).stdout.strip()
    w, h = out.split("x")
    return int(w), int(h)


def main(src, dst):
    w, h = probe(src)
    plate = os.path.join(os.path.dirname(os.path.abspath(dst)) or ".",
                         "_text-plate.png")
    render_plate(w, h, plate)
    subprocess.run(
        ["ffmpeg", "-v", "error", "-i", src, "-i", plate,
         "-filter_complex", "[0:v][1:v]overlay=0:0:format=auto[v]",
         "-map", "[v]", "-map", "0:a?", "-c:v", "libx264", "-crf", "17",
         "-preset", "slow", "-pix_fmt", "yuv420p", "-c:a", "copy",
         dst, "-y"], check=True)
    print(f"{dst}  ({w}x{h}, plate {plate})")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
