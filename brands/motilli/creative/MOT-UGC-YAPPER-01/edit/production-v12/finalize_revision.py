from pathlib import Path
import json
P=Path(__file__).resolve().parents[2];O=P/'edit/production-v12';Q=O/'qa'
f=Q/'revision-qa.json';r=json.loads(f.read_text());assert r['max_pcm_difference']==0;r.update(native_render_job='9dfba5fd-06f7-4230-9907-3e6eb3ef555b',native_render_status='Completed output verified by decoding',visually_reviewed=True,overlay_bounds=[180,600,900,1320],caption_overlap=False,srt_byte_identical_to_v11=(O/'deliverables/Motilli-Unbranded-VSL-v12.srt').read_bytes()==(O.parent/'production-v11/deliverables/Motilli-Unbranded-VSL-v11.srt').read_bytes());assert r['srt_byte_identical_to_v11'];f.write_text(json.dumps(r,indent=2))
text='''V12 complete. Added a centered720×720square bathroom-scale photo over the presenter on “I believed if I just got the number down the rest would follow,”44.366667–47.300000seconds,frames1331–1419. Straight cuts; captions clear below. GPT Image2 built-in generation; selected asset and exact prompt retained. Neutral0.0ready display without a claimed weight result.

Native Resolve timeline v12 FINAL - scale overlay in MOT-UGC-YAPPER-01 v7 V3 20260910; original v11 preserved. MP4/DRP/DRT/SRT exported.8327frames,277.566667seconds,1080×1920/30fps. Full audio sample-identical to v11, max difference0/correlation1; SRT bytes identical.23covering clips;16presenter/audio ranges and229physicalcaptionclips unchanged. Inspected six final frames at1330/1331/1364/1375/1418/1419for cut boundaries, scale visibility and caption separation. All previous wardrobe and square overlay revisions retained. Cut Room B09 and production source use actual selected scale image; exact narration/reference lane preserved.
'''
(P/'edit/production-status.md').write_text('# V12 complete\n\n'+text)
f=P/'edit/editing-plan.md';f.write_text(f.read_text()+'\n\n## V12 completed verification\n\n'+text)
f=P/'README.md';f.write_text('''# MOT-UGC-YAPPER-01 — scale overlay v12

Latest ad: [V12 MP4](edit/production-v12/deliverables/Motilli-Unbranded-VSL-v12.mp4). Centered square bathroom-scale insert at44.37–47.30seconds. All previous wardrobe/cramping/community/research changes retained; voice, captions and runtime unchanged.

[Scale in context](edit/production-v12/qa/frame-1364.jpg) · [Selected scale image](assets/images-v12/bathroom-scale-square.png) · [Generation prompt](edit/production-v12/generation-prompt.txt) · [QA](edit/production-v12/qa/revision-qa.json)

[Resolve project](edit/production-v12/deliverables/MOT-UGC-YAPPER-01-v12-FINAL.drp) · [Timeline](edit/production-v12/deliverables/MOT-UGC-YAPPER-01-v12-FINAL.drt) · [Subtitles](edit/production-v12/deliverables/Motilli-Unbranded-VSL-v12.srt)

[Cut Room](https://cutroom-three.vercel.app/b/mot-ugc-yapper-01) · [Editing plan](edit/editing-plan.md)

## Previous V11 delivery

'''+f.read_text())
for f in (O/'deliverables').iterdir():assert f.stat().st_size>0;print(f.name,f.stat().st_size)
