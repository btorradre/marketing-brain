from pathlib import Path
import json,sys,subprocess,httpx,re
O=Path(__file__).resolve().parent;P=O.parents[1];ROOT=P.parents[3];f=P/'storyboard/cutroom-spec.json';x=json.loads(f.read_text());before=[b['script'] for t in x['timelines'][:6] for b in t['beats'] if b.get('script')];refs=x['timelines'][7:];I=P/'assets/images-v18';I.mkdir(exist_ok=True)
for name,sec in [('presenter-avatar-selected',5),('presenter-ending-selected',313.9)]:
 subprocess.run(['ffmpeg','-v','error','-y','-ss',str(sec),'-i',str(P/'assets/video-v18/presenter-avatar-v.mp4'),'-frames:v','1','-q:v','2',str(I/(name+'.jpg'))],check=True)
presenter=str(I/'presenter-avatar-selected.jpg');end=str(I/'presenter-ending-selected.jpg')
x['summary']='Completed V18: Michelle, an American female voice listed as age 50, using Eleven v3 Creative. Fresh HeyGen Avatar V performance; 25 quiet gaps removed. All 987 spoken words and 227 caption phrases preserved and retimed. Real TikTok MiraLAX close-up replaces the pharmacy aisle. Native Resolve export: 5:14.367, 1080 × 1920, 30 fps.'
for tl in x['timelines'][:7]:
 for b in tl['beats']:
  if 'P01-presenter-base' in b.get('frame','') or 'selected-presenter-v7' in b.get('frame',''):b['frame']=presenter
  if b['t']=='FINAL FACE · NO SILENT HOLD':b['frame']=end
  if b['t']=='V7 ACTUAL PRESENTER':b.update(t='V18 ACTUAL PRESENTER',visual='Selected frame from the fresh HeyGen Avatar V performance driven by Michelle’s new Eleven v3 Creative narration.',note='New performance and audio verified at the beginning, middle and end. Same approved mature woman, car and outfit.')
  if 'V11 CRAMPING' in b['t']:b['note']='720 × 720 centered. New narration alignment: 17.033–21.033 seconds.'
  if 'V15 SELECTED VISUAL HOOK' in b['t']:b.update(visual='Bathroom doorway view: mature woman in grey tee and plum shorts, seated on toilet and holding her abdomen through a cramp.',note='V18: bathroom 0–3.100 seconds; straight cut to couch. Selected source frames 0–92 at 30 fps.')
  if 'V16 SELECTED SECOND HOOK' in b['t']:b['note']='Same approved presenter, powder-blue top. V18: couch 3.100–4.600 seconds, then car. Selected source frames 0–44 at 30 fps.'
notes={
'CURRENT SCRIPT':'987 exact spoken words, 48 beats and 227 caption phrases. Michelle, age 50 per ElevenLabs profile; Eleven v3 Creative. Final runtime 314.367 seconds after 25 quiet-gap cuts. Natural breaths and phrasing retained.',
'CAPTIONS & SOUND':'Fresh Michelle voice, eleven_v3 model with Creative stability 0 and speed 1.0. Caption wording and styling preserved; all times realigned. Fresh Avatar V lip-sync. No music or added sound effects.',
'EDITOR HANDOFF':'Completed in DaVinci Resolve. Timeline: v18 FINAL - Michelle V3 MiraLAX. 9,431 frames; 1 presenter, 26 covering clips, 227 caption clips and 1 continuous voice master. MP4, DRT, DRP and SRT in edit/production-v18/deliverables.',
'FINAL PRODUCTION STATUS':'V18 is the latest completed ad. Native Resolve export and final audio, caption and visual boundary QA completed. Earlier versions preserved.',
'TWO-SHOT HOOK':'Bathroom 0–3.100 seconds, couch 3.100–4.600 seconds, then car presenter. Approved shots retimed to the new narration.',
'FIRST ASSET SET':'Cards show selected production assets, including the fresh V18 avatar, real TikTok MiraLAX crop, fiber-food source, cooking scene and both generated hook frames. Reference images remain in separate lanes.'}
for n in x['notes']:
 if n['title'] in notes:n['text']=notes[n['title']]
assert before==[b['script'] for t in x['timelines'][:6] for b in t['beats'] if b.get('script')];assert refs==x['timelines'][7:];f.write_text(json.dumps(x,indent=2))
sys.path.insert(0,str(ROOT/'cutroom'));import board_builder,supabase_store as s;slug='mot-ugc-yapper-01';board_builder.build(x,slug)
for n in ['presenter-avatar-selected.jpg','presenter-ending-selected.jpg']:s.push_asset(slug+'/'+n)
s.push_board(slug);local=json.loads((ROOT/'cutroom/boards'/f'{slug}.json').read_text());assert json.loads(s.download('boards/'+slug+'.json'))==local
r=httpx.get('https://cutroom-three.vercel.app/b/'+slug,follow_redirects=True,timeout=30);assert r.status_code==200
report={'url':'https://cutroom-three.vercel.app/b/'+slug,'http_status':r.status_code,'cloud_board_exact_match':True,'script_exact':True,'reference_lanes_unchanged':True,'fresh_presenter_images_uploaded':True};(O/'qa/board-verification.json').write_text(json.dumps(report,indent=2));print(report)
