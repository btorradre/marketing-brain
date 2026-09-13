from pathlib import Path
import json,copy
P=Path(__file__).resolve().parent.parent.parent;O=P/'edit/production-v9';A=P/'assets/images-v9'
f=P/'storyboard/cutroom-spec.json';s=json.loads(f.read_text());s['title']='MOT-UGC-YAPPER-01 — Production v9 · apigenin research'
s['summary']='FINAL v9: 4:38 vertical ad with V3 Creative narration and Avatar V. Real PMC article screenshot added during apigenin research at2:33.97–2:38.37, immediately after the celery insert. The supplied paper is an in vitro microbiota study and does not demonstrate the narrated receptor/contraction mechanism; study type is identified on screen. V8 full community post retained. Voice, pacing and captions preserved; no branded products or guarantee graphic; two gummies retained.'
for lane in s['timelines'][:6]:
 for i,b in enumerate(lane['beats']):
  if b['t'].startswith('B27 ·'):
   b['note']='Celery on apigenin from celery juice at2:31.13–2:33.97; straight cut to the actual paper screenshot on research until2:38.37, then presenter. Caption words, timing and placement unchanged.'
   lane['beats'].insert(i+1,{'t':'B27 RESEARCH INSERT · 02:34.0–02:38.4','script':'','frame':str(A/'apigenin-research-overlay.png'),'visual':'Actual PMC article title, authors, date and full abstract, with separate in vitro microbiota study label. Captions below the paper.','emotion':'Research context — let viewers see the supplied source and its actual study scope.','note':'Straight cut at2:33.967 on research;4.4seconds, then presenter. Paper studies gut bacteria in vitro, not the narrated gut-wall receptor/contraction mechanism. No fabricated page text or claim highlighting.'});break
sources=s['timelines'][6]['beats']
for b in sources:
 if b['t']=='FINAL FACE HOLD · 3s':b['t']='FINAL FACE · NO SILENT HOLD';b['note']='End promptly after the final spoken word. No additional silent hold, product or guarantee graphic.'
sources.append({'t':'V9 ACTUAL APIGENIN ARTICLE','script':'','frame':str(A/'apigenin-research-overlay.png'),'visual':'Selected screenshot-based research overlay from PMC6152273.','note':'Actual screenshot captured from the public article, cropped and scaled without altering text. Separate in vitro microbiota label; no claim validation or fabricated highlights.'})
f.write_text(json.dumps(s,indent=2,ensure_ascii=False))
f=P/'storyboard/beat-cards.json';beats=json.loads(f.read_text())
for b in beats:
 if b['id']=='B27':
  b['cue']='Celery151.133–153.967s; real paper screenshot153.967–158.367s; return to presenter.'
  b['additional_inserts']=[{'asset':'apigenin-research','frame':str(A/'apigenin-research-overlay.png'),'start':4619/30,'end':4751/30,'duration':4.4,'study_scope':'In vitro gut microbiota; does not substantiate receptor/contraction claim.'}]
f.write_text(json.dumps(beats,indent=2,ensure_ascii=False));(O/'aligned-beats.json').write_text(json.dumps(beats,indent=2,ensure_ascii=False))
ins=json.loads((O.parent/'production-v8/aligned-inserts.json').read_text())
for b in ins:
 if b['id']=='B27':b['end_frame']=4619;b['end']=4619/30
ins.append({'id':'B27-research','asset':'apigenin-research','type':'overlay','cue':'research','start_frame':4619,'end_frame':4751,'start':4619/30,'end':4751/30,'source_start_frame':0,'source_image':str(A/'apigenin-research-overlay.png'),'path':str(O/'apigenin-research-overlay.mov')});ins.sort(key=lambda x:x['start_frame']);(O/'aligned-inserts.json').write_text(json.dumps(ins,indent=2))
