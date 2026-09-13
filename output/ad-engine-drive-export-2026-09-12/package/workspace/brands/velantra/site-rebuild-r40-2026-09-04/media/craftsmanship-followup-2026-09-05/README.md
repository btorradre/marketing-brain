# Vivienne craftsmanship panels — September 5, 2026

Four square editorial details for the homepage timeline. These illustrate the selected Vivienne design; they are not documentary photographs of a factory or evidence of a manufacturing schedule.

The R40 timeline uses finished-material/product macros: overlapping leather texture, stitched leather edges, finished gusset edges and closure hardware. The local `reference-style-only/` files record that composition study. None was sent to the generation provider or included in delivered artwork.

Every panel uses only `VIVIENNE-MASTER-chocolate-front.png`, selected by Brooks on September 3, as its image input. The intended Chocolate appearance is a soft, dark, pore-grained body with smoother warmer contrast trim, a braided upper edge, rolled handles, inward belt ends and a horizontal oval gold center fitting. No unseen back, lining or opening sequence is constructed here. Physical measurements and material composition remain outside this imagery's evidence.

Production uses model `gpt-image-2-image-to-image`, `1:1`, `2K`, through the existing `_engine/mcp/ad-engine/engines/kie.py` engine. `run_gpt_image2.py` only submits and polls that engine, preserving its job/asset registry and credit checks. It does not define new endpoints. `prompts-and-provenance.json` records the exact prompts, source hash, job IDs, outputs and alt text. `receipts/` preserves returned jobs.

Final approval requires visual comparison of each generated crop against the selected master: local surface character and contrast, seam/braid pattern, edge thickness, handle-root anatomy, original hardware count and orientation. `qa.json` records the completed inspection separately from provider success. No new image should be treated as accepted based only on a successful provider task.

Use the four images with neutral detail descriptions. Do not attach unverified claims about leather grade, certifications, hand stitching, exact production time, waterproofing, or factory inspection standards. No HyperFrames, Remotion, video editor, theme mutation or store mutation is used by this task.

## Completed delivery

All four panels passed visual review. The first leather crop was retained; three first attempts were rejected for braid/attachment/hardware drift and regenerated from exact unaltered crops of the selected master. Accepted originals remain in `final/`; `web/` contains the requested 1024-pixel JPG filenames. `delivery-manifest.json` provides local paths, final provider URLs and alt text. Provider URLs return the untouched PNGs; upload the local JPGs when using `.jpg` theme asset names. The `341:272` center crop passed review at both full color and the theme’s reduced saturation.
