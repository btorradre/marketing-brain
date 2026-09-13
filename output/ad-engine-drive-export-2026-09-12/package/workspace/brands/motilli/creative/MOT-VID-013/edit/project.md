# MOT-VID-013 editing sessions

## September 8, 2026 — reference breakdown and CapCut plan

Latest user instruction selects CapCut and requests ElevenLabs reference-voice cloning, with an editing plan first. Completed every-frame decode, consecutive-frame verification of 32 boundaries, eight transition filmstrips, fresh cached Scribe transcript, two audio-description passes, 33-shot reference analysis and 37-beat CapCut plan. CapCut 9.3.0 installation and plaintext draft schema checked read-only. No CapCut draft changed and no new voice cloned during the planning phase.

Next production work: resolve reference-voice rights or licensed voice ID, produce/review narration, align it, create isolated CapCut project and build three hook variants. Final voice must replace placeholder timing. Files: `reference-analysis/reference-breakdown.md`, `reference-analysis/capcut-editing-plan.md`, `reference-analysis/capcut-edit-plan.json`.

## September 8, 2026 — actual ad edited and exported

Executed in CapCut 9.3.0. Three native A/B/C projects and full MP4s delivered under `capcut/exports/`, with a local review page at http://localhost:8765/assets/mot-vid-013-edited-ad/review.html . Forty picture segments, 95 caption phrases, four seven-frame Horizontal Blur transitions, native ingredient labels, guarantee/CTA, ElevenLabs take 4 and quiet Motilli-library music. Actual export QA caught and resolved small text, CTA overlap, retained presenter framing in S06/S15/HC1, and quiet mix. Final output: 1080×1920, H.264/AAC, 30 fps, 96.633 seconds picture; full decode and exact caption/timing validation passed. Narration remains the clearly identified existing ElevenLabs voice, not a reference clone. See `capcut/README.md` and `capcut/manifest.json` for editable project paths and evidence.

## September 9, 2026 — 1.1× voice and synchronization revision delivered

User requested slower narration, dead-space removal and B-roll sync. Wrote the revision editing plan first. Returned to original ElevenLabs take 4, independently aligned/transcribed actual speech, removed 31 quiet intervals (10.34 source seconds), and rebuilt all 40 picture segments, 95 captions and labels in separate native R2 A/B/C projects. Every voice segment is exactly 1.1×. Actual-export analysis revealed a consistent two-frame renderer delay; corrected picture/text cues and verified final audio retains measured timing. All 291 script words are present; maximum caption/B-roll cue error is 59 ms, excluding immediate opening picture. Clean audio headroom, full decode and visual QA passed. Three 1080×1920/30fps H.264/AAC exports, 95.9 seconds picture. Review page serves R2 files; old exports/projects preserved. See `capcut-r2/README.md`, `manifest.json`, `final-qa.json` and `exports/`.

## September 9, 2026 — all hook variations duplicated

User approved the 1.1× correction and requested duplicate projects for all hook variations. Wrote `hook-variations/editing-plan.md` first. Created three separately named native CapCut projects: HOOK-A-Remedy-Cabinet, HOOK-B-Still-Backed-Up and HOOK-C-Another-Morning (all prefixed MOT-VID-013-). Each preserves its approved R2 content exactly, with the two-shot visual hook joining the common body at 5.000 seconds. Shared spoken hook is intentional per the approved plan. All three duplicated projects opened and exported successfully; full decode, audio correlation and nine actual-export picture comparisons per variant passed. All six hook shots and body joins visually inspected. New full-ad downloads and project details are in `hook-variations/`; review: http://localhost:8765/assets/mot-vid-013-hook-variations/review.html . Prior projects and exports remain available.

## R3 — CapCut route confirmed, all original hook projects revised

User clarified CapCut and requested the original three hook-variation projects as bases. Created separate native R3 copies, applied 24 picture replacements to each, retained all original narration at 1.1×, captions, audio fades and mix, preserved original hooks and delayed celery to the apigenin line at frame 1387. All three exports reviewed and delivered: http://localhost:8765/assets/mot-vid-013-revised-r3/review.html. Technical, full-decode, black-frame, audio-parity, body-parity and review-page QA passed. Source selection and all 39 rendered A cut boundaries manually inspected; full-video Gemini 3.8 Flash review returned pass. See `visual-variety-r3/capcut/manifest.json`. Podcast remains on hold for approval.
