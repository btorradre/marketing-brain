from pathlib import Path
import json,hashlib,time
from shopify_access import SESSION,BASE,BUILD,get
THEME=151410507841
assert get(f'/themes/{THEME}.json')['theme']['role']=='unpublished'
receipt_path=BUILD/'shopify/theme-upload-receipts.json'
receipts=json.loads(receipt_path.read_text()) if receipt_path.exists() else {}
existing={x['key'] for x in get(f'/themes/{THEME}/assets.json')['assets']}
files=[p for p in (BUILD/'theme').rglob('*') if p.is_file() and 'assets' not in p.relative_to(BUILD/'theme').parts]
for p in sorted(files,key=lambda p:(p.parent.name=='templates',str(p))):
 key=p.relative_to(BUILD/'theme').as_posix();text=p.read_text();digest=hashlib.sha256(text.encode()).hexdigest()
 assert 'wk-editorial' in key or key in ['locales/en.default.json','locales/en.default.schema.json']
 if key in receipts and receipts[key]['sha256']==digest:continue
 if key in existing:
  current=get(f'/themes/{THEME}/assets.json',{'asset[key]':key})['asset']['value']
  if key in receipts:
   if hashlib.sha256(current.encode()).hexdigest() not in [receipts[key]['remote_sha256'],receipts[key]['sha256']]:raise RuntimeError('Remote changed since our write: '+key)
  else:
   backup=BUILD/'shopify/staging-backup'/key
   if not backup.exists():raise RuntimeError('Refusing to overwrite unowned file: '+key)
   if current!=backup.read_text():raise RuntimeError('Remote changed since backup: '+key)
   if key.startswith('locales/'):
    old=json.loads(current);new=json.loads(text)
    assert all(k in new and new[k]==v for k,v in old.items()),'Existing translation changed'
 r=SESSION.put(BASE+f'/themes/{THEME}/assets.json',json={'asset':{'key':key,'value':text}},timeout=60)
 if not r.ok:print('Upload failed',key,r.status_code,r.text[:2000]);r.raise_for_status()
 remote=get(f'/themes/{THEME}/assets.json',{'asset[key]':key})['asset']['value']
 receipts[key]={'key':key,'sha256':digest,'remote_sha256':hashlib.sha256(remote.encode()).hexdigest(),'updated_at':r.json()['asset']['updated_at']}
 receipt_path.write_text(json.dumps(receipts,indent=2));print('Staged and read back',key,flush=True);time.sleep(.3)
