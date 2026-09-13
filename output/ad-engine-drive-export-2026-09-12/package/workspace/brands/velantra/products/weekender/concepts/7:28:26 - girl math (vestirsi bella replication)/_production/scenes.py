"""Girl Math — scene definitions. Prompts are the brief's, with BAG BLOCK / ANTI-DRIFT resolved."""

BAG = ("a structured two tone weekend bag, wider than tall, rich cognac brown leather upper flap "
       "section and two rolled cognac leather top handles over a cream ivory woven canvas body, a "
       "small gold oval turn lock on the front, two flat gold clasp plates with cognac leather belt "
       "straps threaded through them, a small cognac leather key bell tied to the handle base, "
       "cognac leather corner patches at the bottom, visible stitching, gold hardware, no logos "
       "anywhere on the bag")

DRIFT = ("the bag in frame is an exact copy of the bag in the attached photo in silhouette, "
         "proportions, materials and details, the two rolled top handles are smooth simple leather "
         "tubes with no wrapping, no braiding and no woven texture")

# v1 of this block was just "raw unedited iPhone photo, available light only, no studio
# lighting" and every frame came back looking like a 3D product render. Two causes: the
# negative was far too weak, and the i2i reference is a clean white-background catalogue
# shot whose rendering aesthetic the model inherited wholesale. Both are addressed below.
RAW = (
    "CRITICAL RENDERING INSTRUCTION. This is a real photograph casually taken on an iPhone 15 "
    "Pro by an ordinary person, handheld, in one second, with no lighting equipment, no tripod "
    "and no styling. It is NOT a 3D render, NOT CGI, NOT a product visualisation, NOT Blender "
    "or Octane or Unreal or Keyshot, NOT ray traced, NOT a commercial or catalogue product "
    "photograph, NOT an advertisement, NOT retouched, NOT airbrushed, NOT studio lit. If it "
    "looks polished or computer generated it is wrong. "
    "Photographic evidence that must be present: visible digital sensor noise and grain through "
    "the shadows and midtones, highlights slightly blown out where the light source hits, mild "
    "chromatic aberration on high contrast edges, faint JPEG compression artefacts, focus that "
    "is slightly imperfect so nothing is tack sharp, a trace of handheld motion blur, and "
    "framing that is a little crooked and off centre the way a real snapshot is. "
    "Real light only: one dominant available light source, mixed colour temperature across the "
    "frame, uneven exposure, and real shadows falling off naturally with visible ambient bounce. "
    "Real surfaces: the leather is creased, faintly scuffed, unevenly grained and dulled where "
    "it has been handled, never a uniform polished finish; the canvas shows individual woven "
    "fibres, slubs and small wrinkles; ordinary dust, lint and fingerprints are present. The "
    "setting is a real lived-in place with ordinary clutter, not a set. "
    "No on-screen text, lettering, signage or graphics anywhere. Vertical 9:16."
)

# The reference is a catalogue cutout on white. Say out loud that only its geometry and
# materials transfer, or the frame comes back looking like the catalogue.
REF = ("Use the attached photo ONLY as the reference for the bag's shape, proportions, "
       "materials, colours, stitching and hardware. Do NOT copy its lighting, its white "
       "background, its clean edges or its polished studio product-photo look. That attachment "
       "is a catalogue image and the picture you produce must not resemble one. Create ")

SCENES = [
    dict(
        id="A", name="restaurant chair, evening", i2i=True,
        keyframe=REF + "a candid iPhone photo of " + BAG + ", sitting closed and upright on the "
        "seat of an empty chair at a restaurant table in the evening. Warm low restaurant light, a "
        "water glass and folded napkin softly out of focus on the table edge behind it, other "
        "diners blurred far in the background. The bag is fully closed, belt straps fastened flat, "
        "flap down. " + RAW,
        motion="Animate this exact frame. The camera drifts in very slowly toward the bag while "
        "warm light shifts gently and blurred people move far behind. The bag itself does not move "
        "at all. Straps stay fastened, flap stays down, nothing on the bag changes. Vertical 9:16.",
    ),
    dict(
        id="B", name="overhead bin", i2i=True,
        keyframe=REF + "a candid iPhone photo taken from just below, looking up into an open "
        "aircraft overhead bin, with " + BAG + " resting inside the bin, closed and upright, "
        "filling it neatly with room to spare. A woman's hands hold the two rolled cognac leather "
        "top handles. Cabin ceiling and bin lighting, other passengers blurred in the aisle behind. "
        "Her hands touch only the rolled handles, never the belt straps and never the flap. The bag "
        "is fully closed, belt straps fastened flat. " + RAW,
        motion="Animate this exact frame. Her hands slide the closed bag a few inches further into "
        "the bin and let go, then the camera holds. The bag stays completely rigid and closed the "
        "entire clip. Her hands never touch the belt straps, the turn lock or the flap. No straps "
        "ever unfasten, no flap ever lifts. Vertical 9:16.",
    ),
    dict(
        id="C", name="three bags at the gate", i2i=False,
        keyframe="Create a candid iPhone photo looking down at a woman's feet at an airport "
        "departure gate, with three plain unbranded bags crowded around her: a small black "
        "hard-shell rolling carry-on, a slouchy beige canvas tote tipped over on its side, and a "
        "plain grey nylon backpack on the floor. A jacket is draped over the tote, a phone charger "
        "cable trails out of the backpack, a boarding pass sticks out of a pocket. Grey airport "
        "carpet, rows of gate seating and a window with a plane blurred behind. Cluttered and "
        "slightly chaotic. No logos, brand marks or lettering on any bag. " + RAW,
        motion="Animate this exact frame. The camera tilts slowly down across the three bags while "
        "she shifts her weight and travellers move past blurred in the background. The bags stay "
        "exactly as they are. No text or signage appears anywhere. Vertical 9:16.",
    ),
    dict(
        id="D", name="leather and canvas seam macro", i2i=True,
        keyframe=REF + "an extreme macro iPhone photograph of the front of this bag where the rich "
        "cognac brown leather upper section meets the cream ivory woven canvas body: the horizontal "
        "seam and its visible stitching fill the frame in sharp detail, the small gold oval turn "
        "lock catching light at the edge of frame, the grain of the leather and the weave of the "
        "canvas both clearly readable. Natural window light raking across the surface. " + RAW,
        motion="Animate this exact frame. The camera drifts very slowly along the stitched seam "
        "while soft daylight moves across the leather grain. Nothing else moves. The seam stays in "
        "exactly the same place, the leather and canvas never change proportion, no hardware is "
        "added. Vertical 9:16.",
    ),
    dict(
        id="E1", name="terminal corridor walk", i2i=True,
        keyframe=REF + "a candid iPhone photo from behind of a woman in her late thirties walking "
        "away down a long bright airport terminal corridor in cream trousers and a soft camel knit, "
        "carrying " + BAG + " closed at her side by its two rolled cognac leather top handles. Late "
        "afternoon light through the terminal windows, travellers blurred ahead of her. " + DRIFT +
        ". The bag is fully closed, belt straps fastened flat. No signage text or lettering "
        "readable anywhere. " + RAW,
        motion="Animate this exact frame. She walks away at an easy pace, the closed bag swinging "
        "gently at her side, the camera following a few steps behind. The bag stays rigid, closed "
        "and unchanged the entire clip, straps fastened, flap down, hardware never changes. No text "
        "appears on any sign. Vertical 9:16.",
    ),
    dict(
        id="E2", name="restaurant entrance at dusk", i2i=True,
        keyframe=REF + "a candid iPhone photo of a woman in her late thirties seen from behind, "
        "stepping through the doorway of a warmly lit restaurant at dusk, in a simple black dress, "
        "carrying " + BAG + " closed at her side by its two rolled cognac leather top handles. Warm "
        "amber light spilling out of the doorway, blue evening street behind her. " + DRIFT + ". "
        "The bag is fully closed, belt straps fastened flat. No signage text or lettering readable "
        "anywhere. " + RAW,
        # v1 motion FAILED QA: Omni built the interior as a handbag boutique with lit display
        # cases and other bags on the shelves. Wrong location, and it put competitor-looking
        # bags on screen. The interior now has to be named explicitly and retail banned.
        motion="Animate this exact frame. She steps forward through the doorway into the warm "
        "light of a busy restaurant dining room, the closed bag swinging gently at her side, the "
        "camera drifting after her. The room she enters is a restaurant: dining tables with white "
        "napkins, wooden chairs, wine glasses and seated diners eating. It is NOT a shop and NOT "
        "a boutique. No display cases, no glass cabinets, no shelves of merchandise, no handbags "
        "or products on display anywhere, no other bags in the room at all. The bag stays rigid, "
        "closed and unchanged the entire clip. No text appears on any sign. Vertical 9:16.",
    ),
    dict(
        id="F", name="front door departure", i2i=True,
        keyframe=REF + "a candid iPhone photo of " + BAG + " sitting closed and upright on the "
        "floor of a quiet entryway beside a front door, early morning light coming through the "
        "door's glass panel and falling across the canvas. A pair of shoes and a set of keys on a "
        "small console table nearby. The bag is fully closed, belt straps fastened flat. " + RAW,
        # v1 motion (hand lifts the bag) FAILED QA — Omni deformed the silhouette mid-lift.
        # Replaced with a static hold. Nothing enters frame, nothing is manipulated.
        motion="Animate this exact frame. The camera pushes in very slowly toward the closed bag "
        "while the early morning light through the door glass creeps gradually across the canvas "
        "and the leather. The bag does not move at all and nothing enters the frame. Straps stay "
        "fastened, flap stays down, the bag stays completely rigid and unchanged for the entire "
        "clip. Vertical 9:16.",
    ),
]

# The 2026-07-10/11 library clips carry the same 3D-render look the v1 keyframes did, so the
# five slots that reused them are regenerated here rather than left to clash with the new
# photographic ones. MECH is the skill's verbatim open-bag block, colourway resolved.
MECH = (
    "Open bag construction: the open bag keeps the exact same two tone split as the closed bag "
    "in the reference image. The entire upper section of the bag body, across the front, the "
    "back and both sides, is smooth rich cognac brown leather, exactly as deep as the cognac "
    "leather upper section on the closed reference bag, and everything below it is cream ivory "
    "woven canvas. Folding the flap back does NOT change this split: the line where the leather "
    "ends and the canvas begins sits in exactly the same place as on the closed reference bag. "
    "The two rolled cognac leather top handles are anchored directly into this wide leather "
    "upper band with sturdy leather bases, never into the canvas. Two thin gold posts stand "
    "upright on the leather band, and the small gold oval turn lock is mounted on the leather "
    "band at the top center of the front. The two cognac leather belt straps hang loose and "
    "unfastened down the front with their gold clasp plates. The wide leather band on the front "
    "is plain smooth leather and is part of the bag body: no tab sections, no scalloped edges, "
    "no pocket shape, no turn lock pocket, it is not a flap. The entire cognac leather flap, one "
    "single piece, is folded backward over the top rear edge of the bag and leans back behind "
    "the open mouth, clearly visible from the front: the inside face of the flap stands behind "
    "the opening showing its two round handle holes, its strap slots and its small gold plate, "
    "with the rear rolled handle rising above it. The flap never covers the front of the bag and "
    "never splits into pieces. The mouth of the bag is a clean open oval at the top of the "
    "leather section, showing the natural cream cotton canvas interior lining and the cognac "
    "leather slip pocket on the back interior wall. The bag has NO zipper anywhere, no zipper "
    "track, no zipper teeth, no zipper pull along the mouth of the bag, and no embossed text or "
    "lettering anywhere on the bag. BOTH handles are clearly visible standing upright: the front "
    "handle rises from the front leather band, the rear handle rises from the back leather band "
    "in front of the folded back flap. Never omit the front handle."
)

SCENES += [
    dict(
        id="G", name="airport gate seating", i2i=True,
        keyframe=REF + "a photo of " + BAG + ", sitting closed and upright on a row of black "
        "airport gate seating, a departure window with grey daylight and a parked aircraft "
        "blurred far behind it, a few travellers out of focus further down the row. The bag is "
        "fully closed, belt straps fastened flat, flap down. " + RAW,
        motion="Animate this exact frame. The camera drifts in slowly toward the bag while "
        "travellers move blurred in the background. The bag does not move at all. Straps stay "
        "fastened, flap stays down, nothing on the bag changes. Vertical 9:16.",
    ),
    dict(
        id="H", name="kitchen counter morning", i2i=True,
        keyframe=REF + "a photo of " + BAG + ", sitting closed and upright on a kitchen counter "
        "in the morning, a set of keys and a half-drunk mug of coffee beside it, ordinary "
        "kitchen clutter softly out of focus behind. Grey morning light through a window off to "
        "one side. The bag is fully closed, belt straps fastened flat, flap down. " + RAW,
        motion="Animate this exact frame. The camera pushes in very slowly toward the bag while "
        "the morning light shifts faintly. The bag does not move at all. Straps stay fastened, "
        "flap stays down, nothing on the bag changes. Vertical 9:16.",
    ),
    dict(
        id="I", name="packed at the foot of the bed", i2i=True,
        keyframe=REF + "a photo of " + BAG + ", sitting closed and packed at the foot of a made "
        "bed in an ordinary bedroom, a folded jumper and a phone charger on the duvet beside it, "
        "soft daylight from a window off frame. The bag is fully closed, belt straps fastened "
        "flat, flap down. " + RAW,
        motion="Animate this exact frame. The camera drifts slowly across the bag while the "
        "daylight shifts faintly. The bag does not move at all. Straps stay fastened, flap stays "
        "down, nothing on the bag changes. Vertical 9:16.",
    ),
    dict(
        id="J", name="hotel luggage rack, holding its shape", i2i=True,
        keyframe=REF + "a photo of " + BAG + ", sitting closed and standing upright and square "
        "on a folding hotel luggage rack in a hotel room, clearly not stuffed full but holding "
        "its shape with no sagging or slumping anywhere, a rumpled bed and a bedside lamp softly "
        "out of focus behind. Warm lamp light mixed with grey daylight from a window. The bag is "
        "fully closed, belt straps fastened flat, flap down. " + RAW,
        motion="Animate this exact frame. The camera moves very slowly around the bag while the "
        "lamp light shifts faintly. The bag does not move and does not deform at all, it holds "
        "its square upright shape for the entire clip. Straps stay fastened, flap stays down. "
        "Vertical 9:16.",
    ),
    dict(
        id="K", name="open packed bag", i2i=True, refs="open",
        keyframe="Use the first attached photo as the exact reference for how this bag opens and "
        "the second attached photo as the reference for its materials and colours. Keep the open "
        "bag EXACTLY as the first reference is constructed. Do NOT copy either attachment's "
        "lighting or polished product-photo look. Create a photo, looking down into this bag "
        "sitting open and packed on a bed, a folded cream cable knit jumper, folded dark jeans, "
        "a small cognac leather pouch and a rolled pair of socks visible inside it, soft daylight "
        "from a window off frame. The only zipper in the entire scene belongs to the small pouch. "
        + MECH + " " + RAW,
        motion="Animate this exact frame. The camera pushes in very slowly toward the open mouth "
        "of the bag. Nothing is touched, nothing is moved, no hands enter the frame. The flap "
        "stays one single piece leaning back behind the opening for the entire clip, the wide "
        "leather band keeps exactly the same depth, and no zipper ever appears on the bag. "
        "Vertical 9:16.",
    ),
]

SCRIPT_MAIN = (
    "Girl math is buying one bag that gets you from the Friday morning flight to Saturday night "
    "dinner without checking anything. This is the Eleanor Weekender from Velantra. It holds three days and it "
    "still slides into the overhead bin. I used to travel with a carry on, plus a tote, plus a "
    "personal item I kept repacking at the gate. Now I just take this one. Three days of clothes, "
    "a pair of shoes, my toiletries, and it still shuts flat. The leather is full grain over woven "
    "canvas, and the frame holds its shape, so it never slumps when it's half empty. I've walked "
    "an airport all day with it, then carried it straight into dinner. I bought it for one "
    "weekend. It hasn't stayed home since."
)

HOOK_B = ("The math on this one is easy. One bag, three days, and I stopped paying to check a "
          "suitcase.")
HOOK_C = "I stopped travelling with three bags the weekend I bought this one."
HOOK_A = ("Girl math is buying one bag that gets you from the Friday morning flight to Saturday "
          "night dinner without checking anything.")

SCRIPTS = {
    "v1": SCRIPT_MAIN,
    "hookb": SCRIPT_MAIN.replace(HOOK_A, HOOK_B),
    "hookc": SCRIPT_MAIN.replace(HOOK_A, HOOK_C),
}
