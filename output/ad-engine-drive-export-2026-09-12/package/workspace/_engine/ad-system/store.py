"""Persistent, revisioned creative records. No external production side effects."""
import copy
import hashlib
import json
import re
import sqlite3
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

class Invalid(ValueError): pass
class Conflict(Invalid): pass

def now(): return datetime.now(timezone.utc).isoformat(timespec='seconds')
def uid(prefix): return prefix + '-' + uuid.uuid4().hex[:12]
def packed(value): return json.dumps(value, ensure_ascii=False, sort_keys=True, allow_nan=False)
def digest(value): return hashlib.sha256(packed(value).encode()).hexdigest()
def content_digest(record):
    return digest({k:v for k,v in record.items() if k not in {"revision","created","updated","stage","operational"}})

def file_hash(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''): h.update(chunk)
    return h.hexdigest()

def blank_record(brand='motilli', title='Untitled concept'):
    return dict(id=uid(brand.upper()[:4]), brand=brand, title=title, product='', kind='concept',
        parent_id=None, parent_revision=None, decision_id=None, stage='intake',
        strategy=dict(buyer_situation='', awareness='', belief_to_change='', promise='', proof='', format='', treatment='', hypothesis='', difference='', fixed='', changed=''),
        evidence=[], claims=[], hooks=[], script='', narration_lock=None, beats=[], assets=[],
        artifacts=[], context_notes='', reference_audit='', editing_plan='', cutroom_url='',
        calibration=dict(reviewed=0, accepted=0, notes='', next_action=''),
        production=dict(image_model='GPT Image 2', video_model='Google Omni', editor='DaVinci Resolve'),
        approvals=[], operational=dict(edit_minutes=None, rework_count=0), revision=0)

class EventConnection(sqlite3.Connection):
    memory_dirty = False

class Store:
    def __init__(self, db=None, root=ROOT):
        self.root = Path(root).resolve()
        self.db = Path(db or HERE/'data/system.sqlite3')
        self.db.parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as c:
            c.executescript('''
            PRAGMA journal_mode=WAL;
            CREATE TABLE IF NOT EXISTS records(id TEXT PRIMARY KEY, brand TEXT NOT NULL, revision INTEGER NOT NULL, body TEXT NOT NULL, updated TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS revisions(record_id TEXT, revision INTEGER, body TEXT NOT NULL, created TEXT NOT NULL, PRIMARY KEY(record_id,revision));
            CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY, record_id TEXT, kind TEXT, body TEXT, created TEXT);
            CREATE TABLE IF NOT EXISTS reviews(id TEXT PRIMARY KEY, record_id TEXT, revision INTEGER, kind TEXT, body TEXT, created TEXT);
            CREATE TABLE IF NOT EXISTS exports(id TEXT PRIMARY KEY, record_id TEXT, revision INTEGER, body TEXT, created TEXT);
            CREATE TABLE IF NOT EXISTS bindings(platform TEXT, account_id TEXT, ad_id TEXT, export_id TEXT, PRIMARY KEY(platform,account_id,ad_id));
            CREATE TABLE IF NOT EXISTS tasks(id TEXT PRIMARY KEY, record_id TEXT, revision INTEGER, body TEXT, updated TEXT);
            CREATE TABLE IF NOT EXISTS imports(id TEXT PRIMARY KEY, fingerprint TEXT UNIQUE, body TEXT, created TEXT);
            CREATE TABLE IF NOT EXISTS measurements(id TEXT PRIMARY KEY, import_id TEXT, row_key TEXT UNIQUE, body TEXT);
            CREATE TABLE IF NOT EXISTS decisions(id TEXT PRIMARY KEY, record_id TEXT, body TEXT, created TEXT);
            CREATE TABLE IF NOT EXISTS inventory(path TEXT PRIMARY KEY, body TEXT);
            ''')
    @contextmanager
    def connect(self):
        c = sqlite3.connect(self.db, timeout=20, factory=EventConnection)
        committed_memory = False
        c.row_factory = sqlite3.Row
        try:
            c.execute('PRAGMA foreign_keys=ON')
            yield c
            c.commit()
            committed_memory = c.memory_dirty
        except Exception:
            c.rollback(); raise
        finally: c.close()
        if committed_memory:self.refresh_memory()
    def refresh_memory(self):
        try:
            from obsidian_memory import sync
            return sync(self)
        except Exception as exc:
            # The database commit succeeded; never misreport it as a failed mutation.
            import sys
            from obsidian_memory import atomic, home
            previous=home(self)/"sync-state.json"
            try:report=json.loads(previous.read_text()) if previous.exists() else {}
            except (ValueError,OSError):report={}
            report.update(status="error",error=str(exc),at=now())
            try:atomic(home(self)/"sync-state.json",packed(report))
            except OSError:pass
            print("Ad memory sync needs attention: "+str(exc),file=sys.stderr)
            return report
    def event(self, c, rid, kind, data):
        c.memory_dirty = True
        c.execute('INSERT INTO events(record_id,kind,body,created) VALUES(?,?,?,?)',(rid,kind,packed(data),now()))
    def get(self, rid, revision=None):
        with self.connect() as c:
            r = c.execute('SELECT body FROM records WHERE id=?',(rid,)).fetchone() if revision is None else c.execute('SELECT body FROM revisions WHERE record_id=? AND revision=?',(rid,revision)).fetchone()
            if not r: raise Invalid('Creative or revision not found: '+str(rid))
            return json.loads(r['body'])
    def list(self, brand=None):
        with self.connect() as c:
            return [json.loads(r['body']) for r in c.execute('SELECT body FROM records WHERE (? IS NULL OR brand=?) ORDER BY updated DESC',(brand,brand))]
    def safe_file(self, value):
        p = Path(value)
        p = (self.root/p).resolve() if not p.is_absolute() else p.resolve()
        allowed = [self.root/'brands',self.root/'cutroom/boards',self.root/'cutroom/assets',self.root/'_engine/ad-system/data',self.root/'_engine/creative-research',self.root/'_engine/creative-tracker']
        if not any(p.is_relative_to(a) for a in allowed): raise Invalid('File must be a brand, board, research, tracker or ad-system artifact.')
        if any(x.startswith('.') for x in p.relative_to(self.root).parts): raise Invalid('Hidden files are not creative artifacts.')
        if p.suffix.lower() not in {'.md','.txt','.json','.csv','.png','.jpg','.jpeg','.webp','.mp4','.mov','.wav','.mp3','.pdf','.html'}: raise Invalid('Unsupported artifact type.')
        if not p.is_file(): raise Invalid('Artifact not found: '+str(value))
        return p
    def source_text(self, evidence):
        path=evidence.get('source_path')
        if path:
            p=self.safe_file(path)
            if p.suffix.lower() not in {'.txt','.md','.csv','.json'}: raise Invalid('Quotation verification requires a text source.')
            return p.read_text(errors='replace')
        return evidence.get('source_excerpt','')
    def validate(self, r, old=None, unlock_reason=''):
        if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,100}',r.get('id','')): raise Invalid('Invalid creative ID.')
        if not re.fullmatch(r'[a-z0-9-]+',r.get('brand','')): raise Invalid('Brand must be a lowercase slug.')
        if not r.get('title','').strip(): raise Invalid('Title is required.')
        for key in ['strategy','calibration','operational']:
            if not isinstance(r.get(key),dict): raise Invalid(key+' must be an object.')
        for key in ['script','product','context_notes','editing_plan','reference_audit','cutroom_url']:
            if not isinstance(r.get(key),str): raise Invalid(key+' must be text.')
        for key,value in r['strategy'].items():
            if not isinstance(value,str): raise Invalid('Strategy fields must be text.')
        for key in ['reviewed','accepted']:
            v=r['calibration'].get(key,0)
            if type(v) is not int or v<0: raise Invalid('Calibration counts must be nonnegative integers.')
        if r['calibration'].get('accepted',0)>r['calibration'].get('reviewed',0): raise Invalid('Accepted count cannot exceed reviewed count.')
        for key in ['edit_minutes','rework_count']:
            v=r['operational'].get(key)
            if v is not None and (type(v) not in {int,float} or v<0): raise Invalid('Operational measurements must be nonnegative numbers.')
        if old and (r['id']!=old['id'] or r['brand']!=old['brand']): raise Invalid('Creative identity cannot change.')
        if old and old.get('narration_lock'):
            if r.get('script')!=old.get('script') or r.get('narration_lock')!=old.get('narration_lock'):
                if not unlock_reason.strip(): raise Invalid('Narration is locked. Record the user-authorized revision reason before changing it.')
                r['narration_lock']=None
        if r.get('kind') not in {'concept','iteration','variant'}: raise Invalid('Unknown creative kind.')
        if r.get('kind')!='concept':
            if not r.get('parent_id') or not r.get('parent_revision'): raise Invalid('An iteration/variant needs an exact parent revision.')
            parent=self.get(r['parent_id'],r['parent_revision'])
            if parent['brand']!=r['brand']: raise Invalid('Parent belongs to a different brand.')
        for section in ['evidence','claims','hooks','beats','assets','artifacts','approvals']:
            if not isinstance(r.get(section),list): raise Invalid(section+' must be a list.')
            ids=[x.get('id') for x in r[section] if isinstance(x,dict)]
            if len(ids)!=len(r[section]) or any(not x for x in ids) or len(set(ids))!=len(ids): raise Invalid(section+' entries require distinct IDs.')
        for a in r['assets']:
            for k in ['entry_ev','peak_ev','rawness']:
                if a.get(k) is not None and (type(a[k]) not in {int,float} or not 1<=a[k]<=5):raise Invalid(k+' must be a score from 1 to 5.')
        for claim in r['claims']:
            if not isinstance(claim.get('evidence_ids',[]),list):raise Invalid('Claim evidence_ids must be a list.')
        for e in r['evidence']:
            if 'verified' in e and type(e['verified']) is not bool:raise Invalid('Evidence verified must be a boolean.')
            if e.get('kind')=='quote':
                if not e.get('text') or e['text'] not in self.source_text(e): raise Invalid('Quote '+e['id']+' does not occur verbatim in its source.')
                if not e.get('source_path') and not e.get('source_url'): raise Invalid('Quote requires source provenance.')
        allowed=dict(image_model='GPT Image 2',video_model='Google Omni',editor='DaVinci Resolve')
        if r.get('production')!=allowed: raise Invalid('Production routes must preserve GPT Image 2, Google Omni and DaVinci Resolve.')
        if r.get('narration_lock') and r['narration_lock'].get('hash')!=digest(r.get('script','')): raise Invalid('Narration lock does not match script.')
        packed(r)
    def save(self, record, expected_revision=None, reason='Saved creative', unlock_reason='', stage_checked=False):
        r=copy.deepcopy(record)
        old=None
        try: old=self.get(r['id'])
        except Invalid: pass
        if not stage_checked and ((old and r.get("stage")!=old.get("stage")) or (not old and r.get("stage")!="intake")): raise Invalid("Use the stage command to run readiness checks.")
        self.validate(r,old,unlock_reason)
        if old and old.get('stage') in {'ready','live'} and content_digest(old)!=content_digest(r):r['stage']='review'
        with self.connect() as c:
            c.execute('BEGIN IMMEDIATE')
            current=c.execute('SELECT revision FROM records WHERE id=?',(r['id'],)).fetchone()
            actual=current['revision'] if current else 0
            expected=expected_revision if expected_revision is not None else r.get('revision',0)
            if expected!=actual: raise Conflict('This creative changed since you opened it. Reload before saving.')
            r['revision']=actual+1;r['updated']=now();r.setdefault('created',now())
            c.execute('INSERT INTO records VALUES(?,?,?,?,?) ON CONFLICT(id) DO UPDATE SET revision=excluded.revision,body=excluded.body,updated=excluded.updated',(r['id'],r['brand'],r['revision'],packed(r),r['updated']))
            c.execute('INSERT INTO revisions VALUES(?,?,?,?)',(r['id'],r['revision'],packed(r),now()))
            self.event(c,r['id'],'revision',dict(revision=r['revision'],reason=reason,unlock_reason=unlock_reason))
        return r
    def history(self,rid):
        with self.connect() as c:
            return [dict(x,body=json.loads(x['body'])) for x in c.execute('SELECT * FROM events WHERE record_id=? ORDER BY id DESC',(rid,))]
    def related(self,table,rid=None):
        if table not in {'reviews','exports','tasks','decisions','imports'}: raise Invalid('Unknown collection.')
        with self.connect() as c:
            sql='SELECT * FROM '+table
            vals=()
            if rid is not None and table!='imports': sql+=' WHERE record_id=?';vals=(rid,)
            return [dict(x,body=json.loads(x['body'])) for x in c.execute(sql,vals)]
    def add_review(self,rid,kind,body,revision=None):
        r=self.get(rid);rev=r['revision'] if revision is None else revision
        if rev!=r['revision']: raise Conflict('Review is for an outdated revision.')
        if kind not in {'automated','human'}: raise Invalid('Unknown review kind.')
        if kind=='human' and not all(body.get(x) for x in ['reviewer','artifact_path','verdict','notes']): raise Invalid('Human review requires reviewer, actual artifact, verdict and observations.')
        if kind=='human':
            p=self.safe_file(body['artifact_path'])
            if p.suffix.lower() not in {'.mp4','.mov','.png','.jpg','.jpeg','.webp'}: raise Invalid('Finished-media review requires an actual image/video artifact.')
            body={**body,'artifact_sha256':file_hash(p)}
            if body['verdict'] not in {'PASS','FLAG','FAIL'}: raise Invalid('Unknown verdict.')
        body={**body,'content_hash':content_digest(r)}
        qid=uid('QA')
        with self.connect() as c:
            current=c.execute('SELECT revision FROM records WHERE id=?',(rid,)).fetchone()['revision']
            if current!=rev: raise Conflict('Creative changed during review.')
            c.execute('INSERT INTO reviews VALUES(?,?,?,?,?,?)',(qid,rid,rev,kind,packed(body),now()))
            self.event(c,rid,'review',dict(id=qid,revision=rev,kind=kind))
        return qid
    def register_export(self,rid,path,revision,hook_id,notes=''):
        r=self.get(rid,revision);p=self.safe_file(path)
        if p.suffix.lower() not in {'.mp4','.mov','.png','.jpg','.webp'}: raise Invalid('Export must be an actual rendered image/video.')
        if hook_id and hook_id not in {h['id'] for h in r['hooks']}: raise Invalid('Hook does not exist in this revision.')
        body=dict(path=str(p.relative_to(self.root)),sha256=file_hash(p),hook_id=hook_id,notes=notes)
        with self.connect() as c:
            # Duplicate registration is idempotent, but two creative revisions remain distinct.
            for row in c.execute('SELECT * FROM exports WHERE record_id=? AND revision=?',(rid,revision)):
                if json.loads(row['body'])==body:return dict(row,body=body)
            eid=uid('EXPORT');c.execute('INSERT INTO exports VALUES(?,?,?,?,?)',(eid,rid,revision,packed(body),now()))
            self.event(c,rid,'export',dict(id=eid,revision=revision,**body))
        return dict(id=eid,record_id=rid,revision=revision,body=body)
    def bind(self,platform,account_id,ad_id,export_id):
        if not all(isinstance(v,str) and v.strip() for v in [platform,account_id,ad_id,export_id]): raise Invalid('Platform, account ID, ad ID and export ID are required.')
        with self.connect() as c:
            e=c.execute('SELECT * FROM exports WHERE id=?',(export_id,)).fetchone()
            if not e:raise Invalid('Export not found.')
            body=json.loads(e['body'])
            if file_hash(self.safe_file(body['path']))!=body['sha256']:raise Invalid('Export file changed after registration; register a new export.')
            brand=self.get(e['record_id'],e['revision'])['brand']
            for measurement in c.execute('SELECT body FROM measurements'):
                m=json.loads(measurement['body']);settings=m['settings']
                if (settings['platform'],settings['account_id'],m['ad_id'])==(platform,account_id,ad_id) and settings['brand']!=brand: raise Invalid('Existing measurement identifies this ad as another brand.')
            old=c.execute('SELECT export_id FROM bindings WHERE platform=? AND account_id=? AND ad_id=?',(platform,account_id,ad_id)).fetchone()
            if old and old['export_id']!=export_id:raise Invalid('This ad ID is already bound to another export. Preserve history; use the correct platform ad ID.')
            c.execute('INSERT OR IGNORE INTO bindings VALUES(?,?,?,?)',(platform,account_id,ad_id,export_id))
            self.event(c,e['record_id'],'ad_binding',dict(platform=platform,account_id=account_id,ad_id=ad_id,export_id=export_id))
    def resolve_binding(self,platform,account,ad):
        with self.connect() as c:
            x=c.execute('SELECT e.* FROM bindings b JOIN exports e ON b.export_id=e.id WHERE b.platform=? AND b.account_id=? AND b.ad_id=?',(platform,account,ad)).fetchone()
            return dict(x,body=json.loads(x['body'])) if x else None
