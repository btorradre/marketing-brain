# /// script
# dependencies = ["pyobjc-framework-ApplicationServices", "pyobjc-framework-Quartz"]
# ///
import json,copy,shutil,importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location('b',Path('_engine/mcp/capcut-kit/capcut-bridge.py'));b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
assert not b.app_pid(),'CapCut must be closed'
p=Path('brands/motilli/creative/MOT-VID-013/edit/capcut')
for v in 'ABC':
 folder=b.DRAFT_ROOT/('MOT-VID-013-science-CapCut-'+v);f=folder/'draft_info.json';d=json.loads(f.read_text());shutil.copy2(f,p/f'draft-{v}-before-final-refine.json')
 mats=d['materials']['videos'];by={m['id']:m for m in mats};pen=next(m for m in mats if m['material_name']=='S36.mp4')
 for t in d['tracks']:
  for s in t['segments']:
   if s.get('source_timerange') is None:s['source_timerange']={'start':0,'duration':s['target_timerange']['duration']}
   if s['material_id'] not in by:continue
   m=by[s['material_id']]
   if m['material_name']=='S15.mp4':
    m.update(path=pen['path'],duration=pen['duration'],width=pen['width'],height=pen['height'],material_name='S15 — capped pen close-up');s['source_timerange']['start']=600000;s['clip']['scale']={'x':1.15,'y':1.15};s['uniform_scale']={'on':True,'value':1.15};s['clip']['transform']={'x':0,'y':.12}
   if m['material_name']=='HC1.mp4':
    s['clip']['scale']={'x':2.2,'y':2.2};s['uniform_scale']={'on':True,'value':2.2};s['clip']['transform']={'x':0,'y':1.1}
 f.write_text(json.dumps(d,ensure_ascii=False,separators=(',',':')));shutil.rmtree(folder/'Timelines',ignore_errors=True)
 print('Final source/crop refinement',v,flush=True)
