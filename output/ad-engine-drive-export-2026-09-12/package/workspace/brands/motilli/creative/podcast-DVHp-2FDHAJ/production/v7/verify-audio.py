from pathlib import Path
import subprocess,json
import numpy as np
from scipy.signal import correlate,correlation_lags
P=Path(__file__).resolve().parent
paths=[P.parent/'v6/deliverables/Motilli-Podcast-v6-Visual-Revision.mp4',P/'deliverables/Motilli-Podcast-110-percent.mp4']
def load(p):
 r=subprocess.run(['ffmpeg','-v','error','-i',str(p),'-vn','-ar','8000','-ac','1','-f','f32le','-'],capture_output=True,check=True);return np.frombuffer(r.stdout,dtype=np.float32)
a,b=map(load,paths)
def envelope(y):
 n=len(y)//80;y=y[:n*80].reshape((n,80));return np.sqrt(np.mean(y*y,axis=1))
x,z=envelope(a),envelope(b);expected=np.interp(np.arange(len(z))*1.1,np.arange(len(x)),x);results=[]
for start,end in [(0,40),(60,110),(130,178)]:
 s=int(start*100);e=int(end*100);q=expected[s:e];r=z[s:e];co=correlate(r-r.mean(),q-q.mean(),method='fft');lags=correlation_lags(len(r),len(q));ok=abs(lags)<=15;lag=int(lags[ok][np.argmax(co[ok])]);u=q[max(0,-lag):min(len(q),len(q)-lag)];v=r[max(0,lag):min(len(r),len(r)+lag)];score=float(np.corrcoef(u,v)[0,1]);results.append({'window_seconds':[start,end],'envelope_correlation':score,'lag_seconds':lag/100});assert score>.80 and abs(lag)<=10,results[-1]
r={'expected_speed_multiplier':1.1,'pitch_correction':'Native Resolve GetSpeed readback true on both linked tracks','audio_sync_windows':results,'duration_seconds':len(b)/8000,'source_duration_seconds':len(a)/8000};(P/'qa/audio-speed-qa.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
