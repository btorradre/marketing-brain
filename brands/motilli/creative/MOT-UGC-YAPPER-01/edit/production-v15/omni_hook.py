import sys,json,time,concurrent.futures,importlib.util
from pathlib import Path
ROOT=Path('/Users/brooksorradre2/Documents/marketing brain');P=ROOT/'brands/motilli/creative/MOT-UGC-YAPPER-01';O=P/'edit/production-v15';D=P/'assets/video-v15'
spec=importlib.util.spec_from_file_location('omni',ROOT/'.claude/skills/omni-ugc/scripts/omni_ugc.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);key=m.env_key().strip('"').strip("'")
actions=json.loads((O/'omni-actions.json').read_text());jobs=[j for j in json.loads((O/'wardrobe-jobs.json').read_text()) if j['type']=='broll' and (not sys.argv[1:] or j['asset'] in sys.argv[1:])]
def run(b):
 name=b['asset'];dest=Path(b['selected_video']);state=D/(name+'.job.json')
 if dest.exists():print(name,'existing',flush=True);return
 assert Path(b['selected_image']).exists(),name+' selected image absent'
 prompt='Animate the supplied approved first frame as one continuous10-second vertical9:16 insert. Preserve this same mature woman, face, hair, age, NEW CLOTHING, objects, setting, lighting, angle and composition. Her outfit is '+b['outfit']+'. '+actions[name]+' Keep the selected outfit unchanged through all frames. No speech, no lip sync, no music, no on-screen captions, no additional text, no product branding. No cuts, transitions, zooms or camera travel. Restrained realistic visible action, not a still-image pan. This is covering footage for separately recorded narration.'
 if state.exists():j=json.loads(state.read_text());iid=j['id']
 else:
  body={'model':m.MODEL,'input':[m.media_part(b['selected_image']),{'type':'text','text':prompt}],'background':True,'generation_config':{'video_config':{}}};r=m.api('POST',m.API,key,body);iid=r.get('id');assert iid,'No interaction ID';j={'id':iid,'asset':name,'beat':b['id'],'prompt':prompt,'source':b['selected_image'],'status':r.get('status')};state.write_text(json.dumps(j,indent=2));print(name,'submitted',flush=True)
 start=time.time()
 while time.time()-start<1200:
  r=m.api('GET',m.API+'/'+iid,key);status=r.get('status');j['status']=status
  if status=='completed':
   blob,kind=m.extract_media(r,'video');dest.write_bytes(blob);j['usage']=r.get('usage');j['bytes']=len(blob);state.write_text(json.dumps(j,indent=2));print(name,'complete',len(blob),flush=True);return
  if status not in ['in_progress','queued',None]:j['error']=r.get('error');state.write_text(json.dumps(j,indent=2));raise RuntimeError(name+' failed: '+str(j['error'])[:200])
  time.sleep(8)
 raise RuntimeError(name+' timed out; resume with saved interaction')
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 futures={pool.submit(run,b):b for b in jobs}
 for f in concurrent.futures.as_completed(futures):
  try:f.result()
  except Exception as e:print(futures[f]['asset'],'ERROR',str(e)[:300],flush=True)
