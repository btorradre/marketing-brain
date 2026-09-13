#!/usr/bin/env python3
"""Assemble VEL-WEEKENDER-OVERSIZED-01 v2: bed + KEYED creator (green screen,
cut by the frame edge per the house geometry) + captions + VO + music.

Creator sizing follows feedback_greenscreen_pip_edge_cut: size on the HEAD
(head ~20% of frame width), head centre 16% in from the near edge, body runs
past the bottom and the near side edge. Bottom-right, as in the reference.

usage: assemble.py <heygen_green_render.mp4> [green_hex] [similarity]
"""
import json, os, subprocess, sys, tempfile
import numpy as np
from PIL import Image

CON = ("/Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/"
       "weekender/concepts/9-1-26-oversized-chic-listicle")
VO = "/Users/brooksorradre2/Documents/marketing brain/_engine/mcp/ad-engine/data/vo/job_5de3cd0ca756/voiceover.mp3"
MUSIC = "/Users/brooksorradre2/Documents/marketing brain/brands/velantra/music/DTPA.mp3"
BED = os.path.join(CON, "production/bed.mp4")
CAPS = os.path.join(CON, "production/captions.webm")
OUTDIR = os.path.join(CON, "production/out"); os.makedirs(OUTDIR, exist_ok=True)
# finished ads land in the CONCEPT folder, never products/<product>/video/ (Brooks, re-stated 9/02)
FINAL = os.path.join(CON, "VEL-WEEKENDER-OVERSIZED-01.mp4")

plate = sys.argv[1]
GREEN = sys.argv[2] if len(sys.argv) > 2 else None
SIM = sys.argv[3] if len(sys.argv) > 3 else "0.11"
W, H = 1080, 1920
HEAD_W_FRAC, HEAD_CX_FRAC, BOTTOM_BLEED = 0.20, 0.16, 60
VO_GAIN, MUSIC_GAIN = "1.8", "0.07"   # VO clearly over the bed (Brooks 9/01)


def frame(t, vf=None):
    p = os.path.join(tempfile.mkdtemp(), "f.png")
    cmd = ["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", plate, "-frames:v", "1"]
    if vf:
        cmd += ["-vf", vf]
    subprocess.run(cmd + [p], check=True)
    return Image.open(p).convert("RGBA")


# 1. measure the plate's actual green from the corners of a mid clip frame
if GREEN is None:
    a = np.asarray(frame(10).convert("RGB"))
    corners = np.concatenate([a[:60, :60].reshape(-1, 3), a[:60, -60:].reshape(-1, 3)])
    g = np.median(corners, axis=0).astype(int)
    GREEN = "0x%02X%02X%02X" % tuple(g)
KEY = f"chromakey={GREEN}:{SIM}:0.08"

# 2. measure the head off keyed frames, size on the head, push her into the corner
meas = []
for t in (5, 20, 35, 45):
    al = np.asarray(frame(t, f"format=rgba,{KEY}"))[:, :, 3] > 128
    ys, xs = np.where(al)
    top = int(ys.min()); band = al[top:top + int(0.11 * (int(ys.max()) - top))]
    hx = np.where(band.any(0))[0]
    meas.append((top, int(hx.min()), int(hx.max())))
ph, pw = al.shape
head_top = int(np.mean([m[0] for m in meas])); hl = int(np.mean([m[1] for m in meas])); hr = int(np.mean([m[2] for m in meas]))
head_w = hr - hl; head_cx = (hl + hr) / 2
s = (HEAD_W_FRAC * W) / head_w
sw, sh = int(round(pw * s)), int(round(ph * s))
y = H + BOTTOM_BLEED - sh
x = int(round((W - HEAD_CX_FRAC * W) - head_cx * s))
geo = {"green": GREEN, "similarity": SIM, "plate": [pw, ph], "head_w": head_w, "head_top": head_top,
       "scaled": [sw, sh], "x": x, "y": y, "head_top_in_frame": int(y + head_top * s),
       "cut_bottom_px": y + sh - H, "cut_right_px": x + sw - W}
json.dump(geo, open(os.path.join(CON, "production/pip-geometry.json"), "w"), indent=1)
print("geometry:", geo)

# 3. composite
cf = (f"[1:v]format=rgba,{KEY},scale={sw}:{sh}[pip];"
      f"[0:v][pip]overlay={x}:{y}:format=auto[v0];"
      f"[v0][2:v]overlay=0:0:format=auto[v];"
      f"[3:a]volume={VO_GAIN}[vo];"
      f"[4:a]volume={MUSIC_GAIN},afade=t=out:st=48:d=2.6[m];"
      f"[vo][m]amix=inputs=2:duration=first:dropout_transition=0:normalize=0[a]")
out = os.path.join(OUTDIR, "VEL-WEEKENDER-OVERSIZED-01.mp4")
cmd = ["ffmpeg", "-nostdin", "-y", "-loglevel", "error",
       "-i", BED, "-i", plate, "-c:v", "libvpx-vp9", "-i", CAPS, "-i", VO, "-i", MUSIC,
       "-filter_complex", cf, "-map", "[v]", "-map", "[a]",
       "-c:v", "libx264", "-crf", "19", "-preset", "medium", "-pix_fmt", "yuv420p",
       "-c:a", "aac", "-b:a", "192k", "-shortest", out]
r = subprocess.run(cmd, capture_output=True, text=True)
if r.returncode:
    print("FAIL", r.stderr[-1500:]); sys.exit(1)
d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out],
                   capture_output=True, text=True).stdout.strip()
subprocess.run(["cp", out, FINAL])
print(f"wrote {out} ({float(d):.2f}s, {os.path.getsize(out)/1e6:.1f}MB)\ncopied to {FINAL}")
