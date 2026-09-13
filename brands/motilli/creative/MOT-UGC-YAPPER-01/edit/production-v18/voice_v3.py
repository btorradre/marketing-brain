from pathlib import Path
import json,httpx,base64,sys
ROOT=Path('/Users/brooksorradre2/Documents/marketing brain');P=ROOT/'brands/motilli/creative/MOT-UGC-YAPPER-01';O=Path(__file__).resolve().parent
def key(k):return next(l.split('=',1)[1].strip().strip('"').strip("'") for l in (ROOT/'.env').read_text().splitlines() if l.startswith(k+'='))
def save(n,j):(O/n).write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n')
if __name__=='__main__':
 beats=json.loads((P/'storyboard/beat-cards.json').read_text());script=' '.join(b['script'] for b in beats);assert script==(O/'narration-exact.txt').read_text().strip();voice=json.loads((O/'selected-voice.json').read_text())['voice_id']
 with httpx.Client(timeout=600,headers={'xi-api-key':key('ELEVENLABS_API_KEY')}) as c:
  for idx,chunk in enumerate([beats[:25],beats[25:]],1):
   n=f'part-{idx}';txt=' '.join(b['script'] for b in chunk);(O/f'{n}-exact.txt').write_text(txt)
   if (O/f'{n}.mp3').exists():print(n,'preserved',flush=True);continue
   text='[conversational] '+txt;assert len(text)<=5000
   payload={'text':text,'model_id':'eleven_v3','voice_settings':{'stability':0.0,'similarity_boost':0.75,'speed':1.0},'seed':910181}
   save(n+'-request.json',{'voice_id':voice,'voice_name':'Michelle - Full and Reassuring','voice_profile_age':50,'preset':'Creative','request':payload});r=c.post('https://api.elevenlabs.io/v1/text-to-speech/'+voice+'/with-timestamps',params={'output_format':'mp3_44100_128'},json=payload);r.raise_for_status();j=r.json();(O/f'{n}.mp3').write_bytes(base64.b64decode(j.pop('audio_base64')));save(n+'-alignment.json',j);save(n+'-receipt.json',{'request_id':r.headers.get('request-id'),'character_cost':r.headers.get('character-cost')});print(n,'generated',len(txt),'characters',flush=True)
