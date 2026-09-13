# VEL-STRAWTOTE-MEET-EMILIA-REPL-01 — "Meet the Straw Tote"

**Reference:** Sarah & Stone "Emilia" — https://app.trendtrack.io/share/ads/sarah-and-stone-Ii5P4b
(local: `reference.mp4`, 33.8s, 720x1280 @30fps, music-only "Am I Wrong", serif title overlay)

**Product:** Velantra Straw Tote — Caramel (lead colorway). Woven natural straw body,
caramel leather trim: wide top leather panel + fold-over center flap, exactly TWO rolled
leather top handles, TWO crossed leather belt straps on the FRONT face only, white contrast
stitching, braided cross-lacing on side edges. Back face = plain straw. No zippers.

**Creator:** Tessa (locked roster) — strawberry blonde curls, freckles, sage green knit.
Nails: short soft cream (replaces reference's lime green).

**Engine:** GPT Image 2 i2i (`gpt-image-2-image-to-image`) keyframes → Seedance 2.0
(`bytedance/seedance-2`) chain-mode i2v with `first_frame` per segment, via kie.ai.
Music + serif overlay added in post (Seedance/native text banned; overlay via Pillow+ffmpeg).

## Shot map (original → replica)

| # | src time | out len | gen len | original | replica |
|---|----------|---------|---------|----------|---------|
| 1 | 0:00.0 | 3.0s | 4s | Seated hero, creator raises navy bag, title overlay | Tessa on green velvet couch raises Straw Tote, smiles |
| 2 | 0:03.6 | 3.5s | 4s | Macro: bag propped on rattan chair, camera drift | Tote on rattan cane chair, slow drift over flap + belts |
| 3 | 0:07.0 | 4.5s | 5s | Extreme macro: nails trace gold zipper | Fingertips trace braided side lacing + leather strap |
| 4 | 0:12.0 | 2.5s | 4s | Table: hands flip magnetic flap open | Hands fold the leather flap open on white table |
| 5 | 0:14.0 | 2.0s | 4s | Open flap, gold snap, hand reaches in | Flap folded back, hand reaches into straw interior |
| 6 | 0:18.0 | 6.5s | 7s | What-fits montage: jar, wallet, brush, bottle | Tessa drops tan pouch, brush, mini bottle inside |
| 7 | 0:22.6 | 4.5s | 5s | Macro pack 2: daylight zipper S-curve | Daylight macro: weave texture + crossed belts drift |
| 8 | 0:28.0 | 3.0s | 4s | Table side profile, hand zips top | Side profile, hand smooths flap closed, rights handles |
| 9 | 0:32.0 | 4.3s | 5s | Final hero: both hands, big smile | Tessa holds tote to camera both hands, big smile |

Total out: 33.8s (matches reference cut-for-cut; trims applied at stitch).

## Overlay (post, 0:00–0:11, fade out)

- `MEET THE` — Didot caps, tracked wide
- `STRAW TOTE` — Didot large
- `from` / `Velantra` — Snell Roundhand script
- footer: `C O A S T A L  &  E F F O R T L E S S`

## Files

- `ref_frames/kf_src_NN.png` — full-res composition sources from reference
- `product_refs/` — Caramel Shopify CDN pulls (front / opened / coastal / dock)
- `keyframes/kf_NN.png` (+ `_916` crops) — GPT Image 2 outputs
- `segments/seg_NN.mp4` — Seedance outputs; `manifest.json` — runner manifest
- Finished videos moved to `brands/velantra/products/straw-birkin/concepts/7:18:26 - sarah stone meet the emilia/`
  (`meet-the-straw-tote.mp4` with overlay, `meet-the-straw-tote-clean.mp4` without)
