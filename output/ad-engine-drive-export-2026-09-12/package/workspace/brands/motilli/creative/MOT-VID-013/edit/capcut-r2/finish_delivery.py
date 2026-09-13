from pathlib import Path
import json,requests
p=Path(__file__).resolve().parent;qa=json.loads((p/'final-qa.json').read_text());url='http://localhost:8765/assets/mot-vid-013-edited-ad/review.html';r=requests.get(url,timeout=10);r.encoding='utf-8';assert r.status_code==200 and '1.1× narration' in r.text
for v in 'ABC':
 name=f'MOT-VID-013-R2-{v}.mp4';assert name in r.text;head=requests.get(url.rsplit('/',1)[0]+'/'+name,timeout=10,stream=True);assert head.status_code==200 and int(head.headers['Content-Length'])==qa['variants'][v]['bytes'];head.close()
manifest={'status':'delivered','revision':'R2 — 1.1x narration, pauses removed, actual-export cue correction','date':'2026-09-09','review_url':url,'projects':json.loads((p/'projects.json').read_text()),'qa':qa,'preserved_previous_delivery':'../capcut/exports','notes':['Existing original ElevenLabs take 4 is the source; no new voice generation.','31 verified source silence intervals removed; native voice speed exactly 1.1 on 32 segments.','Picture and captions compensate for measured native render latency by two frames.','The qualitative audio review passed. Its model-supplied last-word timestamp of 135.3 is invalid and excluded. Actual timing evidence uses Scribe, native ranges and export waveform comparison.','A/B/C audio correlations exceed 0.99985 against the reviewed trial after level correction; all four windowed lag checks per file are zero samples.','Inspected all 40 picture segments, four ending samples, final A/B/C hooks and final caption/CTA spot frames.','Full black-frame scan clear. All three files fully decoded without errors.']};(p/'manifest.json').write_text(json.dumps(manifest,indent=2))
(p/'README.md').write_text('''# MOT-VID-013 — revised ad, September 9, 2026

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
''')
with (p.parent/'project.md').open('a') as f:f.write('''
## September 9, 2026 — 1.1× voice and synchronization revision delivered

User requested slower narration, dead-space removal and B-roll sync. Wrote the revision editing plan first. Returned to original ElevenLabs take 4, independently aligned/transcribed actual speech, removed 31 quiet intervals (10.34 source seconds), and rebuilt all 40 picture segments, 95 captions and labels in separate native R2 A/B/C projects. Every voice segment is exactly 1.1×. Actual-export analysis revealed a consistent two-frame renderer delay; corrected picture/text cues and verified final audio retains measured timing. All 291 script words are present; maximum caption/B-roll cue error is 59 ms, excluding immediate opening picture. Clean audio headroom, full decode and visual QA passed. Three 1080×1920/30fps H.264/AAC exports, 95.9 seconds picture. Review page serves R2 files; old exports/projects preserved. See `capcut-r2/README.md`, `manifest.json`, `final-qa.json` and `exports/`.
''')
plan=p/'editing-plan.md';plan.write_text(plan.read_text().replace('actual final voice-only export','actual final mixed export'))
print('All delivery links verified; manifest and project history updated.')
