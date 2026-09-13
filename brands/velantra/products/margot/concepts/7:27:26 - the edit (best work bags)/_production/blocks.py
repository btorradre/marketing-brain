"""VEL-MARGOT-EDIT-01 — locked prompt blocks + shot table.

The work-bag comparison version of the Edit format (VEL-SOFIA-EDIT-02 clone).
She tests 5 work bags and the Margot wins.

Four of the five are NOT Velantra products: generic bags matching the four
archetypes in our customer's consideration set (see research/), no logos,
deliberately different silhouettes so none of them reads as a Margot. They are
never named as products and never priced — quoting a price for a bag that does
not exist would be inventing a fact, and it makes $99.99 the only number in the ad.

Taste anchors ARE named exactly as the Sofia Edit did ("it is giving Marc
Jacobs", "it is giving The Row") — the reference never holds a house's bag and
neither do we. Hermes and "Birkin" stay out, standing rule.

Every limitation is a WORK limitation: slumps, heavy, reads luggage, too
precious to daily. She never calls a bag bad — she authors a scorecard only
the Margot can pass.
"""

# ---------------------------------------------------------------- the Margot
MARGOT_HERO = ("https://cdn.shopify.com/s/files/1/0627/4092/2433/files/"
               "margot-burgundy-hero.jpg?v=1784826552")

MARGOT_LOCK = (
    "The bag is the exact Velantra Margot leather tote from the bag reference image and every colour matches "
    "that reference image exactly: a softly structured open top tote in deep burgundy wine leather with a fine "
    "embossed swirling grain texture across every panel, never plain smooth leather and never a classic round "
    "pebble grain. The body is clearly wider than it is tall, the top edge wider than the base with a gentle "
    "inward taper, and soft folded accordion gussets on each side. Two slim flat burgundy leather top handles. "
    "A single horizontal burgundy leather belt strap runs across the upper front through one small polished "
    "silver rectangular keeper at each side, and its two strap ends angle down toward the centre in a shallow "
    "open V, each end finished with a polished silver slotted clasp plate, both loose ends hanging free and NOT "
    "fastened. Centred on the front panel above the V sits one small square polished silver turn lock plate "
    "with a small vertical toggle. Four small silver feet under the base. The top is open with no flap and no "
    "top zipper. The bag has ONLY the two flat top handles, it has no shoulder strap and no crossbody strap of "
    "any kind, never add one. No logos, no text anywhere on it.")

MARGOT_STILL = (
    "The bag holds its structured shape for the entire clip and never slumps, sags or collapses. The belt "
    "strap stays exactly as in the bag reference image with both strap ends hanging loose in their shallow "
    "open V, and no hand ever fastens, opens or works the belt strap or the turn lock. The bag stays empty, "
    "nothing is placed inside it and nothing pokes above its top edge. The bag is held still and steady, it is "
    "never shaken, swung, flipped or turned over.")

MARGOT_PROPORTION = (
    "Bag proportions stay exactly as in the bag reference image: the body is clearly wider than it is tall, "
    "width to height about 1.5 to 1, the top edge wider than the base with a gentle inward taper and soft "
    "accordion side gussets. Never stretch it taller than it is wide, never square it into a box.")

MARGOT_COLOUR = (
    "Colour lock: the leather is deep burgundy wine exactly as in the bag reference image, never brown, never "
    "black, never bright red, never washed out, and the fine embossed swirling grain stays visible in every "
    "frame. Hardware lock: ALL hardware is polished silver, never gold, never brass. Belt lock: EXACTLY 1 "
    "horizontal belt strap, EXACTLY 2 silver slotted clasp plate ends hanging in an open V, EXACTLY 1 small "
    "square silver turn lock plate, never a second belt, never extra plates or locks.")

# ---------------------------------------------------------------- the other four
# Generic, unbranded, one per consideration-set archetype (see research/).
# None of them carries a Margot signature: no horizontal belt strap, no turn
# lock, no slotted clasp plates, no embossed swirling grain, or the winner
# stops reading as a category of one.
OTHERS = {
    "black-nylon": (
        "a soft black nylon commuter tote with a matte fabric sheen, two thin flat black nylon shoulder "
        "straps, an unstructured slouching body that visibly sags and folds when held, plain unadorned front, "
        "no belt strap, no turn lock, no clasp plates, no metal hardware, no logos, no text, no leather "
        "texture anywhere on it"),
    "tan-oversized": (
        "an oversized slouchy smooth tan leather tote with a wide open top, two wide flat tan leather "
        "handles, a deep roomy unstructured body, smooth plain leather with no embossed texture, plain "
        "unadorned front, no belt strap, no turn lock, no clasp plates, no metal hardware, no logos, no text, "
        "no fabric anywhere on it"),
    "grey-organizer": (
        "a light grey padded nylon organizer tote with softly quilted puffy panels, a boxy structured body, "
        "two exterior zip pockets with small matching grey zips, two wide flat grey fabric straps, no belt "
        "strap, no turn lock, no clasp plates, no polished silver plates, no logos, no text, no leather "
        "anywhere on it"),
    "ivory-minimal": (
        "a tall minimalist ivory smooth calf leather tote in a north south shape, clearly taller than it is "
        "wide, two long thin ivory leather straps, a completely clean unadorned front, smooth plain leather "
        "with no embossed texture, softly structured, no belt strap, no turn lock, no clasp plates, no metal "
        "hardware, no logos, no text"),
}

# ---------------------------------------------------------------- shared locks
CREATOR = ("The creator stays the exact same person the whole time: woman, 47 years old, chin length "
           "dark brown bob tucked behind her ears, deep brown eyes, medium deep warm skin tone, small "
           "pearl stud earrings, wearing a light camel knit blazer over an ivory crew neck top and dark "
           "blue jeans.")

SCENE = ("Scene lock: copy the exact left right layout of the start frame into every frame. A tall dark wood "
         "bookshelf with neatly arranged books on the LEFT of frame, a small framed abstract print on the "
         "wall at the far LEFT, a slim pale oak console table with a small brass lamp on the RIGHT of frame "
         "below a large window, a small potted olive tree on the RIGHT beside the console, warm white "
         "painted walls, soft daylight from the RIGHT. The window shows green garden trees and soft sky "
         "ONLY, never the ocean, no sea, no beach, no water visible anywhere outside. There is NO mirror in "
         "the room, no round mirror, no rattan mirror on any wall. Do not mirror or flip the scene.")

CAMERA = ("Camera lock: locked off and static, no push in, no zoom, no pan. The creator stays the same size "
          "in frame.")

FRAMING = ("Vertical 9:16 raw iPhone photo shot at chest height about 3.5 feet away, medium close: her head "
           "fills the upper half of frame with clear empty space at chest level.")

NEVER_MARGOT = ("Never: no gold or brass hardware anywhere. No logos, no text, no lettering anywhere. No "
                "shoulder strap or crossbody strap added. No flap added over the top, the top stays open. No "
                "second belt strap, no lattice of straps, no extra clasp plates or turn locks. The belt strap "
                "never fastens itself and never disappears. The bag never slumps, collapses or changes shape. "
                "No contents in the bag. No mirroring or flipping of the scene. No other people. No music. No "
                "camera movement. No cuts.")

NEVER_OTHER = ("Never: no logos, no brand names, no text, no lettering, no monograms anywhere on the bag. No "
               "horizontal belt strap, no turn lock, no slotted clasp plates, no square silver plate, no "
               "embossed swirling grain texture. No burgundy colour anywhere. No mirroring or flipping of the "
               "scene. No other people. No music. No camera movement. No cuts.")

NEVER_NO_PRODUCT = ("Never: no bag, no handbag, no tote and no object of any kind in her hands or anywhere in "
                    "frame. No logos, no text, no lettering anywhere. No mirroring or flipping of the scene. "
                    "No other people. No music. No camera movement. No cuts.")

FOOTER = ("Ambient room tone. No cuts. No zooms. No transitions. Raw iPhone footage, expressive natural ugc "
          "movements, UGC aesthetic. Vertical 9:16. ONE CONTINUOUS SHOT. Expressive natural intonation, no "
          "monotone. Energy holds through the final word, no trailing off, no fading to flat.")

VOICE = ("She says in a polished warm female voice, late 40s, quietly enthusiastic, animated like she is "
         "showing a friend her actual closet")


def bag_lock(bag):
    """bag: None (no product) | 'margot' | a key in OTHERS."""
    if bag is None:
        return [], NEVER_NO_PRODUCT
    if bag == "margot":
        return [MARGOT_LOCK, MARGOT_STILL, MARGOT_PROPORTION, MARGOT_COLOUR], NEVER_MARGOT
    return [f"She is holding {OTHERS[bag]}. This bag is completely plain and carries no branding of any kind."], NEVER_OTHER


# ---------------------------------------------------------------- keyframes
# Margot frames are i2i from the live burgundy PDP hero (passed as a second
# reference URL). The other four are t2i from the Camille ref only — they are
# not real products, so there is nothing to anchor to.
KEYFRAMES = [
    ("EDIT1-K00-hook", None,
     "She stands in her home office entryway looking directly at the camera, both hands open and empty at "
     "chest height, warm relaxed expression. Her hands are empty and no bag or object is anywhere in frame."),
    ("EDIT1-K01-nylon-hold", "black-nylon",
     "She stands in her home office entryway holding the bag up at chest height by both thin straps, the "
     "front of the bag square to the camera, the soft body sagging slightly, sitting in the lower CENTRE of "
     "frame with clear empty margin on both sides and fully visible, looking at the camera."),
    ("EDIT1-K02-nylon-slump", "black-nylon",
     "She stands in her home office entryway with one hand under the soft bag at chest height, the body of "
     "the bag visibly folding and slumping over her fingers, fully visible with clear margin on both sides, a "
     "slightly rueful expression, looking at the bag."),
    ("EDIT1-K03-tan-hold", "tan-oversized",
     "She stands in her home office entryway holding the big bag up at chest height by both wide handles, the "
     "front square to the camera, fully visible with clear empty margin on both sides, an appreciative "
     "expression, looking at the camera."),
    ("EDIT1-K04-tan-heft", "tan-oversized",
     "She stands in her home office entryway holding the big bag at chest height with both hands hugging it "
     "from underneath, her shoulders very slightly dropped under its weight, fully visible with clear margin, "
     "a rueful half smile, looking at the bag."),
    ("EDIT1-K05-organizer-hold", "grey-organizer",
     "She stands in her home office entryway holding the boxy bag up at chest height by both wide straps, the "
     "front square to the camera showing its zip pockets, fully visible with clear empty margin on both "
     "sides, looking at the camera."),
    ("EDIT1-K06-organizer-close", "grey-organizer",
     "She stands in her home office entryway holding the boxy bag slightly closer to the camera at chest "
     "height so the quilted padded panels are clearly readable, fully visible with clear margin, an amused "
     "conceding expression, looking at the bag."),
    ("EDIT1-K07-ivory-hold", "ivory-minimal",
     "She stands in her home office entryway holding the tall bag up at chest height by both long thin "
     "straps, the front square to the camera, fully visible with clear empty margin on both sides, a hushed "
     "admiring expression, looking at the camera."),
    ("EDIT1-K08-ivory-cradle", "ivory-minimal",
     "She stands in her home office entryway cradling the tall bag carefully against her forearm at chest "
     "height like something fragile, fully visible with clear margin on both sides, a protective cautious "
     "expression, looking at the bag."),
    ("EDIT1-K09-burgundy-hold", "margot",
     "She stands in her home office entryway holding the bag up at chest height by both flat top handles, the "
     "front of the bag with its belt strap and turn lock square to the camera, sitting in the lower CENTRE of "
     "frame with clear empty margin on both sides and fully visible, a bright delighted expression, looking "
     "at the camera."),
    ("EDIT1-K10-burgundy-forearm", "margot",
     "She stands in her home office entryway carrying the bag on her right forearm: both flat top handles "
     "are looped over her right forearm, her right elbow is bent so the forearm sits horizontal at waist "
     "height, and the bag hangs directly below her forearm resting lightly against her hip, the same size as "
     "in the bag reference image, its front with the belt strap and turn lock facing the camera, fully "
     "visible in the lower CENTRE of frame with clear margin on both sides, looking at the camera."),
    ("EDIT1-K11-burgundy-final", "margot",
     "She stands in her home office entryway holding the bag up at chest height with both hands, the front of "
     "the bag with its belt strap and turn lock square to the camera, fully visible with clear empty margin "
     "on both sides, a settled certain expression, looking at the camera."),
]

MARGOT_KEYS = {"EDIT1-K09-burgundy-hold", "EDIT1-K10-burgundy-forearm", "EDIT1-K11-burgundy-final"}

REF_NOTE = ("Two reference images are provided: the FIRST is the exact creator, the SECOND is the exact bag. "
            "Match both exactly.")


def image_prompt(bag, blocking):
    locks, never = bag_lock(bag)
    parts = [blocking, FRAMING, CREATOR, SCENE]
    if bag == "margot":
        parts.insert(0, REF_NOTE)
    return " ".join(parts + locks + [never])


# ---------------------------------------------------------------- shots
# duration sized to line length at Seedance's native 1.6-2.0 words/sec
SHOTS = [
    ("S01", 6, "EDIT1-K00-hook", None,
     "Natural and realistic arm movements, both hands open at chest height, small shrug, half smile, looks "
     "directly at the lens the whole time.",
     "bright and brisk",
     "Everyone wants a work bag that looks expensive and carries everything."),
    ("S02", 5, "EDIT1-K00-hook", None,
     "Natural and realistic arm movements, right index finger taps downward twice, pace picks up, eyebrows "
     "lift, looks directly at the lens the whole time.",
     "bright and brisk",
     "Save this, I tested five and one won."),

    ("S03", 6, "EDIT1-K01-nylon-hold", "black-nylon",
     "Natural and realistic arm movements, she holds the bag up at chest height by both thin straps, a small "
     "knowing tilt of the head, looks between the bag and the lens.",
     "familiar and fond",
     "Starting with the nylon one, every woman on my commute has it."),
    ("S04", 6, "EDIT1-K02-nylon-slump", "black-nylon",
     "Natural and realistic arm movements, her hand under the bag lifts once and the soft body folds over her "
     "fingers on the word slumps, small shrug, looks at the lens.",
     "fond but honest",
     "So light and easy. But it slumps, and slump is not polished."),

    ("S05", 5, "EDIT1-K03-tan-hold", "tan-oversized",
     "Natural and realistic arm movements, she holds the big bag up by both handles, small appreciative tilt "
     "of the head, looks at the lens with a pleased expression.",
     "warmth lifting, indulgent",
     "This big leather one is giving Marc Jacobs."),
    ("S06", 6, "EDIT1-K04-tan-heft", "tan-oversized",
     "Natural and realistic arm movements, she hefts the bag once with both hands and lets her shoulders drop "
     "slightly on the word heavy, a rueful half smile, looks at the lens.",
     "affectionate but honest",
     "The leather is gorgeous. It is heavy before you even pack it."),

    ("S07", 5, "EDIT1-K05-organizer-hold", "grey-organizer",
     "Natural and realistic arm movements, she holds the boxy bag up square to the camera and taps one zip "
     "pocket once, eyebrows lift, looks at the lens.",
     "amused, a little insider",
     "The viral organizer tote. There is a pocket for everything."),
    ("S08", 6, "EDIT1-K06-organizer-close", "grey-organizer",
     "Natural and realistic arm movements, she brings the bag slightly closer to the lens then tilts her "
     "head with a conceding smile on the word luggage, looks at the lens.",
     "conceding but kind",
     "So smart for travel. In a meeting it looks like luggage."),

    ("S09", 5, "EDIT1-K07-ivory-hold", "ivory-minimal",
     "Natural and realistic arm movements, she holds the tall bag up by both thin straps and turns it a few "
     "degrees, a hushed admiring expression, looks at the lens.",
     "hushed, admiring",
     "This one is quiet luxury, it is giving The Row."),
    ("S10", 6, "EDIT1-K08-ivory-cradle", "ivory-minimal",
     "Natural and realistic arm movements, she cradles the bag carefully against her forearm, a protective "
     "wince on the word baby, small shrug, looks at the lens.",
     "protective, honest",
     "Stunning. But at that price I would baby it every day."),

    ("S11", 6, "EDIT1-K09-burgundy-hold", "margot",
     "Natural and realistic arm movements, she holds the bag up at chest height by both flat handles, energy "
     "lifts clearly on the word this, looks directly at the lens.",
     "energy climbing, this is the one",
     "And then this one. Real structure, it stands up on its own."),
    ("S12", 6, "EDIT1-K10-burgundy-forearm", "margot",
     "Natural and realistic arm movements, the bag hangs from both handles on her raised forearm, she lifts "
     "the forearm once lightly on the word light, looks directly at the lens.",
     "settled and certain",
     "My laptop fits, my planner fits, and it stays this light."),
    ("S13", 6, "EDIT1-K11-burgundy-final", "margot",
     "Natural and realistic arm movements, her free hand gestures softly outward on the words every single "
     "thing, the bag stays steady at chest height, looks directly at the lens.",
     "settled and certain",
     "And this burgundy goes with every single thing I wear to work."),
    ("S14", 5, "EDIT1-K11-burgundy-final", "margot",
     "Natural and realistic arm movements, she holds the bag up with both hands, eyes flick to the lens on "
     "the last word, small laugh.",
     "a smile in it",
     "And it is under a hundred dollars."),

    ("S15", 6, "EDIT1-K11-burgundy-final", "margot",
     "Natural and realistic arm movements, one small firm nod, the bag stays steady at chest height, looks "
     "directly at the lens.",
     "certain, no hedging",
     "That is the one that won, and it was not close."),
    ("S16", 5, "EDIT1-K09-burgundy-hold", "margot",
     "Natural and realistic arm movements, eyebrows up, open warm expression, the bag held at chest height, "
     "looks directly at the lens.",
     "bright, handing the mic over",
     "Tell me which one you would have picked."),
]


def video_prompt(sid, dur, keyframe, bag, movement, colour, line):
    locks, never = bag_lock(bag)
    parts = [movement, f"{VOICE}, {colour}:", f'"{line}"']
    if sid == "S01":
        parts.append("Voice: warm late 40s American, polished, quietly enthusiastic.")
    parts += [CREATOR, SCENE, CAMERA] + locks + [never, FOOTER]
    if bag is None:
        parts.append("NO PRODUCT IN FRAME, her hands are empty.")
    elif sid == "S12":
        parts.append("PRODUCT ON FOREARM, held still and fully visible.")
    else:
        parts.append("PRODUCT IN HAND, held still and fully visible.")
    return " ".join(parts)
