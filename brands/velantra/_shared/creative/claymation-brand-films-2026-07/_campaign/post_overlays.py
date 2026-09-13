#!/usr/bin/env python3
"""Post overlays for the claymation films (Pillow caption PNG + ffmpeg overlay).

SPILL: "Perfect for the weekend."  over the back half of S4 (17.2s-19.8s)
MADAM: "No luggage, madam?"        over S2 (5.6s-9.4s)

Captions are never generated natively (Seedance text ban). Storybook style:
white serif italic, soft shadow, low in frame. Writes *-final-captioned.mp4.
"""
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
CAMP = os.path.dirname(HERE)

FONTS = [
    "/System/Library/Fonts/Supplemental/Georgia Italic.ttf",
    "/System/Library/Fonts/Supplemental/Times New Roman Italic.ttf",
    "/System/Library/Fonts/Supplemental/Baskerville.ttc",
    "/System/Library/Fonts/HelveticaNeue.ttc",
]

JOBS = [
    ("VEL-CLAY-SPILL-01", "Perfect for the weekend.", 17.2, 19.8),
    ("VEL-CLAY-MADAM-01", "No luggage, madam?", 5.6, 9.4),
]

def font_path():
    for f in FONTS:
        if os.path.exists(f):
            return f
    sys.exit("no serif font found")

def make_caption(text, vid_w, vid_h, dest):
    size = max(28, int(vid_w * 0.055))
    font = ImageFont.truetype(font_path(), size)
    pad = size
    tmp = Image.new("RGBA", (vid_w * 2, size * 3))
    d = ImageDraw.Draw(tmp)
    box = d.textbbox((0, 0), text, font=font)
    tw, th = box[2] - box[0], box[3] - box[1]
    img = Image.new("RGBA", (tw + pad * 2, th + pad * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    x, y = pad - box[0], pad - box[1]
    for dx, dy in ((2, 2), (2, 3), (3, 2)):  # soft shadow
        d.text((x + dx, y + dy), text, font=font, fill=(30, 25, 20, 130))
    d.text((x, y), text, font=font, fill=(255, 253, 248, 255))
    img.save(dest)
    return img.size

def probe_wh(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                          "-show_entries", "stream=width,height", "-of", "csv=p=0", path],
                         capture_output=True, text=True).stdout.strip().split(",")
    return int(out[0]), int(out[1])

def main():
    for film_dir, text, t0, t1 in JOBS:
        final = os.path.join(CAMP, film_dir, "output", f"{film_dir}-final.mp4")
        if not os.path.exists(final):
            print(f"{film_dir}: final missing, skip"); continue
        w, h = probe_wh(final)
        cap = os.path.join(CAMP, film_dir, "output", "caption.png")
        cw, ch = make_caption(text, w, h, cap)
        out = final.replace("-final.mp4", "-final-captioned.mp4")
        y = int(h * 0.86) - ch // 2
        subprocess.run(["ffmpeg", "-y", "-i", final, "-i", cap,
            "-filter_complex",
            f"[0:v][1:v]overlay=x=(W-w)/2:y={y}:enable='between(t,{t0},{t1})'",
            "-c:v", "libx264", "-crf", "18", "-preset", "medium",
            "-c:a", "copy", out], check=True, capture_output=True)
        print(f"{film_dir}: {os.path.basename(out)}")

if __name__ == "__main__":
    main()
