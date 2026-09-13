from pathlib import Path
import json,httpx,time,sys,concurrent.futures,hashlib,os
O=Path(__file__).resolve().parent;P=O.parents[1];ROOT=O.parents[5];D=P/'assets/video-v24';key=next(l.split('=',1)[1].strip().strip('"').strip("'") for l in (ROOT/'.env').read_text().splitlines() if l.startswith('HEYGEN_API_KEY='));look=json.loads((O.parent/'production-v18/heygen-avatar.json').read_text())['data']['avatar_item']['id']
with httpx.Client(timeout=90,headers={'X-Api-Key':key}) as c:
 r=c.get('https://api.heygen.com/v3/avatars/looks/'+look);r.raise_for_status();j=r.json();(O/'heygen-avatar-verified.json').write_text(json.dumps(j,indent=2));d=j['data'];assert d['status']=='completed' and 'avatar_v' in d['supported_api_engines'];print('Existing presenter verified ready for Avatar V',flush=True)
def run(h):
 S=O/(h+'-r2');S.mkdir(exist_ok=True)
 def save(n,j):(S/n).write_text(json.dumps(j,indent=2)+'\n')
 assert json.loads((O/f'qa/{h}-clean-technical.json').read_text())['pass']
 qa=json.loads((O/f'qa/{h}-clean-listening.json').read_text());qa=qa[0] if isinstance(qa,list) else qa;assert qa.get('usable') is True,qa
 audio=O/f'deliverables/Motilli-V24-{h}-Natural-1.2x-clean.mp3';dest=D/f'Motilli-V24-{h}-HeyGen-Natural-clean-r2.mp4'
 if dest.exists():print(h,'existing provider file preserved',flush=True);return
 with httpx.Client(timeout=180,headers={'X-Api-Key':key}) as c:
  jf=S/'heygen-video-job.json'
  if jf.exists():job=json.loads(jf.read_text())
  else:
   uf=S/'heygen-audio-upload.json'
   if uf.exists():up=json.loads(uf.read_text())
   else:
    r=c.post('https://upload.heygen.com/v1/asset',content=audio.read_bytes(),headers={'Content-Type':'audio/mpeg'});r.raise_for_status();up=r.json();save('heygen-audio-upload.json',up);save('uploaded-audio-provenance.json',{'path':str(audio),'sha256':hashlib.sha256(audio.read_bytes()).hexdigest(),'cleaned_before_upload':True})
   aid=up['data'].get('id') or up['data'].get('asset_id');assert aid
   payload={'type':'avatar','avatar_id':look,'audio_asset_id':aid,'engine':{'type':'avatar_v'},'aspect_ratio':'9:16','resolution':'1080p','title':f'Motilli V24 {h} Michelle Natural 1.2x pauses removed'};save('heygen-video-request.json',payload)
   r=c.post('https://api.heygen.com/v3/videos',json=payload);save('heygen-submit-response.json',{'status':r.status_code,'body':r.json()});r.raise_for_status();job=r.json();save('heygen-video-job.json',job);print(h,'submitted',flush=True)
  d=job.get('data') or job;vid=d.get('video_id') or d.get('id');assert vid
  prev=None
  for i in range(180):
   r=c.get('https://api.heygen.com/v3/videos/'+vid);r.raise_for_status();j=r.json();save('heygen-video-status.json',j);d=j.get('data') or j;status=d.get('status')
   if status!=prev or i%3==0:print(h,status,flush=True);prev=status
   if status=='completed':
    with httpx.stream('GET',d['video_url'],timeout=300,follow_redirects=True) as resp:
     resp.raise_for_status()
     with dest.with_suffix('.partial').open('wb') as out:
      for chunk in resp.iter_bytes():out.write(chunk)
    dest.with_suffix('.partial').rename(dest);link=O/'deliverables'/dest.name
    if not link.exists():os.link(dest,link)
    print(h,'downloaded',dest,flush=True);return
   if status=='failed':raise RuntimeError(str(d))
   time.sleep(20)
  raise TimeoutError(h+' pending; resume saved job without resubmission')
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
 fs=[ex.submit(run,h) for h in (sys.argv[1:] or ['H1','H2','H3'])]
 for f in concurrent.futures.as_completed(fs):f.result()
