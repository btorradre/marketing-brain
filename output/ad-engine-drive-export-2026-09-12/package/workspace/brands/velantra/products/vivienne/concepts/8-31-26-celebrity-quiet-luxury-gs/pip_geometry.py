#!/usr/bin/env python3
"""Work out the PiP transform per creator so the keyed creator is CUT BY THE FRAME EDGE,
the way every shipped house greenscreen ad does it, instead of floating as a full cutout.

The bug in the first build: the HeyGen plate is a wide waist-up shot, so scaling the WHOLE
plate to 32% of frame width makes her head tiny and leaves transparent air on every side.
She reads as a sticker pasted in the corner.

The shipped treatment (GS-BIRKIN-01, BLK-01) is a person standing at the edge of frame:
head roughly 17% of frame width, head top around 74% down the frame, body running off the
bottom edge AND off the near side edge. So we size on the HEAD, not on the plate, and we
push her far enough toward the edge that the frame crops her.
"""
import json, subprocess, tempfile
from pathlib import Path
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
REN  = HERE / "creator-renders"
W, H = 1080, 1920

# measured off the shipped house ads at full resolution (GS-BIRKIN-01, BLK-01)
HEAD_W_FRAC  = 0.200      # head width as a fraction of frame width (whitney 0.16, blk-01 0.23)
BOTTOM_BLEED = 60         # px her body runs BELOW the frame bottom, so the edge crops her
HEAD_CX_FRAC = 0.160      # head centre this far in from the NEAR frame edge

def measure(name, times=(5, 25, 45)):
    src = REN / f"{name}-alpha.webm"
    tmp = Path(tempfile.mkdtemp()); out = []
    for t in times:
        p = tmp / f"{t}.png"
        subprocess.run(["ffmpeg","-v","error","-c:v","libvpx-vp9","-ss",str(t),"-i",str(src),
                        "-frames:v","1",str(p)], check=True)
        a = np.asarray(Image.open(p).convert("RGBA"))[:, :, 3] > 128
        ys, xs = np.where(a)
        top = int(ys.min())
        # the head band: the top 11% of the subject. Its width IS the head width.
        band = a[top:top + int(0.11 * (int(ys.max()) - top))]
        hx = np.where(band.any(0))[0]
        out.append((top, int(hx.min()), int(hx.max())))
    top = int(np.mean([o[0] for o in out]))
    hl  = int(np.mean([o[1] for o in out]))
    hr  = int(np.mean([o[2] for o in out]))
    return {"plate_w": a.shape[1], "plate_h": a.shape[0],
            "head_top": top, "head_l": hl, "head_r": hr, "head_w": hr - hl,
            "head_cx": (hl + hr) // 2}

def solve(m, side):
    """Return (scaled_w, scaled_h, x, y) for the overlay.

    Anchored on two things, in this order:
      - her body runs BOTTOM_BLEED px past the frame bottom, so the bottom edge cuts her;
      - her head centre sits HEAD_CX_FRAC in from the near edge, which pushes her near
        shoulder off the side of the frame.
    Both x and y come out NEGATIVE, and that is the point - a PiP fully inside the frame
    shows its whole silhouette and reads as a sticker.
    """
    s = (HEAD_W_FRAC * W) / m["head_w"]              # size on the HEAD, never on the plate
    sw, sh = int(round(m["plate_w"] * s)), int(round(m["plate_h"] * s))
    y = H + BOTTOM_BLEED - sh
    head_cx = m["head_cx"] * s
    x = int(round((HEAD_CX_FRAC * W if side == "L" else W - HEAD_CX_FRAC * W) - head_cx))
    return sw, sh, x, y

if __name__ == "__main__":
    geo = {}
    for n in ("A-diane", "B-bridget", "C-marguerite"):
        m = measure(n)
        g = {"measured": m, "L": solve(m, "L"), "R": solve(m, "R")}
        geo[n] = g
        swL, shL, xL, yL = g["L"]; swR, shR, xR, yR = g["R"]
        sc = (HEAD_W_FRAC * W) / m["head_w"]
        print(f"{n}: plate {m['plate_w']}x{m['plate_h']} head_w {m['head_w']} head_top {m['head_top']}")
        print(f"   -> scaled {swL}x{shL}   L x={xL} y={yL}   R x={xR} y={yR}")
        print(f"      head {HEAD_W_FRAC*W:.0f}px wide, head top at y={yL + m['head_top']*sc:.0f}, "
              f"cut off bottom {yL+shL-H}px, cut off near side {abs(min(xL,0)) or (xR+swR-W)}px")
    json.dump(geo, open(HERE / "pip-geometry.json", "w"), indent=1)
