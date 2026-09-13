import json,requests,subprocess
from pathlib import Path
p=Path(__file__).resolve().parent;root=p.parents[4];out=p/'scribe.json';audio=p/'reel-audio.m4a'
subprocess.run(['ffmpeg','-v','error','-y','-i',str(p/'reel.mp4'),'-vn','-c:a','copy',str(audio)],check=True)
if not out.exists():
 key=next(l.split('=',1)[1].strip().strip('"').strip("'") for l in (root/'.env').read_text().splitlines() if l.startswith('ELEVENLABS_API_KEY='))
 with audio.open('rb') as f:r=requests.post('https://api.elevenlabs.io/v1/speech-to-text',headers={'xi-api-key':key},data={'model_id':'scribe_v2','timestamps_granularity':'word','tag_audio_events':'false','diarize':'true'},files={'file':(audio.name,f,'audio/mp4')},timeout=180)
 if r.status_code!=200:raise RuntimeError('Transcription HTTP '+str(r.status_code))
 out.write_text(json.dumps(r.json(),indent=2))
j=json.loads(out.read_text());(p/'transcript.txt').write_text(j['text']);print(j['text'])
i=json.loads((p/'reel.info.json').read_text());print(json.dumps({k:i.get(k) for k in ['title','description','uploader','duration','webpage_url']},ensure_ascii=False))
