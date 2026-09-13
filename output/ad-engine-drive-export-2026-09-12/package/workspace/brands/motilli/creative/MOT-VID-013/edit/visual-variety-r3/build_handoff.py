import json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parent;P=R.parents[1]
NATIVE=Path('/Users/brooksorradre2/Movies/CapCut/User Data/Projects/com.lveditor.draft/MOT-VID-013-HOOK-A-Remedy-Cabinet')
rows=json.loads((R/'shot-plan.json').read_text());native=json.loads((R/'native-picture-segments.json').read_text());requests=json.loads((R/'video-requests.json').read_text())
parts=[]
for index,n in enumerate(native):
 row=next(x for x in rows if x['start']<=n['start']+.01 and x['end']>n['start']+.01)
 id=row['id'] if row['id']!='S06' else ['S06a','S06b','S06c','S06d'][index-5]
 if row['decision']=='generate':
  motion=R/'motion'/f'{id}.mp4';frame=R/'keyframes'/f'{id}.png';source=motion if motion.exists() else None;state='motion downloaded; source QA complete' if source else 'motion pending'
 elif row['decision']=='graphic':source=Path(row['source']);frame=R/'keyframes'/f'{id}.png';state='editable ingredient-free setup card; use native text or supplied SVG'
 elif row['decision']=='library':source=P/'output/omni'/f'{id}.mp4';frame=R/'audit'/f'library-{id}.jpg';state='existing distinct source; source QA complete'
 else:source=NATIVE/'Resources'/Path(n['source']).name;frame=Path(row['before_frame']);state='retained source'
 parts.append({'id':id,'native_segment_id':n['segment']['id'],'start_frame':round(n['start']*30),'end_frame':round(n['end']*30),'duration_frames':round(n['duration']*30),'decision':row['decision'],'visual':row['visual'],'source':str(source) if source else None,'keyframe':str(frame),'status':state,'original_source':n['source'],'original_source_range':n['segment']['source_timerange'],'picture_speed':1 if row['decision']!='keep' else n['segment']['speed']})
missing=[x['id'] for x in parts if not x['source']];unsubmitted=[x for x in requests if not (R/'receipts'/f"{x['id']}-video.json").exists()]
data={'version':'R3','status':'Three native CapCut R3 projects assembled; final export QA pending','ready_for_export':False,'source_export':'/Users/brooksorradre2/Downloads/MOT-BACKED-UP/MOT-VID-013-HOOK-A-Remedy-Cabinet.mp4','native_source':str(NATIVE),'timing_source':str(P/'edit/capcut-r2/timing.json'),'narration_speed':1.1,'duration_seconds':95.9,'fps':30,'width':1080,'height':1920,'preserve':['all 32 narration segment source ranges, speed and gains','music track','all 95 caption timings','2-frame cue compensation','0.5-second CTA hold'],'editor_dependency':'CapCut confirmed by user; see capcut/projects.json for the three original-project R3 duplicates.','unsubmitted_motion':[x['id'] for x in unsubmitted],'missing_motion':missing,'segments':parts}
(R/'revision-handoff.json').write_text(json.dumps(data,indent=2))
print(json.dumps({'segments':len(parts),'unique_ids':len(set(x['id'] for x in parts)),'missing_motion':missing,'unsubmitted_motion':data['unsubmitted_motion']}))
