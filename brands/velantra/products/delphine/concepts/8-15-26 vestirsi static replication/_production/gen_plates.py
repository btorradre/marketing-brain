#!/usr/bin/env python3
"""THE DELPHINE — Vestirsi 5-format static replication. Clean plates, no text.

Five Vestirsi statics replicated one-to-one on layout, recast for the Velantra
avatar and the Delphine 25 cm handbag:

  D1 new-arrival     <- V1 studio duo, centered caps + subhead, wordmark bottom
  D2 everyday-size   <- V2 full-length model, quote block in left negative space
  D3 effortless      <- V3 4:5 waist-down crop, wordmark left / tagline right
  D4 on-the-fence    <- V4 editorial studio, tracked-caps pull quote lower third
  D5 everyday-staple <- V5 coastal close crop, back to camera, white type lower

The vibe is DELIBERATELY NOT the reference. Vestirsi casts a 25-year-old in a
cold NYC studio with an aloof stare. Ours is the Velantra ICP (`research/
icp-branding/Ideal_Customer_Profile.md`): Caroline, early forties, coastal,
linen and light denim, warm and already arrived. Same layout, opposite
temperature.

Every plate is i2i-anchored on the REAL 25 cm photography in
`products/delphine/real-product/`, never on the 46 cm Eleanor stills — the law
from the 8/15 scrap (see PRODUCT-TRUTH.md 2b).

Plates render CLEAN. All type is composited in compose.py so the typography is
pixel-correct and the copy stays swappable.

Idempotent: skips any plate whose PNG already exists (delete it to regenerate).
"""
import json, os, time, urllib.request, subprocess

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

# --- LOCKED PRODUCT TRUTH (PRODUCT-TRUTH.md 2b, the REAL 25 cm spec) ----------
#
# This bag is NOT a scaled Eleanor. Four things the Eleanor references do not
# carry and that every prompt must state: the domed/arched flap top, the belt
# straps running outward to a roller buckle on each side gusset, the small gold
# feet on the base, and leather that reads warm chestnut with visible grain.

LC = dict(canvas="cream ivory canvas", leather="warm chestnut brown")
DC = dict(canvas="cream ivory canvas", leather="very dark espresso brown, nearly black in shadow")
AG = dict(canvas="deep muted olive green canvas", leather="warm chestnut brown")


def identity(cw):
    return (
        f"a small structured top handle handbag, nearly square from the front and noticeably deep front "
        f"to back. Its upper section is {cw['leather']} leather with visible natural grain, shaped as a "
        f"domed arched flap folded down flat over the front, sitting over a lower body of {cw['canvas']}. "
        f"Two short rolled leather top handles rise from the leather band. A small gold turn lock sits at "
        f"the front centre of the flap. Two leather belt straps run roughly horizontally across the front, "
        f"angling slightly down toward the centre, each passing through a flat gold plate with an oblong "
        f"slot and continuing outward to a small gold roller buckle on each side gusset. A small leather "
        f"clochette tag hangs on a long leather tab at the front centre. Leather corner patches finish the "
        f"bottom, and small gold feet sit along the bottom edge. Visible stitching throughout, warm brass "
        f"gold hardware, and no logos, no lettering and no embossing anywhere on the bag."
    )


# SMALL-SCALE BLOCK. Validated 2026-08-14 and the single most important
# instruction on this product: state the dimensions bluntly, name it a handbag,
# rule out the larger silhouettes by name, and give the two visible consequences.
SCALE = (
    "The bag is SMALL. It is a compact everyday handbag measuring 25 cm wide, 22 cm tall and 14 cm deep, "
    "about 10 by 8.7 by 5.5 inches. It is a handbag and it is never a travel bag, never a weekender, "
    "never a duffel and never a large tote. Two visible consequences that must both show: the rolled top "
    "handles arch only about three inches above the top edge of the bag, and the gold fittings stay full "
    "size so they read LARGE against the small front panel. Held in one hand at her side the bag hangs no "
    "lower than the top of her hip, and carried in the crook of her elbow it sits compactly against her "
    "forearm, clearly smaller than her forearm is long."
)


def construction(cw):
    return (
        f"The bag in frame is an exact copy of the bag in the first reference image in silhouette, "
        f"proportions, materials and details. The two rolled top handles are smooth simple leather tubes "
        f"with no wrapping, no braiding and no woven texture, and each is one single continuous unbroken "
        f"loop. The bag is fully closed exactly as in the reference image: the one piece leather flap is "
        f"folded down flat over the front with its domed arched top edge clearly readable, both leather "
        f"belt straps are threaded through their flat gold slotted plates and fastened outward to the "
        f"gold roller buckle on each side gusset, and the gold turn lock sits closed at the front centre. "
        f"Both top handles are anchored directly into the {cw['leather']} leather upper section with "
        f"sturdy leather bases, never into the {cw['canvas']}. The leather and the canvas meet in one "
        f"clean horizontal line at exactly the same height as on the reference bag. The bag is carried by "
        f"its two short rolled top handles only: it has no shoulder strap, no crossbody strap and no long "
        f"strap of any kind anywhere in the frame. The bag has no zipper anywhere and no embossed text or "
        f"lettering anywhere on it."
    )


# MANDATORY DETAIL CORRECTIONS. Four defects that appear on essentially every
# first roll of this silhouette, all four prompt-fixable. Phrased POSITIVELY --
# stating what is there rather than listing what to avoid (MODERATION LAW).
DETAILS = (
    "Four details must be rendered correctly. First, each belt strap is a continuous piece of leather "
    "that visibly runs from the gold plate outward across the canvas to its side buckle, so the gold "
    "plates always sit ON a leather strap. Second, the leather band carries exactly one gold turn lock "
    "and that is the only round gold fitting on the front. Third, each side tab along the lower edge of "
    "the flap carries its own small vertical oval slot. Fourth, every leather surface on the bag is the "
    "same smooth grained leather with a soft even sheen, on the flap, the band, the handles, the corner "
    "patches and the straps alike."
)


def match(cw):
    return (
        f"The handbag is the exact bag shown in the first reference image, matching its construction, "
        f"proportions, materials, gold hardware and colour exactly. The leather is {cw['leather']}, the "
        f"same tone as in the first reference image and never a pale or orange tan, and the lower body is "
        f"{cw['canvas']}. All leather on the bag is one single shade and one single finish."
    )


# --- LOCKED CASTING (the Velantra ICP, not the reference's model) -------------
#
# NO NECKLACES: fine chains render as mangled gold smears. Small earrings only.
# Hands described POSITIVELY -- naming hand defects to avoid trips the filter.

MODEL = (
    "The woman is in her early forties, with warm skin showing real visible texture and fine lines at "
    "her eyes, no heavy makeup, natural brows and bare lips with a little gloss. Her hair is loose and "
    "slightly undone with a few strands moving, never slicked back. She wears small simple earrings and "
    "no necklace and no other jewelry at all, nothing around her neck. She looks relaxed, warm and "
    "unposed, in the middle of an ordinary good day, with an easy natural expression, never a cold hard "
    "editorial stare and never a wide posed grin. She is slim and healthy looking, comfortable in her "
    "body and standing at ease. Her hands are rendered cleanly and naturally, with five well formed "
    "fingers on each visible hand, each finger clearly separated and correctly proportioned, in a "
    "relaxed everyday grip."
)

# One face per plate. Four distinct castings so the set never reads as one woman
# photographed five times.
CAST = {
    "D2-everyday-size":
        "She has shoulder length sun lightened light brown hair worn loose, green hazel eyes and a "
        "narrow face with soft cheekbones. Small thin gold hoop earrings.",
    "D4-on-the-fence":
        "She has dark hair cut to the jaw with natural silver coming in at her temples, dark brown eyes, "
        "light olive skin with visible fine lines and a calm even featured face. Small gold stud earrings.",
    "D5-everyday-staple":
        "She has long dark brown hair falling loose past her shoulders and deep warm brown skin with a "
        "natural sheen. Small gold ball earrings.",
    "D3-effortless": "",   # waist-down crop, no face in frame
}

# GRIP. Two documented failure modes on this concept: an inert hand resting flat
# on the flap while the handles stand untouched, and a high pinch on the handle
# TOPS that terminates both handles inside the fist with no arc between them.
# Grip LOW on the legs, tube visible above and below the fingers.
GRIP = (
    "How she holds it, this matters and must be exactly right: the two short rolled leather top handles "
    "rise from the leather band and her fingers curl completely around them low down, close to where the "
    "handles enter the band, so each handle tube is clearly visible both ABOVE her curled fingers and "
    "BELOW them, passing through her hand the way a real bag handle does. Each handle is one single "
    "continuous unbroken loop of leather and both complete handle arches read fully along their entire "
    "length. The tops of the handles reach up into her hand, never stopping short below it, and her hand "
    "always closes on leather. The weight of the bag visibly hangs from that grip."
)

STYLE = (
    "Photorealistic editorial lifestyle fashion photograph, shot on a full frame camera with an 85mm "
    "lens at f2.8, natural available light, soft film grain, real skin texture and real fabric texture. "
    "Absolutely no text, no words, no letters, no captions, no watermarks and no logos anywhere in the "
    "image. The bag is closed and nothing is leaning out of it. Only one person in the frame, and no "
    "luggage, no suitcase and no other bag anywhere in the shot."
)

# Anti-CGI footer. The 3D-render look is a global reject condition
# (feedback_no_3d_render_look). Perfect bilateral symmetry is the strongest
# single render tell, so it is named explicitly.
ANTI_CGI = (
    "This is a real photograph taken with a real camera, not a computer rendering. It must not look like "
    "a 3D model, a CGI product visualisation, Octane, Blender, Cinema 4D or any game engine. The leather "
    "shows real grain and slight uneven creasing where it folds, the canvas shows real woven fibre "
    "texture, the gold hardware shows real specular highlights with tiny imperfections, and the bag casts "
    "one real soft contact shadow. The bag is very slightly asymmetric the way a handmade bag is, never "
    "perfectly mirrored left to right."
)

# --- SCENES: one per Vestirsi format, laid out for the type that lands later ---

VARIATIONS = [
    (
        # V1: two raffia bags on a warm seamless, top third empty for the type,
        # wordmark bottom centre. Ours = two colorways, the launch story.
        "D1-new-arrival", ["LC-01.png", "DC-01.png"], LC,
        "STILL LIFE PRODUCT PHOTOGRAPH, NO PERSON ANYWHERE IN THE FRAME. Vertical 9 by 16 frame. TWO of "
        "these handbags stand together on a smooth warm off white seamless studio sweep in colour "
        "#F5F2EC, the floor curving up into a seamless back wall with no visible corner or edge. The bag "
        "on the left is the cream ivory canvas and warm chestnut brown leather version shown in the "
        "first reference image. The bag on the right is the same bag in the cream ivory canvas and very "
        "dark espresso brown leather version shown in the second reference image. Both bags are "
        "identical in construction, proportion and hardware and differ only in the colour of their "
        "leather. They stand upright on their gold feet, angled slightly toward each other, the left bag "
        "set a little forward and lower and the right bag a little further back and higher, overlapping "
        "slightly so they read as a pair. Shot from slightly below the height of the bags with a long "
        "lens so they feel substantial. Soft diffused daylight falls from the upper left, and each bag "
        "casts one soft contact shadow onto the sweep. "
        "CRITICAL COMPOSITION RULE: the two bags together fill the LOWER TWO THIRDS of the frame. The "
        "ENTIRE TOP THIRD of the frame is nothing but the smooth empty warm off white wall, a clean "
        "unbroken pale gradient with no object, no shadow and no detail in it at all, because pale text "
        "will be placed there afterwards. Leave a clear band of empty pale sweep across the very bottom "
        "of the frame as well.",
    ),
    (
        # V2: full-length model against a plain white studio wall over a polished
        # concrete floor, shot in profile, all the type in the LEFT negative space.
        "D2-everyday-size", ["LC-01.png"], LC,
        "She is standing in a bright plain studio: one smooth continuous white painted wall behind her "
        "and a polished pale grey concrete floor beneath her, nothing else in the room at all. She "
        "wears a fitted white short sleeve cotton tee tucked loosely into wide leg light wash blue "
        "jeans with the hems turned up once, and flat brown leather shoes. She stands in profile facing "
        "the right hand side of the frame, weight on one hip, her far hand slipped into her back pocket. "
        "Her near arm hangs relaxed at her side and she carries the handbag from her hand, the bag "
        "hanging beside her hip. She is looking down and slightly behind her with a soft unhurried "
        "expression. Even soft daylight, quiet neutral colour grade, gentle shadow on the wall behind "
        "her. "
        "CRITICAL FRAMING RULE: she stands well over on the RIGHT hand side of the frame, her body "
        "occupying only the right third, and she is framed head to foot with her whole body inside the "
        "frame. "
        "CRITICAL EMPTY SPACE RULE: the entire LEFT HALF of the frame is nothing but the smooth empty "
        "white wall, a clean unbroken pale surface with no object, no fixture, no doorway, no dark patch "
        "and no strong detail anywhere in it, because dark text will be placed there afterwards and must "
        "stay easy to read.",
    ),
    (
        # V3: 4:5, cropped waist-down, bag hanging from the hand, wordmark left and
        # tagline right across the middle band. The one plate with no face.
        "D3-effortless", ["AG-01.png"], AG,
        "CROPPED FRAMING, NO FACE AND NO HEAD IN THE FRAME. Vertical 4 by 5 frame showing the woman only "
        "from just below her ribcage down to her feet. She stands against one smooth continuous pale "
        "greige painted wall over a polished pale concrete floor, nothing else in the room. She wears a "
        "loose cream linen shirt with the sleeves pushed up, untucked and cropped by the top edge of the "
        "frame, over wide leg light wash blue jeans with the hems turned up once, and flat dark brown "
        "leather shoes. She stands with her weight on one hip, turned very slightly toward the camera. "
        "Her near arm hangs straight down at her side and she carries the handbag from that hand, the "
        "bag hanging beside her thigh at about the height of her fingertips. Soft even daylight, quiet "
        "neutral colour grade. "
        "CRITICAL COMPOSITION RULE: her legs and the hanging bag occupy the centre and right of the "
        "frame. The wall behind her is one clean unbroken pale surface across the full width, with no "
        "object, no fixture, no doorway and no dark detail anywhere in it, because text will be placed "
        "across the middle of the frame on both the left and the right side and must stay easy to read.",
    ),
    (
        # V4: editorial studio, C-stand in shot, bag held in the crook of the elbow
        # against the body, lower third kept pale for the tracked-caps pull quote.
        "D4-on-the-fence", ["DC-01.png"], DC,
        "She is standing in a warm off white photography studio with a single slim chrome C stand light "
        "stand visible along the left edge of the frame, one smooth pale plaster wall behind her and a "
        "pale painted floor beneath her. She wears a long oatmeal wool coat worn open over a cream "
        "cotton top and wide leg ivory linen trousers, with flat leather sandals. She stands turned "
        "three quarters toward the camera and carries the handbag tucked up into the crook of her bent "
        "elbow, held in close against the front of her body at waist height, one hand resting easily "
        "over the handles. She is looking straight into the camera, calm and warm and self assured, with "
        "the faintest hint of a smile. Warm directional studio light from the upper left throwing one "
        "soft shadow onto the wall behind her, quiet low contrast colour grade. "
        "CRITICAL FRAMING RULE: she is framed from just above her head down past her knees, standing "
        "slightly left of centre, and the whole handbag including its lowest corner sits inside the "
        "UPPER HALF of the frame, no lower than halfway down. "
        "CRITICAL EMPTY SPACE RULE: the entire bottom two fifths of the frame shows only the smooth pale "
        "fabric of her coat and trousers and the softly out of focus pale wall and floor behind them. "
        "The bag and both of her hands stay entirely above that area. It is a calm even light toned "
        "expanse with no pattern, no clutter, no dark object and no strong detail, because dark text "
        "will be placed there afterwards and must stay easy to read.",
    ),
    (
        # V5: coastal, hazy and warm, back to camera, close crop, white type over
        # the pale dress in the lower third.
        "D5-everyday-staple", ["LC-01.png"], LC,
        "She is standing on a wide pale sand beach at the very end of the afternoon, photographed from "
        "BEHIND with her back to the camera, the soft out of focus sea and a bright hazy sky filling the "
        "background. She wears a soft cream cotton sundress that falls in loose folds. She holds the "
        "handbag behind her at the small of her back, both hands wrapped low around its two rolled top "
        "handles, the bag resting against the back of her dress. Her head is turned slightly away and "
        "her dark hair moves a little in the breeze. Warm hazy backlight from the low sun, soft glowing "
        "highlights, gentle warm summer colour grade, a dreamy shallow depth of field. "
        "CRITICAL FRAMING RULE: this is a CLOSE crop from the top of her shoulders down to her knees, "
        "her head mostly above the top edge of the frame, so the handbag is large and completely "
        "readable in the centre of the frame with the sharpest focus of the whole image falling on its "
        "leather, canvas and gold fittings. The whole bag sits inside the UPPER TWO THIRDS of the frame. "
        "CRITICAL EMPTY SPACE RULE: the entire bottom third of the frame shows only the smooth pale "
        "cream fabric of her dress falling in soft folds and the softly out of focus pale sand beside "
        "it. It is a calm light toned expanse with no pattern, no clutter and no dark detail, because "
        "white text will be placed there afterwards.",
    ),
]

ASPECT = {"D3-effortless": "4:5"}   # everything else is 9:16


def api(url, payload=None, headers=None):
    """Calls go through curl, not urllib.

    This Python has no root-certificate bundle wired up, so urllib raises
    CERTIFICATE_VERIFY_FAILED against api.kie.ai. curl uses the system trust
    store and is already the working path for the uploads below.
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
             "-F", "uploadPath=delphine-vestirsi-statics",
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


def build_prompt(name, cw, scene):
    cast = CAST.get(name, "")
    people = "" if name == "D1-new-arrival" else f"{MODEL} {cast} {GRIP} "
    return (
        f"{scene} {people}"
        f"The handbag in the frame: {identity(cw)} {SCALE} {construction(cw)} {DETAILS} {match(cw)} "
        f"{STYLE} {ANTI_CGI}"
    )


ATTEMPTS = 3   # GPT Image 2's content filter refuses intermittently on identical input


def submit(name, ref_urls, cw, scene):
    payload = {"model": "gpt-image-2-image-to-image",
               "input": {"prompt": build_prompt(name, cw, scene),
                         "input_urls": ref_urls,
                         "aspect_ratio": ASPECT.get(name, "9:16"),
                         "resolution": "2K"}}
    d = api(f"{API}/jobs/createTask", payload, H)
    if d.get("code") != 200:
        payload["input"]["resolution"] = "1K"
        d = api(f"{API}/jobs/createTask", payload, H)
    assert d.get("code") == 200, f"{name} createTask failed: {d}"
    return d["data"]["taskId"]


def main():
    os.makedirs(OUT, exist_ok=True)
    todo = [v for v in VARIATIONS if not os.path.exists(os.path.join(OUT, f"{v[0]}.png"))]
    for name, *_ in VARIATIONS:
        if not any(t[0] == name for t in todo):
            print(f"{name}: exists, skip", flush=True)
    if not todo:
        print("all plates present", flush=True)
        return

    cache = {}
    for _, refs, _, _ in todo:
        for r in refs:
            if r not in cache:
                cache[r] = upload(os.path.join(REF_DIR, r))

    spec = {name: (refs, cw, scene) for name, refs, cw, scene in todo}
    tries = {name: 0 for name in spec}

    pending = {}
    for name, (refs, cw, scene) in spec.items():
        tries[name] += 1
        pending[name] = submit(name, [cache[r] for r in refs], cw, scene)
        print(f"{name}: task {pending[name]} (attempt {tries[name]})", flush=True)

    deadline = time.time() + 2700
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
                refs, cw, scene = spec[name]
                if tries[name] < ATTEMPTS:
                    tries[name] += 1
                    pending[name] = submit(name, [cache[r] for r in refs], cw, scene)
                    print(f"{name}: retry task {pending[name]} (attempt {tries[name]})", flush=True)
                else:
                    print(f"{name}: GIVING UP after {ATTEMPTS} attempts", flush=True)
    if pending:
        print(f"TIMEOUT still pending: {list(pending)}", flush=True)
    done = [v[0] for v in VARIATIONS if os.path.exists(os.path.join(OUT, f"{v[0]}.png"))]
    print(f"complete: {len(done)}/{len(VARIATIONS)} -> {sorted(done)}", flush=True)


if __name__ == "__main__":
    main()
