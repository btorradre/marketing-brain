#!/usr/bin/env python3
"""
Sofia oat-greige system -- v5 job builder (2026-08-05, video-truth correction).

WHY v5: Brooks compared the live v4 gallery against the running Straw Tote video ad and
rejected it -- "the bag looks entirely different." The v4 blocks described a bag the REF
does not show (soft slouch, coarse chunky weave, tonal stitching, greige-taupe caramel),
and since GPT Image 2 follows the PROMPT when prompt and reference disagree, the text
redesigned the bag. Patch-sample proof: REF flap RGB(201,134,87) warm caramel vs live
v4 hero flap RGB(174,144,122) greige.

v5 TRUTH (REF-product.jpg + the ad video, which agree):
  - leather: warm caramel tan (golden toffee), NOT greige taupe
  - stitching: crisp pale cream CONTRAST stitching on every leather edge
  - weave: fine, dense, tightly packed horizontal rows, NOT coarse chunky rope
  - body: holds its shape, stands upright, subtle woven wings only
  - flap cut + belt arrangement: unchanged from v4 blocks (those were correct)

Chain (mirrors v4):
  _REF-product.jpg
     -> _v5/_canon-{a,b,c}.png      caramel HERO restage, 3 variants, pick numerically
     -> _v5/_m5-{interior,onmodel}-v{1,2}.png   masters [REF + composition ref]
     -> _v5/sofia-<color>-hero.png  [canon + REF, colour by text only]
     -> _v5/sofia-<color>-<shot>.png [shot master + colour hero + REF]
No straights (Brooks 8/05: three product images per product).
"""
import json, sys
from pathlib import Path

P = Path("/Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/sofia-woven")
OUT = P / "product-images/system-oat-greige"
REF = str(OUT / "_REF-product.jpg")
CANON = str(OUT / "_v5/_canon-pick.png")  # symlink/copy of the chosen canon variant

COMP = {
    "interior": str(P / "product-images/straw birkin/straw birkin opened.png"),
    "onmodel":  str(P / "statics/straw birkin/cream.webp"),
}

BODY = (
    "BODY SHAPE, CRITICAL: the woven body holds its shape and stands upright on a flat base, "
    "gently structured hand-woven basketry exactly as in the product reference. The side walls "
    "rise into small soft woven wing points at the top outer corners, subtle, exactly as in the "
    "reference, never exaggerated. No heavy slouching, no collapsing, and also no hard moulded "
    "corners or creased leather-goods panels: it reads as neat dense basketry with the slight "
    "organic irregularity of handwork."
)

WEAVE = (
    "WEAVE, CRITICAL: fine, dense and tightly packed thin horizontal rows of twisted straw cord, "
    "neat and uniform, exactly as in the product reference. NEVER coarse, NEVER chunky thick rope, "
    "never a loose open basket weave. A braided lacing with a visible criss-cross X pattern runs "
    "vertically up each side edge of the bag, exactly as in the product reference."
)

FLAP = (
    "FLAP, CRITICAL, copy it EXACTLY from the product reference: one deep leather band lies flat "
    "across the entire top of the bag. The two rolled handles pass through two narrow slots cut "
    "into this band. The band's lower edge is cut, all in the same single sheet, into: a squared "
    "tab stepping down at the far left, a wide flat-bottomed centre panel between the two handle "
    "slots, and a squared tab stepping down at the far right, with square crisp corners "
    "throughout. These are silhouettes cut into ONE sheet, never separate applied patches and "
    "never rounded pillows. The flap lies completely flat against the woven front. No extra "
    "leather pieces, strips, loops or fragments exist anywhere on the bag beyond the flap, the "
    "two handles, the two belt straps and the small centre tab."
)

BELTS = (
    "BELT STRAPS, CRITICAL, copy the arrangement EXACTLY from the product reference: one narrow "
    "leather strap runs nearly horizontally across the front of the bag just below the flap, its "
    "left end angling slightly downward. A second narrow strap crosses over it diagonally, running "
    "from the upper right down toward the lower left, ending in a rounded tip. A short pointed "
    "leather tab hangs down from the centre of the flap behind the straps. This is NOT a symmetric "
    "X and NOT a V. Keep the straps narrow, flat and lying against the weave."
)

STITCH = (
    "STITCHING, CRITICAL: crisp pale cream contrast stitching runs along every leather edge, the "
    "flap band, its tabs, the handles and both belt straps, clearly visible against the leather, "
    "exactly as in the product reference. Never tonal invisible stitching."
)

NOMETAL = "No metal hardware anywhere, no buckles, no logos, no lettering."

REAL = (
    "A real photograph on a medium format camera with a 100mm lens, never a 3D render or CGI: real "
    "straw fibre with individual strands and slight irregularity, real leather grain with soft "
    "natural sheen and micro creasing, natural depth of field falloff, subtle photographic grain. "
    "No plastic smoothness, no glossy render highlights, no synthetic perfection."
)

STAGE = (
    "Setting: one continuous soft warm pale oat-greige seamless studio sweep, hex #E7E3DB, filling "
    "the whole frame. No horizon line, no visible wall-to-floor edge, no corner. Soft even diffused "
    "studio light from the front left. Exactly ONE soft contact shadow directly beneath the bag. No "
    "person, no hand, no props, no pedestal, no table, no surface line. Square 1:1 frame, bag "
    "centred, occupying about 72 percent of the frame height."
)

SHAPE = " ".join([BODY, WEAVE, FLAP, BELTS, STITCH, NOMETAL])

CARAMEL = (
    "The leather colour stays EXACTLY the warm caramel tan of the product reference, a golden "
    "toffee brown of medium saturation, never grey, never taupe, never washed out, never darker."
)

CANON_PROMPT = (
    "Studio e-commerce product photograph of the bag from the reference image. The reference image "
    "is the real product and the ONLY authority on the bag: reproduce this exact bag with every "
    "detail unchanged. Remove the woman, her hand and the white fabric backdrop completely. The "
    "bag stands closed on its base, turned to a gentle three-quarter angle with the front face "
    "dominant and one side just visible. " + STAGE + " " + SHAPE + " " + CARAMEL + " " + REAL
)

AUTHORITY = (
    "The FIRST reference image is the real product and is the ONLY authority on the bag: its "
    "proportions, fine dense weave, braided X-laced side edges, deep flap band with its cut tabs "
    "and handle slots, belt strap arrangement, handles, warm caramel leather and cream contrast "
    "stitching must all be reproduced exactly from image one. "
)

MASTERS = {
    "interior": (
        "Overhead studio photograph shot from directly above, looking down into the open bag. " +
        AUTHORITY +
        "The SECOND reference image supplies ONLY the overhead composition and the items packed "
        "inside: a dark grey laptop, a clear water bottle and a warm tan brown zip-around wallet, "
        "which keep their own colours. The bag is open: the leather flap band is folded all the way "
        "back over the rear and lies flat there, the woven mouth open in front of it, the walls "
        "standing neatly. Do not take any bag geometry from image two. " + SHAPE + " " + CARAMEL +
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
        "image two. " + SHAPE + " " + CARAMEL +
        " Setting: a plain neutral mid-grey seamless studio backdrop and matching grey floor, soft "
        "even diffused light, one soft shadow behind her. No props, no outdoor elements, no logos. "
        "The bag is the sharpest thing in the frame. Square 1:1 frame, the bag centred in the lower "
        "two thirds and occupying about 45 percent of the frame height. " + REAL
    ),
}

COLORS = [
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
    "angle, crop, bag position and scale, background, lighting, shadow, upright gently structured "
    "silhouette, fine dense weave, braided X-laced side edges, deep flap band with its exact cut, "
    "handle slots and belt strap arrangement. The crisp pale cream contrast stitching stays "
    "clearly visible on every leather edge. The woven straw body keeps its natural undyed straw "
    "colour, only the leather changes. Do not change the flap cut, do not move the straps. "
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


def canon():
    return [{"out": f"_v5/_canon-{v}.png", "refs": [REF], "prompt": CANON_PROMPT}
            for v in ("a", "b", "c")]


def masters():
    return [{"out": f"_v5/_m5-{s}-v{v}.png", "refs": [REF, COMP[s]], "prompt": MASTERS[s]}
            for s in MASTERS for v in (1, 2)]


def heroes():
    return [{"out": f"_v5/sofia-{h}-hero.png", "refs": [CANON, REF],
             "prompt": hero_prompt(desc)}
            for h, desc in COLORS]


def rest(picks):
    jobs = []
    for s in ["interior", "onmodel"]:
        m = str(OUT / f"_v5/_m5-{s}-{picks[s]}.png")
        for h, desc in COLORS:
            jobs.append({"out": f"_v5/sofia-{h}-{s}.png",
                         "refs": [m, str(OUT / f"_v5/sofia-{h}-hero.png"), REF],
                         "prompt": rest_prompt(s, desc)})
    return jobs


if __name__ == "__main__":
    mode, arg = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else None)
    (OUT / "_v5").mkdir(exist_ok=True)
    jobs = {"canon": canon, "masters": masters, "heroes": heroes,
            "rest": lambda: rest(json.loads(arg))}[mode]()
    out = OUT / f"_jobs_v5_{mode}.json"
    out.write_text(json.dumps(jobs, indent=2))
    print(f"{len(jobs)} jobs -> {out.name}")
