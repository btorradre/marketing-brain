# 100-clip organic B-roll manifest for the Colette wool tote.
# Every entry: id, category, colorway, open_bag, creator, cam (height, angle, distance, movement, orientation, action, human, env, light),
# scene (keyframe prompt middle), motion (Omni motion body), pattern (TikTok research pattern), dur, engine (omni|kenburns)
# Laws baked in: hand or forearm carry only (short drop), one colorway per frame, faces out of frame or hidden, no text,
# no logos, plausible placement (never a public floor), props unbranded, felt not knit, side gusset clean.

CREATORS = {
 "A": "a woman in her early 30s with long dark brown hair, natural short nails and a thin gold ring",
 "B": "a woman in her late 20s with a blonde bob, pale skin and a silver watch",
 "C": "a woman in her 40s with auburn shoulder-length hair and a few freckles on her hands",
 "D": "a woman in her 50s with silver-blonde hair pulled back and a simple gold wedding band",
 "E": "a woman in her mid 20s with a light brown ponytail and a claw clip, no jewellery",
 "F": "a woman in her mid 30s with dark blonde waves and a gold chain bracelet",
 "G": "a woman in her 60s with a silver bob and soft weathered hands",
 "H": "a woman around 30 with curly red hair and short dark painted nails",
}
FACE = " Her face is out of the frame, cropped away by the top edge of the picture, and she is not holding a phone; someone else is filming her."

def C(id, cat, cw, open_bag, creator, height, angle, dist, move, orient, action, human, env, light, scene, motion, pattern, dur=6, engine="omni"):
    return dict(id=id, category=cat, colorway=cw, open_bag=open_bag, creator=creator, camera_height=height, camera_angle=angle,
                camera_distance=dist, camera_movement=move, product_orientation=orient, product_action=action, human_action=human,
                environment=env, lighting=light, scene=scene, motion=motion, pattern=pattern, duration=dur, engine=engine)

# common motion bodies
HOLD = "Handheld phone footage with a gentle natural sway and tiny hand shake, slight focus breathing. The scene holds, small natural movements only."
PUSH = "Slow handheld push in toward the bag with natural hand shake, as if the person filming steps a little closer, slight focus breathing."
DRIFT = "Slow handheld drift sideways across the scene with slight wobble and one small refocus."

CLIPS = [
# ---------------- 01 PRODUCT ANGLES (8) ----------------
C("COL-001","01_Product_Angles","caramel",False,None,"waist","front","full product","handheld","front","resting","none","bedroom","window light",
  "The bag stands on the edge of a bed on a rumpled white duvet, seen straight on from waist height, filling most of the frame width. A bedside lamp and a stack of books blur behind it. Soft grey window light from the left, slightly underexposed, framing a touch crooked.",
  HOLD, "front-on full product at waist height in a bedroom, the single most common product framing (48% of shots front, bedroom 28% of environments)"),
C("COL-002","01_Product_Angles","caramel",False,None,"chest","behind subject","full product","handheld","back","resting","none","bedroom","warm indoor",
  "The back face of the bag as it sits on top of a wooden dresser, filmed from chest height, a little off centre. A jewellery dish and a half-open drawer are in frame, a lamp glows warm to the right. Evening indoor light, some grain.",
  HOLD, "back orientation appears in only 2% of organic shots, added so an editor has the rear face"),
C("COL-003","01_Product_Angles","espresso",False,None,"waist","side profile","full product","handheld","right side","resting","none","hallway","window light",
  "A true side profile of the bag standing on a wooden entry bench in a hallway, the clean felt gusset toward camera, belt ends and their gold disc caps visible curving on the faces beyond. A coat hangs on a hook above, keys beside the bag. Daylight from a door glass, slightly cool.",
  DRIFT, "side profile is rare (under 1%) but needed for construction; entry-bench set-down moment"),
C("COL-004","01_Product_Angles","caramel",False,None,"chest","three-quarter","full product","handheld","three-quarter","resting","none","living room","window light",
  "Three-quarter view of the bag sitting on the seat of a linen armchair, handles standing up, a throw blanket half over the armrest. Afternoon window light raking across the felt, showing the brushed fibres. Casual framing with the chair cut off at the left.",
  PUSH, "three-quarter product view (9% of shots), bag resting on a chair seat"),
C("COL-005","01_Product_Angles","caramel",False,None,"top-down","top-down","full product","static","top","resting","none","bedroom","window light",
  "Looking straight down at the bag lying on its back on a wrinkled cream duvet, the front face up, handles fallen to the sides, the belt with its curved ends and gold discs fully visible. A phone and a hair claw clip lie beside it. Flat overcast window light.",
  "Very slight handheld hover from directly above with a tiny drift and a soft refocus, nothing in the scene moves.", "top-down framing is 15% of organic bag shots"),
C("COL-006","01_Product_Angles","espresso",False,None,"floor","low angle","full product","handheld","front","resting","none","closet","warm indoor",
  "A low angle from near floor level looking slightly up at the bag standing on the carpeted floor of a walk-in closet at home, rows of shoes and hanging coats behind it. Warm ceiling light, a little dim, heavy grain.",
  PUSH, "low angle is under 1% of organic shots, a deliberate uncommon test; closet backdrop (3%)"),
C("COL-007","01_Product_Angles","caramel",False,None,"high angle","high angle","full product","handheld","three-quarter","resting","none","kitchen","window light",
  "A slight overhead angle looking down at the bag standing on a marble kitchen counter beside a coffee machine, a mug and a bowl of lemons. Morning window light, a bright hot spot on the counter, the frame tilted a couple of degrees.",
  HOLD, "high angle counter shot; kitchen is 4% of environments, morning routine moment"),
C("COL-008","01_Product_Angles","espresso",False,None,"chest","front","full product","handheld","front","resting","none","apartment other","window light",
  "The bag standing on a console table by the front door, a bowl of keys and a stack of mail beside it, a mirror on the wall above reflecting a blurred hallway. Daylight from a window to the side, natural shadows, slightly soft focus.",
  DRIFT, "entryway set-down, the 'grab it on the way out' moment"),

# ---------------- 02 DETAILS (10, Ken Burns from keyframe: hardware macros never survive i2v) ----------------
C("COL-009","02_Details","caramel",False,"A","chest","front","macro","static","top","resting","touching","bedroom","window light",
  "Extreme close-up of one rolled top handle, the smooth cognac leather wrap on the grip meeting the felt below, a woman's fingers with a thin gold ring resting on it. Shallow phone focus, window light from the side, the felt fibres and leather creases sharp.",
  "", "macro detail shots are 3% of organic shots but carry the texture story; fingers entering frame with rings is the convention", 6, "kenburns"),
C("COL-010","02_Details","caramel",False,None,"waist","front","macro","static","front","resting","none","living room","window light",
  "Extreme close-up of one belt end curving away from the felt face and its small round aged gold disc cap, the leather softly creased, fine felt fibres around it. Raking afternoon window light, phone macro softness, the rest of the bag falls out of focus.",
  "", "hardware macro in raking light", 6, "kenburns"),
C("COL-011","02_Details","espresso",False,None,"waist","three-quarter","macro","static","front","resting","none","bedroom","window light",
  "Close-up where the slim dark espresso leather belt passes through the felt loop of one vertical felt strap, the edge stitching on the strap visible. Soft window light, slightly off centre, natural phone sharpening.",
  "", "belt-through-strap construction detail", 6, "kenburns"),
C("COL-012","02_Details","caramel",False,None,"chest","front","macro","static","front","resting","none","bedroom","direct sunlight",
  "Macro of the brushed wool felt surface itself, a patch of the front face in a hard shaft of low sun through a window, every fibre and a little lint visible, the shadow of the belt across it. Nothing else in frame.",
  "", "texture macro; fibre-level surface shots appear in review videos that emphasise material", 6, "kenburns"),
C("COL-013","02_Details","caramel",False,None,"waist","side profile","close-up","static","right side","resting","none","living room","window light",
  "Close-up of the bag's bottom corner where the flat felt base meets the side gusset, sitting on a wooden side table, the corner slightly softened with wear. Window light, phone close focus, background blurred.",
  "", "corner and base construction detail", 6, "kenburns"),
C("COL-014","02_Details","espresso",True,"B","high angle","high angle","close-up","static","interior","open","touching","bedroom","window light",
  "Close-up looking down at the top centre of the open mouth where the small felt tab with its tiny gold snap stud sits on the inner rim, a woman's thumb resting beside it. The same oatmeal felt inside. Window light, phone macro softness.",
  "", "closure demonstration is a standard review beat (opening 8% of interactions)", 6, "kenburns"),
C("COL-015","02_Details","caramel",False,None,"chest","side profile","close-up","static","left side","resting","none","hallway","window light",
  "Close-up of the clean felt side gusset with its single vertical centre seam, the bag standing on an entry bench, one handle rising out of the top of the frame. Cool daylight from a door, slightly grainy.",
  "", "side seam detail", 6, "kenburns"),
C("COL-016","02_Details","caramel",False,None,"waist","front","close-up","static","front","resting","none","bedroom","warm indoor",
  "Close-up of the base of one top handle where the felt strap widens into the loop of the handle, the felt stitching and the start of the leather wrap above. Warm lamp light in a bedroom at night, heavy grain.",
  "", "handle base construction, low light night register", 6, "kenburns"),
C("COL-017","02_Details","espresso",False,None,"chest","front","close-up","static","front","resting","none","living room","window light",
  "Close-up of the two belt ends and their gold discs where they hang free below the belt line, both discs in frame, the felt face behind, slightly crooked framing. Grey window light.",
  "", "paired hardware detail", 6, "kenburns"),
C("COL-018","02_Details","caramel",False,"F","chest","front","close-up","static","top","held","holding handles","kitchen","window light",
  "Close-up of a woman's hand gripping both leather-wrapped handles together, the short handle drop visible, gold bracelet at her wrist, the top of the bag below. Kitchen window light, natural skin texture.",
  "", "hand on handles is 7% of interactions", 6, "kenburns"),

# ---------------- 03 HAND INTERACTION (12) ----------------
C("COL-019","03_Hand_Interaction","caramel",False,"A","chest","front","medium","handheld","three-quarter","being picked up","picking up","bedroom","window light",
  "A woman's hand has just closed around both handles of the bag as it sits on the edge of a bed, her arm entering from the right, the bag beginning to lift. Rumpled duvet, morning window light, slight motion blur on the hand."+FACE,
  "Her hand lifts the bag off the bed by both handles and carries it up out of the frame, the bag swaying slightly. Handheld camera follows a little.", "picking up is 3% of interactions and a common first-second hook"),
C("COL-020","03_Hand_Interaction","espresso",False,"B","waist","front","medium","handheld","front","being set down","putting down","kitchen","window light",
  "A woman's hand lowering the bag onto a kitchen counter by its handles, the base an inch above the marble, a coffee mug and keys nearby. Window light, slightly overexposed on the counter."+FACE,
  "She sets the bag down onto the counter, lets go of the handles and they fall open to either side, her hand withdraws. Small handheld shake.", "set-down moments are a core organic beat"),
C("COL-021","03_Hand_Interaction","caramel",False,"C","chest","three-quarter","medium","handheld","three-quarter","hanging","grabbing handle","living room","warm indoor",
  "The bag hangs from the back of a wooden dining chair by its handles and a woman's hand is reaching in to grab them, seen from chest height. A table with a laptop behind, warm evening lamps."+FACE,
  "Her hand grabs the handles and lifts the bag off the chair back, the bag swings gently as it comes free. Handheld sway.", "grabbing from a chair back, the leaving-the-table moment"),
C("COL-022","03_Hand_Interaction","caramel",False,"D","waist","front","close-up","natural hand movement","front","resting","touching material","living room","window light",
  "A woman's hand with a gold band stroking the felt face of the bag as it sits on her lap on a sofa, fingers slightly spread over the brushed wool, the belt and one disc visible below her hand. Soft window light, cardigan sleeve in frame.",
  "Her fingers slowly stroke across the felt surface, pressing lightly so the fibres catch the light, then rest. Tiny handheld shake.", "touching material is 4% of interactions and the tactile proof beat"),
C("COL-023","03_Hand_Interaction","espresso",False,"E","waist","front","close-up","natural hand movement","front","resting","touching hardware","bedroom","window light",
  "A young woman's fingers flicking one curved belt end so its gold disc cap catches the light, the bag standing on a bed, her claw-clipped ponytail blurred at the top edge. Bright window light.",
  "Her fingers lift the belt end slightly and let it fall back against the felt, the disc glinting. Handheld, small refocus.", "fingering hardware detail"),
C("COL-024","03_Hand_Interaction","caramel",True,"A","high angle","high angle","medium","handheld","open","being opened","opening","bedroom","window light",
  "Looking down from above at a woman's two hands pulling the mouth of the bag open wide on a bed, the handles fallen outward, the empty oatmeal felt interior visible with the small snap tab at the rim. Duvet, window light."+FACE,
  "Her hands pull the rims apart so the mouth opens into a wide oval, then she holds it open and tilts it slightly toward the camera. Handheld from above.", "opening the bag is 8% of interactions"),
C("COL-025","03_Hand_Interaction","caramel",False,"F","chest","front","close-up","natural hand movement","top","being closed","closing","living room","warm indoor",
  "Close-up of a woman's fingers pressing the two top rims of the bag together at the centre, the felt tab snapping shut, handles standing up either side. Warm lamp light, evening, some grain.",
  "Her fingers press the centre of the rims together, hold a beat, then let go and the top relaxes. Small handheld shake.", "closing is 2% of interactions; closure demo beat"),
C("COL-026","03_Hand_Interaction","espresso",False,"C","chest","front","medium","handheld","front","being carried","adjusting handles","hallway","window light",
  "A woman sliding the handles of the bag from her hand up onto her forearm, the bag rising to hip height, seen from chest to thigh, trench coat sleeve. Hallway by a front door, cool daylight."+FACE,
  "She slides the handles up her forearm and settles the bag against her hip with a small shrug, then tugs her coat sleeve. Handheld follow.", "adjusting the carry is a natural transition beat"),
C("COL-027","03_Hand_Interaction","caramel",False,"G","waist","front","close-up","natural hand movement","top","resting","brushing lint","living room","window light",
  "An older woman's hand brushing a bit of lint off the felt near the belt, the bag on an armchair beside her, an oatmeal cardigan sleeve. Soft window light, natural skin texture on her hand.",
  "Her hand brushes the felt twice with her fingertips and flicks the lint away, then smooths the surface. Handheld, slight wobble.", "care gesture, texture proof"),
C("COL-028","03_Hand_Interaction","caramel",True,"B","high angle","POV","medium","natural hand movement","open","receiving","dropping keys in","hallway","window light",
  "POV looking down into the open bag held on a woman's forearm by a front door, her other hand dropping a ring of keys in, a wallet and sunglasses already inside on the felt. Cool daylight."+FACE,
  "The keys drop into the bag and land on the wallet, her hand withdraws and the bag sways a little on her arm. Handheld POV.", "dropping essentials in, the leaving-the-house moment"),
C("COL-029","03_Hand_Interaction","espresso",False,"H","chest","front","medium","handheld","three-quarter","being lifted","lifting by one handle","bedroom","warm indoor",
  "A woman lifting the bag by just one handle so it tilts slightly, the other handle hanging, seen from chest height beside a bed at night, warm lamp light. Her curly red hair blurred at the top edge."+FACE,
  "She lifts the bag by one handle, it tilts and swings, then she catches the second handle with her other hand. Handheld.", "natural one-handle grab"),
C("COL-030","03_Hand_Interaction","caramel",False,"E","waist","front","medium","handheld","front","resting","sliding hand between handles","closet","warm indoor",
  "A young woman's hand sliding between the two handles of the bag as it sits on a closet shelf, about to pull it down, sweaters stacked beside it. Warm closet light."+FACE,
  "Her hand slides through the handles and pulls the bag off the shelf toward the camera, it drops slightly into her grip. Handheld.", "closet reach, getting ready"),

# ---------------- 04 CARRYING (10) ----------------
C("COL-031","04_Carrying","caramel",False,"A","chest","front","medium","walking camera","front","carried on forearm","walking toward camera","sidewalk","overcast daylight",
  "A woman walking toward the camera on a city sidewalk, framed from chin to knee, the bag on her forearm at hip height, long camel coat and jeans. Overcast day, blurred storefront behind, off-centre framing."+FACE,
  "She walks toward the camera at a relaxed pace, the bag swinging gently on her forearm, the camera walking backward with natural footstep bounce.", "walking shots are only 7% of organic bag videos, an outdoor opportunity shot"),
C("COL-032","04_Carrying","espresso",False,"F","chest","behind subject","full body","walking camera","back","carried in hand","walking away","sidewalk","golden hour",
  "From behind, a woman walking away down a tree-lined residential sidewalk carrying the bag by its handles in one hand so it swings near her knee, blazer and trousers, low golden light, long shadows.",
  "She keeps walking away from the camera, the bag swinging with her stride, handheld follow with footstep bounce.", "back-view walking, no face"),
C("COL-033","04_Carrying","caramel",False,"C","waist","side profile","medium","tracking","right side","carried on forearm","walking past","sidewalk","overcast daylight",
  "Side view of a woman walking past brownstone steps, the bag on her forearm, trench coat, framed from shoulder to knee. Grey daylight, wet pavement."+FACE,
  "She walks past the camera left to right, the bag moving with her arm, handheld pan following her with a slight lag.", "side-profile walk, rare orientation"),
C("COL-034","04_Carrying","caramel",False,"D","chest","front","medium","handheld","front","carried on forearm","standing","hallway","window light",
  "A woman standing naturally by her front door with the bag on her forearm, one hand in her coat pocket, framed from the shoulders down. Cool daylight from the door glass, a shoe rack beside her."+FACE,
  "She shifts her weight from one foot to the other and the bag moves slightly with her arm, tiny natural motions. Handheld sway.", "standing carry, chest-height front framing (the dominant framing)"),
C("COL-035","04_Carrying","espresso",False,"B","chest","front","medium","handheld","front","carried on forearm","holding coffee","sidewalk","overcast daylight",
  "A woman holding a paper coffee cup in one hand with the bag hanging from the same forearm, framed chest to hip, cream knit and dark jeans. Sidewalk, overcast, blurred cafe window behind."+FACE,
  "She lifts the coffee cup slightly and the bag sways on her forearm, then she starts to turn. Handheld shake.", "coffee-run carry"),
C("COL-036","04_Carrying","caramel",False,"E","waist","front","medium","handheld","front","carried in hand","coming down stairs","apartment other","window light",
  "A young woman coming down the wooden stairs inside her apartment carrying the bag in her hand, framed from waist to feet, white sneakers, daylight from a landing window."+FACE,
  "She comes down the last steps toward the camera, the bag swinging in her hand, handheld tilt following her feet.", "in-home movement, stairs"),
C("COL-037","04_Carrying","caramel",False,"F","chest","front","medium","handheld","front","carried on forearm","waiting at crosswalk","sidewalk","overcast daylight",
  "A woman waiting at a crosswalk with the bag on her forearm, framed shoulders down, blazer, a blurred taxi passing behind. Flat grey daylight, off-centre."+FACE,
  "She waits, glances down at her phone, the bag resting against her hip, a car passes behind. Handheld shake.", "street pause"),
C("COL-038","04_Carrying","espresso",False,"H","waist","front","medium","handheld","front","carried in hand","holding both handles low","living room","window light",
  "A woman holding the bag by both handles in one hand at knee height, standing in her living room in a leather jacket, framed from the waist down, a rug and a plant behind."+FACE,
  "She swings the bag gently by the handles once, then lifts it. Handheld.", "low hand carry"),
C("COL-039","04_Carrying","caramel",False,"G","chest","front","medium","handheld","front","carried on forearm","standing on porch","outdoors other","overcast daylight",
  "An older woman standing on a house porch with the bag on her forearm, framed from the shoulders down, oatmeal cardigan, a front door and a doormat behind her. Soft overcast light."+FACE,
  "She adjusts the bag on her arm and steps forward slightly. Handheld.", "doorstep moment, older creator"),
C("COL-040","04_Carrying","caramel",False,"A","chest","front","medium","handheld","three-quarter","carried in hand","walking through doorway","apartment other","window light",
  "A woman walking through an interior doorway toward the camera carrying the bag in her hand, framed from the chin down, camel coat half on. Daylight from the room beyond."+FACE,
  "She walks through the doorway and past the camera, the bag swinging. Handheld with a slight pan to follow.", "in-home walking"),

# ---------------- 05 MIRROR (8) ----------------
C("COL-041","05_Mirror","caramel",False,"A","chest","front","full body","mirror filming","front","carried on forearm","outfit check","bedroom","window light",
  "A woman filming herself full length in a bedroom mirror, phone covering her face, the bag on her forearm at hip height, long camel coat, grey knit and jeans. Unmade bed and clothes on a chair reflected. Morning window light, slightly underexposed.",
  "She shifts her weight, tilts the bag slightly toward the mirror and lowers the phone a little, small natural sways. Mirror filming.", "mirror footage in 8% of videos; the phone-over-face full body is the canonical outfit check"),
C("COL-042","05_Mirror","espresso",False,"B","chest","front","medium","mirror filming","front","carried on forearm","waist-up check","bedroom","window light",
  "A waist-up mirror selfie in a bedroom, phone over the face, the bag held up on the forearm at chest height so its front fills the lower half of the frame, cream turtleneck. Window light, a plant reflected.",
  "She raises the bag a little toward the mirror and turns it slightly, the phone steady. Mirror filming with small shake.", "waist-up mirror composition"),
C("COL-043","05_Mirror","caramel",False,"F","chest","front","full body","mirror filming","front","carried on forearm","walking toward mirror","hallway","warm indoor",
  "A woman walking toward a full-length hallway mirror, phone raised over her face, the bag on her forearm swinging, blazer and loafers. Warm hallway light, slightly blurred with motion.",
  "She walks toward the mirror and stops, the bag settling on her arm, then leans on one hip. Mirror filming with walking bounce.", "walking into the mirror shot"),
C("COL-044","05_Mirror","caramel",False,"E","chest","front","full body","mirror filming","front","carried in hand","closet mirror","closet","warm indoor",
  "A young woman in a walk-in closet filming in a mirrored door, phone over her face, the bag held by its handles at her side, athleisure set, rows of clothes reflected. Warm light.",
  "She lifts the bag onto her forearm and turns slightly side to side checking the look. Mirror filming.", "closet mirror, GRWM register"),
C("COL-045","05_Mirror","espresso",False,"C","chest","front","full body","mirror filming","three-quarter","carried on forearm","turning","hallway","window light",
  "A woman mid-turn in front of a leaning floor mirror in a hallway, phone over her face, the bag on her forearm, trench coat flaring. Cool daylight, framing crooked.",
  "She turns a quarter turn away then back toward the mirror, the bag swinging with the turn. Mirror filming.", "the mirror turn"),
C("COL-046","05_Mirror","caramel",False,"D","chest","front","medium","mirror filming","front","carried on forearm","bathroom check","bathroom","bathroom lighting",
  "A waist-up bathroom mirror selfie, phone over the face, the bag on the forearm, black turtleneck, a marble sink and a bottle of hand soap in the reflection. Flat bathroom vanity light.",
  "She adjusts the bag on her arm and tucks her hair back with the free hand. Mirror filming.", "bathroom mirror (bathroom lighting cue)"),
C("COL-047","05_Mirror","caramel",False,"H","chest","front","full body","mirror filming","front","carried on forearm","putting on coat","bedroom","window light",
  "A woman in a bedroom mirror pulling a leather jacket over one shoulder with the bag already on her other forearm, phone over her face. Window light, bed reflected.",
  "She shrugs the jacket on and settles the bag on her forearm, then picks the phone angle back up. Mirror filming.", "GRWM final step"),
C("COL-048","05_Mirror","espresso",False,"G","chest","front","full body","mirror filming","front","held beside body","held beside body","bedroom","window light",
  "An older woman in a bedroom mirror, phone over her face, holding the bag by its handles beside her body so its full front faces the mirror, oatmeal cardigan and dark trousers. Soft window light.",
  "She lifts the bag slightly higher beside her and holds it, a small sway. Mirror filming.", "bag held beside body to show scale"),

# ---------------- 06 OUTFITS (7) ----------------
C("COL-049","06_Outfits","caramel",False,"A","chest","front","medium","handheld","front","carried on forearm","standing","sidewalk","overcast daylight",
  "Chest-to-knee crop of a woman in a long camel wool coat and straight jeans with the bag on her forearm, standing on a sidewalk. Overcast light."+FACE,
  "She shifts her stance and the bag moves slightly with her arm. Handheld sway.", "outfit integration: camel coat; chest-height front framing"),
C("COL-050","06_Outfits","caramel",False,"C","chest","front","medium","handheld","front","carried on forearm","standing","hallway","window light",
  "Chest-to-knee crop of a woman in a belted khaki trench and ankle boots with the bag on her forearm, by a front door. Cool daylight."+FACE,
  "She cinches the trench belt with her free hand, the bag resting on the other arm. Handheld.", "outfit integration: trench"),
C("COL-051","06_Outfits","espresso",False,"B","chest","front","medium","handheld","front","carried in hand","standing","living room","window light",
  "Chest-to-knee crop of a woman in an oversized cream cable knit and wide-leg jeans holding the bag by its handles at her side, living room window light."+FACE,
  "She lifts the bag from her side onto her forearm. Handheld.", "outfit integration: chunky knit"),
C("COL-052","06_Outfits","caramel",False,"F","chest","front","medium","handheld","front","carried on forearm","standing","office","cool indoor",
  "Chest-to-knee crop of a woman in a black blazer and tailored trousers with the bag on her forearm, standing in an office corridor. Cool fluorescent light, slightly green cast."+FACE,
  "She turns slightly and the bag moves with her arm. Handheld.", "outfit integration: workwear; office 4% of environments"),
C("COL-053","06_Outfits","caramel",False,"E","chest","front","medium","handheld","front","carried in hand","standing","kitchen","window light",
  "Chest-to-knee crop of a young woman in a grey athleisure set and white sneakers holding the bag by the handles, kitchen counter behind. Morning window light."+FACE,
  "She swings the bag lightly by the handles and sets a hand on her hip. Handheld.", "outfit integration: athleisure"),
C("COL-054","06_Outfits","espresso",False,"D","chest","front","medium","handheld","front","carried on forearm","standing","living room","warm indoor",
  "Chest-to-knee crop of a woman in a black midi dress and knee boots with the bag on her forearm, living room in the evening, lamps on. Grainy."+FACE,
  "She smooths the dress with her free hand and the bag sways. Handheld.", "outfit integration: dress and boots"),
C("COL-055","06_Outfits","caramel",False,"H","chest","front","medium","handheld","front","carried on forearm","standing","sidewalk","overcast daylight",
  "Chest-to-knee crop of a woman in a black leather jacket, white tee and jeans with the bag on her forearm, on a sidewalk by a brick wall. Overcast."+FACE,
  "She hooks a thumb into her pocket and the bag settles against her hip. Handheld.", "outfit integration: leather jacket"),

# ---------------- 07 POV (8) ----------------
C("COL-056","07_POV","caramel",True,"A","high angle","POV","medium","natural hand movement","open","open","looking inside","bedroom","window light",
  "First-person view looking down into the open bag held by both handles in front of the body, a folded grey knit, a wallet and a notebook inside on the oatmeal felt, jeans visible below. Window light.",
  "The bag tilts slightly as she looks in, one hand releases a handle and the mouth opens wider, handheld POV.", "POV is 11% of organic angles; looking into the bag is the most common POV"),
C("COL-057","07_POV","caramel",True,"B","high angle","POV","close-up","natural hand movement","open","open","reaching in for keys","hallway","window light",
  "POV of a woman's hand reaching into the open bag for a ring of keys, the bag on the other forearm, felt interior visible, sunglasses and a wallet inside. Cool daylight by a door.",
  "Her hand digs briefly among the items and pulls out the keys, the bag shifting on her arm. Handheld POV.", "POV reach-in"),
C("COL-058","07_POV","espresso",False,"C","waist","POV","medium","walking camera","top","carried on forearm","walking","sidewalk","overcast daylight",
  "POV looking down while walking, the bag on the forearm at the left of the frame, trench coat hem and boots on wet pavement below. Overcast, motion blur on the feet.",
  "She keeps walking, the bag bouncing gently on her arm, the pavement scrolling under her boots. Handheld POV with footstep bounce.", "POV walking with the bag in frame"),
C("COL-059","07_POV","caramel",True,"F","high angle","POV","medium","natural hand movement","open","open","packing laptop","office","cool indoor",
  "POV of a woman sliding a matte dark grey laptop, held edge on with no lid face visible, into the open bag standing on a desk, a notebook already inside. Cool office light.",
  "The laptop slides down into the bag and her hand pats it flat, then she pulls the handles up. Handheld POV.", "packing items is 9% of interactions; laptop-fit proof"),
C("COL-060","07_POV","caramel",True,"E","high angle","POV","medium","natural hand movement","open","open","unpacking onto desk","apartment other","window light",
  "POV of a young woman pulling a water bottle out of the open bag onto a desk where a notebook and AirPods case already sit, the bag standing at the top of the frame. Window light.",
  "She lifts the bottle out and sets it down, then reaches back in. Handheld POV.", "removing items (5%)"),
C("COL-061","07_POV","espresso",False,"D","waist","POV","medium","natural hand movement","three-quarter","being placed","placing on passenger seat","car","direct sunlight",
  "POV from the driver's side of a woman's hand setting the bag onto the passenger seat, sunlight through the windshield, a dashboard edge in frame. Slightly blown highlights.",
  "Her hand sets the bag down on the seat, straightens it, and pulls away. Handheld POV.", "car appears in 3.5% of videos; POV seat placement"),
C("COL-062","07_POV","caramel",False,"G","chest","POV","medium","natural hand movement","front","held up","holding handles up","living room","window light",
  "POV of an older woman's hands holding the bag up by both handles in front of her at chest height so the whole front faces the camera, living room window behind.",
  "She raises the bag slightly and turns it a few degrees each way, then lowers it. Handheld POV.", "showing to camera is the top interaction (23%)"),
C("COL-063","07_POV","caramel",True,"H","high angle","POV","close-up","natural hand movement","open","open","pulling out wallet","cafe","window light",
  "POV of a woman's hand pulling a tan leather wallet out of the open bag sitting on a cafe chair beside her table, a coffee cup at the frame edge. Window light.",
  "She pulls the wallet out and the bag settles, her hand comes toward the camera. Handheld POV.", "paying-at-the-cafe reach"),

# ---------------- 08 HOME (10) ----------------
C("COL-064","08_Home","caramel",True,"A","high angle","high angle","medium","handheld","open","open","packing","bedroom","window light",
  "High angle of the bag standing open on a bed while a woman's hand lowers a folded cream knit sweater into it, a water bottle waiting beside. Grey window light, wrinkled duvet."+FACE,
  "The sweater goes into the bag and her hand presses it down, then reaches for the bottle. Handheld from above.", "bed packing, the most common environment and interaction pair"),
C("COL-065","08_Home","espresso",False,"B","waist","front","medium","handheld","front","resting","sitting beside","living room","window light",
  "The bag sitting on a sofa cushion beside a woman's lap, her hand resting on the sofa, a mug on the arm. Window light, framed from her waist down."+FACE,
  "She picks up the mug and settles back, the bag stays put beside her. Handheld.", "bag on the couch beside her"),
C("COL-066","08_Home","caramel",False,None,"chest","front","full product","handheld","front","resting","none","kitchen","window light",
  "The bag standing on a kitchen counter next to a coffee maker mid-pour, a mug filling, a phone and a banana beside it. Morning window light, hot spot on the counter.",
  HOLD, "kitchen morning still life (kitchen 4%)"),
C("COL-067","08_Home","caramel",False,"C","chest","front","medium","handheld","three-quarter","being taken down","reaching to shelf","closet","warm indoor",
  "A woman reaching up to take the bag down from a closet shelf between stacked sweaters, framed from the shoulders down. Warm light."+FACE,
  "She pulls the bag down from the shelf and turns with it. Handheld.", "closet shelf reach"),
C("COL-068","08_Home","espresso",False,None,"waist","three-quarter","full product","handheld","three-quarter","resting","none","bedroom","warm indoor",
  "The bag on top of a dresser at night beside a lamp, a perfume bottle and a hair claw, warm light, heavy grain, slightly soft.",
  PUSH, "dresser top, low-light register"),
C("COL-069","08_Home","caramel",False,None,"waist","front","full product","handheld","front","resting","none","hallway","window light",
  "The bag on a wooden entry bench under a row of coat hooks, a pair of loafers on the floor beneath, keys beside it. Daylight from the door."+"",
  DRIFT, "entry bench set-down"),
C("COL-070","08_Home","caramel",True,"F","high angle","high angle","medium","handheld","open","open","on desk","apartment other","window light",
  "The bag standing open on a home desk beside a closed matte grey laptop, a woman's hand dropping a phone charger in, a plant and a mug behind. Window light."+FACE,
  "The charger drops in, she pulls a notebook from the desk and slides it into the bag too. Handheld.", "home desk pack-up"),
C("COL-071","08_Home","espresso",False,None,"waist","front","full product","static","front","resting","none","bedroom","window light",
  "The bag on a windowsill radiator cover in a bedroom, sheer curtain moving beside it, bright backlight from the window with the felt slightly silhouetted at the edges, exposure blown at the glass.",
  "Very slight handheld hover, the curtain sways gently in a draft, nothing on the bag moves.", "windowsill set-down with blown window (a listed realism cue)"),
C("COL-072","08_Home","caramel",False,"D","waist","front","medium","handheld","front","hanging","hanging on chair","kitchen","window light",
  "The bag hanging by its handles from the back of a kitchen chair, a woman sitting at the table beyond with a laptop, framed at waist height from the side."+FACE,
  "She reaches back without looking and touches the bag handles, then goes back to typing. Handheld.", "chair-back hanging"),
C("COL-073","08_Home","caramel",False,"E","waist","front","medium","handheld","three-quarter","resting","sitting on bed edge","bedroom","window light",
  "A young woman sitting on the edge of her bed pulling on a sneaker, the bag standing beside her on the bed, framed from the waist down. Morning window light."+FACE,
  "She finishes tying the shoe and grabs the bag handles. Handheld.", "morning leave-the-house sequence"),

# ---------------- 09 CAR (6) ----------------
C("COL-074","09_Car","caramel",False,None,"waist","three-quarter","full product","handheld","three-quarter","resting","none","car","direct sunlight",
  "The bag standing upright on a car passenger seat, seat belt across the seat back, an iced coffee in the cup holder, hard afternoon sun through the side window with blown highlights on the felt.",
  HOLD, "car seat portrait; car is 3.5% of videos, rare enough to stand out"),
C("COL-075","09_Car","espresso",False,"B","waist","front","medium","handheld","front","being grabbed","grabbing from seat","car","overcast daylight",
  "From the driver's seat, a woman's hand reaching across to grab the handles of the bag on the passenger seat, dashboard and door in frame. Overcast light through the glass.",
  "Her hand grabs the handles and pulls the bag toward her across the seat. Handheld.", "grabbing from passenger seat"),
C("COL-076","09_Car","caramel",False,"F","chest","high angle","medium","handheld","top","resting","on lap","car","overcast daylight",
  "Looking down at the bag on a woman's lap in the passenger seat, her hands resting on the handles, seat belt across, trousers below. Grey daylight."+FACE,
  "The car moves and the bag rocks slightly with it, her fingers tap the handle. Handheld.", "bag on lap in a moving car"),
C("COL-077","09_Car","caramel",False,"A","waist","front","medium","handheld","three-quarter","being placed","placing in car","car","overcast daylight",
  "From outside the open passenger door, a woman leaning in to set the bag on the seat, camel coat, framed from the shoulders down. Overcast, the street reflected in the door glass."+FACE,
  "She sets the bag on the seat and straightens up, closing the door partly. Handheld.", "placing the bag in the car"),
C("COL-078","09_Car","espresso",False,"C","waist","front","medium","handheld","front","being carried","getting out","car","overcast daylight",
  "A woman stepping out of a parked car, one boot on the pavement, the bag coming out on her forearm, trench coat, framed from waist to ground. Overcast."+FACE,
  "She stands up out of the car with the bag on her arm and swings the door shut. Handheld.", "getting out with the bag"),
C("COL-079","09_Car","caramel",False,None,"waist","front","full product","handheld","front","resting","none","car","golden hour",
  "The bag on the back seat of a car beside a folded coat, low golden sun through the rear window striping the felt, dust in the seat seams.",
  DRIFT, "back-seat golden hour"),

# ---------------- 10 WORK / CAFE (8) ----------------
C("COL-080","10_Work_Cafe","caramel",False,None,"waist","front","full product","handheld","three-quarter","resting","none","cafe","window light",
  "The bag sitting on a cane bistro chair beside a small marble cafe table with a flat white and a croissant, window light with real shadows, other tables blurred.",
  HOLD, "cafe still life; cafe is 2% of environments (never on the floor)"),
C("COL-081","10_Work_Cafe","espresso",False,"D","waist","front","medium","handheld","front","resting","on banquette","cafe","warm indoor",
  "The bag on a leather banquette beside a woman's hip, her hand around a coffee cup on the table, framed at waist height. Warm cafe light."+FACE,
  "She lifts the cup, sips, and sets it down, the bag stays beside her. Handheld.", "banquette seat"),
C("COL-082","10_Work_Cafe","caramel",False,"F","chest","front","medium","handheld","three-quarter","being set down","arriving at desk","office","cool indoor",
  "A woman setting the bag down on an office desk beside a monitor, blazer sleeve, framed from the shoulders down. Cool office light."+FACE,
  "She sets the bag down, pulls the chair out and sits, one hand still on the handles. Handheld.", "arriving at the desk"),
C("COL-083","10_Work_Cafe","caramel",True,"A","high angle","high angle","medium","handheld","open","open","laptop out","cafe","window light",
  "High angle of a woman pulling a matte dark grey laptop, edge on, out of the open bag on a cafe chair beside her table, coffee cup in frame."+FACE,
  "The laptop comes out of the bag and onto the table, she flips the bag handles closed. Handheld from above.", "laptop-out at the cafe"),
C("COL-084","10_Work_Cafe","espresso",False,None,"waist","front","full product","handheld","front","resting","none","office","cool indoor",
  "The bag on an office chair seat pulled up to a desk, a lanyard and a notebook on the desk, fluorescent light with a slight green cast.",
  DRIFT, "office chair set-down"),
C("COL-085","10_Work_Cafe","caramel",False,"B","chest","front","medium","handheld","three-quarter","being picked up","leaving cafe","cafe","window light",
  "A woman picking the bag up off a cafe chair by its handles as she stands to leave, an empty cup on the table, framed from the shoulders down. Window light."+FACE,
  "She lifts the bag onto her forearm and pushes the chair in. Handheld.", "leaving the cafe"),
C("COL-086","10_Work_Cafe","caramel",False,"G","chest","high angle","medium","handheld","top","resting","on lap in waiting area","lobby","cool indoor",
  "Looking down at the bag on an older woman's lap in a lobby waiting chair, her hands folded on the handles, a magazine beside her. Cool lobby light."+FACE,
  "She unfolds her hands and rests one on the felt, glances up. Handheld.", "waiting-room lap"),
C("COL-087","10_Work_Cafe","espresso",False,"H","waist","front","medium","handheld","front","resting","beside laptop","cafe","window light",
  "The bag on the bench seat beside a woman working on a laptop at a long shared cafe table, her hands on the keys, framed at waist height from the side."+FACE,
  "She types, pauses, and touches the bag handle absentmindedly. Handheld.", "co-working bench"),

# ---------------- 11 WHAT'S IN MY BAG (6, interior is felt-only, no invented pockets) ----------------
C("COL-088","11_Whats_In_My_Bag","caramel",False,None,"top-down","top-down","full product","static","front","resting","none","bedroom","window light",
  "Top-down flat lay on a wrinkled cream duvet: the bag lying on its back at the top of the frame and, below it in a loose grid, a tan wallet, a phone, an AirPods case, keys, lip balm, a small notebook, sunglasses and a hand cream tube. Flat window light.",
  "Slight hover from above with a tiny drift, nothing moves.", "what's in my bag is 19% of formats; the flat-lay grid is its canonical composition"),
C("COL-089","11_Whats_In_My_Bag","caramel",True,None,"overhead","top-down","medium","static","interior","open","none","bedroom","window light",
  "Camera looking straight down into the open standing bag on a bed, contents nested inside on the oatmeal felt: a folded knit, a notebook, a wallet, a pouch and keys. Handles fallen outward. Window light.",
  "Slight overhead hover with a soft refocus, the contents settle very slightly.", "open-mouth overhead; 57% of videos show the interior"),
C("COL-090","11_Whats_In_My_Bag","espresso",True,"B","high angle","high angle","medium","handheld","open","open","pulling items out","bedroom","window light",
  "High angle of a woman's hand lifting a tan wallet out of the open bag on a bed, a phone and lip balm already laid out on the duvet beside it."+FACE,
  "She sets the wallet down beside the other items and reaches back in for the next thing. Handheld from above.", "one-by-one reveal (removing items 5%)"),
C("COL-091","11_Whats_In_My_Bag","caramel",False,None,"high angle","high angle","full product","handheld","three-quarter","resting","none","apartment other","window light",
  "The bag standing on a desk with its contents lined up in a row in front of it: notebook, AirPods, wallet, water bottle, keys, glasses case. Window light, slightly crooked.",
  DRIFT, "contents lined up beside the bag"),
C("COL-092","11_Whats_In_My_Bag","caramel",True,"D","high angle","high angle","medium","handheld","open","open","unpacking onto table","kitchen","window light",
  "High angle of a woman unpacking the bag onto a kitchen table: her hand placing a book down next to keys and a phone, the open bag at the edge of the frame."+FACE,
  "She sets the book down and pulls out a small pouch, placing it in the row. Handheld from above.", "kitchen table unpack"),
C("COL-093","11_Whats_In_My_Bag","caramel",True,"E","high angle","POV","close-up","natural hand movement","open","open","pulling out AirPods","living room","window light",
  "POV close-up of a young woman's hand pulling a white AirPods case out of the open bag on the sofa beside her, the felt interior and a wallet visible.",
  "She pulls the case out and pops it open with her thumb. Handheld POV.", "essentials pull"),

# ---------------- 12 MOVEMENT (4) ----------------
C("COL-094","12_Movement","caramel",False,"A","chest","front","medium","handheld","three-quarter","swinging","turning","living room","window light",
  "A woman mid-turn in her living room with the bag on her forearm swinging outward, camel coat flaring, framed from the shoulders down. Window light, motion blur on the coat."+FACE,
  "She completes the turn and the bag swings around with her arm and settles against her hip. Handheld.", "turning is a listed interaction; the bag's natural swing"),
C("COL-095","12_Movement","espresso",False,"F","waist","front","medium","handheld","front","swinging","setting down","hallway","window light",
  "A woman lowering the bag onto an entry bench, the handles still swinging from the motion, framed at waist height."+FACE,
  "The bag lands, the handles swing once and fall open, her hand withdraws. Handheld.", "handles-swing on set-down"),
C("COL-096","12_Movement","caramel",False,"C","waist","behind subject","medium","walking camera","back","carried on forearm","walking through hallway","hallway","window light",
  "From behind, a woman walking down her apartment hallway toward the front door, the bag on her forearm swaying, trench coat, framed from the waist down.",
  "She walks to the door and reaches for the handle, the bag swaying with each step. Handheld follow.", "in-home walk-away"),
C("COL-097","12_Movement","caramel",False,"E","chest","front","medium","handheld","three-quarter","swinging","checking in closet","closet","warm indoor",
  "A young woman in her closet lifting the bag from her hand up onto her forearm and turning toward the mirror door, framed from the chin down. Warm light."+FACE,
  "She lifts the bag onto her arm, turns a quarter turn and stops, the bag swinging then settling. Handheld.", "the lift-and-turn"),

# ---------------- 13 TRANSITIONS (3) ----------------
C("COL-098","13_Transitions","caramel",False,"B","waist","front","medium","static","front","resting","hand entering frame","bedroom","window light",
  "The bag standing on a bed, framed at waist height, a woman's hand just entering the frame from the right about to grab the handles. Window light, still camera."+FACE,
  "Her hand enters, grabs both handles and pulls the bag out of the frame to the right, leaving the empty duvet. Static handheld.", "hand-enters-frame grab, a first-second hook convention"),
C("COL-099","13_Transitions","espresso",False,"H","waist","front","medium","static","front","being set down","setting into frame","kitchen","window light",
  "An empty kitchen counter framed at waist height with a mug at the edge, a woman's hands lowering the bag into the frame from above, base just above the counter."+FACE,
  "The bag is set down into the frame and the hands let go and leave, the bag settles. Static handheld.", "set-down into frame"),
C("COL-100","13_Transitions","caramel",False,"A","chest","front","medium","handheld","three-quarter","carried on forearm","walking out of frame","hallway","window light",
  "A woman with the bag on her forearm passing very close to the camera in a hallway, the bag filling the right half of the frame with motion blur, camel coat. Daylight."+FACE,
  "She walks past and out of the frame to the right, the bag passing close to the lens with motion blur, then the empty hallway. Handheld.", "bag passes camera / walk out"),
]
assert len(CLIPS) == 100, len(CLIPS)
assert len({c["id"] for c in CLIPS}) == 100

TRIM = {"caramel": "warm cognac tan", "espresso": "dark espresso brown"}

def product_truth(cw, open_bag):
    t = TRIM[cw]
    s = (f"PRODUCT TRUTH, follow exactly. The bag is an oatmeal greige brushed wool felt east west tote, about twice as wide as it is tall, "
         f"softly structured and standing on its own, with a flat base. It measures about 50 centimetres wide, 26 centimetres tall and 18 centimetres deep, a wide low landscape shape, never boxy or square. The felt is smooth brushed felt with fine visible fibres, NOT knitted, no knit ribs, no yarn loops. "
         f"Two wide vertical felt straps run down the front face from the top rim to the base. A slim {t} leather belt about half an inch wide crosses the front "
         f"horizontally, passing through a felt loop on each vertical strap, and each of its two ends extends past the straps and curves outward and downward, "
         f"hanging free, finished with a small round aged gold metal disc cap. The back face is identical. Two rolled top handles, one on the front and one on the back, "
         f"wrapped in {t} leather on the grip with felt below, with a short handle drop so the bag hangs from the hand or forearm, never the shoulder. "
         f"The top is open with no flap and no zipper. The side gussets are clean felt with a single vertical centre seam and nothing attached to them. "
         f"The only metal on the bag is aged gold. There are no logos, no embossing, no lettering and no tags anywhere on the bag.")
    if open_bag:
        s += (" The bag stands open and the mouth is a wide oval. Inside, the same oatmeal felt continues with no lining pattern and no pockets; "
              "there is one small felt tab with a tiny gold snap stud at the top centre of the front inner rim and one on the back inner rim. "
              "Contents sit directly on the felt.")
    return s

PRE = ("Use the attached product photos ONLY as the reference for the bag's shape, proportions, materials, colours, stitching and hardware. "
       "Do NOT copy their lighting, plain background, clean edges or catalogue look; those are studio images and the picture you produce must not resemble one. "
       "Create the following real photograph instead.")

FOOTER = ("CRITICAL RENDERING INSTRUCTION. This is a single frame from a real video casually shot on an iPhone 15 Pro by an ordinary person, handheld, "
          "with no lighting equipment, no tripod and no styling. It is NOT a 3D render, NOT CGI, NOT a product visualisation, NOT a catalogue or commercial photograph, "
          "NOT retouched, NOT studio lit. Photographic evidence that must be present: visible sensor noise through the shadows, highlights slightly blown where the "
          "light source hits, mild chromatic aberration on contrast edges, phone sharpening, focus slightly imperfect, a trace of handheld motion blur, and framing that "
          "is a little crooked and off centre the way a real snapshot is. One dominant available light source with mixed colour temperature and uneven exposure. "
          "The wool felt shows individual brushed fibres and small lint, the leather trim is softly creased where it has been handled, ordinary dust and fingerprints exist. "
          "The setting is a real lived in place with ordinary clutter, not a set. Any human skin shows real texture and pores, never retouched, and no face is visible. "
          "Any laptop or phone in the scene is plain matte dark grey with no logo. No on screen text, no captions, no lettering, no signage, no graphics, no watermarks and "
          "no other branded products anywhere. Vertical 9:16 portrait framing.")

def build_prompt(c):
    scene = c["scene"]
    if c.get("creator") and c["creator"] in CREATORS:
        scene = scene + " The woman in the scene is " + CREATORS[c["creator"]] + "."
    return "\n\n".join([PRE, scene, product_truth(c["colorway"], c["open_bag"]), FOOTER])

def refs_for(c):
    k = c["colorway"]
    return [f"{k}_hero", f"{k}_interior"] if c["open_bag"] else [f"{k}_hero", f"{k}_side"]

if __name__ == "__main__":
    import sys, collections
    print(collections.Counter(c["category"] for c in CLIPS))
    print(collections.Counter(c["colorway"] for c in CLIPS), collections.Counter(c["engine"] for c in CLIPS))
    if len(sys.argv) > 1:
        c = next(x for x in CLIPS if x["id"] == sys.argv[1]); print(build_prompt(c)); print("---MOTION---", c["motion"])
