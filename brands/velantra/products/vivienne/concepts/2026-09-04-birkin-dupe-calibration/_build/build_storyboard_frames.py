#!/usr/bin/env python3
"""Build review-only storyboard composites from generated plates and Anna.

These stills preview the intended 9:16 app composition. They do not render or
animate video. The final editor must rebuild text and presenter placement from
the board after the keyframes are approved.
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
GEN = ROOT / "visuals" / "generated"
OUT = ROOT / "visuals" / "storyboard"
ANNA = ROOT / "visuals" / "presenter" / "anna-keyed.png"
SIZE = (1080, 1920)

FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_REG = "/System/Library/Fonts/Supplemental/Arial.ttf"

BEATS = [
    ("01-hook", "vivienne-detail.png", "BIRKIN-INSPIRED", "Love that Birkin-inspired shape?"),
    ("02-desire", "vivienne-detail.png", "WANTED THIS SHAPE", "I've wanted a bag like this for the longest time"),
    ("03-frustration", "vivienne-detail.png", "TIRED OF THE WAITLIST", "paying designer prices for quality that didn't match"),
    ("04-reveal", "vivienne-detail.png", "THE VIVIENNE", "Velantra gave me early access to the Vivienne"),
    ("05-details", "vivienne-detail.png", "BRAIDED TRIM  ·  GOLD-TONE CLOSURE", "that relaxed, slouchy shape, with no logo across the front"),
    ("06-proof", "vivienne-daily-driver.png", "MY DAILY DRIVER", "I've been using it as my daily driver for the past few weeks"),
    ("07-preorder", "vivienne-detail.png", "PRE-ORDER", "expected to ship in October"),
    ("08-cta", "vivienne-detail.png", "LINK BELOW", "I've left the link below"),
]


def crop_fill(im: Image.Image, size: tuple[int, int]) -> Image.Image:
    src = im.convert("RGB")
    scale = max(size[0] / src.width, size[1] / src.height)
    resized = src.resize((round(src.width * scale), round(src.height * scale)), Image.Resampling.LANCZOS)
    left = (resized.width - size[0]) // 2
    top = (resized.height - size[1]) // 2
    return resized.crop((left, top, left + size[0], top + size[1]))


def fit_text(draw: ImageDraw.ImageDraw, text: str, max_width: int, start: int, minimum: int = 34):
    size = start
    while size > minimum:
        font = ImageFont.truetype(FONT_BOLD, size)
        if draw.textbbox((0, 0), text, font=font)[2] <= max_width:
            return font
        size -= 2
    return ImageFont.truetype(FONT_BOLD, minimum)


def rounded_label(canvas: Image.Image, xy: tuple[int, int, int, int], fill=(248, 242, 229, 235), radius=24):
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).rounded_rectangle(xy, radius=radius, fill=fill)
    canvas.alpha_composite(layer)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    anna = Image.open(ANNA).convert("RGBA")
    bbox = anna.getchannel("A").getbbox()
    if bbox:
        anna = anna.crop(bbox)
    anna.thumbnail((450, 900), Image.Resampling.LANCZOS)

    for slug, plate_name, headline, caption in BEATS:
        # Mirror the reference's stable collage: a persistent full product hero
        # plus one lower-left proof tile and Anna at lower right. Only the proof
        # tile changes when the spoken line moves from detail to daily use.
        base = crop_fill(Image.open(GEN / "vivienne-home-hero.png"), SIZE).convert("RGBA")
        tile = crop_fill(Image.open(GEN / plate_name), (610, 720)).convert("RGBA")
        tile_frame = Image.new("RGBA", (626, 736), (246, 238, 224, 255))
        tile_frame.alpha_composite(tile, (8, 8))
        base.alpha_composite(tile_frame, (-8, 1184))
        # A restrained shadow keeps the keyed edge legible without turning the
        # presenter into a sticker.
        shadow = Image.new("RGBA", base.size, (0, 0, 0, 0))
        alpha = anna.getchannel("A").filter(ImageFilter.GaussianBlur(14))
        shadow_piece = Image.new("RGBA", anna.size, (0, 0, 0, 105))
        shadow_piece.putalpha(alpha.point(lambda p: p * 95 // 255))
        pos = (SIZE[0] - anna.width + 56, SIZE[1] - anna.height + 52)
        shadow.alpha_composite(shadow_piece, (pos[0] - 10, pos[1] + 14))
        base.alpha_composite(shadow)
        base.alpha_composite(anna, pos)

        draw = ImageDraw.Draw(base)
        rounded_label(base, (58, 92, 1022, 222))
        draw = ImageDraw.Draw(base)
        headline_font = fit_text(draw, headline, 880, 66, 38)
        hb = draw.textbbox((0, 0), headline, font=headline_font)
        hx = (SIZE[0] - (hb[2] - hb[0])) // 2
        draw.text((hx, 121), headline, font=headline_font, fill=(38, 28, 23, 255))

        cap_font = ImageFont.truetype(FONT_BOLD, 43)
        max_w = 610
        words = caption.split()
        lines, line = [], ""
        for word in words:
            trial = f"{line} {word}".strip()
            if draw.textbbox((0, 0), trial, font=cap_font)[2] <= max_w:
                line = trial
            else:
                lines.append(line)
                line = word
        if line:
            lines.append(line)
        lines = lines[:3]
        box_h = 38 + 58 * len(lines)
        rounded_label(base, (56, 438 - box_h, 806, 438), fill=(20, 16, 14, 220), radius=20)
        draw = ImageDraw.Draw(base)
        y = 438 - box_h + 19
        for line in lines:
            draw.text((82, y), line, font=cap_font, fill=(255, 255, 255, 255))
            y += 58

        if slug == "08-cta":
            disclosure = "PRE-ORDER  ·  SHIPPING EXPECTED OCTOBER"
            rounded_label(base, (56, 462, 806, 534), fill=(248, 242, 229, 235), radius=18)
            draw = ImageDraw.Draw(base)
            disclosure_font = fit_text(draw, disclosure, 690, 32, 26)
            db = draw.textbbox((0, 0), disclosure, font=disclosure_font)
            dx = 56 + (750 - (db[2] - db[0])) // 2
            draw.text((dx, 481), disclosure, font=disclosure_font, fill=(38, 28, 23, 255))

        base.convert("RGB").save(OUT / f"{slug}.jpg", quality=94, subsampling=0)


if __name__ == "__main__":
    main()
