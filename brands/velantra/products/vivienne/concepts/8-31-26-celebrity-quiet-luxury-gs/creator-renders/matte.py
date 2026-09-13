#!/usr/bin/env python3
"""Key each HeyGen green plate to an alpha VP9 webm.

The green is MEASURED off each render's own backdrop, never inherited - HeyGen's
backdrop is not consistent across sources. despill mix stays at 0.15; 0.5 turns a
light garment visibly pink.
"""
import os, subprocess, sys, tempfile
import numpy as np
from PIL import Image
from pathlib import Path

HERE = Path(__file__).resolve().parent
CREATORS = sys.argv[1:] or ["A-diane", "B-bridget", "C-marguerite"]

def measure(mp4):
    """Backdrop green from the TOP corners and top edge only - the subject fills the
    bottom of a 1080x1626 avatar plate, so bottom corners are garment, not backdrop."""
    t = tempfile.mktemp(suffix=".png")
    subprocess.run(["ffmpeg","-v","error","-ss","3.0","-i",str(mp4),"-frames:v","1",t,"-y"], check=True)
    a = np.asarray(Image.open(t).convert("RGB")); os.unlink(t)
    h, w, _ = a.shape
    px = np.concatenate([a[0:60,0:60].reshape(-1,3), a[0:60,w-60:w].reshape(-1,3),
                         a[0:40,w//2-30:w//2+30].reshape(-1,3)]).mean(0)
    return "0x%02X%02X%02X" % tuple(px.round().astype(int))

def fringe(webm):
    """% of visible subject pixels still carrying a green cast."""
    t = tempfile.mktemp(suffix=".png")
    subprocess.run(["ffmpeg","-v","error","-c:v","libvpx-vp9","-ss","3.0","-i",str(webm),
                    "-frames:v","1",t,"-y"], check=True)
    a = np.asarray(Image.open(t).convert("RGBA")).astype(int); os.unlink(t)
    r,g,b,al = a[:,:,0],a[:,:,1],a[:,:,2],a[:,:,3]
    vis = al > 40
    return 100.0 * (vis & (g > r+28) & (g > b+28)).sum() / max(vis.sum(), 1), vis.sum()

for name in CREATORS:
    src = HERE / f"{name}-green.mp4"
    if not src.exists(): print(f"{name}: no render yet, skipped"); continue
    key = measure(src)
    best = None
    for sim in ("0.08", "0.10", "0.12", "0.14"):          # swept, never inherited
        probe = HERE / f".sweep-{name}.webm"
        subprocess.run(["ffmpeg","-y","-v","error","-t","4","-i",str(src),
            "-vf",f"chromakey={key}:{sim}:0.02,despill=type=green:mix=0.15,format=yuva420p",
            "-c:v","libvpx-vp9","-pix_fmt","yuva420p","-b:v","0","-crf","30","-row-mt","1","-an",
            str(probe)], check=True)
        fr, vis = fringe(probe); probe.unlink()
        print(f"  {name} key {key} sim {sim}: fringe {fr:5.2f}%  subject px {vis}")
        if best is None or fr < best[1]: best = (sim, fr, vis)
    sim = best[0]
    out = HERE / f"{name}-alpha.webm"
    subprocess.run(["ffmpeg","-y","-v","error","-i",str(src),
        "-vf",f"chromakey={key}:{sim}:0.02,despill=type=green:mix=0.15,format=yuva420p",
        "-c:v","libvpx-vp9","-pix_fmt","yuva420p","-b:v","0","-crf","24","-row-mt","1","-an",
        str(out)], check=True)
    fr, vis = fringe(out)
    print(f"{name}: key {key} sim {sim} -> {out.name}  fringe {fr:.2f}%\n")
