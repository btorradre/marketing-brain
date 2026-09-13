from pathlib import Path
import json,subprocess,sys,hashlib
P=Path(__file__).resolve().parent;C=P.parent;H=P/'heygen';Q=H/'qa';root=next(p for p in P.parents if (p/'cutroom/board_builder.py').exists())
sys.path.insert(0,str(root/'cutroom'));import supabase_store as store
slug='eleanor-european-travel-storyboard';before=store.download('boards/'+slug+'.json')
assert json.loads(before)==json.loads((H/'cutroom-before.json').read_text()),'Live board changed since intake; reconcile before replacing'
specpath=C/'storyboard/cutroom-spec.json';spec=json.loads(specpath.read_text());(H/'cutroom-spec-before.json').write_text(json.dumps(spec,indent=2))
spec['summary']='Completed HeyGen presenter edit: exact approved ElevenLabs Woman Over 40 / Natural / 1.1× narration. 81.30-second DaVinci Resolve composition with continuous keyed HeyGen Avatar V adviser, distinct women, four-bag photo grid, three Google Omni motion inserts and 76 aligned caption phrases. Every scene image below is an actual exported Resolve frame. Review edit; source-photo commercial reuse remains unverified.'
times=[1,12,16,24,36,42,52,64,70,77]
for b,t in zip(spec['timelines'][0]['beats'],times):
 b['frame']=str(Q/f'final-{t}s.jpg')
 b['note']=b.get('note','').replace('shown image is its actual first frame.','native provider output is retained.').replace('provisional cut cues','aligned cut cues')
 if b['t'].startswith('S07'):
  b['note']=b['note'].replace('Optional single detail-led 110% stepped crop on handles/textures; keep P01 fixed and preserve bag/footwear readability. This is reframing, not a new scene.','London holds its first frame for 2.4 seconds, then plays the native Omni motion without retiming.')
 b['note']+=' Actual completed Resolve frame with moving HeyGen P01 and aligned phrase caption. The adviser remains continuous across the background cut.'
f=H/'presenter-first-frame.jpg';subprocess.run(['ffmpeg','-y','-v','error','-i',str(H/'presenter-native.mp4'),'-frames:v','1',str(f)],check=True)
presenter=spec['timelines'][-1]['beats'][0];presenter['frame']=str(f);presenter['visual']='Actual first frame of the completed HeyGen Avatar V presenter source.';presenter['note']='79.28 seconds driven by the exact selected ElevenLabs MP3; native green source is keyed lower-left in Resolve. Original provider output retained. No second speed change.'
for n in spec['notes']:
 if n['title']=='PRODUCT + HANDOFF':n['text']='Cognac Eleanor reviewed against selected reference lineage; physical scale unverified. Three Google Omni motion clips plus continuous HeyGen Avatar V presenter are composited in the isolated DaVinci Resolve timeline. Completed MP4 and editable DRP saved; original WIP retained.'
 if n['title']=='PRODUCTION STATUS':n['text']='HEYGEN COMPLETE / Presenter generated from the exact selected image and full Woman Over 40 / Natural / 1.1× audio. User explicitly directed HeyGen. Actual presenter and Resolve export checked for audio timing, coarse lip sync, cutout edges, captions and layout. Paris retains its selected photo and planned crop after the optional Omni job failed.'
specpath.write_text(json.dumps(spec,indent=2)+'\n');(H/'cutroom-spec-final.json').write_text(json.dumps(spec,indent=2)+'\n')
r=subprocess.run(['python3',str(root/'cutroom/board_builder.py'),str(specpath)],capture_output=True,text=True);(H/'cutroom-build.log').write_text(r.stdout+r.stderr);assert r.returncode==0,r.stderr
cloud=json.loads(store.download('boards/'+slug+'.json'));local=json.loads((root/'cutroom/boards'/f'{slug}.json').read_text());assert cloud==local
images=[]
for card in cloud['cards']:
 if card.get('type')=='image':
  rel=card['src'].lstrip('/');remote=store.download(rel);file=root/'cutroom'/rel
  assert remote==file.read_bytes(),rel
  images.append({'path':rel,'bytes':len(remote),'sha256':hashlib.sha256(remote).hexdigest()})
words=' '.join(' '.join(b['script'].split()) for b in spec['timelines'][0]['beats']);assert words==' '.join((C/'script-v1.txt').read_text().split())
receipt={'url':'https://cutroom-three.vercel.app/b/'+slug,'cloud_matches_local':True,'cards':len(cloud['cards']),'verified_images':images,'approved_script_exact':True}
(Q/'cutroom-final-verification.json').write_text(json.dumps(receipt,indent=2));print(json.dumps({'url':receipt['url'],'cards':receipt['cards'],'verified_images':len(images),'script_exact':True}),flush=True)
