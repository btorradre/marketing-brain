import json,re,subprocess,concurrent.futures,difflib
from pathlib import Path
import requests,numpy as np
p=Path(__file__).resolve().parent;P=p.parent.parent;root=P.parents[3];src=p/'exports/MOT-VID-013-R2-A.mp4';audio=p/'export-A-audio.m4a';timing=json.loads((p/'timing.json').read_text());script=(P/'narration-script.txt').read_text().strip()
subprocess.run(['ffmpeg','-v','error','-y','-i',str(src),'-vn','-c:a','copy',str(audio)],check=True)
key=next(l.split('=',1)[1].strip().strip('"').strip("'") for l in (root/'.env').read_text().splitlines() if l.startswith('ELEVENLABS_API_KEY='))
def call(kind):
 out=p/('export-A-'+kind+'.json')
 if out.exists():return json.loads(out.read_text())
 data={'text':script} if kind=='forced-alignment' else {'model_id':'scribe_v2','timestamps_granularity':'word','tag_audio_events':'false','language_code':'eng'}
 with audio.open('rb') as f:r=requests.post('https://api.elevenlabs.io/v1/'+('forced-alignment' if kind=='forced-alignment' else 'speech-to-text'),headers={'xi-api-key':key},data=data,files={'file':(audio.name,f,'audio/mp4')},timeout=180)
 if r.status_code!=200:raise RuntimeError('Export ASR HTTP '+str(r.status_code))
 j=r.json();out.write_text(json.dumps(j,indent=2,ensure_ascii=False));print(kind,'complete',flush=True);return j
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:aligned,asr=list(ex.map(call,['forced-alignment','scribe']))
def norm(s):
 s=s.lower().replace('90','ninety');s=re.sub(r'\bmotili\b','motilli',s);return ''.join(c for c in s if c.isalnum())
original=timing['words'];spoken=[w for w in asr['words'] if w.get('type')=='word'];a=''.join(norm(w['text']) for w in original);b=''.join(norm(w['text']) for w in spoken)
if a!=b:print('TRANSCRIPT DIFFERENCE',list(difflib.ndiff([a],[b])),flush=True)
assert a==b,'Actual export transcript differs from exact script (after punctuation and Motilli/90 spelling normalization)'
spans=[];n=0
for w in spoken:spans.append((n,n+len(norm(w['text'])),w));n=spans[-1][1]
mapped=[];n=0
for w in original:
 end=n+len(norm(w['text']));hits=[q for a,b,q in spans if a<end and b>n];mapped.append({'text':w['text'],'expected_start':w['start'],'actual_start':hits[0]['start'],'actual_end':hits[-1]['end'],'error':hits[0]['start']-w['start']});n=end
errs=[abs(w['error']) for w in mapped];caps=[]
for c in timing['captions']:
 w=mapped[c['word_start']];caps.append({'text':c['text'],'caption_start':c['start'],'spoken_start':w['actual_start'],'error':c['start']-w['actual_start']})
shots=[]
for s in timing['shots']:
 w=mapped[s['word_start']];shots.append({'shot':s['id'],'line':s['script'],'cut':s['start_frame']/30,'actual_line_start':w['actual_start'],'error':s['start_frame']/30-w['actual_start']})
report={'exact_script_verified':True,'word_count':len(mapped),'mean_word_start_error':float(np.mean(errs)),'p95_word_start_error':float(np.percentile(errs,95)),'max_word_start_error':max(errs),'outliers_over_120ms':[w for w in mapped if abs(w['error'])>.12],'captions':caps,'shots':shots,'words':mapped}
(p/'export-sync-review.json').write_text(json.dumps(report,indent=2,ensure_ascii=False));print(json.dumps({k:v for k,v in report.items() if k not in ['captions','shots','words']}),flush=True)
