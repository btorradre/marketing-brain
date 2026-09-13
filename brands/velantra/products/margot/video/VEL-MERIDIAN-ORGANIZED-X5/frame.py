#!/usr/bin/env python3
"""Auto-frame Meridian product stills into 9:16 plates with zoom headroom."""
import os, sys
from PIL import Image, ImageChops

W, H = 1080, 1920
HEADROOM = 1.18          # render bigger than final so zoompan has room
PW, PH = int(W * HEADROOM), int(H * HEADROOM)

# how much of the plate height the subject should occupy, per shot type
FILL = {
    "hero":       0.42,
    "straighton": 0.42,
    "interior":   0.50,
    "onmodel":    0.99,
}
# vertical placement of the subject centre inside the plate (0=top, 1=bottom)
ANCHOR = {
    "hero":       0.52,
    "straighton": 0.52,
    "interior":   0.50,
    "onmodel":    0.50,
}


def content_bbox(im, tol=18):
    """bbox of everything that differs from the flat backdrop colour."""
    rgb = im.convert("RGB")
    w, h = rgb.size
    corners = [rgb.getpixel((2, 2)), rgb.getpixel((w - 3, 2)),
               rgb.getpixel((2, h - 3)), rgb.getpixel((w - 3, h - 3))]
    bg = tuple(sum(c[i] for c in corners) // 4 for i in range(3))
    diff = ImageChops.difference(rgb, Image.new("RGB", rgb.size, bg))
    mask = diff.convert("L").point(lambda p: 255 if p > tol else 0)
    return mask.getbbox(), bg


def plate(src_path, shot, out_path):
    im = Image.open(src_path).convert("RGB")
    bbox, bg = content_bbox(im)
    if bbox is None:
        bbox = (0, 0, im.width, im.height)
    bx0, by0, bx1, by1 = bbox
    bw, bh = bx1 - bx0, by1 - by0
    cx, cy = (bx0 + bx1) / 2, (by0 + by1) / 2

    fill = FILL[shot]
    # crop height so the subject fills `fill` of it; also cap subject width at 0.82
    crop_h = bh / fill
    crop_w = crop_h * (PW / PH)
    if bw / crop_w > 0.82:
        crop_w = bw / 0.82
        crop_h = crop_w * (PH / PW)

    # the crop must live entirely inside the source, so cap it at the largest
    # 9:16 window the source can hold, then clamp its position into bounds
    max_w = min(im.width, im.height * PW / PH)
    max_h = max_w * PH / PW
    if crop_w > max_w:
        crop_w, crop_h = max_w, max_h

    anchor = ANCHOR[shot]
    x0 = cx - crop_w / 2
    y0 = cy - crop_h * anchor
    x0 = max(0, min(x0, im.width - crop_w))
    y0 = max(0, min(y0, im.height - crop_h))

    crop = im.crop((round(x0), round(y0), round(x0 + crop_w), round(y0 + crop_h)))
    crop = crop.resize((PW, PH), Image.LANCZOS)
    crop.save(out_path, quality=95)
    return out_path


if __name__ == "__main__":
    color = sys.argv[1]
    outdir = sys.argv[2]
    os.makedirs(outdir, exist_ok=True)
    for shot in ("hero", "interior", "onmodel", "straighton"):
        src = f"src/margot-{color}-{shot}.jpg"
        plate(src, shot, f"{outdir}/{color}-{shot}.jpg")
    print("plated", color)
