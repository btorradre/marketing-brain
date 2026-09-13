#!/usr/bin/env python3
"""VERIFIED BUYER — 6 on-model MOF plates via kie.ai GPT Image 2 i2i.

Replicates the Vestirsi review-quote static (woman + bag, full-bleed 9:16, quote
overlaid in the lower third) for the Velantra Straw Tote, one plate per colorway.

Vibe is DELIBERATELY NOT the reference: the Vestirsi ad is a cold NYC studio,
25-year-old editorial model, wool coat, aloof stare. Ours is the Velantra ICP's
dream outcome — a woman in her early forties on a warm coastal morning, linen,
soft daylight, at ease. Same layout, opposite temperature.

Plates render CLEAN (no text). Quote block is composited in overlay.py so the
typography is pixel-correct.

Each colorway is anchored on its own live PDP "Hand-held front" hero so the
leather color is exact. Verbatim identity + flap mechanism blocks in every prompt.
Idempotent: skips colorways whose plate PNG already exists (delete to regen).
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

# --- LOCKED PRODUCT TRUTH (velantra-straw-tote skill, verbatim; leather color resolved) ---


def identity(leather):
    return (
        f"a structured hand woven straw tote in warm natural sandy tan straw, tightly woven straw body with "
        f"braided cross stitch trim along the edges, a smooth {leather} flap folded over the top of the "
        f"bag from the back: the flap is ONE single seamless piece of leather, its front lower edge cut "
        f"into the silhouette of a wide center panel with 2 squared outer tabs, the leather fully "
        f"continuous and unbroken between and above these shapes, with exactly 2 narrow slots through "
        f"which the handles pass, two rolled {leather} top handles, two {leather} belt straps crossed on "
        f"the front, white contrast stitching on all leather edges, no metal hardware, no logos. The "
        f"leather flap, tabs and belt straps exist ONLY on the FRONT face of the bag, the back face is "
        f"plain woven straw, no duplicated front detailing on any other face."
    )


def flap(leather):
    return (
        f"Flap and opening construction: the {leather} flap is ONE single seamless sheet of leather "
        f"attached along the top rear edge of the tote and folded all the way forward over the front, "
        f"lying completely flat. Its front lower edge is cut into the shape of a wide center panel and 2 "
        f"squared outer tabs, but these are shapes cut into the SAME single sheet, never separate pieces. "
        f"The leather is continuous and unbroken between the shapes and across the entire top of the bag, "
        f"including between the two handle slots. The only openings anywhere in the flap are the 2 narrow "
        f"handle slots. No gap, no seam, no split, no opening exists anywhere else in the flap, and "
        f"nothing behind or inside the bag is ever visible through the flap. The flap never splits into "
        f"pieces, never lifts, never stands up, always folded all the way over. The 2 {leather} belt "
        f"straps lie crossed in an X over the front below the flap with rounded ends and white contrast "
        f"stitching, exactly as on the closed reference bag, never threaded through the flap and never "
        f"wrapped around the contents. No metal hardware anywhere on the bag."
    )


# --- LOCKED CASTING (the Velantra ICP, not the reference's model) ---
#
# Every ad in the set carries a DIFFERENT named reviewer, so every ad must show a
# visibly different woman. One face across six named buyers collapses the review
# device the moment two of them serve to the same person. CAST below is per colorway;
# MODEL holds only what they share.
#
# No necklaces anywhere: fine chains rendered as mangled gold smears on two plates in
# an earlier round. Small earrings only.

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

# --- LOCKED FRAME (Vestirsi skeleton: full bleed 9:16, bag at chest height, clean lower third) ---

FRAME = (
    "Vertical 9 by 16 full frame photograph of the woman standing, shot from just below her eye level, "
    "framed wide from a little above the top of her head all the way down past her knees, so there is a "
    "long clean run of her clothing below the bag. Her head sits in the top eighth of the frame. "
    "CRITICAL FRAMING RULE: the tote is carried high, at chest height, and the whole bag including its "
    "lowest corner must sit inside the UPPER HALF of the frame, no lower than halfway down. The bag is "
    "large and clearly readable and is never cropped by any frame edge. "
    "CRITICAL EMPTY SPACE RULE: the entire bottom two fifths of the frame shows only the smooth pale "
    "fabric of her clothing and the softly out of focus pale ground or wall behind it. The bag and both "
    "of her hands stay entirely above that area. It is a calm, even, light toned expanse with no "
    "pattern, no clutter, no dark objects and no strong detail, because dark text will be placed there "
    "afterwards and must stay easy to read."
)

# Three carry failure modes on this concept, all from a vague hand/handle relationship:
# an "inert" hand resting flat on the flap while the handles stand untouched; a fist
# closed on empty air with the handle apex below the fingertips; and — the one that took
# longest to see — a TWO-HAND grip up at the arc's apex, where both fists occlude exactly
# the span the arc has to cross, so the generator renders two severed risers and a
# floating leather fragment pinched between the fingertips.
#
# The fix is a ONE-HAND grip LOW on the handle legs, which leaves both complete arches
# above the hand, unoccluded and verifiable. Phrase every requirement positively: naming
# a hand failure mode, even clinically, trips the content filter.
GRIP = (
    "How she holds it, this matters and must be exactly right: each of the two rolled leather top "
    "handles is one single continuous unbroken loop that rises out of its slot in the flap, arches up, "
    "and comes back down into the bag, and the complete arch of both handles stays fully visible along "
    "its whole length. The two handles are the SAME size and shape as each other, the same width apart "
    "at their bases and the same height, one directly behind the other, so the rear handle reads as an "
    "identical twin of the front one and never as a smaller thin loop nested inside it. She carries the "
    "bag with ONE hand only. That hand is hooked LOW around both "
    "handle legs, down close to where they enter the top of the bag, so the whole arch of each handle "
    "rises freely above her hand in clear open view. Her fingers curl around the leather so the legs "
    "show both above and below her fingers, and the weight of the bag hangs from that hooked hand. Her "
    "other hand stays well away from the bag. Her forearm stays clearly in front of the bag or beside "
    "it, in front of the leather flap."
)

MATCH = (
    "The tote is the exact bag shown in the first reference image, matching its construction, "
    "proportions, weave pattern, straw color and leather color exactly. The woven straw body is warm "
    "natural sandy tan, only the leather flap, handles, trim and belt straps are colored."
)

STYLE = (
    "Photorealistic editorial lifestyle fashion photograph, shot on a full frame camera with an 85mm "
    "lens at f2.8, natural available light, gentle warm summer color grade, soft film grain, real skin "
    "texture, shallow depth of field with the background softly out of focus. Absolutely no text, no "
    "words, no letters, no captions, no watermarks and no logos anywhere in the image. The tote is "
    "closed and empty, nothing inside it and nothing leaning out of it. Only one person in the frame."
)

# colorway -> (ref file, leather wording, casting, wardrobe + setting + pose)
CAST = {
    # Recast: the first casting here ("sun lightened light brown hair, green hazel eyes,
    # fair freckled skin") rendered as the same woman as lightning-orange's auburn/green
    # hazel/freckled casting — hair colour alone is not a casting. Moved into the
    # blonde/blue lane that opened up when caban-black became a Black casting.
    "caramel":
        "She has light golden blonde hair pulled back into a loose low ponytail, clear blue eyes and "
        "fair lightly sun flushed skin. Small thin gold hoop earrings.",
    "light-chocolate":
        "She has dark brown hair gathered into a low loose twist at her neck with several strands "
        "escaping around her face, deep brown eyes, warm olive tan skin, strong straight brows and a "
        "square jaw. Small flat gold stud earrings.",
    # Recast: the first casting here ("warm blonde bob, clear blue eyes, fair skin") landed
    # on the same woman as caramel, whose light-brown-and-hazel casting drifted blonde.
    # Two variations of blonde-with-pale-eyes is not two women. This slot now contrasts on
    # hair colour AND texture AND eye colour AND skin tone at once.
    "caban-black":
        "She is a Black woman with dark brown hair in a short natural curly crop, warm deep brown "
        "skin, dark brown eyes, high cheekbones and a wide warm smile. Small gold hoop earrings.",
    "cream":
        "She has long straight black hair pushed behind one ear, dark brown eyes, deep warm brown "
        "skin with a natural sheen, full cheeks and a softly rounded face. Small gold ball earrings.",
    # Reworded twice: "pale skin with freckles across her nose and forearms" and then
    # "a fair freckled complexion" were both refused by the content filter 3/3 times
    # alongside a sleeveless dress. Light on skin description, dress given sleeves.
    "lightning-orange":
        "She has wavy auburn red hair falling past her shoulders, grey green eyes, light freckling and "
        "laugh lines around a wide easy smile. Small thin gold hoop earrings.",
    "sky-blue":
        "She has dark hair cut to the jaw with natural silver coming in at her temples, dark brown "
        "eyes, light olive skin with visible fine lines, and a calm even featured face. Small gold "
        "stud earrings.",
}

COLORWAYS = [
    (
        "caramel", "caramel.png", "warm caramel tan leather",
        "She is standing in front of a sunlit whitewashed clapboard wall on a warm mid morning, the pale "
        "boards softly out of focus behind her and filling the whole background. She wears a relaxed "
        "white linen shirt dress with the sleeves rolled to the elbow and the collar open. She holds the "
        "tote in her right hand at chest height, her fingers hooked low around both handle legs just "
        "above the top of the bag, her right elbow bent and her left arm relaxed at her side. She is "
        "turned slightly to her left and looking just past the camera with a small easy smile, as if "
        "someone she likes just said her name.",
    ),
    (
        "light-chocolate", "light-chocolate.png", "medium chocolate brown leather",
        "She is standing beside a whitewashed stone garden wall in warm late morning light, the pale wall "
        "and a soft blurred green hedge behind her. She wears wide leg ecru linen trousers and a fine "
        "cream knit sleeveless top, with a soft camel cardigan draped over one shoulder. She carries the "
        "tote by both top handles lifted up in front of her chest, both hands on the handles, forearms "
        "raised. She is looking slightly off camera, calm and unhurried.",
    ),
    (
        "caban-black", "caban-black.jpg", "black leather",
        "She is standing in front of a sunlit white clapboard wall with warm light bouncing back onto "
        "her face, the pale painted boards softly out of focus and filling the entire background evenly, "
        "with no doorway, no window and no dark opening anywhere in the frame. She wears a crisp white "
        "poplin shirt tucked into pale sand colored linen trousers. She holds the tote in her right hand "
        "at chest height, her fingers hooked low around both handle legs just above the top of the bag, "
        "her right elbow bent and her left arm relaxed at her side. She is turned three quarters toward "
        "the camera and looking straight into it, calm, warm and self assured, with an easy smile.",
    ),
    (
        "cream", "cream.png", "soft ivory cream leather",
        "She is standing in warm morning light in front of a smooth pale sandstone wall, the wall softly "
        "out of focus and filling the background. She wears a pale blue chambray shirt with both sleeves "
        "rolled to the elbow, loosely tucked into a long white linen skirt, and both of her arms are "
        "fully visible and end in clearly rendered hands. She holds the tote in her left hand at chest "
        "height, her fingers hooked low around both handle legs just above the top of the bag, her left "
        "elbow bent and her right arm relaxed at her side. The bag hangs from her hand at chest height "
        "and never rests on her shoulder, and the handles stay short, rising only a little way above the "
        "bag. She is turned three quarters toward the camera, mid laugh, entirely natural.",
    ),
    (
        "lightning-orange", "lightning-orange.png", "bright vermillion orange leather",
        "She is standing against a warm limewashed pale plaster wall in soft late afternoon sunlight, the "
        "wall filling the background in a smooth warm cream tone. She wears a simple ivory linen dress "
        "with short sleeves and a high round neckline, falling straight and clean to below the knee. She "
        "holds the tote in her right hand at chest height, her fingers hooked low around both handle "
        "legs just above the top of the bag, her right elbow bent and her left arm relaxed at her side. "
        "Her head is tilted very slightly and she is looking into the camera with a warm open "
        "expression, sunlight catching one side of her face.",
    ),
    (
        "sky-blue", "sky-blue.png", "bright azure sky blue leather",
        "She is standing beside a pale whitewashed harbor wall in bright warm morning light, the wall and "
        "a soft blurred pale sky filling the background. She wears an ecru linen tank and wide leg white "
        "linen trousers, with a light cream sweater tied loosely over her shoulders. She holds the tote "
        "up at chest height in her right hand, her fingers curled fully around both top handles with the "
        "handles running through her closed hand, her right elbow bent and her left hand tucked casually "
        "into her trouser pocket. She is looking slightly off camera out toward the water, relaxed and "
        "thoughtful, hair moving a little in the breeze.",
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
             "-F", "uploadPath=verified-buyer-mof",
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


def build_prompt(name, leather, scene):
    return (
        f"{scene} {MODEL} {CAST[name]} {FRAME} {GRIP} The bag she is carrying: {identity(leather)} "
        f"{flap(leather)} {MATCH} {STYLE}"
    )


ATTEMPTS = 3  # GPT Image 2's content filter refuses intermittently on identical input


def submit(name, ref_url, leather, scene):
    payload = {"model": "gpt-image-2-image-to-image",
               "input": {"prompt": build_prompt(name, leather, scene),
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
    todo = [c for c in COLORWAYS if not os.path.exists(os.path.join(OUT, f"{c[0]}.png"))]
    for name, *_ in COLORWAYS:
        if not any(t[0] == name for t in todo):
            print(f"{name}: exists, skip", flush=True)
    if not todo:
        print("all plates present", flush=True)
        return

    refs = {name: upload(os.path.join(REF_DIR, ref)) for name, ref, _, _ in todo}
    spec = {name: (leather, scene) for name, _, leather, scene in todo}
    tries = {name: 0 for name in spec}

    pending = {}
    for name in spec:
        tries[name] += 1
        pending[name] = submit(name, refs[name], *spec[name])
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
                if tries[name] < ATTEMPTS:
                    tries[name] += 1
                    pending[name] = submit(name, refs[name], *spec[name])
                    print(f"{name}: retry task {pending[name]} (attempt {tries[name]})", flush=True)
                else:
                    print(f"{name}: GIVING UP after {ATTEMPTS} attempts", flush=True)
    if pending:
        print(f"TIMEOUT still pending: {list(pending)}", flush=True)
    done = [c[0] for c in COLORWAYS if os.path.exists(os.path.join(OUT, f"{c[0]}.png"))]
    print(f"complete: {len(done)}/{len(COLORWAYS)} -> {sorted(done)}", flush=True)


if __name__ == "__main__":
    main()
