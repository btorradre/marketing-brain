#!/usr/bin/env python3
"""Emit manifest.json for VEL-SOFIA-ONEBAG-01.

Beats 1-5 ship as STILLS (still images, held with a slow Ken Burns push in the edit).
Beats 6-9 ship as B-ROLL (Kling 3.0 i2v off the same audited keyframes).
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
VAULT = "/Users/brooksorradre2/Documents/marketing brain"
REFDIR = f"{VAULT}/brands/velantra/products/straw-birkin/product-images/straw birkin"

PRODUCT_LOCK = (
    "The bag is the exact Velantra Straw Tote from the first product reference image and every color "
    "matches that first reference image exactly: a structured hand woven straw tote in warm sandy caramel, "
    "tightly woven straw body with braided cross stitch trim along the edges, a smooth taupe leather flap "
    "folded over the top of the bag from the back: the flap is ONE single seamless piece of leather, its "
    "front lower edge cut into the silhouette of a wide center panel with 2 squared outer tabs, the leather "
    "fully continuous and unbroken between and above these shapes, with exactly 2 narrow slots through which "
    "the handles pass, two rolled taupe leather top handles, two taupe leather belt straps crossed on the "
    "front, white contrast stitching on all leather edges, no metal hardware, no logos. The leather flap, "
    "tabs and belt straps exist ONLY on the FRONT face of the bag, the back face is plain woven straw, no "
    "duplicated front detailing on any other face. The bag has ONLY the two rolled top handles, it has no "
    "shoulder strap and no crossbody strap of any kind, never add one. Keep the bag identical to the "
    "reference image, no added logos, no added hardware, no added straps."
)

FLAP_CLOSED_PIN = (
    "Flap construction: the taupe leather flap is ONE single seamless sheet of leather attached along the top "
    "rear edge of the tote and folded all the way forward over the front, lying completely flat and fully "
    "closed. The leather runs continuously and unbroken across the ENTIRE top of the bag from the far left "
    "edge to the far right edge, forming one uninterrupted top band with a single stitch line. Its front LOWER "
    "edge is cut into the shape of a wide center panel and 2 squared outer tabs, but these are shapes cut into "
    "the SAME single sheet, never separate applied panels, and they never each have their own finished top "
    "edge. The notches between those shapes start low, roughly halfway up the flap, and the leather bridges "
    "solidly above them, exactly as on the reference bag. No vertical gap ever reaches the top edge of the "
    "flap. The 2 narrow handle slots begin below the top edge and never break it. The only openings anywhere "
    "in the flap are those 2 handle slots. No gap, no seam, no split and no opening exists anywhere else in "
    "the flap, and nothing inside the bag is ever visible through the flap. The flap never splits into pieces, "
    "never lifts, never stands up, always folded all the way over. Nothing protrudes from the flap's lower "
    "edge: no nub, stud, tab, fastener or catch of any kind. Nothing sticks out of the bag anywhere and no "
    "contents are visible. HANDLES: the 2 rolled taupe leather top handles rise as two separate clean loops, "
    "one on the left and one on the right, well apart from each other, each passing through its own narrow "
    "slot. They never collapse flat onto the flap, never bunch or fold together into a mass, never form a "
    "puffy blob over the center panel, and are never wrapped, looped or threaded around any strap, buckle or "
    "other element. The 2 taupe leather belt straps lie crossed in an X over the front below the flap with "
    "rounded ends and white contrast stitching, exactly as on the closed reference bag. No metal hardware "
    "anywhere on the bag. The bag holds its structured upright shape and never slumps, sags or collapses."
)

KLING_FLAP_PIN = (
    "The leather flap stays ONE single seamless sheet folded all the way over, lying completely flat the "
    "entire clip: no gap, seam, or split ever opens anywhere in it, nothing behind it ever shows through it, "
    "and its cut edge shapes never separate into pieces. The two leather belt straps stay crossed in an X on "
    "the front the whole clip and never merge into one horizontal strap. The two rolled top handles stay two "
    "separate clean loops well apart from each other and never collapse, bunch or fold together into a mass "
    "over the center panel. No buckle, turn lock, clasp, stud, ring or metal fitting of any kind ever appears "
    "anywhere on the bag, and no shoulder strap ever appears. The bag keeps its structured shape and never "
    "slumps or deforms."
)

STYLE_LINE = (
    "Natural light street style photograph in bright clear summer daylight, editorial but candid, the way a "
    "real photo saved off a mood board looks, true to life color, realistic skin and fabric texture, subtle "
    "sensor grain, shallow but not extreme depth of field, vertical 9:16 framing. Warm sunbleached neutral "
    "palette of cream, white, tan, navy and denim. The leather is a clean unmarked warm tan taupe with no "
    "smudges, blotches, stains or discolored patches, and the straw is evenly woven with no smeared or "
    "flattened patches. The bag silhouette is clean against the background with no stray highlights, spikes "
    "or fragments protruding from any edge. Absolutely no text, captions, watermarks, logos, graphics, "
    "sparkles or corner glyphs anywhere in the image."
)

IMPERFECTIONS = (
    "Subtle inconsistent handheld micro jitter, slight rolling shutter wobble, natural light keeps shifting "
    "gently even when the subject is still, background movement continues throughout. No text or captions on "
    "screen."
)

SHOTS = [
    {
        "id": "S01", "beat": 1, "time": "0:00-0:05", "dur": 5, "kind": "still",
        "vo": "If you buy one handbag this summer, make it a woven raffia tote.",
        "ref_beat": "swipe frame 1 - product hero against a plaster wall, hook card sits over this",
        "keyframe_prompt": (
            "A product still life photograph with no people anywhere in frame. The caramel straw tote stands "
            "upright and centered on a warm sandstone step in front of a rough cream plaster wall, "
            "photographed straight on from the front so the entire front face of the bag reads clearly in the "
            "middle of the frame. Hard midday summer sun rakes across the wall from the left and throws a "
            "crisp dark shadow of the bag onto the stone to the right. The bag sits squarely on its flat "
            "base holding its structured rectangular shape. Both rolled leather handles stand up in two "
            "separate clean loops. Generous empty wall above the bag."
        ),
        "motion_prompt": "",
    },
    {
        "id": "S02", "beat": 2, "time": "0:05-0:13", "dur": 8, "kind": "still",
        "vo": "There are a lot of bags trending right now, but this is the one I actually reach for all summer, because it works for real life.",
        "ref_beat": "swipe frame 8 - walking away down an old town street",
        "keyframe_prompt": (
            "A candid street style photograph of a woman seen entirely from behind, walking away from the "
            "camera down a narrow sunlit old town street paved in pale stone, warm honey colored stone "
            "buildings and a tall arched wooden door behind her. Her face is completely out of frame and "
            "never visible. She has dark hair loosely tied up and wears a crisp white linen shirt, black "
            "tailored shorts and flat tan leather sandals. She carries the caramel straw tote in her right "
            "hand down at her side, the bag rotated so its decorated front face is turned toward the camera. "
            "Bright hard midday sun with deep crisp shadows across the street."
        ),
        "motion_prompt": "",
    },
    {
        "id": "S03", "beat": 3, "time": "0:13-0:21", "dur": 8, "kind": "still",
        "vo": "It instantly makes any outfit feel more summery. You could be wearing jeans and a white tee and it still looks effortless.",
        "ref_beat": "swipe frame 12 - cropped body shot, simple outfit",
        "keyframe_prompt": (
            "A candid street style photograph cropped from the collarbone down to the knee so that no face "
            "and no head are visible anywhere in frame. She wears a simple fitted white cotton tee tucked "
            "into straight leg mid blue jeans. She holds the caramel straw tote in front of her right hip by "
            "both rolled handles gathered in one hand, the full front face of the bag square to the camera "
            "and completely unobstructed. Behind her a sunlit pale stucco wall with a soft cast shadow. "
            "Bright natural daylight."
        ),
        "motion_prompt": "",
    },
    {
        "id": "S04", "beat": 4, "time": "0:21-0:33", "dur": 12, "kind": "still",
        "vo": "Mine is the Sofia from Velantra. It is hand woven, the handles and the flap are real leather, and it is structured, so it holds its shape. You can set it down and it stands up on its own.",
        "ref_beat": "swipe frame 16 - bedroom mirror selfie. CLEANEST PRODUCT READ OF THE AD",
        "keyframe_prompt": (
            "A candid bedroom mirror selfie photograph. A woman stands in front of a full length mirror in a "
            "bright airy bedroom with white walls, pale wood floors and an open wardrobe rail of neutral "
            "clothing along the left edge of frame. She holds a phone up in front of her face so the phone "
            "completely covers her face and no facial features are visible at all. She wears a white ribbed "
            "cotton tank top and cream wide leg linen trousers. The caramel straw tote hangs from her left "
            "forearm at hip height, rotated so its full front face is square to the mirror and completely "
            "unobstructed, with the leather flap, the crossed belt straps, the two separate handle loops and "
            "the woven straw texture all large and clearly legible. Soft bright window daylight from the "
            "right."
        ),
        "motion_prompt": "",
    },
    {
        "id": "S05", "beat": 5, "time": "0:33-0:40", "dur": 7, "kind": "still",
        "vo": "It is also so versatile. Beach, lunch, vacation, errands.",
        "ref_beat": "swipe frame 24 - beside a vintage car on a village street",
        "keyframe_prompt": (
            "A candid travel photograph of a woman standing beside an old red vintage car parked on a narrow "
            "sunlit village street with warm stone walls and painted wooden shutters behind. She is turned "
            "away in profile with her head tipped back and dark sunglasses on, so her face is barely visible "
            "and never front on. She wears an oversized white cotton shirt open over a swimsuit with pale "
            "shorts and flat leather sandals. She holds the caramel straw tote down in her left hand, the "
            "front face of the bag turned toward the camera. Hard bright midday holiday sun."
        ),
        "motion_prompt": "",
    },
    {
        "id": "S06", "beat": 6, "time": "0:40-0:46", "dur": 6, "kind": "broll",
        "vo": "And it is such a good mom bag. It fits a towel, snacks, sunscreen, my whole day, and it still looks good at dinner.",
        "ref_beat": "swipe frame 31 - high overhead angle, white dress",
        "keyframe_prompt": (
            "A candid photograph taken from a high angle looking steeply down at a woman walking along a "
            "sunlit pavement, so she is strongly foreshortened and the top of her head hides her face "
            "completely. She wears a long white cotton summer dress and flat black sandals with a small "
            "string of pearls at her neck. She carries the caramel straw tote in her right hand down at her "
            "side, the front face of the bag turned up toward the camera, the bag sitting full and heavy and "
            "holding its structured shape. Bright hard sunlight with a sharp shadow on the pavement."
        ),
        # v1 mutated: walking + bag small in frame + arm swing = documented drift trigger.
        # v2 removes the walk entirely; only the person and the light move.
        "motion_prompt": (
            "The camera holds completely still at the same high angle looking down. She stands in place and "
            "shifts her weight very slightly, and the hem of her dress settles around her. Her hair moves a "
            "little in the breeze. Leaf shadows drift slowly across the pavement. Her arm and hand do not "
            "move at all: the bag hangs completely frozen and level at her side and stays pixel for pixel "
            "identical to the first frame for the whole clip, never swinging, rotating, tilting, rising, "
            "falling or changing shape. She does not walk, does not step and does not turn."
        ),
    },
    {
        "id": "S07", "beat": 7, "time": "0:46-0:52", "dur": 6, "kind": "broll",
        "vo": "It works with dresses and denim and linen and pretty much everything in your summer closet.",
        "ref_beat": "swipe frame 37 - crossing a street in wide denim",
        "keyframe_prompt": (
            "A candid street style photograph of a woman crossing a wide sunlit city street on a marked "
            "crosswalk, photographed from the side at hip height so she is seen in profile with her face "
            "turned away from the camera and mostly hidden behind her long dark hair. She wears a loose "
            "oversized white cotton shirt with the sleeves pushed up, wide leg mid blue jeans and tan "
            "leather sandals. She carries the caramel straw tote in her right hand at her side, the front "
            "face of the bag square to the camera. Warm late afternoon sun with long shadows across the "
            "asphalt."
        ),
        "motion_prompt": (
            "The camera holds completely still. She walks steadily across the frame from left to right. Her "
            "shirt and her hair move with her stride. She carries the bag held still and level in her hand, "
            "the bag barely moving and never swinging, twisting or rotating. Background traffic and "
            "pedestrians stay soft and distant."
        ),
    },
    {
        "id": "S08", "beat": 8, "time": "0:52-0:59", "dur": 7, "kind": "broll",
        "vo": "So it is practical, but it is also timeless. A woven tote comes back every single summer, so you will wear this one for years.",
        "ref_beat": "swipe frame 43 - close, both hands on the handles",
        "keyframe_prompt": (
            "A close candid photograph of a woman framed from the chin down to the waist so that no face is "
            "visible anywhere in frame. She wears a fine navy knit cardigan over a white top with cream "
            "trousers. She holds the caramel straw tote up at chest height in front of her with both hands "
            "resting on the two rolled leather handles, the full front face of the bag square to the camera "
            "and filling most of the frame, the woven straw texture and the white contrast stitching on the "
            "leather clearly visible. Soft even natural daylight against a plain warm off white wall."
        ),
        "motion_prompt": (
            "The camera holds completely still. She lifts the bag a few centimetres and settles it again, "
            "and one thumb slides slowly along the top of a rolled leather handle. The bag stays square to "
            "the camera and almost completely still throughout. Her cardigan shifts very slightly. Nothing "
            "else in the frame moves. Her hands never touch, lift or open the leather flap."
        ),
    },
    {
        "id": "S09", "beat": 9, "time": "0:56-1:03", "dur": 8, "kind": "broll",
        "vo": "If I was building my summer wardrobe from scratch, this is the first thing I would buy. I have carried mine almost every day since June and people still ask me where it is from.",
        "ref_beat": "swipe frames 49-55 - wide boulevard, the conviction beat",
        "keyframe_prompt": (
            "A wide candid street style photograph of a woman standing still on a broad sunlit tree lined "
            "boulevard with pale stone buildings far behind her. She stands turned away from the camera and "
            "glances back over her shoulder wearing dark sunglasses, so her face reads only as a small "
            "distant profile. She wears a navy short sleeve tee, cream wide leg trousers and flat tan "
            "sandals. The caramel straw tote is hooked over her right forearm and held still at her hip, the "
            "front face of the bag turned toward the camera. Bright clear summer daylight, long shadows "
            "across the pavement, green trees overhead. She is small in a wide frame with generous empty sky "
            "and pavement around her."
        ),
        "motion_prompt": (
            "The camera holds completely still in a wide shot. She stands in place and holds her look back "
            "over her shoulder toward the camera. Only small things move: her hair lifts slightly in the "
            "breeze, the leaves overhead move, and one distant pedestrian walks slowly far behind her. Her "
            "arm and the bag stay completely still, the bag does not swing, rotate or move at all."
        ),
    },
    {
        "id": "S10", "beat": 10, "time": "1:03-1:09", "dur": 6, "kind": "still",
        "vo": "It comes in a bunch of colors, mine is the caramel. I will leave the link below.",
        "ref_beat": "swipe frames 56-60 - the CTA card sits over this, calm frame with headroom for type",
        "keyframe_prompt": (
            "A candid photograph of the caramel straw tote set down on the seat of a pale wooden cafe chair "
            "on a sunny terrace. A woman is seated at the table beside it but only her cream trousers and "
            "tan leather sandals are visible at the right edge of frame, no face, no head and no upper body "
            "anywhere in frame. The bag sits squarely upright on the chair seat holding its structured "
            "shape, its front face turned toward the camera. Dappled sunlight, soft green foliage and a "
            "warm stone wall far behind, everything behind the chair thrown gently out of focus. The bag "
            "sits low in the frame with generous quiet empty space across the whole upper third."
        ),
        "motion_prompt": "",
    },
]

MANIFEST = {
    "concept": "VEL-SOFIA-ONEBAG-01",
    "product": "The Sofia Woven Tote - Caramel",
    "reference_ad": "Marisa Wise IG reel DZLA4ilxHv0 (raffia tote category recommendation), 69.2s",
    "format": "full-bleed stills + b-roll, floating talking-head cutout overlaid by editor",
    "split": "S01-S05 ship as stills (majority). S06-S09 ship as Kling 3.0 b-roll.",
    "pipeline": "gpt-image-2-image-to-image keyframes -> kling-3.0/video (b-roll only) -> ElevenLabs single-track VO",
    "aspect_ratio": "9:16",
    "image_resolution_still": "2K",
    "image_resolution_broll": "1K",
    "kling_mode": "std",
    "refs": {"caramel": f"{REFDIR}/caramel 1.png"},
    "product_lock": PRODUCT_LOCK,
    "flap_closed_pin": FLAP_CLOSED_PIN,
    "kling_flap_pin": KLING_FLAP_PIN,
    "style_line": STYLE_LINE,
    "imperfections": IMPERFECTIONS,
    "shots": SHOTS,
}

if __name__ == "__main__":
    with open(os.path.join(HERE, "manifest.json"), "w") as f:
        json.dump(MANIFEST, f, indent=1)
    print(f"wrote manifest.json  shots={len(SHOTS)}  "
          f"stills={sum(1 for s in SHOTS if s['kind']=='still')}  "
          f"broll={sum(1 for s in SHOTS if s['kind']=='broll')}")
