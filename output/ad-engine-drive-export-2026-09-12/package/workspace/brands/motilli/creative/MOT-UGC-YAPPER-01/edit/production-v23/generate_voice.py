from pathlib import Path
import json,httpx,base64,sys
O=Path(__file__).resolve().parent;ROOT=O.parents[5]
def key(k):return next(l.split('=',1)[1].strip().strip('"').strip("'") for l in (ROOT/'.env').read_text().splitlines() if l.startswith(k+'='))
def save(n,j):(O/n).write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n')
voice=json.loads((O.parent/'production-v18/selected-voice.json').read_text())['voice_id']
with httpx.Client(timeout=600,headers={'xi-api-key':key('ELEVENLABS_API_KEY')}) as c:
 r=c.get('https://api.elevenlabs.io/v1/voices/'+voice);r.raise_for_status();v=r.json();save('selected-voice.json',v);print('Verified voice:',v['name'],v.get('description'),flush=True)
 for name in sys.argv[1:] or ['H1','H2','H3']:
  dest=O/f'deliverables/Motilli-V23-{name}-Eleven-v3-Natural-1.2x.mp3'
  if dest.exists():print(name,'existing output preserved',flush=True);continue
  text=(O/f'{name}-exact.txt').read_text().strip();assert len(text)<=5000
  payload={'text':text,'model_id':'eleven_v3','voice_settings':{'stability':0.5,'similarity_boost':0.75,'speed':1.2},'seed':911230}
  save(name+'-request.json',{'voice_id':voice,'voice_name':v['name'],'preset':'Natural','request':payload})
  print(name,'generation started',len(text),'characters',flush=True)
  r=c.post('https://api.elevenlabs.io/v1/text-to-speech/'+voice+'/with-timestamps',params={'output_format':'mp3_44100_128'},json=payload)
  if not r.is_success:save(name+'-error.json',{'status':r.status_code,'error':r.text});r.raise_for_status()
  j=r.json();dest.write_bytes(base64.b64decode(j.pop('audio_base64')));save(name+'-alignment.json',j);save(name+'-receipt.json',{'request_id':r.headers.get('request-id'),'character_cost':r.headers.get('character-cost'),'bytes':dest.stat().st_size});print(name,'complete',dest,flush=True)
