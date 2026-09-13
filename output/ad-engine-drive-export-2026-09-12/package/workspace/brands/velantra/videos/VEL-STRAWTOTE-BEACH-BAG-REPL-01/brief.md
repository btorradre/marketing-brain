# VEL-STRAWTOTE-BEACH-BAG-REPL-01

1:1 replication of the Sarah & Stone "a beach bag that does it all" TrendTrack ad
(share slug `sarah-and-stone-M3JBBU`, Meta ad 1425700312628789 / collation
3617263241744935, live 34 days, US straw-bags funnel) for the **Velantra Straw
Tote, caramel colorway**. Cast: **Tessa**. Pipeline: Emilia frame-replication
pattern (GPT Image 2 i2i keyframe per cut, Seedance 2.0 chain first_frame,
trim-stitch, Pillow serif overlay).

## Reference structure (11.73s, 720x1280, 30fps, music-driven, no VO)

Persistent on-screen hook the whole runtime, white serif, upper quarter:
**"a beach bag that does it all"** (post overlay in our version, never baked).

| Seg | Ref cut | Len | Shot |
|-----|---------|-----|------|
| 1 | 0.00-4.03 | 4.03 | Macro. Bag upright on navy/white striped beach towel on sand, water behind. Hand drops a sunscreen bottle inside. |
| 2 | 4.03-5.40 | 1.37 | Medium front. Woman at shoreline, bag at hip, reaches in and pulls out a compact digital camera. |
| 3 | 5.40-7.20 | 1.80 | Medium front. Camera raised to eye level, soft smile, takes a photo. |
| 4 | 7.20-8.77 | 1.57 | Back view. She photographs the ocean, bag hanging at her side. |
| 5 | 8.77-9.67 | 0.90 | Medium front. She drops the camera back into the bag. |
| 6 | 9.67-11.73 | 2.07 | Hero. Bare arm holds the bag up against sky/ocean, gentle sway. |

## Straw Tote adaptations (locked product truth)

- No metal, no clasp, no crossbody strap. The clasp-opening beat is replaced by
  sliding contents into the open woven mouth BEHIND the always-flat leather flap.
- Carried in the crook of the elbow / by the two rolled handles (segs 2-5),
  held up by BOTH rolled handles in seg 6.
- Back view (seg 4) shows the plain woven straw back face.
- Sunscreen bottle is a plain matte white bottle, no label text.
- All clips generated at fixed 6s, trimmed to the reference cut lengths at stitch.

## Files

- `reference/sarah-stone-M3JBBU.mp4` + `reference/segframes/` (full-res per-segment frames)
- `ref_frames/kf_src_0N.jpg` = composition source per segment (t0.2 / t4.2 / t5.6 / t7.4 / t8.9 / t9.8)
- `keyframes_gen.py` -> `keyframes/kf_0N.png` + `_916.png`
- `manifest_{a,b,c}.json` (2 segments each, chain mode, explicit first_frame) -> `segments/{a,b,c}`
- `stitch_final.py` -> `final.mp4` + `final_clean.mp4`

Finished deliverables go to
`brands/velantra/products/straw-birkin/concepts/7:18:26 - sarah stone beach bag/`.
