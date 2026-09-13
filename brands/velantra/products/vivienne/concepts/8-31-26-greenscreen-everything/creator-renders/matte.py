#!/usr/bin/env python3
"""Key each HeyGen green plate to an alpha VP9/webm. The green differs PER CREATOR
(HeyGen's backdrop is not consistent across sources), so the value is swept, never inherited.
despill mix stays at 0.15 -- 0.5 turns a light garment pink.
"""
import subprocess, tempfile, os
import numpy as np
from PIL import Image
from pathlib import Path

HERE = Path(__file__).resolve().parent
GREENS = {"A-diane": "0x008922", "B-bridget": "0x00BA5F", "C-marguerite": "0x00923A"}

def fringe(webm):
    """% of subject-edge pixels still carrying a green cast."""
    t = tempfile.mktemp(suffix=".png")
    subprocess.run(["ffmpeg","-v","error","-c:v","libvpx-vp9","-ss","3.0","-i",str(webm),
                    "-frames:v","1",t,"-y"], check=True)
    a = np.asarray(Image.open(t).convert("RGBA")).astype(int); os.unlink(t)
    r,g,b,al = a[:,:,0],a[:,:,1],a[:,:,2],a[:,:,3]
    vis = al > 40
    greenish = vis & (g > r + 28) & (g > b + 28)
    return 100.0 * greenish.sum() / max(vis.sum(), 1)

for name, key in GREENS.items():
    src = HERE / f"{name}-green.mp4"
    out = HERE / f"{name}-alpha.webm"
    vf = (f"chromakey={key}:0.10:0.02,despill=type=green:mix=0.15,"
          f"format=yuva420p")
    subprocess.run(["ffmpeg","-y","-v","error","-i",str(src),"-vf",vf,
                    "-c:v","libvpx-vp9","-pix_fmt","yuva420p","-b:v","0","-crf","24",
                    "-row-mt","1","-an",str(out)], check=True)
    print(f"{name}: key {key} -> {out.name}  fringe {fringe(out):.2f}%")
