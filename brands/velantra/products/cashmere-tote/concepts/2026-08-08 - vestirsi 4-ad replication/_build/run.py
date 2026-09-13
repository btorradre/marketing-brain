#!/usr/bin/env python3
"""Fire the three Seedance 2.5 ads for the Vestirsi replication set.

  python3 run.py upload          upload refs, cache urls
  python3 run.py fire AD1 ...    createTask for the named ads
  python3 run.py poll            poll all in-flight tasks, download finished
  python3 run.py balance
"""
import json, os, pathlib, subprocess, sys, time

HERE = pathlib.Path(__file__).parent
CONCEPT = HERE.parent
ROOT = pathlib.Path("/Users/brooksorradre2/Documents/marketing brain")
STATE = HERE / "state.json"

for line in (ROOT / ".env").read_text().splitlines():
    if "=" in line and not line.strip().startswith("#"):
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
KEY = os.environ["KIE_API_KEY"]

# ref order maps to @Image1..N
REFS = {
    "AD1": ["blair-identity.png", "colette-caramel-front.png", "colette-caramel-side.png"],
    "AD2": ["blair-identity.png", "colette-caramel-front.png", "colette-caramel-interior.png"],
    "AD3": ["blair-identity.png", "colette-caramel-front.png", "colette-caramel-interior.png"],
}
DUR = {"AD1": 25, "AD2": 23, "AD3": 30}


def load():
    return json.loads(STATE.read_text()) if STATE.exists() else {"uploads": {}, "tasks": {}}


def save(s):
    STATE.write_text(json.dumps(s, indent=2))


def curl(args, timeout=300):
    r = subprocess.run(["curl", "-s", "--max-time", str(timeout)] + args,
                       capture_output=True, text=True)
    return r.stdout


def balance():
    d = json.loads(curl(["https://api.kie.ai/api/v1/chat/credit",
                         "-H", f"Authorization: Bearer {KEY}"]))
    return float(d["data"])


def upload():
    s = load()
    for f in sorted({f for v in REFS.values() for f in v}):
        if f in s["uploads"]:
            print(f"  cached {f}")
            continue
        p = CONCEPT / "refs" / f
        out = curl(["https://kieai.redpandaai.co/api/file-stream-upload",
                    "-H", f"Authorization: Bearer {KEY}",
                    "-F", f"file=@{p}",
                    "-F", "uploadPath=images/velantra-colette",
                    "-F", f"fileName={f}"], timeout=600)
        try:
            url = json.loads(out)["data"]["downloadUrl"]
        except Exception:
            print(f"  FAIL {f}: {out[:300]}"); continue
        s["uploads"][f] = url
        print(f"  up {f} -> {url}")
        save(s)
    return s


def fire(names):
    s = load()
    for n in names:
        if s["tasks"].get(n, {}).get("taskId"):
            print(f"{n}: already fired {s['tasks'][n]['taskId']}"); continue
        prompt = (CONCEPT / "prompts" / f"{n}-seedance.txt").read_text().strip()
        urls = [s["uploads"][f] for f in REFS[n]]
        body = {"model": "bytedance/seedance-2-5", "input": {
            "prompt": prompt, "duration": DUR[n], "aspect_ratio": "9:16",
            "resolution": "720p", "generate_audio": True,
            "reference_image_urls": urls}}
        pf = HERE / f"_payload-{n}.json"; pf.write_text(json.dumps(body))
        out = curl(["https://api.kie.ai/api/v1/jobs/createTask",
                    "-H", f"Authorization: Bearer {KEY}",
                    "-H", "Content-Type: application/json",
                    "--data-binary", f"@{pf}"])
        try:
            d = json.loads(out)
        except Exception:
            print(f"{n}: unparseable {out[:300]}"); continue
        tid = (d.get("data") or {}).get("taskId")
        if not tid:
            print(f"{n}: REJECTED  {d.get('code')} {d.get('msg')}"); continue
        s["tasks"][n] = {"taskId": tid, "duration": DUR[n]}
        save(s)
        print(f"{n}: fired {tid}  ({DUR[n]}s, ~{63*DUR[n]}cr)")


def poll():
    s = load()
    done = True
    for n, t in s["tasks"].items():
        if t.get("file"):
            print(f"{n}: done -> {t['file']}"); continue
        out = curl([f"https://api.kie.ai/api/v1/jobs/recordInfo?taskId={t['taskId']}",
                    "-H", f"Authorization: Bearer {KEY}"])
        d = json.loads(out, strict=False)
        rec = d.get("data") or {}
        st = rec.get("state")
        if st == "success":
            urls = json.loads(rec["resultJson"])["resultUrls"]
            dest = CONCEPT / "output" / f"VEL-COL-{n}.mp4"
            dest.parent.mkdir(exist_ok=True)
            subprocess.run(["curl", "-sL", "-A", "Mozilla/5.0", urls[0], "-o", str(dest)])
            t["file"] = str(dest); t["credits"] = rec.get("creditsConsumed")
            save(s)
            print(f"{n}: SUCCESS -> {dest} ({rec.get('creditsConsumed')}cr)")
        elif st == "fail":
            print(f"{n}: FAILED {rec.get('failMsg')}")
        else:
            done = False
            print(f"{n}: {st}")
    return done


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "poll"
    if cmd == "balance":
        print(f"balance: {balance()}")
    elif cmd == "upload":
        upload()
    elif cmd == "fire":
        names = sys.argv[2:] or ["AD1", "AD2", "AD3"]
        print(f"balance before: {balance()}")
        fire(names)
    elif cmd == "poll":
        poll()
