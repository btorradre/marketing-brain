# MOT-VID-013 — science-v2 visual revision

Completed September 8, 2026. Sixteen visuals replaced with GPT Image 2 keyframes and Google Omni native clips. Scientific anatomy and ingredient views now carry the digestive explanation. People appear only for the four literal normal-day activities (S32–S35); in variant A this reduces people/activity footage from 39.03 seconds to 10.17 seconds. Three hook versions and all 291 narration words are preserved.

## Review

- Motion gallery: http://localhost:8765/assets/mot-vid-013-science-v2-motion/review.html
- Storyboard: http://localhost:8765/b/mot-vid-013-science-v2
- Internal editor drafts: `output/science-v2/editor/MOT-VID-013-{A,B,C}-timeline.json`
- Selected sources: `science-v2-motion-picks.json`
- Every line and visual: `science-v2-line-audit.md`

All three internal timeline documents validate: 37 video clips, 70 caption groups, 9 callouts, zero visual gaps, 96.633 seconds each. The previously missing S22 now has a soluble-fiber material animation. Source clips remain unchanged provider MP4s (720×1280, 24fps); the original narration remains unchanged at the already selected 1.22× draft speed.

## Motion QA

All 16 new clips reviewed at four samples per second using Gemini 3.8 Flash. Flagged clips and both regenerated takes were inspected directly. Selected revised S12 removes sprouting fibers; revised S22 shows visible bubble movement despite the automated review incorrectly calling it static. Original versions and QA remain preserved. Decisions: `output/science-v2/motion/qa/selection-review.json`. Source-byte and narration/caption checks: `output/science-v2/handoff-checks.json`.

The gallery plays individual source clips and narration. These are complete editable timeline drafts, not final exported ads. Continuous editor playback, final pacing review and MP4 export remain pending the internal editor’s playback/export surface. No HyperFrames, Remotion or substitute compositor was used.


## Completed edit — September 8, 2026
The actual ad has now been edited and exported in native CapCut following the saved reference plan. Three full MP4s and editable projects are documented in `edit/capcut/README.md`. Review: http://localhost:8765/assets/mot-vid-013-edited-ad/review.html . Earlier timeline-only status above is superseded. Existing ElevenLabs narration is used; the reference clone remains pending.
