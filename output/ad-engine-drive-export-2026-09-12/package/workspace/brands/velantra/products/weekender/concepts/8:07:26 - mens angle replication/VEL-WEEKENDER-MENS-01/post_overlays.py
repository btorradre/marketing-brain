#!/usr/bin/env python3
"""VEL-WEEKENDER-MENS-01 post pass: burned overlays (Pillow PNGs, reference-style
chunked caps, upper left) + single-take VO mux over the assembled cut.
"Weekender" is never rendered natively by Seedance; it only exists here, in post."""
import subprocess, sys, os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "final.mp4")
VO = os.path.join(HERE, "VEL-WEEKENDER-MENS-01-VO.mp3")
OUT = os.path.join(HERE, "VEL-WEEKENDER-MENS-01-rolling-duffle.mp4")

W, H = 720, 1280
FONT_PATHS = ["/System/Library/Fonts/HelveticaNeue.ttc"]

def font(size, index=1):  # index 1 = Helvetica Neue Bold in the ttc
    for p in FONT_PATHS:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size, index=index)
            except OSError:
                return ImageFont.truetype(p, size)
    return ImageFont.load_default()

# (lines, start, end, big_first_line, centered)
OVERLAYS = [
    (["THIS"], 0.3, 4.7, True, False),
    (["3 DAYS.", "ONE BAG."], 5.3, 10.7, True, False),
    (["KEEPS", "ITS SHAPE"], 11.3, 15.7, True, False),
    (["BUILT", "TO LAST"], 16.3, 21.7, True, False),
    (["THE VELANTRA", "WEEKENDER"], 22.6, 27.9, False, True),
]

pngs = []
for i, (lines, t0, t1, big_first, centered) in enumerate(OVERLAYS, 1):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    y = H * 0.44 if centered else 250
    for j, line in enumerate(lines):
        size = 72 if (big_first and j == 0) else (48 if not centered else 56)
        f = font(size)
        bbox = d.textbbox((0, 0), line, font=f)
        tw = bbox[2] - bbox[0]
        x = (W - tw) / 2 if centered else 42
        for dx, dy in [(-2, 2), (2, 2), (-2, -2), (2, -2)]:  # soft edge for legibility
            d.text((x + dx, y + dy), line, font=f, fill=(0, 0, 0, 90))
        d.text((x, y), line, font=f, fill=(255, 255, 255, 255))
        y += size * 1.18
    p = os.path.join(HERE, f"overlay-{i}.png")
    img.save(p)
    pngs.append((p, t0, t1))

inputs = ["-i", SRC]
for p, _, _ in pngs:
    inputs += ["-i", p]
inputs += ["-i", VO]

fc, last = [], "0:v"
for k, (_, t0, t1) in enumerate(pngs, 1):
    out = f"v{k}"
    fc.append(f"[{last}][{k}:v]overlay=0:0:enable='between(t,{t0},{t1})'[{out}]")
    last = out
vo_idx = len(pngs) + 1
# room tone stays under the VO; VO enters at 0.35s
fc.append(f"[0:a]volume=0.10[amb]")
fc.append(f"[{vo_idx}:a]adelay=350|350,volume=1.3,alimiter=limit=0.97[vo]")
fc.append("[amb][vo]amix=inputs=2:duration=first:normalize=0[aout]")

cmd = ["ffmpeg", "-y", "-v", "error"] + inputs + [
    "-filter_complex", ";".join(fc),
    "-map", f"[{last}]", "-map", "[aout]",
    "-c:v", "libx264", "-crf", "18", "-preset", "medium",
    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", OUT,
]
subprocess.run(cmd, check=True)
print("wrote", OUT)
