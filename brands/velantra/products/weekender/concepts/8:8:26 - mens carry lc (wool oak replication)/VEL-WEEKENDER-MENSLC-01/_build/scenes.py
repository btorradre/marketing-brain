"""Scene ledger for VEL-WEEKENDER-MENSLC-01.

13 scenes, Light Chocolate only, one continuous hotel room, congruent throughout.
Every scene authored INDEPENDENTLY from the real-product stills. Nothing chains.

state:   'closed' | 'open'   -> closure state NEVER changes inside a clip
macro:   True -> Omni gets ONE roll; on drift it falls back to Ken Burns
                 (feedback_omni_macro_mutation: macros are 0/5 on re-roll)
"""

from blocks import (PREAMBLE, IDENTITY, ANTI_DRIFT, CLOSURE, HARDWARE_LAW, MECHANISM,
                    SCALE, SETTING, HANDS, FULL_BODY, PHOTOREAL)

# refs: keys into REFS below
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
    dict(
        id="S01", act="hook", state="closed", macro=False, target=2.4, gen=6,
        refs=["closed", "scale"], hardware=True, person="hands",
        shot="a man's hand holding the closed weekend bag suspended in the air by both "
             "rolled leather top handles, at chest height over the white rumpled bedding of "
             "the low walnut platform bed, the bag hanging front on and level at the centre "
             "of the frame, the charcoal grey wool throw folded across the foot of the bed "
             "behind it",
        scale="The bag is as wide as a man's shoulders and hangs from his fist filling the "
              "middle third of the frame, clearly heavy, clearly a piece of luggage.",
        motion="The hand holding the bag by its handles lowers very slightly and the bag "
               "sways once, gently, then steadies. The camera is handheld and almost still. "
               "Nothing on the bag opens, unfastens or changes. The flap stays down, the belt "
               "straps stay hanging loose. No other movement in the room.",
    ),
    dict(
        id="S02", act="hook", state="closed", macro=False, target=2.2, gen=6,
        refs=["closed"], hardware=True, person="none",
        shot="the closed weekend bag resting on the charcoal grey wool throw at the foot of "
             "the low walnut platform bed, photographed straight on from the front and very "
             "slightly above, the flap down over the front and the two cognac belt straps "
             "hanging loose down the sides with their gold end plates visible, the warm oak "
             "slatted headboard wall soft and out of focus behind it",
        scale="The bag is wider than the folded charcoal throw it sits on and spans most of "
              "the frame width, unmistakably carry-on sized rather than handbag sized.",
        motion="The bag is completely still. Only a slow gentle push in toward the front of "
               "the bag, and the soft daylight shifting almost imperceptibly across the "
               "canvas. Nothing on the bag opens, unfastens, moves or changes shape.",
    ),
    dict(
        id="S03", act="capacity", state="open", macro=False, target=2.6, gen=6,
        refs=["open", "slip"], hardware=False, person="none",
        shot="the weekend bag sitting open and empty on the charcoal grey wool throw at the "
             "foot of the bed, photographed from the front and slightly above so the open "
             "mouth and the smooth caramel tan leather interior are clearly visible, the "
             "folded back flap leaning back behind the mouth",
        scale="The open mouth is wide enough and long enough to drop a folded stack of "
              "shirts straight down through it lying flat.",
        motion="A slow gentle push in toward the open mouth of the bag. The bag itself is "
               "completely still. The folded back flap stays exactly where it is, one single "
               "piece leaning back behind the mouth, and never moves, folds, splits or covers "
               "the front. No hands enter the frame. Nothing opens or closes.",
    ),
    dict(
        id="S04", act="capacity", state="open", macro=False, target=2.6, gen=6,
        refs=["open", "slip"], hardware=False, person="hands",
        shot="a man's two hands lowering a neatly folded stack of a white oxford shirt and a "
             "navy crewneck sweater down into the open mouth of the weekend bag, the bag open "
             "on the charcoal grey wool throw at the foot of the bed, the smooth caramel tan "
             "leather interior visible around the clothes",
        scale="The folded stack of clothes looks small against the open mouth, sinking in "
              "with clear room left on both sides of it.",
        motion="His two hands lower the folded stack of clothes down into the open bag, "
               "settle it flat, and withdraw upward out of the top of the frame. The bag does "
               "not move. The folded back flap stays one single piece leaning back behind the "
               "mouth and never moves. Nothing opens or closes. Handheld, almost still.",
    ),
    dict(
        id="S05", act="capacity", state="open", macro=False, target=2.6, gen=6,
        refs=["open", "slip"], hardware=False, person="hands",
        shot="looking down into the open weekend bag from above, a man's hand setting a "
             "charcoal canvas dopp kit down beside three tightly rolled white tee shirts that "
             "already sit inside next to the folded shirts, the smooth caramel tan leather "
             "interior lining visible around everything",
        scale="The dopp kit looks small beside the contents, taking up less than a third of "
              "the interior, with room still left around it.",
        motion="His hand sets the charcoal dopp kit down into the bag beside the rolled tee "
               "shirts, presses it once so it settles, and lifts away out of frame. The bag "
               "does not move at all. Nothing opens or closes. Handheld, almost still.",
    ),
    dict(
        id="S06", act="organization", state="open", macro=False, target=2.4, gen=6,
        refs=["slip", "open"], hardware=False, person="hands",
        shot="a close view inside the open weekend bag, a man's hand sliding a navy passport "
             "and a worn paperback down into the wide matching caramel leather slip pocket "
             "against the interior wall, the smooth caramel tan leather lining filling most "
             "of the frame",
        scale="His hand looks small against the interior wall, and the slip pocket runs wider "
              "than his outstretched hand.",
        motion="His hand slides the passport and the paperback down into the caramel leather "
               "slip pocket, pats them flat, and withdraws. The bag and the pocket do not "
               "change shape. Nothing opens or closes. Handheld, almost still.",
    ),
    dict(
        id="S07", act="organization", state="open", macro=False, target=2.4, gen=6,
        refs=["open", "slip"], hardware=False, person="hands",
        shot="a man's flat palm pressing down on the packed contents inside the open weekend "
             "bag, the bag full of folded shirts, rolled tees and the charcoal dopp kit, the "
             "smooth caramel tan leather interior visible at the edges, photographed from the "
             "front and slightly above",
        scale="His flat palm spans only a fraction of the packed opening, and the packed "
              "contents fill a genuinely large volume.",
        motion="His flat palm presses down firmly on the packed clothes, holds for a moment, "
               "then lifts away and out of the top of the frame. The clothes compress slightly "
               "and stay down. The bag body does not slump or change shape. The folded back "
               "flap stays one single piece behind the mouth. Nothing opens or closes.",
    ),
    dict(
        id="S08", act="closure", state="closed", macro=False, target=2.4, gen=6,
        refs=["closed", "macro"], hardware=True, person="none",
        shot="the weekend bag now closed and packed full, standing on the dark walnut bench "
             "at the foot of the bed, photographed straight on from the front, the flap down "
             "over the front with its gold oval plate resting over the gold turn post, the two "
             "cognac belt straps hanging loose down the sides with their gold end plates",
        scale="The bag fills the width of the walnut bench, wider than it is tall, with a "
              "visibly deep gusset.",
        motion="A slow gentle push in toward the front closure of the bag. The bag is "
               "completely still. Nothing opens, unfastens, twists or moves. No hands enter "
               "the frame. The hardware holds its exact shape throughout.",
    ),
    dict(
        id="S09", act="craft", state="closed", macro=True, target=2.2, gen=6,
        refs=["macro", "closed"], hardware=True, person="none",
        shot="an extreme close view of the front centre of the closed weekend bag, filling the "
             "frame: the small gold turn post with its round knurled mushroom shaped head "
             "standing on the cognac leather band, and the flap's centre tab resting over it "
             "so the gold post head shows through the shaped keyhole cutout in the polished "
             "gold oval plate",
        scale="The hardware fills the frame at macro magnification, every stitch around the "
              "flap edge individually visible.",
        motion="An extremely slow push in on the gold turn post and oval plate. Absolutely "
               "nothing else moves. The hardware does not change shape, does not rotate, does "
               "not turn into a buckle or a padlock, and grows no engraving, lettering or "
               "stamp of any kind.",
    ),
    dict(
        id="S10", act="craft", state="closed", macro=True, target=2.2, gen=6,
        refs=["macro", "side"], hardware=True, person="none",
        shot="an extreme close view of the right side of the closed weekend bag's front, "
             "filling the frame: one cognac leather belt strap coming over the top from the "
             "back, its flat gold rounded rectangular end plate with an oblong slot and small "
             "dome rivets hanging beside the flat vertical gold staple that stands on the "
             "cognac leather band",
        scale="The strap and its gold end plate fill the frame at macro magnification, the "
              "grain of the leather and the edge paint clearly visible.",
        motion="An extremely slow drift to the right across the strap and its gold end plate. "
               "Nothing fastens, unfastens or hooks. The gold plate does not change shape, "
               "does not become a buckle, and grows no engraving, lettering or brand stamp.",
    ),
    dict(
        id="S11", act="craft", state="closed", macro=True, target=2.4, gen=6,
        refs=["scale", "closed"], hardware=False, person="none",
        shot="an extreme close view of the cognac leather upper band of the closed weekend bag "
             "where a rolled leather top handle meets its teardrop shaped stitched base. The "
             "teardrop stitched handle base is unobstructed and fills the centre of the frame, "
             "with the rolled leather handle tube standing proud of the surface and entering it, "
             "the contrast stitching around the teardrop and the dark brown edge paint clearly "
             "visible. The small cognac leather key bell hangs clear to one side and does not "
             "cross or cover the teardrop base. The cream ivory woven canvas begins at the "
             "bottom edge of frame",
        scale="Only a few inches of the bag are in frame at macro magnification, individual "
              "canvas fibres and stitch holes visible.",
        motion="An extremely slow drift down and to the left across the handle base, the "
               "stitching and the key bell. Nothing else moves. The handle stays a smooth "
               "simple leather tube, never becomes braided or woven, and no lettering, "
               "engraving or logo appears anywhere.",
    ),
    dict(
        id="S12", act="payoff", state="closed", macro=False, target=2.8, gen=6,
        refs=["closed", "scale"], hardware=True, person="hands",
        shot="a man's TWO flat hands, palms down and side by side, pressing down firmly on the "
             "top of the closed packed weekend bag where it stands on the dark walnut bench at "
             "the foot of the bed, photographed from the front and slightly above, the flap down "
             "and the belt straps hanging. Both forearms enter the frame from the TOP edge only "
             "and hang straight down to the hands. Neither arm crosses in front of the bag, and "
             "the whole front face of the bag stays visible and unobstructed",
        scale="Both his flat palms together cover only the middle third of the bag's top, the bag "
              "extending well beyond his hands on both sides.",
        motion="His two flat hands press down firmly on the top of the bag, hold, then lift "
               "away and out of the top of the frame. The bag does not slump, buckle or "
               "collapse: it holds its shape exactly. The flap stays down and one single "
               "piece, the belt straps stay hanging loose. Nothing opens or unfastens.",
    ),
    # --- 2026-08-09 rebuild of the packing stretch -------------------------
    # Brooks: five near-identical packing wides in slots 3-7. The redirect kept the
    # reference's beat COUNT but not its beat VARIETY, because our bag has one
    # compartment so four different reference beats all collapsed into "hands putting
    # something in an open bag". Exactly ONE packing scene survives (S05); the rest of
    # the stretch is re-derived as visually distinct shots of the same bag in the same room.
    dict(
        id="S14", act="capacity", state="closed", macro=False, target=1.1, gen=6,
        refs=["closed"], hardware=True, person="none",
        shot="looking straight down at the charcoal grey wool throw at the foot of the bed, "
             "where three days of clothes are laid out in a neat row beside the CLOSED weekend "
             "bag: a folded white oxford shirt, a folded navy crewneck sweater, three tightly "
             "rolled white tee shirts, a pair of dark brown leather shoes and a charcoal canvas "
             "dopp kit. The bag lies closed on its back beside them, flap down",
        scale="The bag is clearly longer than the folded shirts beside it and takes up more of "
              "the throw than all the clothes put together.",
        motion="A slow gentle drift down across the laid out clothes and the closed bag. "
               "Nothing is picked up, moved or packed. No hands enter the frame. The bag stays "
               "closed and completely still.",
    ),
    dict(
        id="S15", act="capacity", state="open", macro=False, target=1.3, gen=6,
        refs=["open", "slip"], hardware=False, person="none",
        shot="the weekend bag seen from its SIDE and slightly behind, open and packed full, "
             "standing on the dark walnut bench at the foot of the bed, so the deep side gusset "
             "runs across the frame and the packed contents sit level with the mouth. The folded "
             "back flap leans back behind the opening on the far side",
        scale="The side gusset is deep, a full seven inches front to back, and the bag stands as "
              "tall on the bench as a piece of carry on luggage.",
        motion="A slow gentle drift along the side of the bag from front to back. The bag is "
               "completely still, nothing is added or removed, no hands enter the frame, and the "
               "folded back flap never moves or changes shape.",
    ),
    dict(
        id="S16", act="closure", state="closed", macro=False, target=1.4, gen=6,
        refs=["closed", "macro"], hardware=True, person="hands",
        shot="a man's open hand resting flat and still on the top of the CLOSED packed weekend "
             "bag, palm down on the smooth cognac leather flap where it folds over the top edge, "
             "photographed from a high angle just behind and above the bag so the flap and the "
             "top of the front band fill most of the frame",
        scale="His hand covers only a small part of the flap, the bag extending well beyond it "
              "on both sides.",
        motion="His hand rests on the flap and stays there, with only the faintest settling "
               "movement of the fingers. The camera drifts in very slightly. Nothing opens, "
               "unfastens, lifts or changes. The flap stays down and one single piece.",
    ),
    dict(
        id="S13", act="exit", state="closed", macro=False, target=3.2, gen=7,
        refs=["closed", "creator"], hardware=False, person="full",
        shot="a wide view of the whole hotel room, the man walking from left to right past the "
             "foot of the low walnut platform bed toward the doorway, carrying the closed "
             "weekend bag by both rolled leather top handles in his right hand with his arm "
             "straight down at his side, seen from behind and slightly to the side",
        scale="The bag hangs from his fist and reaches from his hip down toward his knee, "
              "clearly a full sized piece of luggage rather than a handbag.",
        # 2026-08-09: the pan-follow version read as AI. He appeared to drift backward into
        # the room while his gait marched in place, because the camera pan slid the background
        # past him faster than he travelled. Fixed by LOCKING THE CAMERA and giving him a
        # bounded, unambiguous exit: he simply walks away from us and leaves the frame.
        motion="The camera is completely locked off and does not pan, tilt or move at any "
               "point. He walks steadily AWAY from the camera, directly toward the open "
               "doorway, getting smaller in the frame with every step, and exits through the "
               "doorway so the room is left empty. He only ever moves away from the camera and "
               "never moves back toward it, never reverses, never walks on the spot. The bag "
               "hangs from his right hand at his side the whole time and never goes onto his "
               "shoulder. Nothing on the bag opens, unfastens or changes.",
    ),
]


def build_prompt(s):
    """Assemble the full-density i2i prompt for one scene."""
    person = {"hands": HANDS, "full": FULL_BODY, "none": "No people are in the frame at all."}[s["person"]]
    parts = [
        PREAMBLE + s["shot"] + ".",
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
          f"{sum(1 for s in SCENES if s['macro'])} macros, "
          f"{sum(1 for s in SCENES if s['state']=='open')} open-bag")
    if len(sys.argv) > 1:
        print("\n" + "=" * 70)
        print(build_prompt(scene_by_id(sys.argv[1])))
