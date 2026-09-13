# Handbag detail-film surface cleanup — September 6, 2026

The seven handbag detail films were retouched to remove the reported hairlike lines, etched patterns and exaggerated surface noise. The edit retains the original shot order, cut frames and duration. Revision 2 restages fifteen wide shots from authentic or approved product references in the same studio style; framing and lighting change modestly to preserve product construction and avoid propagating the defective texture. GPT Image 2 edits provide clean reference frames; tracked retouches carry these repairs through the original footage. HyperFrames 0.8.30 assembles and renders the complete films under the owner's explicit instruction to use the HyperFrames skill.

| Film | Shots | Frames at 24 fps | Duration |
| --- | ---: | ---: | ---: |
| Vivienne | 13 | 520 | 21.667 s |
| Weekender / Eleanor | 10 | 432 | 18 s |
| Meridian | 10 | 432 | 18 s |
| Camille | 10 | 432 | 18 s |
| Delphine | 10 | 432 | 18 s |
| Colette | 10 | 432 | 18 s |
| Juliette | 5 | 216 | 9 s |

65 of 68 shots use retouched or restaged plates; three retain their original source frames. Six wide product reference plates were regenerated in revision 2, and two Weekender handle shots were replaced. All thirteen Vivienne repairs from the earlier revision are retained. Native-resolution surface crops and repaired moving frames were reviewed. Fine material grain remains; this is not a claim that every generated surface pixel is artifact-free. Leather grain, canvas weave, wool nap, suede, seams and hardware were reviewed against the source for each family. Product dimensions were not independently measured. These exports are edited derivatives, not untouched generator output.

The delivered Shopify review draft is **151397859393**, “Velantra — Storytelling + Films · Sep 6” (unpublished). It contains the product-storytelling changes and all seven films. The earlier shared draft **151389143105** was being concurrently edited; the review version was isolated rather than overwriting that work. The live theme **151364960321** was not written or published by this task.

[Preview the draft](https://velantrafashion.com/?preview_theme_id=151397859393) · [Open the editor](https://admin.shopify.com/store/uzdgxy-sb/themes/151397859393/editor)

## Reproducible sources

- `shots.json`: original source paths, exact cut frames, selected repairs, anchors and tracking modes.
- `assets/`: original and cleaned reference images, including additional border references where needed.
- `plates/`: repaired moving shots and first/anchor/last samples.
- `track_retouch.py`, `process_ready.py`: repair propagation. Three handle close-ups use a robust smooth fit of the measured affine camera trajectory to suppress tracking jumps.
- `build_composition.py`: exact frame-aligned HyperFrames assembly; `assembly/` retains each family composition.
- `exports/`: seven complete 1920 × 1080, 24 fps films.
- `shopify/uploaded-files.json`: authoritative final Shopify video and poster records.

## Verification evidence

- `qa/revision-2/*-check.json` (six new renders) and the retained Vivienne check: HyperFrames lint, runtime and layout checks.
- `qa/*-export/verification.json`: every rendered frame checked against its intended source or repaired shot; duration, frame count and all cut boundaries verified.
- `qa/*-contact-*.jpg`: first, anchor and last frame of every shot, visually reviewed with full-resolution inspection of problem regions.
- `qa/motion-continuity.json`: adjacent-frame checks inside all 68 shots, excluding intentional cuts.
- `shopify/revision-2-cdn-integrity.json`: SHA-256 comparisons for all six new exports; the unchanged Vivienne export retains its earlier verification.
- `qa/revision-2/film-storefront-151397859393/report.json`: final draft verification for the homepage and eight PDPs at desktop and mobile sizes, including correct media, autoplay, mute, loop, pause/resume and horizontal overflow.

Product-storytelling scope, validation and checkout evidence are documented in `qa/revision-2/PDP-STORYTELLING-DELIVERY.md`. No purchase was placed and the theme was not published.
