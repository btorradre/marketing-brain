from pathlib import Path
import sys,json,subprocess,hashlib
P=Path(__file__).resolve().parent;R=P/'heygen-natural-corrected';R.mkdir(exist_ok=True)
ROOT=next(p for p in P.parents if (p/'_engine/mcp/ad-engine').exists())
sys.path.insert(0,str(ROOT/'_engine/mcp/ad-engine'));from engines import heygen
statepath=R/'state.json';state=json.loads(statepath.read_text()) if statepath.exists() else {}
def save():statepath.write_text(json.dumps(state,indent=2)+'\n')
def api(method,path,data=None):
 d=heygen._curl(method,'https://api.heygen.com'+path,data)
 if d.get('error'):raise RuntimeError(str(d['error'])[:500])
 return d['data']
def upload(path):
 d=heygen._curl('POST','https://api.heygen.com/v3/assets',extra=['-F','file=@'+str(path)])
 if not d.get('data',{}).get('asset_id'):raise RuntimeError(str(d)[:500])
 return d['data']['asset_id']
mode=sys.argv[1] if len(sys.argv)>1 else 'prepare'
if mode=='prepare':
 for kind,path in [('image',P/'plates/presenter-clean.png'),('audio',P/'voice-natural-corrected/narration-natural.mp3')]:
  if kind+'_asset_id' not in state:
   state[kind+'_asset_id']=upload(path);state[kind+'_source']={'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()};save()
 if 'look_id' not in state:
  d=api('POST','/v3/avatars',{'type':'photo','name':'Weekender Haaland Natural Avatar V','file':{'type':'asset_id','asset_id':state['image_asset_id']}})
  state['avatar_response']=d;state['look_id']=d['avatar_item']['id'];save()
 print(json.dumps({k:state[k] for k in ['image_asset_id','audio_asset_id','look_id']}))
elif mode=='submit':
 assert 'video_id' not in state,'Already submitted: poll existing video'
 d=api('GET','/v3/avatars/looks/'+state['look_id']);(R/'look-status.json').write_text(json.dumps(d,indent=2))
 engines=d.get('supported_api_engines',[]);assert 'avatar_v' in engines,engines
 payload={'type':'avatar','avatar_id':state['look_id'],'audio_asset_id':state['audio_asset_id'],'engine':{'type':'avatar_v'},'resolution':'1080p','aspect_ratio':'auto','title':'Weekender — Fresh Reference Clone — Eleven v3 Natural — Avatar V'}
 (R/'request.json').write_text(json.dumps(payload,indent=2));state['submission_started']=True;save()
 d=api('POST','/v3/videos',payload);state['video_id']=d['video_id'];state['submit_response']=d;save();print(json.dumps(d))
elif mode=='poll':
 d=api('GET','/v3/videos/'+state['video_id']);(R/'status.json').write_text(json.dumps(d,indent=2));print(json.dumps({'video_id':state['video_id'],'status':d.get('status'),'error':d.get('error')}),flush=True)
 if d.get('status')=='completed':
  out=R/'presenter-native.mp4'
  if not out.exists():
   subprocess.run(['curl','-f','-sS','-L','-o',str(out)+'.part',d['video_url']],check=True,timeout=600);Path(str(out)+'.part').rename(out)
  probe=subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(out)]);(R/'probe.json').write_bytes(probe)
  state['output']={'path':str(out),'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()};save();print('Downloaded original HeyGen presenter')
