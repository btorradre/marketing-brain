# VEL-SOFIA-CARRYALL-01 — "Your Summer Carry-All"

**Product:** Sofia Woven Tote, caramel
**Format:** 6.8s, 9:16, 720x1280, silent
**Deliverable:** `final/VEL-SOFIA-CARRYALL-01.mp4`
**Built:** 2026-08-08

## Reference

Vestirsi "Resort 26: Italian Summer", Meta ad `1518228100026834`, US, running
since Apr 8 (123 days at time of scan). Headline "Resort 26: Italian Summer",
LP `us.shopvestirsi.com/en-us`. Source: `_production/vestirsi_reference.mp4`.

**Why it works.** No claim, no VO, no offer. It sells a bag by selling the
place you would carry it. Nine cuts in 6.6s alternate macro texture against
full-figure movement, so the eye never settles and the weave keeps getting
re-introduced at a size you can feel. The text plate never changes, so the one
idea, summer carry-all, is on screen the whole time without ever being spoken.

## The cut, 1:1

| # | in–out | dur | shot |
|---|--------|-----|------|
| 1 | 0.00–0.57 | 0.57 | macro, bag at hip, head cropped off above frame |
| 2 | 0.57–1.37 | 0.80 | medium wide, walking away down the path |
| 3 | 1.37–1.87 | 0.50 | macro, bag lifted to chest |
| 4 | 1.87–2.47 | 0.60 | medium, half-turn back to camera |
| 5 | 2.47–3.10 | 0.63 | wide, walking toward camera |
| 6 | 3.10–3.73 | 0.63 | medium wide, same walk, closer |
| 7 | 3.73–4.37 | 0.63 | medium close, hand to sunglasses |
| 8 | 4.37–5.60 | 1.23 | extreme macro on the weave |
| 9 | 5.60–6.62 | 1.02 | medium wide from behind, walking away |

**Held 1:1:** tropical resort garden (thatched pavilion, frangipani, pale
concrete walkway), diffused overcast daylight with no hard sun, handheld
shallow-DOF editorial camera, oversized open white linen shirt + cream mini +
cream slingbacks + tortoiseshell sunglasses + frangipani at a low bun, and a
persistent centred Helvetica Neue Light plate at 47.8% frame height.

## The two departures, and why

**1. The bag.** Vestirsi's is a slouchy raffia hobo with knotted leather
handles. The Sofia is structured, with a one-piece leather flap and crossed
belts. Every carry is therefore re-blocked to top-handle rather than tucked
under-arm. This is the one thing that cannot be 1:1 without misrepresenting
the product.

**2. Text plate line 2.** The reference reads "as seen on @rosalieburns", a
real creator we do not have. Line 2 is the product name instead. Never invent
a handle.

## Watch-outs

- **Product-first opening.** Cut 1 is a macro of the bag, because the
  reference's is. Fine for MOF and retargeting; it is the pattern ruled out
  for cold TOF prospecting.
- **Needs music.** Ships silent. `_production/final-refsound.mp4` carries the
  reference's own audio and exists only as a timing check — do not launch it.
- **Model is deliberately recast.** The prompts force a different woman from
  the reference creator rather than letting i2i reproduce her likeness. Keep
  that line in place on any re-run, given Sofia's DMCA history.

## Pipeline

`_engine/pipelines/scene_replicator.py`, keyframe-first, no chaining.

    fetch -> scan -> image (GPT Image 2 i2i) -> QA -> animate (Kling 3.0) -> finish -> overlay.py

- `_production/build_job.py` authors `anchor_job.json` + `job.json`. Re-run it
  to regenerate either.
- Shared refs holding identity across all 9 scenes: `caramel 1.png` (product)
  and `refs/model_anchor.png` (model, cropped head-and-torso from the v1
  scene-5 pass with the bad bag excluded).
- `_production/overlay.py` burns the text plate. The runner's built-in overlay
  is a bold black-stroked UGC caption and is wrong for this ad; `overlay_text`
  is left null in the job.
- Scene 1 runs at `1K` in `scene1_job.json`. Its prompt is 5249 chars and
  GPT Image 2 hard-fails on ~5k chars at 2K.

**Cost:** ~110cr images (10cr each, 6cr at 1K), 630cr video (70cr per 5s Kling
clip), 9 clips.

## QA record

Rejected passes kept in `_production/refs/`:

- `_reject-v1-scene5` — chunky crochet weave, belts collapsed into one strap
  plus a hanging tab, mini silhouette.
- `_reject-v2-scene5` — scale fixed, belts still one strap plus a tab.
- `_reject-v1-scene1-toowide` — head in frame; the reference crops it off.

Fixes that worked, for the next Sofia run: name the product ref by position
("image 2"), then specify WEAVE, PROPORTION and BELTS as separate labelled
paragraphs. The belt X only resolved once described as two bands each angling
a specific direction with all 4 rounded tips visible, plus explicit negatives
(no vertical strap, no hanging tab, no buckle, no keeper).

All 9 clips audited at 0.2/1.6/3.2/4.8s. No flap splits, no invented hardware,
no weave mutation.
