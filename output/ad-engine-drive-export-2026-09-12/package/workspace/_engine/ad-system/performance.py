"""Ad-ID joins and ratios from source totals; observational decisions stay explicit."""
import copy
import csv
import io
import json
import math
from datetime import date
from store import Invalid, blank_record, digest, now, packed, uid

SETTINGS=['brand','platform','account_id','currency','attribution','conversion_event','click_definition','hook_definition','hold_definition']
COUNTS=['spend','purchases','revenue','impressions','clicks','video_starts','views_3s','thruplays']
REQUIRED=['ad_id','date_start','date_end','spend','purchases','impressions','clicks']
DEFINITIONS=dict(ctr='clicks / impressions × 100',cpa='spend / purchases',roas='revenue / spend',hook_rate='views_3s / impressions × 100',hold_rate='thruplays / views_3s × 100')

def number(value,field,required=False):
    if value is None or str(value).strip()=='':
        if required:raise Invalid('Missing '+field)
        return None
    try:v=float(value)
    except (ValueError,TypeError):raise Invalid(field+' must be a number without currency symbols or thousands separators.')
    if not math.isfinite(v) or v<0:raise Invalid(field+' must be finite and nonnegative.')
    return v

def validate_settings(s):
    for key in SETTINGS:
        if not isinstance(s.get(key),str) or not s[key].strip():raise Invalid('Reporting setting required: '+key)
    if s['hook_definition']!='3s_views/impressions' or s['hold_definition']!='thruplays/3s_views':raise Invalid('This importer currently supports hook=3s_views/impressions and hold=thruplays/3s_views. Other definitions must use a separate adapter.')

def import_csv(store,text,settings):
    validate_settings(settings)
    reader=csv.DictReader(io.StringIO(text));headers=reader.fieldnames or []
    missing=[x for x in REQUIRED if x not in headers]
    fingerprint=digest(dict(text=text,settings=settings))
    with store.connect() as c:
        prev=c.execute('SELECT * FROM imports WHERE fingerprint=?',(fingerprint,)).fetchone()
        if prev:return dict(prev,body=json.loads(prev['body']))
    iid=uid('IMPORT');errors=[];candidates=[];keys=set()
    if len(headers)!=len(set(headers)):errors.append(dict(row=0,error='Duplicate CSV column names.'))
    if missing:errors.append(dict(row=0,error='Missing columns: '+', '.join(missing)))
    else:
        for n,row in enumerate(reader,2):
            try:
                if None in row:raise Invalid('Row contains more values than the header.')
                if not row['ad_id'] or not row['ad_id'].strip():raise Invalid('Missing stable platform ad ID; ad names are not accepted as IDs.')
                for k in SETTINGS:
                    if row.get(k) and row[k]!=settings[k]:raise Invalid('Mixed reporting setting: '+k)
                start=date.fromisoformat(row['date_start']);end=date.fromisoformat(row['date_end'])
                if end<start:raise Invalid('date_end precedes date_start.')
                counts={k:number(row.get(k),k,k in REQUIRED) for k in COUNTS}
                item=dict(id=uid('ROW'),ad_id=row['ad_id'].strip(),date_start=str(start),date_end=str(end),totals=counts,settings=copy.deepcopy(settings),source_row=n,import_id=iid)
                key=digest([settings,item['ad_id'],str(start),str(end)])
                if key in keys:raise Invalid('Duplicate ad ID/date/settings row in this file.')
                keys.add(key);item['row_key']=key;candidates.append(item)
            except (Invalid,ValueError) as ex:errors.append(dict(row=n,error=str(ex),original=row))
    # Atomic validation: no partly imported files when malformed or duplicate input exists.
    with store.connect() as c:
        c.execute('BEGIN IMMEDIATE')
        prev=c.execute('SELECT * FROM imports WHERE fingerprint=?',(fingerprint,)).fetchone()
        if prev:return dict(prev,body=json.loads(prev['body']))
        old=[json.loads(x['body']) for x in c.execute('SELECT body FROM measurements')]
        for i,item in enumerate(candidates):
            for other in old+candidates[:i]:
                if other['ad_id']==item['ad_id'] and other['settings']==item['settings'] and max(other['date_start'],item['date_start'])<=min(other['date_end'],item['date_end']):
                    errors.append(dict(row=item['source_row'],error='Overlapping delivery window for the same ad and reporting settings; would double-count.',other_row_id=other['id']))
                    break
        unmatched=[];wrong_brand=[]
        for item in candidates:
            match=store.resolve_binding(settings['platform'],settings['account_id'],item['ad_id'])
            if not match:unmatched.append(dict(row=item['source_row'],ad_id=item['ad_id']))
            elif store.get(match['record_id'],match['revision'])['brand']!=settings['brand']:wrong_brand.append(dict(row=item['source_row'],error='Ad binding belongs to another brand.'))
        errors+=wrong_brand
        raw=store.db.parent/'performance'/f'{iid}.csv';raw.parent.mkdir(parents=True,exist_ok=True);raw.write_text(text)
        body=dict(settings=settings,source_path=str(raw),errors=errors,unmatched=unmatched,accepted_row_ids=[] if errors else [x['id'] for x in candidates],status='rejected' if errors else 'imported',definitions=DEFINITIONS)
        if not errors:
            for item in candidates:c.execute('INSERT INTO measurements VALUES(?,?,?,?)',(item['id'],iid,item['row_key'],packed(item)))
        c.execute('INSERT INTO imports VALUES(?,?,?,?)',(iid,fingerprint,packed(body),now()))
        store.event(c,None,'performance_import',dict(id=iid,status=body['status'],rows=len(body['accepted_row_ids']),unmatched=len(unmatched),errors=len(errors)))
    return dict(id=iid,body=body)

def measurements(store,import_ids=None):
    with store.connect() as c:rows=[json.loads(x['body']) for x in c.execute('SELECT body FROM measurements')]
    if import_ids is not None:rows=[r for r in rows if r['import_id'] in import_ids]
    for r in rows:
        m=store.resolve_binding(r['settings']['platform'],r['settings']['account_id'],r['ad_id'])
        if m and store.get(m['record_id'],m['revision'])['brand']!=r['settings']['brand']:
            r['join_error']='Ad binding belongs to another brand';m=None
        r['binding']=dict(export_id=m['id'],record_id=m['record_id'],revision=m['revision'],hook_id=m['body']['hook_id']) if m else None
    return rows

def aggregate(rows):
    if not rows:return dict(totals={},metrics={},rows=[],note='Insufficient evidence: no matched measurements.')
    if len({packed(r['settings']) for r in rows})!=1:raise Invalid('Cannot combine different brands, accounts, currencies, attribution windows, conversion events or metric definitions.')
    totals={k:sum(r['totals'][k] for r in rows) if all(r['totals'].get(k) is not None for r in rows) else None for k in COUNTS}
    def ratio(n,d,m=1):return totals[n]/totals[d]*m if totals[n] is not None and totals[d] is not None and totals[d]>0 else None
    metrics=dict(cpa=ratio('spend','purchases'),roas=ratio('revenue','spend'),ctr=ratio('clicks','impressions',100),hook_rate=ratio('views_3s','impressions',100),hold_rate=ratio('thruplays','views_3s',100))
    return dict(settings=rows[0]['settings'],totals=totals,metrics=metrics,rows=[r['id'] for r in rows],definitions=DEFINITIONS,date_start=min(r['date_start'] for r in rows),date_end=max(r['date_end'] for r in rows),note='Observed delivery; not a randomized comparison. Missing totals/zero denominators produce null ratios. No automatic winner verdict.')

def analyze(store,import_ids=None):
    rows=measurements(store,import_ids);groups={};unmatched=[]
    for r in rows:
        if not r['binding']:unmatched.append(dict(row_id=r['id'],ad_id=r['ad_id'],import_id=r['import_id']));continue
        key=packed([r['settings'],r['binding']['export_id']]);groups.setdefault(key,[]).append(r)
    report=[]
    for rs in groups.values():report.append(dict(binding=rs[0]['binding'],**aggregate(rs)))
    return dict(groups=report,unmatched=unmatched,note='Groups stay separated by reporting settings and exact export. Date ranges are displayed; unequal delivery is not a causal test.')

def save_decision(store,rid,body):
    r=store.get(rid)
    for k in ['observation','interpretation','alternative','next_test','fixed','changed','outcome']:
        if not isinstance(body.get(k),str) or not body[k].strip():raise Invalid('Decision requires '+k)
    if body['outcome'] not in ['test','iterate','retire','insufficient_evidence']:raise Invalid('Unknown decision outcome.')
    ids=body.get('measurement_ids',[])
    if not isinstance(ids,list) or len(ids)!=len(set(ids)):raise Invalid('Decision measurement IDs must be a distinct list.')
    byid={x['id']:x for x in measurements(store)}
    for mid in ids:
        if mid not in byid or not byid[mid]['binding']:raise Invalid('Decision references a missing or unmatched performance row.')
        if byid[mid]['binding']['record_id']!=rid:raise Invalid('Decision row belongs to another creative.')
    if not ids and body['outcome']!='insufficient_evidence':raise Invalid('Performance conclusions require matched source rows; otherwise use insufficient_evidence.')
    if ids:aggregate([byid[x] for x in ids])
    did=uid('DECISION');b=copy.deepcopy(body);b.update(id=did,creative_revision=r['revision'],source_bindings=[dict(row_id=x,**byid[x]['binding']) for x in ids],created=now())
    with store.connect() as c:
        c.execute('INSERT INTO decisions VALUES(?,?,?,?)',(did,rid,packed(b),now()))
        store.event(c,rid,'decision',b)
    write_decisions(store,rid)
    return dict(id=did,record_id=rid,body=b)

def write_decisions(store,rid):
    p=store.db.parent/'creatives'/rid/'decisions.md';p.parent.mkdir(parents=True,exist_ok=True)
    lines=['# '+rid+' — decisions','']
    for x in store.related('decisions',rid):
        b=x['body'];lines += ['## '+x['id'],'',f"Creative revision: {b['creative_revision']} · {b['outcome']}",'']
        for k in ['observation','interpretation','alternative','next_test','fixed','changed']:lines += [k.replace('_',' ').capitalize()+': '+b[k],'']
        lines += ['Source rows: '+', '.join(b.get('measurement_ids',[])),'']
    p.write_text('\n'.join(lines));return p

def next_iteration(store,decision_id,title):
    with store.connect() as c:x=c.execute('SELECT * FROM decisions WHERE id=?',(decision_id,)).fetchone()
    if not x:raise Invalid('Decision not found.')
    d=json.loads(x['body']);parent=store.get(x['record_id'],d['creative_revision']);r=blank_record(parent['brand'],title)
    r.update(product=parent['product'],kind='iteration',parent_id=parent['id'],parent_revision=parent['revision'],decision_id=decision_id,strategy=copy.deepcopy(parent['strategy']),evidence=copy.deepcopy(parent['evidence']),claims=copy.deepcopy(parent['claims']),context_notes='Next brief from '+decision_id+'\nEvidence: '+d['observation']+'\nAlternative: '+d['alternative']+'\nNext test: '+d['next_test'])
    r['strategy'].update(fixed=d['fixed'],changed=d['changed'],hypothesis=d['next_test'],difference=d['changed'])
    # Reference the parent exactly; do not silently copy a finished script or its approvals/assets.
    return store.save(r,0,reason='Next brief from '+decision_id)

def operations(store):
    records=store.list();rows=measurements(store);tested={r['binding']['record_id'] for r in rows if r['binding'] and r['totals'].get('spend',0)>0 and r['totals'].get('impressions',0)>0};exported={x['record_id'] for x in store.related('exports')};times=[r['operational'].get('edit_minutes') for r in records if isinstance(r.get('operational',{}).get('edit_minutes'),(int,float))]
    return dict(creatives=len(records),creatives_with_exports=len(exported),creatives_with_attributable_delivery=len(tested),valid_test_coverage=len(tested&exported)/len(exported) if exported else None,recorded_edit_minutes=sum(times) if times else None,creatives_reporting_time=len(times),recorded_reworks=sum(r.get('operational',{}).get('rework_count',0) for r in records),definition='Valid-test coverage = exported creatives with exact-ID matched, positive-spend and positive-impression measurement rows / exported creatives. It measures trackable delivery, not statistical sufficiency. Rework is user-recorded; missing editing time is not zero.')
