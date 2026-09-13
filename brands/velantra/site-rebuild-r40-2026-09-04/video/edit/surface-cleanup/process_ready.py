"""Prepare available retouched shots for subsequent visual QA, two workers max."""
import argparse,json,subprocess,sys
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path

p=argparse.ArgumentParser();p.add_argument('--family');a=p.parse_args()
tasks=[]
for family in json.loads(Path('shots.json').read_text()):
 if a.family and family['family']!=a.family:continue
 for shot in family['shots']:
  if not shot['retouch'] or not Path(shot['clean_frame']).exists():continue
  out=Path('plates')/family['family']/f"shot-{shot['number']:02d}"
  if (out/'tracking.json').exists():continue
  tasks.append((family,shot,out))

def run(task):
 family,s,out=task
 cmd=[sys.executable,'track_retouch.py',family['video'],s['clean_frame'],str(out),
      '--start',str(s['start']),'--end',str(s['end']),'--anchor',str(s['anchor'])]
 for index,path in s.get('extra_references',[]):cmd.extend(['--extra',f'{index}={path}'])
 if s.get('surface_only'):cmd.append('--surface-only')
 if s.get('plate_only'):cmd.append('--plate-only')
 if s.get('smooth_planar'):cmd.append('--smooth-planar')
 if s.get('polish_surface'):cmd.append('--polish-surface')
 if s.get('preserve_clean_lighting'):cmd.append('--preserve-clean-lighting')
 out.mkdir(parents=True,exist_ok=True)
 result=subprocess.run(cmd,capture_output=True,text=True)
 (out/'process.log').write_text(result.stdout+result.stderr)
 return {'family':family['family'],'shot':s['number'],'exit_code':result.returncode,'output':str(out)}

with ThreadPoolExecutor(max_workers=2) as pool:
 for future in as_completed([pool.submit(run,t) for t in tasks]):
  result=future.result();print(json.dumps(result),flush=True)
  if result['exit_code']:raise RuntimeError('Tracking failed; see process.log')
