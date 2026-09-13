from pathlib import Path
import base64,json,time,sys,hashlib
from shopify_access import SESSION,BASE,BUILD,get
THEME=151410507841
assert get(f'/themes/{THEME}.json')['theme']['role']=='unpublished'
receipt_path=BUILD/'shopify/asset-upload-receipts.json'
receipts=json.loads(receipt_path.read_text()) if receipt_path.exists() else {}
existing={x['key'] for x in get(f'/themes/{THEME}/assets.json')['assets']}
files=[p for p in (BUILD/'theme/assets').iterdir() if p.is_file()]
for p in files:
 key='assets/'+p.name
 assert p.name.startswith('wk-editorial-')
 digest=hashlib.sha256(p.read_bytes()).hexdigest()
 if key in receipts and receipts[key].get('sha256')==digest:continue
 if key in existing and key not in receipts:raise RuntimeError('Unowned existing asset '+key)
 r=SESSION.put(BASE+f'/themes/{THEME}/assets.json',json={'asset':{'key':key,'attachment':base64.b64encode(p.read_bytes()).decode()}},timeout=90)
 r.raise_for_status();data=r.json()['asset'];data.pop('attachment',None);data['sha256']=digest;receipts[key]=data
 receipt_path.write_text(json.dumps(receipts,indent=2));print('Staged',key,data.get('public_url'),flush=True)
 time.sleep(.3)
