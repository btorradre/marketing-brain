from pathlib import Path
import httpx,json,base64
ROOT=Path('/Users/brooksorradre2/Documents/marketing brain');P=ROOT/'brands/motilli/creative/MOT-UGC-YAPPER-01';O=Path(__file__).resolve().parent
key=next(l.split('=',1)[1].strip().strip('"').strip("'") for l in (ROOT/'.env').read_text().splitlines() if l.startswith('ELEVENLABS_API_KEY='))
voice='xg7RXypgOlRSIidsSV4l';beats=json.loads((P/'storyboard/beat-cards.json').read_text());txt=' '.join(b['script'] for b in beats[:5])
with httpx.Client(timeout=300,headers={'xi-api-key':key}) as c:
 r=c.get('https://api.elevenlabs.io/v1/voices/'+voice);r.raise_for_status();(O/'selected-voice.json').write_text(json.dumps(r.json(),indent=2));print('Selected',r.json()['name'],r.json().get('description'),flush=True)
 payload={'text':'[conversational] '+txt,'model_id':'eleven_v3','voice_settings':{'stability':0.0,'similarity_boost':0.75,'speed':1.0},'seed':910181}
 (O/'auditions/michelle-request.json').write_text(json.dumps({'voice_id':voice,'preset':'Creative','request':payload},indent=2));r=c.post('https://api.elevenlabs.io/v1/text-to-speech/'+voice+'/with-timestamps',params={'output_format':'mp3_44100_128'},json=payload);r.raise_for_status();j=r.json();(O/'auditions/michelle.mp3').write_bytes(base64.b64decode(j.pop('audio_base64')));(O/'auditions/michelle-alignment.json').write_text(json.dumps(j));print('Audition generated',flush=True)
