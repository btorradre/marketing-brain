#!/usr/bin/env python3
"""Authors anchor_job.json + job.json for VEL-SOFIA-CARRYALL-01.

Vestirsi "Resort 26: Italian Summer" (ad 1518228100026834) replicated 1:1 for
the Velantra Sofia Woven Tote in caramel. Same 9-cut structure, same tropical
resort setting, same diffused-overcast grade, same handheld editorial camera,
same persistent centered text plate.

The ONE thing that is deliberately not 1:1: the bag. Vestirsi's is a slouchy
raffia hobo with knotted handles. The Sofia is structured with a one-piece
leather flap and crossed belts, so every carry is re-blocked to top-handle.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
VAULT = "/Users/brooksorradre2/Documents/marketing brain"
PRODUCT_REF = os.path.join(
    VAULT, "brands/velantra/products/sofia-woven/product-images/straw birkin/caramel 1.png")

# ---------------------------------------------------------------- shared blocks

STYLE = (
    "Editorial fashion film still, full frame cinema camera with a fast prime "
    "lens, shallow depth of field with creamy natural bokeh, handheld. Soft "
    "diffused overcast tropical daylight, no hard sun, no sun flare, no "
    "shadows with hard edges. Warm natural grade: creamy whites, gently "
    "lifted blacks, deep but soft green foliage, fine natural film grain. "
    "Real photography with real photographic skin texture and real woven "
    "fibre texture. NOT a 3D render, not CGI, not an illustration, no plastic "
    "or waxy surfaces, no over sharpening. No on screen text, no caption, no "
    "watermark, no logo anywhere in frame."
)

SETTING = (
    "Location: a lush tropical resort garden. A thatched palm roof pavilion on "
    "dark timber posts sits soft and out of focus behind her, surrounded by "
    "dense glossy green frangipani and palm foliage with scattered pale pink "
    "and white frangipani blooms, along a pale concrete garden walkway."
)

SUBJECT = (
    "Subject: the exact same woman as in the third reference image, same face, "
    "same warm olive skin, same dark brown hair pulled into a low bun with a "
    "single pink and white frangipani flower tucked above one ear. She is a "
    "clearly different individual from the woman in the first reference frame. "
    "She wears the same outfit throughout: oversized tortoiseshell rectangular "
    "sunglasses, small gold hoop earrings, two chunky gold rings, an oversized "
    "crisp white linen button down shirt worn open, untucked, sleeves loose "
    "over her hands, a short cream linen mini skirt underneath, and cream "
    "leather pointed slingback heels."
)

# Verbatim identity block — velantra-straw-tote skill, do not paraphrase.
# The trailing paragraph is this run's correction layer: v1 produced a chunky
# crochet weave, tangled belts and a mini silhouette.
PRODUCT = (
    "She carries a structured hand woven straw tote in warm sandy caramel, "
    "tightly woven straw body with braided cross stitch trim along the edges, "
    "a smooth taupe leather flap folded over the top of the bag from the back: "
    "the flap is ONE single seamless piece of leather, its front lower edge "
    "cut into the silhouette of a wide center panel with 2 squared outer tabs, "
    "the leather fully continuous and unbroken between and above these shapes, "
    "with exactly 2 narrow slots through which the handles pass, two rolled "
    "taupe leather top handles, two taupe leather belt straps crossed on the "
    "front, white contrast stitching on all leather edges, no metal hardware, "
    "no logos. The leather flap, tabs and belt straps exist ONLY on the FRONT "
    "face of the bag, the back face is plain woven straw, no duplicated front "
    "detailing on any other face."
    "\n\n"
    "The bag matches the caramel product reference image exactly in weave, "
    "proportion and leather geometry."
    "\n\n"
    "WEAVE: a fine flat basket weave of many thin even horizontal rows lying "
    "tight against one another. The surface is smooth and dense. There are no "
    "loops, no knots, no crochet stitches, no braiding across the face and no "
    "gaps between rows. It is NOT chunky crochet, NOT knitted or looped yarn, "
    "NOT raffia rope."
    "\n\n"
    "PROPORTION: a large structured day tote about thirteen inches wide, "
    "slightly wider than it is tall, with a flat base and squared sides that "
    "hold their shape, generously sized enough to read as a full day carry "
    "all, never a mini bag."
    "\n\n"
    "BELTS: exactly 2 long taupe leather bands lie flat across the woven front "
    "just below the flap and cross over one another a single time near the "
    "middle of the bag, forming a shallow letter X. The upper band runs from "
    "the left and angles slightly downward to the right. The lower band runs "
    "from the left and angles slightly upward to the right, passing over the "
    "first where they meet. Both bands are the same width, each finishes in a "
    "rounded tip outlined in white contrast stitching, and all 4 rounded tips "
    "are visible. There is no vertical strap, no short hanging tab beneath "
    "them, no buckle, no loop, no keeper and no third band. The bag is closed "
    "and empty throughout."
)

# Flap mechanism block — velantra-straw-tote skill. Mandatory wherever the flap
# is legible. Trimmed of its belt clause only because PRODUCT now specifies the
# belt geometry in more detail; the one-seamless-sheet law is verbatim.
MECHANISM = (
    "Flap construction: the taupe leather flap is ONE single seamless sheet of "
    "leather attached along the top rear edge of the tote and folded all the "
    "way forward over the front, lying completely flat. Its front lower edge is "
    "cut into the shape of a wide center panel and 2 squared outer tabs, but "
    "these are shapes cut into the SAME single sheet, never separate pieces. "
    "The leather is continuous and unbroken between the shapes and across the "
    "entire top of the bag, including between the two handle slots. The only "
    "openings anywhere in the flap are the 2 narrow handle slots. No gap, no "
    "seam, no split, no opening exists anywhere else in the flap, and nothing "
    "behind or inside the bag is ever visible through the flap. The flap never "
    "splits into pieces, never lifts, never stands up, always folded all the "
    "way over. No metal hardware anywhere on the bag."
)

PIN = (
    "The leather flap stays ONE single seamless sheet folded all the way over "
    "and lying flat, with exactly 2 crossed belt straps below it and no metal."
)

VIDEO_PIN = (
    "The leather flap stays ONE single seamless sheet folded all the way over, "
    "lying completely flat the entire clip: no gap, seam or split ever opens "
    "anywhere in it, nothing behind it ever shows through it, and its cut edge "
    "shapes never separate into pieces. The bag never changes shape, never "
    "grows buckles, braids or hardware, and stays the same caramel woven tote "
    "from the first frame to the last."
)

# ---------------------------------------------------------------- per scene

SCENES = [
    dict(
        index=1, target=0.57,
        comp=("Composition: a TIGHT waist level crop. Her HEAD, FACE, HAIR, "
              "NECK and SHOULDERS are all cropped OFF above the top edge of "
              "the frame and are not visible at all. The frame begins at the "
              "middle of her chest and ends at mid thigh, so her torso fills "
              "the whole frame edge to edge. Camera is close, about two feet "
              "away. The caramel woven tote is held at her hip in her right "
              "hand by both rolled top handles gathered together, large in "
              "frame, its front face with the flap and crossed belts turned "
              "toward camera and resting against the white linen shirt. Her "
              "loose sleeve falls half over her hand. Background foliage far "
              "out of focus."),
        mech=True,
        motion=("Handheld, camera drifts slowly a few inches to the left and "
                "settles as she takes one small step. The bag sways gently at "
                "her hip and the loose linen sleeve shifts. Nothing else moves. "
                "No cuts, no zoom, no transition.")),
    dict(
        index=2, target=0.80,
        comp=("Composition: medium wide, camera behind and slightly to her "
              "right as she walks away down the concrete walkway, framed from "
              "head to mid calf. She is turned three quarters away, one arm "
              "swung slightly out so the oversized white shirt catches the air. "
              "The caramel woven tote hangs from her right hand by both top "
              "handles at hip height, its front face angled to camera. Dark "
              "timber posts and the thatched pavilion behind her."),
        mech=False,
        motion=("Handheld, camera walks with her from behind at her pace, "
                "gentle natural bob. Her shirt hem and sleeve move with the "
                "walk, the tote swings a small controlled arc from her hand and "
                "holds its structured shape. No cuts, no zoom, no transition.")),
    dict(
        index=3, target=0.50,
        comp=("Composition: tight chest level crop, head cropped above frame. "
              "She has lifted the caramel woven tote up in front of her chest, "
              "gripping both rolled top handles in one hand just above the "
              "flap, her other hand resting flat against the woven side of the "
              "bag. The open white shirt frames the bag on both sides in a deep "
              "V. The woven straw texture, the leather flap and the crossed "
              "belts read sharp and detailed, background fully soft."),
        mech=True,
        motion=("Handheld, an almost imperceptible push in. Her fingers adjust "
                "their grip on the handles and the bag settles a fraction "
                "lower. The bag holds its exact structured shape. No cuts, no "
                "zoom, no transition.")),
    dict(
        index=4, target=0.60,
        comp=("Composition: medium, from the front, framed from just above her "
              "head to mid thigh. She has half turned back toward camera, chin "
              "slightly up, one hand lifted near her open collar. The caramel "
              "woven tote hangs from her other hand at her hip, front face to "
              "camera. A wall of green frangipani foliage with pale blooms "
              "directly behind her."),
        mech=False,
        motion=("Handheld, camera holds with a soft natural sway. She completes "
                "the half turn toward camera and her hand drops from her "
                "collar. The tote hangs still at her hip. No cuts, no zoom, no "
                "transition.")),
    dict(
        index=5, target=0.63,
        comp=("Composition: wide, full body head to feet, dead centre of frame, "
              "walking toward camera down the pale concrete walkway. Legs and "
              "cream slingback heels visible. The oversized white shirt swings "
              "open as she walks. The caramel woven tote hangs from her right "
              "hand at hip height. Behind her the thatched pavilion roof, dark "
              "timber posts, palms and a strip of pale overcast sky."),
        mech=False,
        motion=("Handheld, camera retreats down the path at her walking pace "
                "keeping her centred, gentle natural bob. She walks steadily "
                "toward camera, shirt swinging open, the tote swinging a small "
                "arc from her hand. No cuts, no zoom, no transition.")),
    dict(
        index=6, target=0.63,
        comp=("Composition: medium wide, same walk toward camera but closer, "
              "framed from above her head to just below the knee. She is "
              "slightly right of centre. The caramel woven tote hangs from her "
              "right hand at hip height, front face angled to camera. Dense "
              "green foliage and the soft thatched roofline behind."),
        mech=False,
        motion=("Handheld, camera retreats at her pace, a touch more shake than "
                "the wider shot. She walks toward camera, the tote swinging "
                "gently and holding its structured shape. No cuts, no zoom, no "
                "transition.")),
    dict(
        index=7, target=0.63,
        comp=("Composition: medium close, framed from above her head to her "
              "waist. She has raised one hand to the temple of her "
              "tortoiseshell sunglasses, chin lifted, mouth relaxed. The "
              "caramel woven tote is held against her waist in her other hand "
              "by both top handles, the flap and crossed belts clearly legible "
              "in the lower third of frame. Green foliage soft behind her."),
        mech=True,
        motion=("Handheld, a slow drift to the right. She lowers her hand from "
                "her sunglasses and turns her head a few degrees. The tote "
                "stays completely still against her waist. No cuts, no zoom, no "
                "transition.")),
    dict(
        index=8, target=1.23,
        comp=("Composition: extreme close macro, the caramel woven tote fills "
              "almost the entire frame, cropped so the rolled taupe leather "
              "handles and the top of the seamless leather flap sit across the "
              "upper third and the woven straw body fills the rest. Her hand "
              "grips the handles at the top of frame, white linen shirt behind "
              "and around the bag, everything else out of focus. Every straw "
              "fibre, the braided cross stitch trim and the white contrast "
              "stitching on the leather read razor sharp."),
        mech=True,
        motion=("Handheld macro, a very slow drift across the woven surface "
                "with a breath of natural shake. Her fingers shift once on the "
                "handles. The weave, flap and stitching stay perfectly stable "
                "and never change pattern. No cuts, no zoom, no transition.")),
    dict(
        index=9, target=1.02,
        comp=("Composition: medium wide from behind, framed from above her head "
              "to her calves, walking away down the concrete walkway. The back "
              "of the oversized white linen shirt fills the centre of frame, "
              "her low bun and the frangipani flower visible at the top. The "
              "caramel woven tote hangs from her right hand at hip height and "
              "reads as a clean caramel shape against the white shirt. Palms, "
              "the thatched roofline and green foliage line the path."),
        mech=False,
        motion=("Handheld, camera follows her from behind at her walking pace "
                "with a gentle natural bob, slowly falling a little further "
                "behind. Her shirt sways with the walk, the tote swings a small "
                "arc from her hand. No cuts, no zoom, no transition.")),
]


def image_prompt(sc):
    parts = [
        "Reference images in order: 1 = framing and lighting reference only, "
        "2 = the caramel handbag, copy it exactly, 3 = the woman, copy her "
        "face and hair exactly. Recreate the framing, lens, lighting and mood "
        "of the first reference frame, but replace its subject with the woman "
        "from image 3 and its bag with the handbag from image 2.",
        sc["comp"], SUBJECT, PRODUCT,
    ]
    if sc["mech"]:
        parts.append(MECHANISM)
    else:
        parts.append(PIN)
    parts += [SETTING, STYLE]
    return "\n\n".join(parts)


def motion_prompt(sc):
    return "\n\n".join([sc["motion"], VIDEO_PIN])


def build(scenes_json, out_path, only=None, shared=None):
    scan = json.load(open(scenes_json))
    by_index = {s["index"]: s for s in scan["scenes"]}
    out_dir = os.path.dirname(scenes_json)

    scenes = []
    for sc in SCENES:
        if only and sc["index"] not in only:
            continue
        src = by_index[sc["index"]]
        scenes.append({
            "index": sc["index"],
            "reference_frame": src["reference_frame"],
            "reference_clip": src["reference_clip"],
            "target_seconds": sc["target"],
            "gen_seconds": 5,
            "image_prompt": image_prompt(sc),
            "motion_prompt": motion_prompt(sc),
            "mode": "first_frame",
            "generate_audio": False,
            "extra_references": [],
            "bake_text": None,
        })

    job = {
        "concept_id": "VEL-SOFIA-CARRYALL-01",
        "output_dir": out_dir,
        "reference_video": scan["reference"],
        "shared_references": shared if shared is not None else [PRODUCT_REF],
        "aspect_ratio": "9:16",
        "resolution": "720p",
        "image_aspect_ratio": "2:3",
        "image_resolution": "2K",
        "engine": "kling",
        "footer_preset": "none",
        "max_seconds": None,
        "upload_path": "vel-sofia-carryall",
        "overlay_text": None,
        "scenes": scenes,
    }
    json.dump(job, open(out_path, "w"), indent=2)
    longest = max(len(s["image_prompt"]) for s in scenes)
    print(f"{out_path}: {len(scenes)} scenes, longest image_prompt {longest} chars")


if __name__ == "__main__":
    scenes_json = os.path.join(HERE, "scenes.json")
    # v1's scene-5 model was right and its bag was wrong, so her head and torso
    # were cropped out (bag excluded) into refs/model_anchor.png. Every scene,
    # scene 5 included, now regenerates against product ref + that model ref.
    model_ref = os.path.join(HERE, "refs", "model_anchor.png")
    shared = [PRODUCT_REF, model_ref]
    build(scenes_json, os.path.join(HERE, "anchor_job.json"),
          only={5}, shared=shared)
    build(scenes_json, os.path.join(HERE, "job.json"), shared=shared)
