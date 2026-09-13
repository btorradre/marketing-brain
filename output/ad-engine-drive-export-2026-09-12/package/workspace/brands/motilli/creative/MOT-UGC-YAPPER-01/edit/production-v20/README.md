# V20 — 1.1× speed saved, export pending

Native Resolve timeline: `v20 FINAL - 1.1x Michelle` in project `MOT-UGC-YAPPER-01 v7 V3 20260910`.

Verified live readback: video and audio 110%, pitch correction true, both 8,573 frames (285.766667 seconds) at 30 fps. One linked nested V18 edit keeps all source layers synchronized and original V18 editable. Nearest-frame retiming selected. A superseded speed setup timeline is preserved separately; do not export that timeline.

No new MP4 exists yet. Resolve console/window became inaccessible and display capture failed during export. The first export attempt failed an assertion before artifact export; the prepared exporter now explicitly finds and selects the final timeline by name. It must run and be verified after access returns.

Resume: run resolve_lua.py with export-check.lua, then export-speed.lua once the correct native timeline state is read back. Poll the new native render job; run qa_speed.py against the resulting MP4, inspect all six boundary sheets, verify audio/pitch/lip-sync samples and full decode. Then update_board.py --complete and finalize production status. Do not claim completion before actual export/QA.

Updated SRT is in deliverables; all 227 original phrases retained with times divided by 1.1. Beat/word/insert mappings updated. Cut Room displays accurate pending-export status and retained actual images. The V19 toilet shot was not inserted because the source text decision remains pending.
