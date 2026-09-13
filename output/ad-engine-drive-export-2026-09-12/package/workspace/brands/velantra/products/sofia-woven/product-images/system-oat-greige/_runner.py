#!/usr/bin/env python3
"""
Sofia Woven Tote -- oat-greige congruent product-image system runner.
GPT Image 2 image-to-image on kie.ai. 1:1, 2K.

Mirrors the Margot (Meridian) system: one master per shot-type on the
oat-greige #E7E3DB seamless, then recolored to every colorway.

SOURCE PROVENANCE RULE (DMCA):
  Only the CLEAN poolside statics + `straw birkin opened.png` may be used
  as i2i sources. The luxboattote compositions (handheld-front on white,
  coastal/hydrangea, dock-side) and every recolor of them are banned.

Usage:  python3 _runner.py jobs.json
"""
import base64, json, mimetypes, os, ssl, sys, time
from pathlib import Path

import certifi
import requests
from PIL import Image

os.environ.setdefault("SSL_CERT_FILE", certifi.where())

ROOT = Path("/Users/brooksorradre2/Documents/marketing brain")
OUT = Path(__file__).resolve().parent
CACHE = OUT / "_upload_cache.json"
TASKS = OUT / "_tasks_inflight.json"
PREP = OUT / "_prepped"
PREP.mkdir(exist_ok=True)

KIE = None
for line in (ROOT / ".env").read_text().splitlines():
    if line.startswith("KIE_API_KEY="):
        KIE = line.split("=", 1)[1].strip()
H = {"Authorization": f"Bearer {KIE}"}


def prep(src: Path) -> Path:
    """kie upload chokes on multi-MB PNG/webp -> ~1600px JPEG."""
    dst = PREP / (src.stem.replace(" ", "-") + ".jpg")
    if dst.exists():
        return dst
    im = Image.open(src).convert("RGB")
    if max(im.size) > 1600:
        im.thumbnail((1600, 1600), Image.LANCZOS)
    im.save(dst, "JPEG", quality=92)
    return dst


def _retry(fn, tries=5, what=""):
    """kie's upload/createTask endpoints drop connections under batch load."""
    for i in range(tries):
        try:
            return fn()
        except Exception as e:
            if i == tries - 1:
                raise
            print(f"  retry {i+1}/{tries-1} {what}: {type(e).__name__}")
            time.sleep(4 * (i + 1))


def upload(path: Path) -> str:
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    key = str(path)
    if key in cache:
        return cache[key]
    p = prep(path)
    mime = mimetypes.guess_type(p.name)[0] or "image/jpeg"

    def _post():
        with open(p, "rb") as fh:
            r = requests.post(
                "https://kieai.redpandaai.co/api/file-stream-upload",
                headers=H,
                files={"file": (p.name, fh, mime)},
                data={"uploadPath": "images/velantra-sofia", "fileName": p.name},
                timeout=180,
            )
        r.raise_for_status()
        return r

    r = _retry(_post, what=f"upload {p.name}")
    url = r.json()["data"]["downloadUrl"]
    cache[key] = url
    CACHE.write_text(json.dumps(cache, indent=2))
    print(f"  uploaded {p.name}")
    return url


def create(prompt: str, urls: list[str]) -> str:
    def _post():
        r = requests.post(
            "https://api.kie.ai/api/v1/jobs/createTask",
            headers={**H, "Content-Type": "application/json"},
            json={
                "model": "gpt-image-2-image-to-image",
                "input": {
                    "prompt": prompt,
                    "input_urls": urls,
                    "aspect_ratio": "1:1",
                    "resolution": "2K",
                },
            },
            timeout=120,
        )
        r.raise_for_status()
        return r

    d = _retry(_post, what="createTask").json()
    if not d.get("data", {}).get("taskId"):
        raise RuntimeError(d)
    return d["data"]["taskId"]


def poll(task_id: str, timeout=900):
    t0 = time.time()
    while time.time() - t0 < timeout:
        r = requests.get(
            "https://api.kie.ai/api/v1/jobs/recordInfo",
            headers=H, params={"taskId": task_id}, timeout=60,
        )
        d = json.loads(r.text, strict=False)["data"]
        st = d.get("state")
        if st == "success":
            return json.loads(d["resultJson"], strict=False)["resultUrls"][0]
        if st == "fail":
            raise RuntimeError(d.get("failMsg") or d)
        time.sleep(6)
    raise TimeoutError(task_id)


def download(url: str, dst: Path):
    def _get():
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=300)
        r.raise_for_status()
        return r

    dst.write_bytes(_retry(_get, tries=6, what=f"download {dst.name}").content)


def run(jobs):
    # taskIds persist so a failed DOWNLOAD never costs a regeneration
    tasks = json.loads(TASKS.read_text()) if TASKS.exists() else {}
    pending = []
    for j in jobs:
        dst = OUT / j["out"]
        if dst.exists() and not j.get("force"):
            print(f"skip (exists) {j['out']}")
            continue
        if j["out"] in tasks and not j.get("force"):
            print(f"resume {j['out']}  {tasks[j['out']]}")
            pending.append((j, tasks[j["out"]], dst))
            continue
        urls = [upload(Path(s)) for s in j["refs"]]
        tid = create(j["prompt"], urls)
        print(f"queued {j['out']}  {tid}")
        tasks[j["out"]] = tid
        TASKS.write_text(json.dumps(tasks, indent=2))
        pending.append((j, tid, dst))
        time.sleep(1.5)

    ok, bad = [], []
    for j, tid, dst in pending:
        try:
            url = poll(tid)
            download(url, dst)
            print(f"DONE  {j['out']}")
            ok.append(j["out"])
            tasks.pop(j["out"], None)
            TASKS.write_text(json.dumps(tasks, indent=2))
        except Exception as e:
            print(f"FAIL  {j['out']}: {e}")
            bad.append((j["out"], str(e)))
        time.sleep(2)
    print(f"\n{len(ok)} ok, {len(bad)} failed")
    for name, err in bad:
        print(f"  {name}: {err[:200]}")


if __name__ == "__main__":
    run(json.loads(Path(sys.argv[1]).read_text()))
