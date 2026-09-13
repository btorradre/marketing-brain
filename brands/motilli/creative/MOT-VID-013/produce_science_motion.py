"""Versioned scientific motion revision; uses native Google Omni outputs."""
import json,sys
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
import produce_motion as m
m.OUT=m.HERE/'output/science-v2/motion';m.OUT.mkdir(parents=True,exist_ok=True)
jobs=json.loads((m.HERE/'science-v2-revisions.json').read_text())['changed_scenes']
m.MOTION={j['id']:j['motion'] for j in jobs}
plan=json.loads((m.HERE/'production-plan-science-v2.json').read_text())
shots=[s for s in plan['shots'] if s['id'] in m.MOTION and Path(s['frame']).exists() and (len(sys.argv)==1 or s['id'] in sys.argv[1:])]
failed=[]
with ThreadPoolExecutor(max_workers=4) as pool:
 futures={pool.submit(m.generate,s):s['id'] for s in shots}
 for f in as_completed(futures):
  try:f.result()
  except Exception as e:
   failed.append(futures[f]);print(futures[f]+': ERROR '+str(e),flush=True)
print(json.dumps({'requested':len(shots),'failed':failed}),flush=True)
