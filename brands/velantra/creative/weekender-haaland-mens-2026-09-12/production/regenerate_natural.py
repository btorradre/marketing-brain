from pathlib import Path
import json,requests,base64,subprocess,hashlib
from dotenv import dotenv_values
P=Path(__file__).resolve().parent;B=P.parent;root=P.parents[4];V=P/'voice-natural';V.mkdir(exist_ok=True);statep=V/'state.json';state=json.loads(statep.read_text()) if statep.exists() else {}
def save():statep.write_text(json.dumps(state,indent=2)+'\n')
ref=B/'edit/reference-analysis/DbdW5anAxg5/DbdW5anAxg5.mp4';source=V/'reference-source.wav'
if not source.exists():subprocess.run(['ffmpeg','-v','error','-i',str(ref),'-vn','-ac','1','-ar','44100','-c:a','pcm_s16le',str(source)],check=True)
h={'xi-api-key':dotenv_values(root/'.env')['ELEVENLABS_API_KEY']}
if 'voice_id' not in state:
 assert not state.get('clone_submission_started'),'Clone submission recorded without receipt; inspect provider before resubmitting'
 state.update(clone_submission_started=True,reference=str(ref),reference_sha256=hashlib.sha256(ref.read_bytes()).hexdigest(),permission='User yes to explicit permission/lawful-use question, September12; user requests fresh clone and Natural regeneration');save()
 with source.open('rb') as f:r=requests.post('https://api.elevenlabs.io/v1/voices/add',headers=h,data={'name':'Weekender Reference — Fresh Natural — Sep12','remove_background_noise':'true','description':'Permitted source speaker from selected Alec Grawe reference; user-requested fresh clone for Eleven v3 Natural.'},files={'files':('reference-source.wav',f,'audio/wav')},timeout=180)
 r.raise_for_status();d=r.json();(V/'clone-receipt.json').write_text(json.dumps({'http_status':r.status_code,'response':d,'source':str(source),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest()},indent=2));state.update(d);save();assert not d.get('requires_verification'),d
if not (V/'narration-natural.mp3').exists():
 assert not state.get('tts_submission_started'),'TTS request already submitted; inspect before retry'
 payload={'text':(B/'storyboard/narration.txt').read_text().strip(),'model_id':'eleven_v3','voice_settings':{'stability':0.5,'similarity_boost':0.85,'use_speaker_boost':True}}
 (V/'tts-request.json').write_text(json.dumps(payload,indent=2));state.update(tts_submission_started=True,preset='Natural',model_id='eleven_v3',stability=.5);save()
 r=requests.post('https://api.elevenlabs.io/v1/text-to-speech/'+state['voice_id']+'/with-timestamps',headers=h,params={'output_format':'mp3_44100_128'},json=payload,timeout=240);r.raise_for_status();d=r.json();(V/'narration-natural.mp3').write_bytes(base64.b64decode(d.pop('audio_base64')));(V/'alignment.json').write_text(json.dumps(d,indent=2));state.update(status='generated',output=str(V/'narration-natural.mp3'),output_sha256=hashlib.sha256((V/'narration-natural.mp3').read_bytes()).hexdigest());save()
print({k:state.get(k) for k in ['voice_id','status','model_id','preset','stability','output']})
