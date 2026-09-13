from pathlib import Path
import json,subprocess,math
import numpy as np
P=Path(__file__).resolve().parent;V7=P.parent/'v7';words=[dict(word=w['text'],start=w['start']/1.1,end=w['end']/1.1) for w in json.load(open(P.parent/'v5/qa/final-scribe.json'))['words'] if w['type']=='word'];raw=subprocess.run(['ffmpeg','-v','error','-i',str(V7/'deliverables/Motilli-Podcast-110-percent.mp4'),'-vn','-ar','48000','-ac','1','-f','f32le','-'],capture_output=True,check=True).stdout;y=np.frombuffer(raw,np.float32);rms=np.array([np.sqrt(np.mean(y[i*1600:(i+1)*1600]**2)) for i in range(5379)]);db=20*np.log10(np.maximum(rms,1e-9));cuts=[];rejected=[]
for a,b in zip(words,words[1:]):
 gap=b['start']-a['end']
 if gap<.18:continue
 s=math.ceil((a['end']+.035)*30);e=math.floor((b['start']-.035)*30)
 # Trim only the quiet center; keep word tail and next onset outside the edit.
 while s<e and db[s]>-34:s+=1
 while e>s and db[e-1]>-34:e-=1
 row={'start':s,'end':e,'gap_start':a['end'],'gap_end':b['start'],'before':a['word'],'after':b['word'],'original_gap_seconds':gap,'removed_seconds':(e-s)/30,'max_frame_rms_db':float(db[s:e].max()) if e>s else None}
 if e-s>=2 and np.max(db[s:e])<=-31:cuts.append(row)
 else:rejected.append(row)
# Only a short exit breath after the final word, rather than a motionless long tail.
s=math.ceil((words[-1]['end']+.1)*30)
if 5379-s>=2 and np.max(db[s:])<=-31:cuts.append({'start':s,'end':5379,'before':words[-1]['word'],'after':'END','removed_seconds':(5379-s)/30,'max_frame_rms_db':float(db[s:].max())})
(P/'pause-cuts.json').write_text(json.dumps(cuts,indent=2));(P/'qa/retained-boundary-gaps.json').write_text(json.dumps(rejected,indent=2));print('Cuts',len(cuts),'removed',sum(c['end']-c['start'] for c in cuts)/30,'seconds; retained boundary gaps',len(rejected))
for c in cuts:print(c['start'],c['end'],c['before'],'→',c['after'],round(c['removed_seconds'],3),round(c['max_frame_rms_db'],1))
