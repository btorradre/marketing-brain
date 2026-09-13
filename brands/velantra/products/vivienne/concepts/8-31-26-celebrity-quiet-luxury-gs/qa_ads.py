#!/usr/bin/env python3
"""Per-ad QA strip: one frame at the midpoint of every cut, so the PiP side, the
captions, the key and the bed can all be read at a glance."""
import json, subprocess, sys, tempfile
from pathlib import Path
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
OUT  = HERE / "production/out"
beats = json.load(open(HERE / "beat-map-final.json"))

for ad in sorted(OUT.glob("VEL-VIV-CELEB-GS-01-*.mp4")):
    tmp = Path(tempfile.mkdtemp())
    tw, th, cols = 200, 356, 9
    rows = (len(beats) + cols - 1) // cols
    sheet = Image.new("RGB", (tw*cols, (th+20)*rows), (18,18,18)); d = ImageDraw.Draw(sheet)
    for k, b in enumerate(beats):
        t = (b["in"] + b["out"]) / 2
        p = tmp / f"{k}.jpg"
        subprocess.run(["ffmpeg","-v","error","-ss",str(t),"-i",str(ad),"-frames:v","1",
                        "-q:v","3",str(p),"-y"], check=True)
        sheet.paste(Image.open(p).resize((tw,th), Image.LANCZOS), ((k%cols)*tw, (k//cols)*(th+20)+20))
        d.text(((k%cols)*tw+4, (k//cols)*(th+20)+4), f"{b['cut']} {b['src']} [{b['pip']}]", fill=(255,255,255))
    dst = OUT / f"_qa-{ad.stem.split('-01-')[1]}.jpg"
    sheet.save(dst, quality=87); print("QA:", dst.name)
