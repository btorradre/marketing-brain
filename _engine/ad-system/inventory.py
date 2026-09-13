"""Conservative discovery of real workspace artifacts; no inferred approval or success."""
import json
import re
from pathlib import Path
from store import blank_record, digest, now, packed, uid

ROLES={'editing-plan.md':'editing-plan','production-status.json':'status','production-status.md':'status','README.md':'notes'}
def infer_format(name):
    n=name.lower()
    return 'podcast' if 'podcast' in n else 'animated' if 'anim' in n else 'ugc' if 'ugc' in n else ''

def sync_brand(store,brand='motilli'):
    base=store.root/'brands'/brand/'creative'
    if not base.is_dir():raise ValueError('Brand creative directory does not exist.')
    boards=[]
    for p in (store.root/'cutroom/boards').glob('*.json'):
        try:
            j=json.loads(p.read_text())
            if j.get('project')==brand:boards.append((p,j))
        except (ValueError,OSError):continue
    records={r['id']:r for r in store.list(brand)};added=[];counts=0
    for folder in sorted(base.iterdir()):
        if not folder.is_dir() or folder.name.lower() in {'assets','archive','sources'}:continue
        rid=re.sub('[^A-Za-z0-9_-]','-',folder.name)
        r=records.get(rid) or blank_record(brand,folder.name);r['id']=rid
        fresh=rid not in records
        if fresh:
            r['context_notes']='Imported workspace project. Existing files are discovery evidence only; current selection, narration approval, claims and campaign status have not been inferred. Review and attach the exact current script/editing plan before production.'
            r['strategy']['format']=infer_format(folder.name)
            if r['strategy']['format']:r['context_notes']+=' Format suggested from folder name; confirm against the actual creative.'
        artifacts={a['path']:a for a in r['artifacts'] if a.get('path')}
        candidates=[]
        for p in folder.rglob('*'):
            if not p.is_file() or any(x in {'node_modules','.git','venv','__pycache__','receipts','candidates','proxies','screening','verdicts','qa','capcut','internal-editor'} for x in p.relative_to(folder).parts):continue
            rel=p.relative_to(folder);role=None
            if p.name in ROLES:role=ROLES[p.name]
            elif p.suffix in {'.md','.txt'} and ('script' in rel.parts or 'brief' in p.name.lower()):role='script' if 'script' in rel.parts else 'brief'
            elif p.suffix in {'.mp4','.mov'} and ('deliverables' in rel.parts or 'export' in p.name.lower() or 'final' in p.name.lower()):role='export-candidate'
            if role:candidates.append((p,role))
        for p,j in boards:
            normalized=re.sub('[^a-z0-9]','',rid.lower())
            if normalized in re.sub('[^a-z0-9]','',(j.get('id','')+' '+j.get('title','')).lower()):candidates.append((p,'cutroom-board'))
        # All discovered paths go into searchable inventory; manageable recent attachments per record.
        for p,role in candidates:
            rel=str(p.relative_to(store.root));meta=dict(path=rel,record_id=rid,brand=brand,role=role,size=p.stat().st_size,modified=p.stat().st_mtime,discovered=now(),status='discovered — current selection unverified')
            with store.connect() as c:c.execute('INSERT INTO inventory VALUES(?,?) ON CONFLICT(path) DO UPDATE SET body=excluded.body',(rel,packed(meta)))
            counts+=1
        candidates.sort(key=lambda pair:pair[0].stat().st_mtime,reverse=True)
        chosen=[]
        for role,limit in [('brief',5),('script',8),('editing-plan',10),('status',4),('cutroom-board',10),('export-candidate',6)]:chosen += [(p,k) for p,k in candidates if k==role][:limit]
        for p,role in chosen:
            rel=str(p.relative_to(store.root))
            if rel not in artifacts:artifacts[rel]=dict(id='FILE-'+digest(rel)[:10],path=rel,role=role,label=p.name,status='discovered; selection unverified')
        changed=fresh or list(artifacts.values())!=r['artifacts'];r['artifacts']=list(artifacts.values())
        if changed:store.save(r,r['revision'],reason='Workspace artifact inventory; no approvals inferred');added.append(rid)
    # Brand context files are catalogued, not promoted into verified claims.
    context=[]
    brandroot=store.root/'brands'/brand
    for p in brandroot.rglob('*'):
        if p.is_file() and 'creative' not in p.relative_to(brandroot).parts and p.suffix.lower() in {'.md','.txt','.json','.csv'} and not any(x.startswith('.') or x in {'node_modules','venv','__pycache__'} for x in p.relative_to(brandroot).parts):
            rel=str(p.relative_to(store.root));m=dict(path=rel,brand=brand,role='brand-context',size=p.stat().st_size,status='source discovered; content/claims unverified')
            with store.connect() as c:c.execute('INSERT INTO inventory VALUES(?,?) ON CONFLICT(path) DO UPDATE SET body=excluded.body',(rel,packed(m)))
            context.append(rel)
    legacy=store.root/'_engine/creative-tracker/performance-snapshot.csv'
    report=dict(brand=brand,changed_creatives=added,artifact_count=counts,brand_context_files=len(context),legacy_performance=dict(path=str(legacy.relative_to(store.root)),exists=legacy.exists(),status='Not imported as attributable results: legacy snapshot has ad names/derived ratios and lacks required IDs, raw denominators and reporting settings.'),created=now())
    out=store.db.parent/'inventory'/f'{brand}.json';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2))
    return report

def inventory(store,brand=None):
    with store.connect() as c:rows=[json.loads(x['body']) for x in c.execute('SELECT body FROM inventory')]
    return [r for r in rows if brand is None or r.get('brand')==brand]
