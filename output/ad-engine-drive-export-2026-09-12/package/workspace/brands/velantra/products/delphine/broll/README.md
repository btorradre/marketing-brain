# The Delphine — B-roll library v4 (real-seed rebuild)

**49 stills + 49 clips**, 9:16, Omni-animated. Built 2026-08-20 after Brooks rejected round 3
as still having "that 3D model sort of look". Approved on Cutroom board
`delphine-broll-v4-rebuild` before animation. Reusable across every concept — point new work
at `stills/` and `clips/` and only generate what is genuinely missing.

```
broll/
  stills/                49 approved keyframes        <- THE LIBRARY
  clips/                 49 Omni clips                <- THE LIBRARY
  animate_v4.py          launch/poll/drift-QA for this set
  _rebuild-2026-08-20/   REBUILD-PLAN.md, SCENE-MAP.md, seeds/, picks/, all renders
  _library/state_v4.json Omni job state (resumable; clips are immutable)
  _library/qa_v4/        first/last frames + drift_report.txt
  _superseded-2026-08-20/ the rejected v3 library (58+58)
```

## Why v3 failed and v4 works — THE LAW FOR ANY FUTURE REBUILD

v3 wrote scene premises as prose (moments, foreground occlusion, wardrobe — all the Colette
rules) and still read as motion-design, because the model imagined the scenes from text.
**v4 seeds every frame from a REAL reference frame** (Mode A of
`feedback_hyperreal_broll_real_ugc_seed`): real TikTok/IG footage sourced per-category, plus
Brooks's own iPhone photos/videos of the AG 25cm. The seed supplies lighting, camera height,
grain, DoF and composition; the real-product refs supply GEOMETRY AND MATERIALS ONLY. The
prompt frame: "your output is the next frame from the same phone in the same place."

Situational awareness gate: every scene has a nameable moment (she just sat down, she's
paying, she's packing). If the moment can't be named, it doesn't get generated.

## Coverage

street/carry 13 · cafe 4 · car 4 · home 10 · packing/chair 6 · open bag 4 · flatlay 2 ·
macro 8 (buckle, turn-lock, feet, grain, seam, handle base, clochette, corner).
Colorways: 23 LC / 14 DC / 12 AG. File names carry scene + colorway.

## QA that every frame passed

- 3D-tell check (waxy sheen, symmetry, editorial light, fake bokeh)
- Turn-lock block — held at MACRO distance this time (050)
- Straps horizontal through kelly plates to side roller buckles; no phantom straps
- Interior = BLACK fabric lining + zip (one caramel-lining fail caught and re-rolled)
- Capacity law: NO phone, NO sunglasses in flatlays/what-fits/packing scenes
- No competitor trade dress (a Damier-patterned pouch was caught and re-rolled)
- Numeric leather warmth consistent across LC set
- Faceless (library standard); ONE exception: `021-car-lipstick-LC` has a profile face —
  flagged on the board, kept by Brooks's animate-all call; treat as creator-adjacent
- Drift QA on all 49 clips: constant-distance held; 053 push-in caught and re-fired with a
  hardened locked-distance motion

## Motion rules (unchanged from v3, they were never the problem)

Constant-distance only: HOLD / DRIFT / OVERHEAD / WALK_AWAY / WALK_BY / CARRY / MACRO / HANDS
from `scenes_delphine.py`. NEVER push in on this 25cm bag — push-ins inflate it.

## Seeds provenance

`_rebuild-2026-08-20/seeds/tiktok/manifest.md` lists every source video URL, timestamp and
moment. Seed rule: frames with burned creator captions are DISQUALIFIED (text bleeds into
renders). Brand-account and sponsored footage rejected at sourcing.

Related: `../PRODUCT-TRUTH.md` · board `delphine-broll-v4-rebuild` ·
[[feedback_hyperreal_broll_real_ugc_seed]] · [[feedback_no_3d_render_look]]
