#!/usr/bin/env python3
"""GPT Image 2 i2i keyframe generation for VEL-STRAWTOTE-BEACH-BAG-REPL-01.

Submits all 6 keyframe tasks to kie.ai (gpt-image-2-image-to-image), polls,
downloads, center-crops to 9:16 (720x1280). Resumable: existing kf_NN.png are
skipped; in-flight taskIds persisted in kf_tasks.json.
"""
import json
import os
import ssl
import subprocess
import sys
import time
import urllib.request

try:
    import certifi
    SSL_CTX = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    SSL_CTX = ssl.create_default_context()

BASE = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = "/Users/brooksorradre2/Documents/marketing brain/.env"
API = "https://api.kie.ai/api/v1"
UPLOAD_API = "https://kieai.redpandaai.co/api/file-stream-upload"
MODEL = "gpt-image-2-image-to-image"
VPS_RELAY = "root@187.124.249.12"
TESSA = ("/Users/brooksorradre2/Documents/marketing brain/brands/velantra/"
         "_shared/ugc-creators/Tessa/tessa-ref.png")

PRODUCT = (
    "the Velantra Straw Tote: a structured hand woven straw tote in warm sandy "
    "caramel, tightly woven straw body with braided cross stitch trim along the "
    "edges, a smooth taupe leather flap section across the top made of exactly 3 "
    "leather elements, one wide center panel and 2 squared outer tabs, two rolled "
    "taupe leather top handles, two taupe leather belt straps crossed on the front, "
    "white contrast stitching on all leather edges, no metal hardware, no logos. "
    "The leather flap, tabs and belt straps exist ONLY on the FRONT face of the "
    "bag, the back face is plain woven straw, no duplicated front detailing on any "
    "other face."
)
MECH = (
    "Flap and opening construction: the taupe leather flap is ONE connected piece "
    "attached along the top rear edge of the tote, folding forward over the front, "
    "made of a wide center panel and 2 squared outer tabs joined at the top, exactly "
    "3 sections, always folded all the way forward over the front and lying "
    "completely flat against the front face together as one unit, never half open, "
    "never lifted at an angle, never standing up. The flap never splits into "
    "separate floating pieces, there is never a gap between its sections, and "
    "nothing ever pokes out through or between the flap sections. When the tote is "
    "open or carrying things, the woven mouth opens BEHIND the flap: contents lean "
    "out of the open mouth at the back of the bag, behind the leather flap, never "
    "through the flap and never between its tabs. The 2 taupe leather belt straps "
    "lie crossed in a flat X over the front below the flap with rounded ends and "
    "white contrast stitching, exactly as on the closed reference bag, never "
    "knotted, never looped, never threaded through the flap sections and never "
    "wrapped around contents. No metal hardware anywhere on the bag, no snaps, no "
    "buckles, no zippers."
)
STYLE = ("Photorealistic raw iPhone UGC still, natural bright beach daylight, "
         "subtle grain, vertical framing. No on-screen text of any kind, no "
         "caption text, no watermark, no logo text.")

KEYFRAMES = [
    {
        "n": 1, "src": "ref_frames/kf_src_01.jpg",
        "inputs": ["product_refs/caramel_front.png",
                   "/Users/brooksorradre2/Documents/marketing brain/brands/"
                   "velantra/products/straw-birkin/product-images/straw birkin/"
                   "caramel 1.png"],
        "prompt": (
            "Recreate the exact composition, framing, camera angle and lighting of "
            "image 1: a close up of a straw handbag sitting upright on a navy blue "
            "and white striped beach towel laid on white sand, calm water and green "
            "shrubs in the far background, bright midday sun, a woman's hand "
            "reaching in from the right side of frame. Replace the handbag entirely "
            f"with {PRODUCT} The tote sits upright on the striped towel, front face "
            "with the flat caramel leather flap and the crossed belt straps facing "
            "the camera. The woven mouth of the tote is relaxed slightly open "
            "BEHIND the flap. The woman's hand reaches in from the right holding a "
            "plain matte white sunscreen bottle with no label text, lowering it "
            "into the woven mouth at the CENTER of the bag between the two "
            "handles. The bottle is BEHIND the leather flap band: its lower "
            "half is already hidden behind the band's top edge, the band's "
            "unbroken top stitch line passes IN FRONT of the bottle, and the "
            "bottle never overlaps the flap's front face, never touches the "
            "handle slits, never passes through or between any flap sections. "
            "Fair skin, short soft cream "
            "fingernails. The tote must match the product in images 2 and 3 "
            "EXACTLY, especially the flap construction: the flap is ONE "
            "continuous smooth leather band running the FULL width of the bag "
            "along the top front edge, sitting over the top rim edge to edge, "
            "and from this single band the wide center panel and the 2 stepped "
            "outer tabs hang down as the SAME piece of leather, no woven straw "
            "visible above the flap band on the front face and no straw between "
            "the band and the hanging sections. The two rolled handles rise "
            "through two narrow slits in the flap between the center panel and "
            "the outer tabs, exactly as in image 3. Exactly 2 belt straps form "
            "ONE single flat X crossing on the front below the flap, never 3 "
            "straps, never a lattice. Smooth light taupe leather exactly the "
            "shade of image 3. " + MECH + " " + STYLE
        ),
    },
    {
        "n": 2, "src": "ref_frames/kf_src_02.jpg",
        "inputs": [TESSA, "product_refs/caramel_front.png"],
        "prompt": (
            "Recreate the exact composition, framing, camera angle and lighting of "
            "image 1: a young woman standing on a white sand beach at the "
            "shoreline, calm ocean and blue sky with big clouds behind her, framed "
            "from the knees up, head tilted down looking at a bag at her hip, both "
            "hands at the bag. Replace the woman with the woman from image 2, "
            "keeping her exact face, strawberry blonde curls and freckles. She "
            "wears a light sage green cropped cotton tank top and white shorts. "
            f"Replace the crossbody bag entirely with {PRODUCT} The tote hangs from "
            "the crook of her left elbow by its two rolled handles at hip height, "
            "front face with the crossed belts facing the camera, and her right "
            "hand reaches into the open woven mouth BEHIND the flat leather flap. "
            "No shoulder strap, no crossbody strap anywhere. The tote is a WIDE "
            "structured tote, clearly wider than it is tall, the same generous "
            "size as a large day tote, matching the proportions of the product in "
            "image 3 exactly. All four top corners of the bag are clean, crisp "
            "woven straw with braided trim, no crumpled straw, no metallic "
            "elements, no hardware at any corner. " + MECH + " " + STYLE
        ),
    },
    {
        "n": 3, "src": "ref_frames/kf_src_03.jpg",
        "inputs": [TESSA, "product_refs/caramel_front.png"],
        "prompt": (
            "Recreate the exact composition, framing, camera angle and lighting of "
            "image 1: a young woman standing on a white sand beach, calm ocean and "
            "blue sky with big clouds behind her, framed from the knees up, holding "
            "a small black compact digital camera raised at eye level with both "
            "hands, about to take a photo. Replace the woman with the woman from "
            "image 2, keeping her exact face, strawberry blonde curls and "
            "freckles, a soft concentrating smile. She wears a light sage green "
            "cropped cotton tank top and white shorts. Replace the crossbody bag "
            f"entirely with {PRODUCT} The tote hangs from the crook of her left "
            "elbow by its two rolled handles at hip height while both hands hold "
            "the camera up, front face with the crossed belts facing the camera "
            "viewer. No shoulder strap, no crossbody strap anywhere. "
            + MECH + " " + STYLE
        ),
    },
    {
        "n": 4, "src": "ref_frames/kf_src_04.jpg",
        "inputs": [TESSA, "product_refs/caramel_front.png"],
        "prompt": (
            "Recreate the exact composition, framing, camera angle and lighting of "
            "image 1: a young woman seen from BEHIND standing on a white sand beach "
            "at the shoreline, calm ocean and blue sky ahead of her, framed from "
            "the knees up, photographing the water with a small black compact "
            "digital camera raised in her hands. Replace the woman with the woman "
            "from image 2 seen from behind, keeping her strawberry blonde curls "
            "falling down her back. She wears a light sage green cropped cotton "
            "tank top and white drawstring shorts. Replace the crossbody bag "
            f"entirely with {PRODUCT} The tote hangs from the crook of her left "
            "elbow at her side, and because it is seen from behind, its PLAIN "
            "woven straw back face is toward the camera viewer with no leather "
            "flap and no belts visible on that face, only the two rolled handles "
            "over her forearm. No shoulder strap, no crossbody strap anywhere. "
            + MECH + " " + STYLE
        ),
    },
    {
        "n": 5, "src": "ref_frames/kf_src_05.jpg",
        "inputs": [TESSA, "product_refs/caramel_front.png"],
        "prompt": (
            "Recreate the exact composition, framing, camera angle and lighting of "
            "image 1: a young woman standing on a white sand beach, calm ocean and "
            "blue sky with big clouds behind her, framed from the knees up, head "
            "tilted down, lowering a small black compact digital camera into a bag "
            "at her hip with both hands. Replace the woman with the woman from "
            "image 2, keeping her exact face, strawberry blonde curls and "
            "freckles. She wears a light sage green cropped cotton tank top and "
            f"white drawstring shorts. Replace the crossbody bag entirely with {PRODUCT} "
            "The tote hangs from the crook of her left elbow by its two rolled "
            "handles at hip height, front face with the crossed belts facing the "
            "camera, and her right hand lowers the compact camera into the open "
            "woven mouth BEHIND the flat leather flap. No shoulder strap, no "
            "crossbody strap anywhere. " + MECH + " " + STYLE
        ),
    },
    {
        "n": 6, "src": "ref_frames/kf_src_06.jpg",
        "inputs": ["product_refs/caramel_front.png"],
        "prompt": (
            "Recreate the exact composition, framing, camera angle and lighting of "
            "image 1: a bare outstretched arm reaching down from the top right of "
            "frame holding a straw handbag up high against blue sky, big white "
            "clouds and calm ocean, white sand below, bright midday sun. Replace "
            f"the handbag entirely with {PRODUCT} The hand grips BOTH rolled taupe "
            "leather top handles together so the tote hangs straight down, front "
            "face with the flat caramel leather flap and the crossed belt straps "
            "facing the camera, no shoulder strap, no crossbody strap, no dangling "
            "extra straps anywhere. Fair skin, short soft cream fingernails. "
            + MECH + " " + STYLE
        ),
    },
]


def env_key():
    key = os.environ.get("KIE_API_KEY")
    if not key and os.path.exists(ENV_PATH):
        for line in open(ENV_PATH):
            if line.strip().startswith("KIE_API_KEY="):
                key = line.strip().split("=", 1)[1]
                break
    if not key:
        sys.exit("KIE_API_KEY not found")
    return key


def api(method, url, key, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {key}")
    if data:
        req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=120, context=SSL_CTX) as r:
        return json.loads(r.read().decode("utf-8", "replace"), strict=False)


def upload(path, key):
    last = ""
    for attempt in range(4):
        if attempt:
            time.sleep(30 * attempt)
        out = subprocess.run(
            ["curl", "-s", "-X", "POST", UPLOAD_API,
             "-H", f"Authorization: Bearer {key}",
             "-F", f"file=@{path}",
             "-F", "uploadPath=velantra-strawtote-repl",
             "-F", f"fileName={int(time.time())}-{os.path.basename(path).replace(' ', '_')}"],
            capture_output=True, text=True)
        try:
            resp = json.loads(out.stdout)
        except ValueError:
            last = out.stdout or out.stderr
            continue
        if resp.get("data", {}).get("downloadUrl"):
            return resp["data"]["downloadUrl"]
        last = out.stdout
    sys.exit(f"upload failed for {path}: {last[:300]}")


def upload_cached(path, key, cache):
    path = os.path.abspath(path)
    if path not in cache:
        cache[path] = upload(path, key)
        print(f"  uploaded {os.path.basename(path)}")
    return cache[path]


def download(url, dest):
    try:
        subprocess.run(["curl", "-sL", "-o", dest, url], check=True,
                       capture_output=True, timeout=25)
        if os.path.getsize(dest) > 10_000:
            return dest
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        pass
    remote = f"/tmp/kie_kf_{os.getpid()}_{abs(hash(url)) % 100000}.png"
    subprocess.run(["ssh", "-o", "ConnectTimeout=10", VPS_RELAY,
                    f"curl -sL -o '{remote}' --max-time 60 '{url}'"], check=True)
    subprocess.run(["scp", "-q", f"{VPS_RELAY}:{remote}", dest], check=True)
    subprocess.run(["ssh", VPS_RELAY, f"rm -f '{remote}'"], check=False)
    return dest


def crop_916(src, dest):
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", src,
         "-vf", "crop='min(iw,ih*9/16)':'min(ih,iw*16/9)',scale=720:1280",
         dest], check=True)


def main():
    key = env_key()
    os.chdir(BASE)
    os.makedirs("keyframes", exist_ok=True)
    cache_file = "upload_cache.json"
    cache = json.load(open(cache_file)) if os.path.exists(cache_file) else {}
    tasks_file = "kf_tasks.json"
    tasks = json.load(open(tasks_file)) if os.path.exists(tasks_file) else {}

    only = {int(x) for x in sys.argv[1:]} if len(sys.argv) > 1 else None
    jobs = [k for k in KEYFRAMES if only is None or k["n"] in only]

    # submit all pending tasks first (parallel server-side)
    for kf in jobs:
        n = kf["n"]
        dest = f"keyframes/kf_{n:02d}.png"
        if os.path.exists(dest) and os.path.getsize(dest) > 10_000:
            print(f"kf {n}: exists, skipping")
            continue
        if str(n) in tasks:
            print(f"kf {n}: resuming task {tasks[str(n)]}")
            continue
        urls = [upload_cached(kf["src"], key, cache)]
        urls += [upload_cached(p, key, cache) for p in kf["inputs"]]
        json.dump(cache, open(cache_file, "w"), indent=1)
        resp = api("POST", f"{API}/jobs/createTask", key, {
            "model": MODEL,
            "input": {"prompt": kf["prompt"], "input_urls": urls,
                      "aspect_ratio": "2:3", "resolution": "2K"}})
        if resp.get("code") != 200:
            sys.exit(f"kf {n}: createTask failed: {resp}")
        tasks[str(n)] = resp["data"]["taskId"]
        json.dump(tasks, open(tasks_file, "w"), indent=1)
        print(f"kf {n}: task {tasks[str(n)]} submitted")

    # poll all
    pending = {kf["n"] for kf in jobs
               if not (os.path.exists(f"keyframes/kf_{kf['n']:02d}.png")
                       and os.path.getsize(f"keyframes/kf_{kf['n']:02d}.png") > 10_000)}
    while pending:
        for n in sorted(pending):
            tid = tasks.get(str(n))
            resp = api("GET", f"{API}/jobs/recordInfo?taskId={tid}", key)
            d = resp.get("data", {})
            state = d.get("state")
            if state == "success":
                result = json.loads(d.get("resultJson") or "{}", strict=False)
                url = (result.get("resultUrls") or [None])[0]
                if not url:
                    sys.exit(f"kf {n}: success but no resultUrls: {result}")
                dest = f"keyframes/kf_{n:02d}.png"
                download(url, dest)
                crop_916(dest, f"keyframes/kf_{n:02d}_916.png")
                tasks.pop(str(n), None)
                json.dump(tasks, open(tasks_file, "w"), indent=1)
                print(f"kf {n}: DONE ({d.get('creditsConsumed')} credits)")
                pending.discard(n)
            elif state == "fail":
                tasks.pop(str(n), None)
                json.dump(tasks, open(tasks_file, "w"), indent=1)
                print(f"kf {n}: FAILED {d.get('failCode')} {d.get('failMsg')} "
                      "(re-run to retry)")
                pending.discard(n)
        if pending:
            time.sleep(15)
    print("all keyframes done")


if __name__ == "__main__":
    main()
