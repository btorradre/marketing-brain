import json,base64,subprocess
from pathlib import Path
import requests
p=Path(__file__).resolve().parent;root=p.parents[5];src=root/'_engine/mcp/ad-engine/data/downloads/job_d78559811694/source.mp4'
out=p/'audio-observations.json'
if out.exists():print('Cached audio analysis');raise SystemExit
key=next(l.split('=',1)[1].strip().strip('"').strip("'") for l in (root/'.env').read_text().splitlines() if l.startswith('GEMINI_API_KEY='))
audio=p/'reference-analysis-audio.m4a';subprocess.run(['ffmpeg','-v','error','-y','-i',str(src),'-vn','-c:a','copy',str(audio)],check=True)
prompt='Listen to the full attached 66-second ad audio. Analyze its editing sound design and narration delivery for an editor, without trying to identify the speaker or assert AI provenance. Return JSON with voice_description (perceived voice qualities, accent, pitch, texture, emotional changes, delivery pace), music (is it audible, instruments or texture, changes with timestamps, confidence; do not invent a bed if absent), sound_effects (timestamps and concrete audible observations, separate from consonants), pauses_and_emphasis (timestamp ranges and short phrases), voice_continuity, ending (last words time and tail), and practical_narration_direction. Be precise and honest about quiet/uncertain sounds. This is analysis only; no voice cloning.'
r=requests.post('https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent',headers={'x-goog-api-key':key},json={'contents':[{'role':'user','parts':[{'text':prompt},{'inlineData':{'mimeType':'audio/mp4','data':base64.b64encode(audio.read_bytes()).decode()}}]}],'generationConfig':{'responseMimeType':'application/json'}},timeout=180)
if r.status_code!=200:raise RuntimeError('Audio review HTTP '+str(r.status_code))
d=r.json();s=''.join(x.get('text','') for x in d['candidates'][0]['content']['parts']);j=json.loads(s);j['model']='gemini-3.8-flash';out.write_text(json.dumps(j,indent=2));print(json.dumps(j),flush=True)
