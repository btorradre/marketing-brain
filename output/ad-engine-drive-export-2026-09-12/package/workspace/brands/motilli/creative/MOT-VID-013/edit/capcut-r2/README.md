# MOT-VID-013 — revised ad, September 9, 2026

Delivered all three opening variants at **1.1× narration**, with long pauses removed and B-roll/captions resynced to actual speech.

[Review the revised ads](http://localhost:8765/assets/mot-vid-013-edited-ad/review.html)

- MP4s: `exports/MOT-VID-013-R2-A.mp4`, `-B.mp4`, `-C.mp4`.
- Editable CapCut projects: `MOT-VID-013-R2-1.1x-A`, `-B`, `-C`; full paths in `projects.json`.
- 1080 × 1920, 30 fps, H.264/AAC; 95.9 seconds of picture.
- Original ElevenLabs take 4: 32 native audio sections at exact 1.1 speed. Removed 31 long quiet intervals totaling 10.34 source seconds, retaining short natural joins.
- Rebuilt 40 picture segments / 37 narrative beats, 95 captions and ingredient/offer labels. Preserved accepted visuals and four native blur transitions.
- Actual-export transcription verifies all 291 words. Maximum caption and scene-cut error: 59 ms (under two frames), excluding the intentional immediate opening picture. Four windowed audio lag checks are zero for each final variant; full audio correlation against the reviewed trial exceeds 0.99985.
- Mix: −20.47 LUFS integrated, −1.28 dB true peak. Full decode passed for all files; black-frame scan clear. Visual inspection and qualitative audio review passed. The model's invalid ending timestamp is excluded from timing evidence.

Previous projects/exports are preserved. Plan: `editing-plan.md`. Pause cuts and word cues: `timing.json`. Verification: `final-qa.json`, `export-sync-review.json`, `manifest.json`. First-export evidence: `qa/pass1/`.
