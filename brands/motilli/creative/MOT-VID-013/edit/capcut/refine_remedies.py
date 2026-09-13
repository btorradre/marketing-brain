# /// script
# dependencies = ["pyobjc-framework-ApplicationServices", "pyobjc-framework-Quartz"]
# ///
import copy,json,shutil,importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location('b',Path('_engine/mcp/capcut-kit/capcut-bridge.py'));b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
assert not b.app_pid(),'Close CapCut normally first'
p=Path('brands/motilli/creative/MOT-VID-013/edit/capcut')
for v in 'ABC':
 folder=b.DRAFT_ROOT/('MOT-VID-013-science-CapCut-'+v);file=folder/'draft_info.json';d=json.loads(file.read_text());shutil.copy2(file,p/f'draft-{v}-before-remedy-crops.json')
 track=next(t for t in d['tracks'] if t['type']=='video' and t['flag']==0)
 ids={m['id']:m for m in d['materials']['videos']};out=[]
 for s in track['segments']:
  if ids[s['material_id']]['material_name']!='S06.mp4':out.append(s);continue
  assert s['target_timerange']['duration']>3700000,'Already refined'
  for i,(a,z,x) in enumerate([(310,352,.20),(352,364,.65),(364,392,.83),(392,423,.415)]):
   ss=copy.deepcopy(s);ss['id']=b.uid();start=round(a/30*1e6);end=round(z/30*1e6);ss['target_timerange']={'start':start,'duration':end-start};ss['source_timerange']={'start':start-s['target_timerange']['start'],'duration':end-start};ss['clip']['scale']={'x':3.,'y':3.};ss['uniform_scale']={'on':True,'value':3.};ss['clip']['transform']={'x':6*(.5-x),'y':1.80};ss['desc']='S06-'+str(i+1);out.append(ss)
 track['segments']=out
 for t in d['tracks']:
  for s in t['segments']:
   if s.get('source_timerange') is None:s['source_timerange']={'start':0,'duration':s['target_timerange']['duration']}
 file.write_text(json.dumps(d,ensure_ascii=False,separators=(',',':')));shutil.rmtree(folder/'Timelines',ignore_errors=True)
 print('Object-only remedy crops installed',v,flush=True)
