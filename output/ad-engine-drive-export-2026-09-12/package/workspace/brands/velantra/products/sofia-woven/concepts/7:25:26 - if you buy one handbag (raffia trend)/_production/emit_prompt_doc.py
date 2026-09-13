#!/usr/bin/env python3
"""Emit the copy-paste image prompt sheet for VEL-SOFIA-ONEBAG-01."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
M = json.load(open(os.path.join(HERE, "manifest.json")))
OUT = os.path.normpath(os.path.join(HERE, "..", "VEL-SOFIA-ONEBAG-01-image-prompts.md"))

# v3 beat map -- what each shot is doing in the cut
BEATS = {
    "S01": ("1 · Verdict", '"If you buy one handbag this summer, make it a woven raffia tote."',
            "Reads as *a raffia tote*, the category, not a brand pitch. Leave empty wall above for the hook card."),
    "S02": ("2 · Reassurance", '"...this is the one I reach for all summer, because it actually works for real life."',
            "Real-life use. She is walking away, so identity never has to hold."),
    "S03": ("3 · Reason 1, it styles you", '"You could be wearing jeans and a white tee, and it still looks put together."',
            "The simplest possible outfit. Cropped, no head in frame."),
    "S04": ("4 · The narrow, ours", '"The Sofia, from Velantra. It is hand woven... it holds its shape."',
            "**Cleanest product read in the set.** Flap, crossed belts, both handle loops and weave all legible."),
    "S05": ("5 · Reason 2, versatility", '"Beach, lunch, vacation, errands."',
            "Holiday register. Face tipped away behind sunglasses."),
    "S06": ("5 · Reason 2, versatility", '"And it is such a good mom bag. It fits a towel, snacks, sunscreen, my whole day."',
            "**B-roll keyframe.** High angle hides the face entirely."),
    "S07": ("6 · Reason 3, wardrobe fit", '"It works with dresses and denim and linen..."',
            "**B-roll keyframe.** Denim beat."),
    "S08": ("7 · Reason 4, longevity", '"...so you will actually wear this one for years."',
            "**B-roll keyframe.** Craft/quality beat, bag fills the frame."),
    "S09": ("8 · Conviction", '"I have carried mine every day since June and people still ask me where it is from."',
            "**B-roll keyframe.** Wide, the bag is small, she is being looked at."),
    "S10": ("9 · CTA", '"It comes in a bunch of colors, mine is the caramel. I will leave the link below."',
            "Calm frame with an empty upper third for the end card."),
}


def full_prompt(shot):
    return " ".join([shot["keyframe_prompt"], M["product_lock"], M["flap_closed_pin"], M["style_line"]])


L = []
w = L.append

w("# VEL-SOFIA-ONEBAG-01 — Image Prompts")
w("### Every image in the video, ready to paste\n")
w(f"**Product:** {M['product']} · **Frames:** 10 · **Aspect:** 9:16\n")
w("---\n")
w("## How to run these\n")
w("| | |")
w("|---|---|")
w("| Engine | kie.ai `gpt-image-2-image-to-image` |")
w("| Reference image | `caramel 1.png` — wire it as the **only** input image on every one of the 10 |")
w("| | (vault: `brands/velantra/products/straw-birkin/product-images/straw birkin/`) |")
w("| Aspect ratio | `9:16` |")
w("| Resolution | `2K` for S01–S05 + S10 (held on screen). `1K` is fine for S06–S09 (they get animated to 720p). |")
w("")
w("These are **image-to-image**, not text-to-image. Without the caramel reference wired in, the flap "
  "geometry and the crossed belts will not come out right — that is the whole reason this bag renders "
  "correctly. Straight text-to-image reinvents the closure every time.\n")
w("Each prompt below is complete and self-contained. Copy the whole block.\n")
w("---\n")
w("## What's in every prompt\n")
w("Each one is four parts glued together: the **scene** (unique per shot), then three fixed blocks that "
  "never change. The fixed blocks are ~80% of the word count and they are the reason the bag survives. "
  "Do not trim them to make a prompt shorter.\n")
w("1. **Scene** — composition, wardrobe, location, light, how the bag is held")
w("2. **Product lock** — the bag is the reference bag, top handles only, no invented straps or hardware")
w("3. **Flap + handles pin** — one seamless sheet folded all the way over, 2 separate handle loops, X belts")
w("4. **Style line** — the photographic look, plus the no-text/no-watermark guard\n")
w("If you write a new shot, keep parts 2–4 verbatim and only swap part 1.\n")
w("---\n")

for sid in [f"S{i:02d}" for i in range(1, 11)]:
    shot = next(s for s in M["shots"] if s["id"] == sid)
    beat, vo, note = BEATS[sid]
    kind = "b-roll keyframe" if shot["kind"] == "broll" else "still"
    w(f"## {sid} — beat {beat}\n")
    w(f"**Lands on:** {vo}  ")
    w(f"**Type:** {kind}  ")
    w(f"**Note:** {note}\n")
    w("```")
    w(full_prompt(shot))
    w("```\n")

w("---\n")
w("## Appendix — motion prompts for the four b-roll shots\n")
w("S06–S09 are animated from their keyframes on kie.ai `kling-3.0/video` "
  "(`mode: std`, `sound: false`, first frame = the keyframe above).\n")
w("**The one rule that matters:** when the bag is small in frame, telling Kling to *carry it still* is "
  "not enough — it will reinvent the closure mid-clip. Take the locomotion out of the shot entirely and "
  "let the person, the hair and the light carry the motion. S06 mutated on the first pass with a walking "
  "prompt and passed once the walk was removed.\n")

for sid in ["S06", "S07", "S08", "S09"]:
    shot = next(s for s in M["shots"] if s["id"] == sid)
    w(f"### {sid} — {shot['dur']}s\n")
    w("```")
    w(" ".join([shot["motion_prompt"], M["kling_flap_pin"], M["imperfections"]]))
    w("```\n")

w("---\n")
w("## QA every frame before it goes anywhere\n")
w("Regenerate on sight if any of these fail:\n")
w("- Flap is one continuous sheet across the whole top. The notches between the centre panel and the two "
  "outer tabs start about halfway up and **never reach the top edge**.")
w("- Exactly **2 rolled handles**, two separate clean loops, well apart. Not collapsed, bunched, or fused "
  "into a mass over the centre panel.")
w("- Exactly **2 belt straps**, crossed in an X. Never merged into one horizontal strap.")
w("- **Zero metal.** No buckle, turn lock, clasp, stud or ring. A glint of hardware is an automatic fail.")
w("- No shoulder or crossbody strap invented.")
w("- Bag holds its structured shape, sitting or hanging square. Not slumped.")
w("- Nothing protruding from the bag and no contents visible.")
w("- No text, watermark or logo anywhere in the frame.\n")
w("For the four clips, pull frames at roughly 10 / 40 / 70 / 97% and run the same checklist on each — "
  "Kling breaks the bag mid-motion from a perfectly clean first frame.\n")

open(OUT, "w").write("\n".join(L))
print(f"wrote {os.path.basename(OUT)}  ({os.path.getsize(OUT)/1024:.0f}KB)")
