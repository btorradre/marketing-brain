#!/usr/bin/env python3
"""THE VIVIENNE — Vestirsi 6-format static replication. Clean plates, no text.

Six Vestirsi Meta statics supplied by Brooks (2026-08-27), replicated one to one
on composition, crop, grade and type geometry, with the Vivienne swapped in:

  V1 first-run     <- R6  still-life pair on a warm sweep, caps + subhead top third
  V2 leather-logo  <- R2  two bags leaning on a white wall over concrete, mark centre
  V3 out-the-door  <- R3  back to camera, bag on the shoulder strap, mark centre
  V4 effortless    <- R4  waist-down, wide leg denim, bag in hand, mark left / copy right
  V5 real-day      <- R5  studio still life, bag open and loaded, caps + body + attribution
  V6 quote         <- R1  torso crop, dark dress, bag on the strap, quote lower left

Plates render CLEAN. Every word is composited in compose.py so tracking, weight
and alignment are pixel correct against the measured reference geometry and the
copy stays swappable without touching a plate.

PRODUCT TRUTH
-------------
Read from `PRODUCT-TRUTH.md`, NOT from the `velantra-vivienne` skill. The skill's
identity and material blocks are stale: they still say "structured trapezoid" and
"high-gloss waxy pull-up finish with heavy natural marbling", and PRODUCT-TRUTH
§1 and §3 ban all of those words after two full image sets were rejected for
exactly them. Truth file wins, it says so itself.

The three corrections that matter here:
  1. SOFT AND SLOUCHY. The bag slumps, bows and folds. Never structured, never
     rigid, never "stands on its own".
  2. TWO LEATHER TEXTURES. Body = matte to satin with real pore grain. Band,
     flap, handles, belt straps and corner caps = smoother and more burnished.
     Never gloss, never lacquered, never wet looking.
  3. CUTOUTS ARE NOT WINDOWS. Every flap cutout, strap slot and keyhole shows
     the shadowed leather immediately behind it, never the background.

CLEAN ROOM
----------
Seeds are our OWN approved v4 gallery renders in `refs/`, never the competitor
TikTok frames in `source/tiktok/` and never the Vestirsi references. PRODUCT-TRUTH
§12 and the clean-room law both forbid competitor photography as an i2i seed for
a published asset.

The seeds are shot in the Vivienne house look (dark teal wall, wood plank, low
key). Every reference here is the opposite: bright white wall, pale concrete,
even daylight. The preamble therefore pins the seed to shape, material, colour
and hardware ONLY and explicitly releases its lighting and background.

Idempotent: skips any plate whose PNG already exists (delete it to regenerate).
"""
import json, os, time, subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
VAULT = "/Users/brooksorradre2/Documents/marketing brain"
REF_DIR = os.path.join(ROOT, "refs")
OUT = os.path.join(os.path.dirname(ROOT), "plates")
API = "https://api.kie.ai/api/v1"
UPLOAD = "https://kieai.redpandaai.co/api/file-stream-upload"

KEY = None
with open(os.path.join(VAULT, ".env")) as f:
    for line in f:
        if line.startswith("KIE_API_KEY="):
            KEY = line.split("=", 1)[1].strip()
assert KEY, "KIE_API_KEY not found"
H = {"Authorization": f"Bearer {KEY}"}


# --- COLORWAYS (PRODUCT-TRUTH.md §9) -----------------------------------------
#
# Chocolate is the hero and the only two-tone: dark chocolate body with CONTRAST
# cognac straps and trim, confirmed on Brooks's photo. The other three are tonal.

CW = {
    "Ch": dict(name="Chocolate", pre="Ch",
               body="deep dark chocolate brown",
               trim="warm mid cognac brown, a clearly lighter and warmer tone than the body",
               two_tone=True),
    "Co": dict(name="Cognac", pre="Co",
               body="warm mid cognac brown",
               trim="the same warm mid cognac brown as the body",
               two_tone=False),
    "Bl": dict(name="Black", pre="Bl",
               body="deep black",
               trim="the same deep black as the body",
               two_tone=False),
    "Ol": dict(name="Olive", pre="Ol",
               body="deep muted olive green",
               trim="the same deep muted olive green as the body",
               two_tone=False),
}


# --- PREAMBLE (velantra-vivienne skill, mandatory at the TOP of every prompt) --
#
# Extended past the skill's wording because our seeds are house-look frames and
# every one of these six references is a bright daylight set. Without the second
# sentence the dark teal wall and the warm rake come through into the plate.

PREAMBLE = (
    "Use the attached photographs ONLY as the reference for the bag's shape, proportions, "
    "materials, colours, stitching and hardware. Do NOT copy their lighting, their background, "
    "their dark green wall, their wooden surface, their warm amber grade, their clean edges or "
    "their polished product photo look. The scene, the light and the colour grade are described "
    "below and they replace the reference's completely. "
)


def identity(c):
    """PRODUCT-TRUTH §1, §4, §5, §6. Soft and slouchy, two leather textures."""
    return (
        f"a LARGE, SOFT, SLOUCHY leather top handle bag with a trapezoid outline that is wider at the "
        f"base than at the mouth. The body is {c['body']} leather with visible natural pore and pebble "
        f"grain and a MATTE to SATIN sheen. The bag is UNSTRUCTURED and carries no internal frame: its "
        f"front panel visibly bows and wrinkles, its sides pinch and fold inward, its base spreads under "
        f"its own weight and its mouth softens rather than holding a crisp rectangle. A single one piece "
        f"leather flap folds all the way over the top from the back panel forward, with a notched "
        f"scalloped front edge, and a braided whip stitched leather trim runs along the top edge of the "
        f"closure band beneath it. Two short rolled leather top handles rise from the band on round "
        f"brass rivets, and one detachable long leather shoulder strap clips to small brass rings at the "
        f"sides. The flap, the closure band, the rolled handles, the belt straps and the corner caps are "
        f"{c['trim']} leather in a smoother and more burnished finish than the grainy body panels. "
        f"Reinforced curved leather corner caps are saddle stitched at all four bottom corners, rolled "
        f"leather piping runs down the side seams and around the base, each side gusset carries one "
        f"vertical leather keeper, and small brass feet sit on the base. All hardware is warm aged brass "
        f"gold, never chrome and never silver. There are no logos, no stamped lettering and no plaques "
        f"anywhere on the bag."
    )


# 🔒 VERBATIM CLOSURE HARDWARE BLOCK (PRODUCT-TRUTH §5). Goes in EVERY prompt
# regardless of crop: the Weekender's logged bug #3 is that gating this on
# "hardware prominent" makes the wide and open shots fail worst of all.
CLOSURE = (
    "Front closure hardware: at the front centre of the leather band stands a small gold turn post with "
    "a round knurled mushroom shaped head. The flap's centre tab carries a polished gold OVAL plate with "
    "a shaped keyhole cutout in its middle, and when the flap is down this tab rests over the post so the "
    "gold post head shows through the cutout. To the left and right, two flat vertical gold staples stand "
    "on the band; when the flap is down its two small oval slots sit over these staples so the staples "
    "poke through. Each staple is TWO PARALLEL FLAT GOLD BARS side by side, never one solid blade and "
    "never a buckle. The two leather belt straps come over the top from the back of the bag, and each "
    "strap tip carries a flat gold rounded rectangular end plate with an oblong slot and small dome "
    "rivets, which hooks over its staple. When unfastened the straps hang straight DOWN close to the left "
    "and right SIDE edges with their gold end plates visible; they never cross the middle of the front, "
    "never run diagonally and never reach the bottom edge. The knurled mushroom post appears ONCE, at the "
    "front centre of the band; never render both a post through the plate and a second post below the "
    "flap edge. The oval plate is FLAT and flush against the leather with a smooth polished face and an "
    "EMPTY keyhole cutout punched through it, flanked by two tiny plain smooth dome rivets sitting almost "
    "flush: no barrel, no cylinder, no knurled drum, no turning bar or toggle standing proud of the plate "
    "face, and the rivets are never slotted screws. The handles pass through keyhole shaped cutouts in "
    "the flap with stitched edges. A small leather key bell is tied at a handle base. One small gold "
    "eyelet sits high on each side face near the gusset edge. All hardware is the same warm brass gold, "
    "both sides identical, no silver, no chrome."
)

# 🔒 HANDLE COUNT. Goes at the very FRONT of the prompt, not buried in identity().
# V5's first roll rendered ONE wide loop spanning the centre instead of two short
# loops side by side. A fitting that renders wrong does not get reworded in
# place: it gets an explicit COUNT read left to right at the head of the prompt.
HANDLE_COUNT = (
    "COUNT THE HANDLES FIRST. This bag has exactly TWO separate short rolled leather top handles, never "
    "one. They are two distinct closed loops standing side by side with a clear gap of bare leather "
    "between them: the LEFT loop rises from the left of the closure band on round brass rivets and comes "
    "back down into the left of the band, and the RIGHT loop rises from the right of the band and comes "
    "back down into the right of the band. There is never one single wide handle, never one loop spanning "
    "the centre of the bag and never three loops. "
)

# 🔒 OPEN-STATE CLOSURE. Replaces CLOSURE on the one plate where the flap is
# folded back.
#
# The first V5 roll came back physically incoherent: flap down in FRONT with the
# mouth gaping open BEHIND it. That was a prompt bug, not a model miss. The
# standing CLOSURE block describes the CLOSED state, where the flap's centre tab
# rests its oval plate over the post, and asking for a folded-back flap in the
# same breath is a contradiction the engine resolved by keeping the flap forward.
# When the flap goes back the oval plate goes back WITH IT, so the front band
# must show a BARE post. Counts read left to right, at the front of the prompt.
OPEN_CLOSURE = (
    "The flap is folded ALL THE WAY BACK, so no part of the flap is visible from the front and the gold "
    "OVAL keyhole plate is NOT anywhere on the front of this bag: the oval plate belongs to the flap's "
    "centre tab and it has travelled backwards with the flap. Reading the front closure band from LEFT to "
    "RIGHT there are exactly FIVE things on it and nothing else. First, one flat vertical gold staple made "
    "of TWO PARALLEL FLAT GOLD BARS side by side, never one solid blade and never a buckle. Second, the "
    "left leather belt strap, hanging straight DOWN close to the left side edge, unfastened, its tip "
    "carrying a flat gold rounded rectangular end plate with an oblong slot and small dome rivets. Third, "
    "at the exact front centre, one small gold turn post with a round knurled mushroom shaped head, "
    "standing BARE and uncovered with nothing resting on it and nothing hanging over it. Fourth, the right "
    "leather belt strap, hanging straight down close to the right side edge, unfastened, with its own gold "
    "end plate. Fifth, one more flat vertical gold staple of two parallel flat gold bars. There is exactly "
    "ONE knurled post, exactly TWO staples, exactly TWO belt straps and ZERO oval plates. Neither belt "
    "strap crosses the middle of the front, runs diagonally or reaches the bottom edge. A small leather "
    "key bell is tied at a handle base. One small gold eyelet sits high on each side face, and one small "
    "brass ring at each side carries the detachable shoulder strap. All hardware is the same warm brass "
    "gold, both sides identical, no silver, no chrome."
)

# 🔒 OCCLUSION (PRODUCT-TRUTH §5, the v3 hero reject). The flap hangs in FRONT of
# the body, so its holes can only ever show the bag's own shadowed back panel.
OCCLUSION = (
    "Every cutout, slot and keyhole on this bag is opaque. The two round handle cutouts in the flap, the "
    "two oval strap slots, the keyhole in the gold oval plate and the oblong slot in each strap end plate "
    "all show the bag's OWN dark shadowed leather immediately behind them. None of them is transparent "
    "and none of them shows the wall, the floor, the sky or anything else from the scene through it."
)

# 🔒 MATERIAL. PRODUCT-TRUTH §3 banned word list, stated positively first.
# v1 crazed from "marbling / crease patina"; v2 came back blotchy and plastic
# from "high-gloss / wet-looking lacquered sheen". Both sets were full rejects.
MATERIAL = (
    "MATERIAL: the body leather is SOFT with real natural pore and pebble grain and a MATTE to SATIN "
    "sheen, catching only broad soft highlights where the light rakes across it, and creasing and folding "
    "naturally as the bag slumps. The flap, band, handles and straps are the same leather in a smoother, "
    "more burnished finish, still satin and never mirror bright. ABSOLUTELY NOT: no gloss, no lacquer, no "
    "wet look, no patent finish, no crack web, no crazing, no network of fine fracture lines, no dry "
    "veining, no spiderweb texture, no reptile or elephant skin, no distressed cracked finish, no bonded "
    "leather pebbling, no crumpled foil look, no blotchy smeared patches and no low frequency mottling "
    "that fails to follow the form."
)

# SCALE. Dimensions never hold scale in a prompt (PRODUCT-TRUTH §8), so the
# relational line does the work. Never shrink the bag (laws.md §6).
SCALE = (
    "The bag is BIG. It measures about 38 cm, roughly 15 inches, across the base and it is the largest "
    "handbag this brand makes. Worn on the shoulder its body reaches from just under her armpit to below "
    "her hip and it is about as wide as her torso. Carried in the hand it hangs to about mid thigh. A "
    "hand laid on it spans only a small fraction of its width. It is never a small handbag, never a mini "
    "bag and never a clutch."
)

# CARRY (PRODUCT-TRUTH §7). The top handles are SHORT and do not reach a
# shoulder. Prompting a shoulder carry on them makes the engine invent a longer
# strap to bridge the pose, so shoulder carries always name the detachable strap.
CARRY_HAND = (
    "How she carries it: by its two short rolled top handles, held in her hand. Her fingers curl "
    "completely around both handles low down near where they enter the band, so each handle tube is "
    "clearly visible both above and below her curled fingers. Each handle is one single continuous "
    "unbroken loop of leather and both arches read fully along their length. The detachable shoulder "
    "strap is not fitted and there is no long strap anywhere in the frame. The weight of the bag visibly "
    "hangs from that grip and the bag hangs plumb, straight down."
)

CARRY_SHOULDER = (
    "How she carries it: on the ONE detachable long leather shoulder strap, which is clipped to a small "
    "brass ring at each side of the bag and runs up over her shoulder in a single clean line. The two "
    "short rolled top handles stay at the top of the bag, unused and clearly too short to reach a "
    "shoulder. There is exactly ONE strap over her shoulder and exactly one strap in the frame, never "
    "two, never a doubled strap and never a second loop hanging free."
)

CARRY_STRAP_IN_HAND = (
    "How she carries it: the ONE detachable long leather shoulder strap is clipped to a small brass ring "
    "at each side of the bag, and she has hooked her fingers over that strap so the bag hangs from it in "
    "front of her, swinging free and clear of her body. The two short rolled top handles stay at the top "
    "of the bag, unused. There is exactly ONE long strap in the frame, never two and never a second loop."
)

# CASTING. The Velantra buyer, not the reference's model. Coastal framing is
# dropped brand wide (the 8/16 pivot), so these are city and studio settings and
# the wardrobe is quiet year round leather-and-linen, not resort.
# NO NECKLACES: fine chains render as mangled gold smears. Hands stated
# positively, since naming hand defects to avoid trips the content filter.
MODEL = (
    "The woman is in her early forties, with warm skin showing real visible texture and fine lines at her "
    "eyes, no heavy makeup, natural brows and bare lips. Her hair is loose and slightly undone with a few "
    "strands out of place, never slicked back. She wears small simple earrings and no necklace and no "
    "other jewelry at all, nothing around her neck. She is slim and healthy looking, relaxed and unposed, "
    "standing at ease in the middle of an ordinary good day, never a cold hard editorial stare and never "
    "a wide posed grin. Her hands are rendered cleanly and naturally with five well formed fingers on "
    "each visible hand, each finger clearly separated and correctly proportioned, in a relaxed everyday "
    "grip. Only one person anywhere in the frame."
)

CAST = {
    "V3-out-the-door":
        "She has long dark blonde hair worn loose down her back, and light warm skin. Small gold stud "
        "earrings.",
    "V4-effortless": "",     # waist down crop, no head in frame
    "V6-quote":
        "She has dark brown hair, deep warm skin and a slim frame. Small gold stud earrings.",
}

MATCH_TAIL = (
    "The bag in the frame is an exact copy of the bag in the reference photographs in silhouette, "
    "proportions, materials, stitching, hardware and colour. All the leather on the bag reads as one "
    "consistent hide. The bag has no zipper anywhere, no padlock, no clochette beyond the small leather "
    "key bell, no studs, no charms and no metal at all beyond the fittings named above."
)

NO_TEXT = (
    "Absolutely no text, no words, no letters, no numbers, no captions, no watermarks, no labels and no "
    "logos anywhere in the image, on the bag, on the clothing, on the wall or on any object."
)

# 🔒 PHOTOREAL FOOTER (velantra-vivienne skill, hardened 2026-08-22). The 3D
# render look is a global reject condition. Do not shorten this.
PHOTOREAL = (
    "CRITICAL RENDERING INSTRUCTION. This is a real photograph taken on a camera by a person. It is NOT a "
    "3D render, NOT CGI, NOT a product visualisation, NOT Blender or Octane or Unreal or Keyshot, NOT ray "
    "traced, NOT retouched, NOT airbrushed. If it looks polished or computer generated it is wrong. "
    "Photographic evidence that must be present: visible digital sensor noise and fine grain through the "
    "shadows and midtones, highlights slightly blown out where the light source strikes the leather, mild "
    "chromatic aberration on high contrast edges, focus that is slightly imperfect so nothing is "
    "uniformly tack sharp, and real shadows falling off naturally with visible ambient bounce. Real "
    "surfaces at high micro detail: individual stitch threads are separately resolved with visible twist, "
    "the whip stitched braid reads as discrete interlocking strands and never as a soft repeating ripple, "
    "the leather shows real pore grain and fine wrinkle lines, faint scuffs and handling marks, and dust "
    "caught in the seams. ABSOLUTELY NOT: blotchy smeared patches on the leather, low frequency mottling "
    "that does not follow the form, an airbrushed or waxy plastic surface, mushy or melted fine detail, "
    "or smooth featureless gradients standing in for texture. The bag is very slightly asymmetric the way "
    "a real soft handmade bag is, never perfectly mirrored left to right."
)


# --- SCENES: one per reference, laid out for the type that lands in compose.py -
#
# Each CRITICAL EMPTY SPACE rule is derived from the measured type band in that
# reference (see measure_refs.py / measure_white2.py output in BRIEF.md).

VARIATIONS = [
    (
        # R6: two raffia pouches on a warm grey sweep, headline band at 26-30%,
        # brand mark at 89%. Ours = the hero pair, Chocolate and Cognac.
        "V1-first-run", ["Ch-front.png", "Co-three-quarter.png"], "Ch",
        "STILL LIFE PRODUCT PHOTOGRAPH, NO PERSON ANYWHERE IN THE FRAME. Vertical 9 by 16 frame. TWO of "
        "these large soft leather top handle bags sit together on a smooth warm pale grey seamless studio "
        "sweep in colour #D6D2CB, the floor curving up into a seamless back wall with no visible corner "
        "or edge. The bag on the left is the deep dark chocolate brown one with contrast cognac straps "
        "and trim shown in the first reference photograph. The bag on the right is the same bag in the "
        "warm mid cognac brown shown in the second reference photograph, where the straps and trim are "
        "the same cognac as the body. The two bags are identical in construction, proportion and hardware "
        "and differ only in colour. They sit angled slightly toward each other, the left bag set a little "
        "forward and lower and the right bag further back and higher, overlapping slightly so they read "
        "as a sculptural pair, both slumping softly under their own weight with their bodies bowing and "
        "their bases spreading on the sweep. Both are closed, flaps down, belt straps hanging loose near "
        "the side edges. Shot from slightly below the height of the bags on a long lens so they feel "
        "substantial. Soft diffused daylight from the upper left, each bag casting one soft contact "
        "shadow on the sweep. "
        "CRITICAL COMPOSITION RULE: the two bags together fill the LOWER TWO THIRDS of the frame, their "
        "topmost handle no higher than 36 percent down from the top edge. The ENTIRE TOP THIRD of the "
        "frame is nothing but smooth empty pale grey sweep, one clean unbroken gradient with no object, "
        "no shadow and no detail in it at all, because pale text will be placed there afterwards. Leave a "
        "clear band of empty sweep across the very bottom of the frame as well.",
    ),
    (
        # R2: two bags leaning against a plain white wall on a polished concrete
        # floor, straps splaying. Brand mark and tagline centred at 48-51%, which
        # lands ON the bags, so the type needs a dark mid-frame to sit on.
        "V2-leather-logo", ["Bl-three-quarter.png", "Ch-front.png"], "Bl",
        "STILL LIFE PRODUCT PHOTOGRAPH, NO PERSON ANYWHERE IN THE FRAME. Vertical 9 by 16 frame. TWO of "
        "these large soft leather top handle bags sit on a polished pale grey concrete floor, leaning "
        "back against a plain smooth off white painted wall. The bag in FRONT and lower left is the deep "
        "black one shown in the first reference photograph. The bag BEHIND it and to the upper right is "
        "the deep dark chocolate brown one with contrast cognac straps and trim shown in the second "
        "reference photograph. Both slump heavily: their bodies collapse and fold, their sides pinch, "
        "their bases spread wide where they meet the floor. Both are closed, flaps down. On each bag the "
        "long detachable leather shoulder strap is clipped on and left loose, sweeping out and up in a "
        "long lazy curve across the wall behind and above them so the two straps draw big soft arcs "
        "through the upper half of the frame. Shot straight on at floor level on a long lens. Flat even "
        "daylight from the front, faint soft shadows pooling under the bags on the concrete, cool neutral "
        "colour grade. "
        "CRITICAL COMPOSITION RULE: the two bags fill the middle and lower two thirds of the frame and "
        "the widest, darkest, most continuous mass of leather sits across the horizontal middle band of "
        "the frame between 44 and 55 percent down from the top, because pale text will be placed exactly "
        "there and needs a dark unbroken surface underneath it. Keep that middle band free of bright "
        "highlights, free of gold hardware and free of the pale wall.",
    ),
    (
        # R3: back to camera, big bag on the shoulder, brand mark and tagline
        # centred at 47-51% which sits ON the bag body.
        "V3-out-the-door", ["Ch-front.png", "Ch-three-quarter.png"], "Ch",
        "She is standing in a bright plain studio, one smooth continuous off white painted wall filling "
        "the whole background, nothing else in the room at all. She is photographed from BEHIND with her "
        "back to the camera, her head turned a little to her right so only the edge of her cheek and jaw "
        "shows. She wears a loose oversized cream linen shirt worn open over a plain cream top and pale "
        "trousers. The large soft leather bag hangs on her nearer shoulder against her back, its body "
        "slumping and folding under its own weight. Soft even daylight from the front, a faint shadow on "
        "the wall behind her, quiet cool neutral colour grade. "
        # First roll put the bag's body at 55-80% and left the 44-55% type band
        # sitting on her pale cream linen, where white type cannot survive.
        # Describing a band did not hold it; pinning the bag's top and bottom
        # edges as explicit percentages does.
        "CRITICAL FRAMING RULE, THIS GOVERNS THE WHOLE PICTURE: she is framed from the crown of her head, "
        "which touches the very top edge of the frame, down to just above her knees. The bag is enormous "
        "in the frame. The tops of its two rolled handles sit about 22 percent of the way down from the "
        "top edge of the frame, and the bottom of the bag sits about 72 percent of the way down, so the "
        "bag occupies half the height of the entire picture and its widest leather panel spans the "
        "horizontal middle of the image. "
        "CRITICAL COMPOSITION RULE: the horizontal band between 44 and 56 percent down from the top edge "
        "must be filled edge to edge across the middle of the frame with one continuous unbroken expanse "
        "of the bag's own dark leather, with no gold hardware, no closure band, no strap, no bright "
        "highlight and no pale linen or pale wall crossing it, because pale text will be placed exactly "
        "there. Position the bag so its closure band and all of its gold fittings sit ABOVE that band, "
        "higher up in the frame, and the plain lower body of the bag fills the band itself.",
    ),
    (
        # R4: waist down crop, wide leg denim, bag hanging from the hand at knee
        # height, mark left at 45% and copy right at 44-47%.
        "V4-effortless", ["Co-front.png", "Co-three-quarter.png"], "Co",
        "CROPPED FRAMING, NO FACE AND NO HEAD IN THE FRAME. Vertical 9 by 16 frame showing the woman only "
        "from about her ribcage down to her feet, her upper body cut off by the top edge. She stands "
        "against one smooth continuous off white painted wall over a polished pale grey concrete floor, "
        "nothing else in the room. She wears a loose cream cotton blouse with softly gathered sleeves, "
        "cropped by the top edge of the frame, over wide leg light wash blue jeans with the hems turned "
        "up once, and flat dark brown leather loafers. She stands with her weight on one hip, turned very "
        "slightly toward the camera. Her near arm hangs straight down and the large soft leather bag "
        "hangs from that hand beside her leg, its base at about the height of her knee, the body slumping "
        "and bowing. Soft even daylight, quiet cool neutral colour grade, one soft shadow on the wall. "
        "CRITICAL FRAMING RULE: her legs run down the centre and right of the frame and the bag hangs on "
        "the LEFT side of the frame, its body sitting between 24 and 60 percent down from the top edge. "
        "CRITICAL EMPTY SPACE RULE: the horizontal band between 42 and 49 percent down from the top must "
        "stay simple and readable across the WHOLE width of the frame. On the LEFT that band is the "
        "bag's own dark leather body, and on the RIGHT it is nothing but her plain blue denim and the "
        "smooth pale wall behind her, with no pocket, no seam detail, no bright highlight and no clutter "
        "in it, because pale text will be placed across that band on both sides.",
    ),
    (
        # R5: studio still life on a warm mauve ground, bag open and overflowing,
        # tracked caps at 21.5%, body to 28%, brand mark at 94%.
        #
        # ⚠️ PRODUCT-TRUTH §3: the lining is TODO and must never be generated, and
        # §11 clears no capacity claim. The mouth is therefore packed solid with
        # the objects themselves so no interior surface is ever visible, and the
        # load is an ordinary handful rather than a volume demonstration.
        "V5-real-day", ["Ol-front.png", "Ol-three-quarter.png"], "Ol",
        "STILL LIFE PRODUCT PHOTOGRAPH, NO PERSON ANYWHERE IN THE FRAME. Vertical 9 by 16 frame. ONE of "
        "these large soft leather top handle bags stands alone on a smooth warm mauve taupe seamless "
        "studio sweep in colour #8C7166, the floor curving up into a seamless back wall with no visible "
        "corner or edge. The bag is the deep muted olive green one shown in the reference photographs. It "
        "is OPEN. The single one piece leather flap has been folded ALL THE WAY BACK over the top of the "
        "bag toward the rear, so it hangs down the BACK of the bag where the camera cannot see it and NO "
        "part of the flap appears anywhere in front of the mouth. The mouth is therefore one single wide "
        "opening between the two soft side gussets, running the full width of the bag, with nothing lying "
        "across it. The two leather belt straps hang loose and unfastened close to the left and right side "
        "edges of the front, their gold end plates visible. The bag slumps heavily, its body bowing and "
        "its base spreading on the sweep. "
        "The open mouth is PACKED COMPLETELY FULL and the objects are crowded tightly against each other "
        "so they fill the entire opening edge to edge and no interior surface, no lining and no inside "
        "wall of the bag is visible anywhere: a closed hardcover notebook standing on its edge, a folded "
        "pair of dark tortoiseshell sunglasses hooked over the front edge, a slim white cylindrical "
        "bottle, a pale wide toothed comb and a small dark tube, all leaning out of the top at slight "
        "angles. Every one of these objects is completely plain and unbranded with no text, no label and "
        "no lettering on it. The long detachable leather shoulder strap is clipped on and drapes down "
        "across the front of the bag and onto the sweep. Shot straight on at about the height of the "
        "bag's mouth on a long lens. One soft warm directional light from the upper left, deep soft "
        "shadow falling to the right, warm low key colour grade, one soft contact shadow. "
        "CRITICAL COMPOSITION RULE: the bag and everything leaning out of it sit entirely in the LOWER "
        "TWO THIRDS of the frame, with the highest object no higher than 34 percent down from the top "
        "edge. The ENTIRE TOP THIRD of the frame is nothing but the smooth empty warm mauve taupe sweep, "
        "one clean unbroken mid tone gradient with no object, no shadow and no detail at all, because "
        "pale text will be placed there. Leave a clear band of empty sweep across the very bottom of the "
        "frame as well.",
    ),
    (
        # R1: torso crop, black dress, warm off white wall, bag hanging from the
        # strap hooked over her hand. Three line quote lower LEFT at 79-84% over
        # the dress, which measures L~23 in the reference: the type needs a very
        # dark lower left quadrant.
        "V6-quote", ["Bl-front.png", "Bl-three-quarter.png"], "Bl",
        "CROPPED FRAMING, NO FACE IN THE FRAME. Vertical 9 by 16 frame showing the woman from just below "
        "her chin down to about her knees, her head cut off by the top edge. She stands against a smooth "
        "warm off white painted wall, nothing else in the room. She wears a plain sleeveless black cotton "
        "dress with a soft scooped neckline and a full skirt that falls in deep folds. She stands turned "
        "very slightly toward the camera with one arm folded loosely across her waist. The large soft "
        "leather bag hangs in front of her at hip height, slumping and bowing under its own weight. Soft "
        "even daylight from the front left, a faint soft shadow on the wall to her right, quiet neutral "
        "colour grade. "
        "CRITICAL FRAMING RULE: she stands slightly left of centre and the bag hangs in the middle right "
        "of the frame between 24 and 62 percent down from the top edge, large and completely readable, "
        "the sharpest thing in the picture. "
        "CRITICAL EMPTY SPACE RULE: the entire LOWER LEFT of the frame, everything below 74 percent down "
        "from the top and left of the middle, is nothing but the deep matte black fabric of her skirt "
        "falling in soft dark folds. It is a very dark, calm, low contrast expanse with no bright "
        "highlight, no pale wall, no hand, no hardware and no strong detail anywhere in it, because white "
        "text will be placed there afterwards and must stay easy to read.",
    ),
]

CARRY_FOR = {
    "V3-out-the-door": CARRY_SHOULDER,
    "V4-effortless": CARRY_HAND,
    "V6-quote": CARRY_STRAP_IN_HAND,
}

# Plates whose flap is folded back, and which therefore take OPEN_CLOSURE instead
# of the closed-state CLOSURE block.
FLAP_OPEN = {"V5-real-day"}

# Plates that lead with the explicit handle count. V5 rendered one loop on the
# first roll; V3 is re-rolled with it as cheap insurance since the bag is the
# largest thing in that frame.
COUNTS_FIRST = {"V5-real-day", "V3-out-the-door"}


NO_TEXT_SHORT = (
    "No text, no words, no letters, no numbers, no captions, no watermarks, no labels and no logos "
    "anywhere in the image."
)


def build_prompt(name, key, scene, trim=False):
    """Full prompt, or the trimmed variant used as the first fallback.

    The Delphine run passed at 2K up to 7975 chars; the three on-body plates here
    land near 9900 because they carry the model, the casting, the carry block and
    the scale anchor on top of the same product truth. `trim` drops MATCH_TAIL
    (whose content is already carried by identity() and CLOSURE) and shortens the
    no-text clause, which pulls those plates back under the proven ceiling.
    Nothing that PRODUCT-TRUTH marks mandatory is ever dropped: the closure
    block, the occlusion block, the material block and the photoreal footer all
    survive both variants.
    """
    c = CW[key]
    people = ""
    if name in CARRY_FOR:
        people = f"{MODEL} {CAST.get(name, '')} {CARRY_FOR[name]} {SCALE} "
    tail = "" if trim else f"{MATCH_TAIL} "
    no_text = NO_TEXT_SHORT if trim else NO_TEXT
    closure = OPEN_CLOSURE if name in FLAP_OPEN else CLOSURE
    counts = HANDLE_COUNT if name in COUNTS_FIRST else ""
    return (
        f"{PREAMBLE}{counts}{scene} {people}"
        f"The bag in the frame: {identity(c)} {closure} {OCCLUSION} {MATERIAL} {tail}"
        f"{no_text} {PHOTOREAL}"
    )


def api(url, payload=None, headers=None):
    """Calls go through curl, not urllib.

    This Python has no root-certificate bundle wired up, so urllib raises
    CERTIFICATE_VERIFY_FAILED against api.kie.ai (logged on the Delphine run).
    curl uses the system trust store and is the working path for the uploads too.
    """
    cmd = ["curl", "-s", "--max-time", "120", url]
    for k, v in (headers or {}).items():
        cmd += ["-H", f"{k}: {v}"]
    if payload is not None:
        cmd += ["-H", "Content-Type: application/json", "-d", json.dumps(payload)]
    for attempt in range(4):
        out = subprocess.run(cmd, capture_output=True, text=True)
        try:
            return json.loads(out.stdout, strict=False)
        except Exception as e:
            if attempt == 3:
                raise RuntimeError(f"{url} -> {(out.stdout or out.stderr)[:300]}") from e
            print(f"  retry {attempt+1}: {e}", flush=True)
            time.sleep(3 * (attempt + 1))


def fetch(url, dest):
    out = subprocess.run(["curl", "-s", "-L", "--max-time", "300",
                          "-A", "Mozilla/5.0", "-o", dest, url],
                         capture_output=True, text=True)
    if out.returncode != 0 or not os.path.exists(dest) or os.path.getsize(dest) < 1024:
        raise RuntimeError(f"download failed: {url} ({out.stderr[:200]})")
    return os.path.getsize(dest)


def upload(path):
    name = os.path.basename(path).replace(" ", "_")
    last = ""
    for attempt in range(4):
        if attempt:
            time.sleep(20 * attempt)
        out = subprocess.run(
            ["curl", "-s", "-X", "POST", UPLOAD,
             "-H", f"Authorization: Bearer {KEY}",
             "-F", f"file=@{path}",
             "-F", "uploadPath=vivienne-vestirsi-statics",
             "-F", f"fileName={int(time.time())}-{name}"],
            capture_output=True, text=True)
        try:
            d = json.loads(out.stdout, strict=False)
            url = (d.get("data") or {}).get("downloadUrl")
            if url:
                print(f"uploaded {name}", flush=True)
                return url
            last = out.stdout
        except Exception:
            last = out.stdout or out.stderr
        print(f"  upload retry for {name}: {last[:150]}", flush=True)
    raise RuntimeError(f"upload failed for {name}: {last[:300]}")


ATTEMPTS = 3   # GPT Image 2's content filter refuses intermittently on identical input


def submit(name, ref_urls, key, scene):
    """2K full prompt, then 2K trimmed, then 1K full.

    Long prompts get rejected at 2K before 1K (Sofia carry-all run), so trimming
    the prompt is tried BEFORE dropping resolution: these plates ship at
    1080x1920 and a 1K render has to be upscaled to get there.
    """
    ladder = [("2K", False), ("2K", True), ("1K", False)]
    last = None
    for res, trim in ladder:
        payload = {"model": "gpt-image-2-image-to-image",
                   "input": {"prompt": build_prompt(name, key, scene, trim),
                             "input_urls": ref_urls,
                             "aspect_ratio": "9:16",
                             "resolution": res}}
        d = api(f"{API}/jobs/createTask", payload, H)
        if d.get("code") == 200:
            if trim or res != "2K":
                print(f"  {name}: accepted at {res}{' trimmed' if trim else ''}", flush=True)
            return d["data"]["taskId"]
        last = d
    raise AssertionError(f"{name} createTask failed on every rung: {last}")


def main():
    os.makedirs(OUT, exist_ok=True)
    only = set(a for a in os.sys.argv[1:])
    todo = [v for v in VARIATIONS
            if (not only or v[0] in only)
            and not os.path.exists(os.path.join(OUT, f"{v[0]}.png"))]
    for name, *_ in VARIATIONS:
        if not any(t[0] == name for t in todo):
            print(f"{name}: exists or not selected, skip", flush=True)
    if not todo:
        print("nothing to do", flush=True)
        return

    for name, _, key, scene in todo:
        print(f"{name}: prompt {len(build_prompt(name, key, scene))} chars", flush=True)

    cache = {}
    for _, refs, _, _ in todo:
        for r in refs:
            if r not in cache:
                cache[r] = upload(os.path.join(REF_DIR, r))

    spec = {name: (refs, key, scene) for name, refs, key, scene in todo}
    tries = {name: 0 for name in spec}
    pending = {}
    for name, (refs, key, scene) in spec.items():
        tries[name] += 1
        pending[name] = submit(name, [cache[r] for r in refs], key, scene)
        print(f"{name}: task {pending[name]} (attempt {tries[name]})", flush=True)

    deadline = time.time() + 3000
    while pending and time.time() < deadline:
        time.sleep(15)
        for name, tid in list(pending.items()):
            d = api(f"{API}/jobs/recordInfo?taskId={tid}", None, H)
            st = (d.get("data") or {}).get("state")
            if st == "success":
                rj = json.loads(d["data"]["resultJson"], strict=False)
                size = fetch(rj["resultUrls"][0], os.path.join(OUT, f"{name}.png"))
                print(f"{name}: DONE ({size//1024} KB)", flush=True)
                del pending[name]
            elif st == "fail":
                msg = (d.get("data") or {}).get("failMsg")
                print(f"{name}: attempt {tries[name]} failed: {msg}", flush=True)
                del pending[name]
                refs, key, scene = spec[name]
                if tries[name] < ATTEMPTS:
                    tries[name] += 1
                    pending[name] = submit(name, [cache[r] for r in refs], key, scene)
                    print(f"{name}: retry task {pending[name]} (attempt {tries[name]})", flush=True)
                else:
                    print(f"{name}: GIVING UP after {ATTEMPTS} attempts", flush=True)
    if pending:
        print(f"TIMEOUT still pending: {list(pending)}", flush=True)
    done = [v[0] for v in VARIATIONS if os.path.exists(os.path.join(OUT, f"{v[0]}.png"))]
    print(f"complete: {len(done)}/{len(VARIATIONS)} -> {sorted(done)}", flush=True)


if __name__ == "__main__":
    main()
