#!/usr/bin/env python3
"""Emit the v4 visuals index + the 12 new prompts."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
M = json.load(open(os.path.join(HERE, "manifest.json")))
OUT = os.path.normpath(os.path.join(HERE, "..", "VEL-SOFIA-ONEBAG-01-visuals.md"))

LANDS = {
    "V01": "If you buy one handbag this summer,",
    "V02": "make it a woven raffia tote. There are a lot of bags trending right now,",
    "V03": "but this is the one I reach for all summer. It is the Sofia, from Velantra.",
    "V04": "And the thing that actually makes it is the shape.",
    "V05": "It is structured, so it holds its shape.",
    "V06": "You can set it down and it stands up on its own.",
    "V07": "Which is why it works for lunch and dinner, not just the beach.",
    "V08": "The straw is hand woven,",
    "V09": "and all the leather on it is real. The flap is one single piece folded over the top,",
    "V10": "the handles are rolled leather,",
    "V11": "and there are two leather straps crossed on the front with white stitching.",
    "V12": "That is what makes it read like a real handbag.",
    "V13": "And there is no logo on it anywhere.",
    "V14": "People ask me about it constantly and they have no idea what it is.",
    "V15": "It also goes with everything. Jeans and a white tee,",
    "V16": "dresses, denim, linen, pretty much your whole summer closet.",
    "V17": "And it fits a full day. Towel, snacks, sunscreen,",
    "V18": "everything, and it still looks good at dinner.",
    "V19": "And a woven tote comes back every single summer,",
    "V20": "so you will actually wear this one for years.",
    "V21": "It comes in a bunch of colors, mine is the caramel.",
    "V22": "I will leave the link below.",
}
DESC = {
    "V01": "Product hero on a sunlit plaster step. Empty wall above holds the hook card.",
    "V02": "Bedroom mirror selfie, phone covering her face. Cleanest product read — brand lands here.",
    "V03": "Stepping out of a stone doorway into hard sun, cream linen dress, seen from behind.",
    "V04": "Standing alone and unsupported on a marble cafe table, espresso and sunglasses beside it.",
    "V05": "Low three-quarter on a stone step — flat base and square corners against raking light.",
    "V06": "Standing square on a cafe chair seat, dappled terrace light.",
    "V07": "On a linen restaurant table at golden hour, wine glass beside it. The dinner proof.",
    "V08": "Macro of the hand-woven straw, braided cross-stitch trim running down the edge.",
    "V09": "Macro of the top — leather running unbroken edge to edge as one band, single stitch line.",
    "V10": "Macro of both rolled handles rising as two separate loops, white stitching sharp.",
    "V11": "Macro of the two belt straps crossing in an X, contrast stitching legible.",
    "V12": "Held at chest height in both hands, navy cardigan, bag fills the frame.",
    "V13": "Hanging dead-on from a wooden peg on a plain wall. Nothing on the front face.",
    "V14": "Wide boulevard, glancing back over her shoulder — she's being looked at.",
    "V15": "Cropped waist shot, white tee and straight jeans, bag square to camera.",
    "V16": "Crossing a city crosswalk in wide-leg denim and an oversized white shirt.",
    "V17": "High overhead angle, long white dress, bag carried full at her side.",
    "V18": "On a pool lounger with a rolled towel, sunscreen and a book beside it.",
    "V19": "Beside a red vintage car on a village street, sunglasses, head turned away.",
    "V20": "Walking away down a sunlit old-town street, arched wooden door behind.",
    "V21": "Three colorways in a row on a plaster ledge — caramel, sky blue, caban black.",
    "V22": "On a sunlit stone ledge, olive foliage behind, empty upper third for the end card.",
}

L = []
w = L.append
shots = M["shots_v4"]
w("# VEL-SOFIA-ONEBAG-01 — Visuals")
w(f"### {len(shots)} images, a new one roughly every 3 seconds\n")
w(f"**Product:** {M['product']} · **VO:** {M['vo_duration']:.2f}s (w30) · **Aspect:** 9:16 · "
  f"**Files:** `assets/visuals/V01.png` … `V{len(shots):02d}.png`\n")
avg = M["vo_duration"] / len(shots)
w(f"Cadence averages **{avg:.2f}s**, range "
  f"{min(s['dur'] for s in shots):.2f}–{max(s['dur'] for s in shots):.2f}s. Cut points are snapped to "
  f"real word boundaries in the VO alignment, not a flat 3.0s metronome, so every cut lands on a word "
  f"instead of chopping a phrase in half.\n")
w("---\n")
w("## Timeline\n")
w("| # | In | Out | Len | Lands on | Shot |")
w("|---|---|---|---|---|---|")
for s in shots:
    w(f"| **{s['id']}** | {s['in']:.2f} | {s['out']:.2f} | {s['dur']:.2f}s | "
      f"{LANDS[s['id']]} | {DESC[s['id']]} |")
w("")
w("---\n")
w("## Where they came from\n")
reuse = [s for s in shots if "reuse" in s]
new = [s for s in shots if "prompt" in s]
w(f"**{len(new)} newly generated** for this cut: " + ", ".join(s["id"] for s in new))
w(f"  \n**{len(reuse)} carried over** from the earlier QA-passed set: " +
  ", ".join(f"{s['id']} (was {s['reuse']})" for s in reuse) + "\n")
w("All 22 passed the product QA gate — flap one continuous sheet, exactly 2 separate handle loops, "
  "exactly 2 crossed belt straps, zero metal, no invented shoulder strap, bag holding its structured "
  "shape. The 12 new ones passed first attempt.\n")
w("**On V21 (colorways):** generated with all three colorway references wired in order, not from the "
  "caramel hero alone — a text-only colour swap renders greige leather. Sky blue matches its reference's "
  "vivid azure; caban black is a natural tan straw body with black leather elements only, never an "
  "all-black bag.\n")
w("---\n")
w("## Prompts for the 12 new frames\n")
w("Engine `gpt-image-2-image-to-image`, 9:16, 2K, `caramel 1.png` wired as the only reference "
  "(V21 takes caramel + blue + black in that order). Each block below is complete — the scene line "
  "plus the three fixed blocks that keep the bag correct.\n")
for s in new:
    w(f"### {s['id']} — {LANDS[s['id']]}\n")
    w("```")
    w(" ".join([s["prompt"], M["product_lock"], M["flap_closed_pin"], M["style_line"]]))
    w("```\n")

open(OUT, "w").write("\n".join(L))
print(f"wrote {os.path.basename(OUT)} ({os.path.getsize(OUT)/1024:.0f}KB)")
