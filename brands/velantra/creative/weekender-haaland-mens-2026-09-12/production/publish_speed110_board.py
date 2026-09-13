from pathlib import Path
import json,subprocess,hashlib,sys,copy
from datetime import datetime,timezone
P=Path(__file__).resolve().parent;B=P.parent;root=P.parents[4];slug='velantra-weekender-haaland-reference-style';sys.path.insert(0,str(root/'cutroom'));import supabase_store as cloud
v=P/'exports/Weekender-Haaland-Gringo-Natural-AvatarV-110-NoGaps-Final.mp4';S=json.loads((P/'resolve-speed110/aligned-scenes.json').read_text());spec=json.loads((B/'storyboard/spec.json').read_text());remote=json.loads(cloud.download(f'boards/{slug}.json'));before=copy.deepcopy(remote);(B/'storyboard/board-before-speed110-publish.json').write_text(json.dumps(before,indent=2))
A=root/'cutroom/assets'/slug;F=P/'qa-speed110-final/final-frames';F.mkdir(exist_ok=True);receipt=[]
visual_updates={'S04':'Airport outfit with the Cognac Weekender; restrained step and head turn. Correct paired front straps and rolled handles.','S06':'Distinct white T-shirt and jeans outfit still with corrected Cognac Weekender. Omni generation failed; inspected still selected.','S07':'Moving close-up of Cognac leather, light canvas and gold-tone hardware; hand lightly traces leather.','S11':'Actual owner-shot footage of the Cognac Weekender opening and its wide slip pocket. Original phone clip IMG_4051.MOV, source7.67–13.33s with synchronized pause removal and110% playback; no generated zipper.','S12':'Hotel entrance outfit with the Cognac Weekender; restrained settling step and head turn.'}
for i,s in enumerate(S):
 sid=s['id'];fn=f'{sid}-gringo-natural-avatarv-speed110-final.jpg';f=A/fn
 subprocess.run(['ffmpeg','-v','error','-y','-ss',str(s['start']/30),'-i',str(v),'-frames:v','1','-q:v','2',str(f)],check=True)
 (F/(sid+'.jpg')).write_bytes(f.read_bytes());cloud.upload(f'assets/{slug}/{fn}',f.read_bytes(),'image/jpeg')
 label=next(c for c in remote['cards'] if c.get('type')=='label' and c.get('text','').startswith(sid+' ·'))
 label['text']=f"{sid} · {s['start']/30:.2f}–{s['end']/30:.2f}s · 110% · pauses closed"
 imagecard=next(c for c in remote['cards'] if c.get('type')=='image' and c.get('src','').split('/')[-1].startswith(sid+'-'))
 imagecard['src']=f'/assets/{slug}/{fn}';imagecard['text']=visual_updates.get(sid,s['visual'])
 beat=spec['timelines'][0]['beats'][i];beat['t']=label['text'];beat['frame']=str(f);beat['visual']=imagecard['text'];beat['note']=beat['note'].replace('Timing remains provisional until voice alignment.','Final selected voice alignment; 30fps Resolve timeline.')
 if sid in ['S04','S12']:beat['note']='Direct cut on the spoken cue. Selected restrained Google Omni motion preserves product visibility. '+s['emotion']
 if sid=='S11':beat['note']='Direct cut on Inside; opening action completes as the slip pocket is named. Original phone footage shows actual caramel lining and pocket. Caption above, presenter below the bag opening.'
 if sid=='S06':beat['note']='Direct cut on the casual-outfit payoff. Inspected corrected still retained after two failed Omni requests; no repeated source clip.'
 if sid=='S05':beat['note']='Direct cut to two distinct simultaneous product views: front for silhouette/flap/canvas, detail for rolled handles. Hold through the named features.'
 if sid=='S13':beat['note']='Direct cut on final product name. Bag only, no presenter or text. Exact spoken CTA; picture ends with narration, with no extra hold.'
 beat['note']+=' Selected source, narration, captions and presenter share the measured pause-removal map and110% speed; no extra ending hold.'
 # Note cards share the scene x column. Preserve script and emotional rationale.
 notes=[c for c in remote['cards'] if c.get('type')=='note' and c.get('title')=='EMOTION' and c.get('x')==label['x']]
 if notes:notes[0]['text']=s['emotion']+'\n\n'+beat['note']
 receipt.append({'scene':sid,'frame':s['start'],'src':imagecard['src'],'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
concept='34.50-second Resolve ad, aligned to the selected gringo-tiktok-male voice / Eleven v3 Natural. Original HeyGen presenter, Google Omni motion and distinct corrected wardrobe stills. Exact approved narration preserved. Long pauses removed, with pitch-corrected110% playback. These13 images are actual first frames from the Gringo Natural / Avatar V110% export; the separate reference lane remains source evidence.'
for c in remote['cards']:
 if c.get('title')=='CONCEPT':c['text']=concept
 if c.get('title','').startswith('VOICE'):
  c['title']='VOICE — SELECTED / HEYGEN';c['text']='User explicitly selected gringo-tiktok-male in the ElevenLabs screenshot. Selected gringo-tiktok-male saved voice; Eleven v3 Natural0.5 drives the original HeyGen presenter. Same selected voice and Avatar V performance, synchronized at110% with pitch correction. Extended pauses removed in Resolve.'
 if c.get('title')=='AUDIO / ALIGNMENT':c['text']='Selected narration, presenter, picture and all31 phrase captions share one pause-removal and110% time map. Speech-only mix, no copied reference music. Final clean hero ends with the full narration at34.50seconds; no extra hold.'
 if c.get('type')=='label' and 'PROPOSED AD / SELECTED FIRST FRAMES' in c.get('text',''):c['text']='VELANTRA — RENDERED AD / ACTUAL FIRST FRAMES'
spec['summary']=concept;spec['timelines'][0]['label']='VELANTRA — RENDERED AD / ACTUAL FIRST FRAMES';spec['timelines'][0]['source']='Resolve Gringo Natural / Avatar V · original HeyGen presenter · gringo-tiktok-male voice / Eleven v3 Natural · GPT Image2 / Google Omni · 110% · pauses closed'
for n in spec['notes']:
 for c in remote['cards']:
  if n['title']==c.get('title') or (n['title'].startswith('VOICE') and c.get('title','').startswith('VOICE')):n['title']=c['title'];n['text']=c['text'];break
# Recheck remote has not changed during asset uploads; do not overwrite concurrent edits.
assert json.loads(cloud.download(f'boards/{slug}.json'))==before,'Concurrent board edit; reconcile before save'
raw=json.dumps(remote,indent=2,ensure_ascii=False).encode();cloud.upload(f'boards/{slug}.json',raw,'application/json');(root/'cutroom/boards'/f'{slug}.json').write_bytes(raw);(B/'storyboard/spec.json').write_text(json.dumps(spec,indent=2,ensure_ascii=False)+'\n')
assert json.loads(cloud.download(f'boards/{slug}.json'))==remote
out={'published_at':datetime.now(timezone.utc).isoformat(),'board_url':'https://cutroom-three.vercel.app/b/'+slug,'export':str(v),'timeline':'Weekender-Haaland-Gringo-Natural-AvatarV-110-v2','images':receipt};(B/'storyboard/speed110-final-board-receipt.json').write_text(json.dumps(out,indent=2));print({'board_url':out['board_url'],'frames':len(receipt)})
