import sys,json,time,hashlib,shutil
from pathlib import Path
sys.path.insert(0,'/tmp')
from velantra_quantity_api import get,s,BASE
ROOT=Path(__file__).resolve().parent;tid=151519330369
assert get(f'/themes/{tid}.json')['theme']['role']=='unpublished'
files=sorted((ROOT/'after').rglob('*'));files=[f for f in files if f.is_file()];files.sort(key=lambda f:f.name=='theme.liquid')
def equal(k,a,b):return json.loads(a)==json.loads(b) if k.endswith('.json') else a.rstrip()==b.rstrip()
receipt=[]
for f in files:
 k=str(f.relative_to(ROOT/'after'));value=f.read_text();old=ROOT/'before'/k
 if old.exists():
  current=get(f'/themes/{tid}/assets.json',params={'asset[key]':k})['asset']['value']
  assert equal(k,current,old.read_text()) or equal(k,current,value),f'Concurrent change: {k}'
 r=s.put(BASE+f'/themes/{tid}/assets.json',json={'asset':{'key':k,'value':value}},timeout=40);r.raise_for_status()
 for i in range(8):
  actual=get(f'/themes/{tid}/assets.json',params={'asset[key]':k})['asset']['value']
  if equal(k,actual,value):break
  time.sleep(1)
 else:raise RuntimeError('Readback mismatch '+k)
 for target in [ROOT/'readback'/k,ROOT.parent/'theme'/k,ROOT.parent/'readback'/k]:target.parent.mkdir(parents=True,exist_ok=True);target.write_text(actual)
 receipt.append({'key':k,'sha256':hashlib.sha256(actual.encode()).hexdigest()});print('Verified',k,flush=True)
(ROOT/'deployment.json').write_text(json.dumps({'theme_id':tid,'role':'unpublished','files':receipt},indent=2))
