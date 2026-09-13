from pathlib import Path
import json,sys,subprocess,base64,hashlib,re
import numpy as np
from scipy.signal import correlate,correlation_lags
import requests
P=Path(__file__).resolve().parent;R=P/'tight';Q=R/'qa';movie=P/'exports/Eleanor-EuropeanTravel-Tight.mp4';m=json.loads((R/'cut-map.json').read_text())
def pcm(path):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-vn','-ac','1','-ar','48000','-f','f32le','-']),dtype=np.float32)
if sys.argv[1]=='audio':
 source=pcm(P/'heygen/narration-resolve.wav');actual=pcm(movie);checks=[]
 for seg in m['segments']:
  a=seg['source_start'];b=min(seg['source_end'],2378);n=b-a
  if n<10:continue
  # Ignore 2 frames at each join when measuring signal identity, not overall timing.
  x=source[round((a+2)/30*48000):round((b-2)/30*48000)];y=actual[round((seg['start']+2)/30*48000):round((seg['start']+n-2)/30*48000)];nn=min(len(x),len(y));x=x[:nn];y=y[:nn]
  cc=correlate(y,x,mode='full',method='fft');lags=correlation_lags(len(y),len(x));valid=np.abs(lags)<=2400;lag=int(lags[valid][np.argmax(cc[valid])]);xx=x[max(0,-lag):min(nn,nn-lag)];yy=y[max(0,lag):min(nn,nn+lag)]
  checks.append({'source_start_seconds':a/30,'edited_start_seconds':seg['start']/30,'lag_seconds':lag/48000,'correlation':float(np.corrcoef(xx,yy)[0,1])})
 scan=subprocess.run(['ffmpeg','-hide_banner','-i',str(movie),'-af','silencedetect=noise=-40dB:d=0.20','-f','null','-'],capture_output=True,text=True,check=True);(Q/'residual-silence.log').write_text(scan.stderr)
 residual=[];a=None
 for line in scan.stderr.splitlines():
  v=re.search(r'silence_start: ([\d.]+)',line)
  if v:a=float(v[1])
  v=re.search(r'silence_end: ([\d.]+)',line)
  if v and a is not None:residual.append({'start':a,'end':float(v[1])});a=None
 internal=[s for s in residual if s['end']<m['frames']/30-.3]
 result={'segments_checked':len(checks),'checks':checks,'audio_identity_and_timing_pass':all(abs(c['lag_seconds'])<=1/48000 and c['correlation']>.98 for c in checks),'residual_internal_silences_over_0_2s':internal,'residual_silences':residual}
 (Q/'audio-verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
else:
 proxy=Q/'review-proxy.mp4';subprocess.run(['ffmpeg','-y','-v','error','-i',str(movie),'-vf','scale=540:960','-c:v','libx264','-preset','fast','-crf','27','-c:a','aac','-b:a','128k',str(proxy)],check=True)
 root=next(p for p in P.parents if (p/'.env').exists());env=dict(l.split('=',1) for l in (root/'.env').read_text().splitlines() if '=' in l and not l.startswith('#'));key=env['GEMINI_API_KEY'].strip().strip('"').strip("'")
 prompt='''Review this actual video and its audio from start to finish. User specifically requested removal of dead spaces and a slightly larger talking presenter fully in the lower-left corner. Quiet gaps were cut synchronously from voice and presenter; natural jump cuts in the small presenter are intentional. Speech speed and wording must stay unchanged. Check for clipped consonants, omitted words, clicks, unexplained silence, rushed or broken joins, major lip-sync drift, caption collisions, and bag obstruction. The CTA graphic appears during the last spoken invitation; its captions sit above it. End hold is only0.2s. Return JSON: heard_transcript, missing_or_added_words, audible_join_problems (exact seconds and heard words), remaining_dead_spaces (exact intervals), pacing_assessment, lip_sync_assessment, corner_placement, caption_or_layout_problems (exact timestamp and location), must_fix, usable_for_review, review_limits. Cite specific visible evidence for any key-edge defect rather than assuming a chroma key must be faulty. No claim of perfect or frame-exhaustive inspection: sample4fps. Intended exact words:\n'''+(P.parent/'script-v1.txt').read_text()
 payload={'contents':[{'role':'user','parts':[{'inlineData':{'mimeType':'video/mp4','data':base64.b64encode(proxy.read_bytes()).decode()},'videoMetadata':{'fps':4}},{'text':prompt}]}],'generationConfig':{'responseMimeType':'application/json'}}
 response=requests.post('https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent',headers={'x-goog-api-key':key},json=payload,timeout=240);response.raise_for_status();d=json.loads(''.join(x.get('text','') for x in response.json()['candidates'][0]['content']['parts']))
 if isinstance(d,list):d=d[0]
 d['source_sha256']=hashlib.sha256(movie.read_bytes()).hexdigest();d['review_method']='Machine actual-video/audio review at4fps; not human approval';(Q/'perceptual-review.json').write_text(json.dumps(d,indent=2));print(json.dumps(d,indent=2),flush=True)
