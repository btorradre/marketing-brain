"""Match each final PNG to the generation receipt that produced its exact bytes."""
import json,pathlib,hashlib,collections
BASE=pathlib.Path(__file__).resolve().parent
jobs=json.loads((BASE/'generation-jobs.json').read_text())
receipts=collections.defaultdict(list)
for p in (BASE/'receipts').glob('*.json'):
 try:
  r=json.loads(p.read_text());r['receipt']=str(p.relative_to(BASE));receipts[int(r['job'])].append(r)
 except (ValueError,KeyError): pass
prompts=[]
for j in jobs:
 f=BASE/j['output']
 if not f.exists():continue
 h=hashlib.sha256(f.read_bytes()).hexdigest(); matched=None
 for r in receipts[j['job']]:
  p=pathlib.Path(r['generated_path'])
  if p.exists() and hashlib.sha256(p.read_bytes()).hexdigest()==h:matched=r;break
 prompts.append({'job':j['job'],'handle':j['handle'],'source_image_id':j['source_image_id'],'final_png':j['output'],'final_png_sha256':h,'receipt':matched['receipt'] if matched else None,'prompt':matched['prompt'] if matched else None,'generation_method':'built-in image_gen','original_references':j['referenced_image_paths']})
(BASE/'final-prompt-set.json').write_text(json.dumps(prompts,indent=2))
print(json.dumps({'final_pngs':len(prompts),'matching_generation_receipts':sum(bool(p['receipt']) for p in prompts),'missing_receipts':[p['job'] for p in prompts if not p['receipt']]}))
