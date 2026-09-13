import sys,json,time,shutil
from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parents[5];sys.path.insert(0,str(ROOT/'_engine/mcp/ad-engine'))
from engines import kie
import db
requests=json.loads((P/'product-image-requests.json').read_text())
for req in requests:
 receipt=P/(req['id']+'-image-job.json')
 if receipt.exists():continue
 assert kie.balance()>50
 url=kie.upload(str(ROOT/req['reference']),'motilli/podcast-v5/product-ref')
 job=kie.generate('gpt-image-2-image-to-image',{'prompt':req['prompt'],'input_urls':[url],'aspect_ratio':'9:16'},brand='motilli',concept='podcast-DVHp-v5')
 receipt.write_text(json.dumps(job,indent=2));print(req['id'],job,flush=True)
for req in requests:
 receipt=P/(req['id']+'-image-job.json');job=json.loads(receipt.read_text())
 while job['status'] not in ['success','fail']:
  time.sleep(6);job=kie.status((job.get('job_id') or job['id']));receipt.write_text(json.dumps(job,indent=2))
 if job['status']=='success':
  with db.get_conn() as conn:a=conn.execute('SELECT path FROM assets WHERE job_id=?',((job.get('job_id') or job['id']),)).fetchone()
  shutil.copy2(a['path'],P/(req['id']+'.png'))
 print(req['id'],job['status'],flush=True)
