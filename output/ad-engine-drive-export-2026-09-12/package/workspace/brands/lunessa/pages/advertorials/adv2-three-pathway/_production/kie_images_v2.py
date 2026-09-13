#!/usr/bin/env python3
"""adv2 v2 images — statin side-effect angle. GPT Image 2 on kie.ai.

Keeps IMG-01 (pill organiser), IMG-04 (three-pathway notebook), IMG-05 (bottle).
Adds hero, side-effect beat, artery diagram, one-year-later.

Usage: kie_images_v2.py gen [HERO ...] | poll | status
"""
import json, os, ssl, subprocess, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "images"))
STATE_PATH = os.path.join(HERE, "state_v2.json")
VAULT = "/Users/brooksorradre2/Documents/marketing brain"
API = "https://api.kie.ai/api/v1/jobs"
T2I = "gpt-image-2-text-to-image"
VARIANTS = 3
KEY = None

FOOTER = (
    "PHOTOGRAPHIC EVIDENCE REQUIRED: visible sensor noise and luminance grain, slightly blown "
    "highlights where light falls, mild chromatic aberration on high-contrast edges, faint JPEG "
    "artefacts, imperfect focus with at least one element slightly soft, mildly crooked handheld "
    "framing, and a genuinely lived-in setting with real clutter, dust and wear. "
    "ABSOLUTELY REFUSE: 3D render, CGI, product visualisation, Blender, Octane, Unreal, Keyshot, "
    "ray tracing, catalogue photography, stock-photo staging, studio lighting, softbox, ring light, "
    "beauty retouching, skin smoothing, HDR, colour grading, or any polished commercial look. "
    "This must read as an ordinary photograph of real people, not a photograph anyone was paid to make."
)

FACE = (
    "The woman is 56, white American, Midwestern. Shoulder-length dark blonde hair going grey at the "
    "temples, worn plainly. A soft lined face with visible pores, crow's feet, sun damage on her "
    "forearms, minimal or no makeup. Slightly heavy build. She looks like a real 56-year-old woman, "
    "never like a model or an actress. "
)

SCENES = {
    "HERO": dict(prompt=(
        "A candid photograph taken from over a clinician's shoulder in a small, plain exam room or "
        "clinic office. A 56-year-old woman sits across a wooden table, hands clasped in front of her "
        "mouth, elbows on the table, staring down at nothing. She looks exhausted and defeated, not "
        "crying. " + FACE +
        "On the table between them sits a clear gallon ziplock bag bulging with a dozen orange "
        "prescription pill bottles, plus a clipboard and a pen. The clinician is visible only as an "
        "out-of-focus shoulder and forearm in a pale blue coat at the right edge of the frame, no face. "
        "Flat daylight from a window on the left, dull green-grey wall behind her. Slightly crooked "
        "framing, shot from a seated height. "
        + FOOTER)),

    "SIDEEFFECT": dict(prompt=(
        "A candid photograph of a 56-year-old woman stopped partway up a carpeted staircase in an "
        "ordinary suburban house, gripping the wooden banister hard with both hands, head down, "
        "clearly waiting out pain in her legs. " + FACE +
        "She wears a plain long cardigan and loose trousers, socks, no shoes. Dim hallway light from "
        "above and a little daylight from a landing window. Worn carpet, a scuffed baseboard, a "
        "framed family photo crooked on the wall. Shot from the bottom of the stairs looking up, "
        "handheld, slightly blurred. Nobody else in frame. "
        + FOOTER)),

    "ONEYEAR": dict(prompt=(
        "A candid photograph of a 56-year-old woman walking a paved neighbourhood path on an ordinary "
        "overcast morning, mid-stride, caught mid-sentence talking to someone off camera, relaxed and "
        "unguarded. " + FACE +
        "She wears a zip fleece, leggings and worn walking shoes. Bare suburban trees, a chain-link "
        "fence, a parked car and a recycling bin in the background. Flat grey daylight, no sun. "
        "Framing is loose and a little tilted, shot on the move from beside her, one arm slightly "
        "motion-blurred. Not posed, not smiling at the camera. "
        + FOOTER)),

    # Illustration, NOT a photo. The anti-CGI footer is deliberately not applied here.
    "ARTERY": dict(prompt=(
        "A clean two-panel medical illustration for a health article, side by side, divided by a thin "
        "vertical rule. Flat editorial vector style with soft shading, muted anatomical colour palette "
        "of warm creams, salmon pinks and deep red, on an off-white background. "
        "LEFT PANEL, header text 'NON-OXIDIZED LDL': a cross-section of a healthy artery, smooth even "
        "pink inner wall, open channel, small tidy pale-yellow LDL particles flowing freely. Small "
        "labels reading 'SMOOTH ARTERY WALL' and 'CLEAR BLOODSTREAM'. "
        "RIGHT PANEL, header text 'OXIDIZED LDL': the same artery now narrowed, the inner wall rough, "
        "swollen and inflamed darker red, with lumpy orange-brown oxidized particles clumping and "
        "sticking to the wall forming a raised plaque deposit that narrows the channel. Small labels "
        "reading 'INFLAMED ARTERY WALL' and 'PLAQUE FORMATION'. "
        "Clean sans-serif labels, all text spelled exactly as given, high legibility, no watermark, "
        "no extra text, no logos. Textbook clarity, not photographic, not 3D rendered."))
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


def cmd_gen(only):
    st = state()
    for sid in (only or list(SCENES)):
        ratio = "3:2" if sid != "ARTERY" else "3:2"
        for v in range(1, VARIANTS + 1):
            slot = f"{sid}-v{v}"
            if st["tasks"].get(slot, {}).get("taskId"):
                print(f"{slot}: skip"); continue
            payload = {"model": T2I, "input": {
                "prompt": SCENES[sid]["prompt"], "aspect_ratio": ratio, "resolution": "2K"}}
            for attempt in range(6):
                try:
                    r = api("/createTask", payload)
                    tid = (r.get("data") or {}).get("taskId")
                    if tid:
                        st["tasks"][slot] = {"taskId": tid, "state": "queued"}
                        save(st); print(f"{slot}: queued {tid}"); break
                    print(f"{slot}: try{attempt+1} {str(r)[:120]}")
                except Exception as e:
                    print(f"{slot}: try{attempt+1} err {e}")
                time.sleep(6 + 5 * attempt)
            time.sleep(3)


def cmd_poll():
    st = state(); os.makedirs(OUT, exist_ok=True)
    pending = [s for s, t in st["tasks"].items() if t.get("state") != "done"]
    while pending:
        for slot in list(pending):
            try:
                d = (api(f"/recordInfo?taskId={st['tasks'][slot]['taskId']}").get("data") or {})
            except Exception as e:
                print(f"{slot}: poll err {e}"); continue
            s = d.get("state")
            if s == "success":
                urls = json.loads(d.get("resultJson") or "{}").get("resultUrls") or []
                if urls:
                    dest = os.path.join(OUT, f"LUN-ADV2-{slot}.png")
                    subprocess.run(["curl", "-s", "-A", "Mozilla/5.0", "-o", dest, urls[0]])
                    st["tasks"][slot].update(state="done", file=dest)
                    print(f"{slot}: DONE {os.path.getsize(dest)//1024}kb")
                else:
                    st["tasks"][slot].update(state="done", file=None); print(f"{slot}: no url")
                pending.remove(slot); save(st)
            elif s == "fail":
                st["tasks"][slot].update(state="done", file=None)
                print(f"{slot}: FAIL {str(d.get('failMsg'))[:100]}")
                pending.remove(slot); save(st)
        if pending:
            print(f"  ... {len(pending)} pending"); time.sleep(20)


if __name__ == "__main__":
    load_key()
    cmd = sys.argv[1] if len(sys.argv) > 1 else "poll"
    {"gen": lambda: cmd_gen(sys.argv[2:]), "poll": cmd_poll}[cmd]()
