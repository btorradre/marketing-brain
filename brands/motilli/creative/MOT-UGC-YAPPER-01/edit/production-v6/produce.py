import pathlib,json,sys,base64,httpx,time
ROOT=pathlib.Path('/Users/brooksorradre2/Documents/marketing brain'); P=ROOT/'brands/motilli/creative/MOT-UGC-YAPPER-01'; O=P/'edit/production-v6'
def key(k):
 for line in (ROOT/'.env').read_text().splitlines():
  if '=' in line and not line.strip().startswith('#'):
   a,b=line.split('=',1)
   if a.strip()==k:return b.strip().strip('"').strip("'")
 raise ValueError('Missing '+k)
def save(n,j): (O/n).write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n')
mode=sys.argv[1]
if mode=='voice':
 beats=json.loads((P/'storyboard/beat-cards.json').read_text());script='\n\n'.join(b['script'] for b in beats)
 (O/'narration-exact.txt').write_text(script+'\n'); voice='xg7RXypgOlRSIidsSV4l'
 payload={'text':script,'model_id':'eleven_multilingual_v2','voice_settings':{'stability':0.45,'similarity_boost':0.75,'style':0.20,'use_speaker_boost':True,'speed':1.12}}
 save('eleven-request.json',{'voice_id':voice,'voice_name':'Michelle - Full and Reassuring','description':'Native USA female age 50','request':payload})
 if (O/'narration.mp3').exists(): print('Existing voice preserved');sys.exit()
 with httpx.Client(timeout=600) as c:
  r=c.post('https://api.elevenlabs.io/v1/text-to-speech/'+voice+'/with-timestamps',headers={'xi-api-key':key('ELEVENLABS_API_KEY')},params={'output_format':'mp3_44100_128'},json=payload)
  print('ElevenLabs generation HTTP',r.status_code,flush=True)
  if r.status_code!=200:save('eleven-error.json',{'status':r.status_code,'body':r.text});sys.exit(1)
  data=r.json();audio=base64.b64decode(data.pop('audio_base64'));(O/'narration.mp3').write_bytes(audio);save('eleven-alignment.json',data);save('eleven-receipt.json',{'request_id':r.headers.get('request-id'),'character_cost':r.headers.get('character-cost'),'audio_bytes':len(audio)});print('Saved continuous voice + alignment',len(audio),flush=True)
elif mode=='avatar':
 if (O/'heygen-avatar.json').exists(): print('Existing avatar preserved');sys.exit()
 with httpx.Client(timeout=180,headers={'X-Api-Key':key('HEYGEN_API_KEY')}) as c:
  image=P/'assets/images-v1/P01-presenter-base.png'
  with image.open('rb') as f:r=c.post('https://api.heygen.com/v3/assets',files={'file':(image.name,f,'image/png')})
  r.raise_for_status();upload=r.json();save('heygen-image-upload.json',upload);d=upload['data'];aid=d.get('id') or d.get('asset_id');assert aid
  r=c.post('https://api.heygen.com/v3/avatars',json={'type':'photo','name':'Motilli Yapper v6 woman 50+ 20260909','file':{'type':'asset_id','asset_id':aid}});r.raise_for_status();avatar=r.json();save('heygen-avatar.json',avatar);print('AVATAR',json.dumps(avatar)[:5000],flush=True)
  d=avatar['data'];item=d.get('avatar_item') or d;look=item['id'];r=c.get('https://api.heygen.com/v3/avatars/looks/'+look);save('heygen-avatar-eligibility.json',r.json());print('ELIGIBILITY',r.status_code,r.text[:4500],flush=True)
