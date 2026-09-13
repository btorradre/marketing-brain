from pathlib import Path
import json,httpx,base64,concurrent.futures,sys,subprocess,re,difflib
import numpy as np
O=Path(__file__).resolve().parent;ROOT=O.parents[5]
def key(k):return next(l.split('=',1)[1].strip().strip('"').strip("'") for l in (ROOT/'.env').read_text().splitlines() if l.startswith(k+'='))
def norm(t):
 t=t.lower().replace('glp-1s','glp ones').replace('glp 1s','glp ones').replace('glp-1','glp one').replace('glp 1','glp one').replace('10am','ten am').replace('10 a.m.','ten am').replace('10 a.m','ten am').replace('2019','twenty nineteen').replace('miralax','mira lax').replace('motilli','motilly')
 for a,b in [('thirty','30'),('ninety','90'),('two','2'),('six','6'),('three','3')]:t=re.sub(r'\b'+a+r'\b',b,t)
 return re.findall(r'[a-z0-9]+',t)
def check(name):
 f=O/f'deliverables/Motilli-V23-{name}-Eleven-v3-Natural-1.2x.mp3';expected=(O/f'{name}-exact.txt').read_text().strip()
 meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(f)]));(O/f'qa/{name}-metadata.json').write_text(json.dumps(meta,indent=2));pcm=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(f),'-ac','1','-ar','16000','-f','f32le','-']),np.float32)
 dst=O/f'qa/{name}-scribe.json'
 if not dst.exists():
  with f.open('rb') as h:r=httpx.post('https://api.elevenlabs.io/v1/speech-to-text',headers={'xi-api-key':key('ELEVENLABS_API_KEY')},data={'model_id':'scribe_v2','language_code':'eng','tag_audio_events':'false','timestamps_granularity':'word'},files={'file':(f.name,h,'audio/mpeg')},timeout=240)
  r.raise_for_status();dst.write_text(json.dumps(r.json(),indent=2))
 s=json.loads(dst.read_text());e=norm(expected);a=norm(s['text']);diff=[{'op':tag,'expected':e[i:j],'heard':a[k:l]} for tag,i,j,k,l in difflib.SequenceMatcher(None,e,a,autojunk=False).get_opcodes() if tag!='equal'];words=[w for w in s['words'] if w['type']=='word'];gaps=[{'after':w['text'],'before':n['text'],'start':w['end'],'end':n['start'],'duration':n['start']-w['end']} for w,n in zip(words,words[1:]) if n['start']-w['end']>.8]
 report={'duration_seconds':float(meta['format']['duration']),'peak_dbfs':float(20*np.log10(max(abs(pcm))+1e-9)),'samples_above_0999':int(np.sum(abs(pcm)>=.999)),'asr_differences':diff,'gaps_over_08s':gaps,'start_padding_seconds':words[0]['start'],'end_padding_seconds':float(meta['format']['duration'])-words[-1]['end']};(O/f'qa/{name}-technical.json').write_text(json.dumps(report,indent=2));print(name,'TECH',json.dumps(report),flush=True)
 return name
def listen(name):
 out=O/f'qa/{name}-listening.json'
 if out.exists():return
 f=O/f'deliverables/Motilli-V23-{name}-Eleven-v3-Natural-1.2x.mp3'
 prompt='Listen critically to this complete generated narration. Intended voice: mature American woman over 40, conversational and natural, brisk 1.2x pace. Evaluate rhythmic robotic/sing-song/announcer delivery, unnatural elongations, pitch artifacts, clipping, abrupt speaker changes, long dead gaps, omitted or added words, and pronunciation of GLP-1, MiraLAX, apigenin, chlorophyllin and Motilli. This is a voice-only QA, not a fact check. Give concise JSON usable, naturalness_score_1_to_10, apparent_age, tone, issues_with_timestamps, pronunciation_observations, missing_or_added_words. Do not assume approval. Exact reference: '+(O/f'{name}-exact.txt').read_text()
 r=httpx.post('https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent',headers={'x-goog-api-key':key('GEMINI_API_KEY')},json={'contents':[{'parts':[{'inline_data':{'mime_type':'audio/mpeg','data':base64.b64encode(f.read_bytes()).decode()}},{'text':prompt}]}],'generationConfig':{'temperature':.1,'responseMimeType':'application/json'}},timeout=240);r.raise_for_status();j=r.json();z=''.join(t.get('text','') for a in j['candidates'] for t in a['content']['parts']);out.write_text(z);print(name,'LISTEN',z,flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
 fs=[ex.submit(fn,n) for n in (sys.argv[1:] or ['H1','H2','H3']) for fn in [check,listen]]
 for f in concurrent.futures.as_completed(fs):f.result()
