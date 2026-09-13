"""Scene ledger for VEL-WEEKENDER-MENSID-01 — men's Haaland-identity travel ad.

11 generated keyframes (K02-K12). K01 is the composited real-photo plate, K13 is the
live PDP screen recording. Light Chocolate protagonist bag, one man, one outfit,
one trip: hotel room -> gate -> terminal -> cabin. iPhone TikTok aesthetic.

Verbatim product blocks are imported from the proven MENSLC-01 build. Only the
SETTING and the person blocks are new; nothing about the bag is re-derived.
"""
import os, sys
MENSLC = ("/Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/"
          "weekender/concepts/8:8:26 - mens carry lc (wool oak replication)/"
          "VEL-WEEKENDER-MENSLC-01/_build")
sys.path.insert(0, MENSLC)
from blocks import (PREAMBLE, IDENTITY, ANTI_DRIFT, CLOSURE, HARDWARE_LAW, MECHANISM,
                    SCALE, PHOTOREAL)  # noqa: E402  (SETTING/HANDS/FULL_BODY replaced below)

VAULT = "/Users/brooksorradre2/Documents/marketing brain"
REFDIR = os.path.join(VAULT, "brands/velantra/products/weekender/product-references/real-product-2026-08-08")
PIMG = os.path.join(VAULT, "brands/velantra/products/weekender/product-images")
HERE = os.path.dirname(os.path.abspath(__file__))

REFS = {
    "closed": os.path.join(REFDIR, "LC-closed-front-unfastened.jpg"),
    "open":   os.path.join(REFDIR, "LC-open-flap-inner-face-interior.jpg"),
    "slip":   os.path.join(REFDIR, "LC-open-interior-slip-pocket.jpg"),
    "macro":  os.path.join(REFDIR, "LC-macro-turnlock-flap.jpg"),
    "scale":  os.path.join(REFDIR, "LC-hand-scale-front.jpg"),
    "side":   os.path.join(REFDIR, "LC-closed-side-strap-detail.jpg"),
    "ag":     os.path.join(REFDIR, "AG-closed-front.jpg"),
    "dc":     os.path.join(PIMG, "dark-chocolate/picks/dc-01-front.png"),
    "blk":    os.path.join(PIMG, "black/picks/blk-01-front.png"),
    "creator": os.path.join(HERE, "creator-ref.png"),   # written after the K08 pick
}

# ---------------------------------------------------------------- settings
SETTING_HOTEL = (
    "The setting is a warm boutique hotel room in the evening: a bed with white rumpled "
    "linen bedding, a neutral upholstered bench, a warm brass table lamp as the dominant "
    "light source with soft window dusk behind, and a silver ribbed aluminum carry-on "
    "suitcase standing upright with its telescoping handle fully extended. A plain paper "
    "luggage tag hangs from the bag's handle on a thin loop, with NO readable writing on it. "
    "Ordinary lived-in clutter: a phone charging, a room key card, a watch on the side table."
)
SETTING_GATE = (
    "The setting is an airport gate seating area: rows of dark grey seats with metal armrests, "
    "a slatted panel wall and big windows onto the apron, mixed cool fluorescent light and "
    "daylight, other travelers soft and far out of focus in the background, a rolling suitcase "
    "parked by his knee. Any signage in the background is completely out of focus and "
    "unreadable, with no legible letters anywhere in the frame."
)
SETTING_TERMINAL = (
    "The setting is a wide airport terminal concourse: polished reflective floor, a moving "
    "walkway railing along one side, big glass walls with soft daylight, travelers far ahead "
    "soft and out of focus. Any overhead signage is far away, completely blurred and "
    "unreadable, with no legible letters anywhere in the frame."
)
SETTING_CABIN = (
    "The setting is a narrow-body aircraft cabin during boarding: an open overhead bin with "
    "its lid up, rows of dark seat backs below, warm cabin downlights mixed with cool window "
    "light, other passengers soft and out of focus down the aisle. No readable text, placards "
    "or lettering anywhere in the frame."
)

# ---------------------------------------------------------------- the one man
WARDROBE = ("an oversized black tailored blazer worn over a plain white crew neck tee, black "
            "relaxed tapered trousers, chunky white leather high-top sneakers, a beige "
            "corduroy cap worn backwards, a plain steel watch on the left wrist")
PROTAGONIST = (
    "The man in frame is in his early 30s, strikingly tall with a broad heavy athletic frame, "
    "short cropped light brown hair under the backwards cap, light stubble, fair skin with "
    "natural texture and visible pores, wearing " + WARDROBE + ". A few flyaway details, "
    "slight phone camera softness, never tack sharp, never airbrushed."
)
HANDS = (
    "Only the man's hands and forearms are in frame: large hands, fair skin with natural "
    "texture, visible pores and fine hair on the forearms, short clean fingernails, a plain "
    "steel watch on the left wrist, no rings, the black sleeve of an oversized blazer and the "
    "white tee cuff visible at the edge of frame. No face, no head."
)
TORSO = (
    "The man is visible only from the shoulders or chest down, his face out of frame above "
    "the top edge: early 30s, strikingly tall with a broad heavy athletic frame, wearing "
    + WARDROBE + ". No face is visible."
)
BEHIND = (
    "The man is seen from behind at a three-quarter angle, his face turned away and not "
    "visible: early 30s, strikingly tall with a broad heavy athletic frame filling the "
    "frame height, the back of a beige corduroy cap worn backwards over short cropped light "
    "brown hair, wearing " + WARDROBE + "."
)
CREATOR_MATCH = (
    "The man in frame is the EXACT same person as in the attached creator reference photo: "
    "same face, same build, same clothing, same backwards beige cap. " + PROTAGONIST
)

# ---------------------------------------------------------------- K12 lineup identity
LINEUP = (
    "FOUR weekend bags of the exact same silhouette, size and construction stand side by side "
    "in one straight row, all four identical to the reference bags in shape, proportions and "
    "hardware, differing ONLY in colorway. From left to right: FIRST the light chocolate bag, "
    "rich cognac brown leather upper flap section and rolled handles over a cream ivory woven "
    "canvas body, exactly as the first reference photo. SECOND the army green bag, deep olive "
    "green twill canvas body with a denser smoother weave that reads almost solid, under a "
    "slightly lighter tan brown leather upper section, exactly as the second reference photo. "
    "THIRD the dark chocolate bag, cream ivory woven canvas body under a very dark espresso "
    "brown leather upper section with subtle vintage pull-up marbling, exactly as the third "
    "reference photo. FOURTH the black bag, its ENTIRE body smooth black leather including the "
    "lower section, with the same construction, exactly as the fourth reference photo. Every "
    "bag is closed with its flap down, straps hanging near its side edges, warm brass gold "
    "hardware, no logos or lettering anywhere on any bag. Every bag is noticeably WIDER than "
    "it is tall, a low wide weekend bag shape like the reference photos, never an upright "
    "narrow satchel, never taller than wide. All four bags are the SAME width and "
    "the SAME height, sitting level in one row."
)

SETTINGS = {"hotel": SETTING_HOTEL, "gate": SETTING_GATE,
            "terminal": SETTING_TERMINAL, "cabin": SETTING_CABIN}
PEOPLE = {"hands": HANDS, "torso": TORSO, "behind": BEHIND,
          "full": PROTAGONIST, "creator": CREATOR_MATCH,
          "none": "No people are in the frame at all."}

SCENES = [
    dict(
        id="K02", line="This is the Eleanor Weekender from Velantra, and it's about a hundred and sixty dollars.",
        state="closed", setting="hotel", person="torso", refs=["closed", "scale"], hardware=True,
        shot="the closed weekend bag sitting balanced flat on top of the extended telescoping "
             "handle of the silver ribbed aluminum carry-on suitcase, front on to camera, the "
             "man's hand just letting go of the top handle as he steps back, a plain paper "
             "luggage tag hanging from the handle base",
        scale="The bag overhangs the carry-on suitcase below it on both sides, clearly wider "
              "than the suitcase itself, unmistakably a large piece of luggage.",
    ),
    dict(
        id="K03", line="It's a Birkin-inspired shape scaled up to travel size,",
        state="closed", setting="gate", person="creator", refs=["closed", "creator"], hardware=True,
        shot="the man seated on a gate seat leaning toward the camera, holding the closed "
             "weekend bag up and out toward the lens by both rolled top handles with one hand, "
             "the bag front on and level, filling the lower two thirds of the frame, his face "
             "and backwards cap visible above it, shot selfie-distance like a phone propped on "
             "his knee",
        scale="Held up at arm's length the bag is as wide as his shoulders and hides his whole "
              "torso, clearly a large travel bag and not a handbag.",
    ),
    dict(
        id="K04", line="so it holds three days of clothes and still keeps its shape packed full.",
        state="open", setting="hotel", person="hands", refs=["open", "slip"], hardware=False,
        shot="the weekend bag sitting open on the white hotel bedding, packed full with a "
             "neatly folded stack of shirts, rolled tee shirts and a charcoal dopp kit, the "
             "man's flat palm pressing down once on the packed clothes, the bag's sides "
             "standing perfectly straight and rectangular under the load, the folded back "
             "flap leaning back behind the mouth",
        scale="The packed opening is wider than both of his spread hands together, and the "
              "walls stand straight with no bulge or slouch.",
    ),
    dict(
        id="K05", line="Smooth leather over canvas, solid brass hardware, contrast stitching,",
        state="closed", setting="hotel", person="hands", refs=["macro", "closed"], hardware=True,
        shot="a tight macro of the front of the closed weekend bag in warm lamp light, the "
             "man's hand resting completely still on the cognac leather band beside the gold "
             "turn post, thumb near the oval plate, the canvas weave and the leather grain and "
             "the contrast stitching filling the frame in sharp detail. The front of the bag has NO pocket of any kind: no pocket flap, no pouch, no postman's lock pocket. The cognac upper section is simply the bag's one-piece fold-over flap lying flat, with its small centre tab, and the oval plate's face is completely blank smooth polished gold with only the empty keyhole cutout, no emblem, no motif, no raised twisting bar. Both belt straps hang at the far left and far right edges of the frame.",
        scale="His hand looks small against the front of the bag, spanning only a fraction of "
              "its width.",
    ),
    dict(
        id="K06", line="and no logo anywhere on it.",
        state="closed", setting="hotel", person="hands", refs=["closed", "side"], hardware=True,
        shot="the man's two hands holding the closed weekend bag up close to the camera, "
             "slowly turning it a few degrees, the bare cream canvas front and the plain "
             "cognac leather band filling most of the frame with nothing printed, stamped, "
             "embossed or written anywhere on it. The front of the bag has NO pocket of any kind: no pocket flap, no pouch, no postman's lock pocket. The cognac upper section is simply the bag's one-piece fold-over flap lying flat, with its small centre tab, and the oval plate's face is completely blank smooth polished gold with only the empty keyhole cutout, no emblem, no motif, no raised twisting bar.",
        scale="The bag is far wider than the frame can comfortably hold, its edges nearly "
              "touching both sides of the frame.",
    ),
    dict(
        id="K07", line="The whole inside is caramel leather with a wide slip pocket.",
        state="open", setting="hotel", person="hands", refs=["slip", "open"], hardware=False,
        shot="the man's two hands holding the mouth of the open weekend bag apart on the "
             "hotel bed, camera looking down and in so the smooth caramel tan leather "
             "interior lining and the wide matching caramel slip pocket on the interior wall "
             "are clearly visible and fill the middle of the frame",
        scale="The open mouth is wide enough that both his hands holding it apart do not "
              "crowd it, with the interior stretching deep below.",
    ),
    dict(
        id="K08", line="For scale, I'm six foot four. It's eighteen inches wide, and it still looks big on me.",
        state="closed", setting="hotel", person="full", refs=["closed", "scale"], hardware=True,
        shot="a full body shot of the man standing in the hotel room beside the silver ribbed "
             "aluminum carry-on suitcase, holding the closed weekend bag at his side by both "
             "rolled top handles in one hand, the bag hanging at his thigh, his whole body "
             "from cap to sneakers in frame with room above his head, shot from across the "
             "room at chest height like a friend took it",
        scale="Even against his strikingly tall broad frame the bag reads large, reaching "
              "from his hip toward his knee, clearly wider than his thigh, and the carry-on "
              "suitcase beside him confirms the scale.",
    ),
    dict(
        id="K09", line="It sits on top of my carry-on through the whole terminal,",
        state="closed", setting="terminal", person="behind", refs=["closed"], hardware=True,
        shot="the man walking away down the terminal concourse at a three-quarter angle from "
             "behind, pulling the silver ribbed aluminum carry-on with the closed weekend bag "
             "riding balanced on top of its extended handle, his stride mid step, the bag's "
             "front three-quarter face catching the light toward camera",
        scale="The bag riding on the carry-on is clearly wider than the suitcase below it, "
              "and against his tall frame it still reads as a large piece of luggage.",
    ),
    dict(
        id="K10", line="it slides straight into the overhead bin,",
        state="closed", setting="cabin", person="hands", refs=["closed"], hardware=True,
        shot="the man's two hands lifting the closed weekend bag up into an open overhead "
             "bin, the bag halfway in, sliding flat on its base with clear space between its "
             "top edge and the bin ceiling, the open bin lid and the bin edge framing it",
        scale="The bag fills most of the bin opening's width yet clears the bin ceiling with "
              "visible room, exactly carry-on sized.",
    ),
    dict(
        id="K11", line="and my laptop and charger live in that slip pocket.",
        state="open", setting="gate", person="hands", refs=["slip", "open"], hardware=False,
        shot="the open weekend bag standing on the man's lap as he sits in a gate seat, his "
             "hand sliding a thin closed dark laptop down into the wide caramel leather slip "
             "pocket against the interior wall, the smooth caramel tan leather lining visible "
             "around it, a coiled white charger cable waiting on his knee",
        scale="The laptop disappears into the slip pocket with the pocket's width to spare, "
              "and the open mouth is far wider than the laptop.",
    ),
    dict(
        id="K12", line="It comes in four colors.",
        state="closed", setting="hotel", person="hands", refs=["closed", "scale"], hardware=True,
        shot="the closed light chocolate weekend bag standing alone on the white hotel bedding, "
             "front on to camera, the man's hand entering from the right and resting on the top "
             "of the flap as he squares the bag toward the camera, the flap down, the two belt "
             "straps hanging near the side edges, warm lamp light from the left",
        scale="The bag is wider than it is tall and spans most of the bed's width in frame, "
              "his hand small against the top of it, unmistakably a large travel bag.",
    ),
]


def build_prompt(s):
    person = PEOPLE[s["person"]]
    identity = s.get("identity_override")
    if identity:
        bag_block = "THE BAGS: " + identity
    else:
        bag_block = "THE BAG: " + IDENTITY + "." + ANTI_DRIFT
    parts = [
        PREAMBLE + s["shot"] + ".",
        "",
        bag_block,
        "",
        SCALE + " " + s["scale"],
        "",
        HARDWARE_LAW,
    ]
    if s["hardware"]:
        parts += ["", CLOSURE]
    if s["state"] == "open":
        parts += ["", MECHANISM]
    parts += ["", person, "", SETTINGS[s["setting"]], "", PHOTOREAL]
    return "\n".join(parts)


def scene_by_id(sid):
    for s in SCENES:
        if s["id"] == sid:
            return s
    raise KeyError(sid)


if __name__ == "__main__":
    import sys as _s
    print(f"{len(SCENES)} scenes, {sum(1 for s in SCENES if s['state']=='open')} open-bag")
    if len(_s.argv) > 1:
        print("=" * 70)
        print(build_prompt(scene_by_id(_s.argv[1])))
