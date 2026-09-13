# Colette Wool Tote: 100-clip organic B-roll library (2026-09-02)

Product source of truth: the six Colette reference images in `../../product-references/` and `../../product-images/square-1to1-2026-08-16/` (Caramel canonical 3/4, side, interior; Espresso hero, side, interior). No PDP or spec sheet was used to generate anything.

## What is here

- `BROLL_LIBRARY/` — 100 approved clips, 9:16, 720x1280, h264, silent, 3 to 8 seconds, sorted into the 13 category folders (14_Misc is empty by design). Filenames: `COL-###-<colorway>-<slug>.mp4`.
- `broll_manifest.csv` — one row per clip: shot spec, environment, orientation, action, duration, engine, keyframe path, full generation prompt, motion prompt, TikTok pattern reference, Gemini 3.7 Flash structural verdict and reason, ten Gemini scores, the human review verdict, the usable window that was cut, and notes.
- `research/organic_broll_research.md` — product analysis, uncertainties, Apify method, the organic visual grammar with frequencies, camera behaviour, environments, interactions, opportunities and the avoid list.
- `research/product_visual_reference_model.md` — what the images establish and what they do not.
- `research/tiktok_reference_dataset.csv` — 1,481 unique TikToks with metadata. `research/gemini_analysis.jsonl` — per-video visual breakdown for the 180 watched. `research/pattern_stats.json` — aggregate.
- `keyframes/<id>/vN.png` — every GPT Image 2 keyframe generated, rejects beside the pick. `state/picks.json` says which variant was used.
- `clips/` — the full 10-second animations before trimming; `clips_rejected/` — every animation that failed drift review, kept for audit.
- `scripts/` — the whole pipeline (see below).

## How each clip was made

1. Keyframe: GPT Image 2 image-to-image on Higgsfield with two product references attached (hero plus side, or hero plus interior for open-bag shots), one 9:16 frame per shot, 14 re-rolls where proportions or construction failed the structural gate.
2. Gate on the keyframe: Gemini structural check with explicit counts (handles, belt ends, disc caps, straps) plus a full-resolution human look at every flagged frame.
3. Animation: human-interaction shots went to Google Omni image-to-video (Omni 1.1 Flash from COL-070 onward, per Brooks's 2026-09-02 rule; the preview model before that). Product-only beats and the ten Details macros never went to a video engine: they are locked-off handheld-feel push-ins from the approved keyframe, per the house rule that hero-product beats do not go to Omni.
4. Drift review: four-point strips (0.5 / 3 / 6 / 9.5 s) of every animation, reviewed by hand. One re-roll budget; anything that drifted twice, grew hardware, or turned a face to camera fell back to the push-in. The usable window per clip is recorded in `state/human_review.json` and is what was cut.
5. Delivered-file QA: Gemini 3.7 Flash watched every trimmed file against the three references and returned a structural verdict with counts. 98 of 100 PASS; the 2 non-PASS are accepted deviations on record after a frame-by-frame human check (COL-039: the left disc cap is cropped by the frame edge for the first second, not missing; COL-041: sub-pixel flicker on the disc caps at full-body scale). COL-070 was regenerated with visible handles and passes.

## A note on the numeric scores

Gemini 3.7 Flash (and every Gemini model tried) compresses its 1-10 scores toward 6 to 7 for every clip, including ones it explicitly calls structurally accurate, even with anchored scale definitions. The numbers are in the manifest for the record, but they are not discriminative; the gate that actually decided approval is the structural verdict plus the human review column. Treat `gemini_verdict` and `human_review` as the approval, not `final_QA_score`.

## Editing notes

- Colourway is the trim only: 69 Caramel, 31 Espresso. Check the belt before cutting a variants beat.
- Faces stay out of frame, behind a phone, or turned away in every clip.
- No text, captions, UI or logos anywhere. Props are unbranded (matte dark laptops, plain phones).
- Cut from the start of each clip: the action is in the first 3 to 5 seconds and the trims already end before any late drift.

## Re-running

`scripts/research_crawl.py` (Apify crawl → select → download → frames) → `scripts/gemini_analyze.py run|stats` → edit `scripts/manifest.py` → keyframes via the Higgsfield connector (`kf_tools.py batch/scenes/save/sheet`) → `qa_clip.py frames` → `pick.py` → `omni_animate.py run` or `kenburns.py` → `clip_strip.py` + `review.py` → `distribute.py` → `qa_clip.py library` → `build_manifest.py`.
