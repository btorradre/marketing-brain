from pathlib import Path
import json,subprocess
import numpy as np
from scipy.signal import correlate,correlation_lags
R=Path(__file__).resolve().parent;P=R.parent
def audio(f):
 return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(f),'-vn','-ac','1','-ar','8000','-f','f32le','-']),dtype=np.float32)
result={}
for h in ('H1','H2','H3'):
 ref=audio(P/'voice'/h/'narration.mp3')
 for a in ('A1','A2','A3'):
  ident='VEL-OM-'+h+'-'+a;got=audio(R/'avatars'/ident/'avatar-native.mp4')
  cor=correlate(got,ref,mode='full',method='fft');lags=correlation_lags(len(got),len(ref));ix=np.argmax(cor);lag=int(lags[ix])
  left=max(0,lag);start=max(0,-lag);n=min(len(got)-left,len(ref)-start)
  score=float(np.corrcoef(got[left:left+n],ref[start:start+n])[0,1])
  result[ident]={'source_audio_offset_seconds':lag/8000,'correlation':score,'native_duration_seconds':len(got)/8000,'selected_duration_seconds':len(ref)/8000}
  print(ident,result[ident],flush=True)
(R/'qa/source-audio-correspondence.json').write_text(json.dumps(result,indent=2))
assert all(abs(v['source_audio_offset_seconds'])<1/30 and v['correlation']>.95 for v in result.values())
