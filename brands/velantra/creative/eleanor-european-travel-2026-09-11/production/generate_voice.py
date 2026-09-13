from pathlib import Path
import json,base64,hashlib,datetime,requests
P=Path(__file__).resolve().parent;ROOT=next(x for x in P.parents if (x/'.env').exists());D=P/'voice';D.mkdir(exist_ok=True)
E={}
for line in (ROOT/'.env').read_text().splitlines():
 if '=' in line and not line.lstrip().startswith('#'):
  k,v=line.split('=',1);E[k.strip()]=v.strip().strip('\"').strip("'")
voice='NBIPq5xdnIg9kaBH5Ape';headers={'xi-api-key':E['ELEVENLABS_API_KEY']}
info=requests.get(f'https://api.elevenlabs.io/v1/voices/{voice}',headers=headers,timeout=40);info.raise_for_status();assert info.json()['name']=='Woman Over 40'
(D/'voice-identity.json').write_text(json.dumps({'voice_id':voice,'name':info.json()['name'],'verified_at':datetime.datetime.now(datetime.timezone.utc).isoformat()},indent=2))
if (D/'state.json').exists():raise SystemExit('Existing submission state; inspect before any retry.')
script=(P.parent/'script-v1.txt').read_text().strip();payload={'text':script,'model_id':'eleven_v3','voice_settings':{'stability':0.5,'similarity_boost':0.75,'style':0.0,'use_speaker_boost':True,'speed':1.1}}
(D/'request.json').write_text(json.dumps(payload,indent=2)+'\n');state={'status':'submitted','voice_id':voice,'voice_name':'Woman Over 40','preset':'Natural','speed':1.1,'submitted_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'script_sha256':hashlib.sha256(script.encode()).hexdigest()};(D/'state.json').write_text(json.dumps(state,indent=2));print('Generating approved narration, Natural, speed 1.1',flush=True)
try:
 r=requests.post(f'https://api.elevenlabs.io/v1/text-to-speech/{voice}/with-timestamps',headers=headers,params={'output_format':'mp3_44100_128'},json=payload,timeout=300)
 state.update(http=r.status_code,request_id=r.headers.get('request-id'),history_item_id=r.headers.get('history-item-id'))
 if r.status_code==200:
  data=r.json();raw=base64.b64decode(data.pop('audio_base64'));(D/'narration-native-1.1x.mp3').write_bytes(raw);(D/'alignment.json').write_text(json.dumps(data,indent=2));state.update(status='generated',bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
 else:state.update(status='failed',error=r.text[:1500])
except Exception as e:state.update(status='unknown_check_provider_before_retry',error=str(e))
(D/'state.json').write_text(json.dumps(state,indent=2)+'\n');print(json.dumps(state),flush=True)
