#!/usr/bin/env python3
"""VEL-WEEKENDER-MENSBADGE-01 — men's-angle BLACK Weekender spec-badge statics.

Swipe: the GRAMS(28) "183 XL Duffle Bag" static Brooks sent — an environmental
product hero, cropped-at-the-chin man holding a black duffle over a hardshell
carry-on, tiny letterspaced wordmark top-left, product name under it, and a row of
four white line-icon trust badges across the bottom.

WHAT PORTS: the layout (wordmark / product label / four-badge trust strip over a real
photograph) and the editorial daylight register.
WHAT DOES NOT: their badge copy. "Premium Italian Leather" is an origin claim
(banned outright) and "100K+ Happy Customers" is a number we cannot substantiate.
Every badge here is a claim that is live on velantrafashion.com today, verified
2026-08-11 against the PDP and the site trust bar.

PRODUCT BLOCKS are the validated BLACK set from VEL-WEEKENDER-BLKCARRYON-01
(black_blocks.py, unmodified). Black is ALL smooth black leather, no canvas anywhere,
caramel tan interior — ANTI_CANVAS travels in every prompt regardless of crop.

THE ONE BLOCK THAT IS NOT INHERITED: PHOTOREAL. The carry-on build wanted raw
shot-on-iPhone. This swipe is the opposite register — a real, lit, editorial
photograph. EDITORIAL below replaces it and still carries the no-CGI law.

MEN'S VOC LAWS OBSERVED (research/voc/2026-08-02-mens-travel-bag-voc.md):
  - hand or forearm carry ONLY, never a shoulder carry (the handles cannot reach)
  - no logos anywhere on the bag, and the badge row says so out loud
  - never gender the bag in copy: no "man bag", no "men's bag", no "masculine"
  - the man is CROPPED — no face in any of the three. The swipe crops at the chin;
    a faceless male presence also keeps the set castable across audiences.
"""

from black_blocks import (
    PREAMBLE, IDENTITY, ANTI_DRIFT, ANTI_CANVAS, HARDWARE_LAW, CLOSURE, SCALE, SUITCASE,
)

# ---------------------------------------------------------------- editorial look
# Replaces the carry-on build's iPhone PHOTOREAL block. Still a photograph, still
# anti-CGI (the standing global law: a frame that reads as a 3D model gets regenerated).
EDITORIAL = (
    "CRITICAL RENDERING INSTRUCTION. This is a real photograph taken on a full frame camera "
    "with a fast prime lens, natural available light only. It is NOT a 3D render, NOT CGI, NOT a "
    "product visualisation, NOT Blender or Octane or Unreal or Keyshot, NOT ray traced, NOT a "
    "composite and NOT an illustration. If it looks computer generated it is wrong. Real "
    "photographic behaviour throughout: a shallow but believable depth of field with the "
    "background falling soft while the bag stays sharp, gentle natural falloff of light across "
    "the leather, real optical vignetting at the corners, fine film-like grain, and the very "
    "slight imperfections of a real frame. The black leather is REAL leather: soft matte to "
    "satin, with visible fine pebbled grain, natural creasing at the corners and along the flap "
    "fold, faint handling marks, and broad soft highlights that fall off gradually. It is never "
    "glossy plastic, never rubbery, never a flat featureless black silhouette with no detail in "
    "it. The gold hardware is warm brushed brass catching a soft specular, never a chrome mirror. "
    "There is absolutely NO text, no lettering, no signage, no numbers, no logos, no watermarks "
    "and no graphics anywhere in the picture, on the bag, on the clothing, on any prop or in the "
    "background."
)

# ---------------------------------------------------------------- layout reservation
# The overlay is composited in post (type is never generated — "Weekender" is a known
# text-render failure on every engine we use). The plate has to leave it room.
LAYOUT = (
    "COMPOSITION AND NEGATIVE SPACE, this matters as much as the bag. Vertical portrait frame, "
    "taller than it is wide. The bag is the hero and sits in the MIDDLE BAND of the frame, large, unobstructed "
    "and completely inside the frame with none of it cropped off by any edge. The TOP FIFTH of "
    "the frame is quiet, uncluttered background with no important detail in it, and the top left "
    "corner especially is plain, calm and free of any object. The BOTTOM FIFTH of the frame is "
    "also quiet and reads distinctly DARKER and calmer than the middle of the frame, holding no "
    "part of the bag, no face, no bright highlight and no busy detail, so that small white "
    "graphics could be laid over it later and stay legible. Nothing important touches the outer "
    "edges of the frame."
)

# ---------------------------------------------------------------- the man (locked, faceless)
# Cropped, hands-and-body only. Consistent wardrobe register across all three so the
# set reads as one campaign.
MAN = (
    "THE MAN IN FRAME IS CROPPED AND HAS NO FACE. The frame cuts him off at or below the chin, "
    "so no eyes, no nose, no mouth, no face and no top of the head appear anywhere in the "
    "picture, and no face is reflected in anything. He is a real man in his mid thirties, warm "
    "fair skin with natural texture and visible fine hair on the forearms, short clean "
    "fingernails, a plain brushed steel watch on a steel link bracelet on his left wrist, no "
    "rings, no bracelets, no tattoos, no phone in hand. His clothing is plain, quiet and "
    "completely unbranded: no logos, no motifs, no patterns, no visible labels, no printed "
    "graphics on any garment. He is never carrying the bag on his shoulder, and no strap of any "
    "kind ever runs over his shoulder or across his body."
)

# ---------------------------------------------------------------- carry law
CARRY = (
    "CARRY LAW. This bag is carried by its two short rolled top handles, in the HAND or over the "
    "FOREARM, and in no other way. It never hangs from a shoulder, there is no long shoulder "
    "strap, no crossbody strap, no luggage strap and no strap of any kind attached to the bag "
    "beyond its two short rolled top handles."
)

REFS = {
    "blkfront": "e74f8b67-d9b7-4561-bba5-4a4dc62ae7ba",  # black-01, front, all-leather truth
    "blkthree": "18eb579d-df10-41ee-bec8-8773659dccc4",  # black-02, three-quarter
    "blkscale": "d45550cc-ed16-4973-b476-d06582c5c25c",  # black-04, carried, scale on a person
}

SCENES = [
    dict(
        key="A-onthecase",
        refs=["blkfront", "blkscale"],
        beat=(
            "SHOT. A vertical editorial travel photograph, camera at chest height and very "
            "slightly below the bag, a medium shot. A man stands facing the camera, cropped by "
            "the frame just below his chin at the top and at mid thigh at the bottom, wearing an "
            "open charcoal grey wool overcoat over a plain black fine knit crewneck and dark "
            "charcoal trousers. He holds the black weekend bag in front of him with BOTH HANDS "
            "gripping its two rolled black leather top handles together, one hand on each handle, "
            "the bag hanging at about waist height directly in front of his body and facing the "
            "camera square on, its front and its gold hardware fully visible. The bag has just "
            "been set down onto the top of a plain unbranded pale silver grey hardshell carry on "
            "suitcase that stands upright on the ground in front of him, so the base of the bag "
            "rests across the top of the suitcase and the suitcase carries its weight. "
            "SCALE CHECK for this frame: the bag is as wide as the man's shoulders and clearly "
            "WIDER than the suitcase is deep, overhanging the top of the suitcase at both ends; "
            "its top edge reaches his waist. Render it large in the frame. "
            "SETTING: outdoors on a city street in soft overcast late afternoon daylight, a warm "
            "pale limestone building wall and a dark wrought iron handrail behind him, thrown "
            "well out of focus. No other people, no vehicles, no shop fronts, no signage."
        ),
        extra=[SUITCASE],
    ),
    dict(
        key="B-curbside",
        refs=["blkscale", "blkfront"],
        beat=(
            "SHOT. A vertical editorial travel photograph, camera low, at about hip height, "
            "looking slightly up, a three quarter angle from the man's right side. A man walks "
            "along a city curb, cropped by the frame just below his chin at the top and at the "
            "ankle at the bottom, wearing a plain navy topcoat over a white crew neck tee and "
            "black trousers, mid stride. The black weekend bag hangs from his RIGHT HAND at his "
            "side, both rolled black leather handles gathered together in that one hand, the bag "
            "swinging just clear of his leg and turned so the camera sees its front three quarter "
            "face with the gold hardware catching the light. His other arm swings free and empty. "
            "SCALE CHECK for this frame: the bag is enormous in his hand, its top edge level with "
            "his hip and its base falling to just above his knee, and it is as wide as his torso. "
            "Render it large in the frame. "
            "SETTING: a quiet city street in soft directional early evening daylight, dark damp "
            "asphalt, a stone curb, and the dark flank of a parked car thrown completely out of "
            "focus behind him. No other people, no signage, no license plates, no visible car "
            "badges."
        ),
        extra=[],
    ),
    dict(
        key="C-overheadbin",
        refs=["blkfront", "blkthree"],
        beat=(
            "SHOT. A vertical editorial travel photograph taken inside an aircraft cabin, camera "
            "at shoulder height looking slightly up toward an open overhead bin. A man lifts the "
            "black weekend bag up into the open overhead bin, seen from behind and to his side: "
            "the frame crops him at the shoulders so only his shoulder, his upper arms and his "
            "forearms are in it, no head and no face at all. He wears a plain white oxford shirt "
            "with the sleeves rolled twice to the forearm and a plain brushed steel watch on his "
            "left wrist. Both of his hands are on the bag, one hand under its base taking the "
            "weight and one hand around a rolled black leather top handle, and the bag is raised "
            "up at the mouth of the open bin, its front face turned toward the camera with the "
            "gold hardware clearly visible, about to slide in. The bin's interior is empty and "
            "plain. "
            "SCALE CHECK for this frame: the bag is wide enough that it very nearly fills the "
            "width of the open bin opening, with only a hand's width of clearance at each end, "
            "and it is far bigger than a handbag. Render it large in the frame. "
            "SETTING: an ordinary aircraft cabin interior in soft even artificial cabin light, "
            "plain pale grey moulded plastic panels and the muted grey blue fabric of seat backs "
            "below, everything but the bag falling gently out of focus. No other passengers, no "
            "safety cards, no placards, no lettering or symbols on any panel."
        ),
        extra=[],
    ),
]


def build(scene):
    parts = [
        PREAMBLE + IDENTITY + ".",
        ANTI_DRIFT,
        ANTI_CANVAS,
        HARDWARE_LAW,
        CLOSURE,
        "The bag is CLOSED in this picture: the flap is folded down over the front, its centre "
        "tab resting against the band, and both short belt straps lie horizontally into their "
        "gold clasp plates. Nothing is open, nothing is being unfastened, no hand is touching the "
        "hardware.",
        SCALE,
        CARRY,
        scene["beat"],
        *scene["extra"],
        MAN,
        LAYOUT,
        EDITORIAL,
    ]
    return "\n\n".join(p.strip() for p in parts)


if __name__ == "__main__":
    import json, os
    out = {}
    for s in SCENES:
        out[s["key"]] = dict(prompt=build(s), medias=[REFS[r] for r in s["refs"]])
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prompts.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2)
    for k, v in out.items():
        print(k, len(v["prompt"]), "chars,", len(v["medias"]), "refs")
