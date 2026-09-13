#!/usr/bin/env python3
"""LUN-ADV2 three-pathway advertorial — 6 native-style images via GPT Image 2 on kie.ai.

Five scenes are text-to-image. IMG-05 (the bottle) is pure i2i off the canonical
Lunessa reference. Three variants per scene per the house rule, fired sequentially
with a retry loop because kie errors on a large fraction of calls.

Usage:
  kie_images.py upload
  kie_images.py gen [IMG-01 ...]
  kie_images.py poll
  kie_images.py status
"""
import json, os, ssl, subprocess, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "images"))
STATE_PATH = os.path.join(HERE, "state.json")
VAULT = "/Users/brooksorradre2/Documents/marketing brain"
PRODUCT_REF = os.path.join(VAULT, "brands/lunessa/brand/product-references/lunessa-canonical-fixed.jpg")

API = "https://api.kie.ai/api/v1/jobs"
UPLOAD_URL = "https://kieai.redpandaai.co/api/file-stream-upload"
T2I = "gpt-image-2-text-to-image"
I2I = "gpt-image-2-image-to-image"
VARIANTS = 3
KEY = None

# ---------------------------------------------------------------- photoreal law
# SOP §3. Both blocks are mandatory on every prompt. The footer names what to
# refuse AND what photographic evidence to include; without it frames read as CGI.
FOOTER = (
    "PHOTOGRAPHIC EVIDENCE REQUIRED: visible sensor noise and luminance grain, "
    "slightly blown highlights wherever light sources fall, mild chromatic aberration "
    "on high-contrast edges, faint JPEG compression artefacts, imperfect focus with at "
    "least one element slightly soft, mildly crooked handheld framing, and a genuinely "
    "lived-in setting with real clutter, dust, crumbs, fingerprints and wear. "
    "ABSOLUTELY REFUSE: 3D render, CGI, product visualisation, Blender, Octane, Unreal, "
    "Keyshot, ray tracing, catalogue photography, studio lighting, softbox, ring light, "
    "beauty retouching, skin smoothing, HDR, colour grading, symmetrical staging, or any "
    "polished commercial look. This must read as an unremarkable snapshot taken by an "
    "ordinary 58-year-old woman on an aging phone, not as a photograph anyone was paid to make."
)

I2I_PREAMBLE = (
    "The attached image supplies the bottle's GEOMETRY, LABEL ARTWORK, TYPOGRAPHY and "
    "MATERIALS ONLY. Do not inherit anything else from it. Reject its grey seamless "
    "background, its clean cut-out edges, its even studio lighting and its polished "
    "product-photograph look entirely. Rebuild the exact same bottle into the real-world "
    "scene described below, lit only by the available light in that room. "
    "PRESERVE EXACTLY: bottle silhouette and proportions, white cap, deep red label, the "
    "wordmark 'Lunessa', the headline 'RED YEAST RICE + COQ10', 'SUGAR FREE', "
    "'RASPBERRY FLAVOR', '60 VEGAN GUMMIES | DIETARY SUPPLEMENT', and the red gummies "
    "visible through the clear plastic above and below the label. Do not re-interpret, "
    "re-letter or re-arrange the label. "
)

SCENES = {
    "IMG-01": dict(model=T2I, prompt=(
        "An overhead phone snapshot of a worn kitchen counter in an ordinary Midwestern house, "
        "framed slightly off-centre and a little crooked. On the counter: a plastic seven-day "
        "pill organiser with several lids flipped open, a generic amber prescription bottle with "
        "a plain white pharmacy label, a half-drunk mug of coffee gone cold with a ring under it, "
        "and a folded lab results printout with rows of numbers. Cheap laminate countertop with "
        "a few scratches and crumbs. Flat grey-yellow morning light coming through a window on "
        "the left, no other light source. Nothing has been tidied or arranged for the photo. "
        + FOOTER)),

    "IMG-02": dict(model=T2I, prompt=(
        "A blurry phone photo taken by a patient lying on her back on an exam table during a "
        "neck ultrasound, shot one-handed at an awkward upward angle. The ultrasound monitor is "
        "partly visible at the top of the frame, out of focus, showing a grainy grey-and-black "
        "scan image. A sonographer's forearm and blue-gloved hand enter from the right edge, "
        "holding a probe. Dim clinical room, the only real light is the cold blue glow of the "
        "screen and a dull overhead fluorescent. Motion blur from the awkward hold. Cropped "
        "badly, part of the ceiling tile in frame. "
        + FOOTER)),

    "IMG-03": dict(model=T2I, prompt=(
        "A phone snapshot looking down at a kitchen table from where someone has been sitting, "
        "taken minutes after a bad phone call. On the table: a printed clinic after-visit summary "
        "with dense small text and a highlighted line, a smartphone lying face down, one crumpled "
        "tissue, a pair of reading glasses folded askew, and a mug of coffee left untouched and "
        "cold. An older wooden table with visible water rings and scratches. Overcast daylight "
        "from a window behind, dull and flat, no lamps on. The frame is tilted and one corner "
        "falls into shadow. Nobody is in the shot. "
        + FOOTER)),

    "IMG-04": dict(model=T2I, prompt=(
        "A close phone photo of an open spiral notebook lying on a kitchen table, shot from a "
        "seated height at an angle so the page is not square to the camera and the left edge is "
        "darker. On the lined page, written in ordinary blue ballpoint cursive-print handwriting "
        "by an older woman, three numbered lines exactly: "
        "'1. Making it' then '2. Clearing it' then '3. Oxidizing'. "
        "The first line, '1. Making it', is circled by hand in the same blue pen, and the single "
        "word 'statin' is written beside that circle with a short arrow pointing to it. "
        "The handwriting is slightly uneven and the ink is heavier where the pen pressed. "
        "A ballpoint pen rests on the page. Warm dim indoor evening light from a single overhead "
        "kitchen fixture, one soft shadow from the notebook's spine. Slight motion blur. "
        + FOOTER)),

    "IMG-05": dict(model=I2I, refs=[PRODUCT_REF], prompt=(
        I2I_PREAMBLE +
        "SCENE: the bottle stands on a worn laminate kitchen counter beside a used ceramic coffee "
        "mug with a faint lip mark and a folded pair of reading glasses. A dish towel is bunched "
        "at the back of the frame and there are a few crumbs and a water spot on the counter. "
        "Shot casually from a standing person's chest height, off-centre and slightly crooked, so "
        "the bottle is not the perfect middle of the frame. Ordinary grey morning light through a "
        "kitchen window camera-left is the ONLY light: soft directional falloff, a real cast "
        "shadow to the right, a dull uneven reflection down the plastic rather than a clean "
        "studio highlight. The background is a real kitchen wall with an outlet and a slight "
        "grease sheen, not a seamless backdrop. "
        + FOOTER)),

    "IMG-06": dict(model=T2I, prompt=(
        "A candid phone photo taken from the passenger seat of a parked sedan, of a 58-year-old "
        "white American woman sitting in the driver's seat. Short greying layered hair, a soft "
        "lined face with real pores, sun damage on her cheeks and forearms, no makeup, reading "
        "glasses pushed up on her head, a plain zip fleece. She is holding her phone loosely in "
        "her lap and looking out through the windshield, not at the camera, not smiling, her jaw "
        "loose with relief. Ordinary flat daylight, harsh glare and dust across the windshield, "
        "a mundane medical-office parking lot visible outside. Framing is loose and a little "
        "tilted, the seatbelt buckle and a coffee cup in the console are in shot. "
        + FOOTER)),
}


def ctx():
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


def load_key():
    global KEY
    for line in open(os.path.join(VAULT, ".env")):
        if line.startswith("KIE_API_KEY="):
            KEY = line.strip().split("=", 1)[1]
    assert KEY, "KIE_API_KEY not found"


def credits():
    req = urllib.request.Request("https://api.kie.ai/api/v1/chat/credit",
                                 headers={"Authorization": f"Bearer {KEY}"})
    with urllib.request.urlopen(req, context=ctx(), timeout=60) as r:
        return json.loads(r.read().decode(), strict=False).get("data")


def state():
    if os.path.exists(STATE_PATH):
        return json.load(open(STATE_PATH))
    return {"uploads": {}, "tasks": {}}


def save(st):
    json.dump(st, open(STATE_PATH, "w"), indent=1)


def api(path, payload=None):
    data = json.dumps(payload).encode() if payload else None
    req = urllib.request.Request(API + path, data=data, headers={
        "Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, context=ctx(), timeout=120) as r:
        return json.loads(r.read().decode(), strict=False)


def upload_file(path):
    for attempt in range(4):
        if attempt:
            time.sleep(8 * attempt)
        out = subprocess.run(
            ["curl", "-s", "-X", "POST", UPLOAD_URL,
             "-H", f"Authorization: Bearer {KEY}",
             "-F", f"file=@{path}",
             "-F", "uploadPath=lunessa-adv2",
             "-F", f"fileName={int(time.time())}-{os.path.basename(path).replace(' ', '_')}"],
            capture_output=True, text=True)
        try:
            resp = json.loads(out.stdout)
            url = (resp.get("data") or {}).get("downloadUrl")
            if url:
                return url
        except Exception:
            pass
        print(f"    upload retry {attempt+1}: {out.stdout[:160]}")
    raise SystemExit(f"upload failed: {path}")


def cmd_upload():
    st = state()
    print(f"uploading product reference ...")
    st["uploads"]["product"] = upload_file(PRODUCT_REF)
    save(st)
    print(f"  ok  {st['uploads']['product'][:90]}")


def cmd_gen(only):
    st = state()
    ids = only or list(SCENES)
    for sid in ids:
        sc = SCENES[sid]
        for v in range(1, VARIANTS + 1):
            slot = f"{sid}-v{v}"
            if st["tasks"].get(slot, {}).get("taskId"):
                print(f"{slot}: already queued, skip")
                continue
            payload = {"model": sc["model"], "input": {
                "prompt": sc["prompt"],
                "aspect_ratio": "3:2",
                "resolution": "2K",
            }}
            if sc.get("refs"):
                url = st["uploads"].get("product")
                assert url, "run `upload` first"
                payload["input"]["input_urls"] = [url]

            for attempt in range(6):
                try:
                    r = api("/createTask", payload)
                    tid = (r.get("data") or {}).get("taskId")
                    if tid:
                        st["tasks"][slot] = {"taskId": tid, "state": "queued"}
                        save(st)
                        print(f"{slot}: queued {tid}")
                        break
                    print(f"{slot}: attempt {attempt+1} -> {str(r)[:150]}")
                except Exception as e:
                    print(f"{slot}: attempt {attempt+1} error {e}")
                time.sleep(6 + 5 * attempt)
            else:
                print(f"{slot}: FAILED to queue after 6 attempts")
            time.sleep(3)


def cmd_poll():
    st = state()
    os.makedirs(OUT, exist_ok=True)
    pending = [s for s, t in st["tasks"].items() if t.get("state") != "done"]
    while pending:
        for slot in list(pending):
            tid = st["tasks"][slot]["taskId"]
            try:
                r = api(f"/recordInfo?taskId={tid}")
            except Exception as e:
                print(f"{slot}: poll error {e}")
                continue
            d = r.get("data") or {}
            s = d.get("state")
            if s == "success":
                urls = json.loads(d.get("resultJson") or "{}").get("resultUrls") or []
                if urls:
                    dest = os.path.join(OUT, f"LUN-ADV2-{slot}.png")
                    subprocess.run(["curl", "-s", "-A", "Mozilla/5.0", "-o", dest, urls[0]])
                    sz = os.path.getsize(dest) if os.path.exists(dest) else 0
                    st["tasks"][slot].update(state="done", file=dest)
                    print(f"{slot}: DONE  {sz//1024}kb")
                else:
                    st["tasks"][slot].update(state="done", file=None)
                    print(f"{slot}: success but no url")
                pending.remove(slot)
                save(st)
            elif s == "fail":
                st["tasks"][slot].update(state="done", file=None,
                                         err=str(d.get("failMsg"))[:200])
                print(f"{slot}: FAIL {str(d.get('failMsg'))[:120]}")
                pending.remove(slot)
                save(st)
        if pending:
            print(f"  ... {len(pending)} pending")
            time.sleep(20)


def cmd_status():
    st = state()
    for slot in sorted(st["tasks"]):
        t = st["tasks"][slot]
        print(f"{slot:14} {t.get('state'):8} {os.path.basename(t.get('file') or '-')}")
    print(f"credits: {credits()}")


if __name__ == "__main__":
    load_key()
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    args = [a for a in sys.argv[2:]]
    {"upload": lambda: cmd_upload(),
     "gen": lambda: cmd_gen(args),
     "poll": lambda: cmd_poll(),
     "status": lambda: cmd_status()}[cmd]()
