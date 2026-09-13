#!/usr/bin/env python3
"""Build the static split-screen hero assets for the Motilli problem->product GIF.

Outputs:
  xray_left.png   640x658  (static left panel)
  overlay.png    1280x658  (transparent: red arrow + Motilli bottle in red circle + seam)
  preview.png    1280x658  (full static composite, for QA only)
"""
import sys, math
from PIL import Image, ImageDraw, ImageFilter

W, H = 1280, 658
PW = W // 2          # panel width 640
RED = (214, 40, 24, 255)

def cover_crop(img, tw, th):
    img = img.convert("RGB")
    sw, sh = img.size
    scale = max(tw / sw, th / sh)
    nw, nh = int(math.ceil(sw * scale)), int(math.ceil(sh * scale))
    img = img.resize((nw, nh), Image.LANCZOS)
    left = (nw - tw) // 2
    top = (nh - th) // 2
    return img.crop((left, top, left + tw, th + top))

def circle_crop(img, d):
    img = cover_crop(img, d, d)
    mask = Image.new("L", (d, d), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, d, d), fill=255)
    out = Image.new("RGBA", (d, d), (0, 0, 0, 0))
    out.paste(img, (0, 0), mask)
    return out

def bezier(p0, p1, p2, n=80):
    pts = []
    for i in range(n + 1):
        t = i / n
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]
        pts.append((x, y))
    return pts

def draw_arrow(draw, p0, p1, p2, width, color):
    pts = bezier(p0, p1, p2)
    # thick rounded shaft
    for i in range(len(pts) - 1):
        draw.line([pts[i], pts[i + 1]], fill=color, width=width)
    for (x, y) in pts[::6]:
        r = width / 2
        draw.ellipse((x - r, y - r, x + r, y + r), fill=color)
    # arrowhead at p2, oriented along last segment
    ax, ay = pts[-1]
    bx, by = pts[-8]
    ang = math.atan2(ay - by, ax - bx)
    hl = width * 2.1   # head length
    hw = width * 1.5   # half head width
    tip = (ax + math.cos(ang) * hl * 0.55, ay + math.sin(ang) * hl * 0.55)
    base = (ax - math.cos(ang) * hl * 0.45, ay - math.sin(ang) * hl * 0.45)
    left = (base[0] + math.cos(ang + math.pi / 2) * hw, base[1] + math.sin(ang + math.pi / 2) * hw)
    right = (base[0] + math.cos(ang - math.pi / 2) * hw, base[1] + math.sin(ang - math.pi / 2) * hw)
    draw.polygon([tip, left, right], fill=color)

def main(xray_path, woman_path, product_path):
    # ---- left panel ----
    xray = cover_crop(Image.open(xray_path), PW, H)
    xray.save("xray_left.png")

    # ---- full static preview ----
    woman = cover_crop(Image.open(woman_path), PW, H)
    base = Image.new("RGB", (W, H))
    base.paste(xray, (0, 0))
    base.paste(woman, (PW, 0))

    # ---- transparent overlay ----
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)

    # seam divider
    d.rectangle((PW - 2, 0, PW + 1, H), fill=(255, 255, 255, 230))

    # red curved arrow: from right side of X-ray sweeping down-right to product
    p0 = (470, 300)
    p1 = (720, 360)
    p2 = (980, 500)
    draw_arrow(d, p0, p1, p2, width=30, color=RED)

    # product bottle in red-ringed circle, bottom-right
    diam = 220
    cx, cy = W - diam // 2 - 26, H - diam // 2 - 26   # circle box top-left
    box = (cx - diam // 2, cy - diam // 2)
    prod = circle_crop(Image.open(product_path), diam)
    # white backing + red ring
    ring = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    rd = ImageDraw.Draw(ring)
    rd.ellipse((box[0] - 8, box[1] - 8, box[0] + diam + 8, box[1] + diam + 8), fill=(255, 255, 255, 255))
    ov.alpha_composite(ring)
    ov.paste(prod, box, prod)
    rd2 = ImageDraw.Draw(ov)
    rd2.ellipse((box[0] - 8, box[1] - 8, box[0] + diam + 8, box[1] + diam + 8), outline=RED, width=9)

    ov.save("overlay.png")

    prev = base.convert("RGBA")
    prev.alpha_composite(ov)
    prev.convert("RGB").save("preview.png", quality=92)
    print("OK panels=%s overlay=%s" % (base.size, ov.size))

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
