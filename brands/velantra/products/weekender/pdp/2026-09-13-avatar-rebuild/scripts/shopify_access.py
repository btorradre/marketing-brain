from pathlib import Path
import json,sys,requests
ROOT=Path(__file__).resolve().parents[7]
BUILD=Path(__file__).resolve().parents[1]
conf=json.loads((ROOT/'.claude/skills/shopify-financials/config/stores.json').read_text())
store=next(s for s in conf['stores'] if s.get('brand')=='Velantra')
sys.path.insert(0,str(ROOT/'.claude/skills/shopify-financials/scripts'))
from auth import token_for
SESSION=requests.Session()
SESSION.headers['X-Shopify-Access-Token']=token_for(store)
BASE=f"https://{store['domain']}/admin/api/2026-07"
def get(path,params=None):
 r=SESSION.get(BASE+path,params=params,timeout=45);r.raise_for_status();return r.json()
def graphql(query,variables=None):
 r=SESSION.post(BASE+'/graphql.json',json={'query':query,'variables':variables or {}},timeout=60);r.raise_for_status();return r.json()
if __name__=='__main__':
 d=get('/products/7971794747457/metafields.json',{'limit':250});fields=d.get('metafields',[]);out=[f for f in fields if any(t in (f['namespace']+' '+f['key']).lower() for t in ['review','rating','judge','loox','yotpo'])];(BUILD/'shopify/review-metadata.json').write_text(json.dumps(out,indent=2));print('REVIEW DATA',out);print('OTHER FIELD KEYS',[(f['namespace'],f['key']) for f in fields if f not in out])
