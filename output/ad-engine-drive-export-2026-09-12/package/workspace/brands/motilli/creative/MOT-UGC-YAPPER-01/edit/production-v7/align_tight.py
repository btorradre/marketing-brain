from pathlib import Path
import json,shutil,subprocess
O=Path(__file__).resolve().parent;edit=json.loads((O/'pause-edit-spec.json').read_text());chars=[];starts=[];ends=[]
for part in [1,2]:
 a=json.loads((O/f'part-{part}-forced.json').read_text());rows=[r for r in edit['rows'] if r['part']==part]
 def mapped(t):
  for r in rows:
   if t<r['source_start']/30:return r['record_start']/30
   if t<=r['source_end']/30:return (r['record_start']-r['source_start'])/30+t
  return rows[-1]['record_end']/30
 if part==2:chars.append(' ');starts.append(ends[-1]);ends.append(rows[0]['record_start']/30)
 for c in a['characters']:chars.append(c['text']);starts.append(mapped(c['start']));ends.append(mapped(c['end']))
text=''.join(chars);assert text==(O/'narration-exact.txt').read_text().strip()
(O/'eleven-alignment.json').write_text(json.dumps({'alignment':{'characters':chars,'character_start_times_seconds':starts,'character_end_times_seconds':ends},'source':'ElevenLabs forced alignment of actual V3 audio, transformed by verified Resolve pause-edit ranges'},indent=2))
for f in ['align_edit.py','prepare_graphics.py']:shutil.copy2(O.parent/'production-v6'/f,O/f)
subprocess.run(['python3',str(O/'align_edit.py')],check=True)
w=json.loads((O/'edited-scribe-words.json').read_text());g=[{'start':a['end'],'end':b['start'],'duration':b['start']-a['end'],'after':a['text'],'before':b['text']} for a,b in zip(w,w[1:])];j={'max_word_gap':max(x['duration'] for x in g),'over_350ms':[x for x in g if x['duration']>.35001],'leading_seconds':w[0]['start'],'ending_seconds':edit['edited_duration']-w[-1]['end'],'duration':edit['edited_duration'],'removed':edit['removed_total_seconds'],'pause_edits':edit['pause_edits']};(O/'tight-pacing-qa.json').write_text(json.dumps(j,indent=2));print(json.dumps(j,indent=2))
