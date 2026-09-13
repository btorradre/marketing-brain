#!/usr/bin/env python3
"""Velantra claymation brand films — campaign orchestrator (kie.ai).

GPT Image 2 i2i keyframes (2:3 @2K, center-cropped to 9:16) -> Seedance 2.0
chain-mode segments (first_frame_url, native ambient audio) -> stitch + endcard.
Prompts = brief scene text composed with the locked style-bible blocks.

Usage:
  python3 orchestrate.py assets                # heroine sheet + endcard image
  python3 orchestrate.py keyframes [FILM ...]  # default: all films
  python3 orchestrate.py videos   [FILM ...]   # segments (needs keyframes)
  python3 orchestrate.py endcard-video
  python3 orchestrate.py stitch   [FILM ...]   # concat segs + endcard
  python3 orchestrate.py status | credit
Films: FERRY HARBOR WOVEN WINDOW SPILL MADAM
State: state.json (upload cache, task ids, credits). Finished files are skipped;
delete a file to regenerate it.
"""
import json, os, ssl, subprocess, sys, time, urllib.request

try:
    import certifi
    SSL_CTX = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    SSL_CTX = ssl.create_default_context()

HERE = os.path.dirname(os.path.abspath(__file__))
CAMP = os.path.dirname(HERE)
VAULT = "/Users/brooksorradre2/Documents/marketing brain"
API = "https://api.kie.ai/api/v1"
UPLOAD_API = "https://kieai.redpandaai.co/api/file-stream-upload"
IMG_MODEL = "gpt-image-2-image-to-image"
VID_MODEL = "bytedance/seedance-2"   # std only; -fast BANNED
VPS_RELAY = "root@187.124.249.12"
WAVE = 6
STATE_F = os.path.join(HERE, "state.json")

# ---------- refs ----------
CARAMEL = os.path.join(VAULT, "brands/velantra/products/straw-birkin/product-images/straw birkin/caramel 1.png")
CHOC1 = os.path.join(VAULT, "brands/velantra/products/weekender/product-images/product images/light chocolate 1.webp")
CHOC4 = os.path.join(VAULT, "brands/velantra/products/weekender/product-images/product images/light chocolate 4.webp")
OPEN_STILL = os.path.join(HERE, "assets/weekender-open-truth-still.png")
HEROINE_PNG = os.path.join(HERE, "assets/heroine.png")
ENDCARD_PNG = os.path.join(HERE, "assets/endcard.png")
ENDCARD_MP4 = os.path.join(HERE, "assets/endcard.mp4")

# ---------- locked blocks (style bible; never paraphrase) ----------
STYLE = ("Handcrafted stop motion claymation world. Every character and prop is a "
"physical plasticine clay puppet with soft visible fingerprint texture, hand "
"sculpted imperfections, felt and fabric miniature clothing and props, wire "
"armature poses. Miniature diorama set with real physical depth, shallow depth "
"of field, warm coastal palette of sandy cream, seafoam green, butter yellow "
"and terracotta, soft practical light like a handmade film.")

NOT_CLAY = ("The bag is the ONLY non clay object in the entire frame: a photorealistic "
"miniature replica of the bag in the first reference image, exact same "
"silhouette, proportions, materials, colors and details, never clay, never "
"simplified, never restyled, no logos anywhere on the bag.")

TOTE_ID = ("The bag is a structured hand woven straw tote in warm sandy caramel, "
"tightly woven straw body with braided cross stitch trim along the edges, a "
"smooth taupe leather flap folded over the top of the bag from the back: the "
"flap is ONE single seamless piece of leather, its front lower edge cut into "
"the silhouette of a wide center panel with 2 squared outer tabs, the leather "
"fully continuous and unbroken between and above these shapes, with exactly 2 "
"narrow slots through which the handles pass, two rolled taupe leather top "
"handles, two taupe leather belt straps crossed on the front, "
"white contrast stitching on all leather edges, no metal hardware, no logos. "
"The leather flap, tabs and belt straps exist ONLY on the FRONT face of the "
"bag, the back face is plain woven straw, no duplicated front detailing on "
"any other face.")

TOTE_MECH = ("Flap and opening construction: the taupe leather flap is ONE single "
"seamless sheet of leather attached along the top rear edge of the tote and "
"folded all the way forward over the front, lying completely flat. Its front "
"lower edge is cut into the shape of a wide center panel and 2 squared outer "
"tabs, but these are shapes cut into the SAME single sheet, never separate "
"pieces. The leather is continuous and unbroken between the shapes and "
"across the entire top of the bag, including between the two handle slots. "
"The only openings anywhere in the flap are the 2 narrow handle slots. No "
"gap, no seam, no split, no opening exists anywhere else in the flap, and "
"nothing behind or inside the bag is ever visible through the flap. The flap "
"never splits into pieces, never lifts, never stands up, always folded all "
"the way over. When the tote is carrying things, the woven mouth opens "
"BEHIND the flap: the croissant, baguette or flowers lean out of the open "
"mouth at the back of the bag, behind the leather flap, never through the "
"flap. The 2 taupe leather belt straps lie crossed in an X over the front "
"below the flap with rounded ends and white contrast stitching, exactly as "
"on the closed reference bag, never threaded through the flap and never "
"wrapped around the contents. No metal hardware anywhere on the bag.")

WEEK_ID = ("The bag is a structured two tone weekend bag, wider than tall, rich cognac "
"brown leather upper flap section and two rolled cognac leather top handles "
"over a cream ivory woven canvas body, a small gold oval turn lock on the "
"front, two flat gold clasp plates with cognac leather belt straps threaded "
"through them, a small cognac leather key bell tied to the handle base, "
"cognac leather corner patches at the bottom, visible stitching, gold "
"hardware, no logos anywhere on the bag, natural cream cotton canvas interior "
"lining with a cognac leather slip pocket on the back wall. The bag has no "
"zipper anywhere.")

MECHANISM = ("Open bag construction: the open bag keeps the exact same two tone split as "
"the closed bag. The entire upper section of the bag body, across the front, "
"the back and both sides, is smooth rich cognac brown leather, exactly as "
"deep as the cognac leather upper section shown in the first reference image, "
"and everything below it is cream ivory woven canvas. Folding the flap back "
"does NOT change this split: the line where the leather ends and the canvas "
"begins sits in exactly the same place as on the closed bag. The two rolled "
"cognac leather top handles are anchored directly into this wide leather "
"upper band with sturdy leather bases, never into the canvas. Two thin gold "
"posts stand upright on the leather band, and the small gold oval turn lock "
"is mounted on the leather band at the top center of the front. The two "
"cognac leather belt straps hang loose and unfastened down the front with "
"their gold clasp plates. The wide leather band on the front is plain smooth "
"leather and is part of the bag body: no tab sections, no scalloped edges, no "
"pocket shape, no turn lock pocket, it is not a flap. The entire cognac "
"leather flap, one single piece, is folded backward over the top rear edge of "
"the bag and leans back behind the open mouth, clearly visible from the "
"front: the inside face of the flap stands behind the opening showing its two "
"round handle holes, its strap slots and its small gold plate, with the rear "
"rolled handle rising above it. The flap never covers the front of the bag "
"and never splits into pieces. The mouth of the bag is a clean open oval at "
"the top of the leather section, showing the natural cream cotton canvas "
"interior lining and the cognac leather slip pocket on the back interior "
"wall. The bag has NO zipper anywhere, no zipper track, no zipper teeth, no "
"zipper pull along the mouth of the bag, and no embossed text or lettering "
"anywhere on the bag. BOTH handles are clearly visible standing upright: the "
"front handle rises from the front leather band, the rear handle rises from "
"the back leather band in front of the folded back flap. Never omit the "
"front handle.")

HEROINE = ("the same clay heroine in every shot: a clay woman in her late twenties with "
"warm tan skin, dark chocolate brown hair sculpted into a low bun with two "
"loose face framing strands, big hazel eyes with tiny white catchlights, soft "
"rosy fingerprint blushed cheeks, small gold hoop earrings, wearing a cream "
"linen sundress with butter yellow trim and tiny woven sandals")

GULL = ("a small hand sculpted clay seagull with a round white body, dove grey wings, "
"a tiny orange beak, little orange stick legs and slightly crooked charming eyes")

MOTION = ("Stop motion animation cadence, twelve frames per second feel, tiny charming "
"jitters between poses, clay and fabric flex slightly as things move, nothing "
"moves with smooth digital motion.")
MOTION_BAG = ("The bag stays exactly as it appears in the first frame, silhouette, "
"materials, colors and details unchanged.")

FOOTER = ("Ambient sound only, no speech, no voiceover, no music. No on screen text, "
"no captions, no watermarks, no logos. One continuous shot. Vertical 9:16.")

FRAME_23 = ("Vertical 2:3 portrait composition, the main subject centered with generous "
"margins above and below so the frame survives a 9:16 center crop, no "
"borders, no letterboxing, no text.")

HERO_MATCH = ("The clay heroine in this shot is exactly the clay woman in the last "
"reference image, same face, same hair, same dress, same sandals.")
STYLE_ONLY = ("The reference image is only a style reference for the clay world and its "
"palette. The woman and the bag from the reference image do NOT appear in "
"this shot. No people and no bags anywhere in this shot.")

def gull(s): return s.replace("the clay seagull", "the clay seagull, " + GULL + ",", 1)

# ---------- film specs: scene text from the briefs ----------
# kf: (refs, [scene-flags]) flags: tote/week/open/hero/styleonly
F = {}

F["FERRY"] = {"dir": "VEL-CLAY-FERRY-01", "bag": "tote", "kf": [
 ([CARAMEL, HEROINE_PNG], "hero", gull("Golden afternoon on the open deck of a miniature clay coastal ferry. The clay heroine sits on a white slatted bench mid frame, the straw tote resting on the bench beside her, a golden brown clay croissant peeking out of the top of the tote. Her hair strands and dress hem lift in the wind. Behind the railing, a sculpted felt ocean with tiny white clay wave caps and a distant terracotta roofed harbor town. The clay seagull is landing on the deck railing at the right of frame, wings spread mid flap, eyes locked on the croissant.")),
 ([CARAMEL, HEROINE_PNG], "hero", gull("Close two shot standoff on the open deck of the miniature clay coastal ferry: on the left of frame the clay heroine sits on a white slatted wooden bench, leaning slightly over the straw tote beside her with her bare hand resting on the flap, one eyebrow raised, side eyeing the clay seagull. There are no tabs, no rivets, no pins, no studs and no attachments of any kind at the flap corners, and she wears no rings. On the right of frame the seagull perches on the white painted bench armrest, head tilted almost upside down, staring at the golden clay croissant sticking out of the tote between them. A white painted ferry railing and the felt ocean soft and out of focus behind them.")),
 ([CARAMEL, HEROINE_PNG], "hero", gull("On the white slatted wooden bench on the deck of the miniature clay coastal ferry, the clay heroine holds a torn piece of a golden clay croissant out toward the clay seagull in her open palm, a warm small smile on her face, the straw tote upright on the bench between them with the rest of the croissant tucked inside. The seagull leans forward from the white painted bench armrest, beak almost touching her palm, one wing lifted in excitement. White ferry railing and sparkling felt ocean behind them.")),
 ([CARAMEL, HEROINE_PNG], "hero", gull("Wide shot from behind the white slatted wooden bench on the open deck of the miniature clay coastal ferry: the clay heroine and the clay seagull sit side by side facing the sea over the white ferry railing, the seagull perched on her shoulder, the straw tote standing on the bench beside her glowing in low golden hour light. Ahead of the moving ferry a tiny clay lighthouse with a warm glowing tip stands on a rocky point, the felt ocean sparkling with sequin glints, the wooden deck planks in the foreground."))],
 "seg": [
 "The ferry rocks gently, the felt ocean waves slide past in looping stop motion, her hair strands and dress hem flutter in little jumps. The seagull finishes its landing on the railing, folds its wings in two jerky steps, and swivels its head toward the croissant peeking out of the straw tote. She has not noticed it yet, she gazes at the horizon. Ambient sound: low ferry engine hum, wind, water lapping, one distant ferry horn.",
 "A silent comic standoff in stop motion: the seagull tilts its head further in three little clicks, she narrows her eyes and slowly slides one protective hand toward the croissant in the tote, the seagull hops one step closer on the armrest, freeze, they stare at each other. The straw tote does not move. Ambient sound: wind, creaking bench wood, one soft questioning seagull chirp.",
 "She offers the torn piece of croissant in stop motion, the seagull takes it from her palm in one gentle careful peck, tosses its head back and swallows it whole with a happy little body wiggle, then does a tiny stomping dance of joy on the armrest. She laughs silently, shoulders bouncing. Ambient sound: wind, water, one delighted seagull squeak, the soft clay tap of the little dance.",
 "The ferry glides slowly toward the lighthouse in stop motion, sequin glints on the felt ocean shimmer frame by frame, her hair and dress flutter, the seagull on her shoulder ruffles its feathers once and settles, she leans her head slightly toward it. The straw tote stays perfectly still on the bench. Ambient sound: wind softening, water lapping, one far away ferry horn, gulls in the distance."]}

F["HARBOR"] = {"dir": "VEL-CLAY-HARBOR-01", "bag": "tote", "kf": [
 ([HEROINE_PNG], "styleonly", gull("Dawn over a miniature clay coastal harbor town: crooked pastel clay houses with terracotta roofs stacked along a cobblestone lane, striped canvas awnings still rolled up over tiny shopfronts, a felt ocean harbor with little clay fishing boats at the bottom of the lane, warm pink morning light. The clay seagull stands on a crooked lamppost in the upper part of frame, chest puffed, beak open mid cry.")),
 ([CARAMEL, HEROINE_PNG], "hero", "The clay heroine strolls down a cobblestone market lane of a miniature clay coastal town in morning light, the straw tote hanging from the crook of her elbow with a golden clay baguette and a bunch of pink clay peonies standing out of it. Market stalls line the lane: one piled with felt lemons, one with paper wrapped clay flowers, one with round clay melons. A round clay flower vendor woman with a headscarf waves from behind her stall."),
 ([CARAMEL, HEROINE_PNG], "hero", "Close macro shot of the straw tote hanging on the clay heroine's elbow in soft morning light: pink clay peonies and a golden clay baguette resting in the woven straw mouth of the tote, her other clay hand gently brushing along the braided straw edge trim, her white linen dress soft in the background. Every straw fiber of the real bag in crisp focus against the soft clay world."),
 ([CARAMEL, HEROINE_PNG], "hero", gull("Golden hour at a wooden dock edge: the clay heroine sits with her bare feet swinging above the felt water, the straw tote standing beside her on the sun bleached planks with peonies and a baguette leaning out of its woven mouth, the clay seagull sitting on her other side like an old friend, both facing the low sun over the harbor, long soft shadows. The mouth of the tote is plain woven straw all the way around: no leather lining, no leather panel, no leather wall anywhere at the mouth or behind the flowers, the peonies and baguette are surrounded by woven straw only, and the entire left side and back of the bag are woven straw."))],
 "seg": [
 "The town wakes in stop motion: the striped awnings flutter gently in the morning breeze, shutters click open on two windows, a tiny clay fisherman figure far below pushes a cart across the lane, smoke starts curling from one crooked chimney in puffy clay wisps. The seagull on the lamppost stretches its wings and cries twice. Ambient sound: morning gulls, soft harbor water, a distant low ferry horn, tiny shutter clicks.",
 "She strolls through the market in gentle stop motion steps, her dress swinging in little jumps, she nods and smiles at the waving flower vendor, a felt lemon wobbles and settles on the nearest stall as she passes. The straw tote swings softly on her elbow, the baguette and peonies bobbing slightly. Ambient sound: soft market murmur, gulls, a bicycle bell somewhere, her tiny footsteps on cobblestone.",
 "Macro stop motion: her clay fingertips travel slowly along the braided straw trim of the tote, one peony petal drops in two stop motion steps and lands on the leather flap, she tucks the peonies a little deeper into the tote with two gentle pushes. The bag itself never deforms. Ambient sound: close quiet, distant gulls, the tiny paper rustle of the flower stems.",
 "Her feet swing slowly over the water in stop motion, tiny sequin glints drift across the felt sea, the seagull sidesteps twice until it leans lightly against her hip, she tilts her head back into the last sun. The straw tote stays perfectly still beside her, glowing, its woven body, mouth and flap locked exactly as in the first frame: the mouth rim stays plain woven straw the entire clip, no leather lining or leather panel ever grows at the mouth, behind the flowers, or on any side of the bag. Ambient sound: calm evening water, one soft gull sound, far away harbor bells."]}

F["WOVEN"] = {"dir": "VEL-CLAY-WOVEN-01", "bag": "tote", "kf": [
 ([HEROINE_PNG], "styleonly", gull("An empty weathered wooden dock at dawn on a miniature clay coast, pale gold mist over a felt ocean, tall clay sea grass bending along the dock edge, a coil of harbor rope beginning to unwind by itself, single straw strands lifting off the dock into the air like ribbons, a ribbon of warm golden light peeling up off the water surface. The clay seagull watches from a wooden mooring post.")),
 ([CARAMEL], "forming", gull("Over weathered dock planks a swirling spiral of straw strands is weaving itself into the straw tote from the bottom up: the lower two thirds of the bag already complete and perfectly woven in warm sandy caramel with braided cross stitch trim, the top edge still dissolving into flying strands, the taupe leather flap pieces and two rolled leather handles hovering just above in the swirl waiting to land, all lit by a ribbon of golden light circling the spiral. The finished portion of the bag matches the bag in the first reference image exactly. The clay seagull leans far forward off its mooring post, mesmerized. No people anywhere in this shot.")),
 ([CARAMEL], "", gull("The finished straw tote stands alone in the center of a weathered wooden dock in first morning sun, complete and perfect, the last three loose straw strands tucking themselves into the weave, tiny straw dust motes settling around it, a felt ocean calm behind, the clay seagull standing on the dock two steps from the bag, head cocked in wonder. No people anywhere in this shot.")),
 ([CARAMEL, HEROINE_PNG], "hero", gull("The clay heroine walks away down a long wooden dock into the low golden morning sun carrying the straw tote, seen from behind at a slight distance, her dress and hair moving in the sea wind, the clay seagull flying low beside her at shoulder height, the felt ocean sparkling on both sides of the dock. At this distance the tote body reads as a fine, tight, almost smooth flat weave with tiny weave cells exactly as in the first reference image, no visible loops, no crochet texture, no knit texture, and only a thin subtle edge trim, never chunky braids. The bag held by the woman in the last reference image is NOT a reference for this bag, only the bag in the first reference image defines this bag weave, texture and construction. The flap silhouette keeps a clearly WIDE center panel about twice the width of each outer tab."))],
 "seg": [
 "Stop motion magic begins: the rope coil unwinds in little jumps, a dozen straw strands rise off the dock one by one and start to swirl in a slow spiral over the planks, the ribbon of golden light lifts off the water and joins the spiral, the sea grass leans toward it. The seagull tilts its head watching. Ambient sound: low wind, creaking dock wood, a soft airy shimmer of straw brushing straw.",
 "The weave rises in stop motion: strands lace the top edge row by row while the taupe leather flap, one connected piece with its wide center panel and 2 squared outer tabs, and the two rolled handles hover in the swirl just above the bag, slowly descending but never touching it. The golden light ribbon spirals tighter and tighter around the forming bag until its glow swells and fills the frame with warm golden light in the final moment. Nothing attaches to the bag on camera, nothing is added to the bag: no chunky braids, no braided columns, no metal buckles, no extra straps, no rings, no metal hardware of any kind. Ambient sound: rapid soft straw whispers, one rising warm shimmer.",
 "Quiet after the magic: the last strands tuck themselves in with three little pulls, straw dust settles in drifting stop motion motes, the golden light ribbon sinks back into the water, the seagull hops one careful step closer and gently taps the woven side with its beak, then looks up. Ambient sound: morning calm, water lapping, one tiny woody tap, a soft distant gull cry.",
 "An almost still living tableau in extremely gentle stop motion: she is mid stride and moves only barely, tiny slow steps, the tote hangs almost motionless at her side, its silhouette, flap and straps locked exactly as in the first frame for the entire clip. The world does the moving: sequin glints shimmer across the felt water, the seagull glides slowly beside her with small wingbeats, her dress hem and loose hair strands sway softly, her long shadow flickers over the planks. Ambient sound: wind, wings flapping softly, the morning sea."]}

F["WINDOW"] = {"dir": "VEL-CLAY-WINDOW-01", "bag": "week", "kf": [
 ([CHOC1, HEROINE_PNG], "hero", "Inside a miniature clay airplane cabin, warm and cozy: the clay heroine in the window seat gazing out, the closed weekend bag resting upright on the empty aisle seat beside her like a travel companion, a fabric seatbelt across her lap, a round clay window filled with puffy cotton clouds in blue sky, soft cabin light, a tiny fabric seatbelt sign glowing above the seats."),
 ([CHOC1, HEROINE_PNG], "hero", "A round clay airplane window fills most of the frame, the clay heroine's silhouette soft at the edge of frame: outside the window puffy cotton clouds are remolding themselves into rolling felt ocean waves with white clay wave caps, and far below a tiny clay lighthouse with a blinking warm light stands where the horizon meets the sea, dreamlike golden light pouring through the window. The closed weekend bag rests on the seat beside her at the very edge of frame."),
 ([CHOC1, HEROINE_PNG], "hero", "The clay heroine stands on the wet sand of a miniature clay beach at golden hour in her cream linen sundress and woven sandals, the closed weekend bag held in her hand, felt waves lapping a step away from her, and across the wet clay sand glides the shadow of an airplane shaped like a gliding gull, a clay lighthouse blinking on the rocky point behind her."),
 ([CHOC1, HEROINE_PNG], "hero", gull("Wide golden hour shot: the clay heroine walks along a shoreline toward a small crooked clay cottage with a glowing amber window on the dune, carrying the closed weekend bag, felt waves rolling in beside her, the clay seagull walking in her footprints behind her, a lighthouse blinking far in the background."))],
 "seg": [
 "Calm stop motion flight: cotton clouds drift past the round window in slow steps, the cabin sways almost imperceptibly, she rests her chin on her hand and watches the sky, one loose hair strand bobs. The weekend bag sits perfectly still on the seat beside her. Ambient sound: soft airplane cabin hum, a muffled gentle chime, quiet.",
 "Dream logic in stop motion: the cotton clouds knead and fold themselves into rolling felt waves one by one, the waves begin to move like a real sea, the tiny lighthouse light blinks in a slow heartbeat, the golden light through the window grows warmer and spills over her face. Ambient sound: the cabin hum slowly dissolving into wind and surf, one soft lighthouse bell.",
 "She arrives in stop motion: she takes two small steps on the wet clay sand leaving little footprints, a felt wave slides up close and retreats, the great gull shaped airplane shadow glides slowly across the beach and out of frame, she watches it pass and smiles. The weekend bag hangs still in her hand. Ambient sound: real surf, wind, one far seagull, the faintest fading airplane hum.",
 "She walks the shoreline in slow stop motion, waves roll and retreat in loops beside her, the cottage window glows warmer as she nears, the seagull hops from footprint to footprint behind her, wind lifts her hem in little jumps. Ambient sound: surf, wind, gulls, one soft porch windchime from the cottage."]}

F["SPILL"] = {"dir": "VEL-CLAY-SPILL-01", "bag": "week", "kf": [
 ([CHOC1, HEROINE_PNG], "hero", "A muted Sunday tidy clay apartment in grey blue tones: the clay heroine kneels on a woven rug facing the closed weekend bag standing on the floor in front of her, her hands resting on the two leather belt straps on its front, the room behind her neat and still, pale window light, a clay couch with felt cushions, everything in the room slightly desaturated except the warm cognac and cream bag."),
 ([OPEN_STILL, CHOC4, HEROINE_PNG], "hero open", "The weekend bag stands OPEN on a woven rug in a muted grey blue clay living room: grey blue plaster walls, a grey blue clay couch with felt cushions directly behind her, a framed clay seascape on the wall, a tall window on the left of frame with pale light, the whole room desaturated grey blue except the bag and its glow. The kneeling clay heroine faces the bag, warm golden light glowing up out of the open mouth of the bag into the grey room and onto her amazed face, and the first magic spilling out: a thin ribbon of seafoam felt water beginning to flow over the front of the bag and down to the rug, two tiny green felt beach grass blades sprouting where it lands."),
 ([os.path.join(CAMP, "VEL-CLAY-SPILL-01/keyframes/K4.png"), OPEN_STILL, HEROINE_PNG], "hero open", "A clay apartment mid transformation: half the room already a warm coastal porch with sun bleached wood and beach grass, the other half still grey apartment, string lights blooming across the ceiling bulb by bulb, the open weekend bag glowing at the center of the woven rug pouring out warm light and a small felt wave rising from its mouth, the clay heroine standing behind the bag turning slowly, arms open, face lit with joy. The bag is seen from the front three quarter angle with its folded back flap clearly visible leaning behind the open mouth and both rolled handles clearly visible."),
 ([OPEN_STILL, CHOC4, HEROINE_PNG], "hero open", gull("Full golden hour coastal porch: the clay heroine reclines in a wooden porch chair with her feet up on the rail, eyes closed in bliss, the open weekend bag standing on the porch boards beside the chair still breathing out a soft warm glow, the clay seagull perched on the porch railing, felt ocean and dunes beyond, string lights glowing overhead."))],
 "seg": [
 "Quiet stop motion: she kneels with both hands resting lightly on the two leather belt straps, she tilts her head as if she heard something inside the bag, a faint warm golden glow starts to seep out of the seam beneath the closed flap edge and pulses very softly, she leans closer and her eyes widen a little. Her hands never unfasten anything and never move the straps. The bag stays perfectly still and completely unchanged the entire clip, the flap stays closed, the belt straps stay exactly as in the first frame, the small gold oval turn lock and the two flat gold clasp plates stay exactly as in the first frame, no buckles ever appear on the bag. Ambient sound: quiet room tone, a clock ticking, one soft low shimmer slowly rising.",
 "The weekend spills out in stop motion: the seafoam felt wave flows off the bag and rolls across the floorboards in widening loops, beach grass sprouts up between the couch cushions blade by blade, warm golden light spreads across the walls washing the grey away, she rises to her feet in wonder. The bag itself never moves and never changes. Ambient sound: rising surf, tiny popping sprouts, a warm low shimmer.",
 "The remodeling completes in stop motion: apartment walls fold away like cardboard and porch beams rise into place, the string lights finish blooming, the felt wave settles into a calm glowing pool around the rug, sunlight floods in. She turns in place with her arms out, hair swinging. The open bag stays exactly as in the first frame at the center. Ambient sound: soft wooden creaks of the world rebuilding, surf arriving, one windchime.",
 "Golden hour stop motion calm: her chest rises and falls slowly, one hand hangs down and taps the chair arm once, the seagull ruffles and tucks its head, the string lights sway a little in the wind, the glow from the open bag pulses very softly like a heartbeat. Ambient sound: evening surf, windchime, one soft gull murmur, quiet."]}

F["MADAM"] = {"dir": "VEL-CLAY-MADAM-01", "bag": "week", "kf": [
 ([CHOC1, HEROINE_PNG], "hero", "Evening outside a grand miniature clay boutique hotel with a striped awning, warm glowing windows and topiary balls in clay pots: a tiny clay taxi pulls away at the edge of frame, the clay heroine stands at the foot of the marble front steps holding the closed weekend bag, and a round eager clay bellhop in a little red cap and jacket pushes open the brass door at the top of the steps."),
 ([CHOC1, HEROINE_PNG], "hero", "At the foot of the same grand clay boutique hotel steps as before, the green and white striped scalloped awning and stone facade visible above and behind them, the round clay bellhop in his red cap and red jacket with gold buttons proudly presents an enormous polished brass luggage cart, big enough for ten suitcases, and looks around the empty pavement for luggage with a puzzled tilted head, while the clay heroine stands serene beside the huge empty cart holding only the closed weekend bag, one eyebrow slightly raised, amused, evening lamplight."),
 ([CHOC1, HEROINE_PNG], "hero", "Close storybook shot: the clay heroine lifts the closed weekend bag lightly to chest height with one graceful hand and gives an astonished round clay bellhop a warm knowing smile, the bag glowing warm cognac and cream under hotel entrance lamps, the bellhop frozen mid gesture with wide clay eyes, red cap slightly askew, a giant empty brass luggage cart looming behind him."),
 ([CHOC1, HEROINE_PNG], "hero", gull("Inside a clay hotel lobby: a sweeping clay staircase with a red felt runner and a glowing chandelier of tiny amber beads, the clay heroine ascending mid staircase with the closed weekend bag in hand, dress swinging, the same round clay bellhop in his red jacket with gold buttons watching from the bottom of the stairs with his red cap held to his chest in admiration, the clay seagull perched outside on the lobby window sill silhouetted against the evening blue."))],
 "seg": [
 "Stop motion arrival: the taxi putters out of frame with a puff of clay smoke, she looks up at the hotel and straightens, the bellhop bounds down two steps with springy jerky enthusiasm and gestures a grand welcome with both arms. Ambient sound: quiet evening street, a tiny putter engine fading, a brass door swinging, one gull far away.",
 "Comic stop motion beat: the bellhop wheels the giant cart in a half circle, peers left, peers right, peers behind the topiary, lifts his cap and scratches his head with big clay gestures, the empty cart gleaming. She waits with perfect calm, a tiny amused smile growing. Ambient sound: cart wheels squeaking, his little confused hums, evening crickets starting.",
 "She raises the bag in one smooth stop motion arc and holds it there, the bellhop looks at the bag, then at her, then at his enormous cart, then back at the bag, and tips his cap with a small defeated bow of respect. She winks. Ambient sound: quiet evening, one small brass squeak from his cap, crickets.",
 "She ascends the staircase in graceful stop motion, the chandelier beads glitter frame by frame, her free hand glides along the banister, the bellhop sighs a happy little sigh at the bottom, the seagull outside taps the glass once with its beak. Ambient sound: warm lobby murmur, her steps on the felt runner, one tiny glass tap."]}

BAG_ID = {"tote": TOTE_ID, "week": WEEK_ID}
BAG_VID_PIN = {"tote": "The leather flap and belt straps exist only on the front face of the bag, the back face is plain woven straw. The leather flap stays ONE single seamless sheet folded all the way over, lying completely flat the entire clip: no gap, seam, or split ever opens anywhere in it, nothing behind it ever shows through it, and its cut edge shapes never separate into pieces. Contents lean out of the mouth behind the flap, never through it.",
               "week": "No zipper ever appears anywhere on the bag."}

# ---------- prompt composition ----------
def compose_kf(film, scene, flags, has_bag=True):
    parts = [scene]
    if "styleonly" in flags:
        parts.append(STYLE_ONLY)
    else:
        if has_bag:
            parts += [NOT_CLAY, BAG_ID[film["bag"]]]
            if film["bag"] == "tote" and "forming" not in flags:
                parts.append(TOTE_MECH)
        if "open" in flags:
            parts.append(MECHANISM)
        if "hero" in flags:
            parts += [HEROINE + ".", HERO_MATCH]
    parts += [STYLE, FRAME_23]
    return " ".join(parts)

def compose_seg(film, scene, has_bag=True, forming=False):
    parts = [scene, MOTION]
    if has_bag:
        if not forming:
            parts.append(MOTION_BAG)
        parts.append(BAG_VID_PIN[film["bag"]])
    parts.append(FOOTER)
    return " ".join(parts)

# ---------- kie plumbing ----------
def env_key():
    for line in open(os.path.join(VAULT, ".env")):
        if line.strip().startswith("KIE_API_KEY="):
            return line.strip().split("=", 1)[1]
    sys.exit("no KIE_API_KEY")

def api(method, url, key, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {key}")
    if data: req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=120, context=SSL_CTX) as r:
        return json.loads(r.read().decode("utf-8", "replace"), strict=False)

def state():
    return json.load(open(STATE_F)) if os.path.exists(STATE_F) else {"uploads": {}, "tasks": {}, "credits": {}}

def save(st): json.dump(st, open(STATE_F, "w"), indent=1)

def upload(path, key, st):
    path = os.path.abspath(path)
    if path in st["uploads"]:
        return st["uploads"][path]
    last = ""
    for attempt in range(4):
        if attempt: time.sleep(30 * attempt)
        out = subprocess.run(["curl", "-s", "-X", "POST", UPLOAD_API,
            "-H", f"Authorization: Bearer {key}",
            "-F", f"file=@{path}", "-F", "uploadPath=velantra-clay",
            "-F", f"fileName={int(time.time())}-{os.path.basename(path).replace(' ', '_')}"],
            capture_output=True, text=True)
        try: resp = json.loads(out.stdout)
        except ValueError: last = out.stdout or out.stderr; continue
        if resp.get("data", {}).get("downloadUrl"):
            st["uploads"][path] = resp["data"]["downloadUrl"]; save(st)
            print(f"  uploaded {os.path.basename(path)}")
            return st["uploads"][path]
        last = out.stdout
    sys.exit(f"upload failed {path}: {last[:200]}")

def download(url, dest):
    try:
        subprocess.run(["curl", "-sL", "-o", dest, url], check=True, capture_output=True, timeout=30)
        if os.path.getsize(dest) > 10_000: return dest
    except Exception: pass
    remote = f"/tmp/kie_dl_{os.getpid()}_{abs(hash(url)) % 100000}"
    subprocess.run(["ssh", "-o", "ConnectTimeout=10", VPS_RELAY,
                    f"curl -sL -o '{remote}' --max-time 90 '{url}'"], check=True)
    subprocess.run(["scp", "-q", f"{VPS_RELAY}:{remote}", dest], check=True)
    subprocess.run(["ssh", VPS_RELAY, f"rm -f '{remote}'"], check=False)
    return dest

def crop_916(src, dst):
    from PIL import Image
    im = Image.open(src); w, h = im.size
    nw = int(h * 9 / 16)
    if nw <= w:
        x = (w - nw) // 2; im = im.crop((x, 0, x + nw, h))
    else:
        nh = int(w * 16 / 9); y = (h - nh) // 2; im = im.crop((0, y, w, y + nh))
    im.save(dst)

def run_wave(jobs, key, st, kind):
    """jobs: list of dicts {id, model, input, dest, is_video}. Skips existing dests."""
    pending = []
    for j in jobs:
        if os.path.exists(j["dest"]) and os.path.getsize(j["dest"]) > 10_000:
            print(f"{j['id']}: exists, skip"); continue
        pending.append(j)
    results = {}
    for i in range(0, len(pending), WAVE):
        wave = pending[i:i + WAVE]
        for j in wave:
            tid = st["tasks"].get(j["id"])
            if not tid:
                resp = api("POST", f"{API}/jobs/createTask", key, {"model": j["model"], "input": j["input"]})
                if resp.get("code") != 200:
                    print(f"{j['id']}: createTask FAILED {resp}"); j["taskId"] = None; continue
                tid = resp["data"]["taskId"]
                st["tasks"][j["id"]] = tid; save(st)
            j["taskId"] = tid
            print(f"{j['id']}: task {tid}")
        live = [j for j in wave if j.get("taskId")]
        while live:
            time.sleep(15)
            for j in list(live):
                d = api("GET", f"{API}/jobs/recordInfo?taskId={j['taskId']}", key).get("data", {})
                s = d.get("state")
                if s == "success":
                    res = json.loads(d.get("resultJson") or "{}", strict=False)
                    urls = res.get("resultUrls") or []
                    if urls:
                        download(urls[0], j["dest"])
                        cc = d.get("creditsConsumed")
                        st["credits"][j["id"]] = cc; save(st)
                        print(f"  {j['id']} done ({cc} cr)")
                        results[j["id"]] = j["dest"]
                    live.remove(j)
                elif s == "fail":
                    print(f"  {j['id']} FAILED: {d.get('failCode')} {d.get('failMsg')}")
                    st["tasks"].pop(j["id"], None); save(st)
                    live.remove(j)
    return results

# ---------- commands ----------
def films_from_args(args):
    names = [a.upper() for a in args if a.upper() in F]
    return names or list(F.keys())

def cmd_assets(key, st):
    jobs = []
    if not os.path.exists(HEROINE_PNG):
        prompt = compose_kf({"bag": "tote"},
            "Character sheet portrait: the clay heroine stands facing the camera on a plain warm cream seamless studio backdrop, full body visible from head to sandals, holding the straw tote in the crook of her elbow, relaxed warm smile, soft window light. " + HEROINE + ".",
            "", has_bag=True)
        jobs.append({"id": "asset_heroine", "model": IMG_MODEL, "dest": HEROINE_PNG, "input": {
            "prompt": prompt, "input_urls": [upload(CARAMEL, key, st)],
            "aspect_ratio": "2:3", "resolution": "2K"}})
    if not os.path.exists(ENDCARD_PNG):
        prompt = (" ".join(["A full frame slab of soft cream clay filling the entire image, the word VELANTRA pressed deep into the clay in elegant tall serif capital letters, perfectly centered, a single subtle human thumbprint pressed into the clay a little below the word, warm golden side light raking across the surface making the pressed letters glow at their edges, a few tiny clay crumbs beside the letters. No people, no bags, no other objects, no other text anywhere. The reference image is only a palette reference.", STYLE, FRAME_23]))
        jobs.append({"id": "asset_endcard", "model": IMG_MODEL, "dest": ENDCARD_PNG, "input": {
            "prompt": prompt, "input_urls": [upload(HEROINE_PNG if os.path.exists(HEROINE_PNG) else CARAMEL, key, st)],
            "aspect_ratio": "2:3", "resolution": "2K"}})
    run_wave(jobs, key, st, "image")
    for p in (HEROINE_PNG, ENDCARD_PNG):
        if os.path.exists(p):
            crop_916(p, p.replace(".png", "-916.png"))

def cmd_keyframes(key, st, names):
    jobs = []
    for name in names:
        film = F[name]
        for i, (refs, flags, scene) in enumerate(film["kf"], 1):
            has_bag = "styleonly" not in flags
            dest = os.path.join(CAMP, film["dir"], "keyframes", f"K{i}.png")
            jobs.append({"id": f"{name}_K{i}", "model": IMG_MODEL, "dest": dest, "input": {
                "prompt": compose_kf(film, scene, flags, has_bag),
                "input_urls": [upload(r, key, st) for r in refs],
                "aspect_ratio": "2:3", "resolution": "2K"}})
    run_wave(jobs, key, st, "image")
    for j in jobs:
        if os.path.exists(j["dest"]):
            crop_916(j["dest"], j["dest"].replace(".png", "-916.png"))

def cmd_videos(key, st, names):
    jobs = []
    for name in names:
        film = F[name]
        for i, scene in enumerate(film["seg"], 1):
            kf = os.path.join(CAMP, film["dir"], "keyframes", f"K{i}-916.png")
            if not os.path.exists(kf):
                print(f"{name} S{i}: keyframe missing, skip"); continue
            flags = film["kf"][i - 1][1]
            has_bag = "styleonly" not in flags
            dest = os.path.join(CAMP, film["dir"], "output", f"seg_{i:02d}.mp4")
            jobs.append({"id": f"{name}_S{i}", "model": VID_MODEL, "dest": dest, "input": {
                "prompt": compose_seg(film, scene, has_bag, "forming" in flags),
                "first_frame_url": upload(kf, key, st),
                "aspect_ratio": "9:16", "resolution": "720p",
                "duration": 5, "generate_audio": True}})
    run_wave(jobs, key, st, "video")

def cmd_endcard_video(key, st):
    if not os.path.exists(ENDCARD_PNG.replace(".png", "-916.png")):
        sys.exit("endcard.png missing, run assets first")
    prompt = (" ".join([
        "Extremely slow push in toward the word VELANTRA pressed deep into a slab of soft cream clay, tiny dust motes drifting through warm golden raking light, the light very slowly warming. The pressed word VELANTRA stays pixel perfect sharp, legible and completely unchanged for the entire clip.",
        MOTION, "The only sound is three soft wooden xylophone notes, then silence.",
        "No speech, no voiceover. No captions, no watermarks. One continuous shot. Vertical 9:16."]))
    run_wave([{"id": "endcard_video", "model": VID_MODEL, "dest": ENDCARD_MP4, "input": {
        "prompt": prompt, "first_frame_url": upload(ENDCARD_PNG.replace(".png", "-916.png"), key, st),
        "aspect_ratio": "9:16", "resolution": "720p", "duration": 4, "generate_audio": True}}],
        key, st, "video")

def cmd_stitch(names):
    for name in names:
        film = F[name]
        outdir = os.path.join(CAMP, film["dir"], "output")
        segs = [os.path.join(outdir, f"seg_{i:02d}.mp4") for i in range(1, len(film["seg"]) + 1)]
        missing = [s for s in segs if not os.path.exists(s)]
        if missing:
            print(f"{name}: missing {[os.path.basename(m) for m in missing]}, skip"); continue
        parts = segs + ([ENDCARD_MP4] if os.path.exists(ENDCARD_MP4) else [])
        final = os.path.join(outdir, f"{film['dir']}-final.mp4")
        lst = final + ".list.txt"
        with open(lst, "w") as f:
            for p in parts: f.write(f"file '{p}'\n")
        subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", lst,
                        "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-r", "24",
                        "-c:a", "aac", "-b:a", "192k", final], check=True, capture_output=True)
        os.remove(lst)
        print(f"{name}: {final}")

def main():
    if len(sys.argv) < 2: sys.exit(__doc__)
    cmd, args = sys.argv[1], sys.argv[2:]
    key, st = env_key(), state()
    if cmd == "assets": cmd_assets(key, st)
    elif cmd == "keyframes": cmd_keyframes(key, st, films_from_args(args))
    elif cmd == "videos": cmd_videos(key, st, films_from_args(args))
    elif cmd == "endcard-video": cmd_endcard_video(key, st)
    elif cmd == "stitch": cmd_stitch(films_from_args(args))
    elif cmd == "credit": print(api("GET", f"{API}/chat/credit", key))
    elif cmd == "status":
        print(json.dumps({"tasks": st["tasks"], "credits": st["credits"],
                          "spent": sum(v for v in st["credits"].values() if v)}, indent=1))
    else: sys.exit(__doc__)

if __name__ == "__main__":
    main()
