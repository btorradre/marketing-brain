import pathlib,json,httpx,time
ROOT=pathlib.Path('/Users/brooksorradre2/Documents/marketing brain');P=ROOT/'brands/motilli/creative/MOT-UGC-YAPPER-01';O=P/'edit/production-v6';D=P/'assets/video-v6';D.mkdir(exist_ok=True)
key=next(l.split('=',1)[1].strip().strip('"').strip("'") for l in (ROOT/'.env').read_text().splitlines() if l.startswith('HEYGEN_API_KEY='))
def save(name,j):(O/name).write_text(json.dumps(j,indent=2)+'\n')
with httpx.Client(timeout=180,headers={'X-Api-Key':key}) as c:
 look=json.loads((O/'heygen-avatar.json').read_text())['data']['avatar_item']['id']
 for i in range(30):
  d=c.get('https://api.heygen.com/v3/avatars/looks/'+look).json()['data']
  assert 'avatar_v' in d['supported_api_engines'];print('Avatar status',d['status'],flush=True)
  if d['status']=='completed':break
  time.sleep(10)
 else:raise RuntimeError('Avatar is not ready')
 if (O/'heygen-video-job.json').exists():job=json.loads((O/'heygen-video-job.json').read_text())
 else:
  if (O/'heygen-audio-upload.json').exists():up=json.loads((O/'heygen-audio-upload.json').read_text())
  else:
   r=c.post('https://upload.heygen.com/v1/asset',content=(O/'narration.mp3').read_bytes(),headers={'Content-Type':'audio/mpeg'});r.raise_for_status();up=r.json();save('heygen-audio-upload.json',up)
  aid=up['data'].get('id') or up['data'].get('asset_id')
  payload={'type':'avatar','avatar_id':look,'audio_asset_id':aid,'engine':{'type':'avatar_v'},'aspect_ratio':'9:16','resolution':'1080p','title':'Motilli Yapper v6 unbranded continuous presenter','motion_prompt':'A mature American woman speaks candidly to a friend from her parked car. Natural restrained expressions, small head movements and occasional gentle nod. Keep the same identity, clothing, background and fixed framing throughout. Hands relaxed and empty. No products, logos, props, large gestures or camera movements.'}
  payload.pop('motion_prompt',None)
  save('heygen-video-request.json',payload);r=c.post('https://api.heygen.com/v3/videos',json=payload);save('heygen-submit-response.json',{'status':r.status_code,'body':r.json()});r.raise_for_status();job=r.json();save('heygen-video-job.json',job);print('Avatar V submitted',json.dumps(job),flush=True)
 d=job.get('data') or job;vid=d.get('video_id') or d.get('id');assert vid
 for i in range(150):
  r=c.get('https://api.heygen.com/v3/videos/'+vid);r.raise_for_status();j=r.json();save('heygen-video-status.json',j);d=j.get('data') or j;print('Avatar V',d.get('status'),flush=True)
  if d.get('status')=='completed':
   url=d['video_url'];f=D/'presenter-avatar-v.mp4'
   with c.stream('GET',url,timeout=300) as resp:
    resp.raise_for_status()
    with f.open('wb') as out:
     for chunk in resp.iter_bytes():out.write(chunk)
   print('Downloaded',f,flush=True);break
  if d.get('status')=='failed':raise RuntimeError(str(d))
  time.sleep(20)
