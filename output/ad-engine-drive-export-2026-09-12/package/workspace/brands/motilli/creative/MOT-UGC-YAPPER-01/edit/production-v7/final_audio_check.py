from pathlib import Path
import json,subprocess,numpy as np
from scipy.signal import correlate
O=Path(__file__).resolve().parent;v=O/'deliverables/Motilli-Unbranded-VSL-v7.mp4';q=O/'qa/final'
def pcm(p):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-vn','-ac','1','-ar','8000','-f','f32le','-']),np.float32)
a=pcm(O/'narration-locked-resolve.mov');b=pcm(v);result=[]
for t in [0,30,60,90,120,150,180,210,240,270]:
 start=t*8000;n=min(5*8000,len(a)-start);ref=a[start:start+n];lo=max(0,start-800);sample=b[lo:min(len(b),start+n+800)];corr=correlate(sample,ref,mode='valid',method='fft');lag=int(np.argmax(corr));fit=float(corr[lag]/np.sqrt(np.sum(ref**2)*np.sum(sample[lag:lag+n]**2)));result.append({'second':t,'lag':(lo+lag-start)/8000,'correlation':fit})
assert min(r['correlation'] for r in result)>.97;assert max(abs(r['lag']) for r in result)<.04
j={'final_audio_matches_verified_Resolve_voice':True,'window_checks':result,'speech_gap_and_silence_evidence':['final-actual-speech-pacing.json','locked-voice-qa.json'],'note':'A maximum 0.359s low-level span overlaps the final consonant/end of off; preserved to avoid clipping. No long quiet gaps or ending hold.'};(q/'audio-match.json').write_text(json.dumps(j,indent=2));print(json.dumps(j,indent=2),flush=True)
