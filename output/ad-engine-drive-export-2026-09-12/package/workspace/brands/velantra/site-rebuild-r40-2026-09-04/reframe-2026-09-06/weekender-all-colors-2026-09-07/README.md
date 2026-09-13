# Weekender details for all colors — September 7, 2026

Saved in unpublished theme **151410507841 — Velantra — Order Status · Sep 7**. Preview: https://velantrafashion.com/products/velantra-weekender?preview_theme_id=151410507841

Both `velantra-weekender` and `the-eleanor-weekender` use the shared Weekender template. Their craft and value sections now follow Cognac, Army Green, Espresso and Black selections. Canvas wording applies to the first three colors; Black has leather-body/no-canvas wording. The fixed brown-trim description is replaced with Leather trim. The remaining body description and details accordion already describe the color distinction correctly.

Added `snippets/weekender-variant-details.liquid`, enabled it only in the Weekender craft/value sections, and added translation strings. It uses the selected listing's existing Shopify variant images as CSS detail crops, preserving the supplied source pixels. The four cards show body texture, stitching, corners and handles. The value image and material row change with the color too. No generated image, recolor, new angle, video or scale claim was created.

Source provenance: `catalog.json` records both listings' current variant image URLs and color labels; the four canonical downloads and QA contact sheets record what was inspected. The product skill flags historical closure/interior conflicts in the existing galleries. The delivered crops focus on material, corners and handle arcs, excluding the disputed center-closure orientation and interiors; this does not certify the full gallery's construction or physical dimensions. The lower value crop also preserves the existing source's body and trim without showing the central closure.

Nineteen browser cases passed: all four colors across both listings at desktop/mobile widths, with color switching and direct-variant reloads in each case; Black initially renders correctly without JavaScript on both listings; unrelated Meridian sections remain unchanged. Image loading, crop layout, horizontal mobile keyboard scrolling, material table content, one-paragraph descriptions, no detail films and no page-width overflow were checked. Desktop screenshots for all colors and Black's mobile value panel were visually inspected. `qa.py` and `qa.json` contain the checks.

All five files passed Shopify theme validation and final semantic/exact readback. Section schemas were uploaded before the template enable flags because Shopify initially dropped unknown settings during a combined upload. `upload-files.json` is the final payload; if replaying, apply section schemas before the template.

The live theme was not changed. Manual publication in Shopify admin is required under the connector's established publishing restriction.
