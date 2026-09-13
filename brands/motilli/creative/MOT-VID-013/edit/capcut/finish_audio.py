# /// script
# dependencies = ["pyobjc-framework-ApplicationServices", "pyobjc-framework-Quartz"]
# ///
import json,shutil,importlib.util,math
from pathlib import Path
spec=importlib.util.spec_from_file_location('b',Path('_engine/mcp/capcut-kit/capcut-bridge.py'));b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
assert not b.app_pid(),'CapCut must be closed'
p=Path('brands/motilli/creative/MOT-VID-013/edit/capcut')
for v in 'ABC':
 folder=b.DRAFT_ROOT/('MOT-VID-013-science-CapCut-'+v);f=folder/'draft_info.json';d=json.loads(f.read_text());shutil.copy2(f,p/f'draft-{v}-before-audio-finish.json')
 for t in d['tracks']:
  for s in t['segments']:
   if s.get('source_timerange') is None:s['source_timerange']={'start':0,'duration':s['target_timerange']['duration']}
   if t['type']=='audio':
    assert s['volume']<=1.001,'Audio gain already applied'
    s['volume']*=10**(11/20);s['last_nonzero_volume']=s['volume']
 f.write_text(json.dumps(d,ensure_ascii=False,separators=(',',':')));shutil.rmtree(folder/'Timelines',ignore_errors=True)
 print('Native audio gain +11dB',v,flush=True)
