from pathlib import Path
import json,subprocess,sys,hashlib
P=Path(__file__).resolve().parent;C=P.parent;R=P/'tight';Q=R/'qa';root=next(p for p in P.parents if (p/'cutroom/board_builder.py').exists())
sys.path.insert(0,str(root/'cutroom'));import supabase_store as store
slug='eleanor-european-travel-storyboard'
before=store.download('boards/'+slug+'.json')
assert json.loads(before)==json.loads((R/'cutroom-before.json').read_text()),'Live board changed since intake; reconcile before replacing'
specpath=C/'storyboard/cutroom-spec.json';spec=json.loads(specpath.read_text());(R/'cutroom-spec-before.json').write_text(json.dumps(spec,indent=2))
scenes=json.loads((R/'aligned-scenes.json').read_text())
for s in scenes:
 s['duration']=s['duration_frames']/30
 for key in ['speech_start','speech_end']:
  if key in s:s['original_voice_'+key]=s.pop(key)
 s['notes']=s['notes'].replace('Timing provisional until final voice alignment.','Cuts aligned to the selected narration after quiet-gap removal.')
 if s['id']=='S10':s['why']=s['why'].replace('Hold two seconds after speech','Show CTA during the shop invitation and hold about 0.2 seconds after speech')
(R/'aligned-scenes.json').write_text(json.dumps(scenes,indent=2)+'\n')
spec['summary']='Completed tight edit: 70.67 seconds, 27 quiet gaps removed, original ElevenLabs Woman Over 40 / Natural / 1.1× delivery preserved. HeyGen presenter enlarged 18% and placed flush against the lower-left corner. Native DaVinci Resolve edit with all 76 caption phrases realigned. Scene cards show actual revised export frames. Review edit; source-photo commercial reuse remains unverified.'
for b,s in zip(spec['timelines'][0]['beats'],scenes):
 assert b['script']==s['line']
 b['t']=f"{s['id']} · {s['start']:.2f}–{s['end']:.2f}s · tight voice alignment"
 b['frame']=str(Q/('cta-spoken.jpg' if s['id']=='S10' else f"scene-{s['id']}.jpg"))
 b['emotion']=b['emotion'].replace('Hold two seconds after speech','Show the CTA during the shop invitation, with about 0.2 seconds after speech')
 b['note']=b['note'].replace('Actual completed Resolve frame with moving HeyGen P01 and aligned phrase caption. The adviser remains continuous across the background cut.','Actual revised Resolve frame. Presenter is 18% larger, flush lower-left. Voice, presenter and captions share the same quiet-gap cuts; background continuity retained.')
 if s['id']=='S10':b['note']+=' Closing graphic starts at 68.30 seconds; final captions sit above it.'
notes={
 'APPROVED WORDS':'Exact approved words preserved in all 76 caption phrases. Existing ElevenLabs Woman Over 40 / Eleven v3 Natural / synthesis speed 1.1 retained. Original voice source is 79.28 seconds. Edited timeline is 70.67 seconds after 27 quiet-gap cuts and a shorter ending; no second speed increase.',
 'CAPTIONS + SOUND':'White sentence-case phrases with dark outline; original styling retained. All captions and presenter segments follow the same silence-cut map as the voice. Final shop captions are above the CTA graphic. No internal quiet gaps longer than 0.2 seconds at the tested -40 dBFS threshold; brief natural breath spaces remain.',
 'PRODUCT + HANDOFF':'Cognac Eleanor reviewed against selected reference lineage; physical scale unverified. Three Google Omni motion sources plus the HeyGen Avatar V presenter are composited in the isolated DaVinci Resolve Tight timeline. Revised MP4 and editable DRP saved; previous versions preserved.',
 'PRODUCTION STATUS':'TIGHT REVISION COMPLETE / 70.67 seconds, 27 internal quiet-gap cuts; 10.63 seconds shorter overall. Presenter enlarged from 0.28 to 0.33 zoom and flush lower-left. Full decode passed; all 28 audio sections have zero sample lag and correlation above 0.99999 against retained source intervals. Actual exported frames and all nine scene-cut boundaries inspected. Technical review is not human approval. Paris retains its selected still and planned crop.'}
for n in spec['notes']:
 if n['title'] in notes:n['text']=notes[n['title']]
spec['timelines'][-1]['beats'][0]['note']+=' Tight revision: same source cut with narration, enlarged 18% and placed flush lower-left; no regeneration.'
specpath.write_text(json.dumps(spec,indent=2)+'\n');(R/'cutroom-spec-final.json').write_text(json.dumps(spec,indent=2)+'\n')
r=subprocess.run(['python3',str(root/'cutroom/board_builder.py'),str(specpath)],capture_output=True,text=True);(R/'cutroom-build.log').write_text(r.stdout+r.stderr);assert r.returncode==0,r.stderr
cloud=json.loads(store.download('boards/'+slug+'.json'));local=json.loads((root/'cutroom/boards'/f'{slug}.json').read_text());assert cloud==local
images=[]
for card in cloud['cards']:
 if card.get('type')=='image':
  rel=card['src'].lstrip('/');remote=store.download(rel);file=root/'cutroom'/rel
  assert remote==file.read_bytes(),rel
  images.append({'path':rel,'bytes':len(remote),'sha256':hashlib.sha256(remote).hexdigest()})
assert ' '.join(' '.join(b['script'].split()) for b in spec['timelines'][0]['beats'])==' '.join((C/'script-v1.txt').read_text().split())
receipt={'url':'https://cutroom-three.vercel.app/b/'+slug,'cloud_matches_local':True,'cards':len(cloud['cards']),'verified_images':images,'approved_script_exact':True}
(Q/'cutroom-verification.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({'url':receipt['url'],'cards':receipt['cards'],'verified_images':len(images),'script_exact':True}),flush=True)
