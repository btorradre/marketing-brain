#!/usr/bin/env python3
"""Colette pre-order statics — composite typography onto text-free plates.

All type is overlaid here (never generated) so spelling can't drift:
  Didot.ttc index 0  -> serif headlines
  HelveticaNeue.ttc index 7 (Light) -> tracked caps + subheads
  velantra_logo.png  -> real wordmark, inverted to white at runtime

Per-ratio layout constants are tuned to each plate's clean band (measured on
the generated plates, not assumed).

Outputs final/9x16/*.png and final/4x5/*.png
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = os.path.dirname(os.path.abspath(__file__))
VAULT = "/Users/brooksorradre2/Documents/marketing brain"
PIMG = os.path.join(VAULT, "brands/velantra/products/cashmere-tote/product-images/system-oat-greige")
PLATES = os.path.join(ROOT, "plates")
DIDOT = "/System/Library/Fonts/Supplemental/Didot.ttc"
HELV = "/System/Library/Fonts/HelveticaNeue.ttc"
WHITE = (255, 255, 255, 255)
ESPRESSO_INK = (62, 50, 39, 255)


def font_didot(px):
    return ImageFont.truetype(DIDOT, px, index=0)


def font_helv(px):
    return ImageFont.truetype(HELV, px, index=7)


def wordmark_white(width):
    wm = Image.open(os.path.join(ROOT, "velantra_logo.png")).convert("RGBA")
    r, g, b, a = wm.split()
    inv = ImageOps.invert(Image.merge("RGB", (r, g, b)))
    wm = Image.merge("RGBA", (*inv.split(), a))
    h = max(1, int(wm.height * width / wm.width))
    return wm.resize((width, h), Image.LANCZOS)


def wordmark_tinted(width, color):
    wm = Image.open(os.path.join(ROOT, "velantra_logo.png")).convert("RGBA")
    solid = Image.new("RGBA", wm.size, color)
    solid.putalpha(wm.split()[3])
    h = max(1, int(wm.height * width / wm.width))
    return solid.resize((width, h), Image.LANCZOS)


def draw_tracked(draw, text, cx, y, font, tracking, fill=WHITE):
    widths = [draw.textlength(c, font=font) for c in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = cx - total / 2
    for c, w in zip(text, widths):
        draw.text((x, y), c, font=font, fill=fill)
        x += w + tracking


def draw_center(draw, text, cx, y, font, fill=WHITE):
    w = draw.textlength(text, font=font)
    draw.text((cx - w / 2, y), text, font=font, fill=fill)


def paste_wordmark(img, width, cy_frac):
    wm = wordmark_white(width)
    img.alpha_composite(wm, (int((img.width - wm.width) / 2),
                             int(img.height * cy_frac - wm.height / 2)))


def load_plate(name):
    return Image.open(os.path.join(PLATES, name)).convert("RGBA")


# ---------------------------------------------------------------- concepts
def ad_a(W, H, d, img, tall):
    f_head = font_helv(int(W * 0.050))
    f_sub = font_helv(int(W * 0.030))
    hy = 0.235 if tall else 0.150
    sy = 0.290 if tall else 0.207
    draw_tracked(d, "NOW ON PRE-ORDER", W / 2, H * hy, f_head, int(W * 0.028))
    draw_center(d, "Our Most Anticipated Fall Essential", W / 2, H * sy, f_sub)
    paste_wordmark(img, int(W * 0.24), 0.945)


def ad_b(W, H, d, img, tall):
    wm = wordmark_white(int(W * 0.42))
    img.alpha_composite(wm, (int((W - wm.width) / 2), int(H * 0.295 - wm.height / 2)))
    f_sub = font_helv(int(W * 0.028))
    draw_center(d, "The first bag of fall. Now on pre-order.", W / 2, H * 0.335, f_sub)


def ad_c(W, H, d, img, tall):
    if tall:
        f_head, f_sub = font_helv(int(W * 0.042)), font_helv(int(W * 0.026))
        hy, ly, gap = 0.120, 0.171, 0.028
    else:
        f_head, f_sub = font_helv(int(W * 0.036)), font_helv(int(W * 0.022))
        hy, ly, gap = 0.042, 0.086, 0.026
    draw_tracked(d, "FEELS LIKE A COAT", W / 2, H * hy, f_head, int(W * 0.026))
    lines = ["The Colette's brushed wool has a cashmere-soft hand,",
             "in a tote that holds its shape on its own.",
             "Now on pre-order, $40 off until it ships."]
    y = H * ly
    for ln in lines:
        draw_center(d, ln, W / 2, y, f_sub)
        y += H * gap
    if tall:
        paste_wordmark(img, int(W * 0.15), 0.958)


def ad_e(W, H, d, img, tall):
    f_head = font_helv(int(W * 0.030))
    f_sub = font_helv(int(W * 0.026))
    hy = 0.135 if tall else 0.098
    l1 = 0.187 if tall else 0.150
    l2 = 0.217 if tall else 0.182
    draw_tracked(d, "THE EVERYTHING BAG OF FALL", W / 2, H * hy, f_head, int(W * 0.012))
    draw_center(d, "Holds your whole day and keeps its shape.", W / 2, H * l1, f_sub)
    draw_center(d, "Now on pre-order, $40 off until it ships.", W / 2, H * l2, f_sub)
    paste_wordmark(img, int(W * 0.24), 0.945 if tall else 0.962)


def ad_f(W, H, d, img, tall):
    f_head = font_didot(int(W * 0.066))
    f_sub = font_helv(int(W * 0.028))
    hy = 0.145 if tall else 0.118
    sy = 0.208 if tall else 0.178
    draw_center(d, "The First Bag of Fall", W / 2, H * hy, f_head)
    draw_center(d, "Pre-order now. Ships early October.", W / 2, H * sy, f_sub)
    if tall:
        paste_wordmark(img, int(W * 0.16), 0.958)
    else:
        paste_wordmark(img, int(W * 0.13), 0.238)


def build_simple(slug, plate_name, fn, out_dir):
    img = load_plate(plate_name)
    W, H = img.size
    d = ImageDraw.Draw(img)
    fn(W, H, d, img, tall=(H / W > 1.4))
    out = os.path.join(ROOT, "final", out_dir, f"{slug}.png")
    img.convert("RGB").save(out, quality=95)
    print("wrote", out)


# ---------------------------------------------------------------- concept D (split)
def build_d(canvas_wh, out_dir):
    CW, CH = canvas_wh
    tall = CH / CW > 1.4
    panel_h = int(CH * 0.615)
    plate = load_plate("d-life-45.png")

    scale = max(CW / plate.width, panel_h / plate.height)
    nw, nh = int(plate.width * scale), int(plate.height * scale)
    p = plate.resize((nw, nh), Image.LANCZOS)
    ox = (nw - CW) // 2
    oy = int((nh - panel_h) * (0.35 if tall else 0.60))
    panel = p.crop((ox, oy, ox + CW, oy + panel_h))

    car = Image.open(os.path.join(PIMG, "colette-v3-caramel-front.png")).convert("RGB")
    esp = Image.open(os.path.join(PIMG, "colette-v3-espresso-front.png")).convert("RGB")
    band_rgb = car.getpixel((20, 20))

    img = Image.new("RGBA", (CW, CH), (*band_rgb, 255))
    img.paste(panel, (0, 0))
    d = ImageDraw.Draw(img)

    f_head = font_helv(int(CW * 0.043))
    f_small = font_helv(int(CW * 0.023))
    tx = int(CW * 0.080)
    ty = int(panel_h * (0.80 if tall else 0.075))
    d.text((tx, ty), "ONE BAG,", font=f_head, fill=WHITE)
    d.text((tx, ty + int(CW * 0.054)), "MONDAY TO SUNDAY.", font=f_head, fill=WHITE)
    lab = "The Colette Wool Tote"
    lw = d.textlength(lab, font=f_small)
    if tall:
        d.text((CW - int(CW * 0.080) - lw, ty + int(CW * 0.060)), lab,
               font=f_small, fill=WHITE)
    else:
        d.text((tx, ty + int(CW * 0.115)), lab, font=f_small, fill=WHITE)

    wmk = wordmark_tinted(int(CW * 0.14), ESPRESSO_INK)
    img.alpha_composite(wmk, (int((CW - wmk.width) / 2),
                              int(CH * 0.636 - wmk.height / 2)))

    slot_h = int(CH * 0.27)
    slot_y = int(CH * 0.650)
    for src, cxf in ((car, 0.28), (esp, 0.72)):
        s = src.copy()
        sc = slot_h / s.height
        s = s.resize((int(s.width * sc), slot_h), Image.LANCZOS)
        img.paste(s, (int(CW * cxf - s.width / 2), slot_y))
    f_lab = font_helv(int(CW * 0.024))
    for cxf, label in ((0.28, "Caramel"), (0.72, "Espresso")):
        lw = d.textlength(label, font=f_lab)
        d.text((CW * cxf - lw / 2, CH * 0.940), label, font=f_lab, fill=ESPRESSO_INK)

    out = os.path.join(ROOT, "final", out_dir, "d-one-bag.png")
    img.convert("RGB").save(out, quality=95)
    print("wrote", out)


def main():
    for outdir in ("final/9x16", "final/4x5"):
        os.makedirs(os.path.join(ROOT, outdir), exist_ok=True)
    plan = [
        ("a-preorder-open", "a-duo-916.png", ad_a, "9x16"),
        ("a-preorder-open", "a-duo-45.png", ad_a, "4x5"),
        ("b-manifesto", "b-model-916.png", ad_b, "9x16"),
        ("b-manifesto", "b-model-45.png", ad_b, "4x5"),
        ("c-feels-like-a-coat", "c-dark-916.png", ad_c, "9x16"),
        ("c-feels-like-a-coat", "c-dark-45.png", ad_c, "4x5"),
        ("e-everything-bag", "e-inside-916.png", ad_e, "9x16"),
        ("e-everything-bag", "e-inside-45.png", ad_e, "4x5"),
        ("f-first-bag-of-fall", "f-flat-916.png", ad_f, "9x16"),
        ("f-first-bag-of-fall", "f-flat-45.png", ad_f, "4x5"),
    ]
    for slug, plate, fn, outdir in plan:
        if os.path.exists(os.path.join(PLATES, plate)):
            build_simple(slug, plate, fn, outdir)
        else:
            print("MISSING plate:", plate)
    if os.path.exists(os.path.join(PLATES, "d-life-45.png")):
        build_d((1152, 2048), "9x16")
        build_d((1280, 1600), "4x5")
    else:
        print("MISSING plate: d-life-45.png")


if __name__ == "__main__":
    main()
