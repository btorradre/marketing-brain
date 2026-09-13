import json
from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parents[5];b=ROOT/'cutroom/boards/motilli-podcast-dvhp-storyboard.json';(P/'qa/board-before-v8.json').write_text(b.read_text());spec=json.load(open(P.parent/'v7/final-board-spec.json'));cards={c['id']:c for c in json.load(open(P/'final-coverage.json'))}
def stamp(t):return f'{int(t)//60}:{t%60:05.2f}'
for lane in spec['timelines']:
 if lane['label'].startswith('REFERENCE'):continue
 lane['label']=lane['label'].replace('V7 · 110% SPEED','V8 · PAUSES REMOVED')
 for beat in lane['beats']:
  id=beat['t'].split(' · ')[0];c=cards[id];beat['t']=id+' · '+stamp(c['start'])+'–'+stamp(c['end']);beat['frame']=str(P/'board-frames'/(id+'.jpg'))
  if id in ['S01-1','S01-2','S01-3']:beat['visual']='Approved podcast coverage with HOW GLP-1s SLOW THE GUT placed at the top, clear of the lower panel and captions.'
  if id=='S06-3':beat['visual']='Small transparent raspberry food cutout appears on the first spoken fiber cue.'
  if id=='S21-1':beat['visual']='Transparent celery and juice appear when apigenin is spoken, with the quiet pause tightened.'
  note='Final v8 rendered frame. Approved 110% speech speed retained. Quiet gaps removed from picture and audio together; caption and overlay timing follows the same cut map.'
  if 'insert_start' in c:note+=f" Insert {stamp(c['insert_start'])}–{stamp(c['insert_end'])}."
  if c['mode']=='Science':note+=' Scientific insert remains text-free.'
  if id.startswith('S01'):note+=' Opening headline is at the top. No duplicate lower banner.'
  beat['note']=note
spec.update(title='Motilli · Podcast ad · Tight cut + top headline',summary='Final v8 at 2:42.73: dead-air pauses removed while retaining the approved 110% speaking speed, voices, avatars, script and visual selection. HOW GLP-1s SLOW THE GUT is now at the top. Picture, dialogue, captions and overlays are cut together in DaVinci Resolve. 75 quiet sections removed, totaling 16.57 seconds. All production frames below come from this final render; reference timings remain unchanged.')
spec['notes']=[{'title':'REQUESTED FIXES','text':'Removed quiet avatar pauses throughout the ad, including speaker changes and the trailing silence. Moved the original HOW GLP-1s SLOW THE GUT layer to the top; the old lower banner is gone.','color':'#dff2e1'},{'title':'PACE AND SYNC','text':'Existing 110% speech pace and pitch correction retained. No additional global speed-up. All picture, caption, overlay and audio cues use one shared cut map. Quiet phonetic handles retained at joins. Final duration 4882 frames / 162.733 seconds at 30fps.','color':'#f7f5ee'},{'title':'DELIVERY','text':'1080×1920 MP4, updated caption SRT and native Resolve DRT/DRP. Original v7 and earlier edits preserved. This board shows the final edited frames and timings.','color':'#dff2e1'}]
(P/'final-board-spec.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2))
