# Sarah & Stone → Velantra Replication Briefs (Seedance 2.0 / Higgsfield)

Four fully-segmented prompt packs, cut-detected from the reference MP4s (`segments-<id>.json` = raw detector output; briefs note any manual merges/splits). Full ad teardowns in `../BREAKDOWN.md`.

| Brief | Ref | Product | Format | Segments | Lip-sync? |
|---|---|---|---|---|---|
| [brief-4-straw-tote-asmr-macro.md](brief-4-straw-tote-asmr-macro.md) **← produce first** | 20.5s | @straw tote | Silent ASMR macro unboxing | 11 (micro-cuts, gen 4s + trim) | No |
| [brief-2-bow-tote-editorial.md](brief-2-bow-tote-editorial.md) | 33.8s | @bow tote | "Meet the Bow Tote" music editorial | 8 | No |
| [brief-3-two-bag-talking-head.md](brief-3-two-bag-talking-head.md) | 35.0s | both | Quality review, bundle play | 8 (3 talking anchors) | Yes |
| [brief-1-straw-tote-unboxing.md](brief-1-straw-tote-unboxing.md) | 50.4s | @straw tote | Bedroom unboxing VO review | 10 (S1–S6 chained take) | Yes |

## Before generating
1. Register both products in Higgsfield as product entities so the tags bind: **`@straw tote`** (source: `brands/velantra/products/straw-birkin/product-images/straw birkin/caramel 1.png`) and **`@bow tote`** (source: `brands/velantra/products/bow-tote/product-images/velantra-bow-tote-scene-1.jpg`).
2. Per brief: generate the AVATAR once → KEYFRAMES (i2i from the listed product refs, never from scratch) → segments in the stated order.
3. Iterate 720p `fast`, regenerate winners 720p `std`. Captions/titles always in post (HyperFrames), never in Seedance.

## Standing rules baked into every prompt
- One camera move per prompt; concrete physical verbs only; 60–120 words.
- Identity lock + "keep @product identical to reference" negatives on every segment.
- Audio line in every prompt (lip-sync line for talking beats, named SFX otherwise).
- Duration = real segment length, clamped to Seedance's 4s floor with trim notes.
- Compliance: no handmade/artisan/origin claims anywhere (Velantra = made in China).
