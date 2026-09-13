from pathlib import Path
import os,re,json,hashlib,collections,sqlite3,csv,zipfile,datetime
HOME=Path.home(); ROOT=Path.cwd(); OUT=ROOT/'output/ad-engine-drive-export-2026-09-12'; STAGE=OUT/'package'; STAGE.mkdir(parents=True,exist_ok=True)
SKIP={'.git','node_modules','.venv','venv','__pycache__','.next','.cache','.pytest_cache','site-packages','dist','build','auth','oauth credentials','browser-profiles','.playwright-mcp'}
TEXT={'.md','.mdx','.markdown','.txt','.rst','.py','.js','.ts','.tsx','.jsx','.mjs','.cjs','.html','.css','.scss','.json','.jsonl','.yaml','.yml','.toml','.ini','.cfg','.sh','.bash','.zsh','.sql','.csv','.tsv','.xml','.srt','.vtt','.svg','.liquid','.j2','.jinja','.graphql','.gql','.proto'}
SPECIAL={'Makefile','Dockerfile','LICENSE','.gitignore','.dockerignore','.env.example','.env.template','requirements.txt'}
exclude_prefix=['output/ad-engine-drive-export-2026-09-12','auth','finances','_engine/finance','_engine/business/hiring/screening','_engine/conversation-log/transcripts','.obsidian/plugins','scratchpad','tmp','.playwright-mcp']
roots=[('workspace',ROOT),('external/adengine',HOME/'Documents/marketing-apps/adengine'),('installed-skills/codex',HOME/'.codex/skills'),('installed-skills/agents',HOME/'.agents/skills'),('installed-skills/claude',HOME/'.claude/skills'),('integrations/davinci-resolve-mcp',HOME/'.local/share/davinci-resolve-mcp'),('integrations/chatcut-plugin',HOME/'.codex/plugins/cache/chatcut-inc/chatcut/1.10.12')]
# Add the exact installed Drive/browser skill packages used for handoff and browser-driven production.
roots += [('integrations/google-drive-skills',HOME/'.codex/plugins/cache/openai-curated-remote/google-drive/0.1.16/skills'),('integrations/browser-skill',HOME/'.codex/plugins/cache/openai-bundled/browser/26.519.41501/skills')]
manifest=[];excluded=[]; redactions=[];symlinks=[];secrets=set()
secretkey=re.compile(r'(api.?key|access.?token|refresh.?token|client.?secret|password|authorization|bearer|private.?key|service.?role|secret.?key)',re.I)
def harvest(o):
 if isinstance(o,dict):
  for k,v in o.items():
   if secretkey.search(k) and isinstance(v,str) and len(v)>=10 and not v.startswith(('${','<','YOUR_')):secrets.add(v)
   else:harvest(v)
 elif isinstance(o,list):
  for v in o:harvest(v)
for base in [ROOT,HOME/'.codex']:
 candidates=[base/'.env',base/'config.toml',base/'.mcp.json']
 for p in candidates:
  if not p.is_file():continue
  try:
   t=p.read_text()
   if p.suffix=='.json':harvest(json.loads(t))
   elif p.suffix=='.toml':
    import tomllib;harvest(tomllib.loads(t))
   else:
    for line in t.splitlines():
     if '=' in line:
      k,v=line.split('=',1);v=v.strip().strip('\"\'')
      if len(v)>=10 and (secretkey.search(k) or k.endswith(('_KEY','_TOKEN','_SECRET'))):secrets.add(v)
  except Exception:pass
patterns=[('private-key',re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----[\s\S]*?-----END (?:RSA |EC |OPENSSH )?PRIVATE KEY-----')),('provider-key',re.compile(r'\b(?:sk-(?:proj-|ant-)?[A-Za-z0-9_-]{20,}|sk_[a-zA-Z0-9]{24,}|AIza[A-Za-z0-9_-]{30,}|gh[pousr]_[A-Za-z0-9]{25,}|github_pat_[A-Za-z0-9_]{30,}|xox[baprs]-[A-Za-z0-9-]{20,}|shpat_[a-fA-F0-9]{24,}|sb_secret_[A-Za-z0-9_-]{20,}|ya29\.[A-Za-z0-9._-]{30,})\b')),('jwt',re.compile(r'\beyJ[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]{15,}\b'))]
assignment=re.compile(r'''(?im)(?<![a-z0-9_])([\"']?(?:[a-z0-9_]{0,80}(?:api_key|apikey|access_token|refresh_token|client_secret|secret_key|service_role_key|password|bearer_token)|authorization)[\"']?\s*[:=]\s*[\"'])([^\"'\n]{10,})([\"'])''')
def clean(t):
 reasons=collections.Counter()
 for s in sorted(secrets,key=len,reverse=True):
  if s in t:reasons['known-secret']+=t.count(s);t=t.replace(s,'[REDACTED_SECRET]')
 for label,pat in patterns:t,n=pat.subn('[REDACTED_SECRET]',t);reasons[label]+=n
 def sub(m):
  v=m.group(2)
  if v.startswith(('${','<','[REDACTED','YOUR_','your_','os.','process.','Bearer {','Bearer $')) or re.search(r'(getenv|environ|example|placeholder)',v,re.I):return m.group(0)
  if re.fullmatch(r'(?:Bearer )?[A-Za-z0-9_.+/=:-]{16,}',v):reasons['secret-assignment']+=1;return m.group(1)+'[REDACTED_SECRET]'+m.group(3)
  return m.group(0)
 t=assignment.sub(sub,t)
 # Signed storage URLs are temporary access credentials; retain the underlying object path.
 t,n=re.subn(r'([?&](?:token|X-Amz-Signature|X-Goog-Signature|signature|access_token)=)[^\s\"\'&<>]+',r'\1[REDACTED_SECRET]',t,flags=re.I);reasons['signed-url']+=n
 return t,{k:v for k,v in reasons.items() if v}
def record(src,dest,data,method='copy',original=None,changes=None):
 p=STAGE/dest;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
 manifest.append({'path':dest,'source':str(src),'resolved_source':str(src.resolve()) if isinstance(src,Path) else str(src),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'source_sha256':hashlib.sha256(original if original is not None else data).hexdigest(),'method':method})
 if changes:redactions.append({'path':dest,'counts':changes})
def scan(label,base,rel=Path('.'),ancestors=()):
 folder=base/rel
 try:real=folder.resolve()
 except OSError:return
 if real in ancestors:excluded.append({'path':label+'/'+str(rel),'reason':'symlink-cycle'});return
 try:children=sorted(folder.iterdir())
 except OSError as e:excluded.append({'path':label+'/'+str(rel),'reason':type(e).__name__});return
 for p in children:
  r=p.relative_to(base);rp=r.as_posix();dest=label+'/'+rp;n=p.name
  if label=='workspace' and any(rp==x or rp.startswith(x+'/') for x in exclude_prefix):excluded.append({'path':dest,'reason':'export-output, temporary, credentials, or unrelated private records'});continue
  if p.is_dir():
   if n in SKIP or n in {'logs','.logs'}:excluded.append({'path':dest,'reason':'dependency/cache/auth/log directory'});continue
   if p.is_symlink():symlinks.append({'path':dest,'target':str(p.resolve()),'action':'materialized permitted files'})
   scan(label,base,r,ancestors+(real,));continue
  if not p.is_file():continue
  if n.startswith('.env') and n not in {'.env.example','.env.template'} or re.search(r'(^|[._-])(credentials?|cookies?|oauth|session|token)([._-]|$)',n,re.I) and p.suffix not in {'.md','.py','.ts','.js'}:
   excluded.append({'path':dest,'reason':'credential/session file'});continue
  if p.suffix.lower() in {'.sqlite','.sqlite3','.db'}:
   if rp not in {'_engine/ad-system/data/system.sqlite3','_engine/mcp/ad-engine/data/registry.sqlite3'}:excluded.append({'path':dest,'reason':'database outside selected ad-system snapshots'});continue
   target=STAGE/dest;target.parent.mkdir(parents=True,exist_ok=True)
   try:
    source=sqlite3.connect(p.as_uri()+'?mode=ro',uri=True);db=sqlite3.connect(target);source.backup(db);source.close()
    edits=0
    for (table,) in db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'").fetchall():
     qt='"'+table.replace('"','""')+'"'
     try:rows=db.execute(f'SELECT rowid,* FROM {qt}').fetchall();cols=[x[0] for x in db.execute(f'SELECT * FROM {qt} LIMIT 0').description]
     except sqlite3.Error:continue
     for row in rows:
      updates={}
      for col,v in zip(cols,row[1:]):
       if isinstance(v,str):
        new,why=clean(v)
        if new!=v:updates[col]=new;edits+=1
      if updates:
       sets=','.join('"'+k.replace('"','""')+'"=?' for k in updates)
       db.execute(f'UPDATE {qt} SET {sets} WHERE rowid=?',[*updates.values(),row[0]])
    db.commit();db.execute('VACUUM');check=db.execute('PRAGMA integrity_check').fetchone()[0];db.close()
    if check!='ok':raise RuntimeError(check)
    data=target.read_bytes();record(p,dest,data,'sqlite-consistent-backup',changes={'sanitized-db-fields':edits} if edits else None)
   except Exception as e:excluded.append({'path':dest,'reason':'sqlite backup error: '+type(e).__name__})
   continue
  if p.suffix.lower() not in TEXT and n not in SPECIAL:
   excluded.append({'path':dest,'reason':'media/binary/dependency artifact; documentation and source export'});continue
  # Unrelated raw financial/customer datasets are not production documentation.
  if label=='workspace' and any(x in rp for x in ['_engine/agents/cfo/','_engine/launchpad/data/','_engine/restock/']) and p.suffix.lower() not in {'.md','.py','.js','.html','.css'}:
   excluded.append({'path':dest,'reason':'operational dataset outside ad production'});continue
  try:raw=p.read_bytes();t=raw.decode('utf-8')
  except (OSError,UnicodeDecodeError) as e:excluded.append({'path':dest,'reason':'not readable UTF-8: '+type(e).__name__});continue
  cleantext,why=clean(t);data=cleantext.encode('utf-8');record(p,dest,data,'sanitized' if why else 'copy',raw,why)
for label,base in roots:
 if base.exists():scan(label,base)
 else:excluded.append({'path':label,'reason':'source not installed'})
# Export only MCP registrations, never whole account/session configs.
configs={}
for p in [ROOT/'.mcp.json',HOME/'.codex/config.toml',HOME/'.claude.json',HOME/'Library/Application Support/Claude/claude_desktop_config.json']:
 if not p.exists():continue
 try:
  if p.suffix=='.toml':
   import tomllib;d=tomllib.loads(p.read_text());v=d.get('mcp_servers',{})
  else:
   d=json.loads(p.read_text());v=d.get('mcpServers',{})
   if p.name=='.claude.json':
    for project,info in d.get('projects',{}).items():
     if 'marketing' in project and info.get('mcpServers'):v={**v,**{project+'::'+k:x for k,x in info['mcpServers'].items()}}
  t,why=clean(json.dumps(v,indent=2));configs[str(p)]=json.loads(t)
 except Exception as e:excluded.append({'path':str(p),'reason':'MCP config parse: '+type(e).__name__})
record('selected MCP config fields','integrations/mcp-configurations.sanitized.json',json.dumps(configs,indent=2).encode(),'selected-fields-and-sanitized')
(OUT/'inventory.json').write_text(json.dumps({'files':manifest,'excluded':excluded,'redactions':redactions,'symlinks':symlinks,'roots':[{'label':l,'source':str(p)} for l,p in roots]},indent=2))
print(json.dumps({'files':len(manifest),'markdowns':sum(Path(m['path']).suffix in {'.md','.mdx','.markdown'} for m in manifest),'skill_files':sum(Path(m['path']).name=='SKILL.md' for m in manifest),'bytes':sum(m['bytes'] for m in manifest),'sanitized_files':len(redactions),'excluded':len(excluded),'symlinks':len(symlinks),'by_root':dict(collections.Counter(m['path'].split('/')[0] for m in manifest))},indent=2))
