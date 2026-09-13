#!/usr/bin/env python3
"""adv2 reviewer + commenter profile photos. Square casual snapshots, GPT Image 2 on kie.ai.

Usage: kie_avatars.py gen | poll
"""
import json, os, ssl, subprocess, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "images", "avatars"))
STATE_PATH = os.path.join(HERE, "state_avatars.json")
VAULT = "/Users/brooksorradre2/Documents/marketing brain"
API = "https://api.kie.ai/api/v1/jobs"
T2I = "gpt-image-2-text-to-image"
VARIANTS = 2
KEY = None

BASE = (
    "A casual square profile photo of the kind an ordinary person uses on Facebook. Head and "
    "shoulders, centred, looking at the camera, a small natural closed-mouth or slight smile. "
    "Shot on a phone by themselves or a family member in an everyday place: a kitchen, a porch, a "
    "living room, a car, a back yard. Ordinary available light only. "
)
FOOT = (
    "The face must look like a real, unremarkable person of this exact age: visible pores, real skin "
    "texture, uneven tone, age spots, fine lines, flyaway hair, slightly imperfect teeth, no makeup or "
    "very little. ABSOLUTELY REFUSE: 3D render, CGI, stock photography, model casting, headshot "
    "photography, studio lighting, softbox, ring light, beauty retouching, skin smoothing, HDR, "
    "airbrushing, glamour styling, or anyone who looks professionally photographed. Include mild "
    "sensor noise, slightly soft focus and imperfect phone-camera framing."
)

PEOPLE = {
    "steve":    "A 62-year-old white American man with thinning grey hair, a lined weathered face, reading glasses pushed up on his head, wearing a faded polo shirt. Photographed on a sunny Florida porch.",
    "carol":    "A 59-year-old Black American woman with short natural greying hair, warm round face, small gold earrings, wearing a simple purple blouse. Photographed in her kitchen.",
    "patricia": "A 58-year-old Latina woman with dark hair going grey at the roots pulled back loosely, glasses, wearing a plain grey t-shirt. Photographed in a sunny back yard in Arizona.",
    "diane":    "A 71-year-old white American woman with short white curly hair, deep smile lines, glasses on a beaded chain, wearing a soft cardigan. Photographed in her living room.",
    "susan":    "A 67-year-old Black American woman with short grey-black hair, glasses, a warm lined face, wearing a red cardigan. Photographed on her front porch.",
    "david":    "A 49-year-old white American man with short brown hair receding slightly, stubble, wearing a plain zip hoodie. Photographed in a home office in front of a bookshelf.",
    "nancy":    "A 63-year-old white American woman with shoulder-length grey-blonde hair, glasses, wearing a plain navy sweater. Photographed in her car in a parking lot.",
    "margaret": "A 64-year-old white American woman with a short practical grey bob, no glasses, wearing a light blue button shirt. Photographed in a bright kitchen.",
}


def ctx():
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


def load_key():
    global KEY
    for line in open(os.path.join(VAULT, ".env")):
        if line.startswith("KIE_API_KEY="):
            KEY = line.strip().split("=", 1)[1]
    assert KEY


def state():
    return json.load(open(STATE_PATH)) if os.path.exists(STATE_PATH) else {"tasks": {}}


def save(st):
    json.dump(st, open(STATE_PATH, "w"), indent=1)


def api(path, payload=None):
    data = json.dumps(payload).encode() if payload else None
    req = urllib.request.Request(API + path, data=data, headers={
        "Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, context=ctx(), timeout=120) as r:
        return json.loads(r.read().decode(), strict=False)


def cmd_gen():
    st = state()
    for who, desc in PEOPLE.items():
        for v in range(1, VARIANTS + 1):
            slot = f"{who}-v{v}"
            if st["tasks"].get(slot, {}).get("taskId"):
                print(f"{slot}: skip"); continue
            payload = {"model": T2I, "input": {
                "prompt": BASE + desc + " " + FOOT,
                "aspect_ratio": "1:1", "resolution": "1K"}}
            for attempt in range(6):
                try:
                    r = api("/createTask", payload)
                    tid = (r.get("data") or {}).get("taskId")
                    if tid:
                        st["tasks"][slot] = {"taskId": tid, "state": "queued"}
                        save(st); print(f"{slot}: queued"); break
                except Exception as e:
                    print(f"{slot}: try{attempt+1} {e}")
                time.sleep(5 + 4 * attempt)
            time.sleep(2)


def cmd_poll():
    st = state(); os.makedirs(OUT, exist_ok=True)
    pending = [s for s, t in st["tasks"].items() if t.get("state") != "done"]
    while pending:
        for slot in list(pending):
            try:
                d = (api(f"/recordInfo?taskId={st['tasks'][slot]['taskId']}").get("data") or {})
            except Exception:
                continue
            s = d.get("state")
            if s == "success":
                urls = json.loads(d.get("resultJson") or "{}").get("resultUrls") or []
                if urls:
                    dest = os.path.join(OUT, f"{slot}.png")
                    subprocess.run(["curl", "-s", "-A", "Mozilla/5.0", "-o", dest, urls[0]])
                    st["tasks"][slot].update(state="done", file=dest)
                    print(f"{slot}: DONE")
                else:
                    st["tasks"][slot].update(state="done"); print(f"{slot}: no url")
                pending.remove(slot); save(st)
            elif s == "fail":
                st["tasks"][slot].update(state="done"); print(f"{slot}: FAIL")
                pending.remove(slot); save(st)
        if pending:
            print(f"  ... {len(pending)} pending"); time.sleep(15)


if __name__ == "__main__":
    load_key()
    {"gen": cmd_gen, "poll": cmd_poll}[sys.argv[1] if len(sys.argv) > 1 else "poll"]()
