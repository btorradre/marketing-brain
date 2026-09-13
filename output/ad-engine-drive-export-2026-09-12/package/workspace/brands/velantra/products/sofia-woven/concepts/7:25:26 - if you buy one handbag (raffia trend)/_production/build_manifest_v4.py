#!/usr/bin/env python3
"""22-shot visual plan for VEL-SOFIA-ONEBAG-01 v4 — a new visual roughly every 3s.

Cut points are snapped to real phrase boundaries in the w30 VO word alignment rather than
a flat 3.0s metronome, so every cut lands on a word rather than mid-phrase.

10 of the 22 reuse frames already generated and QA'd. 12 are new.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
OLD = json.load(open(os.path.join(HERE, "manifest.json")))
WORDS = json.load(open(os.path.join(ROOT, "assets", "vo", "VEL-SOFIA-ONEBAG-VO-w30.words.json")))

REFDIR = ("/Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/"
          "straw-birkin/product-images/straw birkin")

TARGET, MIN_D, MAX_D = 2.9, 1.8, 4.0

# ---------------------------------------------------------------- shot list
# reuse = copy an existing QA-passed frame. prompt = generate new.
SHOTS = [
    # B1 verdict
    ("V01", "Verdict", {"reuse": "S01"}),
    # B2 reassurance + reveal
    ("V02", "Reassurance + reveal", {"reuse": "S04"}),
    ("V03", "Reassurance + reveal", {"prompt":
        "A candid street style photograph of a woman stepping out of a shaded stone doorway into hard "
        "sunlight, caught mid stride and seen at three quarters from behind so her face is turned away "
        "and never visible. She wears a cream linen shirt dress and flat tan sandals, dark hair loose. "
        "She carries the caramel straw tote down in her right hand, the bag rotated so its front face is "
        "toward the camera. Warm stone wall and a sliver of bright street beyond."}),
    # B3 structure
    ("V04", "Structure", {"prompt":
        "A candid photograph of the caramel straw tote standing alone and upright on a small round "
        "marble cafe table in bright morning sun, an espresso cup and a folded pair of sunglasses on the "
        "table beside it. No people anywhere in frame. The bag stands unsupported on its own flat base, "
        "square and rigid, holding a clean rectangular shape with crisp upright corners, not leaning on "
        "anything and not slumping."}),
    ("V05", "Structure", {"prompt":
        "A low three quarter angle photograph of the caramel straw tote standing unsupported on a warm "
        "sunlit stone step, photographed from slightly below so the flat base and the square upright "
        "corners read clearly against the light. Hard raking side light rakes across the weave and casts "
        "a long crisp shadow. No people anywhere in frame. The bag is rigid and self supporting, holding "
        "its rectangular shape with no sagging or leaning anywhere."}),
    ("V06", "Structure", {"reuse": "S10"}),
    ("V07", "Structure", {"prompt":
        "A candid photograph of the caramel straw tote standing upright on a linen covered restaurant "
        "table at golden hour, a glass of white wine and a folded napkin beside it, warm low evening "
        "light and soft bokeh of a terrace behind. No faces and no people in frame. The bag stands "
        "unsupported and square on its own base, holding its rigid rectangular shape. The mood is "
        "dinner, not beach."}),
    # B4 leather work
    ("V08", "Leather work", {"prompt":
        "An extreme macro photograph of the hand woven straw body of the caramel tote, filling the whole "
        "frame, the weave tight and even in clean parallel rows with the braided cross stitch trim "
        "running along one edge. Hard raking daylight picks out the texture of every strand. No people, "
        "no hands and no leather flap in frame, only the woven straw surface and the braided edge."}),
    ("V09", "Leather work", {"prompt":
        "A macro photograph of the top of the caramel straw tote, framed tight and straight on so the "
        "top edge of the leather flap fills the frame horizontally. The smooth taupe leather runs "
        "continuously and unbroken from the far left edge to the far right edge as one single "
        "uninterrupted band with one clean stitch line along it, folded over from the back and lying "
        "completely flat. Soft directional daylight. No people and no hands in frame."}),
    ("V10", "Leather work", {"prompt":
        "A macro photograph of the two rolled taupe leather top handles of the caramel straw tote, "
        "framed tight so both handles fill the frame, each rising as its own separate clean rounded loop "
        "well apart from the other, each passing down through its own narrow slot in the leather. The "
        "rolled edge and the white contrast stitching along each handle are sharp and clearly visible. "
        "Soft daylight. No people and no hands in frame."}),
    ("V11", "Leather work", {"prompt":
        "A macro photograph of the front of the caramel straw tote framed tight on the two taupe leather "
        "belt straps where they cross over each other in an X against the woven straw, the white contrast "
        "stitching running along both straps crisp and clearly legible, the rounded strap ends visible. "
        "Soft directional daylight rakes across the leather grain. No people and no hands in frame."}),
    ("V12", "Leather work", {"reuse": "S08"}),
    # B5 no logo
    ("V13", "No logo", {"prompt":
        "A clean straight on photograph of the caramel straw tote hanging from a simple wooden peg on a "
        "plain warm off white wall, shot dead centre and square to the camera so the entire front face "
        "of the bag fills the middle of the frame in even soft daylight. The front face is completely "
        "plain and unmarked: woven straw, the leather flap, the two crossed belt straps and nothing "
        "else. No people in frame."}),
    ("V14", "No logo", {"reuse": "S09"}),
    # B6 goes with everything
    ("V15", "Goes with everything", {"reuse": "S03"}),
    ("V16", "Goes with everything", {"reuse": "S07"}),
    # B7 holds a real day
    ("V17", "Holds a real day", {"reuse": "S06"}),
    ("V18", "Holds a real day", {"prompt":
        "A candid photograph of the caramel straw tote standing upright on a cream canvas sun lounger by "
        "a pool, a rolled striped beach towel, a bottle of sunscreen and a paperback lying on the "
        "lounger beside the bag, not inside it. Bright hard midday sun and clean pool blue in the soft "
        "background. No people in frame. The bag is closed and stands square and full on its own base."}),
    # B8 longevity
    ("V19", "Longevity", {"reuse": "S05"}),
    ("V20", "Longevity", {"reuse": "S02"}),
    # B9 CTA
    ("V21", "CTA", {"colorways": True, "prompt":
        "A clean editorial photograph of three straw totes of the identical same structured design "
        "standing upright in a row on a long warm cream plaster ledge in soft even daylight, "
        "photographed straight on, evenly spaced and all facing the camera. Left bag: the caramel "
        "colorway exactly as in the first reference image, warm sandy caramel straw with taupe leather. "
        "Middle bag: the sky blue colorway exactly as in the second reference image, its leather "
        "elements matching that second reference image's colors exactly and never left taupe or greige. "
        "Right bag: the caban black colorway exactly as in the third reference image, a NATURAL TAN "
        "straw body with BLACK leather elements only, never an all black bag. All three bags are the "
        "same shape, same size and stand square on their own bases. No people in frame."}),
    ("V22", "CTA", {"prompt":
        "A candid photograph of the caramel straw tote standing upright on a sunlit pale stone ledge, "
        "soft green foliage and a warm stone wall thrown gently out of focus behind it, dappled "
        "afternoon light. No people in frame. The bag sits low in the frame and stands square on its own "
        "base, with generous quiet empty space across the whole upper third of the image for a text "
        "overlay."}),
]


def plan_slots(n):
    """Snap n cut points to real word boundaries in the VO.

    Phrase ends (comma/period) are preferred, but any word end is allowed — punctuation alone
    leaves 3-4s gaps in places and forces 5s slots. Target self-corrects each step off the
    remaining time so the last shot can't end up a 1.4s flash.
    """
    phrase = {round(w["end"], 2) for w in WORDS["words"]
              if w["word"].rstrip().endswith((".", ",", "!", "?"))}
    allw = sorted({round(w["end"], 2) for w in WORDS["words"]})
    total = round(WORDS["duration"], 2)
    cuts, t = [0.0], 0.0
    for _ in range(n - 1):
        remaining = n - len(cuts)                      # shots still to place after this cut
        target = t + (total - t) / (remaining + 1)     # self-correcting
        cands = [b for b in allw
                 if t + MIN_D <= b <= min(t + MAX_D, total - remaining * MIN_D)]
        if not cands:
            cands = [b for b in allw if b > t + MIN_D * 0.6] or [total]
        # prefer a phrase boundary, but not at the cost of a badly sized slot
        b = min(cands, key=lambda x: abs(x - target) + (0.0 if x in phrase else 0.45))
        cuts.append(b)
        t = b
    cuts.append(total)
    return cuts


cuts = plan_slots(len(SHOTS))
shots = []
for i, (sid, beat, spec) in enumerate(SHOTS):
    if i + 1 >= len(cuts):
        break
    shots.append({"id": sid, "beat": beat,
                  "in": round(cuts[i], 2), "out": round(cuts[i + 1], 2),
                  "dur": round(cuts[i + 1] - cuts[i], 2), **spec})

M = dict(OLD)
M.update({
    "version": "v4 — 22 visuals, ~3s cadence",
    "vo_duration": WORDS["duration"],
    "refs": {"caramel": f"{REFDIR}/caramel 1.png",
             "blue": f"{REFDIR}/blue 1.png",
             "black": f"{REFDIR}/black-colorway/black-tote-1.jpeg"},
    "image_resolution": "2K",
    "shots_v4": shots,
})
json.dump(M, open(os.path.join(HERE, "manifest.json"), "w"), indent=1)

new = sum(1 for s in shots if "prompt" in s)
print(f"{len(shots)} visuals over {WORDS['duration']:.2f}s  "
      f"(avg {WORDS['duration']/len(shots):.2f}s, "
      f"min {min(s['dur'] for s in shots):.2f}, max {max(s['dur'] for s in shots):.2f})")
print(f"  {len(shots)-new} reuse existing QA-passed frames, {new} new\n")
for s in shots:
    src = f"reuse {s['reuse']}" if "reuse" in s else "NEW"
    print(f" {s['id']} {s['in']:>6.2f}-{s['out']:>6.2f} ({s['dur']:>4.2f}s)  {s['beat']:<22} {src}")
