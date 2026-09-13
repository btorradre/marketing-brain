"""Readiness checks, concept comparison and resumable skill work packets."""
import copy
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from store import Invalid, Conflict, blank_record, content_digest, digest, file_hash, now, packed, uid

FORMATS = {
 'heygen-vsl':'broll-heygen-vsl','podcast':'broll-podcast','skeleton':'broll-skeleton-ads',
 'animated':'broll-animated-ads','voiceover-vsl':'broll-ai-voiceover-vsl','ugc':'broll-storytelling',
 'product-lifestyle':'broll-storytelling','static':'broll-storytelling'}
STAGES=['intake','research','concept','script','plan','calibration','production','storyboard','editing','review','ready','live','learning','archived']
TASKS={
 'research':('research',[],'Extract source-backed buying situations, desires, objections and product evidence. Preserve quotes exactly; label hypotheses and counterevidence.'),
 'concept':('research',[],'Compare substantive arguments. Separate buying reason, belief, proof, format and opening. Label same-argument work as iterations and define the changed variable.'),
 'script':('brief',['ai-ugc-vsl-scripting'],'Write or revise authorized narration and hook tests using approved evidence. Preserve locked narration unless the user authorized its revision.'),
 'plan':('brief',['broll-storytelling','ad-editing-style'],'Read the existing editing plan first. Inspect actual reference frames. Map every approved line to action, meaning, style, placement, source/gap, timing and editorial reason. Save the concrete plan in the concept edit folder.'),
 'source':('production',['broll-storytelling'],'Source the exact authorized actions in the concept’s treatment. Review a calibration sample before scaling, save real originals/provenance and actual interval audits. For TikTok extreme sourcing preserve EV5/no-text rules. Record gaps without inventing matches or switching to generation.'),
 'images':('production',['broll-storytelling','imagegen'],'Produce the planned first-frame images with GPT Image 2. Preserve approved identity, inspect actual output and attach receipts by beat. Use available approved generation tools.'),
 'video':('production',['broll-storytelling'],'Generate authorized video using Google Omni from inspected approved references. Preserve format/duration; report actual provider limitations and keep provider handles for resuming.'),
 'storyboard':('production',['broll-storytelling','cutroom'],'Use the existing Cut Room skill and board_builder.py. Deliver the correct brand board with actual first asset set, reference lane and per-card rationale; verify the saved board/URL. Never mark a text-only board as finished unless explicitly requested.'),
 'edit':('assets',['ad-editing-style'],'Read/update the editing plan, check the current DaVinci Resolve connection, preserve existing projects and use an isolated timeline. Align to approved voice/captions. Inspect actual selected replacements and export QA.'),
 'review':('assets',['broll-storytelling','ad-editing-style'],'Watch the finished asset, inspect timing, meaning, claims, identity, variety, text and sound. Record PASS/FLAG/FAIL with exact cue, evidence and fix; do not infer a full review from thumbnails.'),
 'analyze':('research',[],'Import performance with exact ad-ID/export joins and reporting settings. Calculate from totals. Write evidence-backed decisions, alternate explanations and the next test; do not call observational delivery causal.')}

def issue(out,verdict,field,reason,fix):out.append(dict(verdict=verdict,field=field,reason=reason,fix=fix))
def overall(checks):return 'FAIL' if any(x['verdict']=='FAIL' for x in checks) else 'FLAG' if any(x['verdict']=='FLAG' for x in checks) else 'PASS'
def qa(store,r,scope='delivery'):
    if scope not in ['research','brief','production','assets','delivery']:raise Invalid('Unknown review scope.')
    level=['research','brief','production','assets','delivery'].index(scope);out=[]
    def required(value,field,why):
        if not value:issue(out,'FAIL',field,why,'Supply the missing information or evidence at this field.')
    required(r.get('product'),'product','The product is unspecified.')
    required(r.get('context_notes') or r.get('artifacts'),'context_notes','No brief or context is attached.')
    evidence={e['id']:e for e in r['evidence']}
    for e in r['evidence']:
        if not e.get('source_path') and not e.get('source_url'):issue(out,'FLAG','evidence.'+e['id'],'Evidence lacks a retrievable source.','Attach the original path/URL, date and product version where relevant.')
        if not e.get('date'):issue(out,'FLAG','evidence.'+e['id']+'.date','Evidence date is missing.','Record the source date, or explicitly unknown.')
        if e.get('kind')=='quote':
            try:
                if e.get('text','') not in store.source_text(e):issue(out,'FAIL','evidence.'+e['id'],'The source no longer contains this quotation.','Restore exact source text or correct the quotation with provenance.')
            except Invalid as ex:issue(out,'FAIL','evidence.'+e['id'],str(ex),'Restore the source artifact.')
    if level>=1:
        for k in ['buyer_situation','belief_to_change','promise','proof','format','treatment','hypothesis']:
            required(r['strategy'].get(k),'strategy.'+k,'Concept decision is unspecified.')
        if r['strategy'].get('format') not in FORMATS:issue(out,'FLAG','strategy.format','No specialist route is registered for this format.','Choose the closest format and describe the intended treatment; extend routing if needed.')
        if not evidence:issue(out,'FLAG','evidence','No research evidence has been attached.','Keep buying motivation explicitly hypothetical; attach verified product facts before claim-based production.')
        if r['kind']!='concept':
            for k in ['fixed','changed']:required(r['strategy'].get(k),'strategy.'+k,'The iteration does not isolate its intended change.')
        for claim in r['claims']:
            refs=claim.get('evidence_ids',[])
            if claim.get('status')!='supported' or not refs or any(x not in evidence for x in refs):issue(out,'FAIL','claims.'+claim['id'],'Claim is unsupported or references missing evidence.','Attach relevant verified evidence and the reviewer rationale, or remove the claim.')
            elif any(evidence[x].get('kind')=='hypothesis' or not evidence[x].get('verified') for x in refs):issue(out,'FAIL','claims.'+claim['id'],'A hypothesis/unverified source is being used as verified product evidence.','Supply relevant verified evidence; customer experience alone does not establish efficacy.')
            if not claim.get('review_notes'):issue(out,'FLAG','claims.'+claim['id']+'.review_notes','Claim relevance and implied-visual meaning have not been reviewed.','Document why this evidence supports this exact wording and visual.')
    if level>=2:
        required(r.get('script'),'script','No production narration/copy is saved.')
        required(r.get('hooks'),'hooks','Opening and hook test are unspecified.')
        for h in r['hooks']:
            for k in ['line','visual','test']:required(h.get(k),'hooks.'+h['id']+'.'+k,'The hook does not describe what the viewer hears/sees or what changes.')
        hook_pairs=[(h.get('line','').strip().lower(),h.get('visual','').strip().lower()) for h in r['hooks']]
        if len(set(hook_pairs))!=len(hook_pairs):issue(out,'FAIL','hooks','Duplicate spoken-and-visual hooks.','Change the actual test variable or remove duplicates.')
        required(r.get('editing_plan'),'editing_plan','A concrete editing plan must precede production.')
        if r.get('editing_plan'):
            try:store.safe_file(r['editing_plan'])
            except Invalid as ex:issue(out,'FAIL','editing_plan',str(ex),'Attach the actual saved plan from this concept edit folder.')
        required(r.get('beats'),'beats','The story has no line-by-line scene plan.')
        if any(a.get('role')=='reference' for a in r['artifacts']) and not r.get('reference_audit'):issue(out,'FAIL','reference_audit','Reference media is attached but its actual frame audit is missing.','Inspect actual media and consecutive cut frames; attach the source audit.')
        for b in r['beats']:
            for k in ['line','action','story_function','medium','placement','why_line','viewer_response','style_fit','why_here','duration','cut_cue','transition_in','transition_out','source_route']:
                required(b.get(k) if k!='duration' else isinstance(b.get(k),(int,float)) and b['duration']>0,'beats.'+b['id']+'.'+k,'The scene is not executable or its editorial reason is missing.')
        if r['strategy'].get('format')=='animated' and any(b.get('medium') not in ['animation','illustration','presenter-animation'] for b in r['beats']):issue(out,'FLAG','beats.medium','A fully animated concept contains another medium.','Confirm the intentional hybrid treatment or generate matching animation.')
        if r['brand']=='velantra' and not any('product-skills' in a.get('path','') for a in r['artifacts']):issue(out,'FLAG','artifacts','Exact Velantra product/color/size routing is not attached.','Resolve the product registry and dedicated fidelity skill before generation.')
    if level>=3:
        assets={a['id']:a for a in r['assets']};seen={}
        for b in r['beats']:
            if b.get('placement')=='presenter':continue
            aid=b.get('asset_id');a=assets.get(aid)
            if not a:issue(out,'FAIL','beats.'+b['id']+'.asset_id','The scene has no selected asset.','Source/generate and inspect the actual asset, preserving the chosen route.');continue
            try:p=store.safe_file(a.get('path',''))
            except Invalid as ex:issue(out,'FAIL','assets.'+aid+'.path',str(ex),'Attach an accessible actual media file.');continue
            required(a.get('origin'),'assets.'+aid+'.origin','Asset provenance is unspecified.')
            required(a.get('inspection'),'assets.'+aid+'.inspection','Actual asset inspection is missing.')
            if a.get('origin')=='sourced':
                required(a.get('source_url'),'assets.'+aid+'.source_url','Original source URL is missing.')
                if a.get('rights')!='cleared':issue(out,'FLAG','assets.'+aid+'.rights','Commercial reuse is not cleared.','Keep research eligibility separate from permission to run the asset in an ad.')
            if a.get('specialization')=='tiktok-extreme':
                if a.get('action_match')!='verified':issue(out,'FAIL','assets.'+aid+'.action_match','The exact requested action/context has not been verified.','Inspect the selected interval against the spoken line; emotion alone does not establish action matching.')
                if a.get('entry_ev')!=5 or a.get('peak_ev')!=5 or a.get('rawness',0)<4:issue(out,'FAIL','assets.'+aid,'Extreme action sourcing gates are not met.','Find a sustained EV5 interval with rawness >=4 and the exact action.')
                if a.get('text_status')!='verified-clean' or not a.get('frame_audit'):issue(out,'FAIL','assets.'+aid+'.text_status','No complete selected-interval text audit is attached.','Inspect every selected frame; preserve current no-text requirements.')
            ident=a.get('source_identity') or a.get('sha256') or str(p)
            if ident in seen:issue(out,'FLAG','beats.'+b['id'],'This B-roll source is reused from '+seen[ident]+'.','Review actual composition/action variety; recrops do not count as unique scenes.')
            seen[ident]=b['id']
        cal=r.get('calibration',{})
        if cal.get('reviewed',0)>0 and cal.get('accepted',0)==0:issue(out,'FLAG','calibration','Calibration produced zero accepted assets.','Review the specific failures before another bulk run; do not silently lower the requirements.')
    if level>=4:
        required(r.get('cutroom_url'),'cutroom_url','The delivered storyboard URL is missing.')
        human=[x for x in store.related('reviews',r['id']) if x['kind']=='human' and x['body'].get('content_hash')==content_digest(r) and x['body'].get('verdict')=='PASS']
        if not human:issue(out,'FAIL','finished_review','No current-revision finished-media PASS review exists.','Watch the exact finished asset and save an evidenced review against this revision.')
        else:
            for x in human:
                try:
                    if file_hash(store.safe_file(x['body']['artifact_path']))!=x['body']['artifact_sha256']:issue(out,'FAIL','finished_review','Reviewed media has changed.','Review the current bytes and register a new export.')
                except Invalid:issue(out,'FAIL','finished_review','Reviewed artifact is unavailable.','Restore and verify the exact reviewed asset.')
    if not out:issue(out,'PASS',scope,'Recorded structural requirements are complete.','Actual truth, media meaning and campaign success are not established by structural checks.')
    return dict(scope=scope,revision=r['revision'],verdict=overall(out),checks=out,created=now())

def compare(records):
    result=[]
    for i,a in enumerate(records):
        for b in records[i+1:]:
            keys=['buyer_situation','belief_to_change','promise','proof']
            changed=[k for k in keys if a['strategy'].get(k,'').strip().lower()!=b['strategy'].get(k,'').strip().lower()]
            known=all(a['strategy'].get(k) and b['strategy'].get(k) for k in keys)
            result.append(dict(a=a['id'],b=b['id'],classification='needs strategy detail' if not known else 'substantive concept difference' if changed else 'same argument: execution/copy iteration',argument_changes=changed,format_change=a['strategy'].get('format')!=b['strategy'].get('format'),note='Field comparison aids review; it does not prove semantic uniqueness.'))
    return result

def task_packet(store,record,kind):
    if kind not in TASKS:raise Invalid('Unknown task type.')
    scope,skills,direction=TASKS[kind];r=record
    if kind=='source' and (any('tiktok' in b.get('source_route','').lower() for b in r['beats']) or any(a.get('specialization')=='tiktok-extreme' for a in r['assets'])):skills=skills+['tiktok-broll-sourcing']
    specific=FORMATS.get(r['strategy'].get('format'))
    if kind in {'plan','source','images','video','storyboard','edit','review'} and specific and specific not in skills:skills=skills+[specific]
    checks=qa(store,r,scope)
    lines=[f"# {r['id']} — {kind}",f"Creative revision: {r['revision']}",f"Brand / product: {r['brand']} / {r['product']}",'',direction,'', '## Current requirements','Read workspace AGENTS.md and the exact linked specialist instructions. User authorization persists; this packet creates no extra approval gate. GPT Image 2 / Google Omni / DaVinci Resolve. No HyperFrames or Remotion. No campaign launches or creator messages without explicit authorization.','']
    for s in skills:
        path=store.root/'.claude/skills'/s/'SKILL.md'
        if not path.exists():path=Path.home()/'.codex/skills'/s/'SKILL.md'
        if s=='imagegen':path=Path.home()/'.codex/skills/.system/imagegen/SKILL.md'
        lines.append('- '+str(path)+(' [MISSING — discover the current tool/skill before proceeding]' if not path.exists() else ''))
    from obsidian_memory import home as memory_home
    memory_note=memory_home(store)/'notes'/f"{r['id']}.md"
    lines+=['','## Shared Obsidian memory',str(memory_home(store)/'creatives'/f"{r['id']}.md"),'Read current memory and notes before execution; this packet is a snapshot. Notes are context, not approval.','Agent notes: '+str(memory_note),memory_note.read_text() if memory_note.exists() else '[No notes yet]']
    lines+=['','## Context and unresolved decisions',r['context_notes'],'','## Strategy',packed(r['strategy']),'','## Exact current narration',r['script'] or '[Not written]','','## Evidence',json.dumps(r['evidence'],indent=2,ensure_ascii=False),'','## Scene decisions']
    for b in r['beats']:lines.append(json.dumps(b,ensure_ascii=False,indent=2))
    lines+=['','## Existing artifacts',json.dumps(r['artifacts'],indent=2,ensure_ascii=False),'Editing plan: '+(r['editing_plan'] or '[Missing]'),'Cut Room: '+(r['cutroom_url'] or '[Not verified]'),'','## Readiness issues',json.dumps(checks,indent=2,ensure_ascii=False),'','## Receipt to save','Record exact outputs, beat IDs, original/provider source, local files, inspection evidence and unresolved gaps. For external jobs retain the real provider/process handle and last verified state; a stale status file does not prove a live job. Resume a confirmed handle before considering a retry. Save changes with the expected creative revision so another session cannot overwrite newer work.']
    return '\n'.join(lines)+'\n',checks

def queue_task(store,rid,kind,depends_on=None):
    r=store.get(rid);text,checks=task_packet(store,r,kind);deps=depends_on or []
    with store.connect() as c:
        for dep in deps:
            d=c.execute('SELECT record_id FROM tasks WHERE id=?',(dep,)).fetchone()
            if not d or d['record_id']!=rid:raise Invalid('Dependencies must be existing tasks for this creative.')
        existing=c.execute('SELECT * FROM tasks WHERE record_id=? AND revision=?',(rid,r['revision'])).fetchall()
        for x in existing:
            j=json.loads(x['body'])
            if j['kind']==kind and j['state'] not in {'done','cancelled'}:return dict(x,body=j)
        tid=uid('TASK');path=store.db.parent/'work-packets'/rid/f"r{r['revision']}-{tid}.md";path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text)
        body=dict(kind=kind,state='queued',depends_on=deps,packet=str(path),readiness=checks,handle=None,receipt=None,owner=None,lease_until=None)
        c.execute('INSERT INTO tasks VALUES(?,?,?,?,?)',(tid,rid,r['revision'],packed(body),now()));store.event(c,rid,'task_queued',dict(id=tid,kind=kind,revision=r['revision']))
    return dict(id=tid,record_id=rid,revision=r['revision'],body=body)

def update_task(store,tid,action,owner='',handle=None,receipt=None):
    with store.connect() as c:
        c.execute('BEGIN IMMEDIATE');x=c.execute('SELECT * FROM tasks WHERE id=?',(tid,)).fetchone()
        if not x:raise Invalid('Task not found.')
        b=json.loads(x['body']);r=json.loads(c.execute('SELECT body FROM records WHERE id=?',(x['record_id'],)).fetchone()['body'])
        if action=='start':
            if b['state'] not in {'queued','failed'}:raise Invalid('Reconcile the existing work/handle before starting again.')
            if r['revision']!=x['revision']:raise Conflict('Task belongs to an older creative revision. Queue a fresh packet.')
            if not owner:raise Invalid('Record the person/session taking this task.')
            for dep in b['depends_on']:
                d=c.execute('SELECT body FROM tasks WHERE id=?',(dep,)).fetchone()
                if json.loads(d['body'])['state']!='done':raise Invalid('Dependency is incomplete: '+dep)
            readiness=qa(store,r,TASKS[b['kind']][0])
            if readiness['verdict']=='FAIL' and b['kind'] not in {'research','concept','script','plan','review','analyze'}:raise Invalid('Resolve production readiness failures before execution.')
            b.update(state='working',owner=owner,lease_until=(datetime.now(timezone.utc)+timedelta(minutes=30)).isoformat())
        elif action=='submitted':
            if b['state']!='working' or not handle or not all(handle.get(k) for k in ['provider','id','verified_at']):raise Invalid('Submission requires working state and a real provider/process handle with verification time.')
            b.update(state='submitted',handle=handle)
        elif action=='reconcile':
            if b['state'] not in {'working','submitted','needs_reconcile'}:raise Invalid('Only unfinished work can be reconciled.')
            if not receipt or not receipt.get('observation') or receipt.get('state') not in {'live','terminal','missing'}:raise Invalid('Record current live/terminal/missing handle evidence.')
            if receipt['state']=='live':b.update(state='submitted' if b.get('handle') else 'working',lease_until=(datetime.now(timezone.utc)+timedelta(minutes=30)).isoformat())
            else:b.update(state='failed')
            b['last_reconciliation']=receipt
        elif action in {'done','failed','cancelled'}:
            if b['state'] in {'done','cancelled'}:raise Invalid('Task is already terminal.')
            if b['state']=='submitted' and action!='done':raise Invalid('Verify external termination or missing handle through reconciliation first.')
            if action=='done':
                if b['state'] not in {'working','submitted'}:raise Invalid('Only work in progress can be completed.')
                if not receipt or not receipt.get('path') or not receipt.get('observation'):raise Invalid('Completion requires an actual artifact and outcome observations.')
                p=store.safe_file(receipt['path']);receipt={**receipt,'sha256':file_hash(p)}
            b.update(state=action,receipt=receipt)
        else:raise Invalid('Unknown task action.')
        c.execute('UPDATE tasks SET body=?,updated=? WHERE id=?',(packed(b),now(),tid));store.event(c,x['record_id'],'task_'+action,dict(id=tid,body=b))
    return dict(id=tid,record_id=x['record_id'],revision=x['revision'],body=b)

def task_view(task):
    t=copy.deepcopy(task);b=t['body']
    if b.get('lease_until') and b['state'] in {'working','submitted'}:
        if datetime.fromisoformat(b['lease_until'])<datetime.now(timezone.utc):b['display_state']='needs_reconcile'
    b.setdefault('display_state',b['state']);return t

def transition(store,rid,stage,expected_revision):
    if stage not in STAGES:raise Invalid('Unknown stage.')
    r=store.get(rid)
    scopes={'concept':'research','script':'brief','plan':'brief','calibration':'production','production':'production','storyboard':'assets','editing':'assets','review':'assets','ready':'delivery'}
    if stage in scopes:
        review=qa(store,r,scopes[stage])
        if review['verdict']=='FAIL':raise Invalid('Resolve '+scopes[stage]+' readiness failures before moving to '+stage+'.')
    if stage=='live':
        if qa(store,r,'delivery')['verdict']=='FAIL':raise Invalid('Resolve delivery checks before marking this revision live.')
        with store.connect() as c:
            bound=c.execute('SELECT e.* FROM bindings b JOIN exports e ON e.id=b.export_id WHERE e.record_id=?',(rid,)).fetchall()
        matches=[]
        for e in bound:
            b=json.loads(e['body'])
            if content_digest(store.get(rid,e['revision']))==content_digest(r) and file_hash(store.safe_file(b['path']))==b['sha256']:matches.append(e)
        if not matches:raise Invalid('Record an actual platform ad ID bound to an unchanged export of this creative content before marking live.')
    r['stage']=stage
    return store.save(r,expected_revision,reason='Stage changed to '+stage,stage_checked=True)
