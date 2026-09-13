# Velantra white studio product photography

This package standardizes the public Velantra product catalog captured on September 4, 2026. The 13 active product records contain 68 variants and 185 gallery image positions. The two Eleanor Weekender handles use one canonical 33-image production set, resulting in 152 generated gallery assets mapped to all 185 original image positions.

Completed: all 152 final images are visually approved and encoded into 19.22 MB of theme-ready WebP assets. `VALIDATION.json` verifies complete source/variant/Shopify ID coverage. Each approval is pinned to the final PNG's SHA-256 hash.

The source product geometry, color, materials, hardware and useful view were preserved through image edits. Product and model photographs use white studio surroundings with diffuse lighting and a restrained contact shadow. Model carry views, packed interiors, trolley demonstrations and hardware close-ups keep their distinct purpose. A macro filled entirely by product material remains a macro; adding a white border would destroy the original detail crop.

## Reference study

The visual reference was [ARFORTI's ALIR product page](https://arforti.com/products/alir-gray-taupe), inspected September 4, 2026. Its gallery combines isolated products with ample pale studio space, restrained floor shadows, neutral model portraits and detail photographs. The production adopts those photographic qualities using Velantra's own catalog products. ARFORTI reference photographs are retained in `references/` for comparison and are not included in theme delivery assets.

## Files

- `production-manifest.json`: complete product, variant, original-image and generated-asset mapping, including both Shopify REST ProductImage and GraphQL MediaImage/ImageSource IDs, original Admin alt text, dimensions and review status.
- `studio-image-map.json`: flat mapping indexed separately by REST image, GraphQL media and GraphQL image-source ID.
- `theme-assets/`: compressed WebP copies intended for the new Shopify theme. Source image pixels are encoded without semantic edits; generated PNG originals remain intact.
- `generated/<handle>/`: final PNG images. Filenames include original source IDs.
- `sources/<handle>/`, `catalog-public.json`, `source-manifest.json`, `admin-image-alts.json`: catalog and source snapshots.
- `generation-jobs.json`: initial per-source prompts and original references. `receipts/` records generated file paths and the actual prompts used, including replacement attempts. For a corrected image, its highest numbered attempt is authoritative.
- `final-prompt-set.json`: exact final prompt per image, verified by matching the delivered PNG's SHA-256 hash to its original generation receipt.
- `qa/`: source and generated contact sheets plus per-job visual review results.
- `rejected/`: earlier outputs that failed visual review, retained for traceability and excluded from theme delivery.
- `build_delivery.py`: refreshes WebP encodings and mappings from saved PNGs and review records.

## Product fidelity review

Every generated view is compared visually against its source for silhouette, hardware placement, color/material, useful crop and demonstrated scale/context. Failures such as turning a close-up into an invented full bag or removing a model are rejected and regenerated from the original source with a specific preservation prompt. Per-job approval records are stored in `qa/review-status*.json` and copied into the production manifest.

All creative edits use the built-in `image_gen` tool. No alternative image-generation API or background-removal script was used. Pillow only reads images, assembles inspection contact sheets and encodes generated PNGs into delivery WebP format.

## Existing source inconsistencies retained for review

The source catalog contains conflicting depictions of two accessories and one Weekender detail. There was no verified product authority establishing which construction is current, so the source versions are preserved and separately regenerated.

- **Horse Charm / Verdant:** variant `42021263016001` is attached to source image `38959491383361` (position 6), which depicts a brown horse with a gold clasp. Source image `36065269973057` (position 5) depicts a green horse with a long green loop and white mane/tail. The variant label, color and construction differ across these source images.
- **Cherry Charm / Cherry Red:** variant `42682508542017` is attached to source image `38959489024065` (position 4), which depicts stitched red leather cherries with a green leaf. Source image `36093867262017` (position 1) depicts glossy red spheres on gold metal stems, a gold leaf and a keyring/chain. The Pink and Black source variants use the latter construction.
- **Weekender / Black detail:** source image `40845616087105` (position 32 on `velantra-weekender`) shows a horizontal oval clasp/flap arrangement, while the Black front and three-quarter images show a vertical oval clasp. The detail source was preserved; a speculative correction was archived and excluded from delivery.

Native catalog mappings and all source gallery images remain available. This image work does not change the live catalog, product variants, inventory or published theme.

Final delivery: 152 of 152 images were generated and visually approved. All 185 original gallery positions and 68 native variant image assignments are mapped to the new theme, including the cart drawer. Shopify CDN serves optimized encodings; dimensions and visual content were verified against delivery assets.
