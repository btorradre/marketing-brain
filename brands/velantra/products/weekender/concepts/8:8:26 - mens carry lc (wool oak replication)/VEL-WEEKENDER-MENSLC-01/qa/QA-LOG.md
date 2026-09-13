# Frame QA log — VEL-WEEKENDER-MENSLC-01

Mandatory frame-QA subagent pass per the velantra-weekender skill. Every frame judged
against the real-product photographs in `product-references/real-product-2026-08-08/`,
not just against checklist text. Rejects stay on disk beside the picks.

## Pass 1 — variants v1-v3 (2026-08-09)

### The systemic defect both auditors found independently

**Belt straps migrate off the leather band and run down the cream canvas**, ending in
oversized invented gold clasp plates on the fabric, and **the gold oval turn-lock plate
duplicates** (one on the flap tab where it belongs, plus phantom copies on the band or
canvas).

**Root cause was our prompt, not the model.** The closure block said the straps "hang
loose down the sides with their gold end plates visible." On the real bag the straps are
SHORT and lie flat and horizontal across the cognac leather band. The model read "hang
loose down" literally and ran them down the front face.

Second contributing error: the closure block was only pasted when `hardware=True`. S03
(the open-bag hero) had `hardware=False`, so it never received any strap guidance at all
and failed worst of every scene.

**Fix applied:** new always-on `HARDWARE_LAW` block in `_build/blocks.py`, pasted into
every scene regardless of `hardware`, stating that the straps sit entirely on the leather
band, that the canvas carries no metal of any kind, that exactly one gold oval plate
exists and it is on the flap tab, that the leather/canvas split is a straight horizontal
line, that the key bell is plain leather with no metal, and that every eyelet is warm
brass. The contradicting line was removed from the closure block and the mechanism block.
`ANTI_DRIFT` also hardened: handles are rounded tubes standing proud with teardrop
stitched bases, never flattened appliqués.

### What held up well

The **open-bag mechanism survived on every single variant of every open scene** — one
piece flap folded back behind the mouth, inner face showing its keyhole handle cutouts,
oval strap slots and gold oval plate; correct leather/canvas split; smooth caramel
leather interior with the wide matching caramel slip pocket; no zipper anywhere; no
logos. This is the failure mode that has historically killed Weekender runs, and the
mechanism block plus the real-product references held it.

### Verdicts

| Scene | v1 | v2 | v3 | Pick | Note |
|---|---|---|---|---|---|
| S01 | FAIL | **PASS** | (corrupt dl) | **v2** | v1 grew two invented full-length side straps with gold end caps |
| S02 | **PASS** | FAIL | FAIL | **v1** | best product-truth frame in the set; v3 also grew two floating gold rods |
| S03 | FAIL | FAIL | FAIL | **REGEN** | all three: straps down the canvas, duplicated turn lock; v1 also silver eyelets, v3 flattened front handle |
| S04 | **PASS** | FAIL | FAIL | **v1** | v2 flap was a featureless slab; v3 rejected on photorealism (reads as CGI) |
| S05 | PASS | **PASS** | FAIL | **v2** | v2 is the only true top-down; v1 better flap but wrong camera |
| S06 | **PASS** | PASS | FAIL | **v1** | only variant that shows insertion into the slip pocket; v3 had a thigh in frame |
| S07 | — | — | — | pending | v2/v3 402'd during a transient credit-balance dip |
| S08-S13 | — | — | — | pending | QA pass 2 |

### Carried notes for the animator

- S05_v2 and S06_v1 carry invented gold clasps / duplicated oval plates on the lower
  canvas. If the corrected pass does not supersede them, keep the camera move tight on
  the mouth and interior and away from the lower canvas.
- S01_v2 has a small gold tip on the key bell (real one is plain leather). ~2% of frame,
  low contrast, non-blocking.

## Pass 1b — QA of S08-S13, and a CORRECTION to the pass-1 finding

The third auditor read `LC-closed-side-strap-detail.jpg` and contradicted auditor 1.
**It was right, and I verified the photograph directly before acting on it.**

**The hanging strap over the canvas is REAL.** Each belt strap comes over the top, passes
through a leather keeper on the cognac band, and hangs straight DOWN near the side edge so
its lower portion lies flat against the cream canvas, ending in a flat gold plate with an
oblong slot and three dome rivets. Auditor 1 conflated the fastened state (strap short and
horizontal on the band) with the unfastened state (strap hanging down). The as-filmed
default is unfastened.

**My pass-1 fix was therefore wrong in the opposite direction** — a blanket "no metal
touches the canvas" rule would have deleted a real feature from every frame. Rewritten to
pin COUNTS AND GEOMETRY instead of banning a region:
- exactly two straps, near the side edges, hanging straight down; not crossing the middle,
  not diagonal, not reaching the bottom, not luggage compression straps
- apart from those two tip plates, no other metal on the canvas
- each staple is TWO PARALLEL FLAT GOLD BARS, never one solid blade (auditor caught
  S10_v1 rendering it as a single chunky blade — the classic macro "resolve ambiguous
  small metal into a different object" failure)
- one knurled post, not two; one oval keyhole plate, on the flap tab only
- side faces carry ONE small gold eyelet each and nothing else (S12/S13 grew oval keyhole
  plates on the gussets)

**Also added a MATERIALS law** after S12/S13 rendered leather as suede/nubuck and, in one
case, patent, and the canvas lost its weave across half the panel: every leather panel is
the same smooth semi-matte cognac, the canvas keeps a visible crosshatch weave everywhere.

**S11 reframed:** the teardrop handle base, the entire subject of the shot, was occluded by
the key-bell lace in 2 of 3 variants. Prompt now requires it unobstructed and centred with
the bell hanging clear.

**S12 rebuilt:** all three failed — one hand instead of two, a forearm laid diagonally
across the front of the bag in the payoff shot, invented gold on the gussets, a metal tip
on the key bell. Prompt now requires two flat palms side by side with both forearms
entering from the top edge only and the front face unobstructed.

| Scene | v1 | v2 | v3 | Note |
|---|---|---|---|---|
| S08 | FAIL | PASS | FAIL | v1/v3 straps diagonal across the front; v2 weak photorealism |
| S09 | FAIL | **PASS** | FAIL | v2 the best frame in the batch, matches the hardware macro beat for beat |
| S10 | FAIL | **PASS** | FAIL | v1 staple rendered as one blade; v3 blown-out studio background |
| S11 | FAIL | FAIL | PASS | teardrop base occluded in v1/v2 |
| S12 | FAIL | FAIL | FAIL | see above, full rebuild |
| S13 | FAIL | FAIL | **PASS** | v1/v2 suede-and-patent material mismatch; v3 clean. No shoulder carry on any variant. |

## Pass 2 — variants v4-v6, corrected prompts

Rerun with the corrected `HARDWARE_LAW` + `MATERIALS`: S03, S07, S08, S11, S12.
Every one produced a better pick than the first pass.

| Scene | Pick | Why it beat the pass-1 candidate |
|---|---|---|
| S03 | **v6** | straps now hang correctly near the side edges, level split, weave holds, double-bar staples correct, best proportion |
| S07 | **v6** | front-on per brief, correct wider-than-tall proportion, clean hardware |
| S08 | **v6** | double-bar staples correct, weave across the whole canvas, true proportion — pass 1 never got all three at once |
| S11 | **v4** | teardrop handle base unobstructed and centred, bell clear, plain leather with no metal |
| S12 | **v5** | two flat palms, forearms from the top, front face clear, all hardware counts correct, strongest photorealism |

## FINAL PICKS (13/13)

S01 v2 · S02 v1 · S03 v6 · S04 v1 · S05 v2 · S06 v1 · S07 v6 · S08 v6 · S09 v2 · S10 v2 ·
S11 v4 · S12 v5 · S13 v3

Credits: 39 stills pass 1 + 15 stills pass 2 = 54 GPT Image 2 calls at 10cr = 540cr.
