"""Build the revised selected-image storyboard without modifying narration."""
import json, re, hashlib, copy, html, subprocess, sys
from pathlib import Path
V=Path(__file__).resolve().parent
D=V.parent
ROOT=next(p for p in V.parents if (p/'cutroom/board_builder.py').exists())
A=V/'assets'
OLD=D/'v3-archive'
def read(p):return json.loads(p.read_text())
def save(p,d):p.write_text(json.dumps(d,indent=2))
def norm(s):return ' '.join(s.split())
old=read(OLD/'podcast-coverage.json')
coverage=copy.deepcopy(old)
story=read(OLD/'storyboard.json')
script=D.parents[1]/'script-v7-podcast.txt'
assert hashlib.sha256(script.read_bytes()).hexdigest()==story['meta']['script_sha256']
changes={
 'S03-1':('stomach-open','Science','Open stomach wall reveals rugae, retained contents and pyloric outlet.','The stomach wall opens aside over the first 0.5s, then a restrained push into the exposed cavity; slow liquid movement.','See where the slowdown occurs.'),
 'S04-2':('contractions','Science','Diagonal intestinal muscle sleeve; visible lumen and one shallow muscular squeeze.','One weak contraction moves along the intestinal sleeve; contents advance slightly. Different organ and camera axis from S03-1.','Understand propulsion through visible muscular action.'),
 'S06-2':('appetite','Science','Interior stomach chamber, looking across folded upper wall from just above a modest retained meal.','Small internal ripple with food lingering; camera remains inside the stomach. No exterior organ silhouette, plate overlay or text.','Explain reduced appetite through a tangible internal view.'),
 'S08-1':('constipation','Science','Descending and sigmoid colon cutaway with dry stool backed up along the lumen.','Slow camera track along the colon; contents barely advance. No complete obstruction or gross-out treatment.','Recognize the constipation nightmare state.'),
 'S11-2':('colon-water','Science','Close internal colon view: fluid wets and softens stool beside the tissue wall.','Fluid remains in the lumen and slowly permeates the stool surface. No words, arrows, captions or label strip.','Understand water retention in the colon.'),
 'S13-2':('fullness','Phone B-roll','Woman leans back from her unfinished lunch and presses her upper abdomen.','Handheld phone drift; a small tense exhale and hand on upper abdomen convey uncomfortable fullness.','Feel the discomfort after eating.'),
 'S16-1':('bulk-fiber','Science','Psyllium fibers absorb surrounding fluid inside the intestinal lumen.','Hydrated gel slowly swells around actual fiber particles. Keep tissue walls visible throughout.','See absorption and expansion in the body.'),
 'S19-2':('burp','Phone B-roll','Woman in a parked car briefly covers her mouth after a burp.','Small natural mouth-cover gesture and embarrassed glance aside; no smell cloud.','Recognize the everyday symptom without an abstract odor icon.'),
 'S21-1':('celery-overlay','Ingredient overlay','Photographic celery stalks and green juice over the speaking guest.','Ingredient image appears on the first celery/apigenin cue, small gentle scale-in, clears by 94.11s. Keep guest face visible.','Identify the plant ingredient visually.'),
 'S22-2':('pylorus','Science','Close cutaway of antrum, pyloric channel and beginning of duodenum.','A restrained antral squeeze passes a small chyme ribbon through the outlet; not a wide stomach repeat.','Show the movement being discussed with a distinct anatomical action.'),
 'S23-1':('chlorophyll-overlay','Ingredient overlay','Photographic green leaf and deep-green extract overlay on guest.','Brief plant-pigment image appears and clears on the handoff to the stomach scene. No molecular icon or headline.','Make the named ingredient concrete.'),
 'S23-2':('fermentation','Science','Inside the stomach, small gas bubbles arise at retained food surfaces.','Low internal macro camera; bubbles form locally and rise. No nose, external smell plume or magical neutralization.','Visualize the requested in-body fermentation concept.'),
 'S25-1':('soluble-fiber-overlay','Ingredient overlay','Measured fine soluble supplement powder, spoon and water over the guest.','Brief photographic FOS ingredient overlay; no grain pile, tangled fibers or thick-gel comparison chart.','Show the actual supplement form being discussed.'),
 'S26-1':('prebiotic-arrival','Science','Dispersed soluble substrate arrives at a colon microbial community.','Wide microscopic surface track, particles drifting toward microbes. Continue into S26-2, no presenter return.','Begin the prebiotic mechanism explanation.'),
 'S26-2':('prebiotic-uptake','Science','Distinct close microcolony cross-section, soluble substrate at bacterial surfaces.','Straight cut to the tighter microcolony action. Two different scientific views in one continuous 5.37s sequence, explicitly requested.','Explain microbes using the substrate.'),
}
def set_asset(c,key,kind,visual,motion,emotion):
 c.update(frame=str(A/(key+'.png')),asset_key=key,mode=kind,visual=visual,motion=motion,emotion=emotion,
          insert_id=('V4-'+c['id']),overlay_windows=[],text_policy='No text or captions on this visual.' if kind in ['Science','Phone B-roll'] else 'No added editorial text; ingredient image only.',
          proxy='Generated storyboard first frame; motion direction only, no finished animation.' if kind!='Ingredient overlay' else 'Generated ingredient overlay mockup; presenter likeness is an AI concept, not an endorsement.')
 c['edit']=f"Straight cut in at ~{c['start']:.2f}s on the spoken cue; cut out at ~{c['end']:.2f}s. Continuous podcast dialogue. "+motion

def split(c,times,counts):
 words=c['script_excerpt'].split(); out=[];pos=0
 for i,(start,end,count) in enumerate(zip(times[:-1],times[1:],counts),1):
  n=copy.deepcopy(c); n.update(id=c['beat_id']+'-'+str(i),start=start,end=end,duration=round(end-start,2),script_excerpt=' '.join(words[pos:pos+count]));pos+=count;out.append(n)
 assert pos==len(words)
 return out

result=[]
for c in coverage:
 if c['id']=='S09-1':
  parts=split(c,[38.85,41.06,43.76,44.53],[7,9,len(c['script_excerpt'].split())-16])
  set_asset(parts[1],'fiber-supplement','Phone B-roll','Hand reaches for an actual Metamucil psyllium supplement tub beside water.','Candid phone close-up; preserve sourced packaging identity. No invented pack, fiber bowl or outcome comparison.','Recognize the familiar supplement remedy.')
  result.extend(parts);continue
 if c['id']=='S36-1':
  parts=split(c,[153.16,156.66,158.21],[11,len(c['script_excerpt'].split())-11])
  set_asset(parts[0],'getting-dressed','Phone B-roll','Woman comfortably fastens trousers while getting dressed in an ordinary bedroom.','Small natural fastening movement, relaxed shoulders, subtle relief; casually filmed on phone.','Picture a comfortable morning and the freedom to leave home.')
  result.extend(parts);continue
 if c['id']=='S37-1':
  parts=split(c,[158.21,159.45,162.95],[4,len(c['script_excerpt'].split())-4])
  set_asset(parts[1],'lunch','Phone B-roll','Two women enjoy lunch at a neighborhood cafe and pay attention to each other.','Candid phone view from a friend’s seat; listening smile and one natural conversational gesture.','Enjoy connection and give the conversation full attention.')
  result.extend(parts);continue
 if c['id']=='S38-1':
  parts=split(c,[162.95,164.45,167.95,168.95],[5,11,len(c['script_excerpt'].split())-16])
  set_asset(parts[1],'afternoon','Phone B-roll','Woman takes her keys and jacket at the doorway, ready for afternoon plans.','Casual phone framing; pick up keys and step toward the open door.','Feel free to follow through on ordinary plans.')
  result.extend(parts);continue
 if c['id'] in changes:set_asset(c,*changes[c['id']])
 if c['id'] in ['S01-1','S06-1','S06-3','S07-1']:
  c.update(frame=str(A/'podcast-split.png'),asset_key='podcast-split',mode='Podcast · female host TOP / guest BOTTOM',visual='Same female host in the TOP panel; same existing speaking guest in the BOTTOM panel. No male listening cohost.',emotion='Keep creator identity and conversation continuous.',proxy='Generated presenter composition; AI concept, not a real recording or endorsement.')
  if c['id']!='S01-1':c['overlay_windows']=[]
 result.append(c)
coverage=result
for c in coverage:
 if 'motion' not in c and 'Podcast' in c['mode']:
  c['edit']=f"Podcast camera at ~{c['start']:.2f}–{c['end']:.2f}s; natural listening/speaking gesture. Keep dialogue continuous and clear preceding insert."
 c.setdefault('emotion','Keep the exchange natural and let the spoken idea land.' if 'Podcast' in c['mode'] else 'Show the small practical product serving clearly.')
 c['duration']=round(c['end']-c['start'],2)
 # Remove stale explanatory labels; retain deliberate hook/serving/CTA text only.
 c['overlay_windows']=[w for w in c['overlay_windows'] if w.get('id') in ['T01','T04','T05','I12-label','I13-label']]

assert norm(' '.join(c['script_excerpt'] for c in old))==norm(' '.join(c['script_excerpt'] for c in coverage))
assert coverage[0]['start']==0 and coverage[-1]['end']==182.6
for a,b in zip(coverage,coverage[1:]):assert abs(a['end']-b['start'])<.001,(a['id'],b['id'])
for c in coverage:
 assert Path(c['frame']).is_file(),c['frame']
 if c.get('asset_key') and 'Podcast' not in c['mode']:assert c['duration']<=4.001,c['id']

inserts=[]
for c in coverage:
 if c.get('insert_id'):
  inserts.append({'id':c['insert_id'],'beat_id':c['beat_id'],'coverage_id':c['id'],'start':c['start'],'end':c['end'],'duration':c['duration'],'kind':c['mode'],'frame':c['frame'],'label':'','visual':c['visual'],'cue':c['script_excerpt'],'transition_in':'straight cut','transition_out':'straight cut to next scheduled picture','max_visible_seconds':4,'timing':'provisional; final 1.1× voice alignment required'})
schedule={'revision':4,'max_seconds':4,'timing_basis':story['meta']['timing_basis'],'inserts':inserts,'text_overlays':[w for c in coverage for w in c['overlay_windows']],
 'explicit_continuous_sequence_exception':{'coverage':['S26-1','S26-2'],'start':109.58,'end':114.95,'duration':5.37,'reason':'Latest user specifically requests scientific B-roll across both cards; two distinct microviews, no presenter interruption.'}}
for b in story['beats']:
 cs=[c for c in coverage if c['beat_id']==b['id']]
 b.update(frame=cs[0]['frame'],visual=' / '.join(c['visual'] for c in cs),mode='Timed picture — see coverage cards',overlay='',overlay_windows=[w for c in cs for w in c['overlay_windows']],insert_windows=[x for x in inserts if x['beat_id']==b['id']],coverage_ids=[c['id'] for c in cs],edit='Follow the v4 coverage schedule; all timing provisional.',proxy='Selected storyboard images and motion directions; no finished video.')
story['meta'].update(title='Motilli · Podcast storyboard v4 · mechanism and everyday relief',revision=4,status='Selected replacement first frames and ingredient overlays; exact script v7 preserved. No finished motion or video.',image_provider='Kie.ai',image_model='GPT Image 2',mechanism_coverage='Text-free navy scientific inserts; candid phone footage for symptom and desired-state emotions.')
story['meta'].pop('podcast_picture_seconds',None);story['meta'].pop('insert_seconds',None)
story['coverage']=coverage
spec=read(OLD/'board-spec.json')
spec.update(title=story['meta']['title'],project='motilli',summary='V4 · Follow the spoken meaning: distinct navy scientific views for mechanisms; candid phone footage for discomfort and everyday relief. Same female host on top of the reaction split. Actual fiber-supplement reference. Ingredient images over the guest. Exact narration preserved. All timing provisional; selected first frames and motion directions, not finished video.')
reference=[l for l in spec['timelines'] if l['label'].startswith('REFERENCE')][0]
for b in reference['beats']:
 b['note']='Original source evidence only. The source’s male listening cohost is not part of our version. Our reaction split uses the established female host on top; original footage remains unaltered.'
presenters=spec['timelines'][0]
presenters['label']='PRESENTER CONTINUITY · AI VISUAL CONCEPTS'
presenters['beats'].append({'t':'OUR REACTION SPLIT · female host TOP','frame':str(A/'podcast-split.png'),'visual':'Female host above the existing speaking guest. Replaces the source’s unrelated male listening cohost.','note':'Same identities and wardrobe throughout; AI concepts, not recordings or endorsements.'})
spec['timelines']=[presenters]
for section in sorted(set(c['section'] for c in coverage)):
 cs=[c for c in coverage if c['section']==section]
 spec['timelines'].append({'label':f"{section:02} · {cs[0]['chapter']} · V4 TIMED PICTURE",'beats':[
  {'t':f"{c['id']} · ~{c['start']:.2f}–{c['end']:.2f}s · {c['duration']:.2f}s",'script':c['script_excerpt'],'frame':c['frame'],'visual':c['visual'],'emotion':c['emotion'],
   'note':c['edit']+'\n'+c.get('text_policy','Separate phrase captions only, maximum four seconds.')+'\n'+'\n'.join(f"Text window {w['start']:.2f}–{w['end']:.2f}s: {w['label']}" for w in c['overlay_windows'])+'\n'+c['proxy']} for c in cs]})
spec['timelines'].append(reference)
spec['notes']=[
 {'title':'KEEP THE WORDS','text':'Script v7, 575 spoken words, remains unchanged. 182.60 seconds is a provisional allocation, not final voice alignment. Final voice preference 1.1×; remove dead air before aligning cuts.','color':'#dff2e1'},
 {'title':'SCIENCE VS EMOTION','text':'Scientific mechanisms: dark navy, physically distinct anatomy and action, no text. Fullness, burps and relief: casual candid iPhone footage of ordinary women. Ingredient names: photographic image overlays over the guest.','color':'#dff2e1'},
 {'title':'S26 CONTINUITY','text':'Scientific B-roll spans S26-1 and S26-2 as requested: 5.37 seconds continuously, using two different microscopic views. This specific latest direction overrides the old continuous-insert cap for this passage only. Other individual inserts remain at most four seconds.','color':'#fdf3c9'},
 {'title':'FEMALE HOST ON TOP','text':'The female host stays in the top reaction panel. The original source’s male listening cohost remains visible only in the separate reference lane as historical evidence. Do not use that source reaction image in our ad.','color':'#dff2e1'},
 {'title':'MOTION HANDOFF','text':'All replacement cards contain selected generated first frames and explicit actions. Use Google Omni when motion production is requested; DaVinci Resolve for the eventual edit. This revision does not generate a new narration or final video.','color':'#f7f5ee'},
 {'title':'SOURCE AND PRODUCT PROVENANCE','text':'Metamucil pack identity comes from its official product image. Soluble powder depicts FOS as an ingredient, not a different finished-product recommendation. Existing Motilli product frames retain their prior composition-reference status. Scientific visuals illustrate the supplied narrative; they are not clinical evidence.','color':'#f7f5ee'}]
save(D/'podcast-coverage.json',coverage);save(D/'overlay-schedule.json',schedule);save(D/'storyboard.json',story);save(D/'board-spec.json',spec)
save(V/'selected-asset-map.json',{c['id']:{'asset':c.get('asset_key'),'frame':c['frame'],'mode':c['mode']} for c in coverage})
md='# Motilli podcast storyboard v4\n\n[Open Cut Room](http://localhost:8765/b/motilli-podcast-dvhp-storyboard). Exact script v7 preserved; timing provisional.\n\n'
for c in coverage:md+=f"## {c['id']} · {c['start']:.2f}–{c['end']:.2f}s\n\n{c['script_excerpt']}\n\n**Picture:** {c['visual']}\n\n**Purpose:** {c['emotion']}\n\n**Edit:** {c['edit']}\n\n"
(D/'storyboard.md').write_text(md)
(D/'asset-list.md').write_text('# V4 selected assets\n\nCurrent image selections and motion instructions are in the Cut Room board and `v4/selected-asset-map.json`. Prior versions are in archives. The first frames are generated stills, not finished motion.\n\n'+ '\n'.join(f"- {c['id']}: {c['visual']}" for c in coverage if c.get('asset_key')))
for f in ['storyboard.html','whiteboard.html']:
 (D/f).write_text('<!doctype html><html><head><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=http://localhost:8765/b/motilli-podcast-dvhp-storyboard"><title>Motilli Podcast v4 — Cut Room</title></head><body><a href="http://localhost:8765/b/motilli-podcast-dvhp-storyboard">Open the current V4 Cut Room storyboard</a></body></html>')
# Protect any human edits made since this revision began.
board=ROOT/'cutroom/boards/motilli-podcast-dvhp-storyboard.json'
assert read(board)==read(OLD/'cutroom-board-before-v4.json'),'Live board changed since archive: reconcile before replacing.'
subprocess.run([sys.executable,str(ROOT/'cutroom/board_builder.py'),str(D/'board-spec.json'),'--slug','motilli-podcast-dvhp-storyboard'],check=True)
save(V/'audit/structural-qa.json',{'revision':4,'script_hash_preserved':True,'ordered_spoken_words_preserved':True,'spoken_words':575,'dialogue_beats':41,'picture_cards':len(coverage),'duration':182.6,'picture_contiguous':True,'all_selected_files_exist':True,'new_asset_ids':sorted({c['asset_key'] for c in coverage if c.get('asset_key')}),'individual_new_inserts_max_4s':True,'continuous_exception':schedule['explicit_continuous_sequence_exception'],'final_video_exported':False})
print('Rebuilt v4:',len(coverage),'picture cards; narration preserved.')
