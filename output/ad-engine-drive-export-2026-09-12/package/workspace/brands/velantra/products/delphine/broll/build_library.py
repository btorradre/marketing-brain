#!/usr/bin/env python3
"""Delphine B-roll library — built on the Colette/Margot library pipeline.

    python3 build_library.py keyframes [N]   # generate stills (N variants/scene, default 2)
    python3 build_library.py animate         # Omni-animate every picked still
    python3 build_library.py poll            # download finished clips

Brooks, 2026-08-16: "Go study the Colette B-Roll Library. That is exactly how we need to build
out this B-Roll Library." This is a direct port of
`_shared/creative/broll-library-2026-08/pipeline.py` with Delphine product truth.

FOUR THINGS COPIED FROM COLETTE THAT THE FIRST DELPHINE LIBRARY GOT WRONG
------------------------------------------------------------------------
1. **resolution "1K", not 2K.** The Colette library renders at 1K. I used 2K, and the extra
   resolution buys over-resolved micro-detail that no phone camera produces. This is a real part
   of the CGI read, not a cost setting.
2. **Scenes are MOMENTS, not product shots.** Colette scenes put a person in frame with the face
   cropped out, name the wardrobe every time, and state the crop. Mine were a bag placed
   centrally in a nice setting, which is a catalogue photo no matter how it is lit.
3. **Foreground occlusion.** Colette shoots THROUGH a latte, a table edge, a dashboard. Shooting
   past something is what makes a frame read as grabbed rather than composed.
4. **Volume.** 12 shots cut into 5 ads is why they all looked the same. This file carries 58.

The FOOTER and ANTIDRIFT text below are byte-identical to the Colette library's so the house
look stays consistent across products.
"""
import json, os, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scenes_delphine import SCENES

HERE = os.path.dirname(os.path.abspath(__file__))
VAULT = "/Users/brooksorradre2/Documents/marketing brain"
REAL = os.path.join(VAULT, "brands/velantra/products/delphine/real-product")
KEYF = os.path.join(HERE, "_library", "keyframes")
STILLS = os.path.join(HERE, "stills")
CLIPS = os.path.join(HERE, "clips")
STATE = os.path.join(HERE, "_library", "state.json")
for p in (KEYF, STILLS, CLIPS, os.path.dirname(STATE)):
    os.makedirs(p, exist_ok=True)

KIE_KEY = next(l.split("=", 1)[1].strip() for l in open(os.path.join(VAULT, ".env"))
               if l.startswith("KIE_API_KEY="))
GEM_KEY = next(l.split("=", 1)[1].strip().strip('"').strip("'")
               for l in open(os.path.join(VAULT, ".env")) if l.startswith("GEMINI_API_KEY="))
OMNI = "https://generativelanguage.googleapis.com/v1beta/interactions"

# Real 25 cm photography is the i2i base, never the 46 cm Eleanor stills (PRODUCT-TRUTH.md 2b).
REFS = {
    ("LC", False): ["LC-01.png"],
    ("DC", False): ["DC-01.png"],
    ("AG", False): ["AG-01.png"],
    ("LC", True): ["ref-interior.jpg", "LC-01.png"],
    ("DC", True): ["DC-02.png", "DC-01.png"],
}
LEATHER = {"LC": "warm chestnut brown", "DC": "very dark espresso brown that reads nearly black in shadow",
           "AG": "warm chestnut brown"}
CANVAS = {"LC": "cream ivory", "DC": "cream ivory", "AG": "deep muted olive green"}


def delphine_id(cw, open_bag):
    t = (f"PRODUCT TRUTH, follow exactly. The bag is the Delphine, a small structured top handle handbag, "
         f"25 centimeters wide, 22 centimeters tall and 14 centimeters deep, so it is nearly square seen "
         f"from the front and noticeably deep front to back. It is a handbag and never a travel bag, never "
         f"a weekender, never a duffel and never a large tote. Its upper section is {LEATHER[cw]} leather "
         f"with visible natural grain, shaped as a domed arched flap, over a lower body of {CANVAS[cw]} "
         f"canvas. Two short rolled leather top handles rise from the leather band and arch only about three "
         f"inches above the top edge. Two leather belt straps run roughly horizontally across the front, "
         f"angling slightly down toward the centre, each passing through a flat gold plate with an oblong "
         f"slot and continuing outward to a small gold roller buckle on each side gusset. A small gold turn "
         f"lock sits at the front centre. A small leather clochette tag hangs on a long leather tab. Leather "
         f"corner patches finish the bottom and small gold feet sit along the bottom edge. The gold fittings "
         f"stay full size so they read large against the small front panel. All metal is warm brass gold. "
         f"There are no logos, no embossed text and no lettering anywhere on the bag. The bag has no zipper "
         f"on the outside and no shoulder strap, no crossbody strap and no long strap of any kind.")
    if open_bag:
        t += (" The bag is OPEN: the one piece leather flap is folded all the way BACK behind the bag, so "
              "the front shows NO flap, no scalloped tabs and no oval keyhole plate, only the shallow "
              "leather band carrying the turn lock with one flat gold plate either side. The mouth stands "
              "open above it and the fabric lining with its zip pocket is visible inside.")
    else:
        t += (" The bag is CLOSED: the one piece leather flap is folded down flat over the front with its "
              "domed top edge clearly readable, both belt straps fastened outward to their side buckles. "
              "No hand touches the flap, the turn lock or the belt straps.")
    return t


SURF = ("the leather is creased at stress points, faintly scuffed, its natural grain uneven and dulled "
        "where it has been handled, never a uniform polished finish, and the canvas shows individual "
        "woven fibres, slubs and small wrinkles")

FOOTER = ("CRITICAL RENDERING INSTRUCTION. This is a real photograph casually taken on an iPhone 15 Pro by "
          "an ordinary person, handheld, in one second, with no lighting equipment, no tripod and no styling. "
          "It is NOT a 3D render, NOT CGI, NOT a product visualisation, NOT Blender or Octane or Unreal or "
          "Keyshot, NOT ray traced, NOT a commercial or catalogue product photograph, NOT an advertisement, "
          "NOT retouched, NOT airbrushed, NOT studio lit. If it looks polished or computer generated it is "
          "wrong. Photographic evidence that must be present: visible digital sensor noise and grain through "
          "the shadows and midtones, highlights slightly blown out where the light source hits, mild "
          "chromatic aberration on high contrast edges, faint JPEG compression artefacts, focus that is "
          "slightly imperfect so nothing is tack sharp, a trace of handheld motion blur, and framing that is "
          "a little crooked and off centre the way a real snapshot is. Real light only: one dominant "
          "available light source, mixed colour temperature across the frame, uneven exposure, and real "
          "shadows falling off naturally with visible ambient bounce. Real surfaces: " + SURF + "; ordinary "
          "dust, lint and fingerprints are present; the setting is a real lived in place with ordinary "
          "clutter, not a set. When human skin appears it shows real texture, visible pores and fine hairs, "
          "never retouched, and any face stays fully outside the frame. This bag is the only bag anywhere in "
          "the picture. No on screen text, no lettering, no signage, no graphics and no other branded "
          "products anywhere. Vertical 9:16 portrait framing.")

ANTIDRIFT = ("The bag keeps exactly these proportions and details everywhere in the frame, even when it is "
             "small in frame or partly out of focus.")


def build_prompt(s):
    sid, cw, cat, open_bag, scene, motion = s
    n = len(REFS[(cw, open_bag)])
    pl = "s" if n > 1 else ""
    pre = (f"Use the attached product photo{pl} ONLY as the reference for the bag shape, proportions, "
           f"materials, colours, stitching and hardware. Do NOT copy the lighting, the plain background, "
           f"the clean edges or the polished studio product photo look of the attachment{pl}. Those are "
           f"catalogue images and the picture you produce must not resemble one. Create the following real "
           f"photograph instead.")
    return "\n\n".join([pre, scene, delphine_id(cw, open_bag), ANTIDRIFT + " " + FOOTER])


# ---------------- kie ----------------
def curl_json(args, timeout=180):
    out = subprocess.run(args, capture_output=True, text=True, timeout=timeout).stdout
    try:
        return json.loads(out)
    except Exception:
        return {"_raw": out[:300]}


def kie_upload(path):
    for a in range(4):
        if a:
            time.sleep(10 * a)
        d = curl_json(["curl", "-s", "-X", "POST", "https://kieai.redpandaai.co/api/file-stream-upload",
                       "-H", f"Authorization: Bearer {KIE_KEY}", "-F", f"file=@{path}",
                       "-F", "uploadPath=delphine-broll"])
        u = (d.get("data") or {}).get("downloadUrl")
        if u:
            return u
    raise RuntimeError(f"upload failed {path}")


def kie_image(prompt, urls):
    d = curl_json(["curl", "-s", "-X", "POST", "https://api.kie.ai/api/v1/jobs/createTask",
                   "-H", f"Authorization: Bearer {KIE_KEY}", "-H", "Content-Type: application/json",
                   "-d", json.dumps({"model": "gpt-image-2-image-to-image",
                                     "input": {"prompt": prompt, "input_urls": urls,
                                               "aspect_ratio": "9:16",
                                               "resolution": "1K"}})])   # 1K, like Colette
    if d.get("code") != 200:
        return None
    tid = d["data"]["taskId"]
    for _ in range(80):
        time.sleep(10)
        r = curl_json(["curl", "-s", f"https://api.kie.ai/api/v1/jobs/recordInfo?taskId={tid}",
                       "-H", f"Authorization: Bearer {KIE_KEY}"])
        st = (r.get("data") or {}).get("state")
        if st == "success":
            return json.loads(r["data"]["resultJson"], strict=False)["resultUrls"][0]
        if st == "fail":
            return None
    return None


def keyframes(nvar=2, only=None):
    cache = {}
    todo = []
    for s in SCENES:
        if only and not any(o in s[0] for o in only):
            continue
        for v in range(1, nvar + 1):
            dst = os.path.join(KEYF, f"{s[0]}-v{v}.png")
            if not os.path.exists(dst):
                todo.append((s, v, dst))
    print(f"{len(todo)} images to generate", flush=True)
    for cw, ob in {(s[1], s[3]) for s, _, _ in todo}:
        for f in REFS[(cw, ob)]:
            if f not in cache:
                cache[f] = kie_upload(os.path.join(REAL, f))
                print(f"uploaded {f}", flush=True)

    def one(job):
        s, v, dst = job
        url = kie_image(build_prompt(s), [cache[f] for f in REFS[(s[1], s[3])]])
        if not url:
            print(f"FAIL {os.path.basename(dst)}", flush=True)
            return
        subprocess.run(["curl", "-s", "-L", "-o", dst, url], check=True)
        print(f"ok {os.path.basename(dst)} ({os.path.getsize(dst)//1024} KB)", flush=True)

    with ThreadPoolExecutor(max_workers=6) as ex:
        list(ex.map(one, todo))


# ---------------- Omni ----------------
def load_state():
    return json.load(open(STATE)) if os.path.exists(STATE) else {}


def save_state(s):
    json.dump(s, open(STATE, "w"), indent=1)


def animate(only=None):
    import base64
    st = load_state()
    motions = {s[0]: s[5] for s in SCENES}
    for f in sorted(os.listdir(STILLS)):
        if not f.endswith(".png"):
            continue
        key = f[:-4]
        if only and not any(o in key for o in only):
            continue
        if key in st or os.path.exists(os.path.join(CLIPS, key + ".mp4")):
            continue
        if key not in motions:
            print(f"no motion for {key}"); continue
        payload = {"model": "models/gemini-omni-flash-preview",
                   "input": [{"type": "image",
                              "data": base64.b64encode(open(os.path.join(STILLS, f), "rb").read()).decode(),
                              "mime_type": "image/png"},
                             {"type": "text",
                              "text": motions[key] + " No people speaking, natural ambient sound only. "
                                                     "Vertical 9:16."}],
                   "background": True, "generation_config": {"video_config": {}}}
        p = os.path.join(HERE, "_library", ".payload.json")
        open(p, "w").write(json.dumps(payload))
        d = curl_json(["curl", "-s", "-X", "POST", f"{OMNI}?key={GEM_KEY}",
                       "-H", "Content-Type: application/json", "--data-binary", f"@{p}"], timeout=300)
        if "id" in d:
            st[key] = d["id"]; print(f"launched {key}", flush=True)
        else:
            print(f"FAILED {key}: {json.dumps(d)[:160]}", flush=True)
        save_state(st); time.sleep(1)


def poll():
    import base64
    st = load_state(); done = pend = 0
    for key, iid in st.items():
        out = os.path.join(CLIPS, key + ".mp4")
        if os.path.exists(out) and os.path.getsize(out) > 100_000:
            done += 1; continue
        d = curl_json(["curl", "-s", f"{OMNI}/{iid}?key={GEM_KEY}"], timeout=300)
        if d.get("status") == "completed":
            vid = None
            for step in d.get("steps", []):
                for c in step.get("content", []):
                    if c.get("type") == "video":
                        vid = c.get("data")
            if vid:
                open(out, "wb").write(base64.b64decode(vid)); done += 1
                print(f"landed {key}", flush=True)
        elif d.get("status") in ("failed", "error"):
            print(f"FAILED {key}")
        else:
            pend += 1
    print(f"{done} landed, {pend} pending")
    return pend


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "poll"
    if cmd == "keyframes":
        n = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 2
        keyframes(n, only=sys.argv[3:] or None)
    elif cmd == "animate":
        animate(only=sys.argv[2:] or None)
    else:
        poll()
