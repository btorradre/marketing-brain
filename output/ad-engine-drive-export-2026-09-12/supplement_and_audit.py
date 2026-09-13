from pathlib import Path
import json,re,hashlib,collections
out=Path('output/ad-engine-drive-export-2026-09-12').resolve()
ns={};code=(out/'build_export.py').read_text();exec(code.split('for label,base in roots:')[0],ns)
d=json.loads((out/'inventory.json').read_text())
ns['manifest']=d['files'];ns['excluded']=d['excluded'];ns['redactions']=d['redactions'];ns['symlinks']=d['symlinks'];ns['TEXT']={'.md','.mdx','.markdown'};ns['SPECIAL']=set()
for name in ['scratchpad','tmp']:
 ns['scan']('workspace/'+name,Path.cwd()/name)
# Credential audit with an independent assignment pattern; report paths/line numbers only.
rx=re.compile(r'''(?i)(?<![A-Z0-9_])([A-Z_]{0,80}(?:API_KEY|ACCESS_TOKEN|CLIENT_SECRET|SERVICE_ROLE_KEY)[A-Z_]{0,80}|password|authorization)\s*["']?\s*[:=]\s*["']([^"'\n]{20,})["']''')
candidates=[]
for m in d['files']:
 p=out/'package'/m['path']
 if p.suffix in {'.db','.sqlite','.sqlite3'}:continue
 t=p.read_text()
 for match in rx.finditer(t):
  val=match.group(2)
  if val=='[REDACTED_SECRET]' or not re.fullmatch(r'(?:Bearer )?[A-Za-z0-9_./+=:-]{20,}',val):continue
  if any(x in val.lower() for x in ['example','placeholder','your_','getenv','environment','api_key','api-key','access_token','os.environ']):continue
  candidates.append({'path':m['path'],'line':t.count('\n',0,match.start())+1,'key':match.group(1)})
(out/'secret-audit-candidates.json').write_text(json.dumps(candidates,indent=2))
(out/'inventory.json').write_text(json.dumps(d,indent=2))
print(json.dumps({'files':len(d['files']),'markdowns':sum(Path(m['path']).suffix in {'.md','.mdx','.markdown'} for m in d['files']),'secret_audit_candidates':candidates[:60],'candidate_count':len(candidates)},indent=2))
