from pathlib import Path
import json,shutil
P=Path(__file__).resolve().parents[2];O=P/'edit/production-v11';jobs=json.loads((O/'wardrobe-jobs.json').read_text());mapping={j['id']:j for j in jobs}
f=P/'storyboard/cutroom-spec.json';s=json.loads(f.read_text());s['title']='MOT-UGC-YAPPER-01 — Production v11 · varied wardrobe + cramping overlay';s['summary']='V11: twelve unique lifestyle B-roll outfits, regenerated with Google Omni from GPT Image2 wardrobe edits. Added centered720×720 emotional cramping still during the concrete line. Exact V3 Creative audio, Avatar V, captions and pacing preserved. Existing square community/research overlays retained. Two gummies; no branded products or guarantee overlay.'
for lane in s['timelines'][:6]:
 for b in lane['beats']:
  ident=b['t'].split(' ·')[0]
  if ident in mapping:
   j=mapping[ident];b['frame']=j['selected_image'];b['visual']=('Mature woman seated on sofa, leaning forward and holding her abdomen with a restrained wince. Centered720×720 square overlay.' if j['type']=='overlay' else b['visual'])+' Wardrobe: '+j['outfit'];b['note']=f"V11 selected replacement. {j['start']:.3f}–{j['end']:.3f}s; frames{j['start_frame']}–{j['end_frame']}. Straight cuts. Exact narration/captions preserved. "+('Square at x180/y600; returns to presenter.' if j['type']=='overlay' else 'Google Omni moving B-roll; unique outfit and original scene action.')
for b in s['timelines'][6]['beats']:
 if b['t'].startswith('TWO-GUMMY ROUTINE'):b['frame']=mapping['B35']['selected_image'];b['visual']='Exactly two dark-green heart gummies with dusty-peach sleeve.';b['note']='Selected provider source0.000–2.333s; unchanged70frame insert.'
s['timelines'][6]['beats'].append({'t':'V11 CRAMPING SQUARE · B04','frame':mapping['B04']['selected_image'],'visual':'Selected emotional square: mature presenter holding stomach in dusty-rose sweatshirt.','note':'720×720 centered;16.733–20.733seconds.'})
f.write_text(json.dumps(s,indent=2,ensure_ascii=False))
f=P/'storyboard/beat-cards.json';beats=json.loads(f.read_text())
for b in beats:
 if b['id'] in mapping:
  j=mapping[b['id']];b['frame']=j['selected_image'];b['wardrobe']=j['outfit'];b['visual']=next(x['visual'] for l in s['timelines'][:6] for x in l['beats'] if x['t'].split(' ·')[0]==b['id']);b['cue']=j['cue']+f"; {j['start']:.3f}–{j['end']:.3f}s, straight cuts."
f.write_text(json.dumps(beats,indent=2,ensure_ascii=False));(O/'aligned-beats.json').write_text(json.dumps(beats,indent=2,ensure_ascii=False))
ins=json.loads((O.parent/'production-v10/aligned-inserts.json').read_text())
for b in ins:
 if b['id'] in mapping:
  j=mapping[b['id']];b.update(source_image=j['selected_image'],path=str(O/f"normalized/{j['asset']}.mp4"),source_start_frame=j['source_start_frame'],wardrobe=j['outfit'])
 if b['id']=='B26':b['caption_tilt']=0
j=mapping['B04'];ins.append({**j,'source_image':j['selected_image'],'path':str(O/'woman-cramping-square.mov'),'source_start_frame':0,'layout':'720×720 centered x180/y600'})
ins.sort(key=lambda b:b['start_frame']);(O/'aligned-inserts.json').write_text(json.dumps(ins,indent=2));shutil.copy2(O.parent/'production-v10/deliverables/Motilli-Unbranded-VSL-v10.srt',O/'deliverables/Motilli-Unbranded-VSL-v11.srt')
print('Updated13selected cards and production sources; exact narration retained')
