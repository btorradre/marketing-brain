"""R3 asset jobs. Credentials come from the environment only."""
import json,sys,shutil
from pathlib import Path
R=Path(__file__).resolve().parent
ROOT=R.parents[5]
sys.path.insert(0,str(ROOT/'_engine/mcp/ad-engine'))
from engines import kie
import db
kie.VIDEO_MODELS.update({'gemini-omni-video','google/gemini-omni-flash-1-1'})
def save(p,data):p.write_text(json.dumps(data,indent=2))
mode=sys.argv[1];kind=sys.argv[2] if len(sys.argv)>2 else 'image'
requests=json.loads((R/f'{kind}-requests.json').read_text())
jobs_dir=R/'receipts';jobs_dir.mkdir(exist_ok=True)
for req in requests:
 receipt=jobs_dir/f"{req['id']}-{kind}.json"
 if mode=='submit':
  if receipt.exists():continue
  credit=kie.balance()
  if credit is None or credit < 30:raise RuntimeError('Balance unavailable or below reserve; no further submissions.')
  job=kie.generate(req['model'],req['input'],brand='motilli',concept='MOT-VID-013-visual-variety-r3')
  save(receipt,{**req,'job':job})
  print(req['id'],job['status'],flush=True)
 elif mode=='status' and receipt.exists():
  rec=json.loads(receipt.read_text());job_id=rec['job'].get('job_id') or rec['job']['id'];job=kie.status(job_id);rec['job']=job
  if job['status']=='success':
   with db.get_conn() as conn:
    assets=conn.execute('SELECT path,source_url FROM assets WHERE job_id=?',(job_id,)).fetchall()
   if assets and assets[0]['path']:
    dst=R/('keyframes' if kind=='image' else 'motion')/f"{req['id']}{'.png' if kind=='image' else '.mp4'}";dst.parent.mkdir(exist_ok=True)
    if not dst.exists():shutil.copy2(assets[0]['path'],dst)
    rec['output']=str(dst);rec['source_url']=assets[0]['source_url']
  save(receipt,rec);print(req['id'],job['status'],rec.get('output',''),flush=True)
