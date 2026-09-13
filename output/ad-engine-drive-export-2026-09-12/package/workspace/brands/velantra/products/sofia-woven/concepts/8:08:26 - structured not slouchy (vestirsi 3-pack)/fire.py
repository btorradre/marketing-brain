#!/usr/bin/env python3
"""
Fires the 3 Sofia Seedance 2.5 replications. One pass each, no chaining.

    python3 fire.py            # fire all three
    python3 fire.py ALLEY      # fire one

Checks the credit balance before each createTask, because 2.5 hard-rejects
on an insufficient balance rather than queueing.
"""
import functools, json, os, ssl, sys, time, urllib.request, certifi

# Unbuffered, so a backgrounded run streams progress instead of going dark
# until it exits. Learned the hard way on the first fire, 2026-08-08.
print = functools.partial(print, flush=True)

VAULT = "/Users/brooksorradre2/Documents/marketing brain"
HERE = os.path.dirname(os.path.abspath(__file__))
KIE = "https://api.kie.ai/api/v1"
CTX = ssl.create_default_context(cafile=certifi.where())

# Sofia caramel hero, uploaded 2026-08-08. Re-upload if this 404s.
PRODUCT_REF = "https://tempfile.redpandaai.co/kieai/706342/velantra/sofia/1786256948632-k1iukj075f.png"

JOBS = {
    "ALLEY":   ("VEL-SOFIA-ALLEY-01",   25),
    "LANE":    ("VEL-SOFIA-LANE-02",    23),
    "QUALITY": ("VEL-SOFIA-QUALITY-03", 30),
}


def key():
    for line in open(os.path.join(VAULT, ".env")):
        if line.startswith("KIE_API_KEY="):
            return line.split("=", 1)[1].strip()
    sys.exit("no KIE_API_KEY")


K = key()
HDR = {"Authorization": f"Bearer {K}", "Content-Type": "application/json"}


def get(url):
    r = urllib.request.Request(url, headers=HDR)
    return json.load(urllib.request.urlopen(r, context=CTX, timeout=60))


def post(url, body):
    r = urllib.request.Request(url, data=json.dumps(body).encode(), headers=HDR)
    return json.load(urllib.request.urlopen(r, context=CTX, timeout=120))


def credits():
    return get(f"{KIE}/chat/credit")["data"]


def fire(name, seconds):
    prompt = open(os.path.join(HERE, "prompts", f"{name}.txt"), encoding="utf-8").read()
    need = 63 * seconds
    bal = credits()
    if bal < need:
        print(f"  SKIP {name}: needs {need}, balance {bal:.0f}")
        return None
    res = post(f"{KIE}/jobs/createTask", {
        "model": "bytedance/seedance-2-5",
        "input": {
            "prompt": prompt,
            "duration": seconds,
            "aspect_ratio": "9:16",
            "resolution": "720p",
            "generate_audio": True,
            "reference_image_urls": [PRODUCT_REF],
        },
    })
    tid = (res.get("data") or {}).get("taskId")
    print(f"  {name}: {seconds}s, {need}cr -> {tid or res}")
    return tid


def poll(tasks):
    done = {}
    while len(done) < len(tasks):
        for name, tid in tasks.items():
            if name in done:
                continue
            d = get(f"{KIE}/jobs/recordInfo?taskId={tid}").get("data") or {}
            st = d.get("state")
            if st == "success":
                url = json.loads(d.get("resultJson") or "{}").get("resultUrls", [None])[0]
                done[name] = url
                print(f"  DONE {name}: {url}")
            elif st == "fail":
                done[name] = None
                print(f"  FAIL {name}: {d.get('failMsg')}")
        if len(done) < len(tasks):
            time.sleep(20)
    return done


if __name__ == "__main__":
    want = sys.argv[1:] or list(JOBS)
    print(f"balance: {credits():.0f} credits")
    tasks = {}
    for w in want:
        name, secs = JOBS[w.upper()]
        tid = fire(name, secs)
        if tid:
            tasks[name] = tid
    if tasks:
        out = poll(tasks)
        json.dump(out, open(os.path.join(HERE, "results.json"), "w"), indent=2)
        print(f"\nwrote results.json")
