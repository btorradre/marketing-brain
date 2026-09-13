# Velantra PDP refinement — September 6, 2026

Weekender color correction: draft 151410507841 now has craft and value sections that follow the selected Weekender color on both listings. Cognac/Army Green/Espresso display canvas details; Black displays leather-specific images and text. See `weekender-all-colors-2026-09-07/README.md` for source provenance and 19 passed browser cases. This replaces the visible Army Green-only lower PDP treatment.

September 7 status: theme 151389143105 is now MAIN. The next unpublished draft is **151410507841 — Velantra — Order Status · Sep 7**. It adds order-availability/confirmed-lead-time messaging across PDPs while retaining the earlier corrections. See `order-status-2026-09-07/README.md` for current preview and verification. No actual production batch number or closing deadline has been supplied; fabricated scarcity was not enabled.

Single-paragraph correction: all 13 active Shopify product descriptions now retain only their first paragraph. In the draft, 25 body-copy fields across 12 product templates have likewise had their second paragraph removed, including lower craft/value introductions. Meridian's material fact and translation fallback are now exactly **Pebbled leather**, superseding the earlier vegetable-tanned wording for that product. October preorders and detail-film removals are preserved. See `single-paragraph/` for fresh backups, exact Shopify readback and browser checks. These changes supersede earlier two-paragraph copy artifacts and upload payloads; always refresh the current theme before further edits.

October correction: Colette and Vivienne are now clearly marked as preorders in all colors, with stock expected in October 2026 and dispatch afterward. Their earlier ten-day wording is superseded. Banner, lead-time fields, shipping accordions, global cart messages and fallback defaults are updated in the draft. See `october-preorders/README.md` for verification and remaining publication/policy limitations.

Latest user direction supersedes the film-regeneration work below: **remove all detail films from the website**. The homepage and all 12 product templates containing detail-film sections have now had those sections and their order entries removed in draft theme 151389143105. Shopify readback confirms zero remaining detail-film template references. The original files are backed up in `remove-films/`; media files were retained. The live theme 151364960321 still contains the films because the connector prohibits MAIN-theme writes and automated publication. Publish the updated draft manually in Shopify admin to make the removal live. The earlier request for an internal editor entry point is no longer needed for this removal task.

## Applied to Shopify

All 13 active product descriptions are now short narrative paragraphs. The copy describes each bag's silhouette, materials and visible construction; it contains no invented leather grade, tannery certification or measured capacity claims. `catalog-before.json` preserves the original descriptions. Exact Shopify readback matched all 13 updates.

## Ready in the unpublished theme

Theme **151389143105**, “Velantra — Detail Film Cleanup · Sep 6”.

- [Preview the draft](https://velantrafashion.com/?preview_theme_id=151389143105)
- [Open Shopify theme editor](https://admin.shopify.com/store/uzdgxy-sb/themes/151389143105/editor)

The 12 product templates serving 13 active listings now use consistent short paragraphs and Craft, Leather/Material, Lead time information. The user-supplied artisan experience, vegetable-tanned leather and 10-day lead time wording is incorporated where applicable. These are owner-provided specifications, not independent supplier certification. Camille retains canvas and contrasting trim wording because the trim composition is unresolved.

Details, Care, Shipping & delivery and Returns are contiguous 45px rows (46px for the final bottom border), with zero summary margin/padding and a 44px minimum interactive area. The excess spacing came from the global eyebrow margin plus summary padding. Paragraph bodies remain readable when expanded. Variant-specific material and lead-time behavior remains intact, including Black Weekender. Existing newer theme changes were refreshed and merged before upload.

All 26 desktop/mobile PDP checks passed: no horizontal overflow, no description bullets, four working accordion rows, correct compact heights, and visible 10-day lead time. Sixteen Liquid/theme files passed validation and matched Shopify readback semantically. Evidence: `pdp-qa.json`, `theme-validation.txt`, `deployment-receipts.json`, and the saved desktop/mobile buybox screenshots. `upload-files.json` is the final merged uploaded payload; do not rerun `reframe.py` blindly because later refinements were merged afterward.

## Manual Shopify actions still required

The connector's automatic safety review rejected `themePublish`: “Publishing a theme is blocked — making a theme live must be done manually in Shopify admin to prevent accidental storefront changes.” The working theme remains **UNPUBLISHED**. Main theme 151364960321 was not replaced. No alternative route was used to bypass this rejection.

Updating the shop shipping policy failed because the connector lacks `write_legal_policies`. `shipping-policy-proposed.html` contains the prepared 10-day processing wording, preserving the rest of the existing policy. The current live policy still says 1–2 business days of processing; update its Processing Time paragraph in Shopify Settings → Policies when publishing the draft. The requested ten days is before dispatch; delivery time is additional.

## Detail films — incomplete, no replacements deployed

Seven fresh Google Omni first segments and a Colette continuation were generated using approved product references, then rejected after full-resolution review for remaining surface artifacts or changed construction. Individual reasons are in `video/qa-verdicts.json` and per-film receipts. A GPT Image 2 cleanup reference improved the Colette wool macro; Google Omni's explicit edit produced a nine-second 720p partial repair. A native extension returned 18 seconds but changed earlier shots, reintroduced stray fibers and altered ending belt caps. It was rejected. A Juliette still cleanup candidate also remains unapproved. None of these outputs replaced store videos.

The native edit transport did not preserve the original 1080p resolution, and full-length extension did not preserve the approved repaired shots. Do not label the nine-second Colette candidate as an 18-second complete film, or use its failed extension. Provider MP4 bytes were retained without local trimming, retiming, transcoding or assembly. HyperFrames and Remotion were not invoked. Earlier files already present in the draft are not new deliverables from this work.

To complete the films, obtain the current URL or launch path for the user's internal video editor. Workspace/adengine documentation located so far describes a timeline schema but does not expose an implemented editing/export entry point. An asynchronous request for that location was sent; no reply had arrived when this handoff was written. Use the internal editor to replace approved regenerated shots while preserving complete sequences, then inspect every shot at full resolution and start/middle/end motion before changing Shopify media bindings.

Original durations to preserve unless the user changes the brief: Vivienne 21.666667 seconds; Weekender, Meridian, Camille, Delphine and Colette 18 seconds; Juliette 9 seconds. Product physical scale remains unverified from uncalibrated references.
