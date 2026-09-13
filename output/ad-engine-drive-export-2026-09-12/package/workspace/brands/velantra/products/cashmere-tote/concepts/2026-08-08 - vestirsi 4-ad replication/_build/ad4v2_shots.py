#!/usr/bin/env python3
"""AD4 v2 shot list: one creator, one outfit, one room, alternating
wearing-shots and her-own-hands detail shots. Ported from Vestirsi ref 4.

Stage 1 keyframes: GPT Image 2 i2i on kie (10cr each) off Blair + the bag.
Stage 2 motion:    Google Omni i2v (Gemini Interactions API, no kie credits).
"""

# Held identical in every keyframe so 13 independent generations read as one shoot.
CREATOR = (
 "The woman from the first reference image, exactly the same face, same early forties age, "
 "same voluminous golden blonde wavy hair parted off center, same blue gray eyes. "
 "Natural skin texture with visible pores and fine lines, a few flyaway hairs, never airbrushed. "
 "Her mouth is closed with her lips gently together and her jaw relaxed. She is not talking, "
 "not mid-word, not smiling widely. Calm, easy, self-assured expression."
)
WARDROBE = (
 "She wears an oversized oatmeal wool coat open over a cream ribbed knit, "
 "white wide leg trousers and black ankle boots, small gold hoop earrings, bare hands."
)
SET = (
 "A bare off-white wall behind her, pale oak floorboards, one low dark wood bench "
 "against the wall at the right of frame. The room is empty and uncluttered."
)
LIGHT = (
 "Soft daylight from a tall window out of frame at the LEFT, shadows falling gently to the "
 "right, low contrast, the wall behind her a stop darker than she is. Neutral daylight, "
 "slightly desaturated, lifted blacks."
)
LOOK = (
 "Shot on an iPhone, handheld, slightly imperfect framing, mild sensor noise, real photograph. "
 "Not a 3D render, not CGI, no plastic skin, no glossy studio product sheen, no color grading."
)
BAG = (
 "The tote from the second reference image, exactly as shown. Oatmeal brushed wool felt body, "
 "trapezoid tote wider at the top with a flat base, structured so it stands upright unaided. "
 "Exactly 2 handles, caramel leather along the upper arc and oatmeal wool down the legs, and "
 "those legs continue down the FRONT face as exactly 2 vertical wool straps. Exactly 1 caramel "
 "leather belt crosses the FRONT face behind both straps, its 2 ends curving down and outward "
 "into exactly 1 round gold disc cap each, 2 caps total and the only hardware outside. "
 "The mouth is a plain open rim of wool edge to edge. Every outer surface is blank wool and "
 "plain caramel leather, nothing printed or stamped anywhere on it."
)

# (id, start, end, kind, framing/action for the keyframe, motion for Omni)
SHOTS = [
 ("s01", 0.00,  2.74, "wear",
  "Full body, straight on, standing centered. She holds the tote by both handles down at hip height, "
  "looking at the lens.",
  "She gives the tote one small lift and settle at her hip and shifts her weight. Handheld micro sway."),

 ("s02", 2.74,  4.60, "wear",
  "Full body, three quarter angle, the tote hooked in the crook of her right elbow.",
  "She turns a few degrees toward the lens and the tote swings very slightly on her forearm."),

 ("s03", 4.60,  6.54, "wear",
  "Full body, the tote on her right shoulder, mid stride one step toward camera.",
  "She takes one slow step toward the lens, the tote riding on her shoulder. Handheld micro sway."),

 ("s04", 6.54,  7.79, "wear",
  "Full body from BEHIND, her back to camera, the tote on her right shoulder so its back face reads.",
  "She turns her head a little to the right, over her shoulder. The tote stays still on her shoulder."),

 ("s05", 7.79, 10.00, "wear",
  "Waist up. She grips the two leather handles at the top of their arc, one hand closed around each "
  "handle with the fingers fully wrapped over the leather and the thumb in front, knuckles visible. "
  "The whole weight of the tote hangs from those two fists so both handles are pulled taut and straight, and the bag hangs below her hands with a visible gap between the top rim and her fists. Her palms and forearms do not touch the body of the bag anywhere. The front face is square to the lens so the caramel belt and both gold disc caps read clearly.",
  "The tote hangs from the two leather handles held in her hands and settles, swaying a centimetre or two. Her hands stay closed on the handles for the whole clip and the handles stay taut under the weight of the bag."),

 ("s06",10.00, 12.19, "hands",
  "Close on her hands against the tote, her coat sleeve in frame at the edge. Her thumb presses into "
  "the brushed wool body.",
  "Her thumb presses slowly into the brushed wool and the fibres compress under it, then release."),

 ("s07",12.19, 14.90, "hands",
  "Close on her fingers tracing along the caramel leather belt where it curves down into one round "
  "gold disc cap, her coat sleeve at the edge of frame.",
  "Her fingertips travel slowly along the belt toward the gold disc cap. Nothing else moves."),

 ("s08",14.90, 17.95, "wear",
  "Medium wide. She is beside the low dark bench, lowering the loaded tote onto it, both hands still "
  "on the handles.",
  "She sets the tote down on the bench and lifts both hands away, and the tote stands upright on its "
  "own without slumping. Camera locked off."),

 ("s09",17.95, 20.60, "wear",
  "Waist up. She holds the tote by the rim with both hands, tipped toward the lens so the wide mouth reads. The inside is FULL and the contents fill the cavity completely: a folded cream knit packed across the whole base and the dark charcoal edge of a laptop standing against the back wall. The interior is a plain wool lining with the contents pressed against it, and there is nothing else inside it.",
  "She tips the mouth a little further toward the lens. Her hands stay on the rim and the folded knit and laptop edge stay exactly where they are, filling the inside."),

 ("s10",20.60, 23.23, "hands",
  "Close over the open tote from slightly above. A laptop is ALREADY almost entirely inside the tote, sunk down between the wool walls, with only a thin dark top edge of it showing just above the rim. No lid face, no flat panel and no corner of the laptop is visible, only that thin edge. Her two hands rest on the rim of the tote on either side. A folded cream knit is already inside beside it.",
  "Her hands press the thin exposed top edge of the laptop down until it disappears below the rim, then tuck the folded knit in beside it. The tote keeps its shape. The laptop stays hidden inside."),

 ("s11",23.23, 25.28, "hands",
  "Close on her hand closed around the caramel leather handle at the top of its arc, coat sleeve in frame.",
  "Her hand slides a few centimetres along the leather handle and settles. Nothing else moves."),

 ("s12",25.28, 27.07, "hands",
  "Very close on one round gold disc cap at the end of the caramel belt, her fingertip resting beside it.",
  "A slow drift across the gold disc cap as the light moves over it. Her fingertip stays still."),

 ("s13",27.07, 29.24, "wear",
  "Waist up, she is standing upright at full height, not crouching and not kneeling. She holds the tote up beside her at chest height with its blank front face square to the lens, and rests her flat open palm against that front face.",
  "She draws her flat palm slowly across the blank front face of the tote, left to right."),

 # 29.24-30.88 colorway plate, already built as ad4/duo-colorways.mp4

 ("s15",30.88, 35.17, "wear",
  "Full body, the tote on her shoulder, standing square to the lens with her weight on one hip.",
  "She shifts her weight and adjusts the tote on her shoulder once. Handheld micro sway."),

 ("s16",35.17, 37.68, "wear",
  "Full body wide, she is turned toward the left of frame with the tote in the crook of her elbow, "
  "about to walk out of frame.",
  "She walks out of frame to the left, the tote in the crook of her elbow. Camera holds on the empty room."),
]


def keyframe_prompt(shot):
    _id, _a, _b, kind, framing, _motion = shot
    if kind == "hands":
        who = ("Her hands only, cropped above the wrist or at the forearm, her face is not in frame. "
               + CREATOR.split(".")[0] + ". Her coat sleeve is visible at the edge of frame so it "
               "reads as the same person. Natural skin texture on the hands, short bare nails.")
    else:
        who = CREATOR
    return (f"A vertical 9:16 photograph. {framing}\n\n"
            f"WOMAN: {who}\n\nWARDROBE: {WARDROBE}\n\nROOM: {SET}\n\n"
            f"BAG: {BAG}\n\nLIGHT: {LIGHT}\n\nLOOK: {LOOK}")


def motion_prompt(shot):
    """Lean and POSITIVE.

    The heavy version of this prompt re-asserted the whole PRODUCT block plus a
    negation footer ("no other people", "no text", "no music", "no zoom...").
    Omni's input filter reads that prose, and on some frames the cumulative
    negation stack trips it: s05 and s07 came back `Input blocked` on every
    attempt (5/5 on a bounded retry) while the very same images animated fine
    from a bland prompt. Both passed first try once the negations were removed.
    The keyframe already carries the product truth, so restating it buys nothing.
    """
    _id, _a, _b, _kind, _framing, motion = shot
    return (f"Vertical 9:16 video. Animate this exact photograph, keeping every detail identical. "
            f"{motion} The bag keeps exactly the shape, colour and hardware it has in the "
            f"photograph. Shot on an iPhone, handheld, a real photograph.")


if __name__ == "__main__":
    tot = 0
    for s in SHOTS:
        tot += s[2] - s[1]
        print(f"{s[0]}  {s[1]:5.2f}-{s[2]:5.2f}  {s[2]-s[1]:4.2f}s  {s[3]:5s}  {s[4][:64]}")
    print(f"\n{len(SHOTS)} generated shots, {tot:.2f}s + 1.64s colorway plate = {tot+1.64:.2f}s")
