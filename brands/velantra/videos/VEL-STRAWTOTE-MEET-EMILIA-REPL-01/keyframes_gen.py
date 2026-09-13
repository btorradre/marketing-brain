#!/usr/bin/env python3
"""GPT Image 2 i2i keyframe generation for VEL-STRAWTOTE-MEET-EMILIA-REPL-01.

Submits all 9 keyframe tasks to kie.ai (gpt-image-2-image-to-image), polls,
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
    "Flap and opening construction: the leather flap is ONE single seamless sheet "
    "of leather attached along the top rear edge of the tote and folded all the "
    "way forward over the front, lying completely flat. Its front lower edge is "
    "cut into the shape of a wide center panel and 2 squared outer tabs, but these "
    "are shapes cut into the SAME single sheet, never separate pieces. The leather "
    "is continuous and unbroken between the shapes and across the entire top of "
    "the bag, including between the two handle slots, with no straw weave ever "
    "visible between the top band and the panel or tab shapes. The only openings "
    "anywhere in the flap are the 2 narrow handle slots. No gap, no seam, no "
    "split, no opening exists anywhere else in the flap, and nothing behind or "
    "inside the bag is ever visible through the flap. The 2 leather belt straps "
    "lie crossed in a flat X over the front below the flap with rounded ends and "
    "white contrast stitching, exactly as on the closed reference bag, never "
    "knotted, never looped, never threaded through the flap and never wrapped "
    "around contents. No metal hardware anywhere on the bag, no snaps, no "
    "buckles, no zippers."
)
CANONICAL = ("/Users/brooksorradre2/Documents/marketing brain/brands/velantra/"
             "products/straw-birkin/product-images/straw birkin/caramel 1.png")
OPENED = ("/Users/brooksorradre2/Documents/marketing brain/brands/velantra/"
          "products/straw-birkin/product-images/straw birkin/straw birkin opened.png")
TONE_ANCHOR = ("/Users/brooksorradre2/Documents/marketing brain/brands/velantra/"
               "videos/VEL-STRAWTOTE-MEET-EMILIA-REPL-01/segments/qa_v3/seg01_a.jpg")
TONE = ("The bag's colors must exactly match the bag in the tone reference image: "
        "warm caramel leather and golden sandy straw weave, never grey, never "
        "taupe, never olive, never khaki.")
STYLE = ("Photorealistic raw iPhone UGC still, natural daylight, subtle grain, "
         "vertical framing. No on-screen text of any kind, no watermark, no logo text.")

KEYFRAMES = [
    {
        "n": 1, "src": "ref_frames/kf_src_01.png",
        "inputs": [TESSA, "product_refs/caramel_front.png"],
        "prompt": (
            "Recreate the exact composition, pose, framing, camera angle and lighting of "
            "image 1: a woman sitting on a dark green velvet couch in a bright apartment "
            "living room with a kitchen visible behind her, holding a handbag up at chest "
            "height facing the camera, smiling warmly. Replace the woman with the woman "
            "from image 2, keeping her exact face, strawberry blonde curls and freckles. "
            "She wears a sage green knit sweater and light blue jeans, short soft cream "
            "fingernails, small gold hoop earrings. Replace the navy leather handbag "
            f"entirely with {PRODUCT} The tote front face with the crossed belts points at "
            "the camera and covers her torso exactly where the original bag sat. " + STYLE
        ),
    },
    {
        "n": 2, "src": "ref_frames/kf_src_02.png",
        "inputs": ["product_refs/caramel_front.png"],
        "prompt": (
            "Recreate the exact composition, camera angle, crop and soft daylight of "
            "image 1: a handbag propped upright on a cane rattan chair against a plain "
            "wall, the bag's front face filling the lower two thirds of the frame at a "
            "slight angle, shallow depth of field. Replace the navy leather bag entirely "
            f"with {PRODUCT} Show the woven straw front, the caramel leather flap and the "
            "two crossed belt straps in crisp macro detail. " + STYLE
        ),
    },
    {
        "n": 3, "src": "ref_frames/kf_src_03.png",
        "inputs": ["product_refs/caramel_front.png"],
        "prompt": (
            "Recreate the exact extreme macro composition and moody close lighting of "
            "image 1: a woman's fingers gently touching the edge detail of a handbag, "
            "fingers entering from the left, the bag filling the frame diagonally. "
            "Change the nails to short soft cream polish on light freckled skin. Replace "
            f"the navy bag and gold zipper entirely with {PRODUCT} Her fingertips rest on "
            "the braided straw cross lacing along the edge where straw meets the caramel "
            "leather trim, woven texture in sharp macro focus. " + STYLE
        ),
    },
    {
        "n": 4, "src": "keyframes/kf_04_v2.png",
        "inputs": [TONE_ANCHOR, CANONICAL],
        "prompt": (
            "Reproduce image 1 exactly: same composition, same white table and gold "
            "framed painting, same hands on the two rolled handles, same bag geometry "
            "and same lighting. Change ONLY the colors of the bag to match the bag in "
            f"image 2. {TONE} The flap stays one single seamless sheet as in image 3 "
            "with no straw visible between the top band and the panel or tab shapes. "
            + STYLE
        ),
    },
    {
        "n": 5, "src": "keyframes/kf_04.png",
        "inputs": [OPENED],
        "prompt": (
            "Same white table scene, wall, soft daylight and same warm caramel straw "
            "tote as image 1, but now the tote is shown OPEN exactly like the bag in "
            "image 2: the ENTIRE one piece leather flap is folded all the way over "
            "the top edge to the back of the bag as one seamless sheet, its smooth "
            "leather underside draping down the back, the woven mouth fully open "
            "showing the woven straw interior walls, the two belt straps still "
            "crossed in a flat X on the front below. Copy the handle construction "
            "from image 2 exactly: the two rolled handles attach to the bag body at "
            "the top rim on stitched leather bases, and where the folded flap meets "
            "them it wraps around them through its two narrow handle slots, exactly "
            "as in image 2. No grommets, no stubs, no anchors inside the straw "
            "interior, no invented attachments. A woman's hand with light freckled "
            "skin and short cream nails rests on the front rim of the open mouth. "
            "Camera at a high three quarter angle looking into the bag. The bag "
            "keeps the exact warm caramel leather and golden sandy straw colors of "
            "image 1. No metal hardware anywhere on the bag. " + STYLE
        ),
    },
    {
        "n": 6, "src": "keyframes/kf_06_v2.png",
        "inputs": [CANONICAL],
        "prompt": (
            "Edit image 1 minimally. The ONLY change: extend the leather of the "
            "tote's top band downward so it seamlessly connects to the existing wide "
            "center panel and the existing two squared outer tabs, filling the straw "
            "gap between the band and those shapes with smooth continuous leather so "
            "the whole flap reads as one uninterrupted sheet exactly like the flap "
            "of the bag in image 2. Keep every other detail of image 1 exactly as "
            "it is: same woman, same face, same strawberry blonde curls, same sage "
            "green sweater, same pose holding the small tan leather pouch, same "
            "green velvet couch, same lighting, same bag colors, same panel and tab "
            "shapes, same handles, same crossed belt straps. Do not merge or remove "
            "the tab shapes, do not enclose the handle slots into ovals, do not add "
            "extra layers, do not add metal hardware. " + STYLE
        ),
    },
    {
        "n": 7, "src": "ref_frames/kf_src_07.png",
        "inputs": ["product_refs/caramel_front.png"],
        "prompt": (
            "Recreate the exact bright daylight macro composition of image 1: a diagonal "
            "close-up across the front face of a handbag, crisp texture detail, soft "
            "window light from the upper right, teal fabric just visible in the corner. "
            f"Replace the navy leather bag entirely with {PRODUCT} The frame is filled by "
            "the woven straw texture, the caramel leather flap edge, white contrast "
            "stitching and one crossed belt strap in razor sharp macro. " + STYLE
        ),
    },
    {
        "n": 8, "src": "keyframes/kf_08_v2.png",
        "inputs": [TONE_ANCHOR, CANONICAL],
        "prompt": (
            "Reproduce image 1 exactly: same composition, same white table and gold "
            "framed painting, same hand resting flat on the leather flap, same upright "
            "structured tote geometry and same lighting. Change ONLY the colors of "
            f"the bag to match the bag in image 2. {TONE} The flap stays one single "
            "seamless sheet as in image 3 with no straw visible between the top band "
            "and the panel or tab shapes. " + STYLE
        ),
    },
    {
        "n": 9, "src": "keyframes/kf_09_v2.png",
        "inputs": [CANONICAL],
        "prompt": (
            "Edit image 1 minimally. The ONLY change: rebuild the tote's leather "
            "flap so it exactly matches the flap construction of the bag in image 2: "
            "a top leather band running uninterrupted across the full width of the "
            "bag between the handles, flowing continuously downward into a wide "
            "center panel and two squared outer tabs, all one uninterrupted sheet "
            "of leather with no straw weave visible between the band and the shapes, "
            "no straw reaching the top rim on the front face, and the only openings "
            "being the two narrow handle slots. Keep every other detail of image 1 "
            "exactly as it is: same woman, same face, same strawberry blonde curls "
            "and big warm smile, same sage green sweater, same both hands holding "
            "the tote, same green velvet couch, same lighting, same warm caramel "
            "leather and golden sandy straw colors, same handles, same crossed belt "
            "straps. Do not enclose the handle slots into ovals, do not add extra "
            "layers or a second sheet, do not add metal hardware. " + STYLE
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
