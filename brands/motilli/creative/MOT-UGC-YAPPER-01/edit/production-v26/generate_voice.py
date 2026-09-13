from pathlib import Path
import json,httpx,base64,sys,concurrent.futures
O=Path(__file__).resolve().parent;ROOT=O.parents[5]
key=next(l.split('=',1)[1].strip().strip('"').strip("'") for l in (ROOT/'.env').read_text().splitlines() if l.startswith('ELEVENLABS_API_KEY='));voice='NBIPq5xdnIg9kaBH5Ape'
def save(n,j):(O/n).write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n')
r=httpx.get('https://api.elevenlabs.io/v1/voices/'+voice,headers={'xi-api-key':key},timeout=30);r.raise_for_status();v=r.json();assert v['name']=='Woman Over 40';save('selected-voice.json',v)
def work(name):
 dest=O/f'sources/{name}-default-speed.mp3'
 if dest.exists():print(name,'existing output preserved',flush=True);return
 text=(O/f'{name}-exact.txt').read_text().strip();payload={'text':text,'model_id':'eleven_v3','voice_settings':{'stability':0.5,'similarity_boost':0.75},'seed':911260};assert 'speed' not in payload['voice_settings'];save(name+'-request.json',{'voice_id':voice,'voice_name':v['name'],'preset':'Natural','generation_speed':'default; speed field omitted','request':payload})
 print(name,'generating at default speed',len(text),'characters',flush=True)
 r=httpx.post('https://api.elevenlabs.io/v1/text-to-speech/'+voice+'/with-timestamps',headers={'xi-api-key':key},params={'output_format':'mp3_44100_128'},json=payload,timeout=600)
 if not r.is_success:save(name+'-error.json',{'status':r.status_code,'error':r.text});r.raise_for_status()
 j=r.json();dest.write_bytes(base64.b64decode(j.pop('audio_base64')));save(name+'-alignment.json',j);save(name+'-receipt.json',{'request_id':r.headers.get('request-id'),'character_cost':r.headers.get('character-cost'),'bytes':dest.stat().st_size});print(name,'complete',flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:list(ex.map(work,sys.argv[1:] or ['H1','H2','H3','B1','B2','B3','B4']))
