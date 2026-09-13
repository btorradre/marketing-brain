import json,shutil
from pathlib import Path
P=Path(__file__).resolve().parent;V5=P.parent/'v5';ROOT=P.parents[5];C=P.parents[1];board=ROOT/'cutroom/boards/motilli-podcast-dvhp-storyboard.json';old=json.loads(board.read_text());(P/'qa/board-before-v6.json').write_text(json.dumps(old,indent=2));spec=json.loads((V5/'final-board-spec.json').read_text());cards=json.loads((P/'final-coverage.json').read_text());frames=P/'board-frames';frames.mkdir(exist_ok=True)
def stamp(t):return f'{int(t)//60}:{t%60:05.2f}'
lanes=[]
for section in sorted({c['section'] for c in cards}):
 beats=[];group=[c for c in cards if c['section']==section]
 for c in group:
  src=P/'qa'/(c['id']+'-render.jpg');dst=frames/('v6-'+c['id']+'.jpg');shutil.copy2(src,dst)
  note='Final v6 rendered frame. Direct cut; original approved dialogue and avatars preserved.'
  if 'insert_start' in c:note+=f" Insert {stamp(c['insert_start'])}–{stamp(c['insert_end'])}."
  if c['mode']=='Science':note+=' No text or captions.'
  if c['id']=='S06-2':note+=' Old orange stomach shot removed; guest camera and phrase captions restored.'
  if c['id']=='S06-3':note+=' Raspberry cutout appears exactly on fiber, 31.733–33.533, with true transparency.'
  if c['id']=='S21-1':note+=' Celery enters on apigenin at 98.167; no pop-up on First. True transparent background; clears at 100.567.'
  if c['id']=='S22-1':note+=' Celery cutout from the preceding apigenin cue remains briefly through 100.567.'
  if c['id'] in ['S23-1','S25-1']:note+=' True transparent ingredient cutout; no navy/white rectangle.'
  if c['id'].startswith('S41'):note+=' 90-day guarantee promotional overlay removed. Only link CTA remains; spoken narration and phrase captions stay exact.'
  if c['id'] in ['S26-1','S26-2']:note+=' Continuous two-view fiber/microbe explanation requested by user.'
  beats.append(dict(t=c['id']+' · '+stamp(c['start'])+'–'+stamp(c['end']),script=c['script_excerpt'],frame=str(dst),visual=c['visual'],emotion=c.get('emotion','Keep explanation tied to the spoken idea.'),note=note))
 lanes.append({'label':f'{section:02d} · {group[0]["chapter"]} · V6 FINAL','beats':beats})
lanes += [t for t in spec['timelines'] if t['label'].startswith('REFERENCE')]
spec.update(title='Motilli · Podcast ad · V6 visual revision',summary='Final visual-only revision of the approved 3:17 podcast ad in DaVinci Resolve. Original HeyGen Avatar V performances and selected ElevenLabs voices unchanged. Removed mismatched appetite stomach shot; added a quick transparent raspberry food cue; new stool-hydration, gastric-muscle and gastric-retention scientific motion; celery enters precisely on apigenin; every ingredient pop-up has real transparency; guarantee promotional graphic removed. Frames below come from the final v6 render. Exact v7 narration and word timing preserved.',timelines=lanes)
spec['notes']=[{'title':'V6 CHANGES','text':'31.733s fiber food pop-up; 49.133s stool hydration → 50.233s gastric muscle action; 57.833s retained stomach contents; 98.167s apigenin-triggered celery. Transparent food/ingredient cutouts. Orange appetite insert removed. Link-only CTA.','color':'#dff2e1'},{'title':'LOCKED PERFORMANCES','text':'Both approved HeyGen avatars, voices, speaking order and speed are unchanged. The original v5 remains preserved. Full ad length remains 5917 frames at 30 fps.','color':'#f7f5ee'},{'title':'DELIVERY AND QA','text':'1080 × 1920 · H.264/AAC · native DaVinci Resolve timeline and project. 102 word-aligned phrase captions; scientific inserts text-free. Decoded audio bit-identical to the approved v5. Every affected cut inspected on consecutive frames.','color':'#dff2e1'},{'title':'VISUAL RULES','text':'Food and ingredient pop-ups have actual alpha transparency. Candid phone-style footage keeps its photographed setting. Ordinary insert windows stay within four seconds; S26 retains its explicitly requested continuous two-view exception. Reference frames are in their separate lane.','color':'#f7f5ee'}]
(P/'final-board-spec.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2));print('Prepared v6 board',len(cards),'production frames')
