from pathlib import Path
import json,httpx,time,sys,hashlib
O=Path(__file__).resolve().parent;ROOT=O.parents[5];key=next(l.split('=',1)[1].strip().strip('"').strip("'") for l in (ROOT/'.env').read_text().splitlines() if l.startswith('HEYGEN_API_KEY='));look='3c421c1dc94c35b2f46a50496bbd781c';h=sys.argv[1];S=O/h
with httpx.Client(timeout=180,headers={'X-Api-Key':key}) as c:
 def save(n,j):(S/n).write_text(json.dumps(j,indent=2)+'\n')
 r=c.get('https://api.heygen.com/v3/avatars/looks/'+look);r.raise_for_status();d=r.json();save('avatar-verified.json',d);assert d['data']['status']=='completed' and 'avatar_v' in d['data']['supported_api_engines']
 assert json.loads((O/f'qa/{h}-final-technical.json').read_text())['pass'];assert (O/f'qa/{h}-final-scribe.json').exists()
 audio=O/f'deliverables/Motilli-V27-{h}-Woman-Over-40-Natural-Resolve-1.1x.mp3';dest=S/'presenter-avatar-v-original.mp4';jf=S/'heygen-video-job.json'
 if jf.exists():job=json.loads(jf.read_text())
 else:
  uf=S/'heygen-audio-upload.json'
  if uf.exists():up=json.loads(uf.read_text())
  else:
   r=c.post('https://upload.heygen.com/v1/asset',content=audio.read_bytes(),headers={'Content-Type':'audio/mpeg'});r.raise_for_status();up=r.json();save('heygen-audio-upload.json',up);save('uploaded-audio-provenance.json',{'path':str(audio),'sha256':hashlib.sha256(audio.read_bytes()).hexdigest(),'cleaned_before_upload':True,'speed_applied_in':'DaVinci Resolve','native_speed_percent':110})
  aid=up['data'].get('id') or up['data'].get('asset_id');assert aid
  payload={'type':'avatar','avatar_id':look,'audio_asset_id':aid,'engine':{'type':'avatar_v'},'aspect_ratio':'9:16','resolution':'1080p','title':f'Motilli V27 {h} Woman Over 40 Natural Resolve 1.1x'};save('heygen-video-request.json',payload)
  r=c.post('https://api.heygen.com/v3/videos',json=payload);save('heygen-submit-response.json',{'status':r.status_code,'body':r.json()});r.raise_for_status();job=r.json();save('heygen-video-job.json',job);print(h,'submitted',flush=True)
 d=job.get('data') or job;vid=d.get('video_id') or d.get('id');assert vid
 for i in range(180):
  r=c.get('https://api.heygen.com/v3/videos/'+vid);r.raise_for_status();j=r.json();save('heygen-video-status.json',j);d=j.get('data') or j;status=d.get('status');print(h,status,flush=True)
  if status=='completed':
   if not dest.exists():
    with httpx.stream('GET',d['video_url'],timeout=300,follow_redirects=True) as resp:
     resp.raise_for_status()
     with dest.with_suffix('.partial').open('wb') as f:
      for chunk in resp.iter_bytes():f.write(chunk)
    dest.with_suffix('.partial').rename(dest)
   print(h,'downloaded',dest,flush=True);break
  if status=='failed':print(json.dumps(d),flush=True);raise RuntimeError('HeyGen render failed; see saved status')
  time.sleep(20)
 else:raise TimeoutError('Resume saved job, do not submit again')
