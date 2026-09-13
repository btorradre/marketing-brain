#!/usr/bin/env python3
"""THE DELPHINE — full PDP gallery, rolled off the APPROVED masters.

Approved 2026-08-30: AG = master-r1, LC = master-r2, DC = master-r2, copied to
`approved/`. Per feedback_one_approved_master_is_the_only_product_seed the
approved master is the ONLY product seed for every exterior frame. The interior
frames are the one legitimate exception -- the master contains no lining, so
they anchor on the real interior photograph instead.

Seven shots per colorway, mirroring the live 18-media gallery plus one new one:

  01-front        the approved master itself (copied, not regenerated)
  02-threequarter studio
  03-interior     TIGHT on the lining only  -- AG SKIPPED, lining unconfirmed
  04-hardware     macro, turn-lock block mandatory, 2 rolls
  05-crossbody    NEW. The strap the library has never shown.
  06-onarm        sunlit Mediterranean loggia
  07-modelcarry   full length, plain warm wall

Laws enforced here, each one learned the hard way on this product:
  - The interior is shot VERY TIGHT on the lining alone. The folded-back flap
    shatters in macro (PRODUCT-TRUTH v5), so it never appears large in frame.
  - The hardware macro carries the §4 turn-lock block AND a 3x crop of the
    correct lock lifted from the approved master, the 8/16 repair recipe.
  - CAPACITY LAW: no phone and no sunglasses anywhere in any frame. Provable
    load is a wallet, cards, a lip colour, keys, one slim pouch.
  - Background props are named explicitly and kept plain -- a background basket
    once rendered a competitor's emblem and this brand has live DMCA history.
"""
import os, shutil, json, time, subprocess
from gen_masters import (identity, SCALE, MATERIAL, ANTI_CGI, LC, DC, AG,
                         api, upload, H, API, OUT as MASTER_DIR, ROOT)

APPROVED = os.path.join(ROOT, "approved")
GALLERY = os.path.join(ROOT, "gallery")
CW = {"LC": LC, "DC": DC, "AG": AG}

# --- BLOCKS ------------------------------------------------------------------

# The strap. Proven on camera in the Trybe creator ad at 0:26-0:35 and absent
# from every image in the old library.
STRAP_ON = (
    "THE SHOULDER STRAP IS FITTED AND IN USE. A long thin detachable shoulder strap of the same leather as "
    "the bag runs from the bag up over her shoulder, attached at each end by a small gold snap hook clipped "
    "to the gold fitting at each top side corner of the bag. The strap is narrow, about as wide as two "
    "fingers, one continuous unbroken length of leather, and it lies flat across her body. The bag hangs "
    "from it at her hip. Both of the bag's short rolled top handles are still present and stand upright "
    "above the bag, unused."
)
STRAP_OFF_HANDLES = (
    "The long detachable shoulder strap is not fitted in this frame, but the small gold roller buckle and "
    "strap fitting on each side gusset that it clips to are present and clearly visible."
)

# §4 turn-lock block. The lock survives at medium distance and shatters in
# macro. Negatives are named because the positive description alone did not hold.
TURNLOCK = (
    "THE TURN LOCK, which is the subject of this frame and must be exactly right: one upright oval brass "
    "plate, solid and unbroken, with one small domed screw near its top and one near its bottom, a short "
    "round brass boss at its centre, and ONE short rounded brass turning bar lying across that boss, no "
    "longer than about a third of the plate's height. There is no second bar, no duplicated toggle, no long "
    "pill or capsule shape, no bar floating free of the plate or casting its own shadow, no bar running past "
    "the plate's edge, no hole, slot, keyhole or open gap, no exposed post or screw thread, and no silver, "
    "chrome or nickel anywhere. The second reference image is a magnified crop of this exact lock rendered "
    "correctly; copy its shape precisely."
)

MODEL = (
    "The woman is in her early forties, with warm skin showing real visible texture and fine lines at her "
    "eyes, no heavy makeup, natural brows and bare lips with a little gloss. Her hair is loose and slightly "
    "undone with a few strands moving, never slicked back. She wears small simple earrings and no necklace "
    "and no other jewelry at all, nothing around her neck. She looks relaxed and unposed, in the middle of "
    "an ordinary good day, never a cold editorial stare and never a wide posed grin. Her hands are rendered "
    "cleanly and naturally, five well formed fingers on each visible hand, each finger clearly separated and "
    "correctly proportioned, in a relaxed everyday grip. Only one person in the frame."
)

GRIP = (
    "How she holds it: her fingers curl completely around the two short rolled top handles low down, close "
    "to where the handles enter the leather, so each handle tube is clearly visible both ABOVE her curled "
    "fingers and BELOW them, passing through her hand the way a real bag handle does. Each handle is one "
    "single continuous unbroken loop and both complete arches read fully along their length. The weight of "
    "the bag visibly hangs from that grip."
)

# CAPACITY LAW. Phone and sunglasses are banned from Delphine imagery until
# physically confirmed in the real 25 cm unit. The old VO set violated this in
# the footage while the scripts were clean.
NO_PHONE = (
    "There is no phone and no sunglasses anywhere in this image. There is no laptop, no water bottle and no "
    "second bag of any kind in the frame."
)

CLEAN_PROPS = (
    "Every object in the background is plain and unbranded, with no emblems, no crests, no monograms, no "
    "hardware badges and no writing of any kind on anything in the frame."
)

STUDIO = (
    "Warm off white seamless studio sweep in colour #F5F2EC, the floor curving up into the back wall with no "
    "visible corner or edge. Soft diffused daylight from the upper left, one soft contact shadow under the "
    "bag, a warm quiet low contrast grade. Photorealistic product photograph on a full frame camera, 100mm "
    "macro lens at f8, the whole bag sharp."
)

NO_TEXT = (
    "Absolutely no text, no words, no letters, no captions, no watermarks, no measurements and no logos "
    "anywhere in the image."
)

LINING = {"LC": "smooth black fabric lining", "DC": "deep olive green suede lining"}

# --- SHOTS -------------------------------------------------------------------
# (id, needs_model, extra_ref_key, aspect, scene)


def shots(k):
    cw = CW[k]
    s = [
        ("02-threequarter",
         f"The {cw['name']} handbag alone, photographed from a three quarter angle so the front panel and one "
         f"full leather side gusset are both visible, turned about thirty degrees from straight on, standing "
         f"upright on its own gold feet. {STRAP_OFF_HANDLES} {STUDIO}", None, "1:1"),

        ("04-hardware",
         f"EXTREME CLOSE UP MACRO of the centre front of the {cw['name']} handbag, filling the frame with the "
         f"upright oval gold turn lock on its leather flap and the leather immediately around it. The leather "
         f"grain and the stitching are razor sharp. {TURNLOCK} {STUDIO}", "lock", "1:1"),

        ("05-crossbody",
         f"A woman standing in a bright plain room by a window, framed from her thighs up, turned slightly "
         f"toward the camera, wearing the {cw['name']} handbag CROSSBODY on its long shoulder strap. She wears "
         f"a simple cream knit and soft tailored trousers in a warm neutral. {STRAP_ON} {MODEL} {NO_PHONE} "
         f"{CLEAN_PROPS} Photorealistic lifestyle photograph on a full frame camera, 85mm lens at f2.8, soft "
         f"natural window light, real skin texture and real fabric texture.", None, "1:1"),

        ("06-onarm",
         f"A woman walking through a sunlit Mediterranean stone loggia with olive trees and warm limestone "
         f"beyond the arches, framed from her waist up and slightly behind, carrying the {cw['name']} handbag "
         f"in the crook of her elbow. She wears a cream linen shirt and sand coloured trousers. The bag sits "
         f"compactly against her forearm, clearly smaller than her forearm is long. {STRAP_OFF_HANDLES} "
         f"{MODEL} {GRIP} {NO_PHONE} {CLEAN_PROPS} Photorealistic editorial lifestyle photograph, full frame "
         f"camera, 85mm lens at f2.8, warm late afternoon sun, real skin and fabric texture.", None, "1:1"),

        ("07-modelcarry",
         f"A woman standing full length against a plain warm off white wall in soft daylight, her whole body "
         f"in frame from head to shoes, holding the {cw['name']} handbag by its two top handles down at her "
         f"side. She wears a relaxed cream knit, straight leg light denim and simple flat shoes. Held at her "
         f"side the bag hangs no lower than the top of her hip, reading clearly as a small handbag. "
         f"{STRAP_OFF_HANDLES} {MODEL} {GRIP} {NO_PHONE} {CLEAN_PROPS} Photorealistic full length fashion "
         f"photograph, full frame camera, 50mm lens at f4, soft even daylight.", None, "1:1"),
    ]
    if k in LINING:
        s.insert(1, (
            "03-interior",
            f"TIGHT INTERIOR DETAIL of the {cw['name']} handbag, shot straight down into the open mouth of "
            f"the bag from directly above, filling the frame with the {LINING[k]} inside and the gold zipped "
            f"interior pocket running along one wall, its small gold zipper pull clearly visible. The bag is "
            f"empty. Only the inside of the bag and the very top edge of its opening are in frame: the flap, "
            f"the handles, the front panel and the outside of the bag are all entirely OUTSIDE the frame and "
            f"none of them is visible. {NO_PHONE} {STUDIO}", "interior", "1:1"))
    return s


EXTRA = {"lock": lambda k: os.path.join(APPROVED, f"{k}-lock.png"),
         "interior": lambda k: os.path.join(ROOT, "seeds", f"{k}-interior.png")}

ROLLS = {"04-hardware": 2}   # known macro failure regime


def prompt(k, scene):
    cw = CW[k]
    return (f"{scene} THE BAG ITSELF: {identity(cw)} {SCALE} {MATERIAL} "
            f"The bag matches the bag in the first reference image exactly in construction, proportion, "
            f"hardware and colour. {NO_TEXT} {ANTI_CGI}")


def submit(k, scene, refs, aspect):
    payload = {"model": "gpt-image-2-image-to-image",
               "input": {"prompt": prompt(k, scene), "input_urls": refs,
                         "aspect_ratio": aspect, "resolution": "2K"}}
    d = api(f"{API}/jobs/createTask", payload, H)
    if d.get("code") != 200:
        payload["input"]["resolution"] = "1K"
        d = api(f"{API}/jobs/createTask", payload, H)
    assert d.get("code") == 200, f"createTask failed: {d}"
    return d["data"]["taskId"]


def main():
    os.makedirs(GALLERY, exist_ok=True)
    cache = {}
    pending = {}

    for k in ("LC", "DC", "AG"):
        # 01-front IS the approved master. Never regenerated.
        front = os.path.join(GALLERY, f"{k}-01-front.png")
        if not os.path.exists(front):
            shutil.copy(os.path.join(APPROVED, f"{k}-master.png"), front)
            print(f"{k}-01-front: copied from approved master", flush=True)

        mp = os.path.join(APPROVED, f"{k}-master.png")
        if mp not in cache:
            cache[mp] = upload(mp)

        for sid, scene, extra, aspect in shots(k):
            refs = [cache[mp]]
            if extra:
                ep = EXTRA[extra](k)
                if ep not in cache:
                    cache[ep] = upload(ep)
                # interior anchors on the real lining photo FIRST
                refs = [cache[ep], cache[mp]] if extra == "interior" else [cache[mp], cache[ep]]
            for r in range(1, ROLLS.get(sid, 1) + 1):
                suf = "" if ROLLS.get(sid, 1) == 1 else f"-r{r}"
                tag = f"{k}-{sid}{suf}"
                if os.path.exists(os.path.join(GALLERY, f"{tag}.png")):
                    print(f"{tag}: exists, skip", flush=True)
                    continue
                pending[tag] = submit(k, scene, refs, aspect)
                print(f"{tag}: task {pending[tag]}", flush=True)

    deadline = time.time() + 3600
    while pending and time.time() < deadline:
        time.sleep(15)
        for tag, tid in list(pending.items()):
            d = api(f"{API}/jobs/recordInfo?taskId={tid}", None, H)
            data = d.get("data") or {}
            st = data.get("state")
            if st == "success":
                urls = (json.loads(data.get("resultJson") or "{}")).get("resultUrls") or []
                if urls:
                    dest = os.path.join(GALLERY, f"{tag}.png")
                    subprocess.run(["curl", "-s", "-L", "--max-time", "300", "-o", dest, urls[0]])
                    print(f"{tag}: SAVED {os.path.getsize(dest)//1024}kb", flush=True)
                pending.pop(tag)
            elif st == "fail":
                print(f"{tag}: FAILED {str(data.get('failMsg'))[:150]}", flush=True)
                pending.pop(tag)
    if pending:
        print("timed out:", list(pending), flush=True)


if __name__ == "__main__":
    main()
