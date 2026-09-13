from pathlib import Path
import json,math
P=Path(__file__).resolve().parent;B=P.parent;R=P/'resolve-speed110';R.mkdir(exist_ok=True)
scribe=[w for w in json.loads((R/'source-scribe.json').read_text())['words'] if w['type']=='word']
gaps=[]
for a,b in zip(scribe,scribe[1:]):
 if b['start']-a['end']>.22:
  end=a['end']
  if a['text']=='Weekender.':end=max(end,12.319)
  gaps.append({'after':a['text'],'before':b['text'],'speech_end':end,'next_start':b['start']})
gaps.append({'after':'Weekender.','before':'Check','speech_end':46.039,'next_start':46.5})
gaps.sort(key=lambda x:x['speech_end'])
# Keep 2–3 frames after articulation and 2 frames before next onset.
# Earlier Scribe compartment end (38.959) resolves forced-alignment's erroneous39.959.
remove=[{'start':0,'end':3,'reason':'0.10s leading empty margin; first word onset0.14 retained'}]
for g in gaps:
 a=math.ceil((g['speech_end']+.060)*30);b=math.floor((g['next_start']-.060)*30)
 if b-a>=2:remove.append({'start':a,'end':b,'reason':g})
keep=[];pos=0;record=0
for d in remove:
 if d['start']>pos:
  keep.append({'source_start':pos,'source_end':d['start'],'record_start':record,'record_end':record+d['start']-pos});record+=d['start']-pos
 pos=d['end']
keep.append({'source_start':pos,'source_end':1431,'record_start':record,'record_end':record+1431-pos});record+=1431-pos
out={'source_timeline':'Weekender-Haaland-Gringo-Natural-AvatarV-v2','fps':30,'speed':1.1,'pitch_correction':True,'source_frames':1431,'kept_frames':record,'removed_frames':1431-record,'removed_seconds':(1431-record)/30,'estimated_output_frames':int(record/1.1),'remove':remove,'keep':keep}
(R/'time-map-plan.json').write_text(json.dumps(out,indent=2))
def mapped(f):
 return sum(max(0,min(f,k['source_end'])-k['source_start']) for k in keep)/1.1
scenes=json.loads((P/'resolve-gringo-aligned/aligned-scenes.json').read_text())
for s in scenes:
 s['source_start']=s['start'];s['source_end']=s['end'];s['start']=round(mapped(s['start']));s['end']=round(mapped(s['end']));s['speech_end']=round(mapped(s['speech_end']))
scenes[-1]['end']=int(record/1.1)
(R/'aligned-scenes-planned.json').write_text(json.dumps(scenes,indent=2))
p=B/'edit/editing-plan.md';p.write_text(p.read_text()+'\nMeasured pacing map: '+str(len(remove)-1)+' inter-word/sentence gaps shortened with two-frame articulation margins, plus0.10s leading trim. Removed '+str(round((1431-record)/30,3))+'s from the47.70s source; remaining '+str(round(record/30,3))+'s becomes approximately '+str(round(record/33,3))+'s at110%. Source Scribe independently resolves compartment ending38.959s (forced alignment had incorrectly extended it into the following pause). Explicit keep/remove ranges are in production/resolve-speed110/time-map-plan.json.\n\n| Scene | Revised provisional seconds | Spoken cue / scene purpose |\n|---|---|---|\n'+'\n'.join('| '+s['id']+' | '+f"{s['start']/30:.3f}–{s['end']/30:.3f}"+' | '+s['script']+' |' for s in scenes)+'\n')
print({k:v for k,v in out.items() if k not in ['remove','keep']});print(remove)
