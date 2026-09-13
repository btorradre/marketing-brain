# Delphine B-roll library scenes, written to the Colette/Margot library standard.
# Each entry: (id, colorway, category, open_bag, scene, motion)
#
# WHY THIS FILE REPLACES THE FIRST DELPHINE LIBRARY (2026-08-16, Brooks):
#   "All of the b-roll still looks like it was created in a motion design software... Go study
#    the Colette B-Roll Library. That is exactly how we need to build out this B-Roll Library."
#
# The first Delphine library used the same two engines (GPT Image 2 -> Omni) and still read as
# motion design. Studying the Colette library against it, the engines were never the problem.
# Four things were:
#
#   1. RESOLUTION. Colette renders at 1K. I rendered at 2K. The extra resolution buys
#      over-resolved micro-detail that no phone produces and it is a large part of the CGI read.
#   2. THE SCENES WERE PRODUCT SHOTS, NOT MOMENTS. Mine were a bag placed centrally in a pretty
#      setting. Colette's are a person mid-stride at a crosswalk, a bag on the floor by a cafe
#      table leg shot past a latte, a bag on a passenger seat with sunflowers laid against it.
#      A human is in most frames with the face cropped out, wardrobe is specified every time,
#      and the crop is stated ("chest to knee crop", "from below", "from behind at waist height").
#   3. NO FOREGROUND. Colette shoots THROUGH things: a latte in the near foreground, a table edge,
#      a car dashboard. Foreground occlusion is what makes a frame read as a grabbed snapshot.
#   4. TOO FEW SCENES. Twelve shots cut into five ads is why they looked the same. Colette has 90
#      per bag across street, cafe, car, home, open-bag, packing, flat lay, macro and set-downs.
#
# Style rules carried over verbatim from the Colette file: simple sentences, commas and periods
# only, no em dashes, no on-screen text, faces never in frame, one colorway per frame, 9:16.

# Motion constants. Same set the Colette library used, minus its STILL push-in.
#
# Colette's STILL is "slow handheld push in toward the bag". That is safe on a 50cm tote and NOT
# safe here: every push-in on the Delphine inflated it, and B11 once opened as a handbag and
# ended as a weekender. On a 25cm bag a push-in destroys the size read. HOLD replaces it.
HOLD     = ("Slow handheld hold on the bag with a gentle natural sway and small breathing motion, as if "
            "someone is holding a phone. The camera never moves closer to the bag and never zooms, so the "
            "bag stays the same size in frame from the first moment to the last. Everything in the scene "
            "stays where it is and every detail of the bag stays exactly as in the image.")
DRIFT    = ("Very slow handheld drift sideways across the scene with slight focus breathing, the camera "
            "holding the same distance from the bag throughout so the bag never grows in frame. Every "
            "detail of the bag stays exactly as in the image, nothing on the bag moves or changes shape.")
OVERHEAD = ("Slow overhead handheld drift with a slight wobble, holding the same height above the scene "
            "throughout. The contents settle naturally but the bag itself stays exactly as in the image.")
WALK_AWAY= ("She keeps walking away from the camera at a relaxed pace and the bag sways gently with her "
            "stride. Handheld follow with natural footstep bounce, holding the same distance behind her. "
            "The bag keeps its exact shape and details.")
WALK_BY  = ("She walks past the camera at a relaxed pace and the bag swings gently at her side. Handheld "
            "with natural shake, the camera panning to follow rather than moving toward her. The bag keeps "
            "its exact shape and details.")
CARRY    = ("She shifts her weight slightly and the bag moves with her arm in tiny natural motions. "
            "Handheld camera with a soft sway at a constant distance. The bag keeps its exact shape and "
            "details.")
MACRO    = ("Extremely slow macro drift sideways across the surface with shallow focus breathing, never "
            "moving in toward the bag. Nothing in the scene moves. Every detail of the bag stays exactly "
            "as in the image.")
HANDS    = ("Her hands move in small natural motions to place the item and then withdraw. Handheld camera "
            "at a constant distance with a soft sway. The bag itself does not move and every detail of it "
            "stays exactly as in the image.")

SCENES = []
d = [

# --- A. Street and carry (12): LC x6, DC x4, AG x2 -------------------------------------------
("street-crosswalk-back", "LC", "carry", False,
 "A photo taken from behind of a woman mid stride crossing a city crosswalk on an overcast fall morning. She wears a long camel wool coat, straight leg jeans and leather ankle boots, and carries the bag by its top handles in her right hand so it swings near her hip. Her head is turned slightly so no face is visible. A few fallen leaves sit in the gutter and the far pedestrians are out of focus.",
 WALK_AWAY),
("street-crook-elbow", "LC", "carry", False,
 "A chest to knee crop of a woman standing on a quiet sidewalk with the bag in the crook of her elbow at hip height. She wears an oversized grey knit sweater and dark trousers, no face in frame. Soft overcast daylight, a brick storefront blurred behind her.",
 CARRY),
("street-coffee-run", "DC", "carry", False,
 "A mid body crop of a woman on a fall sidewalk holding a paper coffee cup in one hand and the bag by its handles in the other. Cream cardigan, gold ring on her finger, no face in frame. Morning sun rakes across the pavement behind her.",
 CARRY),
("street-walking-side", "LC", "carry", False,
 "A side view of a woman walking past old brownstone steps carrying the bag by both top handles so it swings near her knee. Long black coat and cream scarf, face out of frame above the shoulders. Late afternoon golden light.",
 WALK_BY),
("street-stairs-down", "DC", "carry", False,
 "A photo from below of a woman coming down wide stone museum steps with the bag in one hand. Plaid wool skirt, black tights, loafers, her face cropped out by the top of the frame. Cold bright fall daylight.",
 WALK_BY),
("street-leaves-path", "LC", "carry", False,
 "A photo from behind at waist height of a woman walking down a leaf covered park path, the bag swinging softly from her hand. Trench coat and white sneakers, fallen yellow leaves everywhere, low afternoon sun flaring slightly into the lens.",
 WALK_AWAY),
("street-shopfront-pause", "AG", "carry", False,
 "A photo of a woman from the shoulders down standing in front of a flower shop window with the bag in the crook of her arm and her other hand resting on the handles. Chunky cream knit and dark jeans. Buckets of dahlias blur in the window behind her.",
 CARRY),
("street-crossing-front", "LC", "carry", False,
 "A photo of a woman walking straight toward the camera on a wet city street, cropped at the collarbone, the bag held down at her side in one hand. Belted camel coat, wet asphalt reflecting shop lights behind her.",
 WALK_BY),
("street-bakery-door", "DC", "carry", False,
 "A waist down photo of a woman pushing open a bakery door with her shoulder, the bag hanging from the hand that also holds her keys. Dark wool trousers, worn leather boots, warm light spilling out of the doorway onto the pavement.",
 CARRY),
("street-bus-stop", "LC", "carry", False,
 "A photo from the side of a woman waiting at a bus shelter with the bag resting on the bench beside her thigh, her hand loosely over the handles. Grey overcast light, city traffic blurred behind the glass.",
 CARRY),
("street-phone-check", "AG", "carry", False,
 "A chest down photo of a woman stopped on a sidewalk looking at her phone in one hand, the bag hanging from the other. Oatmeal knit and dark denim, a plane tree trunk and railings soft behind her.",
 CARRY),
("street-market-stall", "DC", "carry", False,
 "A photo of a woman from the shoulders down at an outdoor produce stall, the bag over her forearm while she reaches for a bunch of grapes. Navy peacoat, crates of fruit filling the blurred background.",
 CARRY),

# --- B. Cafe and indoor tables (8): LC x4, DC x2, AG x2 ---------------------------------------
("cafe-floor-table-leg", "LC", "cafe", False,
 "A photo of the bag standing on the floor beside a cafe table leg, shot from table height so a latte in a ceramic cup sits large and out of focus in the near foreground and the bag is sharp below it. Terrazzo floor, warm afternoon light.",
 HOLD),
("cafe-window-counter", "DC", "cafe", False,
 "A photo of the bag on a wooden window counter of a coffee shop with the city street soft behind the glass. A book lies face down next to it with a pair of reading glasses on top. Late golden light through the window.",
 HOLD),
("cafe-bistro-chair", "LC", "cafe", False,
 "A photo of the bag sitting on the cane seat of a bistro chair pulled out from a marble table, shot from standing height at a slight angle. An espresso cup and a crumpled napkin sit on the table edge in the blurred foreground.",
 HOLD),
("cafe-banquette", "AG", "cafe", False,
 "A photo of the bag on a green velvet banquette beside a woman's hip, cropped at her waist, her hand resting on the seat next to it. Warm low restaurant light, a wine glass base blurred in the foreground.",
 HOLD),
("cafe-terrace-table", "LC", "cafe", False,
 "A photo of the bag standing on a small round outdoor cafe table shot from a seated person's eye level, one knee in dark denim just inside the bottom of the frame. A saucer with a spoon and a folded receipt beside it, low autumn sun flaring from behind.",
 DRIFT),
("cafe-checkout-setdown", "DC", "cafe", False,
 "A photo of the bag set down on a cafe counter next to a card reader while a woman's hand, cropped at the wrist, reaches past it. Pastry case glass glowing warm and out of focus behind.",
 HANDS),
("cafe-rainy-window", "LC", "cafe", False,
 "A photo of the bag on a table beside a rain streaked cafe window, cold grey daylight through the water on the glass, a half drunk cup of tea in the soft foreground.",
 HOLD),
("cafe-communal-table", "AG", "cafe", False,
 "A photo of the bag on a long communal wooden table between a laptop closed flat and a stack of two books, other diners far out of focus down the table. Overhead pendant light pooling warm on the wood.",
 DRIFT),

# --- C. Car (5): LC x3, DC x1, AG x1 ----------------------------------------------------------
("car-passenger-seat", "LC", "car", False,
 "A photo of the bag standing upright on a grey cloth passenger seat with the seat belt buckle lying beside it, golden hour light striping across it through the side window. An iced coffee in the cup holder sits blurred in the near foreground.",
 HOLD),
("car-seat-flowers", "LC", "car", False,
 "A photo of the bag on a car passenger seat with a paper wrapped bunch of sunflowers laid against it and a phone tossed beside it. Dust motes in the warm light, dashboard blurred across the top of the frame.",
 HOLD),
("car-footwell-groceries", "DC", "car", False,
 "A photo looking down into a car footwell where the bag stands upright next to a paper grocery bag with celery leaves poking out. Late afternoon light through the open door, the door sill in the foreground.",
 HOLD),
("car-door-open", "LC", "car", False,
 "A photo from outside a parked car of the bag on the passenger seat through the open door, a woman's hand cropped at the wrist reaching in for the handles. Street trees reflected in the window glass.",
 HANDS),
("car-console-latte", "AG", "car", False,
 "A photo of the bag wedged upright between the passenger seat and the centre console with a takeaway cup in the holder in front of it. Windscreen light blown out at the top of the frame, dashboard dust visible.",
 HOLD),

# --- D. Home still life (10): LC x5, DC x3, AG x2 ---------------------------------------------
("home-entry-bench", "LC", "home", False,
 "A photo of the bag on a wooden entryway bench with a pair of loafers underneath and a coat sleeve hanging into the top of the frame. Morning light from a nearby window falling across the floorboards.",
 HOLD),
("home-bed-morning", "LC", "home", False,
 "A photo of the bag lying on a rumpled linen duvet in morning light, the duvet creased and not smoothed out, a folded jumper at the edge of the frame.",
 DRIFT),
("home-closet-shelf", "DC", "home", False,
 "A photo of the bag standing on a white closet shelf at eye level among folded sweaters in cream and grey tones, a shoebox stacked beside it and one shelf light glowing softly above.",
 HOLD),
("home-console-keys", "LC", "home", False,
 "A photo of the bag on a narrow hallway console table with a set of keys, an unopened envelope and a small dish beside it. A mirror edge catches soft daylight at the side of the frame.",
 HOLD),
("home-kitchen-counter", "AG", "home", False,
 "A photo of the bag on a kitchen island counter next to a bowl of pears and a French press mid brew with steam curling up. Morning window light across the marble with real crumbs near the sink.",
 HOLD),
("home-sofa-corner", "LC", "home", False,
 "A photo of the bag slumped against the arm of a linen sofa with a throw blanket half pulled off the seat, low lamp light from the right.",
 HOLD),
("home-floor-lean", "DC", "home", False,
 "A photo of the bag standing on a wooden floor leaning against a plaster wall, shot from low down so the skirting board runs across the frame, late afternoon sun laying a long window shape on the boards.",
 DRIFT),
("home-hook-hallway", "LC", "home", False,
 "A photo of the bag hanging by its top handles from a brass hook in a hallway with a wool coat hanging beside it, cropped so only the coat body shows. Dim hallway light with a bright doorway glowing behind.",
 HOLD),
("home-desk-chair", "AG", "home", False,
 "A photo of the bag on the seat of a wooden desk chair pushed under a desk, a laptop corner and a mug visible on the desk above in soft focus. Cool north light from a window on the left.",
 HOLD),
("home-stairs", "DC", "home", False,
 "A photo of the bag sitting on a carpeted stair tread halfway up a staircase, shot from the bottom looking up, banister rails blurred across the foreground.",
 HOLD),

# --- E. Open bag overhead (4): LC x3, DC x1. AG has no interior photograph -----------------
("open-overhead-daily", "LC", "open", True,
 "An overhead photo looking down into the open top of the bag standing on a linen duvet. Inside, a small folded wallet, a set of keys, a lip balm and two cards sit loosely at the bottom. The interior lining and its zip pocket are clearly visible.",
 OVERHEAD),
("open-overhead-counter", "LC", "open", True,
 "A photo at a sixty degree angle looking into the open bag on a marble kitchen counter, a folded wallet and a set of keys inside. A mug and a folded tea towel sit blurred behind it.",
 OVERHEAD),
("open-bench-angle", "DC", "open", True,
 "A photo of the open bag on an entryway bench shot from above and slightly to the side, the interior lining catching the light, a wallet resting against the inside wall.",
 OVERHEAD),
("open-lap-car", "LC", "open", True,
 "A photo looking down into the open bag held on a woman's lap in a car passenger seat, her knees in dark denim framing the bottom of the shot, one hand resting on the rim.",
 OVERHEAD),

# --- F. Packing actions (6): LC x4, DC x1, AG x1 ----------------------------------------------
("pack-wallet-in", "LC", "packing", True,
 "A photo of a woman's hand, cropped at the wrist, lowering a small folded wallet down into the open bag on a marble kitchen counter. A mug and a set of keys sit blurred behind it in warm side light.",
 HANDS),
("pack-keys-drop", "LC", "packing", True,
 "A photo of a hand dropping a set of keys into the open bag on an entryway bench, the keys caught mid fall just above the opening. Bright doorway light behind.",
 HANDS),
("pack-lipbalm", "DC", "packing", True,
 "A close photo of a hand tucking a lip balm down the inside edge of the open bag, the interior lining and zip pocket visible beside it. Soft window light from the left.",
 HANDS),
("pack-card-slip", "LC", "packing", True,
 "A photo of fingers slipping two cards into the zip pocket inside the open bag on a bed, the duvet creased around it, morning light raking across the fabric.",
 HANDS),
("pack-pickup-handles", "AG", "packing", False,
 "A photo of a hand closing around both rolled top handles of the closed bag on a hallway console, about to lift it, the handles compressing slightly under the grip.",
 HANDS),
("pack-setdown-counter", "LC", "packing", False,
 "A photo of the closed bag being set down onto a kitchen counter, a hand still on the handles, the bag just meeting the surface. Morning light, a bowl of fruit soft behind.",
 HANDS),

# --- G. What fits flat lay (3): LC x2, DC x1 --------------------------------------------------
("flatlay-daily", "LC", "flatlay", False,
 "An overhead photo on a rumpled linen bedspread of the closed bag at the bottom of the frame with a small folded wallet, two cards, a set of keys on a ring and a lip balm scattered loosely above it, not arranged. A woman's hand rests at the corner of the frame. There are no sunglasses and no phone anywhere in the picture.",
 OVERHEAD),
("flatlay-counter", "DC", "flatlay", False,
 "An overhead photo on a marble counter of the closed bag beside a wallet, a set of keys and a lip balm, a folded tea towel at the edge of the frame. Hard morning light throwing crisp shadows. There are no sunglasses and no phone anywhere in the picture.",
 OVERHEAD),
("flatlay-bench", "LC", "flatlay", False,
 "An overhead photo on a wooden entry bench of the closed bag with a wallet and keys beside it and a pair of loafers just inside the bottom edge of the frame. Soft daylight from a doorway.",
 OVERHEAD),

# --- H. Macro details (8): LC x5, DC x2, AG x1 ------------------------------------------------
("macro-side-buckle", "LC", "macro", False,
 "An extreme close up of the small gold roller buckle on the side gusset of the bag with the leather belt strap running into it, the pin through a hole in the strap. Raking window light, the canvas soft and out of focus behind.",
 MACRO),
("macro-turnlock", "LC", "macro", False,
 "A macro photo of the gold turn lock at the front centre of the leather band, the knurled edge catching warm light, a faint fingerprint on the metal, stitching soft on either side.",
 MACRO),
("macro-feet", "DC", "macro", False,
 "A very low close photo along the bottom edge of the bag where the small gold feet lift the canvas just clear of a worn stone step, grit and a dry leaf beside them.",
 MACRO),
("macro-leather-grain", "LC", "macro", False,
 "An extreme close up of the leather flap surface in raking light so the natural grain and a soft crease across it catch the light, the stitch line running diagonally through the frame.",
 MACRO),
("macro-canvas-weave", "AG", "macro", False,
 "An extreme close up of the canvas body of the bag in side light so the individual woven fibres and small slubs are visible, a leather corner patch curving into one side of the frame.",
 MACRO),
("macro-handle-base", "LC", "macro", False,
 "A macro photo of where one rolled leather top handle meets the leather band, the stitching and the slight compression in the rolled leather visible, warm light from above.",
 MACRO),
("macro-clochette", "DC", "macro", False,
 "A macro photo of the small leather clochette tag hanging on its long tab against the canvas, turning very slightly, the stitching along its edge in focus.",
 MACRO),
("macro-corner-patch", "LC", "macro", False,
 "A close photo of one leather corner patch at the base of the bag where it meets the canvas, the edge paint and stitch line visible, a scuff worn into the leather.",
 MACRO),

# --- I. Set down and pick up (2) --------------------------------------------------------------
("setdown-cafe-floor", "LC", "setdown", False,
 "A photo from a seated height of a hand lowering the bag onto a cafe floor beside a chair leg, the bag just about to touch the terrazzo. A table edge crosses the top of the frame out of focus.",
 HANDS),
("setdown-bench-stand", "DC", "setdown", False,
 "A photo of the bag just released onto a park bench, a hand withdrawing out of the top of the frame, the bag standing square on its gold feet on the weathered slats with leaves caught between them.",
 HANDS),
]

for i, (sid, cw, cat, ob, scene, motion) in enumerate(d, 1):
    SCENES.append((f"VEL-DEL-{i:03d}-{sid}", cw, cat, ob, scene, motion))
