"""Scene ledger for VEL-WEEKENDER-MENSPACK-01 (IG packing-reel replication) — v2.

v2 changes (2026-08-10, Brooks review of the 36.7s v1 cut):
1. S01 (closed set-down) and S02 (empty reveal) are CUT — the ad opens directly on
   the first item being packed. 13 scenes, ~28.8s + card.
2. Every packing keyframe stages the NEW item held IN MID AIR above the open mouth,
   clearly entering from outside the bag, never resting on the contents with hands
   merely touching it. Kills the "items spawn in the hands / hand just moves things
   around" read.
3. SETTING/PHOTOREAL blocks rebuilt for flat daylight raw-TikTok look (see blocks.py).

state:   'closed' | 'open'   -> closure state NEVER changes inside a clip
pack:    key into CONTENTS -> this scene adds that item; prompt carries the
         verbatim lines of everything packed before it
"""

from blocks import (PREAMBLE, IDENTITY, ANTI_DRIFT, CLOSURE, HARDWARE_LAW, MECHANISM,
                    SCALE, SETTING, HANDS, FULL_BODY, PHOTOREAL, OVERHEAD,
                    CONTENTS, CONTENTS_ORDER, contents_so_far)

REFS = {
    "closed":   "LC-closed-front-unfastened.jpg",
    "open":     "LC-open-flap-inner-face-interior.jpg",
    "slip":     "LC-open-interior-slip-pocket.jpg",
    "macro":    "LC-macro-turnlock-flap.jpg",
    "scale":    "LC-hand-scale-front.jpg",
    "side":     "LC-closed-side-strap-detail.jpg",
    "band":     "LC-open-band-post-hand.jpg",
    "creator":  "creator-ref.jpg",
}

SCENES = [
    # v3 (2026-08-10, Brooks): the human set-down hook comes BACK (only the static
    # empty-bag reveal stays cut). Re-staged for the v2 daylight apartment.
    dict(
        id="S01", act="hook", state="closed", macro=False, target=2.6, gen=6,
        refs=["closed", "scale"], hardware=True, person="hands", overhead=False, pack=None,
        shot="a man's hand and forearm lowering the closed weekend bag by both rolled "
             "leather top handles onto the low dark wood coffee table, the bag a hand's "
             "width above the table top, front on to the camera, the flap down and the two "
             "cognac belt straps hanging loose near the side edges, the bright daylight "
             "living room soft behind it with the couch and its rumpled throw out of focus",
        scale="The bag is as wide as the table's near edge and fills the middle third of "
              "the frame, clearly heavy, clearly a piece of luggage rather than a handbag.",
        motion="The hand lowers the bag the last few inches onto the table, the bag settles "
               "with a small shift of weight, and the hand lets go and withdraws upward out "
               "of frame. Nothing on the bag opens, unfastens or changes. The flap stays "
               "down, the belt straps stay hanging. The camera is handheld and almost still.",
    ),
    dict(
        id="S03", act="pack", state="open", macro=False, target=2.2, gen=6,
        refs=["open", "slip"], hardware=False, person="hands", overhead=True, pack="tees",
        shot="a man's two hands entering the frame holding three tightly rolled navy cotton "
             "tee shirts together IN MID AIR above the open mouth of the bag, a clear gap of "
             "air visible between the rolled tees and the empty caramel interior below them, "
             "the tees clearly just carried in from outside the bag and not yet inside, about "
             "to be lowered into the far end of the interior at the top of the frame",
        scale="The three rolled tees together span less than half the length of the open "
              "mouth, with clear caramel leather interior left empty around them.",
        motion="His two hands carry the rolled tees down through the air into the far end of "
               "the bag, nest them side by side with one small press, and withdraw out of the "
               "top of the frame. The bag does not move. The folded back flap never moves. "
               "Nothing opens or closes. Handheld, almost still.",
    ),
    dict(
        id="S04", act="pack", state="open", macro=False, target=2.2, gen=6,
        refs=["open", "slip"], hardware=False, person="hands", overhead=True, pack="stack",
        shot="a man's two hands entering the frame holding a neatly folded stack of a cream "
             "oxford shirt under a folded charcoal knit sweater flat IN MID AIR above the open "
             "mouth of the bag, a clear gap of air between the stack and the interior below, "
             "the stack clearly just carried in from outside the bag and not yet inside, about "
             "to be lowered flat into the centre of the interior",
        scale="The folded stack sinks into the middle of the mouth with visible room left at "
              "both ends of the bag.",
        motion="His two hands carry the folded stack down through the air and lower it flat "
               "into the centre of the bag, settle it with one light press, and withdraw "
               "upward out of frame. The bag does not move. The folded back flap never moves. "
               "Nothing opens or closes.",
    ),
    dict(
        id="S05", act="pack", state="open", macro=False, target=2.0, gen=6,
        refs=["open", "slip"], hardware=False, person="hands", overhead=True, pack="dopp",
        shot="a man's hand entering the frame gripping a small structured black pebbled "
             "leather dopp kit IN MID AIR above the open mouth of the bag, a clear gap of air "
             "between the dopp kit and the interior below, the dopp kit clearly just carried "
             "in from outside the bag and not yet inside, about to be set down against the "
             "near end of the interior at the bottom of the frame",
        scale="The dopp kit takes up less than a quarter of the interior, standing snug "
              "against the near wall.",
        motion="His hand carries the black dopp kit down through the air, sets it against the "
               "near end, gives it one small push so it stands snug, and lifts away out of "
               "frame. The bag does not move. Nothing opens or closes. Handheld, almost still.",
    ),
    dict(
        id="S06", act="pack", state="open", macro=False, target=2.0, gen=6,
        refs=["open", "slip"], hardware=False, person="hands", overhead=True, pack="shoebag",
        shot="a man's two hands entering the frame holding a cream cotton drawstring shoe "
             "bag, rounded with the shape of a pair of sneakers inside it, IN MID AIR above "
             "the open mouth of the bag, a clear gap of air between the shoe bag and the "
             "contents below, the shoe bag clearly just carried in from outside the bag and "
             "not yet inside, about to be tucked lengthwise along the left wall of the "
             "interior",
        scale="The shoe bag runs most of the length of the left wall but stays narrow, "
              "leaving the centre of the bag visible.",
        motion="His two hands carry the cream shoe bag down through the air and slide it "
               "along the left wall, tuck it flat with a push of the knuckles, and withdraw. "
               "The bag does not move. Nothing opens or closes. Handheld, almost still.",
    ),
    dict(
        id="S07", act="pack", state="open", macro=False, target=2.0, gen=6,
        refs=["open", "slip"], hardware=False, person="hands", overhead=True, pack="bottle",
        shot="a man's hand entering the frame gripping a plain brushed stainless steel water "
             "bottle with no label and no lettering, holding it upright IN MID AIR above the "
             "near right corner of the open bag, a clear gap of air between the bottle's base "
             "and the interior below, the bottle clearly just carried in from outside the bag "
             "and not yet inside, about to be slotted down between the black dopp kit and the "
             "right wall",
        scale="The bottle stands no taller than the bag's mouth is deep, its brushed steel "
              "cap just below the rim of the opening once seated.",
        motion="His hand lowers the steel bottle straight down into the near right corner, "
               "wiggles it once so it sits snug between the dopp kit and the wall, and lets "
               "go and withdraws. The bag does not move. Nothing opens or closes.",
    ),
    dict(
        id="S08", act="pack", state="open", macro=False, target=2.2, gen=6,
        refs=["open", "slip"], hardware=False, person="hands", overhead=True, pack="headphones",
        shot="a man's two hands entering the frame holding a pair of plain matte black over "
             "ear headphones with smooth unbranded ear cups IN MID AIR above the open mouth "
             "of the bag, a clear gap of air between the headphones and the folded cream and "
             "charcoal clothing stack below, the headphones clearly just carried in from "
             "outside the bag and not yet inside, about to be laid flat on top of the stack "
             "in the centre",
        scale="The headphones span only the width of the folded stack beneath them, small "
              "against the full open mouth of the bag.",
        motion="His two hands carry the headphones down through the air and lay them flat on "
               "the clothing stack, square them with a fingertip, and withdraw out of frame. "
               "The bag does not move. Nothing opens or closes. Handheld, almost still.",
    ),
    dict(
        id="S09", act="pack", state="open", macro=False, target=2.0, gen=6,
        refs=["open", "slip"], hardware=False, person="hands", overhead=True, pack="hat",
        shot="a man's hand entering the frame holding a tan cotton canvas bucket hat by its "
             "brim IN MID AIR above the far end of the packed bag, a clear gap of air between "
             "the hat and the rolled navy tees below, the hat clearly just carried in from "
             "outside the bag and not yet inside, about to be dropped crown up onto the tees",
        scale="The bucket hat covers the rolled tees beneath it and nothing else, the rest of "
              "the packed interior still visible around it.",
        motion="His hand lowers the tan bucket hat down through the air and places it crown "
               "up onto the rolled tees, gives the brim one small pat, and lifts away. The "
               "bag does not move. Nothing opens or closes. Handheld, almost still.",
    ),
    dict(
        id="S10", act="organization", state="open", macro=False, target=2.4, gen=6,
        refs=["slip", "open"], hardware=False, person="hands", overhead=False, pack="pocketed",
        shot="a close view down into the open weekend bag at the wide caramel leather slip "
             "pocket against the interior wall, a man's hand entering the frame holding a "
             "navy passport and a slim cognac leather wallet together IN MID AIR just above "
             "the open slip pocket, the pocket mouth still empty below them, the passport and "
             "wallet clearly just brought in from outside the bag and not yet inside, about "
             "to be slid down into the pocket, the smooth caramel tan leather lining filling "
             "most of the frame and the packed clothes soft at the edge of frame",
        scale="His hand looks small against the interior wall, and the slip pocket runs "
              "wider than his outstretched hand.",
        motion="His hand slides the passport and the wallet down into the caramel slip "
               "pocket, pats them once so their top edges stand just above the pocket's edge, "
               "and withdraws. The bag and the pocket do not change shape. Nothing opens or "
               "closes. Handheld, almost still.",
    ),
    dict(
        id="S11", act="pack", state="open", macro=False, target=2.0, gen=6,
        refs=["open", "slip"], hardware=False, person="hands", overhead=True, pack="case",
        shot="a man's hand entering the frame gripping a cognac leather sunglasses case IN "
             "MID AIR above the packed bag, a clear gap of air between the case and the gap "
             "between the clothing stack and the black dopp kit below it, the case clearly "
             "just carried in from outside the bag and not yet inside, about to be wedged "
             "down into that last gap",
        scale="The case disappears into the one remaining gap, and with it the packed "
              "contents sit level with the mouth of the bag.",
        motion="His hand lowers the cognac case down through the air and presses it into the "
               "gap until it sits flush with the packed contents, and withdraws out of frame. "
               "The bag does not move. Nothing opens or closes.",
    ),
    dict(
        id="S12", act="payoff", state="open", macro=False, target=2.6, gen=6,
        refs=["open", "slip"], hardware=False, person="none", overhead=True, pack=None,
        packed_full=True,
        shot="the weekend bag packed completely full, every item in its place, nothing "
             "overflowing and the contents sitting level with the mouth",
        scale="The packed contents fill the entire mouth of the bag edge to edge, and the "
              "caramel interior is visible only in thin margins around them.",
        motion="Everything is completely still. Only the faintest handheld drift above the "
               "packed bag. No hands enter the frame. The folded back flap never moves. "
               "Nothing opens or closes.",
    ),
    dict(
        id="S13", act="closure", state="closed", macro=False, target=2.4, gen=6,
        refs=["closed", "macro"], hardware=True, person="none", overhead=False, pack=None,
        shot="the weekend bag now closed and packed full, standing on the low dark wood "
             "coffee table, photographed straight on from the front and very slightly above, "
             "the flap down over the front with its gold oval plate resting over the gold "
             "turn post, the two cognac belt straps hanging loose down the sides with their "
             "gold end plates, the bright daylight room soft and out of focus behind it",
        scale="The bag fills the width of the frame's middle, wider than it is tall, its "
              "sides gently rounded with the packed contents, unmistakably carry-on sized.",
        motion="A slow gentle push in toward the front of the bag. The bag is completely "
               "still. Nothing opens, unfastens, twists or moves. No hands enter the frame. "
               "The hardware holds its exact shape throughout.",
    ),
    dict(
        id="S14", act="payoff", state="closed", macro=False, target=2.6, gen=6,
        refs=["closed", "scale"], hardware=True, person="hands", overhead=False, pack=None,
        shot="a man's TWO flat hands, palms down and side by side, pressing down firmly on "
             "the top of the closed packed weekend bag where it stands on the low dark wood "
             "coffee table, photographed from the front and slightly above, the flap down and "
             "the belt straps hanging. Both forearms enter the frame from the TOP edge only "
             "and hang straight down to the hands. Neither arm crosses in front of the bag, "
             "and the whole front face of the bag stays visible and unobstructed",
        scale="Both his flat palms together cover only the middle third of the bag's top, "
              "the bag extending well beyond his hands on both sides.",
        motion="His two flat hands press down firmly on the top of the packed bag, hold, "
               "then lift away and out of the top of the frame. The bag does not slump, "
               "buckle or collapse: it holds its shape exactly. The flap stays down and one "
               "single piece, the belt straps stay hanging loose. Nothing opens or unfastens.",
    ),
    dict(
        id="S15", act="exit", state="closed", macro=False, target=3.2, gen=7,
        refs=["closed", "creator"], hardware=False, person="full", overhead=False, pack=None,
        shot="a wide view of the bright daylight apartment, the man standing beside the low "
             "dark wood coffee table having just lifted the closed weekend bag, carrying it "
             "by both rolled leather top handles in his left hand with his arm straight down "
             "at his side, facing away toward the door at the back of the room, daylight from "
             "the window washing the room flat and even",
        scale="The bag hangs from his fist and reaches from his hip down toward his knee, "
              "clearly a full sized piece of luggage rather than a handbag.",
        motion="The camera is completely locked off and does not pan, tilt or move at any "
               "point. He walks steadily AWAY from the camera toward the door, getting "
               "smaller in the frame with every step, and exits so the room is left empty in "
               "plain daylight. He only ever moves away from the camera and never moves back "
               "toward it, never reverses, never walks on the spot. The bag hangs from his "
               "left hand at his side the whole time and never goes onto his shoulder. "
               "Nothing on the bag opens, unfastens or changes.",
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
        parts += ["", contents_so_far(s["pack"], include=False)]
    if s.get("packed_full"):
        parts += ["", contents_so_far(CONTENTS_ORDER[-1], include=True)]
    parts += [
        "",
        "THE BAG: " + IDENTITY + "." + ANTI_DRIFT,
        "",
        SCALE + " " + s["scale"],
        "",
        HARDWARE_LAW,
    ]
    if s["hardware"]:
        parts += ["", CLOSURE]
    if s["state"] == "open":
        parts += ["", MECHANISM]
    packed = s.get("pack") or s.get("packed_full")
    if packed and (s.get("packed_full") or
                   CONTENTS_ORDER.index(s["pack"]) >= CONTENTS_ORDER.index("dopp")):
        parts += ["", "The only zipper in the entire scene belongs to the small black "
                      "leather dopp kit. The bag itself has no zipper anywhere."]
    if packed and (s.get("packed_full") or
                   CONTENTS_ORDER.index(s["pack"]) >= CONTENTS_ORDER.index("bottle")):
        parts += ["", "The brushed stainless steel water bottle prop is the one exception "
                      "to the gold hardware rule: the bottle is allowed to be plain brushed "
                      "steel. Every piece of metal on the bag itself stays warm brass gold."]
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
          f"{sum(1 for s in SCENES if s['state']=='open')} open-bag")
    if len(sys.argv) > 1:
        print("\n" + "=" * 70)
        print(build_prompt(scene_by_id(sys.argv[1])))
