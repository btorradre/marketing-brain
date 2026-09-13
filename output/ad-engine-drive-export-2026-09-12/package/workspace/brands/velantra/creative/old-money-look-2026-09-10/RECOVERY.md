# Current: R5 complete, September 11 2026

Latest caption-only revision completed across all nine ads. Nuamore reference captions inspected at native and enlarged scale. White Arial Regular lettering with black outlines around individual letters, no black boxes or shadows; fixed bottom-center near 88.75% height. Actual source font metadata unknown; rendered appearance reconstructed and compared using the same phrase. R4 exact copy, phrase timing, visuals, Weekender reveal cues, pause edits and 1.1× synchronized narration/presenter retained.

Delivery: `production/final-nine-ads-r5/` and `production/Eleanor-OldMoney-All-9-Ads-R5.zip`. Prior R4 preserved. Isolated Resolve project `VEL_Eleanor_OldMoney_R5_OutlineCaptions_2026-09-11` has exactly nine final timelines and nine Complete render jobs; probe timeline removed. Final DRP in delivery. Reproducible build and QA in `production/revision-5/`. QA Python uses `/opt/anaconda3/bin/python3` for OpenCV. Resolve mutations run sequentially through `production/resolve/run_lua.py`; do not interrupt another project render.

All nine exports decoded with no black frames; 333 caption graphs verified outline-only, exact R4 words/timing unchanged, audio correlation minimum 0.9999777. Visual review scope documented in QA report. ZIP CRC and nine hashes verified. Active Cut Room updated with 22 actual R5 composite assets, all verified accessible: https://cutroom-three.vercel.app/b/eleanor-old-money-nine-ad-storyboard . Editing plan updated; prior version retained as `edit/editing-plan-before-r5.md`.

Earlier state below is historical. Do not resume those pending steps.

---

# Current: R4 complete, September 11 2026

Latest user revision completed across all nine ads. New grids have four different white women in old-money outfits carrying distinct bags; larger bold high-contrast captions; Weekender revealed at H1 “This one gives you that classic” (5.300s), H2 “Just swap this in” (5.867s), H3 “That's where this one comes in” (8.967s). Quiet pauses tightened and voice + presenter native-retimed to 1.1× with pitch preserved.

Delivery: `production/final-nine-ads-r4/` and `production/Eleanor-OldMoney-All-9-Ads-R4.zip`. R4 Resolve project: `VEL_Eleanor_OldMoney_R4_110pct_2026-09-11`, nine final timelines, DRP in delivery. Complete QA and reproducible build scripts: `production/revision-4/`. Active Cut Room: https://cutroom-three.vercel.app/b/eleanor-old-money-nine-ad-storyboard — 22 new actual composites verified accessible.

All previous R3 exports preserved. Current editing plan is `edit/editing-plan.md`; older plan saved as `edit/editing-plan-before-r4.md`. Do not resume older pending steps below; they are historical.

---

# LATEST DELIVERY — all nine complete ads, old-money style first

Follow-up request checked against full approved scripts: every hook, entire bridge, body and CTA is present across all nine R3 exports. File hashes and durations verified; no missing sections found, so approved edits were preserved.

- Priority: production/final-nine-ads/01-Old-Money-Style/ (three complete H1 presenter variants).
- All nine organized: production/final-nine-ads/ . Each hook group includes its full approved script.
- Verified download ZIP: production/Eleanor-OldMoney-All-9-Ads-R3.zip . Nine MP4s, editable DRP, full scripts and coverage report; ZIP CRC passes.
- Coverage evidence: production/revision-3/qa/nine-ad-coverage-verification.json .

# CURRENT — R3 regenerated HeyGen / presenter on first hook — complete (2026-09-11)

Latest user reference: https://app.trendtrack.io/share/ads/nuamore-8cnpbi . All 738 source frames inspected, including consecutive native cut boundaries; source media and audit in edit/reference-analysis/nuamore-8cnpbi-r3/.

- Deliverables: production/revision-3/exports/ — nine MP4s, Eleanor-OldMoney-R3.drp, README.md and DELIVERY.json with exact hashes. All nine final Resolve jobs report Complete.
- Nine NEW HeyGen videos generated from exact selected Woman Over 40 / Eleven v3 Creative MP3 files, using approved A1/A2/A3 looks. Job states and native outputs in revision-3/avatars/. Existing narration, speed and deadspace cut maps preserved.
- Continuous background-removed presenter lower-left from frame zero through CTA; reference-style small white phrase captions. No full-screen bridge or presenter flashes. Corrected R2 background assets retained. Hook collage stays until named Eleanor introduction.
- Final source frame held 4/3/2 frames for H1/H2/H3 provider duration shortfalls. Fusion DeltaKeyer LowThreshold .18, HighThreshold .96, CleanBackground .1 removes faint residue discovered on ivory backgrounds. Earlier render passes retained under qa/, not final exports.
- Isolated Resolve project: VEL_Eleanor_OldMoney_ContinuousPresenter_R3_2026-09-11. Prior projects preserved. Source media still references this workspace.
- QA: revision-3/qa/final/report.json (all 14,202 export frames decoded; audio preserved; presenter source correspondence checked at base cuts), key-background-residue.json (every-frame empty-key-strip comparison), render-completion.json (under revision-3/resolve/). Actual visual inspection scope is recorded explicitly; do not claim every export frame was manually watched.
- Cut Room: https://cutroom-three.vercel.app/b/eleanor-old-money-nine-ad-storyboard . 616 cards; 32 new actual selected/reference assets hash-verified through cloud storage and deployed asset API. Active scene cards show R3 composites; new reference is in its own lane. Earlier reference lanes, V1 archive and human notes preserved.
- Documented difference from reference: approved voice-only mix retained because no suitable documented alternate music bed was found. No competitor music copied.
- Resolve automation: production/resolve/run_lua.py, now explicitly activates Resolve before the menu click. Another MOT project is being edited concurrently; always save and check the active project, avoid interrupting active renders, and operate only on the isolated R3 project.

---
Historical recovery notes follow; R3 supersedes conflicting presenter and caption instructions.

# CURRENT — corrected R2 ads complete (2026-09-11)

User rejected the C02 man shot and strap artifacts. Six GPT Image 2 selected corrections are complete, inspected and attached to active Cut Room cards. C02 is product-only luggage/bench still. C03/C10 straps and C04/C11/C13 flap slots corrected. Only C09 motion is selected; old C02 man still and generated clip are rejected historical assets.

- Deliverables: production/revision-2/exports/ (nine MP4s, Eleanor-RawPhone-R2.drp, README.md).
- Saved isolated Resolve project: VEL_Eleanor_OldMoney_RawPhone_R2_2026-09-11. Nine timelines; original projects preserved.
- QA: production/revision-2/qa/final/report.json and motion-source-comparison.json. All nine pass frame counts, decoding, static hold checks and approved-audio alignment. Boundary visual review complete; inspection scope documented honestly.
- Cut Room: https://cutroom-three.vercel.app/b/eleanor-old-money-nine-ad-storyboard
- Latest source selection: storyboard/raw-phone-r2/user-correction-manifest.json, storyboard/body-beats-r2.json.
- Working Resolve control remains in-app Lua via production/resolve/run_lua.py; external scripting is unavailable. Preserve current project before switching.
- Resolve was restarted after running out of disk and saved R2 reloaded. Final seven jobs completed; resumed-seven-status.json confirms 100 percent. Avoid duplicating the export folder into a ZIP while disk space is low.

---
Historical recovery notes follow; superseded where they conflict with the current correction.

# CURRENT — Raw phone storyboard R2 restored (2026-09-11)

Latest user requested restoryboarding from Nuamore and Instagram references, raw phone-looking photos and B-roll, broader subject variety.

- Consecutive-frame visual audits complete: Instagram 2222 frames / 30 base photos, Nuamore 1465 frames / 28 base intervals plus internal jump. Audits and source media in edit/reference-analysis/raw-phone-r2/. Audio not auditioned.
- Active editing plan updated before generation: edit/editing-plan.md. Historical plan archived separately.
- 16 new selected GPT Image 2 images and prompts/QA in storyboard/raw-phone-r2/. Three new raw designer hook collages, 11 held body stills and two action first frames C02/C09.
- Cut Room restored: https://cutroom-three.vercel.app/b/eleanor-old-money-nine-ad-storyboard . 77 active/reference image uploads hash-verified, exact copy verified, old 309 cards preserved as archive.
- Approved Woman Over 40 Eleven v3 Creative audio, deadspace trims, A1/A2/A3 presenters retained. New board removes ongoing inset and intermittent presenter body returns; bridge is intentional full frame.
- Next production: Google Omni motion for C02/C09, all-frame source QA, then check current Resolve connection and build isolated R2 timelines. Preserve original V1 projects and exports below. No new moving B-roll or final exports yet.

---
Historical recovery record follows:

# Eleanor old-money ads — completed

User requested all nine ads, Woman Over 40 / Eleven V3 Creative, DaVinci Resolve, and removal of dead spaces. All nine final MP4s and the editable DRP are completed and verified.

Delivery: production/Eleanor-OldMoney-9Ads.zip (nine MP4s, DRP, README, hashes). Individual files: production/exports/. Durations H1 51.3s / H2 54.8s / H3 51.7s, each crossed with three selected presenters. Voice/copy/speed preserved; deep silence cuts synchronized across all tracks. No authored on-screen text.

Native project VEL_Eleanor_OldMoney_9Ads_2026-09-11 exists and is saved. Previous MOT-UGC-YAPPER-01 v7 V3 20260910 project was saved and preserved. External Python remains unavailable, but supported in-app Lua works: production/resolve/run_lua.py writes a task-specific user Utility script and invokes it through AppleScript, returning tagged diagnostics through ResolveDebug.txt. Use that route for authorized revisions. Do not recreate the project or regenerate paid assets. Fusion edits on imported clips required ExportFusionComp/ImportFusionComp to commit; finish-template.lua records the working route. Current narration media is lossless WAV, avoiding a measured MP3 decoder offset.

QA: production/qa/final/file-frame-audio-checks.json, presenter-frame-correspondence.json, review-adjudication.json. All 14,202 frames scanned for black/green failures; all 54 voice comparison windows have zero measured offset and correlation >0.99999. Several model review flags were contradicted by actual images and byte-identical audio; adjudications retained. No claim of exhaustive human listening/full-resolution frame review.

Cut Room finished production previews are saved and verified:
https://cutroom-three.vercel.app/b/eleanor-old-money-nine-ad-storyboard
