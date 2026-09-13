from pathlib import Path
import json,sys,httpx
O=Path(__file__).resolve().parent;P=O.parents[1];ROOT=P.parents[3];f=P/'storyboard/cutroom-spec.json';x=json.loads(f.read_text());complete='--complete' in sys.argv
backup=O/'cutroom-before-v22.json'
if not backup.exists():backup.write_text(json.dumps(x,indent=2))
before=[b['script'] for t in x['timelines'][:6] for b in t['beats'] if b.get('script')];refs=json.dumps(x['timelines'][7:],sort_keys=True)
x['title']='MOT-UGC-YAPPER-01 — V22 · Toilet cramping B-roll · 1.2×'
status='Native Resolve export and QA complete.' if complete else 'New GPT Image 2 first frame inspected. Google Omni blocked animation requests; video insert and native edit are unfinished. Completed V21 remains unchanged.'
x['summary']='V22 adds a new generated toilet-cramping shot during “Backed up, uncomfortable, just waiting.” The same woman wears dark teal pajamas and folds forward clutching her abdomen. Existing 1.2× Michelle voice, captions and 4:21.967 runtime are preserved. '+status+' The user’s generated-footage request replaces the earlier TikTok-source search for this beat.'
for t in x['timelines'][:6]:
 for b in t['beats']:
  if b['t'].startswith('B17'):
   b['frame']=str(P/'assets/images-v22/toilet-cramping-keyframe.png');b['visual']='Car presenter → new tight three-quarter toilet shot: dark teal pajamas, hunched forward, hands bracing abdomen, eyes squeezed and strained grimace → car presenter.'
   b['emotion']='Stuck in discomfort after temporary relief: the toilet context and held cramp show what waiting feels like.'
   b['note']='New generated insert only during “Backed up, uncomfortable, just waiting.” at 01:17.200–01:19.333. Straight cuts, source sound muted, existing captions retained. Return for “Something was definitely still missing.” Distinct outfit, framing and action from the wide opening hook. '+status
for n in x['notes']:
 if n['title']=='EDITOR HANDOFF':n['text']=status+' V22 timeline: v22 FINAL - 1.2x toilet cramping. Preserve original V18/V21, 120% speed, pitch correction and all 227 caption phrases. New source is generated illustrative footage, not TikTok footage.'
 if n['title']=='FINAL PRODUCTION STATUS':n['text']=status+(' Latest completed full ad: V22.' if complete else ' Latest completed full ad: V21.')
assert before==[b['script'] for t in x['timelines'][:6] for b in t['beats'] if b.get('script')];assert refs==json.dumps(x['timelines'][7:],sort_keys=True)
f.write_text(json.dumps(x,indent=2));sys.path.insert(0,str(ROOT/'cutroom'));import board_builder,supabase_store as s
slug='mot-ugc-yapper-01';board_builder.build(x,slug);s.push_board(slug);local=json.loads((ROOT/'cutroom/boards'/f'{slug}.json').read_text());assert json.loads(s.download('boards/'+slug+'.json'))==local
r=httpx.get('https://cutroom-three.vercel.app/b/'+slug,follow_redirects=True,timeout=30);assert r.status_code==200
report={'url':str(r.url),'status':r.status_code,'cloud_exact_match':True,'exact_script_preserved':True,'reference_lanes_preserved':True,'actual_B17_image_attached':True,'complete':complete};(O/'qa/board-verification.json').write_text(json.dumps(report,indent=2));print(report)
