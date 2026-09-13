#!/usr/bin/env python3
"""Sofia per-colorway product shots — oat-greige seamless system via kie GPT Image 2 i2i.

Master is derived ONLY from provenance-clean sources (hero-studio-plinth / straw birkin opened).
Never seed from shot1_handheld_front / shot2_coastal_outdoor / shot3_dock_side / black-tote-*.
"""
import json, os, sys, time, mimetypes, urllib.request, subprocess

KEY = os.environ["KIE_API_KEY"]
OUT = "/Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/straw-birkin/product-images/system-oat-greige"
VAULT = "/Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/straw-birkin"
os.makedirs(OUT, exist_ok=True)

GREIGE = "#E7E3DB"

MASTER_SRC = f"{VAULT}/product-images/straw birkin/homepage-stills/hero-studio-plinth.jpeg"
INTERIOR_SRC = f"{VAULT}/product-images/straw birkin/straw birkin opened.png"

MASTER_PROMPT = (
    "Edit this image. Keep the bag EXACTLY as it is — identical woven straw body, leather flap, "
    "crossed front straps, rolled top handles, stitching, proportions, angle and colour. "
    f"Change ONLY the setting: remove the plinth and any props, and place the bag on one continuous "
    f"seamless sweep of soft warm pale oat-greige {GREIGE} with no horizon line and no visible floor edge. "
    "Soft even diffused studio light, exactly ONE soft contact shadow directly under the bag. "
    "Re-frame to a vertical portrait composition with the bag centred and filling about 70% of the frame "
    "height. Photographic studio packshot. No text, no logos, no props, no hands, no people."
)

RECOLOR = (
    "Edit this image. Change ONLY the colour of the LEATHER parts (the flap, the crossed front straps, "
    "the top handles and the leather trim) to {desc}. "
    "Keep the natural straw woven body its original undyed straw colour. "
    "Preserve EXACTLY: composition, framing, bag shape and proportions, angle, stitching, the oat-greige "
    "seamless background, lighting and the contact shadow. Do not move or resize the bag. "
    "This is a pure colour swap — nothing else may change."
)

INTERIOR_RECOLOR = (
    "Edit this image. Change ONLY the colour of the OUTER leather (flap, straps, handles, trim) to {desc}. "
    "Keep the interior lining, the items inside, the straw weave, the surface, composition, angle, "
    "framing and lighting EXACTLY as they are. Pure colour swap only."
)

COLORS = [
    ("caramel",          "Caramel",          "a warm mid caramel tan leather"),
    ("sky-blue",         "Sky Blue",         "a soft mid sky blue leather"),
    ("lightning-orange", "Lightning Orange", "a vivid warm orange leather"),
    ("light-chocolate",  "Light Chocolate",  "a medium warm chocolate brown leather"),
    ("lady-pink",        "Lady Pink",        "a bright fuchsia pink leather"),
    ("cream",            "Cream",            "a soft off-white cream leather"),
    ("sunny-yellow",     "Sunny Yellow",     "a bright sunny yellow leather"),
    ("caban-black",      "Caban Black",      "a deep true black leather"),
]


def api(method, path, payload=None):
    url = f"https://api.kie.ai{path}"
    data = json.dumps(payload).encode() if payload else None
    req = urllib.request.Request(url, data=data, method=method,
                                 headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read(), strict=False)


def upload(path):
    """kie temp upload; downscale big files first (upload chokes on multi-MB PNGs)."""
    small = f"/tmp/kie_{os.path.basename(path).replace(' ','_').rsplit('.',1)[0]}.jpg"
    subprocess.run(["sips", "-Z", "1500", "-s", "format", "jpeg", path, "--out", small],
                   check=True, capture_output=True)
    # the upload host 403s urllib; curl works
    out = subprocess.run(
        ["curl", "-s", "-X", "POST", "https://kieai.redpandaai.co/api/file-stream-upload",
         "-H", f"Authorization: Bearer {KEY}", "-F", f"file=@{small}",
         "-F", "uploadPath=images/user-uploads"],
        check=True, capture_output=True, text=True).stdout
    return json.loads(out)["data"]["downloadUrl"]


def gen(prompt, input_urls, label, dest):
    t = api("POST", "/api/v1/jobs/createTask", {
        "model": "gpt-image-2-image-to-image",
        "input": {"prompt": prompt, "input_urls": input_urls,
                  "aspect_ratio": "2:3", "resolution": "2K"}})
    tid = t["data"]["taskId"]
    for _ in range(90):
        time.sleep(6)
        r = api("GET", f"/api/v1/jobs/recordInfo?taskId={tid}")
        st = r["data"]["state"]
        if st == "success":
            u = json.loads(r["data"]["resultJson"], strict=False)["resultUrls"][0]
            subprocess.run(["curl", "-sL", "-A", "Mozilla/5.0", u, "-o", dest], check=True)
            print(f"  OK  {label} -> {os.path.basename(dest)}", flush=True)
            return dest
        if st == "fail":
            print(f"  FAIL {label}: {r['data'].get('failMsg')}", flush=True)
            return None
    print(f"  TIMEOUT {label}", flush=True)
    return None


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "all"

    if which in ("master", "all"):
        print("=== MASTER (oat-greige restyle of the clean studio plinth shot) ===", flush=True)
        gen(MASTER_PROMPT, [upload(MASTER_SRC)], "master", f"{OUT}/sofia-master-oat-greige.png")

    if which in ("hero", "all"):
        master = f"{OUT}/sofia-master-oat-greige.png"
        if not os.path.exists(master):
            sys.exit("master missing — run `master` first")
        mu = upload(master)
        print("=== HERO PER COLORWAY ===", flush=True)
        for h, label, desc in COLORS:
            d = f"{OUT}/sofia-{h}-hero.png"
            if os.path.exists(d):
                print(f"  skip {label} (exists)", flush=True); continue
            gen(RECOLOR.format(desc=desc), [mu], label, d)

    if which in ("interior", "all"):
        iu = upload(INTERIOR_SRC)
        print("=== INTERIOR PER COLORWAY ===", flush=True)
        for h, label, desc in COLORS:
            d = f"{OUT}/sofia-{h}-interior.png"
            if os.path.exists(d):
                print(f"  skip {label} (exists)", flush=True); continue
            gen(INTERIOR_RECOLOR.format(desc=desc), [iu], label, d)


if __name__ == "__main__":
    main()
