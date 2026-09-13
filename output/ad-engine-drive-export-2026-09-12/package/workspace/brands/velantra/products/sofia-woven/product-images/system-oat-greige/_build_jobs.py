#!/usr/bin/env python3
"""
Sofia oat-greige system -- v4 job builder.

REFERENCE LAW (Brooks, 8/05): `_REF-product.jpg` is wired into EVERY generation as the
product-truth reference. Colour is driven by TEXT ONLY (a colour-reference photo leaks its
geometry -- proven on Lady Pink in v3).

Chain:
  _REF-product.jpg
     -> _v4-canon-v3.png  = caramel HERO (3/4)          [restage of REF, already approved]
     -> _v4-canon-v2.png  = caramel STRAIGHT (front-on) [restage of REF, already approved]
     -> _m4-interior / _m4-onmodel masters               [REF + composition ref]
     -> per-colour heroes  [canon-v3 + REF, colour by text]
     -> per-colour rest    [shot master + that colour's hero + REF]
"""
import json, sys
from pathlib import Path

from _v3_blocks import SHAPE, STAGE, REAL

P = Path("/Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/sofia-woven")
OUT = P / "product-images/system-oat-greige"
REF = str(OUT / "_REF-product.jpg")
HERO_CANON = str(OUT / "_v4-canon-v3.png")
STRAIGHT_CANON = str(OUT / "_v4-canon-v2.png")

COMP = {
    "interior": str(P / "product-images/straw birkin/straw birkin opened.png"),
    "onmodel":  str(P / "statics/straw birkin/cream.webp"),
}

AUTHORITY = (
    "The FIRST reference image is the real product and is the ONLY authority on the bag: its soft "
    "slouched silhouette, woven wings at the top corners, proportions, coarse weave, braided X-laced "
    "side edges, deep flap band with its cut tabs and handle slots, belt strap arrangement and "
    "handles must all be reproduced exactly from image one. "
)

MASTERS = {
    "interior": (
        "Overhead studio photograph shot from directly above, looking down into the open bag. " +
        AUTHORITY +
        "The SECOND reference image supplies ONLY the overhead composition and the items packed "
        "inside: a dark grey laptop, a clear water bottle and a warm tan brown zip-around wallet, "
        "which keep their own colours. The bag is open: the leather flap band is folded all the way "
        "back over the rear and lies flat there, the woven mouth open in front of it, the soft woven "
        "walls slouching gently outward. Do not take any bag geometry from image two. " + SHAPE +
        " Setting: one continuous soft warm pale oat-greige seamless studio surface, hex #E7E3DB, "
        "filling the whole frame, perfectly even, no horizon line, no props beyond the items inside "
        "the bag. Soft even diffused overhead light, one soft shadow hugging the base. Square 1:1 "
        "frame, bag centred, occupying about 82 percent of the frame. " + REAL
    ),
    "onmodel": (
        "Studio fashion photograph of a woman holding the bag from the first reference image. " +
        AUTHORITY +
        "The SECOND reference image supplies ONLY the pose and crop: the woman cropped from just "
        "below the shoulders to mid-calf, standing three quarters to camera, holding the closed bag "
        "by both top handles in one hand so it hangs at hip height, her other arm relaxed. She wears "
        "a soft oatmeal linen shirt and wide cream linen trousers. Do not take any bag geometry from "
        "image two. " + SHAPE +
        " Setting: a plain neutral mid-grey seamless studio backdrop and matching grey floor, soft "
        "even diffused light, one soft shadow behind her. No props, no outdoor elements, no logos. "
        "The bag is the sharpest thing in the frame. Square 1:1 frame, the bag centred in the lower "
        "two thirds and occupying about 45 percent of the frame height. " + REAL
    ),
}

COLORS = [
    ("caramel",          "a muted greige taupe, a soft desaturated warm grey-taupe exactly as on the real product reference, never a saturated orange tan"),
    ("cream",            "a clean warm off-white cream"),
    ("light-chocolate",  "a rich mid chocolate brown"),
    ("sky-blue",         "a vivid azure sky blue"),
    ("lady-pink",        "a bright magenta-leaning fuchsia pink"),
    ("lightning-orange", "a saturated red-leaning coral orange"),
    ("caban-black",      "a deep true black"),
    ("sunny-yellow",     "a warm golden mustard yellow"),
]

KEEP = (
    " Everything else stays identical to the first reference image: the same composition, camera "
    "angle, crop, bag position and scale, background, lighting, shadow, soft slouched silhouette, "
    "woven wings, coarse weave, braided X-laced side edges, deep flap band with its exact cut, "
    "handle slots, belt strap arrangement and subtle tonal stitching. The woven straw body keeps "
    "its natural undyed straw colour, only the leather changes. Do not stiffen the bag, do not "
    "change the flap cut, do not move the straps. "
)

PIN = (
    " HANDLE HEIGHT: the handles keep exactly the same arc and height as in the first reference "
    "image. The overall height of the bag including handles must match it exactly."
)


def hero_prompt(desc):
    return (
        "Take the first reference image and change ONLY the colour of the leather parts of the bag, "
        "the flap band, its tabs, the handles and the belt straps, to " + desc + ". The straw body "
        "stays its natural undyed colour." + KEEP +
        "The SECOND reference image is the real product; use it to keep every construction detail "
        "true. " + SHAPE + PIN + " " + REAL
    )


def rest_prompt(shot, desc):
    extra = ""
    if shot == "interior":
        extra = (
            " Change only the bag's OUTER leather. The dark grey laptop, the clear water bottle, "
            "the warm tan brown zip-around wallet and the interior keep their own colours."
        )
    if shot == "onmodel":
        extra = (
            " Keep the model, her pose, her hands, her oatmeal linen shirt, her cream linen "
            "trousers and the grey studio exactly as they are. Change only the bag's leather colour."
        )
    return (
        "Take the first reference image and change ONLY the colour of the leather parts of the bag, "
        "the flap band, its tabs, the handles and the belt straps, to " + desc + ". The straw body "
        "stays its natural undyed colour. The SECOND reference image is the same bag in this same "
        "colourway already approved: match its leather colour EXACTLY, same hue, same saturation, "
        "same lightness. Take nothing else from image two. The THIRD reference image is the real "
        "product; use it to keep every construction detail true." + KEEP + extra + " " + SHAPE +
        " " + REAL
    )


def masters():
    return [{"out": f"_m4-{s}-v{v}.png", "refs": [REF, COMP[s]], "prompt": MASTERS[s]}
            for s in MASTERS for v in (1, 2)]


def heroes():
    return [{"out": f"sofia-{h}-hero.png", "refs": [HERO_CANON, REF],
             "prompt": hero_prompt(desc)}
            for h, desc in COLORS if h != "caramel"]


def rest(picks):
    jobs = []
    for s in ["straight", "interior", "onmodel"]:
        m = STRAIGHT_CANON if s == "straight" else str(OUT / f"_m4-{s}-{picks[s]}.png")
        for h, desc in COLORS:
            if s == "straight" and h == "caramel":
                continue  # _v4-canon-v2 IS the caramel straight
            jobs.append({"out": f"sofia-{h}-{s}.png",
                         "refs": [m, str(OUT / f"sofia-{h}-hero.png"), REF],
                         "prompt": rest_prompt(s, desc)})
    return jobs


if __name__ == "__main__":
    mode, arg = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else None)
    jobs = {"masters": masters, "heroes": heroes,
            "rest": lambda: rest(json.loads(arg))}[mode]()
    out = OUT / f"_jobs_{mode}.json"
    out.write_text(json.dumps(jobs, indent=2))
    print(f"{len(jobs)} jobs -> {out.name}")
