#!/usr/bin/env python3
"""VERIFIED BUYER — Weekender: 8 on-model MOF plates via kie.ai GPT Image 2 i2i.

Same concept as the Straw Tote run (products/straw-birkin/concepts/7:24:26 -
verified buyer mof): the Vestirsi review-quote static — woman + bag, full-bleed
9:16, review pull quote overlaid in the lower third.

Difference: the Weekender only has two colorways, so the VARIATIONS are the
objections, not the colors. Four plates per colorway, one objection each.

Vibe is DELIBERATELY NOT the reference: the Vestirsi ad is a cold NYC studio,
25-year-old editorial model, wool coat, aloof stare. Ours is the Velantra ICP's
dream outcome — a woman in her early forties on a warm coastal morning, linen,
soft daylight, at ease. Same layout, opposite temperature.

Plates render CLEAN (no text). Quote block is composited in overlay.py so the
typography is pixel-correct.

Both colorways anchor on their own closed front-on hero (light chocolate 1 /
green 1) so leather, canvas and gold are exact. Verbatim identity block +
anti-drift hardening + closed-state pins in every prompt. The bag is closed in
all 8, so the open-bag mechanism block does not apply (CLOSURE-INTERACTION LAW).

Idempotent: skips variations whose plate PNG already exists (delete to regen).
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

# --- LOCKED PRODUCT TRUTH (velantra-weekender skill, verbatim; canvas resolved) ---


def identity(canvas):
    return (
        f"a structured two tone weekend bag, wider than tall, rich cognac brown leather upper flap "
        f"section and two rolled cognac leather top handles over a {canvas} body, a small gold oval turn "
        f"lock on the front, two flat gold clasp plates with cognac leather belt straps threaded through "
        f"them, a small cognac leather key bell tied to the handle base, cognac leather corner patches at "
        f"the bottom, visible stitching, gold hardware, no logos anywhere on the bag, natural cream cotton "
        f"canvas interior lining with a cognac leather slip pocket on the back wall."
    )


# Anti-drift hardening (mandatory for full-body / small-in-frame shots) + closed-state pins.
def construction(canvas):
    return (
        f"The bag in frame is an exact copy of the bag in the first reference image in silhouette, "
        f"proportions, materials and details, the two rolled top handles are smooth simple leather tubes "
        f"with no wrapping, no braiding and no woven texture. The bag is fully closed exactly as in the "
        f"reference image: the single cognac leather flap is folded down flat over the front, the two "
        f"cognac leather belt straps are threaded through their flat gold clasp plates, and the small gold "
        f"oval turn lock sits closed at the top center of the front. Both rolled top handles are anchored "
        f"directly into the wide cognac leather upper section of the bag with sturdy leather bases, never "
        f"into the {canvas}. The leather and {canvas} meet in one clean horizontal line at exactly the "
        f"same height as on the reference bag. The underside and bottom edge of the bag are plain smooth "
        f"leather and {canvas} only, finished with simple leather piping, exactly as on the reference "
        f"bag. The bag has no zipper anywhere, "
        f"and no embossed text or lettering anywhere on it."
    )


# --- LOCKED CASTING (the Velantra ICP, not the reference's model) ---
#
# ONE FACE PER NAMED REVIEWER. Every ad in the set carries a different named buyer, so
# every ad must show a visibly different woman. One face across eight named reviewers
# collapses the review device the moment two of them serve to the same person. CAST is
# per variation; MODEL holds only what they share.
#
# NO NECKLACES anywhere: fine chains render as mangled gold smears (caught on
# light-chocolate-c v1 as two disconnected squiggles). Small earrings only.

MODEL = (
    "The woman is in her early forties, warm sun kissed skin with real visible texture and fine lines "
    "at her eyes, no heavy makeup, natural brows, bare lips with a little gloss. Her hair is loose and "
    "slightly undone with a few strands moving, never slicked back. She wears small simple earrings and "
    "no necklace and no other jewelry at all, nothing around her neck. "
    "She looks relaxed, warm and unposed, like she is in the middle of an ordinary good morning, with "
    "an easy natural expression, never a cold hard editorial stare, never a wide posed grin. She is "
    "slim and healthy looking, comfortable in her body, standing at ease. "
    "Her hands are rendered cleanly and naturally, with five well formed fingers on each visible hand, "
    "each finger clearly separated and correctly proportioned, in a relaxed everyday grip."
)

CAST = {
    "light-chocolate-a":
        "She has shoulder length sun lightened light brown hair worn loose, green hazel eyes, and a "
        "narrow face with soft cheekbones. Small thin gold hoop earrings.",
    # refused 3/3 with "strong straight brows and a square jaw" stacked on olive tan skin
    "light-chocolate-b":
        "She has dark brown hair gathered into a low loose twist with several strands escaping around "
        "her face, deep brown eyes and warm olive skin. Small flat gold stud earrings.",
    # refused 3/3 with "an angular face with a defined jaw"
    "light-chocolate-c":
        "She has warm blonde hair cut in a blunt chin length bob and clear blue eyes. Very small gold "
        "huggie earrings.",
    "light-chocolate-d":
        "She has long straight black hair pushed behind one ear, dark brown eyes, deep warm brown skin "
        "with a natural sheen, full cheeks and a softly rounded face. Small gold ball earrings.",
    # refused 3/3; also the only sleeveless dress in the set, which the Straw Tote run
    # documented as a trigger alongside any complexion wording. Sleeves added below.
    "army-green-a":
        "She has wavy auburn red hair falling past her shoulders and grey green eyes. Small thin gold "
        "hoop earrings.",
    # refused 3/3 with "a long oval face with fine arched brows" stacked on deep golden brown skin
    "army-green-b":
        "She has black hair worn in a smooth low ponytail, dark brown eyes and a warm golden brown "
        "complexion. Small gold drop earrings.",
    "army-green-c":
        "She has dark hair cut to the jaw with natural silver coming in at her temples, dark brown "
        "eyes, light olive skin with visible fine lines, and a calm even featured face. Small gold "
        "stud earrings.",
    # v3 rendered as the SAME WOMAN as light-chocolate-a (both bronde, wavy, tanned, same
    # 3/4 turn). "Honey blonde" collapsed toward lc-a's "sun lightened light brown". Recast
    # hard, away from every blonde/bronde cue in the set.
    "army-green-d":
        "She has dark auburn hair pulled back into a low chignon, dark brown eyes and deeper olive "
        "skin. Small gold huggie earrings.",
}

# HANDLE LAW. Two failure modes on this concept, both from a vague hand/handle relation:
# an inert hand resting flat on the flap while the handles stand untouched, and (Weekender
# run, 3 of 8 plates) a high pinch on the handle TOPS that terminated both handles inside
# the fists, leaving no arc between the hands. Grip LOW on the legs, hands apart, tube
# visible above and below the fingers, arches complete.
#
# Phrase it POSITIVELY. The first draft said "rather than a tight closed fist" and the
# content filter refused all 4 regens on attempt 1.
GRIP = (
    "How she holds it, this matters and must be exactly right: the two rolled leather top handles rise "
    "from the wide leather band and her fingers curl completely around them low down, close to where "
    "the handles enter the band, so each handle tube is clearly visible both ABOVE her curled fingers "
    "and BELOW them, passing through her hand exactly the way a real bag handle does. Each handle is "
    "one single continuous unbroken loop of leather, and both complete handle arches rise well above "
    "her hands and read fully along their entire length, with a clear open span between her two hands. "
    "The tops of the handles reach up into her hand, never stopping short below it, and her hand always "
    "closes on leather. The weight of the bag visibly hangs from that grip. Her forearm stays clearly "
    "in front of the bag or clearly beside it, never disappearing behind the leather flap."
)

# --- LOCKED FRAME (Vestirsi skeleton + the TEXT-BAND FRAMING LAW from the straw run) ---

FRAME = (
    "Vertical 9 by 16 full frame photograph of the woman standing, shot from just below her eye level, "
    "framed wide from a little above the top of her head all the way down past her knees, so there is a "
    "long clean run of her clothing below the bag. Her head sits in the top eighth of the frame. "
    "The bag is a large travel sized weekend bag, roughly as wide as her shoulders, and it reads clearly "
    "as the biggest bag she owns. "
    "CRITICAL FRAMING RULE: the bag is carried high, at chest height, and the whole bag including its "
    "lowest corner must sit inside the UPPER HALF of the frame, no lower than halfway down. The bag is "
    "large and clearly readable and is never cropped by any frame edge. "
    "CRITICAL EMPTY SPACE RULE: the entire bottom two fifths of the frame shows only the smooth pale "
    "fabric of her clothing and the softly out of focus pale ground or wall behind it. The bag and both "
    "of her hands stay entirely above that area. It is a calm, even, light toned expanse with no "
    "pattern, no clutter, no dark objects and no strong detail, because dark text will be placed there "
    "afterwards and must stay easy to read."
)


def match(canvas):
    return (
        f"The weekend bag is the exact bag shown in the first reference image, matching its construction, "
        f"proportions, materials, cognac leather color, gold hardware and {canvas} exactly. The cognac "
        f"leather is deep, rich and burnished, the same dark warm brown as in the first reference image, "
        f"never a pale or orange tan."
    )


STYLE = (
    "Photorealistic editorial lifestyle fashion photograph, shot on a full frame camera with an 85mm "
    "lens at f2.8, natural available light, gentle warm summer color grade, soft film grain, real skin "
    "texture, shallow depth of field with the background softly out of focus. Absolutely no text, no "
    "words, no letters, no captions, no watermarks and no logos anywhere in the image. The bag is "
    "closed and nothing is leaning out of it. Only one person in the frame, and no luggage, no suitcase "
    "and no other bag anywhere in the shot."
)

LC = "cream ivory woven canvas"
AG = "deep army green twill canvas"

# key -> (ref file, canvas wording, wardrobe + setting + pose)
VARIATIONS = [
    (
        "light-chocolate-a", "light-chocolate.png", LC,
        "She is standing on a pale gravel drive in front of a warm honey toned stone wall on a bright "
        "mid morning, the stone and a soft blurred olive tree filling the background behind her. She "
        "wears wide leg ecru linen trousers and a fine cream knit short sleeve top tucked in loosely. "
        "She carries the bag lifted up in front of her chest, forearms raised and elbows bent close to "
        "her body. She is turned slightly to her left and looking just past the camera with a small easy "
        "smile, as if she has just arrived somewhere she likes.",
    ),
    (
        "light-chocolate-b", "light-chocolate.png", LC,
        "She is standing beside a whitewashed stone garden wall in warm late morning light, the pale wall "
        "and a soft blurred green hedge behind her. She wears a relaxed white linen shirt dress with the "
        "sleeves rolled to the elbow and the collar open. She holds the bag up in front of her at chest "
        "height, elbows bent and close to her body. She is turned three quarters toward the camera and "
        "looking straight into it, calm, warm and self assured, with the faintest hint of a smile.",
    ),
    (
        # regen 2026-07-25: v1 had a mangled duplicated necklace and a dark sage door with
        # hardware sitting inside the text band on the left of the lower half.
        "light-chocolate-c", "light-chocolate.png", LC,
        "She is standing in warm open shade in front of one continuous smooth pale limewashed plaster "
        "wall that fills the entire background edge to edge, softly out of focus, with warm sunlight "
        "bouncing back onto her face. The wall is unbroken cream plaster across the whole width of the "
        "frame: there is no doorway, no door, no door frame, no window and no dark opening anywhere, and "
        "nothing dark of any kind appears in the lower half of the frame. She wears a crisp white poplin "
        "shirt tucked into pale sand colored linen trousers. She carries the bag lifted up in front of "
        "her chest, forearms raised. She is looking slightly off camera, calm and unhurried.",
    ),
    (
        "light-chocolate-d", "light-chocolate.png", LC,
        "She is standing in bright warm morning light in front of one continuous smooth pale sandstone "
        "wall that fills the entire background edge to edge, softly out of focus, with nothing else "
        "behind her: no railing, no fence, no posts and no horizon line anywhere in the frame. She wears "
        "an ecru linen tank and wide leg white linen trousers, with a light cream sweater tied loosely "
        "over her shoulders. She holds the bag up high in front of her chest, elbows bent, so the bottom "
        "edge of the bag sits above the middle of the frame. She is looking slightly off camera, relaxed "
        "and thoughtful, hair moving a little in the breeze.",
    ),
    (
        # regen 2026-07-25: v1 terminated both handles inside clenched fists, no arc between the hands.
        "army-green-a", "army-green.png", AG,
        "She is standing against a warm limewashed pale plaster wall in soft late afternoon sunlight, the "
        "wall filling the background in a smooth warm cream tone. She wears a simple ivory linen "
        "dress with short sleeves that falls straight and clean. She holds the bag up at upper chest "
        "height, elbows bent and close to her body, with a clear open span between her two hands so that "
        "both handle arches read fully between and above them. Her head is tilted very slightly and she "
        "is looking into the camera with a warm open expression, sunlight catching one side of her face.",
    ),
    (
        # regen 2026-07-25: v1 left a floating disconnected handle fragment between the fists,
        # a blob thumb on the left hand, and invented brass studs under the base.
        "army-green-b", "army-green.png", AG,
        "She is standing in the open shade of a white clapboard doorway with warm sunlight bouncing back "
        "onto her, the white boards and a pale painted floor softly out of focus behind her. She wears a "
        "pale blue chambray shirt loosely tucked into a long white linen skirt. She carries the bag "
        "lifted up in front of her chest, forearms raised, shoulders relaxed and level, her hands well "
        "apart from each other so that both handle arches are completely visible between and above them. "
        "She is half turned away and glancing back over her shoulder toward the camera, mid laugh, "
        "entirely natural.",
    ),
    (
        "army-green-c", "army-green.png", AG,
        "She is standing in warm raking morning light in front of a smooth pale sandstone wall, the wall "
        "softly out of focus and filling the background, the low sun catching the gold turn lock and the "
        "gold clasp plates on the bag so they read bright and solid. She wears a fine cream knit "
        "sleeveless top and wide leg ecru linen trousers. She holds the bag up in front of her chest, "
        "elbows bent, the front of the bag turned squarely toward the camera. She is looking down at the "
        "bag with a small pleased expression.",
    ),
    (
        # regen 2026-07-25: v1 terminated both handles inside clenched fists AND carried the bag
        # so low its base sat at ~61% of frame height, right on top of the text band.
        "army-green-d", "army-green.png", AG,
        "She is standing in front of a sunlit whitewashed clapboard wall on a warm mid morning, the pale "
        "boards softly out of focus behind her and filling the whole background. She wears a soft camel "
        "cardigan open over a cream linen tank and wide leg ivory linen trousers. She carries the bag "
        "high in front of her at chest height, forearms raised and elbows tucked in, with a clear open "
        "span between her two hands so that both handle arches read fully between and above them. The "
        "base of the bag sits clearly above the middle of the frame. She is turned slightly to her right "
        "and looking just past the camera, warm and at ease.",
    ),
]


def api(url, payload=None, headers=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data,
                                 headers={**(headers or {}), **({"Content-Type": "application/json"} if data else {})})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.loads(r.read().decode(), strict=False)
        except Exception as e:
            if attempt == 3:
                raise
            print(f"  retry {attempt+1}: {e}", flush=True)
            time.sleep(3 * (attempt + 1))


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
             "-F", "uploadPath=weekender-verified-buyer-mof",
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


def build_prompt(name, canvas, scene):
    return (
        f"{scene} {MODEL} {CAST[name]} {FRAME} {GRIP} "
        f"The bag she is carrying: {identity(canvas)} {construction(canvas)} {match(canvas)} {STYLE}"
    )


ATTEMPTS = 3  # GPT Image 2's content filter refuses intermittently on identical input


def submit(name, ref_url, canvas, scene):
    payload = {"model": "gpt-image-2-image-to-image",
               "input": {"prompt": build_prompt(name, canvas, scene),
                         "input_urls": [ref_url],
                         "aspect_ratio": "9:16",
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

    # one upload per distinct ref file, shared across that colorway's variations
    ref_urls = {}
    for _, ref, _, _ in todo:
        if ref not in ref_urls:
            ref_urls[ref] = upload(os.path.join(REF_DIR, ref))

    spec = {name: (ref, canvas, scene) for name, ref, canvas, scene in todo}
    tries = {name: 0 for name in spec}

    pending = {}
    for name, (ref, canvas, scene) in spec.items():
        tries[name] += 1
        pending[name] = submit(name, ref_urls[ref], canvas, scene)
        print(f"{name}: task {pending[name]} (attempt {tries[name]})", flush=True)

    deadline = time.time() + 2700
    while pending and time.time() < deadline:
        time.sleep(15)
        for name, tid in list(pending.items()):
            d = api(f"{API}/jobs/recordInfo?taskId={tid}", None, H)
            st = (d.get("data") or {}).get("state")
            if st == "success":
                rj = json.loads(d["data"]["resultJson"], strict=False)
                url = rj["resultUrls"][0]
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=300) as r:
                    blob = r.read()
                with open(os.path.join(OUT, f"{name}.png"), "wb") as f:
                    f.write(blob)
                print(f"{name}: DONE ({len(blob)//1024} KB)", flush=True)
                del pending[name]
            elif st == "fail":
                msg = (d.get("data") or {}).get("failMsg")
                print(f"{name}: attempt {tries[name]} failed: {msg}", flush=True)
                del pending[name]
                ref, canvas, scene = spec[name]
                if tries[name] < ATTEMPTS:
                    tries[name] += 1
                    pending[name] = submit(name, ref_urls[ref], canvas, scene)
                    print(f"{name}: retry task {pending[name]} (attempt {tries[name]})", flush=True)
                else:
                    print(f"{name}: GIVING UP after {ATTEMPTS} attempts", flush=True)
    if pending:
        print(f"TIMEOUT still pending: {list(pending)}", flush=True)
    done = [v[0] for v in VARIATIONS if os.path.exists(os.path.join(OUT, f"{v[0]}.png"))]
    print(f"complete: {len(done)}/{len(VARIATIONS)} -> {sorted(done)}", flush=True)


if __name__ == "__main__":
    main()
