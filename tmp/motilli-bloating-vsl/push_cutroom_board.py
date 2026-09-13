from pathlib import Path
import json,sys
root=Path('brands/motilli/creative/MOT-UGC-YAPPER-01').resolve()
d=json.loads((root/'storyboard/beat-cards.json').read_text())
shots=json.loads((root/'edit/reference-analysis/verified-shot-map.json').read_text())
frames=list((root/'edit/reference-analysis/boundary-frames').glob('frame-*.jpg'))
def tc(s):
 m=int(s//60);return f'{m:02}:{s-m*60:04.1f}'
refs=[]
for target in [0,4.1,17,39.5,50,60,84,96.5,173.8]:
 shot=next(s for s in shots if s['start_seconds']<=target<s['end_seconds'])
 choices=[p for p in frames if shot['start_frame']<=int(p.stem.split('-')[1])<shot['end_frame_exclusive']]
 chosen=min(choices,key=lambda p:abs(int(p.stem.split('-')[1])-(shot['start_frame']+shot['end_frame_exclusive'])/2)) if choices else None
 beat={'t':f"{shot['shot']} · {tc(shot['start_seconds'])}–{tc(shot['end_seconds'])}",'script':shot['narration'],'visual':shot['visual'],'emotion':'Observed reference coverage: use the shot to understand the presenter/insert rhythm, not as Motilli proof.','note':f"{shot['incoming']}. {shot['outgoing']}. Reference transcript is local ASR, approximate; source claims are not Motilli evidence."}
 if chosen:beat['frame']=str(chosen)
 refs.append(beat)
ours=[]
for r in d['cards']:
 ours.append({'t':f"{r['id']} · {tc(r['start'])}–{tc(r['end'])} · {r['duration']:.1f}s",'script':r['copy'],'visual':r['visual'],'emotion':f"{r['group']} — {r['performance']}",'note':f"CUT CUE: {r['transition']}\nASSET / SOURCE GAP: {r['gap']}\nTiming provisional; this thought may span presenter coverage and short inserts."})
notes=[
 {'title':'TIMING & SCRIPT','text':'Exact supplied H1 + body: 892 words. 205 wpm planning pace with brief pauses; 4:34 including a 3-second end hold. 27 thought beats are not 27 cuts or generation clips. Preserve the script; align final cuts and captions to recorded words.'},
 {'title':'PRESENTER','text':'One woman over 50, parked-car phone selfie, eye-level camera, available window light. Keep her identity, clothing and camera axis consistent. Engaged conversation; reactions and emotional payoffs stay on her face. Character assets not generated yet.'},
 {'title':'CAPTIONS & CUTS','text':'Black sentence-case sans serif on snug white boxes, chest height, 1–2 lines. Straight cuts on spoken actions/nouns; mostly 1–3-second inserts. Exact source font is unverified. Target cut positions await voice alignment.'},
 {'title':'VISUAL VARIETY','text':'Give each B-roll insert a distinct composition and action. Do not reuse the same waistband, food or science shot. Competitor images appear only in the reference lane; proposed Motilli scenes remain text until actual selected assets exist.'},
 {'title':'EDITOR & SOUND','text':'Edit in DaVinci Resolve. V1 presenter; V2 inserts; V3 product; subtitle track; A1 voice, A2 room tone, A3 optional music/SFX. Live MCP connection remains pending. Reference music/SFX matching awaits critical listening.'},
 {'title':'END HOLD & QA','text':'04:31–04:34: hold the final product/CTA composition for 3 seconds with no added speech. Proposed delivery: 1080×1920, 30fps, H.264/AAC, clean and captioned versions. Check exact script, voice alignment, captions, product identity, visual variety, sound and full exported playback.'},
 {'title':'COPY DEPENDENCIES','text':'Preserve source copy in planning. Before production, substantiate the physician/group accounts, ingredient mechanism and clinical claims, first-person results, exclusivity, availability and guarantee. Do not manufacture clinician posts or before/after proof.'},
 {'title':'REFERENCE SCOPE','text':'Alicia Darling, TrendTrack ad 1833962050620738: about 2:56, 71 retained source shots/pickups, median 2 seconds, presenter base about 54%. Nine selected source frames shown here. The separate original Facebook ad remains unavailable. Full frame audit saved with the editing plan.'}
]
for h in d['hook_alternatives'][1:]:notes.append({'title':h['beat']+' · ALTERNATE OPENING','text':h['copy']})
notes.append({'title':'SOURCE REFERENCE','text':'https://app.trendtrack.io/share/ads/alicia-darling-LFj90I'})
spec={'title':'Motilli — AI UGC Yapper 01','project':'motilli','summary':'GLP-1 gut slowdown · first-person woman · exact approved Motilli script. Three consecutive target lanes cover all 27 thought beats; selected Alicia Darling source frames follow in a separate reference lane. Proposed runtime 4:34. Cut Room is the editable storyboard; DaVinci Resolve is the production editor. Target images and voice have not been generated.','timelines':[{'label':f'OUR VERSION · PART {i+1} OF 3','source':'Exact Motilli narration · provisional timing','beats':ours[i*9:(i+1)*9]} for i in range(3)]+[{'label':'REFERENCE CREATIVE · SELECTED OBSERVED SHOTS','source':'Alicia Darling · source frames, not proposed Motilli assets','beats':refs}], 'notes':notes}
path=root/'storyboard/cutroom-spec.json';path.write_text(json.dumps(spec,indent=2,ensure_ascii=False))
sys.path.insert(0,str(Path('_engine/mcp/dr-os').resolve()))
from boards import push_board
result=push_board(spec,slug='mot-ugc-yapper-01',project='motilli')
(root/'storyboard/cutroom-delivery.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result))
