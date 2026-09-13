#!/usr/bin/env python3
"""Stage 1: GPT Image 2 i2i keyframes on kie, Blair + the bag as refs."""
import json, os, pathlib, subprocess, sys, time

HERE = pathlib.Path(__file__).parent
KEYS = HERE / "ad4v2/keys"; KEYS.mkdir(parents=True, exist_ok=True)
STATE = HERE / "ad4v2/keys.json"
ROOT = pathlib.Path("/Users/brooksorradre2/Documents/marketing brain")
for l in (ROOT / ".env").read_text().splitlines():
    if "=" in l and not l.strip().startswith("#"):
        k, v = l.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
KEY = os.environ["KIE_API_KEY"]

sys.path.insert(0, str(HERE))
from ad4v2_shots import SHOTS, keyframe_prompt

REFS = json.loads((HERE / "state.json").read_text())["uploads"]
BLAIR = REFS["blair-identity.png"]
BAGF = REFS["colette-caramel-front.png"]
BAGS = REFS["colette-caramel-side.png"]


def curl(a, t=600):
    return subprocess.run(["curl", "-s", "--max-time", str(t)] + a,
                          capture_output=True, text=True).stdout


def load():
    return json.loads(STATE.read_text()) if STATE.exists() else {}


def save(s):
    STATE.write_text(json.dumps(s, indent=2))


def fire():
    s = load()
    for sh in SHOTS:
        sid = sh[0]
        if s.get(sid, {}).get("taskId"):
            continue
        body = {"model": "gpt-image-2-image-to-image", "input": {
            "prompt": keyframe_prompt(sh),
            "input_urls": [BLAIR, BAGF, BAGS],
            "aspect_ratio": "9:16", "resolution": "1K"}}
        pf = HERE / f"ad4v2/_k-{sid}.json"; pf.write_text(json.dumps(body))
        out = curl(["https://api.kie.ai/api/v1/jobs/createTask",
                    "-H", f"Authorization: Bearer {KEY}",
                    "-H", "Content-Type: application/json", "--data-binary", f"@{pf}"])
        d = json.loads(out)
        tid = (d.get("data") or {}).get("taskId")
        if not tid:
            print(f"{sid}: REJECT {d.get('code')} {d.get('msg')}"); continue
        s[sid] = {"taskId": tid}; save(s)
        print(f"{sid}: fired {tid}")


def poll():
    s = load(); pending = []
    for sid, t in s.items():
        if t.get("file"):
            continue
        d = json.loads(curl([f"https://api.kie.ai/api/v1/jobs/recordInfo?taskId={t['taskId']}",
                             "-H", f"Authorization: Bearer {KEY}"]), strict=False)
        rec = d.get("data") or {}
        st = rec.get("state")
        if st == "success":
            url = json.loads(rec["resultJson"])["resultUrls"][0]
            dest = KEYS / f"{sid}.png"
            subprocess.run(["curl", "-sL", "-A", "Mozilla/5.0", url, "-o", str(dest)])
            t["file"] = str(dest); save(s); print(f"{sid}: ok")
        elif st == "fail":
            print(f"{sid}: FAIL {rec.get('failMsg')}")
        else:
            pending.append(sid)
    return pending


if __name__ == "__main__":
    if sys.argv[1:] and sys.argv[1] == "poll":
        while True:
            p = poll()
            if not p:
                break
            print(f"  waiting on {len(p)}: {' '.join(p)}")
            time.sleep(20)
        print("all keyframes done")
    else:
        fire()
