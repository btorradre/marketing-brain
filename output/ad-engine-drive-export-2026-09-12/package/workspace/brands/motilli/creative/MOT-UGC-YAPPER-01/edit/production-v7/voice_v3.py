import pathlib,json,httpx,base64,sys
ROOT=pathlib.Path('/Users/brooksorradre2/Documents/marketing brain');P=ROOT/'brands/motilli/creative/MOT-UGC-YAPPER-01';O=P/'edit/production-v7'
def key(k):return next(l.split('=',1)[1].strip().strip('"').strip("'") for l in (ROOT/'.env').read_text().splitlines() if l.startswith(k+'='))
def save(n,j):(O/n).write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n')
beats=json.loads((P/'storyboard/beat-cards.json').read_text());script=' '.join(b['script'] for b in beats);(O/'narration-exact.txt').write_text(script+'\n')
description='A 50-year-old American woman chatting candidly to a close friend from her parked car. Warm mid-low female register with a little lived-in grain and natural vocal fry. Clear neutral American accent. Relaxed, quick conversational delivery with varied inflection and connected phrases. Emotionally present, matter-of-fact about discomfort, gently skeptical, then relieved. Sounds like a real ordinary woman sharing something personal into her phone, with spontaneous human rhythm, not polished narration. Clean dry close microphone.'
with httpx.Client(timeout=600,headers={'xi-api-key':key('ELEVENLABS_API_KEY')}) as c:
 mode=sys.argv[1]
 if mode=='design':
  if (O/'voice-design.json').exists():print('Existing voice designs preserved');sys.exit()
  payload={'model_id':'eleven_ttv_v3','voice_description':description,'text':' '.join(b['script'] for b in beats[:5]),'guidance_scale':3,'seed':9102026}
  save('voice-design-request.json',payload);r=c.post('https://api.elevenlabs.io/v1/text-to-voice/design',json=payload);print('Design',r.status_code,flush=True)
  if r.status_code!=200:print(r.text[:1500]);sys.exit(1)
  j=r.json()
  for i,v in enumerate(j['previews']):(O/f'voice-preview-{i+1}.mp3').write_bytes(base64.b64decode(v.pop('audio_base_64')))
  save('voice-design.json',j);print(json.dumps(j),flush=True)
 elif mode=='create':
  if (O/'selected-voice.json').exists():print('Existing voice preserved');sys.exit()
  j=json.loads((O/'voice-design.json').read_text());v=j['previews'][int(sys.argv[2])-1]
  r=c.post('https://api.elevenlabs.io/v1/text-to-voice',json={'voice_name':'Motilli Yapper woman 50 V3 20260910','voice_description':description,'generated_voice_id':v['generated_voice_id']});print('Create',r.status_code,flush=True)
  if r.status_code!=200:print(r.text[:1500]);sys.exit(1)
  save('selected-voice.json',r.json());print('Saved voice',r.json()['voice_id'])
 elif mode=='generate':
  voice=json.loads((O/'selected-voice.json').read_text())['voice_id']
  for idx,chunk in enumerate([beats[:25],beats[25:]],1):
   n=f'part-{idx}';txt=' '.join(b['script'] for b in chunk);(O/f'{n}-exact.txt').write_text(txt)
   if (O/f'{n}.mp3').exists():print(n,'preserved');continue
   payload={'text':txt,'model_id':'eleven_v3','voice_settings':{'stability':0.0,'similarity_boost':0.75,'speed':1.0},'seed':9102026}
   save(f'{n}-request.json',{'voice_id':voice,'preset':'Creative','request':payload});r=c.post('https://api.elevenlabs.io/v1/text-to-speech/'+voice+'/with-timestamps',params={'output_format':'mp3_44100_128'},json=payload);print(n,r.status_code,flush=True)
   if r.status_code!=200:save(f'{n}-error.json',{'status':r.status_code,'body':r.text});print(r.text[:1500]);sys.exit(1)
   j=r.json();(O/f'{n}.mp3').write_bytes(base64.b64decode(j.pop('audio_base64')));save(f'{n}-alignment.json',j);save(f'{n}-receipt.json',{'request_id':r.headers.get('request-id'),'character_cost':r.headers.get('character-cost')});print(n,'saved',len(txt),'characters',flush=True)
