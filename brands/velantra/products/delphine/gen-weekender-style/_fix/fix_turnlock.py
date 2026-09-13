#!/usr/bin/env python3
"""THE DELPHINE — turn-lock artifact repair on the three -04-hardware macros.

DEFECT (2026-08-16, caught by Brooks). All three hardware macros
(LC/DC/AG-04-hardware.png) render the front turn-lock wrong in the identical
way: the oval brass plate carries TWO long detached pill-shaped bars floating
over it (a tall pale/chrome one on the right, a shorter brass one on the left)
with a dark void and an exposed post between them. The real lock is a single
compact brass toggle on a solid oval plate — visible and correct in every other
frame of the set (AG-02-threequarter, all three -01-front shots) and in the
supplier photography at real-product/ref-front-clean.jpg.

This is the macro failure mode from [[feedback_seedance_flap_survives_medium_breaks_macro]]:
the lock survives at medium distance and shatters when the crop goes close.

FIX = single-variable i2i edit. Two references per job:
  1. the artifacted pick itself  -> everything that must stay pixel-identical
  2. refs/turnlock-correct.png   -> a 5x crop of the CORRECT lock from AG-02
Only the lock changes. Everything else is pinned.

Transport is curl, not urllib — this Python has no root-cert bundle and urllib
dies on CERTIFICATE_VERIFY_FAILED against api.kie.ai
(law from the vestirsi statics run, PRODUCT-TRUTH / project_delphine_vestirsi_statics).

Idempotent: skips any output that already exists. Rejects land in _fix/raw/,
picks are promoted by hand after QA.
"""
import json, os, time, subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
VAULT = "/Users/brooksorradre2/Documents/marketing brain"
PICKS = os.path.join(os.path.dirname(ROOT), "picks")
REFS = os.path.join(ROOT, "refs")
OUT = os.path.join(ROOT, "raw")
API = "https://api.kie.ai/api/v1"
UPLOAD = "https://kieai.redpandaai.co/api/file-stream-upload"

KEY = None
with open(os.path.join(VAULT, ".env")) as f:
    for line in f:
        if line.startswith("KIE_API_KEY="):
            KEY = line.split("=", 1)[1].strip()
assert KEY, "KIE_API_KEY not found"
H = {"Authorization": f"Bearer {KEY}"}

VARIANTS = 2          # two rolls per colorway, pick the better
ATTEMPTS = 3          # GPT Image 2's filter refuses intermittently on identical input

JOBS = [
    ("LC-04-hardware", "warm chestnut brown leather over cream ivory canvas"),
    ("DC-04-hardware", "very dark espresso brown leather over cream ivory canvas"),
    ("AG-04-hardware", "warm chestnut brown leather over deep muted olive green canvas"),
]

# --- THE ONE THING THAT CHANGES ---------------------------------------------
# Described positively AND negatively. The negative half matters: the model
# produced the long floating pills three times across three colorways, so the
# shape has to be ruled out by name, not just replaced.
LOCK = (
    "The ONLY change you make is the gold turn lock on the front flap. In the first image that turn "
    "lock is malformed and must be rebuilt so that it matches the turn lock in the second image "
    "exactly. The correct turn lock is one upright oval brass plate lying flat and flush against the "
    "leather, smooth and unbroken across its whole face, with one small domed brass screw head near "
    "the top of the oval and one near the bottom. At the centre of the oval a short round brass boss "
    "stands slightly proud of the plate, and across that boss sits ONE single short rounded brass "
    "turning bar, compact and centred, no longer than about one third of the height of the oval "
    "plate. The whole fitting is one continuous piece of the same warm brass gold as the rest of the "
    "hardware in the frame. "
    "The rebuilt lock must NOT contain any of the following: a second bar, a duplicated toggle, any "
    "long pill or capsule shaped bar, any bar that floats detached from the plate or casts its own "
    "separate shadow, any bar that runs past the edge of the oval plate, a dark hole, a slot, a "
    "keyhole, an open gap in the plate, an exposed post or screw thread, and no silver, chrome, "
    "nickel or pale grey metal anywhere. Brass gold only, one bar only, plate solid."
)

# --- EVERYTHING THAT MUST NOT MOVE ------------------------------------------
PRESERVE = (
    "This is a single element repair of a finished photograph, not a new photograph. Reproduce the "
    "first image pixel for pixel everywhere outside the oval turn lock plate. Keep the identical "
    "crop, framing, camera angle, focal length, depth of field and the exact same areas in and out "
    "of focus. Keep the leather grain, every crease, every stitch line and every stitch hole, the "
    "canvas weave, the colour, the warmth and the contrast exactly as they are. Keep the long gold "
    "strap plate with its oblong slot and its two domed rivets, the leather clochette tag and its "
    "stitching, the leather strap crossing the frame, the two gold posts at the top of the frame and "
    "the leather flap tabs all in exactly their current position, size, angle and finish. Keep the "
    "lighting direction, every highlight, every reflection and every shadow, including the shadows "
    "cast onto the canvas, unchanged. Do not recompose, do not re-light, do not zoom, do not rotate, "
    "do not clean up, do not sharpen and do not restyle. Nothing moves except the malformed lock."
)

ANTI_CGI = (
    "The result is a real photograph of a real leather bag shot on a full frame camera with a macro "
    "lens. Real leather grain with uneven natural creasing, real brass with slightly uneven polish "
    "and faint fine surface marks, real soft daylight falloff, real film grain. It is not a render, "
    "not a 3D model, not a CGI product visualisation, not Octane, Blender, Cinema 4D or any game "
    "engine. No perfect bilateral symmetry, no plastic sheen, no waxy surfaces, no flawless edges."
)


def prompt(material):
    return (
        f"Edit the first image. It is a macro photograph of a small structured top handle handbag in "
        f"{material}, cropped close on the front flap and its gold fittings. {LOCK} {PRESERVE} {ANTI_CGI}"
    )


def api(url, payload=None, headers=None):
    cmd = ["curl", "-s", "--max-time", "120", url]
    for k, v in (headers or {}).items():
        cmd += ["-H", f"{k}: {v}"]
    if payload is not None:
        cmd += ["-H", "Content-Type: application/json", "-d", json.dumps(payload)]
    for attempt in range(4):
        out = subprocess.run(cmd, capture_output=True, text=True)
        try:
            return json.loads(out.stdout, strict=False)
        except Exception as e:
            if attempt == 3:
                raise RuntimeError(f"{url} -> {(out.stdout or out.stderr)[:300]}") from e
            print(f"  retry {attempt+1}: {e}", flush=True)
            time.sleep(3 * (attempt + 1))


def fetch(url, dest):
    out = subprocess.run(["curl", "-s", "-L", "--max-time", "300",
                          "-A", "Mozilla/5.0", "-o", dest, url],
                         capture_output=True, text=True)
    if out.returncode != 0 or not os.path.exists(dest) or os.path.getsize(dest) < 1024:
        raise RuntimeError(f"download failed: {url} ({out.stderr[:200]})")
    return os.path.getsize(dest)


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
             "-F", "uploadPath=delphine-turnlock-fix",
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


def submit(refs, material):
    payload = {"model": "gpt-image-2-image-to-image",
               "input": {"prompt": prompt(material),
                         "input_urls": refs,
                         "aspect_ratio": "1:1",
                         "resolution": "2K"}}
    d = api(f"{API}/jobs/createTask", payload, H)
    if d.get("code") != 200:
        payload["input"]["resolution"] = "1K"
        d = api(f"{API}/jobs/createTask", payload, H)
    assert d.get("code") == 200, f"createTask failed: {d}"
    return d["data"]["taskId"]


def main():
    os.makedirs(OUT, exist_ok=True)
    lock_url = upload(os.path.join(REFS, "turnlock-correct.png"))

    spec, pending, tries = {}, {}, {}
    for base, material in JOBS:
        src = upload(os.path.join(PICKS, f"{base}.png"))
        for v in range(1, VARIANTS + 1):
            name = f"{base}-v{v}"
            if os.path.exists(os.path.join(OUT, f"{name}.png")):
                print(f"{name}: exists, skip", flush=True)
                continue
            spec[name] = ([src, lock_url], material)
            tries[name] = 1
            pending[name] = submit([src, lock_url], material)
            print(f"{name}: task {pending[name]}", flush=True)

    if not pending:
        print("nothing to do", flush=True)
        return

    deadline = time.time() + 2700
    while pending and time.time() < deadline:
        time.sleep(15)
        for name, tid in list(pending.items()):
            d = api(f"{API}/jobs/recordInfo?taskId={tid}", None, H)
            st = (d.get("data") or {}).get("state")
            if st == "success":
                rj = json.loads(d["data"]["resultJson"], strict=False)
                size = fetch(rj["resultUrls"][0], os.path.join(OUT, f"{name}.png"))
                print(f"{name}: DONE ({size//1024} KB)", flush=True)
                del pending[name]
            elif st == "fail":
                print(f"{name}: attempt {tries[name]} failed: {(d.get('data') or {}).get('failMsg')}", flush=True)
                del pending[name]
                refs, material = spec[name]
                if tries[name] < ATTEMPTS:
                    tries[name] += 1
                    pending[name] = submit(refs, material)
                    print(f"{name}: retry task {pending[name]} (attempt {tries[name]})", flush=True)
                else:
                    print(f"{name}: GIVING UP", flush=True)
    if pending:
        print(f"TIMEOUT still pending: {list(pending)}", flush=True)
    done = sorted(f[:-4] for f in os.listdir(OUT) if f.endswith(".png"))
    print(f"complete: {len(done)} -> {done}", flush=True)


if __name__ == "__main__":
    main()
