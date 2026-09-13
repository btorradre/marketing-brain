from pathlib import Path
from PIL import Image
import json
P=Path(__file__).resolve().parent.parent.parent;O=P/'edit/production-v10';A=P/'assets/images-v10';Q=O/'qa'
for f,n in [(4257,'group-post-square-selected.png'),(4685,'research-square-selected.png')]:
 im=Image.open(Q/f'frame-{f}.jpg');im.crop((180,600,900,1320)).save(A/n)
r=json.loads((Q/'revision-qa.json').read_text());r.update({'native_render_job':'600aaa05-fb6e-4c82-a0bd-ff1ce7b28d5e','native_render_status':'Completed output verified by decoding the corrected MP4','replacement_frames':[[4197,4317],[4619,4751]],'overlay_dimensions':[720,720],'overlay_bounds':[180,600,900,1320],'caption_overlap':False,'visually_reviewed':True,'source_post_name':'Deborah Williams','profile':'Original synthetic woman over50','srt_byte_identical_to_v9':(O/'deliverables/Motilli-Unbranded-VSL-v10.srt').read_bytes()==(O.parent/'production-v9/deliverables/Motilli-Unbranded-VSL-v9.srt').read_bytes()});(Q/'revision-qa.json').write_text(json.dumps(r,indent=2))
f=P/'README.md';f.write_text('''# MOT-UGC-YAPPER-01 — centered square overlays v10

Latest ad: [V10 MP4](edit/production-v10/deliverables/Motilli-Unbranded-VSL-v10.mp4). Support-group post now names Deborah Williams with an original synthetic woman over50 as profile picture. Both support-group and apigenin research visuals are1:1square crops,720×720 centered over the presenter. Captions sit below; V3 Creative voice, Avatar V, exact word timing and4:38duration preserved.

[Post in context](edit/production-v10/qa/frame-4257.jpg) · [Research in context](edit/production-v10/qa/frame-4685.jpg) · [Complete post source](assets/images-v10/group-post-deborah.png) · [Generation prompt](edit/production-v10/generation-prompt.txt)

[Resolve project](edit/production-v10/deliverables/MOT-UGC-YAPPER-01-v10-FINAL.drp) · [Timeline](edit/production-v10/deliverables/MOT-UGC-YAPPER-01-v10-FINAL.drt) · [Subtitles](edit/production-v10/deliverables/Motilli-Unbranded-VSL-v10.srt) · [QA](edit/production-v10/qa/revision-qa.json)

[Cut Room](http://localhost:8765/b/mot-ugc-yapper-01) · [Team board](https://cutroom-three.vercel.app/b/mot-ugc-yapper-01) · [Editing plan](edit/editing-plan.md)

## Previous V9 delivery

'''+f.read_text())
(P/'edit/production-status.md').write_text('''# V10 complete

Deborah Williams and an original synthetic woman over50 profile portrait replace Anonymous member. Both support-group and research screenshots are cropped1:1 and centered at720×720over the presenter, boundsx180/y600–x900/y1320. Native Resolve cropping. B26 captions return to normal position below the overlay; timing and words unchanged. GPT Image2 built-in edit; full original post source and prompt retained.

Timeline v10 FINAL - centered square overlays in MOT-UGC-YAPPER-01 v7 V3 20260910. Corrected render600aaa05-fb6e-4c82-a0bd-ff1ce7b28d5e completed; corrected output decoded and verified. Full export audio sample-identical to v9,8327frames/277.566667seconds,1080×1920/30fps. Both windows' consecutive boundaries and interior frames reviewed, text/caption clearance and square dimensions verified. Deliverables in production-v10/deliverables; selected square crops on Cut Room. V9 and earlier exports preserved.
''')
f=P/'edit/editing-plan.md';s=f.read_text();s+='''

## V10 completed verification

Final corrected render600aaa05-fb6e-4c82-a0bd-ff1ce7b28d5e completed; corrected output decoded and verified. Inspected twelve frames covering both windows' consecutive first/last boundaries and interiors, including the corrected post bottom edge. Both720×720squares are centered atx540/y960with clear captions below. Deborah Williams spelling, mature synthetic profile and recreation label visible. Research title and study type visible. Full audio sample-identical to v9, max PCM difference0/correlation1.0.8327frames,277.566667seconds,1080×1920/30fps. SRT bytes identical;229physicalcaptionclips and16linked presenter/audio ranges preserved. Cut Room selected images are extracted from the actual final native render; complete post source retained separately. Native DRP/DRT/MP4/SRT in production-v10/deliverables.
''';f.write_text(s)
