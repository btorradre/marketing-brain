#!/usr/bin/env python3
"""A01 / A02 — the agitation cutaways.

Deliberately TEXT-to-image, not i2i off the caramel hero: these frames must carry
none of the Sofia's DNA. Every prompt forces a soft round floppy basket silhouette
with no leather, no flap, no straps and no structure, so the worn bag can never be
misread as our product.
"""
import json, os, ssl, subprocess, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "assets", "keyframes"))
API = "https://api.kie.ai/api/v1/jobs"
MODEL = "gpt-image-2-text-to-image"

NOT_OUR_BAG = (
    "The bag in frame is a soft round floppy unstructured woven straw basket bag: it has no leather at "
    "all, no leather flap, no leather panel, no crossed belt straps, no stitching detail and no structure "
    "of any kind, and it collapses and slumps under its own weight. It is clearly a plain cheap basket "
    "bag and nothing like a structured leather trimmed tote. Absolutely no text, captions, watermarks, "
    "logos or graphics anywhere in the image."
)

SHOTS = {
    "A01": (
        "A candid photograph looking at a shelf inside a bright airy closet in soft natural daylight. Two "
        "soft round woven straw basket bags sit on the shelf, both collapsed flat and slumped over onto "
        "their sides, their rims caved in and their woven fibres visibly fuzzy and frayed along the "
        "corners and edges. Neutral linen and cotton clothing hangs softly out of focus to one side. The "
        "mood is quiet, muted and a little forgotten, like something put away and not picked up again. No "
        "people anywhere in frame. " + NOT_OUR_BAG
    ),
    "A02": (
        "An extreme macro photograph of the bottom corner of a soft unstructured woven straw basket bag. "
        "The straw fibres are split, dried out, fuzzy and frayed, several strands snapped and standing out "
        "loose from the weave, the weave itself loosened and pulled out of shape, one corner worn thin and "
        "misshapen. Soft directional window light rakes across the texture, very shallow depth of field, "
        "muted desaturated color. No people anywhere in frame. " + NOT_OUR_BAG
    ),
}


def ctx():
    import certifi
    return ssl.create_default_context(cafile=certifi.where())


def key():
    for line in open("/Users/brooksorradre2/Documents/marketing brain/.env"):
        if line.startswith("KIE_API_KEY="):
            return line.strip().split("=", 1)[1]
    raise SystemExit("KIE_API_KEY not found")


def api(path, payload=None, k=None):
    data = json.dumps(payload).encode() if payload else None
    req = urllib.request.Request(API + path, data=data, headers={
        "Authorization": f"Bearer {k}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, context=ctx(), timeout=120) as r:
        return json.loads(r.read().decode(), strict=False)


def main():
    k = key()
    tasks = {}
    for sid, prompt in SHOTS.items():
        r = api("/createTask", {"model": MODEL, "input": {
            "prompt": prompt, "aspect_ratio": "9:16", "resolution": "2K"}}, k)
        if r.get("code") != 200:
            print(f"{sid} CREATE FAIL: {r}")
            continue
        tasks[sid] = r["data"]["taskId"]
        print(f"{sid} task {tasks[sid]}")

    deadline = time.time() + 30 * 60
    while tasks and time.time() < deadline:
        for sid in list(tasks):
            d = (api(f"/recordInfo?taskId={tasks[sid]}", None, k).get("data") or {})
            if d.get("state") == "success":
                urls = json.loads(d.get("resultJson") or "{}", strict=False).get("resultUrls") or []
                dest = os.path.join(OUT, f"{sid}.png")
                subprocess.run(["curl", "-sL", "--fail", "-A", "Mozilla/5.0", "-o", dest, urls[0]],
                               check=True)
                print(f"{sid} DONE -> {dest}")
                del tasks[sid]
            elif d.get("state") == "fail":
                print(f"{sid} FAIL: {d.get('failMsg')}")
                del tasks[sid]
        if tasks:
            time.sleep(15)


if __name__ == "__main__":
    main()
