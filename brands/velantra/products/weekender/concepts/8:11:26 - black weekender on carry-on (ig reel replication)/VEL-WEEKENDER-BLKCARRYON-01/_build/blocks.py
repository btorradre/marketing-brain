"""Verbatim locked blocks for VEL-WEEKENDER-BLKCARRYON-01.

BLACK COLOURWAY build. Inherited from the validated MENSPACK-01 harness, but every
product block has been rewritten for Black, which is NOT a recolour of the other
colourways: it is ALL smooth black leather over the whole exterior with NO canvas
panel anywhere, caramel tan leather interior, warm brass gold hardware.

Ground truth = the five REAL iPhone photos in
  products/weekender/product-images/black/original-iphone-photos/
(black-01 front, black-03 open + caramel interior, black-04 hand-scale on a person,
black-05 hardware macro). Those photos outrank every written description here.

Two things the Black photos settle that the Light Chocolate blocks got to leave open:
  1. NO canvas. The signature i2i failure for Black is LEFTOVER CANVAS — the model
     recolours the canvas panel instead of replacing it and leaves a crosshatch weave
     or a grey/cream wedge. ANTI_CANVAS below is the corrective and travels in every
     single prompt.
  2. The belt straps are SHORT AND HORIZONTAL on the band in all three ground-truth
     photos (fastened state), open bag included. This build locks that state, which
     also removes the "straps drifting diagonally across the body" failure class
     entirely — there is nothing hanging to drift.
"""

# ---------------------------------------------------------------- preamble
PREAMBLE = (
    "Use the attached photos ONLY as the reference for the bag's shape, proportions, "
    "materials, colours, stitching and hardware. Do NOT copy their lighting, their "
    "backgrounds, their clean edges or any polished studio product-photo look. The "
    "picture you produce must not resemble a catalogue image. Create "
)

# ---------------------------------------------------------------- identity (BLACK)
IDENTITY = (
    "a structured all black weekend bag, wider than tall, the entire exterior in one single "
    "smooth semi matte black leather, a scalloped one piece black leather fold over flap with "
    "two rolled black leather top handles rising up through keyhole shaped cutouts in it, a "
    "polished gold oval turn lock plate on the flap's centre tab, two flat gold clasp plates on "
    "the body band with short black leather belt straps lying horizontally into them, a small "
    "black leather key bell hanging on a long thin black leather lace from the base of the front "
    "handle down the front of the bag, black leather corner patches at the bottom, a small gold "
    "eyelet high on each side face, visible stitching, warm brass gold hardware, no logos "
    "anywhere on the bag, smooth caramel tan leather interior lining with a wide matching "
    "caramel slip pocket on the interior wall"
)

ANTI_DRIFT = (
    " The bag in frame is an exact copy of the bag in the reference image in silhouette, "
    "proportions, materials and details. The two rolled top handles are smooth simple black "
    "leather tubes with no wrapping, no braiding and no woven texture. Both handles are rounded "
    "tubes that stand proud of the surface, and each end is anchored with its own teardrop shaped "
    "stitched leather base. A handle is never flattened into a strip, never an appliqué lying "
    "flat on the leather, and never fused into the band without a base."
)

# ---------------------------------------------------------------- THE BLACK LAW
# The signature failure mode for this colourway (proven across two i2i passes on
# 2026-08-09): the model RECOLOURS the canvas body instead of REPLACING it, leaving a
# crosshatch weave across the body, a grey-body-vs-black-flap material split, or a small
# unconverted cream wedge at a side gusset. This block is the corrective and is pasted
# into EVERY prompt regardless of crop.
ANTI_CANVAS = (
    "BLACK COLOURWAY LAW, the single most important material rule in this picture. This bag is "
    "ALL BLACK LEATHER. Every exterior panel of it, the flap, the upper band, the entire lower "
    "body, both side gussets, the back, the corner patches, the handles and the belt straps, is "
    "the SAME single smooth semi matte black leather. There is NO woven canvas anywhere on this "
    "bag, NO crosshatch weave, NO basketweave, NO pin dot texture, NO fabric of any kind, NO "
    "cream panel, NO ivory panel, NO beige panel, NO grey panel and NO two tone split of any "
    "kind. The body below the band is BLACK LEATHER, not canvas. Where the upper section meets "
    "the body there is only a fine horizontal stitched seam joining two panels of the SAME black "
    "leather: never a change of material, never a change of colour, never a visible edge between "
    "two different textures. If any part of the bag's exterior reads as woven fabric, or reads "
    "lighter or greyer than the rest of the bag, the picture is WRONG. The only colour anywhere "
    "on this bag other than black leather and gold hardware is the caramel tan leather lining "
    "INSIDE it."
)

# ---------------------------------------------------------------- hardware law (BLACK)
HARDWARE_LAW = (
    "HARDWARE LAW, applies to the whole bag in every shot. Count and place the hardware exactly "
    "as follows and add nothing else. "
    "BELT STRAPS: there are exactly TWO short black leather belt straps on the front, one to the "
    "left of centre and one to the right of centre, and both lie HORIZONTALLY across the black "
    "leather band, level with each other. Each strap runs horizontally into its own flat warm "
    "gold clasp plate, and each plate has a single oblong slot and small dome rivets. The straps "
    "are SHORT and sit close against the band. They never hang down the front, never run "
    "diagonally, never reach the bottom edge of the bag, never dangle below it, and never turn "
    "into long luggage compression straps. Both plates are the SAME warm brass gold and the same "
    "modest size, the RIGHT plate identical in colour to the LEFT plate. "
    "Apart from those two clasp plates and the small gold eyelet on each side face, the body of "
    "the bag carries NO other hardware at all: no extra straps, no extra plates, no buckles, no "
    "studs, no rings, no rivets, no floating metal rods. "
    "OVAL PLATE: there is exactly ONE gold oval plate with a keyhole cutout on the entire bag and "
    "it belongs to the FLAP's centre tab. Never duplicate it, never add a second oval turn lock "
    "onto the band or onto the body. "
    "WHAT THE OVAL PLATE ACTUALLY LOOKS LIKE, and this matters most in close views: it is a FLAT "
    "gold oval plate lying flush against the black leather, with a smooth polished face and an "
    "EMPTY cross shaped keyhole cutout punched through the middle of it so you see dark shadow "
    "through the hole. Flanking the cutout are two TINY PLAIN SMOOTH DOME RIVETS sitting almost "
    "flush. There is NO barrel, NO cylinder, NO knurled drum, NO turning bar and NO toggle "
    "standing proud of the plate face. The rivets are never slotted screws and never have a "
    "driver slot cut across them. Nothing on the plate protrudes toward the camera. "
    "FLAP SHAPE: the flap is ONE single piece of black leather with a gently scalloped lower "
    "edge. It has two keyhole shaped cutouts that the rolled handles pass up through, and two "
    "small plain leather keyhole slits out toward its left and right ends with NO metal in them. "
    "SIDE FACES AND GUSSETS: each side face carries exactly ONE small gold eyelet high up near "
    "the gusset edge and NOTHING else. No oval keyhole plates, no D plates, no clasps, no studs, "
    "no floating gold bars or spikes anywhere on the side faces or gussets. "
    "The key bell is plain black leather on a plain thin black leather lace: no metal ring, cap "
    "or tip. "
    "Every piece of metal on and inside the bag, including the small side eyelets, is WARM BRASS "
    "GOLD. No silver, no chrome, no nickel, no white metal anywhere. No engraving, lettering or "
    "brand stamp on any metal surface. "
    "MATERIALS, and every panel of the bag obeys this: the flap, the band, the body, the "
    "handles, the belt straps and the corner patches are all the SAME smooth semi matte black "
    "leather with fine natural creasing and a soft low sheen. They are never suede, never nubuck, "
    "never brushed, never fuzzy, never glossy patent, and no panel is a different finish or a "
    "different black from any other panel."
)

# ---------------------------------------------------------------- closure hardware (BLACK)
CLOSURE = (
    "Front closure hardware, exactly as on the reference photo of the black bag: the flap's "
    "centre tab carries a polished gold oval plate with a shaped keyhole cutout in its middle, "
    "and when the flap is down this tab rests flat against the black leather band with a small "
    "gold turn post showing through the cutout. To the left and right of it, the two short black "
    "leather belt straps lie horizontally across the band, each running into its own flat warm "
    "gold clasp plate with an oblong slot and small dome rivets. The two rolled black leather "
    "handles rise up through the two keyhole shaped cutouts in the flap, and the flap's stitched "
    "scalloped lower edge runs across the front just above the straps. The small black leather "
    "key bell hangs on its long thin lace from the base of the front handle, down over the front "
    "of the bag, swinging free. All hardware is the same warm brass gold, both sides identical, "
    "no silver, no chrome, no white metal on any hardware."
)

# ---------------------------------------------------------------- opening mechanism (BLACK)
MECHANISM = (
    "Open bag construction: the open bag keeps the exact same all black leather exterior as the "
    "closed bag in the reference image. Folding the flap back changes NOTHING about the "
    "materials: every exterior panel is still the same smooth black leather from the top edge "
    "down to the corner patches, with no canvas and no colour change anywhere. "
    "The two rolled black leather top handles are anchored directly into the wide black leather "
    "upper band with sturdy teardrop stitched leather bases. Both rolled handles STAND UPRIGHT "
    "and arch cleanly over the open mouth in a firm rounded loop. A handle never droops, flops, "
    "sags or hangs down as a long slack loop across the front of the bag, and never dangles "
    "below the bottom edge. "
    "On the front band, the two short black belt straps still lie HORIZONTALLY into their two "
    "flat gold clasp plates exactly as they do on the closed bag. There is NO oval plate on the "
    "band: the one and only gold oval keyhole plate in the whole picture is the one on the "
    "folded back flap's centre tab. The wide black leather band on the front is plain smooth "
    "leather and is part of the bag body: no tab sections, no scalloped edges, no pocket shape, "
    "no turn lock pocket, it is not a flap. "
    "The entire black leather flap, ONE single piece, is folded backward over the top rear edge "
    "of the bag and leans back behind the open mouth, clearly visible: the inside face of the "
    "flap shows its two keyhole shaped handle cutouts, its two small plain leather strap slits "
    "and its small gold oval plate with a shaped keyhole cutout, with the rear rolled handle "
    "rising above it. The flap never covers the front of the bag and never splits into pieces. "
    "The mouth of the bag is a clean open oval at the top, and inside it the lining is smooth "
    "CARAMEL TAN LEATHER, a warm butterscotch tan that contrasts strongly against the black "
    "exterior, with a wide matching caramel slip pocket standing against the interior wall. The "
    "interior is never black, never cream, never canvas and never fabric. "
    "The bag has NO zipper anywhere, no zipper track, no zipper teeth, no zipper pull along the "
    "mouth of the bag, and no embossed text or lettering anywhere on the bag. "
    "BOTH handles are clearly visible standing upright: the front handle rises from the front "
    "leather band, the rear handle rises from the back leather band in front of the folded back "
    "flap. Never omit the front handle."
)

# ---------------------------------------------------------------- scale
SCALE = (
    "SCALE IS CRITICAL. This is a LARGE TRAVEL BAG, 18 inches wide by 14.5 inches tall by 7 "
    "inches deep, big enough to pack two to three days of clothes. It is NOT a handbag, NOT a "
    "purse, NOT a medium tote. Roughly the size of a carry-on duffel. Render it noticeably "
    "oversized rather than too small."
)

# ---------------------------------------------------------------- the suitcase prop (locked)
# Deliberately NOT the reference reel's branded aluminium case with orange trim. A plain
# unbranded carry-on: no competitor product gets replicated, and nothing on it can render
# as lettering.
SUITCASE = (
    "THE SUITCASE, identical in every shot it appears in: a plain pale silver grey hard shell "
    "carry-on suitcase with a lightly ribbed vertical shell, four small black spinner wheels, a "
    "black telescoping trolley handle and a black grab handle on its side. It carries NO logos, "
    "NO brand marks, NO stickers, NO badges, NO coloured trim and no lettering of any kind "
    "anywhere on it. It is an ordinary unbranded carry-on, faintly scuffed at the corners from "
    "real use. It is a little shorter than the weekend bag is wide."
)

# ---------------------------------------------------------------- setting (locked)
# Same doctrine as MENSPACK v2: flat midday daylight in an ordinary room. A black bag on a
# dark floor goes muddy, so this build packs on plain white bedding — it separates the bag
# and makes the caramel interior read.
SETTING = (
    "The setting is an ordinary bright bedroom in the middle of the day: strong soft daylight "
    "pouring in from a large window just out of frame, plain white walls, a bed made up with "
    "plain white cotton bedding that is slightly rumpled, a pale wood floor, a phone charger "
    "cable and a folded pile of clothes left on a chair in the background, ordinary lived in "
    "mess. Plain flat daylight only: no lamps, no mood lighting, no golden glow, no evening "
    "warmth, just the slightly cool neutral light of a bright day coming through window glass, "
    "the way an unedited phone clip looks."
)

# ---------------------------------------------------------------- creator (locked)
HANDS = (
    "Only a man's hands and forearms are in frame: mid 20s, warm fair skin with natural texture, "
    "visible pores and fine hair on the forearms, short clean fingernails, a plain steel watch "
    "with a steel link bracelet on the left wrist, no rings, no tattoos, the rolled cuff of a "
    "plain washed navy overshirt visible at the edge of frame. No face, no head, no torso."
)

FULL_BODY = (
    "The man in frame is the exact same person as in the attached creator reference photo: mid "
    "20s, thick wavy medium brown hair, clean shaven, warm fair skin with natural texture and "
    "visible pores, a broad athletic build, wearing a plain washed navy overshirt with the "
    "cuffs rolled once over a white tee, straight dark indigo jeans and a plain steel watch on "
    "his left wrist, a few flyaway hairs, slight phone camera softness, never tack sharp, never "
    "airbrushed."
)

# ---------------------------------------------------------------- overhead camera (locked state)
# CALIBRATED 2026-08-11 to the S03 v1 probe. The originally authored state put the bag's
# long axis VERTICAL in the 9:16 frame; the model rendered it HORIZONTAL instead, and the
# render is better — the bag is wider than tall, so a horizontal long axis shows the whole
# mouth without cropping. Footage-wins rule: the block was rewritten to describe the frame
# that actually came back, so all 6 packing beats agree with the one already approved.
OVERHEAD = (
    "CAMERA STATE, identical in every overhead shot of this ad: the camera looks STRAIGHT DOWN "
    "from directly above the open bag, perfectly top down, never at a three quarter angle. The "
    "open bag lies on the plain white bedding with its LONG axis running ACROSS the frame from "
    "left to right, so the bag reads wider than it is tall in frame, and its open mouth is a "
    "wide oval filling the middle of the frame with plain white bedding visible above and below "
    "it. The folded back flap lies across the TOP of the frame, its black outer face turned up, "
    "its two keyhole shaped handle cutouts, its two plain leather strap slits and its single "
    "gold oval keyhole plate all clearly visible on it. The FRONT band of the bag, carrying the "
    "two short horizontal belt straps and their two gold clasp plates, runs across the BOTTOM of "
    "the frame, with the front rolled handle lying over it. The rear rolled handle arches up "
    "above the folded back flap at the very top of the frame. A small gold eyelet shows at the "
    "far left and far right edges of the mouth. This framing, position and scale are identical "
    "in every overhead shot, as if the phone never moved between takes."
)

# Wired alongside the geometry-anchor reference image (the approved S03 frame). The
# MENSPACK v3 trick: handing a QA-passed SIBLING frame to i2i and telling it to match
# proportions cures scale and elongation drift across independently authored stills.
GEOMETRY_ANCHOR = (
    "The LAST attached photo is a frame from earlier in this same phone video: it shows THIS "
    "exact black bag, open, on this exact bed, from this exact camera position. Match that "
    "photo EXACTLY for framing, orientation, proportions, the bag's size and position within "
    "the frame, the shape of the open mouth, the colour of the caramel lining and the lighting. "
    "The bag must be the same size and sit in the same place in the frame as it does in that "
    "photo. Do not zoom in, do not zoom out, do not rotate the bag and do not change the angle."
)

# 2026-08-11: the S03 probe rendered the jeans already resting on the interior floor rather
# than held in the air. It still read as placing rather than rearranging, so it passed — but
# every later beat gets this hardened clause so the accumulation never reads as fidgeting.
MIDAIR = (
    "THE ITEM BEING PACKED IS NOT YET IN THE BAG. It is held clearly ABOVE the rim of the bag, "
    "higher than the bag's top edge, still in the air, with the caramel interior and everything "
    "already packed fully visible in the gap of air beneath it. The hands are carrying it in "
    "from outside the bag. The hands are NOT rearranging, patting, folding or tidying anything "
    "that is already inside the bag."
)

# ---------------------------------------------------------------- cumulative contents map
# Fixed stated position per item. A scene's prompt includes, verbatim, the line of every
# item ALREADY in the bag plus the line of the item being added. Items never move once
# placed; that is what holds continuity across independently authored stills.
# Positions RE-EXPRESSED 2026-08-11 for the calibrated horizontal overhead geometry above
# (left end / centre / right end / far wall), matching where the S03 probe actually put the
# jeans. Left-to-right, not near-to-far.
CONTENTS = {
    "jeans":    "a pair of neatly folded dark indigo jeans lies flat in the CENTRE of the "
                "caramel interior",
    "stack":    "a neatly folded stack of a white cotton tee under a folded heather grey "
                "crewneck sweatshirt lies flat against the LEFT end of the interior",
    "dopp":     "a small structured black pebbled leather dopp kit stands against the RIGHT end "
                "of the interior",
    "shoebag":  "a cream cotton drawstring shoe bag with the rounded shape of a pair of sneakers "
                "inside it lies lengthwise along the FAR wall of the interior, behind the "
                "folded jeans",
    "tech":     "a flat plain black nylon tech pouch lies on top of the folded dark indigo jeans "
                "in the centre",
    "pocketed": "a navy passport and a pair of folded black sunglasses sit inside the wide "
                "caramel leather slip pocket against the far interior wall, their top edges "
                "just visible above the pocket's edge",
}

CONTENTS_ORDER = ["jeans", "stack", "dopp", "shoebag", "tech", "pocketed"]


def contents_so_far(upto_key, include=True):
    """The verbatim lines for everything packed before (and optionally including) upto_key."""
    idx = CONTENTS_ORDER.index(upto_key)
    keys = CONTENTS_ORDER[: idx + (1 if include else 0)]
    if not keys:
        return "The bag is completely empty, nothing is inside it and the caramel tan leather " \
               "lining is fully visible across the whole interior."
    lines = [CONTENTS[k] for k in keys]
    return ("ALREADY INSIDE THE BAG, exactly as in the previous shots and never moved: "
            + "; ".join(lines) + ".")


# ---------------------------------------------------------------- photoreal footer
PHOTOREAL = (
    "CRITICAL RENDERING INSTRUCTION. This is one frame of a casual vertical phone video, shot "
    "on an iPhone held in one hand, about to be uploaded to TikTok. It was filmed in the middle "
    "of an ordinary day in plain daylight with zero setup: no lighting equipment, no tripod, no "
    "styling, no colour grade. It is NOT a 3D render, NOT CGI, NOT a product visualisation, NOT "
    "Blender or Octane or Unreal or Keyshot, NOT ray traced, NOT a commercial or catalogue "
    "product photograph, NOT an advertisement, NOT retouched, NOT airbrushed, NOT studio lit, "
    "NOT cinematic, NOT moody, NOT atmospheric, NOT editorial. If it looks polished, styled, "
    "dramatic or computer generated it is wrong. The look is plain and a little unflattering: "
    "flat even daylight with the slightly cool white balance of phone auto exposure, the window "
    "side of the frame slightly blown out, visible sensor noise in the shadows, mild chromatic "
    "aberration on high contrast edges, faint JPEG compression artefacts, focus slightly "
    "imperfect so nothing is tack sharp, a trace of handheld motion blur, and framing a little "
    "crooked and off centre the way a real one handed phone shot is. Real surfaces: the black "
    "leather is creased, faintly scuffed and dulled where it has been handled, catching the "
    "window as a soft uneven sheen rather than a clean highlight, never a uniform polished "
    "finish and never a flat black silhouette with no detail in it; ordinary dust and lint are "
    "present on it. The room is a real lived in bedroom with ordinary clutter, not a set. No "
    "on-screen text, lettering, signage or graphics anywhere. Vertical 9:16."
)
