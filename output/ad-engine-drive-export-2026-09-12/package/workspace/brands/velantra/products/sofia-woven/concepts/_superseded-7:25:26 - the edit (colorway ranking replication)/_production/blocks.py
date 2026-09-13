"""VEL-SOFIA-EDIT-01 — locked prompt blocks + shot table.

Single source of truth for every string that goes into a kie.ai call.
Read alongside VEL-SOFIA-EDIT-01-seedance-prompts.md (human-readable twin).
"""

# ---------------------------------------------------------------- colorways
# Straw body is NATURAL TAN in every colorway. The colorway names the LEATHER.
# Belt geometry differs per colorway and must match that colorway's own hero.
COLORWAYS = {
    "cream": {
        "leather": "ivory cream",
        "belts": "two ivory cream leather belt straps crossed on the front in a symmetric X",
        "hero": "https://cdn.shopify.com/s/files/1/0627/4092/2433/files/shot1_handheld_front_7f945c34-2d10-4639-98e0-a7387259f43b.png",
    },
    "caban-black": {
        "leather": "black",
        "belts": ("two black leather belt straps on the front, one running level and the second "
                  "angling down across it, exactly as in the reference image"),
        "hero": "https://cdn.shopify.com/s/files/1/0627/4092/2433/files/black-tote-1_1800fa94-c358-447a-90a0-2f955d5b7695.jpg",
    },
    "caramel": {
        "leather": "warm tan caramel",
        "belts": "two warm tan caramel leather belt straps crossed on the front in a symmetric X",
        "hero": "https://cdn.shopify.com/s/files/1/0627/4092/2433/files/shot1_handheld_front_0158b8ee-96cd-49da-8120-df74d5cadd50.png",
    },
    "light-chocolate": {
        "leather": "medium chocolate brown",
        "belts": "two medium chocolate brown leather belt straps crossed on the front in a symmetric X",
        "hero": "https://cdn.shopify.com/s/files/1/0627/4092/2433/files/shot1_handheld_front_f0b4b773-6412-4774-bd69-ce6748fffdfd.png",
    },
    "lightning-orange": {
        "leather": "bright orange",
        "belts": "two bright orange leather belt straps crossed on the front in a symmetric X",
        "hero": "https://cdn.shopify.com/s/files/1/0627/4092/2433/files/shot1_handheld_front_e0dbe9b0-22b0-484c-992d-f7841eee11ab.png",
    },
    "lady-pink": {
        "leather": "soft rose pink",
        "belts": "two soft rose pink leather belt straps crossed on the front in a symmetric X",
        "hero": "https://cdn.shopify.com/s/files/1/0627/4092/2433/files/shot1_handheld_front_b56b0a6d-0d23-4c13-b77a-b32b023a190a.png",
    },
}

# ---------------------------------------------------------------- locks
CREATOR = ("The creator stays the exact same person the whole time: woman, 47 years old, chin length "
           "dark brown bob tucked behind her ears, deep brown eyes, medium deep warm skin tone, small "
           "pearl stud earrings, wearing an ivory cashmere crewneck sweater.")

SCENE = ("Scene lock: copy the exact left right layout of the start frame into every frame. Doorway to a "
         "dark hallway on the LEFT of frame, a small framed photograph on the wall at the far LEFT, a round "
         "rattan mirror on the RIGHT of frame with a window and ocean visible through it, white flowering "
         "branches in a vase on the RIGHT below the mirror, cream painted walls, warm daylight from the "
         "RIGHT. Do not mirror or flip the scene.")

CAMERA = ("Camera lock: locked off and static, no push in, no zoom, no pan. The creator stays the same size "
          "in frame.")

FRAMING = ("Vertical 9:16 raw iPhone photo shot at chest height about 3.5 feet away, medium close: her head "
           "fills the upper half of frame with clear empty space at chest level.")


def product_lock(cw):
    c = COLORWAYS[cw]
    return (
        f"The bag is the exact Velantra Sofia woven tote from the reference image and every colour matches "
        f"that reference image exactly: a structured hand woven tote with a NATURAL TAN straw body, tightly "
        f"woven straw with braided cross stitch trim along the edges, and smooth {c['leather']} leather "
        f"elements. A {c['leather']} leather flap folds over the top of the bag from the back: the flap is "
        f"ONE single seamless piece of leather, its front lower edge cut into the silhouette of a wide center "
        f"panel with 2 squared outer tabs, the leather fully continuous and unbroken between and above these "
        f"shapes, with exactly 2 narrow slots through which the handles pass, two rolled {c['leather']} "
        f"leather top handles, {c['belts']}, white contrast stitching on all leather edges, no metal hardware, "
        f"no logos. The leather flap, tabs and belt straps exist ONLY on the FRONT face of the bag, the back "
        f"face is plain woven straw, no duplicated front detailing on any other face. The bag has ONLY the two "
        f"rolled top handles, it has no shoulder strap and no crossbody strap of any kind, never add one.")


CLOSED_EMPTY = (
    "The flap stays ONE single seamless sheet folded all the way over, lying completely flat and fully closed "
    "for the entire clip: no gap, seam or split ever opens anywhere in it, nothing behind it ever shows through "
    "it, and its cut edge shapes never separate into pieces. The flap never lifts, never stands up, never "
    "splits. The bag is completely empty and closed the whole clip, no food, no flowers, no objects in or near "
    "it, and no hand ever touches or works the flap or the belt straps.")

PROPORTION = (
    "Bag proportions stay exactly as in the reference image: the body is wider than it is tall, width to height "
    "about 1.18 to 1, widest at the base with a gentle inward taper and soft straw side wings. Never stretch it "
    "taller or pinch the shoulders.")


def colour_strap_lock(cw):
    c = COLORWAYS[cw]
    belts = c['belts'].replace("two ", "", 1)
    return (f"Colour lock: the leather is {c['leather']} exactly as in the reference image, never grey, never "
            f"taupe, never washed out. Strap lock: EXACTLY 2 belt straps, {belts}, never a lattice, never a "
            f"third strap.")


NEVER = ("Never: no metal hardware of any kind, no buckles, no turnlocks, no grommets, no zippers, no rivets. "
         "No logos, no text, no lettering anywhere. No shoulder strap or crossbody strap added. No third belt "
         "strap, no lattice of straps. No flap lifting, splitting, standing up or opening. No contents in the "
         "bag. No mirroring or flipping of the scene. No other people. No music. No camera movement. No cuts.")

# No-product clips must not name bag parts at all — naming them invites one into frame.
NEVER_NO_PRODUCT = ("Never: no bag, no handbag, no tote and no object of any kind in her hands or anywhere in "
                    "frame. No logos, no text, no lettering anywhere. No mirroring or flipping of the scene. "
                    "No other people. No music. No camera movement. No cuts.")

FOOTER = ("Ambient room tone. No cuts. No zooms. No transitions. Raw iPhone footage, expressive natural ugc "
          "movements, UGC aesthetic. Vertical 9:16. ONE CONTINUOUS SHOT. Expressive natural intonation, no "
          "monotone. Energy holds through the final word, no trailing off, no fading to flat.")

VOICE = ("She says in a polished warm female voice, late 40s, quietly enthusiastic, animated like she is "
         "showing a friend her actual closet")

# ---------------------------------------------------------------- keyframes
# Every product keyframe is i2i: [camille-ref, colorway-hero] -> GPT Image 2.
KEYFRAMES = [
    ("EDIT-K00-camille-wide", None,
     "She stands in her coastal home entryway looking directly at the camera, both hands open and empty at "
     "chest height, warm relaxed expression. Her hands are empty and no bag or object is anywhere in frame."),
    ("EDIT-K01-cream-hold", "cream",
     "She stands in her coastal home entryway holding the woven tote up at chest height by both rolled top "
     "handles, one in each hand, the front of the bag square to the camera, looking at the camera."),
    # QA fix 2026-07-25: v1 lost a belt strap and ran the bag off the RIGHT frame edge. Squared
    # up, pulled fully into frame, and the touching hand moved to the woven panel BELOW the
    # belts so no hand goes near the closure.
    ("EDIT-K02-cream-macro", "cream",
     "She stands in her coastal home entryway holding the woven tote up at chest height, her left hand on the "
     "rolled top handles and her right hand resting flat against the woven straw panel LOW on the front of the "
     "bag, well below the crossed belt straps, the front of the bag square to the camera and sitting in the "
     "lower CENTRE of frame with clear empty margin on both sides, the whole bag fully visible and never "
     "touching or crossing any edge of the frame, looking down at the bag. Neither hand ever touches the "
     "leather flap or the belt straps."),
    ("EDIT-K03-black-hold", "caban-black",
     "She stands in her coastal home entryway holding the woven tote up at chest height, turned to a gentle "
     "three quarter angle so the front and one side wing are both visible, looking at the camera."),
    # QA fix 2026-07-25: v1 put her index finger on the flap tab. Hands near the closure are
    # the exact trigger for the closure-interaction failure, so both hands stay on the handles
    # and the stitching is sold by framing the bag closer instead.
    ("EDIT-K04-black-stitch", "caban-black",
     "She stands in her coastal home entryway holding the woven tote up close to the camera at chest height by "
     "both rolled top handles, one hand on each handle, the front of the bag square to the camera and filling "
     "the lower half of frame so the white contrast stitching along the leather edges is clearly readable, "
     "looking down at the bag with a pleased expression. Both her hands stay on the rolled handles and neither "
     "hand ever touches the leather flap or the belt straps."),
    ("EDIT-K05-caramel-hold", "caramel",
     "She stands in her coastal home entryway holding the woven tote up at chest height by both rolled top "
     "handles, one in each hand, the front of the bag square to the camera, warm smile, looking at the camera."),
    ("EDIT-K06-chocolate-hold", "light-chocolate",
     "She stands in her coastal home entryway holding the woven tote up at chest height by both rolled top "
     "handles, one in each hand, the front of the bag square to the camera, looking at the camera."),
    ("EDIT-K07-orange-hold", "lightning-orange",
     "She stands in her coastal home entryway holding the woven tote up at chest height by both rolled top "
     "handles, one in each hand, the front of the bag square to the camera, eyebrows raised, looking at the "
     "camera."),
    ("EDIT-K08-pink-hold", "lady-pink",
     "She stands in her coastal home entryway holding the woven tote up at chest height by both rolled top "
     "handles, one in each hand, the front of the bag square to the camera, a soft apologetic expression, "
     "looking at the camera."),
    # QA fix 2026-07-25: v1 ran the bag off the LEFT frame edge, so proportion could not be
    # verified. Pulled in with margin on all sides and squared up to camera.
    ("EDIT-K09-caramel-shoulder", "caramel",
     "She stands in her coastal home entryway with the woven tote hanging from both rolled top handles at her "
     "shoulder, the bag sitting in the lower CENTRE of frame with clear empty margin on both its left and its "
     "right, the whole bag fully visible and never touching or crossing any edge of the frame, the front of the "
     "bag square to the camera, her hand resting on the rolled handles, warm settled smile, looking at the "
     "camera."),
    ("EDIT-K10-caramel-final", "caramel",
     "She stands in her coastal home entryway holding the woven tote up at chest height with both hands on the "
     "rolled top handles, the front of the bag square to the camera, bright open expression, looking directly "
     "at the camera."),
]


def image_prompt(cw, blocking):
    parts = [blocking, FRAMING, CREATOR, SCENE]
    if cw:
        parts += [product_lock(cw), CLOSED_EMPTY, PROPORTION, colour_strap_lock(cw), NEVER]
    else:
        parts.append(NEVER_NO_PRODUCT)
    return " ".join(parts)


# ---------------------------------------------------------------- shots
# duration sized to line length per the ASKME learnings: <=7w -> 4s, <=10w -> 5s, else 6s
SHOTS = [
    ("S01", 5, "EDIT-K00-camille-wide", None,
     "Natural and realistic arm movements, both hands open at chest height, small shrug on the words every "
     "single, half smile, looks directly at the lens the whole time.",
     "bright and brisk",
     "Okay so, I own this bag in every single color."),
    ("S02", 5, "EDIT-K00-camille-wide", None,
     "Natural and realistic arm movements, right index finger taps downward twice on the words save this, pace "
     "picks up, eyebrows lift, looks directly at the lens the whole time.",
     "bright and brisk",
     "Save this, I am ranking all of them for you."),
    ("S03", 6, "EDIT-K01-cream-hold", "cream",
     "Natural and realistic arm movements, she holds the bag up at chest height by both rolled handles, right "
     "thumb presses into the woven straw on the words tight and dense, looks between the bag and the lens.",
     "warmth lifting, indulgent",
     "Starting with cream. Hand woven, so the straw feels tight and dense."),
    ("S04", 6, "EDIT-K02-cream-macro", "cream",
     "Natural and realistic arm movements, her fingertips travel slowly across the woven straw, eyes flick up "
     "to the lens on the word welcome, small laugh.",
     "a smile in it",
     "That one is a hundred and nineteen dollars, so you are welcome."),
    ("S05", 6, "EDIT-K03-black-hold", "caban-black",
     "Natural and realistic arm movements, she turns the bag slightly to a three quarter angle and holds it "
     "there, chin lifts on the word dinner, looks directly at the lens.",
     "warm and a little pleased with herself",
     "Black leather on natural straw takes the whole thing into dinner."),
    ("S06", 6, "EDIT-K04-black-stitch", "caban-black",
     # QA fix 2026-07-25: no hand goes near the flap. She tips the bag toward the lens instead.
     "Natural and realistic arm movements, both hands stay on the rolled top handles and she tips the bag "
     "gently toward the lens so the stitching catches the light, voice drops slightly on the numbers, small nod.",
     "appreciative",
     "It fits so much, and the stitching, 10 out of 10."),
    ("S07", 5, "EDIT-K05-caramel-hold", "caramel",
     "Natural and realistic arm movements, she holds the bag high at chest height, briefly squeezes both "
     "rolled handles together, warm laugh on the words I love her, looks directly at the lens.",
     "affectionate",
     "You have all seen this caramel one. I love her."),
    ("S08", 5, "EDIT-K06-chocolate-hold", "light-chocolate",
     "Natural and realistic arm movements, she lifts the bag a little higher in a small presentational move on "
     "the words little sister, then holds it steady, looks between the bag and the lens.",
     "playful",
     "But meet her little sister. Same weave, deeper leather."),
    ("S09", 5, "EDIT-K07-orange-hold", "lightning-orange",
     "Natural and realistic arm movements, head tilts, eyebrows lift, energy climbs, she holds the bag steady "
     "at chest height and looks directly at the lens.",
     "energy climbing",
     "There is something about orange in July that gets me."),
    ("S10", 6, "EDIT-K07-orange-hold", "lightning-orange",
     "Natural and realistic arm movements, her free hand presses firmly against the woven side wall of the bag "
     "and it does not give, small satisfied nod, looks directly at the lens.",
     "certain",
     "It holds its shape all day. Mine has never gone soft."),
    ("S11", 6, "EDIT-K08-pink-hold", "lady-pink",
     "Natural and realistic arm movements, a small wince on the words sold out, her free hand presses flat "
     "against her chest, genuinely apologetic, looks directly at the lens.",
     "a touch quieter but fully present, genuinely sorry",
     "I could not not include this one. Pink is sold out."),
    ("S12", 5, "EDIT-K08-pink-hold", "lady-pink",
     "Natural and realistic arm movements, quick shake of the head, half laugh of disbelief, she keeps the bag "
     "held steady at chest height, looks directly at the lens.",
     "half laughing",
     "I am sorry, it went in about a week."),
    ("S13", 5, "EDIT-K09-caramel-shoulder", "caramel",
     # Matches K09 v2, which resolved as a chest hold rather than a shoulder carry.
     "Natural and realistic arm movements, she holds the bag up at chest height by both rolled handles and "
     "gives the handles one small settling squeeze on the words every time, looks directly at the lens.",
     "settled and certain",
     "But the one I reach for is caramel, every time."),
    ("S14", 6, "EDIT-K10-caramel-final", "caramel",
     "Natural and realistic arm movements, her free hand counts lightly in the air on the words browns and "
     "blacks, the bag stays steady at chest height, looks directly at the lens.",
     "settled and certain",
     "It goes with everything. Browns, blacks, white dresses, you name it."),
    ("S15", 5, "EDIT-K10-caramel-final", "caramel",
     "Natural and realistic arm movements, she holds the bag up with both hands, direct to the lens, bright "
     "and open.",
     "back to bright and brisk",
     "Every color is a hundred and nineteen dollars."),
    ("S16", 6, "EDIT-K10-caramel-final", "caramel",
     "Natural and realistic arm movements, eyebrows up, one small nod on the last word, the bag stays steady "
     "at chest height, looks directly at the lens.",
     "bright with a nudge in it",
     "Tell me your favorite, and go before yours goes like pink."),
]


def video_prompt(sid, dur, keyframe, cw, movement, colour, line):
    parts = [movement, f"{VOICE}, {colour}:", f'"{line}"']
    if sid == "S01":
        parts.append("Voice: warm late 40s American, polished, quietly enthusiastic.")
    parts += [CREATOR, SCENE, CAMERA]
    if cw:
        parts += [product_lock(cw), CLOSED_EMPTY, PROPORTION, colour_strap_lock(cw), NEVER]
        tail = ("PRODUCT ON SHOULDER, hanging from the two rolled top handles, held still and fully visible."
                if sid == "S13" else "PRODUCT IN HAND, held still and fully visible.")
    else:
        parts.append(NEVER_NO_PRODUCT)
        tail = "NO PRODUCT IN FRAME, her hands are empty."
    parts += [FOOTER, tail]
    return " ".join(parts)
