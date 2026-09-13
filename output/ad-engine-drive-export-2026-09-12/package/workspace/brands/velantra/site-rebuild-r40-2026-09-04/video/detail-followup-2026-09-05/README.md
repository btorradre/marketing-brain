# Vivienne detail film — production record

Status: accepted v5 native film, uploaded to Shopify Files and verified in the unpublished theme.

The sequence studies the R40 homepage detail film: a 21.6-second, 13-shot studio film with restrained camera movement and hard cuts. Its visual rhythm is adapted to the supported exterior of the Chocolate Vivienne. R40 footage is reference research only and is not used inside the produced film or as provider input.

The product source is the owner-approved September 3 Chocolate master. GPT Image 2 produced the checked charcoal-studio and opening-belt reference images in `references/`. Google Omni (`gemini-omni-1.1-flash`) generates the film directly through the Google Interactions API; native `previous_interaction_id` extensions produce a single cumulative MP4. No local editing, assembly, trimming or re-encoding is used. The MP4 returned by the provider is preserved. JPEG poster and review frames are read-only extractions.

The current internal editor/export entry point could not be verified from the documented current codebase, so no editor was invoked. See `workflow-evidence.json` and [Google Omni documentation](https://ai.google.dev/gemini-api/docs/omni).

`generate_detail.py` is the reusable generation source. Every paid submission has its exact prompt, reference hashes, provider interaction ID, requested response format and result receipt under `exports/`. Earlier rejected attempts are retained for traceability and must not be deployed. `shot-list.json` records the requested sequence and supported substitutions. Accepted output: `exports/v5/vivienne-detail-stage-3.mp4`, 21.666667 seconds of video, 520 frames at24fps, 1920×1080, 44,789,823 bytes. SHA-256: `7b70e72c1a7cd3234f09a480b16429f042c9ebb6e2d4613010b39838c04f5e4f`. Original Shopify CDN bytes match the provider output. Twelve planned hard cuts produce thirteen distinct views; scene analysis records ten high-contrast cut candidates at threshold0.20, with additional similar-leather cuts checked visually. Shopify delivery creates its own streaming renditions; the original provider MP4 remains unchanged.

The bag is a generated product visualization based on the approved image. Physical dimensions cannot be verified from these photographs. No unseen interior, zipper, rear construction, long strap mechanism or closure operation is represented. Side/body crops use only surfaces already visible in the master.

Responsive presentation: one native 16:9 file, `object-fit: cover`, desktop ratio 1434/726 and mobile 390/340, `object-position:50% 65%`. The final QA checks the complete bag and local detail subjects in both display crops.

Native Shopify Video: `gid://shopify/Video/30822907740225`, filename `velantra-vivienne-detail-film-2026-09-05.mp4`. See `../../research/vivienne-native-film-deployment.json` and `../../research/home-detail-followup-qa.json`. The cover is the full-bag view at2.5seconds; all poster/frame work is read-only extraction.
