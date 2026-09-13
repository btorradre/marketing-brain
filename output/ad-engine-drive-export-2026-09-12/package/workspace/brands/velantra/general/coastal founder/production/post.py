#!/usr/bin/env python3
"""Post pass for VEL-COASTAL-FOUNDER-01.

assembled.mp4 (from scene_replicator finish) ->
  + phrase-timed white captions (Vestirsi style, Avenir, mid-left)
  + VELANTRA end-card wordmark (20.0s -> end, fade in)
  + ONE continuous VO track (costal founder.m4a) — no per-clip audio
-> final-captioned.mp4
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ASSEMBLED = os.path.join(HERE, "assembled.mp4")
VO = os.path.join(HERE, "..", "costal founder.m4a")
OUT = os.path.join(HERE, "final-captioned.mp4")
OVERLAY_DIR = os.path.join(HERE, "overlays")

# phrase, start, end — from whisper word timestamps of the actual VO take
CAPTIONS = [
    ("Velantra started", 1.28, 2.20),
    ("with two things,", 2.20, 3.55),
    ("a childhood spent sailing,", 3.66, 4.98),
    ("and three generations", 4.98, 6.60),
    ("of women in my family", 6.60, 7.52),
    ("who carried the same bags", 7.52, 8.72),
    ("for decades.", 8.72, 9.70),
    ("I couldn't find bags", 9.86, 11.22),
    ("made like that anymore,", 11.22, 12.34),
    ("so I decided to make them.", 12.44, 13.90),
    ("Something timeless and coastal,", 14.10, 15.75),
    ("built for one woman.", 15.84, 16.80),
    ("The woman who needs one bag", 17.00, 18.34),
    ("that works for every occasion.", 18.34, 19.80),
]
ENDCARD_START = 20.00


def find_font(names):
    for n in names:
        if os.path.exists(n):
            return n
    sys.exit("no usable font found")


def render_caption(text, w, h, dest, font_path):
    from PIL import Image, ImageDraw, ImageFont
    size = max(30, w // 17)
    # Avenir Next .ttc: hunt for a Regular/Medium face
    font = None
    for idx in range(12):
        try:
            f = ImageFont.truetype(font_path, size=size, index=idx)
            name = " ".join(f.getname())
            if "Regular" in name or "Medium" in name:
                font = f
                break
        except OSError:
            break
    if font is None:
        font = ImageFont.truetype(font_path, size=size)
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    x = int(w * 0.10)
    y = int(h * 0.455)
    # soft shadow for legibility on bright frames, no hard stroke
    for ox, oy, a in ((2, 2, 90), (1, 1, 120)):
        d.text((x + ox, y + oy), text, font=font, fill=(20, 20, 20, a))
    d.text((x, y), text, font=font, fill=(255, 255, 255, 242))
    img.save(dest)


def render_endcard(w, h, dest, font_path):
    from PIL import Image, ImageDraw, ImageFont
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    word = "VELANTRA"
    size = max(40, w // 10)
    font = ImageFont.truetype(font_path, size=size)
    tracking = int(size * 0.32)
    widths = [d.textbbox((0, 0), c, font=font)[2] for c in word]
    total = sum(widths) + tracking * (len(word) - 1)
    x = (w - total) // 2
    y = int(h * 0.47)
    for c, cw in zip(word, widths):
        for ox, oy, a in ((2, 2, 80),):
            d.text((x + ox, y + oy), c, font=font, fill=(20, 20, 20, a))
        d.text((x, y), c, font=font, fill=(255, 255, 255, 250))
        x += cw + tracking
    sub = "Find yours."
    sfont = ImageFont.truetype(font_path, size=max(20, w // 26))
    sw = d.textbbox((0, 0), sub, font=sfont)[2]
    sy = y + int(size * 1.55)
    d.text(((w - sw) // 2 + 1, sy + 1), sub, font=sfont, fill=(20, 20, 20, 80))
    d.text(((w - sw) // 2, sy), sub, font=sfont, fill=(255, 255, 255, 235))
    img.save(dest)


def main():
    if not os.path.exists(ASSEMBLED):
        sys.exit("assembled.mp4 missing — run scene_replicator finish first")
    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height", "-of", "csv=p=0", ASSEMBLED],
        capture_output=True, text=True)
    w, h = (int(x) for x in probe.stdout.strip().split(","))
    os.makedirs(OVERLAY_DIR, exist_ok=True)

    cap_font = find_font(["/System/Library/Fonts/Avenir Next.ttc",
                          "/System/Library/Fonts/Avenir.ttc",
                          "/System/Library/Fonts/HelveticaNeue.ttc"])
    mark_font = find_font(["/System/Library/Fonts/Optima.ttc",
                           "/System/Library/Fonts/Avenir Next.ttc",
                           "/System/Library/Fonts/HelveticaNeue.ttc"])

    pngs = []
    for i, (text, a, b) in enumerate(CAPTIONS):
        p = os.path.join(OVERLAY_DIR, f"cap{i:02d}.png")
        render_caption(text, w, h, p, cap_font)
        pngs.append((p, a, b))
    endcard = os.path.join(OVERLAY_DIR, "endcard.png")
    render_endcard(w, h, endcard, mark_font)

    cmd = ["ffmpeg", "-y", "-v", "error", "-i", ASSEMBLED]
    for p, _, _ in pngs:
        cmd += ["-i", p]
    cmd += ["-loop", "1", "-i", endcard, "-i", VO]

    n = len(pngs)
    parts = []
    prev = "[0:v]"
    for i, (_, a, b) in enumerate(pngs):
        out = f"[v{i}]"
        parts.append(f"{prev}[{i + 1}:v]overlay=0:0:enable='between(t,{a},{b})'{out}")
        prev = out
    # end card: fade the overlay itself in, then gate by time
    parts.append(f"[{n + 1}:v]format=rgba,fade=t=in:st={ENDCARD_START}:d=0.5:alpha=1[ec]")
    parts.append(f"{prev}[ec]overlay=0:0:enable='gte(t,{ENDCARD_START})'[vout]")

    vdur = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", ASSEMBLED], capture_output=True, text=True).stdout.strip()
    cmd += ["-filter_complex", ";".join(parts),
            "-map", "[vout]", "-map", f"{n + 2}:a",
            "-c:v", "libx264", "-crf", "18", "-preset", "medium",
            "-c:a", "aac", "-b:a", "192k", "-t", vdur,
            "-movflags", "+faststart", OUT]
    subprocess.run(cmd, check=True)
    dur = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", OUT], capture_output=True, text=True).stdout.strip()
    print(f"final-captioned.mp4 -> {OUT} ({float(dur):.2f}s)")


if __name__ == "__main__":
    main()
