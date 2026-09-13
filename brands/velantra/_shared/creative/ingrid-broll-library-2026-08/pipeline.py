#!/usr/bin/env python3
"""Ingrid B-roll library pipeline: prompts + kie GPT Image 2 keyframes (3 variants/scene, resumable).

Commands:
  python3 pipeline.py probe ING-001            # single variant of one scene (validation)
  python3 pipeline.py run [PREFIX] [--variants N]
  python3 pipeline.py status
  python3 pipeline.py prompt ING-001           # print assembled prompt
"""
import base64, json, os, subprocess, sys, time, urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from scenes import SCENES

VAULT = os.path.expanduser("~/Documents/marketing brain")
ENV = {}
for line in open(os.path.join(VAULT, ".env")):
    line = line.strip()
    if "=" in line and not line.startswith("#"):
        k, v = line.split("=", 1)
        ENV[k] = v.strip().strip('"').strip("'")
KIE_KEY = ENV["KIE_API_KEY"]

INGDIR = os.path.join(VAULT, "brands/velantra/products/ingrid/product-images/system-oat-greige")
CWFILE = {"bordeaux": "bordeaux-brown", "black": "midnight-black", "cognac": "cognac"}

def _ref(cw, shot):
    return os.path.join(INGDIR, f"ingrid-{CWFILE[cw]}-{shot}.png")

ING_COLOR = {
    "bordeaux": {
        "body": ("deep bordeaux brown vegetable tanned leather, a dark chocolate body with oxblood red "
                 "undertones that lightens to warm chestnut where the finish has burnished"),
        "handles": "dark espresso brown",
        "piping": ("Light whiskey tan edge piping runs down the side gussets and around the base, "
                   "standing out clearly against the dark body."),
        "closure": ("Two contrasting light whiskey tan leather belt straps cross the front horizontally, "
                    "always two separate straps that never merge into one, each passing through its own "
                    "raised brass staple loop, and each strap ends in an angled brushed gold clasp plate "
                    "with small round rivets. A small brass turn lock sits at the top center of the front "
                    "between the two straps. The front hardware reads as three separate metal elements "
                    "spaced apart in a row, a gold clasp plate toward the left, the small turn lock at the "
                    "center, and a gold clasp plate toward the right, and this stays true from every "
                    "camera angle."),
        "extra": "",
    },
    "black": {
        "body": "glossy midnight black vegetable tanned leather",
        "handles": "black",
        "piping": "Self colored black edge piping runs down the side gussets and around the base.",
        "closure": ("A slim black leather belt crosses the front horizontally, its ends passing through "
                    "raised brass staple loops toward the left and right, and it closes at exactly ONE "
                    "brushed gold Kelly style clasp plate at the top center of the front, with a gold "
                    "diamond shaped turn lock sitting on the plate and small round rivets on it. There is "
                    "only this one clasp plate on the whole front, there are no clasp plates near the "
                    "staple loops and no second lock anywhere."),
        "extra": "",
    },
    "cognac": {
        "body": ("burnished cognac vegetable tanned leather, a warm whiskey tan with darker smoky amber "
                 "patches where the antique finish has gathered"),
        "handles": "matching cognac",
        "piping": "Matching cognac edge piping runs down the side gussets and around the base.",
        "closure": ("A matching cognac leather belt crosses the front horizontally, its ends passing "
                    "through raised brass staple loops toward the left and right, and it closes at exactly "
                    "ONE brushed gold Kelly style clasp plate at the top center of the front, with a gold "
                    "ring shaped turn lock standing up through the plate slot and small round rivets on "
                    "it. There is only this one clasp plate on the whole front, there are no clasp plates "
                    "near the staple loops and no second lock anywhere."),
        "extra": (" A double row of decorative braided stitching runs along the curved top edge of the "
                  "front panel and the top rim."),
    },
}


def ingrid_id(cw, open_bag):
    c = ING_COLOR[cw]
    t = (f"PRODUCT TRUTH, follow exactly. The bag is the Ingrid, an oversized top handle carryall in "
         f"{c['body']}. The leather is high oil veg tan with a softly glossy antiqued patina, heavily "
         f"creased and rumpled all over so light moves across it unevenly, never a smooth uniform surface. "
         f"The bag is clearly wider than it is tall, about 38 centimeters wide, 31 centimeters tall and 16 "
         f"centimeters deep, softly structured so the body relaxes slightly while still standing upright on "
         f"its own, with deep triangular side gussets. Two rolled round leather top handles in "
         f"{c['handles']} rise high above the top. A sculpted front panel folds down over the upper front, "
         f"its curved hand stitched edge visible, and the handles pass through shaped cutouts in it. "
         f"{c['closure']}{c['extra']} {c['piping']} The base corners are "
         f"reinforced with darker leather corner caps and the bag stands on four small metal feet. A small "
         f"round rivet sits at each top corner of the front panel. Every piece of metal on the bag is "
         f"brushed antique brass gold, there is no silver and no shiny chrome anywhere on it. There is no "
         f"shoulder strap anywhere in the scene. There are no logos, no embossed text and no lettering "
         f"anywhere on the bag.")
    if open_bag:
        t += (" The bag stands wide open. The top gapes open, the handles fall away to the sides and the "
              "belt straps hang loose and separate. The inside is the natural flesh side of the same "
              "leather, a matte caramel tan suede feel surface, completely unlined, with no fabric lining, "
              "no interior zipper, no logo tag and no lettering inside.")
    return t


SURF = ("the veg tanned leather is heavily creased and rumpled, its glossy antique patina uneven, darker "
        "in the folds and lighter where it has rubbed, with fine scratches and scuffs from real use, never "
        "a uniform polished finish")

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
          "shadows falling off naturally with visible ambient bounce. Real surfaces: {surf}; ordinary dust, "
          "lint and fingerprints are present; the setting is a real lived in place with ordinary clutter, "
          "not a set. When human skin appears it shows real texture, visible pores and fine hairs, never "
          "retouched, and any face stays fully outside the frame. No on screen text, no lettering, no "
          "signage, no graphics and no other branded products anywhere. Vertical 9:16 portrait framing.")

ANTIDRIFT = ("The bag keeps exactly these proportions and details everywhere in the frame, even when it is "
             "small in frame or partly out of focus.")


def scene_by_id(sid):
    for s in SCENES:
        if s[0] == sid or s[0].startswith(sid):
            return s
    raise KeyError(sid)


def refs_for(s):
    sid, product, cw, cat, open_bag, scene, motion = s
    files = [_ref(cw, "hero")]
    if cat == "macro":
        files.append(_ref(cw, "detail"))
    if open_bag:
        files.append(_ref(cw, "interior"))
    return files


def build_prompt(s):
    sid, product, cw, cat, open_bag, scene, motion = s
    n_refs = len(refs_for(s))
    plural = "s" if n_refs > 1 else ""
    pre = (f"Use the attached product photo{plural} ONLY as the reference for the bag shape, proportions, "
           f"materials, colours, stitching and hardware. Do NOT copy the lighting, the plain background, the "
           f"clean edges or the polished studio product photo look of the attachment{plural}. Those are "
           f"catalogue images and the picture you produce must not resemble one. Create the following real "
           f"photograph instead.")
    return "\n\n".join([pre, scene, ingrid_id(cw, open_bag), ANTIDRIFT + " " + FOOTER.format(surf=SURF)])


def motion_prompt(s):
    return s[6] + " No people speaking, natural ambient sound only. Vertical 9:16."


# ---------------- kie helpers ----------------
def _req(url, data=None, headers=None, timeout=90):
    h = {"Authorization": f"Bearer {KIE_KEY}"}
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, data=data, headers=h)
    return urllib.request.urlopen(req, timeout=timeout).read()


def kie_upload(path):
    last = ""
    for attempt in range(4):
        if attempt:
            time.sleep(20 * attempt)
        out = subprocess.run(
            ["curl", "-s", "-X", "POST", "https://kieai.redpandaai.co/api/file-stream-upload",
             "-H", f"Authorization: Bearer {KIE_KEY}",
             "-F", f"file=@{path}",
             "-F", "uploadPath=broll-library",
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
    raise RuntimeError(f"upload failed for {path}: {last[:200]}")


def kie_create(model, inp):
    out = _req("https://api.kie.ai/api/v1/jobs/createTask",
               data=json.dumps({"model": model, "input": inp}).encode(),
               headers={"Content-Type": "application/json"})
    d = json.loads(out)
    if not d.get("data") or not d["data"].get("taskId"):
        raise RuntimeError(f"createTask: {d}")
    return d["data"]["taskId"]


def kie_poll(task_id, timeout_s=600):
    t0 = time.time()
    while time.time() - t0 < timeout_s:
        raw = _req(f"https://api.kie.ai/api/v1/jobs/recordInfo?taskId={task_id}")
        d = json.loads(raw.decode(), strict=False)
        st = d.get("data", {}).get("state")
        if st == "success":
            rj = d["data"].get("resultJson")
            rj = json.loads(rj, strict=False) if isinstance(rj, str) else rj
            return rj.get("resultUrls") or rj.get("result_urls")
        if st == "fail":
            raise RuntimeError(f"task failed: {d['data'].get('failMsg', d['data'].get('failCode'))}")
        time.sleep(8)
    raise TimeoutError(task_id)


def download(url, out):
    subprocess.run(["curl", "-s", "-L", "-A", "Mozilla/5.0", "--max-time", "180", url, "-o", out], check=True)
    return os.path.getsize(out) > 10000


STATE_DIR = os.path.join(HERE, "state")
KF_DIR = os.path.join(HERE, "keyframes")
os.makedirs(STATE_DIR, exist_ok=True)
os.makedirs(KF_DIR, exist_ok=True)
STATE_FILE = os.path.join(STATE_DIR, "keyframes.json")
UPLOADS_FILE = os.path.join(STATE_DIR, "uploads.json")


def load(f, default):
    return json.load(open(f)) if os.path.exists(f) else default


def save(f, d):
    tmp = f + ".tmp"
    json.dump(d, open(tmp, "w"), indent=1)
    os.replace(tmp, f)


def get_upload(path, uploads):
    key = path
    ent = uploads.get(key)
    if ent and time.time() - ent["ts"] < 20 * 3600:
        return ent["url"]
    url = kie_upload(path)
    uploads[key] = {"url": url, "ts": time.time()}
    save(UPLOADS_FILE, uploads)
    return url


def gen_variant(s, v, uploads, aspect="9:16"):
    sid = s[0]
    d = os.path.join(KF_DIR, sid)
    os.makedirs(d, exist_ok=True)
    out = os.path.join(d, f"v{v}.png")
    if os.path.exists(out) and os.path.getsize(out) > 10000:
        return out, "cached"
    prompt = build_prompt(s)
    input_urls = [get_upload(p, uploads) for p in refs_for(s)]
    last_err = None
    for attempt in range(6):
        try:
            tid = kie_create("gpt-image-2-image-to-image",
                             {"prompt": prompt, "input_urls": input_urls,
                              "aspect_ratio": aspect, "resolution": "1K"})
            urls = kie_poll(tid)
            if not urls:
                raise RuntimeError("no result urls")
            if not download(urls[0], out):
                raise RuntimeError("download too small")
            return out, tid
        except Exception as e:
            last_err = e
            msg = str(e)
            if "aspect" in msg.lower() and aspect == "9:16":
                aspect = "2:3"
                continue
            time.sleep(10 + attempt * 10)
    raise RuntimeError(f"{sid} v{v}: {last_err}")


def cmd_probe(sid):
    uploads = load(UPLOADS_FILE, {})
    s = scene_by_id(sid)
    out, tid = gen_variant(s, 1, uploads)
    print("OK", out, tid)


def cmd_run(prefix=None, variants=3, workers=6):
    import queue, threading
    uploads = load(UPLOADS_FILE, {})
    state = load(STATE_FILE, {})
    lock = threading.Lock()
    q = queue.Queue()
    for s in SCENES:
        if prefix and not s[0].startswith(prefix):
            continue
        st = state.get(s[0], {})
        for v in range(1, variants + 1):
            ent = st.get(f"v{v}")
            if not (ent and ent.get("ok")):
                q.put((s, v))
    total = q.qsize()
    print(f"queue: {total} variants to generate, {workers} workers", flush=True)
    # pre-upload all refs serially to avoid duplicate uploads across threads
    ref_files = set()
    for s in SCENES:
        if prefix and not s[0].startswith(prefix):
            continue
        ref_files.update(refs_for(s))
    for p in sorted(ref_files):
        get_upload(p, uploads)
    counters = {"done": 0, "fail": 0}

    def worker(wid):
        time.sleep(wid * 7)
        while True:
            try:
                s, v = q.get_nowait()
            except queue.Empty:
                return
            sid = s[0]
            try:
                out, tid = gen_variant(s, v, uploads)
                with lock:
                    state.setdefault(sid, {})[f"v{v}"] = {"ok": True, "path": out, "task": tid}
                    counters["done"] += 1
                    save(STATE_FILE, state)
                    n = counters["done"] + counters["fail"]
                print(f"[{n}/{total}] {sid} v{v} ok", flush=True)
            except Exception as e:
                with lock:
                    state.setdefault(sid, {})[f"v{v}"] = {"ok": False, "err": str(e)[:300]}
                    counters["fail"] += 1
                    save(STATE_FILE, state)
                print(f"{sid} v{v} FAIL {e}", flush=True)
            q.task_done()

    threads = [threading.Thread(target=worker, args=(i,), daemon=True) for i in range(workers)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(f"done: {counters['done']} generated, {counters['fail']} failed")


def cmd_status():
    state = load(STATE_FILE, {})
    total = len(SCENES) * 3
    ok = sum(1 for st in state.values() for v in st.values() if isinstance(v, dict) and v.get("ok"))
    fail = sum(1 for st in state.values() for v in st.values() if isinstance(v, dict) and v.get("ok") is False)
    print(f"variants ok {ok}/{total}, failed {fail}, scenes touched {len(state)}/{len(SCENES)}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd == "probe":
        cmd_probe(sys.argv[2])
    elif cmd == "run":
        pref = None
        var = 3
        args = sys.argv[2:]
        for a in args:
            if a.startswith("--variants"):
                var = int(a.split("=")[1]) if "=" in a else 3
            elif not a.startswith("--"):
                pref = a
        cmd_run(pref, var)
    elif cmd == "prompt":
        print(build_prompt(scene_by_id(sys.argv[2])))
        print("\n--- MOTION ---\n" + motion_prompt(scene_by_id(sys.argv[2])))
    else:
        cmd_status()
