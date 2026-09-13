import json,re
from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parents[5];old=json.load(open(ROOT/'cutroom/boards/motilli-podcast-dvhp-storyboard.json'));(P/'qa/board-before-speed.json').write_text(json.dumps(old,indent=2));spec=json.load(open(P.parent/'v6/final-board-spec.json'));cards=json.load(open(P/'final-coverage.json'));lookup={c['id']:c for c in cards}
def stamp(t):return f'{int(t)//60}:{t%60:05.2f}'
for lane in spec['timelines']:
 if lane['label'].startswith('REFERENCE'):continue
 lane['label']=lane['label'].replace('V6 FINAL','V7 · 110% SPEED')
 for beat in lane['beats']:
  id=beat['t'].split(' · ')[0];c=lookup[id];beat['t']=id+' · '+stamp(c['start'])+'–'+stamp(c['end']);beat['frame']=str(P/'board-frames'/(id+'.jpg'))
  beat['visual']=re.sub(r'\b(31\.733|33\.533|98\.167)\b',lambda m:f'{float(m.group())/1.1:.3f}',beat['visual'])
  note='Final 110% render. Entire approved v6 ad plays 1.1× faster; both voices pitch-corrected. Every shot, caption, overlay and end hold shares the same timing scale.'
  if 'insert_start' in c:note+=f" Insert {stamp(c['insert_start'])}–{stamp(c['insert_end'])}."
  if id=='S06-3':note+=' Transparent raspberries on fiber, 28.848–30.485.'
  if id=='S21-1':note+=' Transparent celery enters on apigenin at 89.242, clears 91.424; no pop-up on First.'
  if c['mode']=='Science':note+=' Text-free scientific motion.'
  beat['note']=note
spec.update(title='Motilli · Podcast ad · 110% speed',summary='Approved v6 ad uniformly accelerated by an additional 1.1× in DaVinci Resolve, with pitch correction. Runtime 2:59.3, 1080×1920 at 30 fps. Exact narration and all approved images, avatars, ingredient cutouts and visual fixes retained. Every picture, caption, overlay and audio cue stays synchronized. These frames are extracted from the final faster export; reference lane retains its original timecodes.')
spec['notes']=[{'title':'SPEED REVISION','text':'Entire finished ad at 110% playback. Original v6 length 197.233s → 179.300s at 30fps. Both audio and video read back at 110%, pitch correction enabled. No regenerated voices or avatars.','color':'#dff2e1'},{'title':'TIMING','text':'Every production cue is divided by 1.1. Fiber food 28.848–30.485; stool/muscle science 44.667–48.303; celery/apigenin 89.242–91.424. Captions and end hold follow the same scale. Reference timings remain unchanged.','color':'#f7f5ee'},{'title':'DELIVERY','text':'Final MP4 plus updated SRT and editable DaVinci Resolve DRT/DRP. Earlier v6 and v5 versions are preserved. No changes to the approved visuals or script.','color':'#dff2e1'}]
(P/'final-board-spec.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2))
