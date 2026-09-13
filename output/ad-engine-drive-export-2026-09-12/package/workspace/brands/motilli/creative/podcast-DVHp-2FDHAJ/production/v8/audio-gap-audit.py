import json,subprocess,numpy as np
from pathlib import Path
P=Path(__file__).resolve().parent;v7=P.parent/'v7';y=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',str(v7/'deliverables/Motilli-Podcast-110-percent.mp4'),'-vn','-ar','48000','-ac','1','-f','f32le','-'],capture_output=True,check=True).stdout,np.float32);x=y[:5379*1600].reshape(5379,1600);db=20*np.log10(np.maximum(np.sqrt(np.mean(x*x,axis=1)),1e-9));quiet=db<=-34;words=[dict(word=w['text'],start=w['start']/1.1,end=w['end']/1.1) for w in json.load(open(P.parent/'v5/qa/final-scribe.json'))['words'] if w['type']=='word'];ranges=[];start=None
for i,q in enumerate(np.append(quiet,False)):
 if q and start is None:start=i
 if not q and start is not None:
  if i-start>=6:
   s=start+1;e=i-1;overlap=[w['word'] for w in words if min(e/30,w['end'])-max(s/30,w['start'])>.025];ranges.append(dict(start=s,end=e,quiet_start=start,quiet_end=i,overlap_words=overlap,max_frame_rms_db=float(db[s:e].max())))
  start=None
print('Global quiet candidates',len(ranges),'removed',sum(c['end']-c['start'] for c in ranges)/30)
for c in ranges:
 if c['overlap_words']:print(c['start']/30,c['end']/30,c['overlap_words'],c['max_frame_rms_db'])
(P/'qa/global-quiet-audit.json').write_text(json.dumps(ranges,indent=2))
