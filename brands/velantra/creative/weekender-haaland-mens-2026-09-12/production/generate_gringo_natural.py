from pathlib import Path
import json,requests,base64,hashlib
from dotenv import dotenv_values
P=Path(__file__).resolve().parent;B=P.parent;root=P.parents[4];V=P/'voice-gringo-natural';V.mkdir(exist_ok=True)
statep=V/'state.json';state=json.loads(statep.read_text()) if statep.exists() else {'voice_id':'hnRXaWYxr5tqZBrH55Cp','name':'gringo-tiktok-male','selection':'Explicit user screenshot; existing saved voice; no new clone'}
def save():statep.write_text(json.dumps(state,indent=2)+'\n')
h={'xi-api-key':dotenv_values(root/'.env')['ELEVENLABS_API_KEY']}
r=requests.get('https://api.elevenlabs.io/v1/voices/'+state['voice_id'],headers=h,timeout=30);r.raise_for_status();voice=r.json();assert voice['name']=='gringo-tiktok-male';(V/'catalog-receipt.json').write_text(json.dumps({k:voice.get(k) for k in ['voice_id','name','category','description','settings']},indent=2))
if not (V/'narration-natural.mp3').exists():
 assert not state.get('tts_submission_started'),'TTS request already submitted; inspect before retry'
 payload={'text':(B/'storyboard/narration.txt').read_text().strip().replace('Velantra','Vell-Ahn-Trah').replace('does it like','DOES IT like'),'model_id':'eleven_v3','voice_settings':{'stability':0.5,'similarity_boost':0.85,'use_speaker_boost':True}}
 (V/'tts-request.json').write_text(json.dumps(payload,indent=2));state.update(tts_submission_started=True,preset='Natural',model_id='eleven_v3',stability=.5);save()
 r=requests.post('https://api.elevenlabs.io/v1/text-to-speech/'+state['voice_id']+'/with-timestamps',headers=h,params={'output_format':'mp3_44100_128'},json=payload,timeout=240);r.raise_for_status();d=r.json();(V/'narration-natural.mp3').write_bytes(base64.b64decode(d.pop('audio_base64')));(V/'alignment.json').write_text(json.dumps(d,indent=2));state.update(status='generated',output=str(V/'narration-natural.mp3'),output_sha256=hashlib.sha256((V/'narration-natural.mp3').read_bytes()).hexdigest());save()
print({k:state.get(k) for k in ['voice_id','status','model_id','preset','stability','output']})
