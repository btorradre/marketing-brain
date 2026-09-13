"""Scene ledger for VEL-WEEKENDER-BLKCARRYON-01.

Replication of IG reel DbkwLfUAXf6 (@sebaswl, 18.4s, music-only, no dialogue):
a man reveals a carry-on, pulls its handle, packs it flat-lay overhead, closes it,
then leaves with it and moves through the city.

BROOKS'S REDIRECT (2026-08-11): men's angle, BLACK Weekender, and the suitcase is
no longer the thing being packed — he brings the suitcase out, sets the Weekender
ON TOP of it, then the cut lands on the packing, shot-on-iPhone in natural light,
ready to post to IG or TikTok.

STRUCTURE MAP against the reference:
  ref 0-3s   dust bag off -> case revealed -> handle pulled   ->  S01-S02  suitcase in, bag placed on top
  ref 3-9s   overhead flat-lay packing, ~6 items              ->  S03-S08  overhead packing, 6 items
  ref 9-12s  straps buckled, laptop slid in, case closed      ->  S09-S10  packed full, then closed
  ref 12-18s stands with it, walks out, city, bench           ->  S11-S12  back on the suitcase, walks out

DELIBERATE DEPARTURES FROM THE REFERENCE (and why):
  - The reference's third act is four outdoor beats (POV roll, street tracking, bench,
    walk-off). Cut to two indoor beats. Outdoor continuity on a generated creator across
    four locations is the single most expensive thing in the reference and it sells the
    creator's lifestyle, not our bag.
  - The reference's suitcase is a branded aluminium case with orange trim. Ours is a
    plain unbranded pale grey shell (see SUITCASE in blocks.py). We don't replicate a
    competitor's product design.
  - The bag NEVER rides on top of the rolling suitcase while he walks. It has no trolley
    sleeve (the back is a plain leather band) and a bag balanced on a tilted case falls
    off. On-the-suitcase is the PARKED image, S02 and S11; the walking exit is one item
    in each hand.

PRODUCTION LAWS OBSERVED:
  state:  'closed' | 'open'  -> closure state NEVER changes inside a clip. Every
          closure change happens across a hard cut between audited frames.
  Open-bag beats NEVER go to Seedance. GPT Image 2 i2i still -> Omni i2v, always.
  Every packing beat stages the NEW item IN MID AIR above the mouth, entering from
          outside the frame. Hands rearranging existing contents reads fake = FAIL.
  Single-hand blocking wherever one hand can do the job (two hands across the bag
          breeds a second wristwatch).
"""

from blocks import (PREAMBLE, IDENTITY, ANTI_DRIFT, ANTI_CANVAS, CLOSURE, HARDWARE_LAW,
                    MECHANISM, SCALE, SUITCASE, SETTING, HANDS, FULL_BODY, PHOTOREAL,
                    OVERHEAD, GEOMETRY_ANCHOR, MIDAIR, CONTENTS, CONTENTS_ORDER,
                    contents_so_far)

# Black ground truth outranks the LC library for this build. `blkopen` carries the
# caramel interior against black leather; `blkfront` is the closed/material anchor.
REFS = {
    "blkfront":  ("black", "black-01.png"),   # front, all black leather, gold hardware
    "blkthree":  ("black", "black-02.png"),   # three-quarter
    "blkopen":   ("black", "black-03.png"),   # OPEN — caramel tan interior truth
    "blkscale":  ("black", "black-04.png"),   # carried, scale against a person
    "blkmacro":  ("black", "black-05.png"),   # gold hardware macro on black leather
    "lcopen":    ("lc",    "LC-open-flap-inner-face-interior.jpg"),  # fold-back geometry
    "creator":   ("creator", "creator-ref.jpg"),
    # the QA-approved S03 pick, re-uploaded as the sibling geometry anchor
    "anchor":    ("anchor",  "S03-anchor.png"),
}

SCENES = [
    # ---------------------------------------------------------------- ACT 1: the suitcase
    # TOF law: open on a person doing a thing, not on the product. The suitcase is the
    # expected travel object; the Weekender landing on it is the upgrade.
    dict(
        id="S01", act="hook", state=None, macro=False, target=3.0, gen=6,
        refs=["creator"], hardware=False, person="full", overhead=False, pack=None,
        suitcase=True, bag=False,
        shot="a man wheeling a plain pale silver grey hard shell carry-on suitcase in through "
             "the bedroom doorway by its extended black trolley handle and parking it upright "
             "on the pale wood floor at the foot of the bed, seen from across the room at "
             "chest height, the bright white bedding and the window light filling the room "
             "behind him",
        scale="The parked suitcase stands about as high as his hip.",
        motion="He wheels the suitcase in through the doorway, rolls it the last couple of "
               "steps to the foot of the bed, stands it upright and lets go of the handle. "
               "The camera is handheld and almost still. Nothing else in the room moves.",
    ),
    dict(
        id="S02", act="hook", state="closed", macro=False, target=2.6, gen=6,
        refs=["blkfront", "blkscale"], hardware=True, person="hands", overhead=False,
        pack=None, suitcase=True, bag=True,
        shot="a man's hand and forearm lowering the closed all black weekend bag by both rolled "
             "black leather top handles down onto the flat top face of the parked silver grey "
             "carry-on suitcase, the bag a hand's width above the suitcase and front on to the "
             "camera, its scalloped flap down and its two short belt straps lying horizontally "
             "into their gold clasp plates, the suitcase's trolley handle pushed all the way "
             "down flush so the top of the suitcase is flat, the bright bedroom soft behind them",
        scale="The weekend bag is WIDER than the top of the suitcase and overhangs it slightly "
              "at both ends, clearly a full piece of luggage rather than a handbag.",
        motion="The hand lowers the black bag the last few inches onto the top of the suitcase, "
               "the bag settles with a small shift of weight, and the hand lets go and "
               "withdraws upward out of frame. Nothing on the bag opens, unfastens or changes: "
               "the flap stays down and one single piece, the two belt straps stay horizontal "
               "in their gold plates. The suitcase does not move. Handheld, almost still.",
    ),

    # ---------------------------------------------------------------- ACT 2: the packing
    # Hard cut. New setup: bag open on the bed, locked top-down phone camera.
    dict(
        id="S03", act="pack", state="open", macro=False, target=2.4, gen=6,
        refs=["blkopen", "lcopen"], hardware=False, person="hands", overhead=True, pack="jeans",
        shot="a man's two hands entering the frame holding a pair of neatly folded dark indigo "
             "jeans flat IN MID AIR above the open mouth of the black bag, a clear gap of air "
             "visible between the folded jeans and the empty caramel tan leather interior below "
             "them, the jeans clearly just carried in from outside the bag and not yet inside, "
             "about to be lowered flat into the CENTRE of the interior",
        scale="The folded jeans fill the middle third of the open mouth, with empty caramel "
              "leather visible at both ends of the interior beside them.",
        motion="His two hands carry the folded jeans down through the air into the centre of "
               "the bag, lay them flat with one light press, and withdraw out of the bottom of "
               "the frame. The bag does not move. The folded back flap never moves. Nothing "
               "opens or closes. Handheld, almost still.",
    ),
    dict(
        id="S04", act="pack", state="open", macro=False, target=2.4, gen=6,
        refs=["blkopen", "lcopen", "anchor"], hardware=False, person="hands", overhead=True, pack="stack",
        shot="a man's two hands entering the frame holding a neatly folded stack of a white "
             "cotton tee under a folded heather grey crewneck sweatshirt flat IN MID AIR above "
             "the open mouth of the black bag, a clear gap of air between the stack and the "
             "interior below, the stack clearly just carried in from outside the bag and not "
             "yet inside, about to be lowered flat against the LEFT end of the interior",
        scale="The folded stack fills the left third of the mouth with the folded jeans still "
              "visible beside it in the centre.",
        motion="His two hands carry the folded stack down through the air and lower it flat "
               "against the left end of the bag, settle it with one light press, and withdraw upward "
               "out of frame. The bag does not move. The folded back flap never moves. Nothing "
               "opens or closes.",
    ),
    dict(
        id="S05", act="pack", state="open", macro=False, target=2.2, gen=6,
        refs=["blkopen", "lcopen", "anchor"], hardware=False, person="hands", overhead=True, pack="dopp",
        shot="a man's ONE hand entering the frame gripping a small structured black pebbled "
             "leather dopp kit IN MID AIR above the open mouth of the black bag, a clear gap of "
             "air between the dopp kit and the contents below, the dopp kit clearly just "
             "carried in from outside the bag and not yet inside, about to be set down against "
             "the RIGHT end of the interior",
        scale="The dopp kit takes up less than a quarter of the interior, standing snug against "
              "the right wall.",
        motion="His hand carries the black dopp kit down through the air, sets it against the "
               "right end, gives it one small push so it stands snug, and lifts away out of "
               "frame. The bag does not move. Nothing opens or closes. Handheld, almost still.",
    ),
    dict(
        id="S06", act="pack", state="open", macro=False, target=2.2, gen=6,
        refs=["blkopen", "lcopen", "anchor"], hardware=False, person="hands", overhead=True, pack="shoebag",
        shot="a man's two hands entering the frame holding a cream cotton drawstring shoe bag, "
             "rounded with the shape of a pair of sneakers inside it, IN MID AIR above the open "
             "mouth of the black bag, a clear gap of air between the shoe bag and the contents "
             "below, the shoe bag clearly just carried in from outside the bag and not yet "
             "inside, about to be tucked lengthwise along the FAR wall of the interior behind the folded jeans",
        scale="The shoe bag runs most of the length of the far wall but stays narrow, leaving "
              "the packed contents in front of it visible.",
        motion="His two hands carry the cream shoe bag down through the air and slide it along "
               "the far wall behind the jeans, tuck it flat with a push of the knuckles, and withdraw. The bag "
               "does not move. Nothing opens or closes. Handheld, almost still.",
    ),
    dict(
        id="S07", act="pack", state="open", macro=False, target=2.2, gen=6,
        refs=["blkopen", "lcopen", "anchor"], hardware=False, person="hands", overhead=True, pack="tech",
        shot="a man's ONE hand entering the frame holding a flat plain black nylon tech pouch "
             "IN MID AIR above the open mouth of the black bag, a clear gap of air between the "
             "pouch and the folded dark indigo jeans below it, the pouch clearly "
             "just carried in from outside the bag and not yet inside, about to be laid flat on "
             "top of the jeans in the centre",
        scale="The flat pouch spans only the width of the folded jeans beneath it, small "
              "against the full open mouth of the bag.",
        motion="His hand carries the black pouch down through the air and lays it flat on the "
               "folded jeans, squares it with a fingertip, and withdraws out of frame. The "
               "bag does not move. Nothing opens or closes. Handheld, almost still.",
    ),
    dict(
        id="S08", act="organization", state="open", macro=False, target=2.6, gen=6,
        refs=["blkopen", "lcopen"], hardware=False, person="hands", overhead=False,
        pack="pocketed",
        shot="a close view down into the open black weekend bag at the wide caramel tan leather "
             "slip pocket standing against the interior wall, a man's hand entering the frame "
             "holding a navy passport and a pair of folded black sunglasses together IN MID AIR "
             "just above the open slip pocket, the pocket mouth still empty below them, the "
             "passport and sunglasses clearly just brought in from outside the bag and not yet "
             "inside, about to be slid down into the pocket, the smooth caramel tan lining "
             "filling most of the frame with the black leather rim of the bag across the top of "
             "the frame and the packed clothes soft at the edge of frame",
        scale="His hand looks small against the interior wall, and the slip pocket runs wider "
              "than his outstretched hand.",
        motion="His hand slides the passport and the sunglasses down into the caramel slip "
               "pocket, pats them once so their top edges stand just above the pocket's edge, "
               "and withdraws. The bag and the pocket do not change shape. Nothing opens or "
               "closes. Handheld, almost still.",
    ),

    # ---------------------------------------------------------------- ACT 3: closed and gone
    dict(
        id="S09", act="payoff", state="open", macro=False, target=2.4, gen=6,
        refs=["blkopen", "lcopen", "anchor"], hardware=False, person="none", overhead=True, pack=None,
        packed_full=True,
        shot="the black weekend bag packed completely full on the white bedding, every item in "
             "its place, nothing overflowing and the contents sitting level with the mouth, no "
             "hands anywhere in the frame",
        scale="The packed contents fill the entire mouth of the bag edge to edge, and the "
              "caramel lining is visible only in thin margins around them.",
        motion="Everything is completely still. Only the faintest handheld drift above the "
               "packed bag. No hands enter the frame. The folded back flap never moves. Nothing "
               "opens or closes.",
    ),
    dict(
        id="S10", act="closure", state="closed", macro=False, target=2.4, gen=6,
        refs=["blkfront", "blkmacro"], hardware=True, person="none", overhead=False, pack=None,
        shot="the black weekend bag now closed and packed full, sitting on the white bedding, "
             "photographed straight on from the front and very slightly above, its scalloped "
             "flap down over the front with the gold oval plate seated at the centre, the two "
             "short black belt straps lying horizontally into their gold clasp plates, the small "
             "black leather key bell hanging on its lace down the front, the bright bedroom soft "
             "and out of focus behind it",
        scale="The bag fills the width of the frame's middle, wider than it is tall, its sides "
              "gently rounded with the packed contents, unmistakably carry-on sized.",
        motion="A slow gentle push in toward the front of the bag. The bag is completely still "
               "apart from the key bell settling on its lace. Nothing opens, unfastens, twists "
               "or moves. No hands enter the frame. The hardware holds its exact shape "
               "throughout.",
    ),
    dict(
        id="S11", act="payoff", state="closed", macro=False, target=2.6, gen=6,
        refs=["blkfront", "blkscale"], hardware=True, person="hands", overhead=False, pack=None,
        suitcase=True, bag=True,
        shot="a man's hand and forearm setting the closed, packed, visibly fuller black weekend "
             "bag down by both rolled handles onto the flat top of the parked silver grey "
             "carry-on suitcase, front on to the camera, exactly the same framing and the same "
             "spot as the earlier shot of him placing the empty bag there, the trolley handle "
             "still pushed all the way down flush",
        scale="The packed bag is WIDER than the top of the suitcase and overhangs it slightly at "
              "both ends, its sides now rounded out with the contents.",
        motion="The hand lowers the packed bag the last few inches onto the top of the "
               "suitcase, the bag settles heavily, and the hand releases the handles and "
               "withdraws upward out of frame. The bag holds its shape and does not slump or "
               "buckle. Nothing opens or unfastens. The suitcase does not move.",
    ),
    dict(
        id="S12", act="exit", state="closed", macro=False, target=3.2, gen=7,
        refs=["blkfront", "creator"], hardware=False, person="full", overhead=False, pack=None,
        suitcase=True, bag=True,
        shot="a wide view of the bright bedroom from across the room, the man walking away "
             "toward the open doorway at the back, rolling the silver grey carry-on suitcase "
             "beside him by its extended black trolley handle in his RIGHT hand while the "
             "closed black weekend bag hangs from his LEFT hand by both rolled leather handles, "
             "his left arm straight down at his side, daylight from the window washing the room "
             "flat and even",
        scale="The weekend bag hangs from his fist and reaches from his hip down toward his "
              "knee, about as tall as the suitcase rolling on his other side.",
        motion="The camera is completely locked off and does not pan, tilt or move at any "
               "point. He walks steadily AWAY from the camera toward the doorway, the suitcase "
               "rolling along beside him on its wheels, getting smaller in the frame with every "
               "step, and exits through the door so the room is left empty in plain daylight. "
               "He only ever moves away from the camera and never moves back toward it, never "
               "reverses and never walks on the spot. The weekend bag hangs from his left hand "
               "at his side the whole time and never goes onto his shoulder and never goes on "
               "top of the suitcase. Nothing on the bag opens, unfastens or changes.",
    ),
]


def build_prompt(s):
    """Assemble the full-density i2i prompt for one scene."""
    person = {"hands": HANDS, "full": FULL_BODY,
              "none": "No people are in the frame at all."}[s["person"]]
    parts = [PREAMBLE + s["shot"] + "."]
    if s.get("overhead"):
        parts += ["", OVERHEAD]
    if s.get("pack"):
        parts += ["", contents_so_far(s["pack"], include=False), "", MIDAIR]
    if s.get("packed_full"):
        parts += ["", contents_so_far(CONTENTS_ORDER[-1], include=True)]

    # S01 is the only scene with no bag in it at all.
    if s.get("bag", True):
        parts += [
            "",
            "THE BAG: " + IDENTITY + "." + ANTI_DRIFT,
            "",
            ANTI_CANVAS,
            "",
            SCALE + " " + s["scale"],
            "",
            HARDWARE_LAW,
        ]
        if s["hardware"]:
            parts += ["", CLOSURE]
        if s["state"] == "open":
            parts += ["", MECHANISM]
    else:
        parts += ["", SCALE.replace("SCALE IS CRITICAL. This is", "For reference the weekend "
                                    "bag that appears later in this ad is") + " " + s["scale"]]

    if s.get("suitcase"):
        parts += ["", SUITCASE]

    packed = s.get("pack") or s.get("packed_full")
    if packed and (s.get("packed_full") or
                   CONTENTS_ORDER.index(s["pack"]) >= CONTENTS_ORDER.index("dopp")):
        parts += ["", "The only zippers in the entire scene belong to the small black leather "
                      "dopp kit and the flat black tech pouch. The bag itself has no zipper "
                      "anywhere."]
    if "anchor" in s["refs"]:
        parts += ["", GEOMETRY_ANCHOR]
    parts += ["", person, "", SETTING, "", PHOTOREAL]
    return "\n".join(parts)


def scene_by_id(sid):
    for s in SCENES:
        if s["id"] == sid:
            return s
    raise KeyError(sid)


if __name__ == "__main__":
    import sys
    total = sum(s["target"] for s in SCENES)
    print(f"{len(SCENES)} scenes, {total:.1f}s target, "
          f"{sum(1 for s in SCENES if s['state']=='open')} open-bag, "
          f"{sum(1 for s in SCENES if s.get('suitcase'))} with the suitcase")
    if len(sys.argv) > 1:
        print("\n" + "=" * 70)
        print(build_prompt(scene_by_id(sys.argv[1])))
