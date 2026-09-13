#!/usr/bin/env python3
"""Stage 2: animate each keyframe with Google Omni (Gemini Interactions API).

curl only — urllib SSL fails against generativelanguage on this machine.
Handle comes back as `id`, not `name`. Result is base64 mp4 in the step whose
type == "video" (never steps[-1], steps[0] is the request echo).
"""
import base64, concurrent.futures as cf, json, os, pathlib, subprocess, sys, time

HERE = pathlib.Path(__file__).parent
KEYS = HERE / "ad4v2/keys"
CLIPS = HERE / "ad4v2/clips"; CLIPS.mkdir(parents=True, exist_ok=True)
TMP = HERE / "ad4v2/tmp"; TMP.mkdir(parents=True, exist_ok=True)
STATE = HERE / "ad4v2/omni.json"
ROOT = pathlib.Path("/Users/brooksorradre2/Documents/marketing brain")
for l in (ROOT / ".env").read_text().splitlines():
    if "=" in l and not l.strip().startswith("#"):
        k, v = l.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
K = os.environ.get("GEMINI_OMNI_API_KEY") or os.environ["GEMINI_API_KEY"]
B = "https://generativelanguage.googleapis.com/v1beta"

sys.path.insert(0, str(HERE))
from ad4v2_shots import SHOTS, motion_prompt


def jpeg(png):
    out = TMP / (png.stem + ".jpg")
    if not out.exists():
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(png),
                        "-vf", "scale=720:1280", "-q:v", "3", str(out)], check=True)
    return out


def launch(shot):
    sid = shot[0]
    img = jpeg(KEYS / f"{sid}.png")
    payload = {"model": "models/gemini-omni-flash-preview", "background": True,
               "generation_config": {"video_config": {}},
               "input": [
                   {"type": "image", "data": base64.b64encode(img.read_bytes()).decode(),
                    "mime_type": "image/jpeg"},
                   {"type": "text", "text": motion_prompt(shot) + "\n\nVertical 9:16."},
               ]}
    pf = TMP / f"p-{sid}.json"; pf.write_text(json.dumps(payload))
    out = subprocess.run(["curl", "-s", "--max-time", "300", f"{B}/interactions?key={K}",
                          "-H", "Content-Type: application/json",
                          "--data-binary", f"@{pf}"], capture_output=True, text=True).stdout
    try:
        d = json.loads(out)
    except Exception:
        return sid, None, out[:200]
    if "id" not in d:
        return sid, None, json.dumps(d)[:250]
    return sid, d["id"], None


def fetch(sid, iid):
    for _ in range(60):
        out = subprocess.run(["curl", "-s", "--max-time", "180", f"{B}/interactions/{iid}?key={K}"],
                             capture_output=True, text=True).stdout
        try:
            d = json.loads(out)
        except Exception:
            time.sleep(10); continue
        if d.get("error"):
            # terminal, and it comes back with no `status` at all — do not keep polling
            print(f"  {sid} REJECTED: {d['error'].get('message', '')[:300]}")
            (TMP / f"error-{sid}.json").write_text(json.dumps(d, indent=1)[:100000])
            return None
        if d.get("status") in ("completed", "succeeded"):
            for st in d.get("steps", []):
                for c in st.get("content", []):
                    if c.get("type") == "video":
                        dest = CLIPS / f"{sid}.mp4"
                        dest.write_bytes(base64.b64decode(c["data"]))
                        return dest
            kinds = [c.get("type") for st in d.get("steps", []) for c in st.get("content", [])]
            txt = " | ".join(c.get("text", "")[:300] for st in d.get("steps", [])
                             for c in st.get("content", []) if c.get("type") == "text")
            print(f"  {sid} completed with NO video. content types={kinds}")
            if txt:
                print(f"  {sid} model said: {txt[:500]}")
            (TMP / f"novideo-{sid}.json").write_text(json.dumps(d, indent=1)[:200000])
            return None
        if d.get("status") in ("failed", "cancelled"):
            print(f"  {sid} {d.get('status')}: {json.dumps(d)[:400]}")
            return None
        time.sleep(10)
    return None


def load():
    return json.loads(STATE.read_text()) if STATE.exists() else {}


def save(s):
    STATE.write_text(json.dumps(s, indent=2))


def run(only=None):
    s = load()
    todo = [sh for sh in SHOTS
            if (only is None or sh[0] in only) and not (CLIPS / f"{sh[0]}.mp4").exists()]
    print(f"{len(todo)} to animate")
    with cf.ThreadPoolExecutor(max_workers=5) as ex:
        for sid, iid, err in ex.map(launch, todo):
            if err:
                print(f"  {sid} LAUNCH FAIL {err}")
            else:
                s[sid] = iid; save(s); print(f"  {sid} -> {iid}")
    with cf.ThreadPoolExecutor(max_workers=5) as ex:
        futs = {ex.submit(fetch, sid, iid): sid for sid, iid in s.items()
                if not (CLIPS / f"{sid}.mp4").exists()}
        for f in cf.as_completed(futs):
            sid = futs[f]
            r = f.result()
            print(f"  {sid}: {'ok ' + r.name if r else 'NO VIDEO'}")


if __name__ == "__main__":
    run(sys.argv[1:] or None)
