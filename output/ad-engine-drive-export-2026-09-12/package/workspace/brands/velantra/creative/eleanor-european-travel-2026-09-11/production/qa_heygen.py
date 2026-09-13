from pathlib import Path
import sys,json,subprocess,base64,hashlib
import numpy as np
from scipy.signal import correlate,correlation_lags
import requests
P=Path(__file__).resolve().parent;H=P/'heygen';Q=H/'qa';Q.mkdir(exist_ok=True)
mode=sys.argv[1];native=H/'presenter-native.mp4';final=P/'exports/Eleanor-EuropeanTravel-HeyGen.mp4'
def pcm(path):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-vn','-ac','1','-ar','8000','-f','f32le','-']),dtype=np.float32)
if mode=='audio':
 a=pcm(P/'voice/narration-native-1.1x.mp3');results={}
 for tag,path in [('native',native),('final',final)]:
  if not path.exists():continue
  b=pcm(path);checks=[]
  for t in [0,32,65]:
   x=a[t*8000:(t+10)*8000];y=b[t*8000:(t+10)*8000];n=min(len(x),len(y));x=x[:n];y=y[:n]
   cc=correlate(y,x,mode='full',method='fft');lags=correlation_lags(len(y),len(x));valid=np.abs(lags)<=8000;lag=int(lags[valid][np.argmax(cc[valid])])
   xx=x[max(0,-lag):min(n,n-lag)];yy=y[max(0,lag):min(n,n+lag)]
   checks.append({'start_seconds':t,'lag_seconds':lag/8000,'correlation':float(np.corrcoef(xx,yy)[0,1])})
  results[tag]={'decoded_seconds':len(b)/8000,'checks':checks,'pass':all(abs(c['lag_seconds'])<.05 and c['correlation']>.95 for c in checks)}
 (Q/'audio-correlation.json').write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2))
elif mode in ['native','final']:
 path=native if mode=='native' else final
 proxy=Q/(mode+'-review-proxy.mp4');out=Q/(mode+'-perceptual.json')
 digest=hashlib.sha256(path.read_bytes()).hexdigest()
 if out.exists() and json.loads(out.read_text()).get('source_sha256')==digest:print('Existing review matches bytes');sys.exit()
 subprocess.run(['ffmpeg','-y','-v','error','-i',str(path),'-vf','scale=540:-2','-c:v','libx264','-preset','fast','-crf','27','-c:a','aac','-b:a','128k',str(proxy)],check=True)
 root=next(p for p in P.parents if (p/'.env').exists());env=dict(l.split('=',1) for l in (root/'.env').read_text().splitlines() if '=' in l and not l.startswith('#'));key=env['GEMINI_API_KEY'].strip().strip('"').strip("'")
 prompt='''Review this actual supplied fashion-ad video with its audio from start to finish. Report observations, not assumed compliance. Return JSON: heard_transcript, missing_or_added_words, lip_sync_assessment (with timestamped examples at beginning, middle, end), facial_or_hand_artifacts, audio_clipping_or_dead_air, layout_or_keying_issues, caption_issues, ending_assessment, usable_for_review (boolean), must_fix (timestamped list), review_limits. Sampling is 4fps, not frame exhaustive and not adequate for precise phoneme sync; do not claim otherwise. Intended words:\n'''+(P.parent/'script-v1.txt').read_text()
 if mode=='native':prompt+='\nThis is the original HeyGen green-screen presenter source. Bright green background is intentional, and there should be no captions. Assess naturalness and continuity of this one presenter, especially her lip and hand motion.'
 else:prompt+='\nThis is the finished Resolve composite. A small, continuous lower-left speaking presenter is intentional. Full-background held photos and three short motion inserts alternate. The four designer hook bags intentionally differ from Eleanor. Aligned white outlined phrase captions are intentional. Two-second static final presenter/product CTA hold after speech is intentional. Report visible green edges, cutout problems, obscured bags, offline frames, significant unwanted silence, mismatched captions or obvious sync drift.'
 payload={'contents':[{'role':'user','parts':[{'inlineData':{'mimeType':'video/mp4','data':base64.b64encode(proxy.read_bytes()).decode()},'videoMetadata':{'fps':4}},{'text':prompt}]}],'generationConfig':{'responseMimeType':'application/json'}}
 r=requests.post('https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent',headers={'x-goog-api-key':key},json=payload,timeout=240);r.raise_for_status()
 raw=''.join(x.get('text','') for x in r.json()['candidates'][0]['content']['parts']);d=json.loads(raw)
 if isinstance(d,list):d=d[0]
 d['source_sha256']=digest;d['review_method']='Actual audio/video machine perceptual review at 4fps; not human approval or frame-exhaustive audit';out.write_text(json.dumps(d,indent=2));print(json.dumps(d,indent=2),flush=True)
