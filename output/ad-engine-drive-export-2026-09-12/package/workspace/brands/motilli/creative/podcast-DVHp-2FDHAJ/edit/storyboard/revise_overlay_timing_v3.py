from pathlib import Path
import json,shutil,sys,hashlib,html
D=Path(__file__).resolve().parent;P=D.parents[1];ROOT=P.parents[3];R=ROOT/'brands/motilli/creative/MOT-VID-013/edit/visual-variety-r3'
archive=D/'v2-archive';archive.mkdir(exist_ok=True)
for name in ['storyboard.json','board-spec.json','storyboard.html','storyboard.md','whiteboard.html','asset-list.md']:
 if not (archive/name).exists():shutil.copy2(D/name,archive/name)
old=json.loads((archive/'storyboard.json').read_text());spec_old=json.loads((archive/'board-spec.json').read_text());beats=old['beats'];meta=old['meta']
G=D/'generated'
# One independent insert per selected concept, with actual podcast coverage in between.
raw=[
('I01','S03',11.69,14.21,R/'keyframes/S04.png','SLOWER STOMACH EMPTYING','Isolated stomach exterior, emptying location.','slowed emptying from the stomach'),
('I02','S04',16.21,18.32,R/'keyframes/S18.png','SLOWER CONTRACTIONS','Side-on intestinal contraction view.','contractions'),
('I03','S06',25.50,29.50,G/'intake-gpt-image-2-5-kie.png','LESS FOOD · LESS FIBER','Scientific smaller-meal and fiber-intake illustration.','appetite decreases / fiber'),
('I04','S11',49.20,53.20,G/'hydration-gpt-image-2-5-kie.png','WATER IN THE COLON','Scientific colon hydration illustration.','water in the stool in your colon'),
('I05','S13',57.50,61.50,R/'keyframes/S09.png','FULLNESS AFTER EATING','Empty gastric section; different composition from the earlier exterior.','fullness after eating'),
('I06','S16',67.90,69.79,R/'keyframes/S12.png','BULKING FIBER + WATER','Laboratory-style fiber hydration beaker.','absorb water and expand'),
('I07','S19',83.70,87.20,R/'keyframes/S13.png','SULFUR ODOR','Scientific oesophagus and rising gas; no early ingredient name or swatch.','rotten-egg burps / sulfur odor'),
('I08','S22',94.85,98.85,G/'movement-gpt-image-2-5-kie.png','SUPPORTING NATURAL MOVEMENT','Full scientific stomach-movement overview.','natural wave-like movement'),
('I09','S23',100.85,103.58,R/'keyframes/S26.png','SULFUR-ODOR CONTROL','Scientific odor particles near a nose profile; distinct from the earlier schematic.','sulfur-odor control'),
('I10','S25',106.74,109.58,G/'fiber-gpt-image-2-5-kie.png','LOW-VISCOSITY FIBER','Scientific fiber comparison; separate from the earlier beaker pour.','low-viscosity soluble prebiotic fiber'),
('I11','S26',111.58,114.95,G/'prebiotic-gpt-image-2-5-kie.png','PREBIOTIC FIBER','Microscopic beneficial-bacteria illustration.','feeds beneficial bacteria'),
('I12','S29',122.20,125.69,Path(next(b['frame'] for b in beats if b['id']=='S29')),'MOTILLI · 2 GUMMIES DAILY','Product reveal composition proxy; approved packaging still required.','combined in Motilli'),
('I13','S32',137.48,140.98,R/'keyframes/S28.png','A SMALL DAILY SERVING','Two heart-shaped gummies on a palm, rather than a second jar shot.','small daily serving')]
inserts=[]
for id,bid,a,z,frame,label,visual,cue in raw:
 assert frame.exists(),frame
 inserts.append({'id':id,'beat_id':bid,'start':a,'end':z,'duration':round(z-a,2),'kind':'science' if id<'I12' else 'product','frame':str(frame),'label':label,'visual':visual,'cue':cue,'transition_in':'hard cut','transition_out':'hard cut to active speaker / podcast','max_visible_seconds':4.0,'timing':'provisional; align to actual speech, never exceed 120 frames at 30 fps'})
text_overlays=[
{'id':'T01','beat_id':'S01','start':0.0,'end':3.5,'label':'HOW GLP-1s SLOW THE GUT'},
{'id':'T02','beat_id':'S09','start':39.48,'end':42.98,'label':'MiraLAX? MORE FIBER?'},
{'id':'T03','beat_id':'S21','start':90.64,'end':93.64,'label':'APIGENIN · PLANT COMPOUND'},
{'id':'T04','beat_id':'S31','start':130.4,'end':133.4,'label':'A SMALL DAILY SERVING'},
{'id':'T05','beat_id':'S41','start':178.6,'end':182.6,'label':'MOTILLI · LINK BELOW · 90-DAY MONEY-BACK GUARANTEE'}]
for x in text_overlays:x.update(duration=round(x['end']-x['start'],2),max_visible_seconds=4.0,transition='cut on / cut off; timing includes all visibility')
coverage=[]
for b in beats:
 previous_mode=b['mode'];is_host=previous_mode=='Podcast · host';mixed=b['id']=='S01'
 base_mode='Podcast · two-person' if mixed else 'Podcast · host' if is_host else 'Podcast · guest'
 base_frame=str(G/('host-gpt-image-2-5-kie.png' if is_host or mixed else 'guest-gpt-image-2-5-kie.png'))
 base_visual='Host and guest exchange the opening lines; use the speaking camera or a clean two-person view.' if mixed else 'Host asks the question; keep the guest audible at handoff.' if is_host else 'Guest continues speaking naturally; host listens. Use the active-speaker camera or a clean two-person view.'
 ib=[x for x in inserts if x['beat_id']==b['id']];tb=[x for x in text_overlays if x['beat_id']==b['id']]
 boundaries=sorted(set([b['start'],b['end']]+[t for x in ib for t in [x['start'],x['end']]]))
 words=b['spoken'].split();segments=[]
 for n,(a,z) in enumerate(zip(boundaries,boundaries[1:])):
  insert=next((x for x in ib if x['start']<=a+.00001 and x['end']>=z-.00001),None)
  i0=round((a-b['start'])/(b['end']-b['start'])*len(words));i1=round((z-b['start'])/(b['end']-b['start'])*len(words))
  seg={'id':f"{b['id']}-{n+1}",'beat_id':b['id'],'section':b['section'],'chapter':b['chapter'],'start':a,'end':z,'duration':round(z-a,2),'mode':('Science · insert' if insert['kind']=='science' else 'Product · insert') if insert else base_mode,'frame':insert['frame'] if insert else base_frame,'visual':insert['visual'] if insert else base_visual,'script_excerpt':' '.join(words[i0:i1]),'script_excerpt_timing':'proportional estimate, not forced alignment','insert_id':insert['id'] if insert else None,'overlay_windows':([{'id':insert['id']+'-label','start':a,'end':z,'label':insert['label']}] if insert else [x for x in tb if x['end']>a and x['start']<z]),'edit':f"{'Cut to the insert' if insert else 'Podcast camera coverage'} at ~{a:.2f}s. {'Return to the speakers' if insert else 'Keep the natural spoken answer continuous'} at ~{z:.2f}s. No lingering overlay beyond its listed out cue.",'proxy':('Product composition reference only; current approved packaging required.' if insert and insert['id']=='I12' else 'Selected scientific/product keyframe; finished motion not implied.' if insert else 'AI presenter visual concept; not an actual recording or endorsement.')}
  coverage.append(seg);segments.append(seg['id'])
 b.update(mode=base_mode,frame=base_frame,visual=base_visual,overlay='',overlay_windows=tb,insert_windows=ib,coverage_ids=segments,edit='Default to the podcasters. Show only the explicit insert/overlay windows; clear all other graphics. Guest audio remains continuous. All times provisional.',proxy='AI presenter concept; actual footage and final voice alignment pending.',source_key='kie-presenter:host' if is_host or mixed else 'kie-presenter:guest')
# Validate continuous exposure, not just individual card labels.
assert all(0<x['duration']<=4.0 for x in inserts+text_overlays)
assert all(round(b['start']-a['end'],2)>=2.0 for a,b in zip(inserts,inserts[1:]))
assert all(abs(a['end']-b['start'])<.001 for a,b in zip(coverage,coverage[1:]))
assert abs(coverage[-1]['end']-meta['estimated_seconds'])<.001
for b in beats:
 rebuilt=' '.join(x['script_excerpt'] for x in coverage if x['beat_id']==b['id']).strip()
 assert rebuilt==b['spoken'],b['id']
assert [b['script'] for b in beats]==[b['script'] for b in json.loads((archive/'storyboard.json').read_text())['beats']]
assert len(set(hashlib.sha256(Path(x['frame']).read_bytes()).hexdigest() for x in inserts))==len(inserts)
insert_seconds=round(sum(x['duration'] for x in inserts),2);podcast_seconds=round(meta['estimated_seconds']-insert_seconds,2)
meta.update(title='Motilli · Podcast storyboard v3 · four-second overlay cap',revision=3,status='Podcast-first coverage. Every insert and editorial overlay is limited to four seconds. Full script intact; all timing provisional, no finished edit implied.',overlay_max_seconds=4.0,mechanism_coverage='Short full-frame scientific inserts; return to podcasters between them.',podcast_picture_seconds=podcast_seconds,insert_seconds=insert_seconds)
doc={'meta':meta,'beats':beats,'coverage':coverage}
(D/'storyboard.json').write_text(json.dumps(doc,indent=2));(D/'overlay-schedule.json').write_text(json.dumps({'max_seconds':4,'timing_basis':meta['timing_basis'],'inserts':inserts,'text_overlays':text_overlays,'caption_rule':'Phrase chunks, each <=4 seconds; align after final voice.'},indent=2));(D/'podcast-coverage.json').write_text(json.dumps(coverage,indent=2))
notes=[]
for n in spec_old['notes']:
 if n['title']=='Mechanisms always use science':n={'title':'FOUR SECONDS MAXIMUM','text':'Every overlay and B-roll insert lasts at most 4.0 seconds, including its entrance and exit. Return to the host/guest between inserts. A crop, label change or new storyboard card never resets the same continuous insert.'}
 elif n['title']=='Caption and overlay system':n={'title':'Caption and overlay system','text':'Only the explicit overlay windows appear. No general graphic held over a long answer. Captions advance in short phrases, <=4 seconds each. Clear all future-pacing callouts and keep the conversation visible.'}
 elif n['title']=='Scientific direction':n={'title':'Scientific direction','text':'Use brief, relevant full-frame scientific views at the marked mechanism cues. Let the guest explain the rest on camera. Distinct selected compositions; at least two seconds of podcast picture between inserts.'}
 notes.append(n)
notes.insert(1,{'title':'PICTURE BALANCE','text':f'{podcast_seconds:.2f}s podcast picture; {insert_seconds:.2f}s across {len(inserts)} short inserts. All {meta["spoken_words"]} spoken words and the ~182.6s planning length are unchanged. Final 1.1× voice alignment still required.'})
spec={**spec_old,'title':meta['title'],'summary':f'Podcast first. {len(inserts)} inserts, each at most 4 seconds. {round(podcast_seconds/meta["estimated_seconds"]*100)}% podcast picture. Long explanations return to the speakers; no 15-second overlays. Times remain provisional.','notes':notes}
# Preserve reference and casting context; replace production lanes with actual picture segments.
spec['timelines']=spec_old['timelines'][:2]
for section in sorted(set(x['section'] for x in coverage)):
 subset=[x for x in coverage if x['section']==section]
 spec['timelines'].append({'label':f"{section:02} · {subset[0]['chapter']} · TIMED PICTURE",'beats':[{'t':f"{x['id']} · ~{x['start']:.2f}–{x['end']:.2f}s · {x['duration']:.2f}s",'script':x['script_excerpt'],'frame':x['frame'],'visual':x['visual'],'emotion':x['mode']+' | '+('INSERT OUT → PODCAST' if x['insert_id'] else 'PODCAST CAMERA'),'note':x['edit']+'\n'+('\n'.join(f"Overlay {o['start']:.2f}–{o['end']:.2f}s: {o['label']}" for o in x['overlay_windows']) if x['overlay_windows'] else 'No editorial overlay; phrase captions only.')+'\n'+x['proxy']} for x in subset]})
(D/'board-spec.json').write_text(json.dumps(spec,indent=2));sys.path.insert(0,str(ROOT/'cutroom'));from board_builder import build
build(spec,'motilli-podcast-dvhp-storyboard')
md='# Podcast storyboard v3 — four-second overlay cap\n\nAll timing is provisional. Every overlay/insert <=4 seconds; podcast cameras carry the rest.\n\n'
md+='| Scene | In | Out | Duration | Spoken cue | Picture |\n|---|---|---|---|---|---|\n'+''.join(f"| {x['id']} / {x['beat_id']} | {x['start']:.2f} | {x['end']:.2f} | {x['duration']:.2f}s | {x['cue']} | {x['visual']} |\n" for x in inserts)
for b in beats:md+=f"\n## {b['id']} · ~{b['start']:.2f}–{b['end']:.2f}s\n\n{b['script']}\n\nDefault picture: {b['visual']}\n\n"+'\n'.join(f"Insert {x['id']}: {x['start']:.2f}–{x['end']:.2f}s, then return to podcast." for x in b['insert_windows'])+'\n'
(D/'storyboard.md').write_text(md)
# Standalone reader with local published assets, not a video-composition pipeline.
out=ROOT/'cutroom/assets/motilli-podcast-dvhp-storyboard';preview=out/'v3-previews';preview.mkdir(exist_ok=True)
from PIL import Image
urls={}
for x in coverage:
 f=Path(x['frame']);sha=hashlib.sha256(f.read_bytes()).hexdigest()[:12];dst=preview/(sha+'.jpg')
 if not dst.exists():im=Image.open(f).convert('RGB');im.thumbnail((420,748));im.save(dst,quality=88)
 urls[x['frame']]='/assets/motilli-podcast-dvhp-storyboard/v3-previews/'+dst.name
esc=html.escape
parts=['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Podcast v3 · four-second overlays</title><style>body{margin:0;background:#f2f0e9;color:#213b2e;font:16px/1.5 system-ui}header,main{max-width:1320px;margin:auto;padding:24px}header{background:#173f30;color:white}a{color:inherit}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(330px,1fr));gap:18px}.card{border:1px solid #d2d9cc;background:#fff;border-radius:10px;padding:14px}.card img{width:130px;float:left;margin:0 14px 8px 0;border-radius:6px}.card:after{content:"";display:block;clear:both}small{color:#64775e}.tag{font-weight:700;color:#416c36}.script{font-weight:600}.cue{padding:8px;background:#edf2e7}h1{line-height:1.1}section{margin:35px 0}</style><header><h1>Podcast first.<br>Every overlay: four seconds maximum.</h1><p>'+f'{round(podcast_seconds/meta["estimated_seconds"]*100)}% podcast picture · {len(inserts)} short inserts · {meta["spoken_words"]} spoken words preserved · provisional timing'+'</p><a href="/b/motilli-podcast-dvhp-storyboard?v=3">Open Cutroom</a></header><main><p>Short science and product inserts support the explanation. Return to the speaking podcaster when each insert ends. These are storyboard keyframes and AI presenter concepts; the finished edit and final voice alignment are pending.</p>']
for section in sorted(set(x['section'] for x in coverage)):
 subset=[x for x in coverage if x['section']==section];parts.append('<section><h2>'+esc(subset[0]['chapter'])+'</h2><div class="grid">')
 for x in subset:
  ov=''.join(f"<p class=\"cue\">Overlay ~{o['start']:.2f}–{o['end']:.2f}s: {esc(o['label'])}</p>" for o in x['overlay_windows']) or '<p>No editorial overlay. Phrase captions only.</p>'
  parts.append(f"<article class=\"card\" id=\"{x['id']}\"><h3>{x['id']} · ~{x['start']:.2f}–{x['end']:.2f}s</h3><img src=\"{urls[x['frame']]}\" alt=\"{esc(x['visual'])}\"><div class=\"tag\">{esc(x['mode'])} · {x['duration']:.2f}s</div><p class=\"script\">{esc(x['script_excerpt'])}</p>{ov}<p>{esc(x['edit'])}</p><small>{esc(x['proxy'])}</small></article>")
 parts.append('</div></section>')
parts.append('<section><h2>Unchanged full dialogue</h2>'+''.join('<p><b>'+b['id']+'</b><br>'+esc(b['script']).replace('\n','<br>')+'</p>' for b in beats)+'</section></main></html>')
reader=''.join(parts);(D/'storyboard.html').write_text(reader);(out/'storyboard.html').write_text(reader)
qa={'revision':3,'beats':len(beats),'picture_segments':len(coverage),'inserts':len(inserts),'insert_seconds':insert_seconds,'podcast_seconds':podcast_seconds,'podcast_percentage':round(podcast_seconds/meta['estimated_seconds']*100,1),'max_insert_seconds':max(x['duration'] for x in inserts),'max_editorial_overlay_seconds':max(x['duration'] for x in inserts+text_overlays),'min_podcast_gap_between_inserts':round(min(b['start']-a['end'] for a,b in zip(inserts,inserts[1:])),2),'all_insert_sources_unique':True,'dialogue_preserved':True,'continuous_picture_coverage':True,'finished_video_exported':False,'timing_provisional':True}
(D/'qa-v3.json').write_text(json.dumps(qa,indent=2));print(json.dumps(qa,indent=2))
