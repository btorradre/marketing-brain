from pathlib import Path
import json,requests
R=Path(__file__).resolve().parent;P=R.parent;root=next(p for p in R.parents if (p/'.env').exists())
env={}
for line in (root/'.env').read_text().splitlines():
 if '=' in line and not line.startswith('#'):
  k,v=line.split('=',1);env[k.strip()]=v.strip().strip('"').strip("'")
for h in ['H1','H2','H3']:
 out=R/'qa'/f'{h}-render-forced-alignment.json'
 if out.exists():continue
 text=json.loads((P/'voice'/h/'request.json').read_text())['text']
 import subprocess
 audio=R/'qa'/f'{h}-render-audio.m4a'
 subprocess.run(['ffmpeg','-v','error','-i',str(R/'exports'/f'VEL-OM-{h}-A1-R4.mp4'),'-vn','-c:a','copy','-y',str(audio)],check=True)
 with audio.open('rb') as f:
  response=requests.post('https://api.elevenlabs.io/v1/forced-alignment',headers={'xi-api-key':env['ELEVENLABS_API_KEY']},data={'text':text},files={'file':('narration.m4a',f,'audio/mp4')},timeout=180)
 response.raise_for_status();out.write_text(json.dumps(response.json(),indent=2));print(h,response.status_code,len(response.json().get('words',[])),flush=True)
