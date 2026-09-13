"""Step 1 — GPT Image 2 keyframes on kie.ai. i2i from the Light Chocolate closed hero."""
import base64, json, os, subprocess, sys, time, pathlib

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from scenes import SCENES

KEY = os.environ["KIE_API_KEY"]
OUT = HERE / "keyframes"; OUT.mkdir(exist_ok=True)
PROD = pathlib.Path(os.path.expanduser(
    "~/Documents/marketing brain/brands/velantra/products/weekender"))
HERO = PROD / "product-images/product images/light chocolate 1.webp"
# Open-bag i2i uses the skill's validated pair: a still from the Brooks-approved fold-back
# clip for the mechanism, plus light chocolate 4 for material identity. The closed hero is
# deliberately NOT wired here — it is what reconstructs the phantom front flap.
OPEN_CLIP = PROD / "broll/Open_bag_packed_for_weekend_202607111429.mp4"
OPEN_ALT = PROD / "product-images/product images/light chocolate 4.webp"


def sh(args):
    return subprocess.run(args, capture_output=True, text=True).stdout


def upload(path, tag, ss=None):
    """kie temp file upload -> public URL (expires, re-upload per run)."""
    cache = HERE / f".url_{tag}"
    if cache.exists():
        u, ts = cache.read_text().split("\n")
        if time.time() - float(ts) < 6 * 3600:
            return u
    png = HERE / ".tmp" / f"{tag}.png"
    png.parent.mkdir(exist_ok=True)
    args = ["ffmpeg", "-v", "error"]
    if ss is not None:
        args += ["-ss", str(ss)]
    subprocess.run(args + ["-i", str(path), "-frames:v", "1", "-y", str(png)], check=True)
    r = sh(["curl", "-s", "-X", "POST", "https://kieai.redpandaai.co/api/file-stream-upload",
            "-H", f"Authorization: Bearer {KEY}", "-F", f"file=@{png}",
            "-F", "uploadPath=velantra/girlmath"])
    url = json.loads(r)["data"]["downloadUrl"]
    cache.write_text(f"{url}\n{time.time()}")
    return url


def create(model, inp):
    r = sh(["curl", "-s", "-X", "POST", "https://api.kie.ai/api/v1/jobs/createTask",
            "-H", f"Authorization: Bearer {KEY}", "-H", "Content-Type: application/json",
            "-d", json.dumps({"model": model, "input": inp})])
    d = json.loads(r, strict=False)
    if d.get("code") != 200:
        raise RuntimeError(f"createTask failed: {r[:400]}")
    return d["data"]["taskId"]


def poll(tid, timeout=900):
    t0 = time.time()
    while time.time() - t0 < timeout:
        r = sh(["curl", "-s", f"https://api.kie.ai/api/v1/jobs/recordInfo?taskId={tid}",
                "-H", f"Authorization: Bearer {KEY}"])
        d = json.loads(r, strict=False)["data"]
        st = d.get("state")
        if st == "success":
            return json.loads(d["resultJson"], strict=False)["resultUrls"][0]
        if st == "fail":
            raise RuntimeError(f"task {tid} failed: {d.get('failMsg')}")
        time.sleep(10)
    raise TimeoutError(tid)


VARIANTS = 3  # house rule: never ship the first roll, generate 3 and pick the clean one


def main():
    only = sys.argv[1:] or [s["id"] for s in SCENES]
    hero = upload(HERO, "hero")
    refs_open = None
    if any(s.get("refs") == "open" for s in SCENES if s["id"] in only):
        refs_open = [upload(OPEN_CLIP, "openclip", ss=6.5), upload(OPEN_ALT, "openalt")]
    tasks = {}
    for s in SCENES:
        if s["id"] not in only:
            continue
        for v in range(1, VARIANTS + 1):
            key = f"{s['id']}-v{v}"
            dst = OUT / f"KF-{key}.png"
            if dst.exists():
                print(f"[{key}] exists, skip", flush=True); continue
            if s["i2i"]:
                urls = refs_open if s.get("refs") == "open" else [hero]
                model, inp = "gpt-image-2-image-to-image", {
                    "prompt": s["keyframe"], "input_urls": urls,
                    "aspect_ratio": "9:16", "resolution": "2K"}
            else:
                model, inp = "gpt-image-2-text-to-image", {
                    "prompt": s["keyframe"], "aspect_ratio": "9:16", "resolution": "2K"}
            # kie returns "Internal Error" on a large fraction of calls regardless of pacing.
            # Failed tasks are not charged, so the fix is simply to keep asking.
            for attempt in range(1, 7):
                try:
                    url = poll(create(model, inp))
                    subprocess.run(["curl", "-sL", "-A", "Mozilla/5.0", url, "-o", str(dst)],
                                   check=True)
                    print(f"[{key}] saved ({dst.stat().st_size//1024}kb)", flush=True)
                    break
                except Exception as e:
                    print(f"[{key}] attempt {attempt}: {str(e)[:90]}", flush=True)
                    time.sleep(6)
            else:
                print(f"[{key}] GAVE UP", flush=True)


if __name__ == "__main__":
    main()
