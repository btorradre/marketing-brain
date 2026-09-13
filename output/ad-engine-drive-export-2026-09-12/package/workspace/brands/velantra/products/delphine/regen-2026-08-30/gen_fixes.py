#!/usr/bin/env python3
"""Re-roll of the two shots that failed QA: 03-interior and 04-hardware.

WHAT WENT WRONG. Every prompt in gen_gallery.py appends the full head-to-toe
identity block ("THE BAG ITSELF: ...handles, flap, canvas panel, base, sides").
On the wide shots that block is what makes the bag correct. On a MACRO or an
INTERIOR it fights the crop: the model is told to render an entire bag and does,
so all six frames came back as ordinary front packshots with no macro and no
lining anywhere. Not a lock defect and not a distance-regime problem -- we never
got the crop at all.

THE FIX, and the general rule: a crop shot gets a crop-specific block describing
ONLY what is inside the frame, never the whole-object identity block. The
framing goes FIRST, the subject second, and the prompt states explicitly which
parts of the object are outside the frame.
"""
import os, json, time, subprocess
from gen_masters import api, upload, H, API, ROOT, MATERIAL, ANTI_CGI, LC, DC, AG

APPROVED = os.path.join(ROOT, "approved")
SEEDS = os.path.join(ROOT, "seeds")
GALLERY = os.path.join(ROOT, "gallery")
CW = {"LC": LC, "DC": DC, "AG": AG}
LINING = {"LC": "smooth black fabric", "DC": "deep olive green suede"}

NO_TEXT = ("Absolutely no text, no words, no letters, no captions, no watermarks and no logos anywhere "
           "in the image.")

# Framing first, and the excluded parts named. Both blocks deliberately omit the
# whole-bag identity description.

def interior(k):
    return (
        f"EXTREME CLOSE UP. The camera is directly above an open handbag, pointing straight down INTO it, so "
        f"close that the inside of the bag fills the entire frame edge to edge. What is visible: the "
        f"{LINING[k]} lining of the inside walls and floor of the bag, and one interior pocket set into one "
        f"wall closing with a small brass zip whose pull hangs down against the lining. The bag is empty. "
        f"The frame contains NOTHING except the inside of this bag -- the flap, the handles, the turn lock, "
        f"the front panel, the canvas, the corner caps and the whole outside of the bag are all far outside "
        f"the frame and none of them appears anywhere in the picture. There is no background, no table, no "
        f"floor, no wall and no person visible, because the open bag fills the frame completely. Soft even "
        f"daylight falls into the bag from above. Photorealistic photograph, full frame camera, 50mm lens at "
        f"f5.6. The lining shows real fabric texture and the soft irregular slump of a real empty bag. "
        f"{NO_TEXT} {ANTI_CGI}"
    )


def hardware(k):
    cw = CW[k]
    return (
        f"EXTREME CLOSE UP MACRO PHOTOGRAPH, magnified so far that a piece of leather roughly the size of a "
        f"credit card fills the whole frame. The subject filling the frame is ONE upright oval brass turn "
        f"lock plate sitting on {cw['leather']}, shown exactly as in the reference images. The oval brass "
        f"plate is solid and unbroken, with one small domed screw near its top and one near its bottom, a "
        f"short round brass boss at its centre, and ONE short rounded brass turning bar lying across that "
        f"boss, no longer than about a third of the plate's height. There is no second bar, no duplicated "
        f"toggle, no long pill or capsule shape, no bar floating free of the plate or casting its own "
        f"shadow, no bar running past the plate's edge, no hole, slot, keyhole or open gap, no exposed post "
        f"or screw thread, and no silver, chrome or nickel anywhere. Around the plate there is only leather, "
        f"filling the rest of the frame, with its grain and a line of hand stitching rendered razor sharp. "
        f"The frame contains NOTHING else: no handles, no canvas, no corner caps, no whole bag, no "
        f"background and no person. The bag is so magnified that only this one fitting and the leather "
        f"immediately around it are in the picture. Soft diffused daylight from the upper left raking across "
        f"the leather. Photorealistic macro photograph, full frame camera, 100mm macro lens at f8, shallow "
        f"depth of field falling off at the frame edges. {MATERIAL} {NO_TEXT} {ANTI_CGI}"
    )


JOBS = []
for k in ("LC", "DC", "AG"):
    JOBS.append((f"{k}-04-hardware", hardware(k),
                 [os.path.join(APPROVED, f"{k}-lock.png"), os.path.join(APPROVED, f"{k}-master.png")]))
    if k in LINING:
        JOBS.append((f"{k}-03-interior", interior(k),
                     [os.path.join(SEEDS, f"{k}-interior.png")]))


def submit(p, refs):
    payload = {"model": "gpt-image-2-image-to-image",
               "input": {"prompt": p, "input_urls": refs, "aspect_ratio": "1:1", "resolution": "2K"}}
    d = api(f"{API}/jobs/createTask", payload, H)
    if d.get("code") != 200:
        payload["input"]["resolution"] = "1K"
        d = api(f"{API}/jobs/createTask", payload, H)
    assert d.get("code") == 200, f"createTask failed: {d}"
    return d["data"]["taskId"]


def main():
    cache, pending = {}, {}
    for tag, p, refs in JOBS:
        urls = []
        for r in refs:
            if r not in cache:
                cache[r] = upload(r)
            urls.append(cache[r])
        for roll in (1, 2):                      # 2 rolls, pick on a contact sheet
            t = f"{tag}-v2r{roll}"
            if os.path.exists(os.path.join(GALLERY, f"{t}.png")):
                print(f"{t}: exists, skip", flush=True); continue
            pending[t] = submit(p, urls)
            print(f"{t}: task {pending[t]}", flush=True)

    deadline = time.time() + 2400
    while pending and time.time() < deadline:
        time.sleep(15)
        for tag, tid in list(pending.items()):
            d = api(f"{API}/jobs/recordInfo?taskId={tid}", None, H)
            data = d.get("data") or {}
            st = data.get("state")
            if st == "success":
                u = (json.loads(data.get("resultJson") or "{}")).get("resultUrls") or []
                if u:
                    dest = os.path.join(GALLERY, f"{tag}.png")
                    subprocess.run(["curl", "-s", "-L", "--max-time", "300", "-o", dest, u[0]])
                    print(f"{tag}: SAVED", flush=True)
                pending.pop(tag)
            elif st == "fail":
                print(f"{tag}: FAILED {str(data.get('failMsg'))[:130]}", flush=True)
                pending.pop(tag)
    if pending:
        print("timed out:", list(pending), flush=True)


if __name__ == "__main__":
    main()
