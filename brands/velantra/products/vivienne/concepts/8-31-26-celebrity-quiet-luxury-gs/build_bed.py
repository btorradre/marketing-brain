#!/usr/bin/env python3
"""Bed for VEL-VIV-CELEB-GS-01: 17 cuts, re-timed off the real VO alignment.

Each celebrity still appears EXACTLY ONCE, as a HARD HOLD - no push-in, no drift.
There is no burned price card: the $10,000 lands in the voiceover and in the ordinary
word-synced caption, not as a graphic.
"""
import json, subprocess, tempfile
from pathlib import Path
from PIL import Image, ImageFilter

HERE  = Path(__file__).resolve().parent
VIV   = HERE.parent.parent
BROLL = VIV / "broll/final"
BF    = HERE / "board-frames"
PROD  = HERE / "production"; PROD.mkdir(exist_ok=True)
W, H, FPS = 1080, 1920, 24
FONT = "/System/Library/Fonts/Helvetica.ttc"

# src -> how to get a 1080x1920 frame/clip
STILL = {
 "HOOK-A": BF / "c01-HOOK-A-katie.jpg",
 "HOOK-B": BF / "c02-HOOK-B-sofia.jpg",
}
CLIP  = {"GAP-02": (BROLL / "O2.mp4", 5.5),          # approved fallback: bare front panel, hand clear
         "PDP-SCROLL": (HERE / "broll-new/PDP-scroll.mp4", 0.0)}

def sharpen(src, dst):
    """Katie's source is 398x768. LANCZOS alone reads mushy at 1080; a light unsharp
    puts the press-photo edge back without haloing."""
    im = Image.open(src).convert("RGB")
    im = im.filter(ImageFilter.UnsharpMask(radius=2.2, percent=115, threshold=3))
    im.save(dst, quality=95); return dst

def seg(b, out):
    src, sin, dur = b["src"], b["src_in"], b["out"] - b["in"]
    if src in STILL:
        tmp = PROD / f"_{b['cut']}.jpg"
        if src == "HOOK-A": sharpen(STILL[src], tmp)
        else:               tmp.write_bytes(STILL[src].read_bytes())
        # HARD HOLD: -loop on a single image, zero zoom, zero pan
        subprocess.run(["ffmpeg","-v","error","-y","-loop","1","-i",str(tmp),"-t",f"{dur:.3f}",
            "-vf",f"scale={W}:{H},fps={FPS},format=yuv420p","-c:v","libx264","-crf","17",
            "-preset","veryfast",str(out)], check=True)
        return
    path, ss = CLIP.get(src, (BROLL / f"{src}.mp4", sin or 0.0))
    subprocess.run(["ffmpeg","-v","error","-y","-ss",f"{ss:.3f}","-t",f"{dur:.3f}","-i",str(path),
        "-vf",f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS}",
        "-c:v","libx264","-crf","17","-preset","veryfast","-pix_fmt","yuv420p","-an",
        str(out)], check=True)

if __name__ == "__main__":
    beats = json.load(open(HERE / "beat-map-final.json"))
    tmp = Path(tempfile.mkdtemp()); parts = []
    for b in beats:
        p = tmp / f"{b['cut']}.mp4"; seg(b, p); parts.append(p)
        d = float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
            "-of","csv=p=0",str(p)],capture_output=True,text=True).stdout)
        want = b["out"] - b["in"]
        flag = "  ** SHORT **" if d < want - 0.05 else ""
        print(f"  {b['cut']} {b['src']:<12} want {want:5.2f}s got {d:5.2f}s{flag}")
    lst = tmp / "l.txt"; lst.write_text("".join(f"file '{p}'\n" for p in parts))
    bed = PROD / "bed.mp4"
    subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i",str(lst),
        "-c:v","libx264","-crf","18","-preset","medium","-pix_fmt","yuv420p","-r",str(FPS),
        str(bed)], check=True)
    print("bed:", bed, subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
        "-of","csv=p=0",str(bed)],capture_output=True,text=True).stdout.strip(), "s")
