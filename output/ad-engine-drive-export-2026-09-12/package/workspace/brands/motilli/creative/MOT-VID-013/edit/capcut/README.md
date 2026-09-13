# MOT-VID-013 — edited ad delivery

Three complete native CapCut edits and H.264/AAC exports are ready. Each picture is 1080×1920 at 30 fps, 2,899 frames / 96.633 seconds. Provider source footage is 720×1280 at 24 fps.

Watch and download: http://localhost:8765/assets/mot-vid-013-edited-ad/review.html

- `exports/MOT-VID-013-A.mp4` — Tried all of these?
- `exports/MOT-VID-013-B.mp4` — Still backed up?
- `exports/MOT-VID-013-C.mp4` — Another remedy. Still waiting?
- `MOT-VID-013.srt` — 95 phrases, exact 291-word script.
- `manifest.json` — voice, music, source overrides, native project locations and verified output hashes.

Open CapCut projects named `MOT-VID-013-science-CapCut-A`, `-B`, `-C`. Their complete native draft folders, caches and Resources are under `~/Movies/CapCut/User Data/Projects/com.lveditor.draft/`. Forty picture segments cover 37 narrative beats. Captions, labels, narration and underscore remain native editable materials. CapCut may organize nonoverlapping text segments into shared tracks.

The selected narration is the existing reviewed ElevenLabs Woman Over 40 take 4 at 1.22×. It is not the requested reference clone; permission/licensed-source resolution for that clone remains outstanding. The exact current narration and word timing were retained throughout editing.

QA: actual rendered frames for all caption phrases and all four consecutive-frame blur strips, plus revised remedy/pen/hook-C frames. Full output decode passed with no black gaps. Final mix measures -19.54 LUFS integrated / -1.72 dBTP. Audio waveforms correspond across all three variants (>0.9999999 correlation); AAC bytes need not be identical. See `qa/final-validation.json`, `qa/native-timeline-validation.json` and `qa/manual-review.json`.

Existing user drafts and provider media were preserved. `root_meta_info.before.json` is the pre-build CapCut registry backup. No social publishing or CapCut cloud export sync was used.

Build records: `build.py`, `refine_remedies.py`, `final_refine.py`, `finish_audio.py`, `export_variants.py`. Native structural mutations require CapCut to be fully closed; never rerun the builder against existing project folders. These scripts are production records, not necessary to edit the projects in CapCut.
