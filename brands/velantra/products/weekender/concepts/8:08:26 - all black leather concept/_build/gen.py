#!/usr/bin/env python3
"""VEL-WEEKENDER-NOIR concept: all-black, all-leather, no canvas.
kie GPT Image 2 i2i off the real physical-bag stills. 3 variants per shot, sequential + retry.
"""
import json, os, subprocess, time, urllib.request, pathlib

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT.parent / "renders"
OUT.mkdir(exist_ok=True)
VAULT = "/Users/brooksorradre2/Documents/marketing brain"
REFS = pathlib.Path(VAULT) / "brands/velantra/products/weekender/product-references/real-product-2026-08-08"

KEY = None
for line in open(os.path.join(VAULT, ".env")):
    if line.startswith("KIE_API_KEY="):
        KEY = line.split("=", 1)[1].strip()
assert KEY

KIE_API = "https://api.kie.ai/api/v1"
KIE_UPLOAD = "https://kieai.redpandaai.co/api/file-stream-upload"

# ---------------------------------------------------------------- blocks

IDENTITY = (
    "The bag is a structured all black weekend bag, wider than tall, made entirely of smooth black leather. "
    "It has the identical silhouette, proportions, panel construction, seam lines, stitching and hardware as the "
    "reference bag, with one single change: every exterior surface that is woven canvas on the reference bag is "
    "instead smooth black leather on this bag, and every leather section is that same black leather, so the whole "
    "exterior is one continuous black leather in a single tone. The two tone split of the reference bag survives "
    "only as a stitched seam line and a faint change in grain direction across that seam, never as a change in "
    "colour or material. Two rolled black leather top handles, a small gold oval turn lock at the front centre, "
    "two short black leather belt straps lying flat and horizontal high on the leather upper band beside the flap, "
    "each ending in a flat gold clasp plate hooked over a gold staple, a small black leather key bell tied to the handle "
    "base, black leather corner patches at the bottom, a small gold eyelet high on each side face, tonal black "
    "topstitching, warm brass gold hardware throughout, no logos or lettering anywhere on the bag, and a smooth "
    "caramel tan leather interior lining with a wide matching caramel slip pocket on the interior wall. "
    "CRITICAL MATERIAL RULE: there is NO canvas, NO woven fabric, NO twill, NO cream, NO ivory, NO beige, NO "
    "basketweave and NO pin dot texture anywhere on this bag. The leather is a deep true black with real grain, "
    "soft natural creasing where it folds and a low semi matte sheen, never patent, never glossy, never uniform."
)

HARDWARE = (
    "Front closure hardware, exactly as on the reference photo: at the front centre of the leather band stands a "
    "small gold turn post with a round knurled mushroom shaped head. The flap's centre tab carries a polished gold "
    "oval plate with a shaped keyhole cutout in its middle, and when the flap is down this tab rests over the post "
    "so the gold post head shows through the cutout. To the left and right, two flat vertical gold staples stand on "
    "the leather band, and when the flap is down its two small oval slots sit over these staples so the staples poke "
    "through. There are two short black leather belt straps, one to the left of the flap and one to the right, and "
    "each one lies FLAT and HORIZONTAL against the wide leather upper band, level with the bottom edge of the flap, "
    "high on the bag. Each strap tip carries a flat gold rounded rectangular end plate with an oblong slot and small "
    "dome rivets, and that plate hooks over the gold staple beside it. STRAP GEOMETRY IS CRITICAL: each strap and "
    "its gold end plate sit entirely within the upper leather band, close beside the flap, in the top third of the "
    "bag. The straps are short. They never run diagonally, never run downward across the front of the bag body, "
    "never reach the middle or the lower half of the bag, and the gold plates are never mounted low on the body or "
    "near the bottom corners. The handles pass through keyhole "
    "shaped cutouts in the flap with stitched edges. All hardware is the same warm brass gold, both sides identical, "
    "no silver, no chrome, no white metal."
)

MECHANISM = (
    "Open bag construction: the open bag keeps the exact same panel split as the closed reference bag. The entire "
    "upper section of the bag body, across the front, the back and both sides, is smooth black leather, exactly as "
    "deep as the leather upper section on the closed reference bag, and everything below it is that same smooth "
    "black leather, so the split reads only as a stitched seam. Folding the flap back does NOT change this "
    "construction: the seam where the upper section ends sits in exactly the same place as on the reference bag. "
    "The two rolled black leather top handles are anchored directly into this wide leather upper band with sturdy "
    "leather bases, never into a thin trim. Two thin gold posts stand upright on the band and the small gold oval "
    "turn lock is mounted on the band at the top centre of the front. The two short black leather belt straps lie flat "
    "and horizontal on this band, one to each side, unhooked, each ending in its flat gold clasp plate, and they "
    "never run down the front of the bag body. The wide band on the front is plain smooth leather "
    "and is part of the bag body: no tab sections, no scalloped edges, no pocket shape, no turn lock pocket, it is "
    "not a flap. The entire black leather flap, one single piece, is folded backward over the top rear edge of the "
    "bag and leans back behind the open mouth, clearly visible from the front: the inside face of the flap stands "
    "behind the opening showing its two keyhole shaped handle cutouts, its two small oval strap slots and its small "
    "gold oval plate with a shaped keyhole cutout, with the rear rolled handle rising above it. The flap never "
    "covers the front of the bag and never splits into pieces. BOTH handles are clearly visible standing upright: "
    "the front handle rises from the front leather band, the rear handle rises from the back band in front of the "
    "folded back flap, never omit the front handle. The mouth of the bag is a clean open oval at the top, showing "
    "the smooth caramel tan leather interior lining and the wide matching caramel slip pocket on the interior wall. "
    "The bag has NO zipper anywhere, no zipper track, no zipper teeth, no zipper pull, and no embossed text or "
    "lettering anywhere on the bag."
)

SCALE = (
    "SCALE IS CRITICAL. This is a LARGE TRAVEL BAG, 18 inches wide by 14.5 inches tall by 7 inches deep, big enough "
    "to pack two to three days of clothes. It is NOT a handbag, NOT a purse, NOT a medium tote. Roughly the size of "
    "a carry-on duffel. Render it noticeably oversized rather than too small. "
)

PREAMBLE = (
    "Use the attached photos ONLY as the reference for the bag's shape, proportions, construction, stitching and "
    "hardware. Do NOT copy their lighting, their background, their framing or their look. Create a new photograph. "
)


def footer(ratio):
    v = "Vertical 9:16." if ratio == "9:16" else "Square 1:1."
    return (
        " CRITICAL RENDERING INSTRUCTION. This is a real photograph casually taken on an iPhone 15 Pro by an "
        "ordinary person, handheld, in one second, with no lighting equipment, no tripod and no styling. It is NOT "
        "a 3D render, NOT CGI, NOT a product visualisation, NOT Blender or Octane or Unreal or Keyshot, NOT ray "
        "traced, NOT a commercial or catalogue product photograph, NOT an advertisement, NOT retouched, NOT "
        "airbrushed, NOT studio lit. If it looks polished or computer generated it is wrong. Photographic evidence "
        "that must be present: visible digital sensor noise and grain through the shadows and midtones, highlights "
        "slightly blown out where the light source hits, mild chromatic aberration on high contrast edges, faint "
        "JPEG compression artefacts, focus that is slightly imperfect so nothing is tack sharp, a trace of handheld "
        "motion blur, and framing that is a little crooked and off centre the way a real snapshot is. Real light "
        "only: one dominant available light source, mixed colour temperature across the frame, uneven exposure, and "
        "real shadows falling off naturally with visible ambient bounce. Real surfaces: the black leather is "
        "creased, faintly scuffed, unevenly grained and dulled where it has been handled, catching light in uneven "
        "patches and never a uniform polished finish, with ordinary dust, lint and fingerprints present. The setting "
        "is a real lived-in place with ordinary clutter, not a set. No on-screen text, lettering, signage or "
        "graphics anywhere. " + v
    )


HARDEN = (
    " The bag in frame is an exact copy of the reference bag in silhouette, proportions, construction and hardware, "
    "changed only in colour and material to all black leather. The two rolled top handles are smooth simple leather "
    "tubes with no wrapping, no braiding and no woven texture. BOTH clasp plates are the SAME warm brass gold, the "
    "right plate identical in colour to the left plate. Both belt straps are SHORT and lie flat and horizontal "
    "high on the leather upper band beside the flap, never running down the front of the bag body."
)

# ---------------------------------------------------------------- shots

CLOSED = str(REFS / "LC-closed-front-unfastened.jpg")
SIDE = str(REFS / "LC-closed-side-strap-detail.jpg")
MACRO = str(REFS / "LC-macro-turnlock-flap.jpg")
OPEN_A = str(REFS / "LC-open-flap-inner-face-interior.jpg")
OPEN_B = str(REFS / "LC-open-interior-slip-pocket.jpg")
SCALE_REF = str(REFS / "LC-hand-scale-front.jpg")

JOBS = [
    {
        "name": "01-hero-front-closed",
        "refs": [CLOSED],
        "ratio": "1:1",
        "scene": (
            "Create a straight-on front photograph of the all black bag standing upright on a pale oak wood floor "
            "beside a doorway in a real apartment, late afternoon daylight raking in from a window on the left. "
            "The flap is down over the front but unfastened: the gold oval plate rests over the gold turn post, the "
            "two gold staples are exposed, and the two short black leather belt straps lie flat and horizontal on the "
            "leather upper band beside the flap with their gold end plates hooked over those staples. The bag fills most of the frame. "
        ),
        "extra": [HARDWARE],
    },
    {
        "name": "02-three-quarter",
        "refs": [CLOSED, SIDE],
        "ratio": "1:1",
        "scene": (
            "Create a three quarter angle photograph of the all black bag sitting on an unmade linen bed in a real "
            "bedroom, soft window light from behind and to the right. The angle shows the front face and one full "
            "side face, so the deep seven inch gusset is clearly readable and the bag looks long and roomy. The "
            "small gold eyelet high on the side face near the gusset edge is visible, and the short black leather belt "
            "strap on that side lies flat and horizontal high on the leather band with its gold end plate. "
        ),
        "extra": [HARDWARE],
    },
    {
        "name": "03-hardware-macro",
        "refs": [MACRO, CLOSED],
        "ratio": "1:1",
        "scene": (
            "Create a tight macro photograph of the front closure hardware on the all black bag, shot close and "
            "slightly from above with a shallow depth of field so the gold catches a hard specular highlight "
            "against the black leather. The black leather grain, the pores, the tonal black topstitching and the "
            "dark edge paint fill the frame around the hardware. "
        ),
        "extra": [HARDWARE],
    },
    {
        "name": "04-open-interior",
        "refs": [OPEN_A, OPEN_B],
        "ratio": "1:1",
        "scene": (
            "Create a photograph of the all black bag standing open on a hotel luggage bench, shot from the front "
            "and slightly above so the open mouth and the caramel tan leather interior are clearly visible. The "
            "warm caramel interior glows against the black exterior. A folded knit sweater and a rolled pair of "
            "jeans sit inside. "
        ),
        "extra": [MECHANISM],
    },
    {
        "name": "05-carry-scale",
        "refs": [CLOSED, SCALE_REF],
        "ratio": "9:16",
        "scene": (
            "Create a candid photograph of a woman in her early thirties in a black wool coat and jeans standing in "
            "an apartment hallway, holding the all black bag by both rolled top handles in one hand at her side. "
            "Her face is partly out of frame at the top. The bag is carried by the hand only, never on the "
            "shoulder, and there is no shoulder strap of any kind anywhere on the bag. The bag reaches from her "
            "hip toward her knee and is almost as wide as her shoulder span, reading unmistakably as a large "
            "travel bag rather than a handbag. The flap is down, with the two short belt straps lying flat and horizontal high on the leather band. "
        ),
        "extra": [],
    },
]

# ---------------------------------------------------------------- runner


def api(path, payload=None):
    req = urllib.request.Request(
        KIE_API + "/" + path,
        headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json"},
    )
    if payload is not None:
        req.data = json.dumps(payload).encode()
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.loads(r.read().decode(), strict=False)


state_path = OUT / "_state.json"
state = json.loads(state_path.read_text()) if state_path.exists() else {"uploads": {}, "tasks": {}}


def save():
    state_path.write_text(json.dumps(state, indent=1))


def upload(path):
    if path in state["uploads"]:
        return state["uploads"][path]
    for attempt in range(4):
        out = subprocess.run(
            ["curl", "-s", "-X", "POST", KIE_UPLOAD,
             "-H", "Authorization: Bearer " + KEY,
             "-F", "file=@" + path,
             "-F", "uploadPath=images/velantra-weekender-noir",
             "-F", "fileName=%d-%s" % (int(time.time()), os.path.basename(path).replace(" ", "_"))],
            capture_output=True, text=True)
        try:
            resp = json.loads(out.stdout)
        except ValueError:
            time.sleep(5)
            continue
        url = resp.get("data", {}).get("downloadUrl")
        if url:
            state["uploads"][path] = url
            save()
            print("[upload] %s" % os.path.basename(path), flush=True)
            return url
        time.sleep(5)
    raise SystemExit("upload failed: " + path)


def build_prompt(job):
    parts = [PREAMBLE, job["scene"], SCALE, IDENTITY]
    parts += job["extra"]
    parts.append(HARDEN)
    parts.append(footer(job["ratio"]))
    return " ".join(p.strip() for p in parts)


def create(key, prompt, urls, ratio):
    if key in state["tasks"]:
        return state["tasks"][key]
    for attempt in range(6):
        try:
            r = api("jobs/createTask", {"model": "gpt-image-2-image-to-image", "input": {
                "prompt": prompt, "input_urls": urls,
                "aspect_ratio": ratio, "resolution": "2K"}})
            tid = r.get("data", {}).get("taskId")
            if tid:
                state["tasks"][key] = tid
                save()
                print("[%s] task %s" % (key, tid), flush=True)
                return tid
            print("[%s] no taskId: %s" % (key, str(r)[:200]), flush=True)
        except Exception as e:
            print("[%s] create attempt %d: %s" % (key, attempt, e), flush=True)
        time.sleep(8)
    return None


def poll(key, tid):
    for _ in range(150):
        try:
            r = api("jobs/recordInfo?taskId=" + tid)
            st = r.get("data", {}).get("state")
            if st == "success":
                res = json.loads(r["data"]["resultJson"], strict=False)
                return res.get("resultUrls", [None])[0]
            if st == "fail":
                print("[%s] FAILED: %s" % (key, r["data"].get("failMsg")), flush=True)
                state["tasks"].pop(key, None)
                save()
                return None
        except Exception as e:
            print("[%s] poll err: %s" % (key, e), flush=True)
        time.sleep(10)
    return None


def download(key, url):
    dest = OUT / (key + ".png")
    try:
        subprocess.run(["curl", "-sf", "-A", "Mozilla/5.0", "-o", str(dest), url],
                       check=True, timeout=240)
        print("[%s] saved (%d bytes)" % (key, dest.stat().st_size), flush=True)
        return True
    except Exception as e:
        print("[%s] download failed: %s" % (key, e), flush=True)
        (OUT / (key + ".url.txt")).write_text(url)
        return False


if __name__ == "__main__":
    for job in JOBS:
        urls = [upload(p) for p in job["refs"]]
        prompt = build_prompt(job)
        (OUT / (job["name"] + ".prompt.txt")).write_text(prompt)
        for v in (1, 2, 3):
            key = "%s-v%d" % (job["name"], v)
            if (OUT / (key + ".png")).exists():
                print("[%s] exists, skip" % key, flush=True)
                continue
            tid = create(key, prompt, urls, job["ratio"])
            if not tid:
                continue
            u = poll(key, tid)
            if u:
                download(key, u)
    print("DONE", flush=True)
