from pathlib import Path
import json,requests,base64
from dotenv import dotenv_values
v=Path(__file__).resolve().parent;b=v.parents[1];root=b.parents[3]
d=json.loads((v/'clone-receipt.json').read_text())['response'];assert not d.get('requires_verification')
text=(b/'storyboard/narration.txt').read_text().strip()
payload={'text':text,'model_id':'eleven_v3','voice_settings':{'stability':0.0,'similarity_boost':0.85,'use_speaker_boost':True}}
(v/'tts-request-v2.json').write_text(json.dumps(payload,indent=2)+'\n')
assert not (v/'narration-v2-creative.mp3').exists()
h={'xi-api-key':dotenv_values(root/'.env')['ELEVENLABS_API_KEY']}
r=requests.post('https://api.elevenlabs.io/v1/text-to-speech/'+d['voice_id']+'/with-timestamps',params={'output_format':'mp3_44100_128'},headers=h,json=payload,timeout=240)
if not r.ok: print(r.status_code,r.text[:500]);raise SystemExit(1)
z=r.json();(v/'narration-v2-creative.mp3').write_bytes(base64.b64decode(z.pop('audio_base64')));(v/'alignment-v2.json').write_text(json.dumps(z,indent=2)+'\n');print({'status':r.status_code,'bytes':(v/'narration-v2-creative.mp3').stat().st_size,'voice_id':d['voice_id']})
