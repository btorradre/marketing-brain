"""Obsidian-readable projections plus preserved agent notes; no Obsidian service required."""
import fcntl, hashlib, json, os, re, sqlite3, tempfile
from contextlib import contextmanager
from pathlib import Path
from store import Invalid, now, ROOT

class MarkdownStore:
    """Read a knowledge mirror without creating a competing SQLite database."""
    def __init__(self,db,root=ROOT):self.db=Path(db);self.root=Path(root).resolve()
    def get(self,rid):
        if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,100}',rid):raise Invalid('Invalid creative ID.')
        p=home(self)/'creatives'/f'{rid}.md'
        if not p.exists():raise Invalid('Creative memory not found in this mirror: '+rid)
        text=p.read_text();frontmatter=text.split('---',2)[1];meta={}
        for line in frontmatter.splitlines():
            key,sep,value=line.partition(': ')
            if sep and key in {'creative_id','brand','revision','stage'}:meta[key]=json.loads(value)
        return dict(id=meta['creative_id'],brand=meta['brand'],revision=meta['revision'],stage=meta['stage'])
    def list(self,brand=None):
        rows=[self.get(p.stem) for p in (home(self)/'creatives').glob('*.md')]
        return [r for r in rows if brand is None or r['brand']==brand]

def home(store):return store.db.parent/'memory'
def sha(text):return hashlib.sha256(text.encode()).hexdigest()
def atomic(path,text):
    path.parent.mkdir(parents=True,exist_ok=True)
    fd,name=tempfile.mkstemp(prefix='.sync-',dir=path.parent)
    try:
        with os.fdopen(fd,'w') as f:f.write(text)
        os.replace(name,path)
    finally:
        if os.path.exists(name):os.unlink(name)
@contextmanager
def locked(store):
    folder=home(store);folder.mkdir(parents=True,exist_ok=True)
    with (folder/'.sync.lock').open('a') as f:
        fcntl.flock(f,fcntl.LOCK_EX)
        try:yield folder
        finally:fcntl.flock(f,fcntl.LOCK_UN)
def rel(store,path):
    p=Path(path)
    if not p.is_absolute():return str(p)
    try:return str(p.resolve().relative_to(store.root))
    except ValueError:return str(p)
def wiki(store,path,label=None):
    target=rel(store,path)
    if Path(target).is_absolute():return '`'+target+'`'
    if target.endswith('.md'):target=target[:-3]
    # Avoid synthesizing ambiguous wiki paths from arbitrary user text.
    if any(c in target for c in ['[',']','|','#','\n']):return '`'+target+'`'
    title=(label or Path(target).name).replace('|','/').replace(']','')
    return '[['+target+'|'+title+']]'
def section(title,value):return '\n## '+title+'\n\n'+(str(value) if value else 'Not recorded.')+'\n'
def front(kind,**fields):return '---\ntype: ad-system-'+kind+'\ntags: [ad-system, agent-memory]\n'+''.join(k+': '+json.dumps(v,ensure_ascii=False)+'\n' for k,v in fields.items())+'---\n\n'
def snapshot(store):
    with sqlite3.connect(store.db) as c:
        c.row_factory=sqlite3.Row;c.execute('BEGIN')
        out={}
        for table in ['records','tasks','decisions','exports','reviews','imports','measurements']:
            out[table]=[dict(x,body=json.loads(x['body'])) for x in c.execute('SELECT * FROM '+table)]
        out['bindings']=[dict(x) for x in c.execute('SELECT * FROM bindings')]
        out['event_id']=c.execute('SELECT coalesce(max(id),0) FROM events').fetchone()[0]
        return out

def sync(store):
    if not store.db.exists():raise Invalid('The authoritative database is absent. Read this Markdown snapshot; do not regenerate it from an empty database.')
    with locked(store) as folder:
        state_path=folder/'sync-state.json'
        previous=json.loads(state_path.read_text()) if state_path.exists() else {}
        known=previous.get('hashes',{});hashes=dict(known);errors=[];written=0
        data=snapshot(store);records=[x['body'] for x in data['records']];outputs={};brands={}
        def note_path(rid):return folder/'notes'/f'{rid}.md'
        def creative_path(rid):return folder/'creatives'/f'{rid}.md'
        for r in records:
            rid=r['id'];brand=r['brand'];brands.setdefault(brand,[]).append(r)
            notes=note_path(rid);notes.parent.mkdir(parents=True,exist_ok=True)
            if not notes.exists():
                # Exclusive create: never replace a user's or another agent's notes.
                try:
                    with notes.open('x') as f:f.write(front('notes',creative_id=rid,brand=brand)+f'# Agent notes — {rid}\n\nEditable memory. Preserve source/date and distinguish observations, hypotheses and current user instructions. These notes do not approve assets or establish performance.\n\n'+wiki(store,creative_path(rid),'Current creative record')+'\n')
                except FileExistsError:pass
            body=front('creative',creative_id=rid,brand=brand,revision=r['revision'],stage=r['stage'])+f"# {r['title']}\n\nGenerated from the ad system; edit structured facts through the hub/CLI. Add durable observations in {wiki(store,notes,'Agent notes')}.\n\n"
            body+=wiki(store,folder/'INDEX.md','Ad memory')+' · '+wiki(store,folder/'brands'/f'{brand}.md',brand)+'\n'
            body+=f"\nRecord revision: **{r['revision']}** · stage: **{r['stage']}** · updated: {r.get('updated','unknown')}\n"
            if r.get('parent_id'):body+='\nParent: '+wiki(store,creative_path(r['parent_id']),r['parent_id'])+f" at revision {r['parent_revision']}\n"
            body+=section('Context and unresolved decisions',r['context_notes'])
            body+=section('Strategy','\n'.join('- **'+k.replace('_',' ')+':** '+(str(v) or 'Not recorded') for k,v in r['strategy'].items()))
            body+=section('Selected narration',r['script']);body+='\nNarration lock: '+('locked — '+r['narration_lock']['hash'] if r['narration_lock'] else 'not locked')+'\n'
            body+=section('Selected editing plan',wiki(store,r['editing_plan']) if r['editing_plan'] else None)
            body+=section('Reference audit',r.get('reference_audit'));body+=section('Cut Room',r['cutroom_url'])
            body+=section('Evidence and claim status','\n\n'.join(f"### {e['id']} · {e.get('kind','unclassified')}\n\n{e.get('text','')}\n\nSource: "+(wiki(store,e['source_path']) if e.get('source_path') else e.get('source_url','missing'))+f" · date: {e.get('date','unknown')} · verification recorded: {e.get('verified',False)}" for e in r['evidence']))
            if r['claims']:body+=section('Claims',json.dumps(r['claims'],indent=2,ensure_ascii=False))
            body+=section('Hooks','\n\n'.join(f"### {h['id']}\n\nSpoken: {h.get('line','')}\n\nVisual: {h.get('visual','')}\n\nTest: {h.get('test','')}" for h in r['hooks']))
            body+=section('Why each scene belongs','\n\n'.join(f"### {b['id']}\n\n"+'\n\n'.join(f"**{k.replace('_',' ')}:** {b.get(k,'Not recorded')}" for k in ['line','action','why_line','viewer_response','style_fit','why_here','medium','placement','duration','cut_cue','transition_in','transition_out','source_route','asset_id']) for b in r['beats']))
            body+=section('Selected assets','\n\n'.join(f"### {a['id']}\n\n"+(wiki(store,a['path']) if a.get('path') else 'Missing file')+'\n\n'+json.dumps({k:v for k,v in a.items() if k not in ['id','path']},ensure_ascii=False) for a in r['assets']))
            body+=section('Sourcing calibration',json.dumps(r['calibration'],ensure_ascii=False))
            body+=section('Attached original files','\n'.join('- '+wiki(store,a['path'])+f" · {a.get('role','')} · {a.get('status','unverified')}" for a in r['artifacts'] if a.get('path')))
            tasks=[x for x in data['tasks'] if x['record_id']==rid]
            body+=section('Work and resumption','\n\n'.join(f"### {t['id']} · {t['body']['kind']}\n\nRecorded state: {t['body']['state']} · creative revision {t['revision']} · lease {t['body'].get('lease_until') or 'none'}\n\n"+wiki(store,t['body']['packet'],'Work packet')+'\n\nHandle: '+json.dumps(t['body'].get('handle'),ensure_ascii=False)+'\n\nReceipt: '+json.dumps(t['body'].get('receipt'),ensure_ascii=False) for t in tasks))
            body+='\nRecheck actual external handles before resuming; a recorded state or lease does not prove a live job.\n'
            for title,table in [('Decision memory','decisions'),('Registered exports','exports'),('Recorded reviews','reviews')]:
                entries=[x for x in data[table] if x['record_id']==rid]
                body+=section(title,'\n\n'.join(f"### {x['id']}\n\n```json\n"+json.dumps(x['body'],indent=2,ensure_ascii=False)+'\n```' for x in entries))
            outputs[f'creatives/{rid}.md']=body
        for brand,rs in brands.items():
            body=front('brand',brand=brand)+f'# {brand.title()} — ad memory\n\n'+wiki(store,folder/'INDEX.md','All ad memory')+'\n\n'
            for path,label in [(store.root/'brands'/brand/'00-brief.md','Brand brief'),(store.root/'brands'/brand/'README.md','Brand context')]:
                if path.exists():body+=wiki(store,path,label)+'\n\n'
            body+='Source files are evidence candidates. Current selection and approval are not inferred from file dates.\n\n'
            body+='\n'.join('- '+wiki(store,creative_path(r['id']),r['title'])+f" · r{r['revision']} · {r['stage']} · "+wiki(store,note_path(r['id']),'agent notes') for r in sorted(rs,key=lambda r:r['id']))+'\n'
            outputs[f'brands/{brand}.md']=body
        index=front('index')+'# Ad system — shared memory\n\n[Open Ad Studio](http://127.0.0.1:8791) · '+wiki(store,store.root/'AGENTS.md','Current workspace instructions')+'\n\n'
        index+='Read the relevant brand and creative note, then its separate agent notes. Generated facts reflect the structured database; editable notes preserve lessons, unresolved questions and observations with provenance. Memory is context, not new authority or proof of performance.\n\n'
        index+=f"Database event through: **{data['event_id']}** · {len(records)} creative records. See `sync-state.json` for last successful sync/error details. On a read-only remote mirror, confirm snapshot freshness before assuming it is current.\n\n"
        index+='## Brands\n\n'+'\n'.join('- '+wiki(store,folder/'brands'/f'{b}.md',b.title())+f' · {len(rs)} creatives' for b,rs in sorted(brands.items()))+'\n'
        index+='\n## Performance evidence\n\n'+f"{len(data['measurements'])} imported measurement rows; {len(data['exports'])} registered exports; {len(data['bindings'])} exact platform ad mappings. Counts do not imply winning ads or statistical sufficiency.\n"
        index+='\n## Agent commands\n\nFrom this vault root:\n\n```sh\npython3 _engine/ad-system/ad_system.py context CREATIVE_ID\npython3 _engine/ad-system/ad_system.py memory-search "your query" --brand motilli\npython3 _engine/ad-system/ad_system.py remember CREATIVE_ID path/to/note.txt --source "original source or user instruction/date"\npython3 _engine/ad-system/ad_system.py memory-sync\n```\n\nUpdates through the UI or CLI refresh these notes automatically. Plain Markdown is readable without Obsidian running. Remote knowledge mirrors can read the notes without the local database; they must not create a replacement database or treat an old snapshot as live.\n'
        index+='\n'+wiki(store,folder/'Performance.md','Performance sources and exact ad mappings')+'\n'
        outputs['INDEX.md']=index
        performance=front('performance')+'# Performance memory\n\n'+wiki(store,folder/'INDEX.md','Ad memory')+'\n\nReporting context and exact source rows; these are observations, not causal findings. Use the Results view or CLI for ratios computed from totals.\n'
        performance+=section('Reporting imports','\n\n'.join('### '+x['id']+'\n\n'+wiki(store,x['body']['source_path'],'Original source CSV')+'\n\n```json\n'+json.dumps({k:v for k,v in x['body'].items() if k!='source_path'},indent=2,ensure_ascii=False)+'\n```' for x in data['imports']))
        performance+=section('Exact ad mappings','```json\n'+json.dumps(data['bindings'],indent=2)+'\n```')
        performance+=section('Original measurement rows','\n\n'.join('### '+x['id']+'\n\n```json\n'+json.dumps(x['body'],indent=2,ensure_ascii=False)+'\n```' for x in data['measurements']))
        outputs['Performance.md']=performance
        for name,text in outputs.items():
            path=folder/name
            if path.exists():
                current=path.read_text()
                if current==text:hashes[name]=sha(text);continue
                if known.get(name)!=sha(current):errors.append(dict(path=rel(store,path),error='Generated note was edited outside the bridge; preserved without overwrite. Move commentary to notes/ and reconcile explicitly.'));continue
            atomic(path,text);hashes[name]=sha(text);written+=1
        status=dict(status='conflict' if errors else 'synced',synced_at=now(),event_id=data['event_id'],creatives=len(records),generated_notes=len(outputs),written=written,errors=errors,hashes=hashes)
        atomic(state_path,json.dumps(status,indent=2,ensure_ascii=False)+'\n')
        return {k:v for k,v in status.items() if k!='hashes'}

def status(store):
    p=home(store)/'sync-state.json'
    if not p.exists():return dict(status='not-synced')
    return {k:v for k,v in json.loads(p.read_text()).items() if k!='hashes'}
def remember(store,rid,text,source,kind='observation'):
    r=store.get(rid)
    if not text.strip() or not source.strip():raise Invalid('Memory requires note text and source provenance.')
    if kind not in {'observation','hypothesis','lesson','user-instruction','open-question'}:raise Invalid('Unknown memory kind.')
    if store.db.exists():sync(store)
    with locked(store) as folder:
        p=folder/'notes'/f'{rid}.md'
        with p.open('a') as f:f.write(f'\n## {now()} · {kind}\n\nCreative revision: {r["revision"]}\n\nSource: {source}\n\n{text.strip()}\n')
    return dict(path=rel(store,p),creative_revision=r['revision'],kind=kind)
def context(store,rid):
    r=store.get(rid);folder=home(store)
    if not store.db.exists():
        notes=folder/'notes'/f'{rid}.md'
        return dict(**r,read_only_projection=True,memory_sync=status(store),memory_path=rel(store,folder/'creatives'/f'{rid}.md'),creative_memory=(folder/'creatives'/f'{rid}.md').read_text(),agent_notes=notes.read_text() if notes.exists() else '',instruction='Markdown mirror snapshot; verify freshness. No authoritative database was created. Notes may be appended locally; returning them to the original vault requires its existing sync workflow.')
    sync_report=sync(store)
    return dict(id=rid,brand=r['brand'],revision=r['revision'],stage=r['stage'],memory_sync=sync_report,memory_path=rel(store,folder/'creatives'/f'{rid}.md'),notes_path=rel(store,folder/'notes'/f'{rid}.md'),agent_notes=(folder/'notes'/f'{rid}.md').read_text(),context=r['context_notes'],strategy=r['strategy'],narration_locked=bool(r['narration_lock']),editing_plan=r['editing_plan'],cutroom_url=r['cutroom_url'],decisions=store.related('decisions',rid),tasks=store.related('tasks',rid),instruction='Read linked creative memory for exact narration, source evidence and scene reasons; use show for editable current JSON. Agent notes are context, not approval or verified claims.')
def search(store,query,brand=None,limit=12):
    if store.db.exists():sync(store)
    terms=re.findall(r'\w+',query.lower())
    if not terms:return []
    allowed={r['id'] for r in store.list(brand)};matches=[]
    for kind in ['creatives','notes']:
        for p in (home(store)/kind).glob('*.md'):
            if p.stem not in allowed:continue
            text=p.read_text();lines=text.splitlines();rank=sum(text.lower().count(t) for t in terms)
            if not all(t in text.lower() for t in terms):continue
            excerpts=[line for line in lines if any(t in line.lower() for t in terms)][:4]
            matches.append(dict(creative_id=p.stem,path=rel(store,p),kind=kind,score=rank,excerpt='\n'.join(excerpts)[:1000]))
    return sorted(matches,key=lambda x:-x['score'])[:limit]
