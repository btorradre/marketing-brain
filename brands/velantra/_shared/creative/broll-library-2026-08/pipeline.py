#!/usr/bin/env python3
"""B-roll library pipeline: prompts + kie GPT Image 2 keyframes (3 variants/scene, resumable).

Commands:
  python3 pipeline.py probe COL-001            # single variant of one scene (validation)
  python3 pipeline.py run [PREFIX] [--variants N]
  python3 pipeline.py status
  python3 pipeline.py prompt COL-001           # print assembled prompt
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

MER = os.path.join(VAULT, "brands/velantra/products/margot/product-references/meridian")
MOG = os.path.join(VAULT, "brands/velantra/products/margot/product-images/system-oat-greige")
COLR = os.path.join(VAULT, "brands/velantra/products/cashmere-tote/product-references")
COLG = os.path.join(VAULT, "brands/velantra/products/cashmere-tote/product-images/system-oat-greige")

REFS = {
    ("colette", "caramel"): [os.path.join(COLR, "colette-canonical-caramel-v3.png")],
    ("colette", "espresso"): [os.path.join(COLG, "colette-v3-espresso-hero.png")],
    ("colette", "caramel", "open"): [os.path.join(COLR, "colette-canonical-caramel-v3.png"),
                                     os.path.join(COLG, "colette-v3-caramel-interior.png")],
    ("colette", "espresso", "open"): [os.path.join(COLG, "colette-v3-espresso-hero.png"),
                                      os.path.join(COLG, "colette-v3-espresso-interior.png")],
    ("margot", "burgundy"): [os.path.join(MER, "burgundy 1.webp")],
    ("margot", "black"): [os.path.join(MER, "black 1.webp")],
    ("margot", "brown"): [os.path.join(MER, "brown 1.webp")],
    ("margot", "burgundy", "open"): [os.path.join(MER, "burgundy 1.webp"),
                                     os.path.join(MOG, "margot-burgundy-interior.png")],
    ("margot", "black", "open"): [os.path.join(MER, "black 1.webp"),
                                  os.path.join(MOG, "margot-black-interior.png")],
    ("margot", "brown", "open"): [os.path.join(MER, "brown 1.webp"),
                                  os.path.join(MOG, "margot-brown-interior.png")],
}

COL_TRIM = {"caramel": "warm cognac tan", "espresso": "dark espresso brown"}
MAR_COLOR = {"burgundy": "deep wine burgundy", "black": "midnight black", "brown": "warm tan brown"}


def colette_id(cw, open_bag):
    trim = COL_TRIM[cw]
    t = (f"PRODUCT TRUTH, follow exactly. The bag is the Colette, a wide east west tote in oatmeal greige "
         f"brushed wool felt with a soft cashmere feel surface where fine brushed fibres are visible. It is "
         f"50 centimeters wide, 26 centimeters tall and 18 centimeters deep, clearly wider than it is tall, "
         f"about twice as wide as it is tall seen from the front. It is softly structured and stands upright "
         f"on its own. Two wide felt straps run vertically down the front face. A slim {trim} leather belt "
         f"about half an inch wide crosses the front horizontally, passing through the vertical felt straps, "
         f"and each of its two ends curves outward and downward away from the body, finished with a small "
         f"round aged gold metal disc cap. The two top handles are rolled and wrapped in {trim} leather on "
         f"the grip with felt below, with a short 16 centimeter handle drop. The top of the bag is fully "
         f"open, there is no flap, no zipper and no closure of any kind on the mouth. The only metal on the "
         f"bag is aged gold. There are no logos, no embossed text and no lettering anywhere on the bag.")
    if open_bag:
        t += (" The bag stands open. Inside, the same oatmeal felt continues, the interior is simple with no "
              "visible lining pattern and the contents sit directly inside the felt walls.")
    return t


def margot_id(cw, open_bag):
    color = MAR_COLOR[cw]
    t = (f"PRODUCT TRUTH, follow exactly. The bag is the Margot, a structured leather work tote in {color} "
         f"with an embossed swirling grain texture, never a smooth surface. It is clearly wider than it is "
         f"tall, the top rim is about as wide as the base, with clean geometric lines, and it stands upright "
         f"on its own with a rigid back panel, never slouching and never stretched tall. It has two slim flat "
         f"top handles in the same leather. The top is OPEN, there is no flap covering the mouth and no "
         f"zipper across the top. Two slim decorative belt straps run down over the front face through slim "
         f"silver keepers, and they always hang open and relaxed, their two angled polished silver clasp "
         f"plates meeting in a shallow V on the lower front. One small square polished silver turn lock "
         f"plate sits at the top center of the front face above the V. Every piece of metal on the bag is "
         f"polished silver, there is no gold, no brass and no colored hardware anywhere on it. There is no "
         f"shoulder strap anywhere in the scene. The belts are never fastened and never being handled.")
    if open_bag:
        t += (" The bag stands open. The interior is lined in soft tan suede feel fabric with a slim center "
              "zip divider pocket running front to back through the middle, and a flat padded sleeve against "
              "the rigid back wall. There is no other zipper on the bag itself.")
    return t


SURF = {
    "colette": ("the wool felt shows individual brushed fibres, slight fuzz, small lint and gentle wear, and "
                "the leather trim is softly creased and dulled where it has been handled"),
    "margot": ("the leather is creased at stress points, faintly scuffed, its embossed grain uneven and "
               "dulled where it has been handled, never a uniform polished finish"),
}
SURF["duo"] = SURF["colette"] + "; " + SURF["margot"]

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
    if product == "duo":
        c_cw, m_cw = cw.split("+")
        files = [REFS[("colette", c_cw)][0], REFS[("margot", m_cw)][0]]
        if open_bag:
            files.append(REFS[("margot", m_cw, "open")][1])
        return files
    key = (product, cw, "open") if open_bag else (product, cw)
    return REFS[key]


def build_prompt(s):
    sid, product, cw, cat, open_bag, scene, motion = s
    n_refs = len(refs_for(s))
    plural = "s" if n_refs > 1 else ""
    pre = (f"Use the attached product photo{plural} ONLY as the reference for the bag shape, proportions, "
           f"materials, colours, stitching and hardware. Do NOT copy the lighting, the plain background, the "
           f"clean edges or the polished studio product photo look of the attachment{plural}. Those are "
           f"catalogue images and the picture you produce must not resemble one. Create the following real "
           f"photograph instead.")
    if product == "colette":
        idb = colette_id(cw, open_bag)
    elif product == "margot":
        idb = margot_id(cw, open_bag)
    else:
        c_cw, m_cw = cw.split("+")
        idb = ("TWO bags appear in this scene. Follow both product truths exactly and never blend features "
               "between the two bags. FIRST BAG: " + colette_id(c_cw, open_bag) +
               " SECOND BAG: " + margot_id(m_cw, open_bag) +
               " The first attached photo is the felt tote, the second attached photo is the leather tote.")
    return "\n\n".join([pre, scene, idb, ANTIDRIFT + " " + FOOTER.format(surf=SURF[product])])


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
