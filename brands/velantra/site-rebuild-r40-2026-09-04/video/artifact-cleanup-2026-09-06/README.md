> Superseded: user authorized HyperFrames for this correction on 2026-09-06. Active work is in `../edit/surface-cleanup`. Prior rejected video generations remain archived.

# Handbag surface-artifact correction

User scope: all handbag detail films. Remove the artificial squiggly/hairlike lines on physical bag surfaces. Preserve the approved cuts, sequence, bag geometry, materials, lighting and full duration. Includes the Vivienne homepage detail film and both Weekender product listings.

Status: **incomplete; no replacement media deployed**. Original Shopify files and theme bindings are unchanged.

## Tested corrections

- Weekender v1: stateful Google Omni edit using the accepted final interaction. Rejected: output shortened from 18 to 9 seconds, invented a rear/handle-root panel in the final shot, and did not fully clean the surface. Never deploy.
- Weekender v2 and Juliette v1: provider rejected the combination of explicit `task: edit` and `previous_interaction_id` before generation. These are failed requests, not deliverables.
- Juliette v2: direct original-video input with explicit `task: edit`. Output retained 9 seconds but changed cut timing and the final handle-only shot to the upper front panel, which still has excessive etched texture. Rejected. Never deploy.

Each attempt keeps its prompt, source SHA-256, provider receipt, original output bytes, and any QA frames in its own folder. No local video trim, transcode, retime, smoothing or assembly was performed. Rejected outputs are outside theme assets and native Shopify Files.

## Working requirements

1. Resolve the user's internal video editor app, URL or local launch path. An asynchronous text question is pending. The local `Documents/marketing-apps/adengine/packages/timeline` package is the timeline document/reducer only; the inspected repository has no implemented video editor/export entry point. Do not pretend it can export. Do not substitute HyperFrames, Remotion, CapCut or another editor.
2. Import each complete original from `../shopify-detail-films.json` and preserve its exact edit. The original source videos and accepted first-segment provenance are in `original-segments.json`.
3. Use localized surface cleanup with source-relative material fidelity. Canvas keeps tight weave, wool keeps short matte fibers, suede keeps natural nap, leather keeps fine grain and real folds. Remove exaggerated stray strands/etched squiggles, not seams, stitches or authentic grain. Inspect every shot at full resolution, including first and final frames and the Weekender 8.9-second shot flagged by the user.
4. Verify shot order, cut positions, full duration, geometry, hardware, crop safety and surface consistency through motion before uploading any replacement.
5. The previously working theme 151364960321 is now MAIN, freshly verified this turn. The connector permits theme-file writes only on UNPUBLISHED themes. Duplicate the current MAIN into a new correction draft when corrected media passes review, preserving latest merchant settings. Do not replace current live video file contents as a workaround.
6. Upload newly named native Shopify videos and clean posters; update only corresponding draft bindings. Vivienne also appears in `templates/index.json`; both Weekender handles share `templates/product.weekender.json`. Verify CDN original hashes and native desktop/mobile playback. Refresh delivery package and manifests only after accepted corrections exist.

The theme duplication operation has been schema checked and validated but has **not** been executed. No corrected draft exists yet.

## Exact material authorities

Read the router and each dedicated product skill in `/Users/brooksorradre2/.codex/skills/velantra-*-product`. The seven selected source images were visually reviewed during this audit. Preserve the current selected variant and view. Physical dimensions remain unverified; this task does not establish new scale measurements.

Provider reference: https://ai.google.dev/gemini-api/docs/omni (checked 2026-09-06). Uploaded video edits are limited to 10 seconds; the attempted stateful 18-second correction did not preserve the full result. Do not silently shorten films to meet this limit.
