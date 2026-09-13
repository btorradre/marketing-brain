import json,sys
from pathlib import Path
R=Path(__file__).resolve().parent;ROOT=R.parents[5];P=R.parents[1]
sys.path.insert(0,str(ROOT/'cutroom'))
from board_builder import build
rows=json.loads((R/'shot-plan.json').read_text());image_requests=json.loads((R/'image-requests.json').read_text())
items=[]
for x in rows:
 parts=['S06a','S06b','S06c','S06d'] if x['id']=='S06' else [x['id']]
 for id in parts:
  y=dict(x);y['id']=id
  if id.startswith('S06') and id!='S06':
   i=parts.index(id);cues=[10.6,11.766667,12.666667,13.6,14.566667]
   y['start'],y['end']=cues[i:i+2];y['script']=['you reach for MiraLAX,','magnesium,','stool softeners,','or more fiber.'][i]
   y['visual']=next(a['prompt'] for a in image_requests if a['id']==id).split(' Vertical')[0]
  new=R/'keyframes'/f'{id}.png'
  if new.exists():
   frame=new;status='NEW VISUAL · motion generated' if (R/'motion'/f'{id}.mp4').exists() else 'NEW KEYFRAME · motion awaits Kie credits'
   if y['decision']=='graphic':status='EDITABLE NUMBER CARD · ingredients revealed in following scene'
  elif y['decision']=='library':frame=R/'audit'/f'library-{id}.jpg';status='DISTINCT EXISTING CLIP · selected'
  elif y['decision']=='keep':frame=Path(y['before_frame']);status='RETAIN SELECTED SHOT'
  else:frame=None;status='NEW VISUAL GENERATING · no old placeholder'
  items.append({'t':f"{id} · {y['start']:.2f}–{y['end']:.2f}",'script':y['script'],'frame':str(frame) if frame else None,'visual':y['visual'],'emotion':y['purpose'],'note':status+'\n'+y['cut']})
lanes=[{'label':'HOOK + PROBLEM','beats':items[:20]},{'label':'SOLUTION + PRODUCT','beats':items[20:32]},{'label':'FUTURE PACING + CTA','beats':items[32:]}]
spec={'title':'MOT-VID-013 Hook A — revised visual storyboard','project':'motilli','summary':'40 distinct shot selections. Celery first appears at 46.23s on “First, apigenin…”. The preceding “three specific things” line uses an ingredient-free 1 / 2 / 3 card. Original audio stays 1.1× and 95.9s. All three original hook projects are revised and exported from CapCut. Watch the completed ads: http://localhost:8765/assets/mot-vid-013-revised-r3/review.html','timelines':lanes,'notes':[{'title':'REVISION STATUS','text':'Completed in CapCut. All three full R3 exports passed rendered and technical QA. Review and download: http://localhost:8765/assets/mot-vid-013-revised-r3/review.html'},{'title':'CELERY REVEAL','text':'43.433–46.233s: ingredient-free 1 / 2 / 3 card. Celery enters at 46.233s on “First, apigenin…”. No early ingredient insert or overlapping transition.'},{'title':'SOURCE GALLERY','text':'http://localhost:8765/assets/mot-vid-013-variety-r3/sources.html'}]}
(R/'board-spec.json').write_text(json.dumps(spec,indent=2));build(spec,'mot-vid-013-variety-r3')
print('Updated Cutroom with actual new frames and four distinct library sources.')
