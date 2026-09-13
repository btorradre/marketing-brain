#!/usr/bin/env python3
"""Generate the v4 22-visual set.

Reused shots are copied from the QA-passed originals. New shots go to GPT Image 2 i2i off the
caramel hero, except the colorway lineup which gets all three colorway refs wired in order.

Usage: gen_v4.py copy | fire [V03 ...] | poll | status
"""
import json, os, shutil, ssl, subprocess, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
M = json.load(open(os.path.join(HERE, "manifest.json")))
STATE = os.path.join(HERE, "state_v4.json")
SRC = os.path.join(ROOT, "assets", "keyframes")
OUT = os.path.join(ROOT, "assets", "visuals")
API = "https://api.kie.ai/api/v1/jobs"
UPLOAD = "https://kieai.redpandaai.co/api/file-stream-upload"
MODEL = "gpt-image-2-image-to-image"


def ctx():
    import certifi
    return ssl.create_default_context(cafile=certifi.where())


def key():
    for l in open("/Users/brooksorradre2/Documents/marketing brain/.env"):
        if l.startswith("KIE_API_KEY="):
            return l.strip().split("=", 1)[1]
    raise SystemExit("no KIE_API_KEY")


K = key()


def api(path, payload=None):
    data = json.dumps(payload).encode() if payload else None
    r = urllib.request.Request(API + path, data=data,
                               headers={"Authorization": f"Bearer {K}", "Content-Type": "application/json"})
    with urllib.request.urlopen(r, context=ctx(), timeout=120) as f:
        return json.loads(f.read().decode(), strict=False)


def st():
    return json.load(open(STATE)) if os.path.exists(STATE) else {"uploads": {}, "images": {}}


def save(s):
    json.dump(s, open(STATE, "w"), indent=1)


def upload(path):
    for a in range(4):
        if a:
            time.sleep(8 * a)
        o = subprocess.run(["curl", "-s", "-X", "POST", UPLOAD, "-H", f"Authorization: Bearer {K}",
                            "-F", f"file=@{path}", "-F", "uploadPath=velantra-onebag-v4",
                            "-F", f"fileName={int(time.time())}-{os.path.basename(path).replace(' ','_')}"],
                           capture_output=True, text=True)
        try:
            u = json.loads(o.stdout)["data"]["downloadUrl"]
            return u
        except Exception:
            continue
    raise RuntimeError(f"upload failed {path}")


def build_prompt(shot):
    return " ".join([shot["prompt"], M["product_lock"], M["flap_closed_pin"], M["style_line"]])


def cmd_copy():
    os.makedirs(OUT, exist_ok=True)
    for s in M["shots_v4"]:
        if "reuse" in s:
            shutil.copy2(os.path.join(SRC, f"{s['reuse']}.png"), os.path.join(OUT, f"{s['id']}.png"))
            print(f"{s['id']} <- {s['reuse']}.png")


def cmd_fire(ids):
    s = st()
    for name, path in M["refs"].items():
        if name not in s["uploads"]:
            s["uploads"][name] = upload(path)
            print(f"uploaded {name}")
            save(s)
    todo = [x for x in M["shots_v4"] if "prompt" in x and (not ids or x["id"] in ids)]
    for shot in todo:
        refs = ([s["uploads"]["caramel"], s["uploads"]["blue"], s["uploads"]["black"]]
                if shot.get("colorways") else [s["uploads"]["caramel"]])
        r = api("/createTask", {"model": MODEL, "input": {
            "prompt": build_prompt(shot), "input_urls": refs,
            "aspect_ratio": M["aspect_ratio"], "resolution": M["image_resolution"]}})
        if r.get("code") != 200:
            print(f"{shot['id']} CREATE FAIL: {r}")
            continue
        s["images"][shot["id"]] = {"taskId": r["data"]["taskId"], "state": "created"}
        print(f"{shot['id']} task {r['data']['taskId']}  refs={len(refs)}")
        save(s)


def cmd_poll():
    s = st()
    os.makedirs(OUT, exist_ok=True)
    pend = {k: v for k, v in s["images"].items() if v.get("state") not in ("success", "fail")}
    deadline = time.time() + 45 * 60
    while pend and time.time() < deadline:
        for sid in list(pend):
            try:
                d = (api(f"/recordInfo?taskId={s['images'][sid]['taskId']}").get("data") or {})
            except Exception as e:
                print(f"{sid} poll err {e}")
                continue
            s["images"][sid]["state"] = d.get("state")
            if d.get("state") == "success":
                urls = json.loads(d.get("resultJson") or "{}", strict=False).get("resultUrls") or []
                if urls:
                    dest = os.path.join(OUT, f"{sid}.png")
                    subprocess.run(["curl", "-sL", "--fail", "-A", "Mozilla/5.0", "-o", dest, urls[0]],
                                   check=True)
                    print(f"{sid} DONE")
                del pend[sid]
            elif d.get("state") == "fail":
                print(f"{sid} FAIL: {d.get('failMsg')}")
                del pend[sid]
            save(s)
        if pend:
            time.sleep(15)


def cmd_status():
    s = st()
    have = {f[:-4] for f in os.listdir(OUT)} if os.path.isdir(OUT) else set()
    for x in M["shots_v4"]:
        print(f" {x['id']} {'OK ' if x['id'] in have else '-- '} "
              f"{s['images'].get(x['id'],{}).get('state','reuse' if 'reuse' in x else '')}")
    print(f"{len(have)}/{len(M['shots_v4'])} present")


if __name__ == "__main__":
    c = sys.argv[1] if len(sys.argv) > 1 else "status"
    {"copy": lambda: cmd_copy(), "fire": lambda: cmd_fire(sys.argv[2:]),
     "poll": lambda: cmd_poll(), "status": lambda: cmd_status()}.get(c, lambda: print(__doc__))()
