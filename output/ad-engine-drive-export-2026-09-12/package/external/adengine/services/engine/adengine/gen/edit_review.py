"""Immutable, workspace-scoped edit-style review rounds and revision protocol.

Gemini inspects original media; Astra grades; deterministic code owns pass/fail.
Review state lives in existing job records. Editor repairs happen through the
internal editor, followed by a new render and a new review round.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import time
from pathlib import Path

import jsonschema

from adengine.core.errors import GateRefused, ProviderError
from adengine.core.settings import settings
from adengine.core.store import Store
from adengine.engines import edit_grader, shell, watch
from adengine.gen import edit_plan as E, registry as R
from adengine.quality import load_rubric, evaluate_review
from adengine.workers import queue

KIND = "grade_edit_style"
MAX_EVENT_FRAMES = 180


def asset_hash(store, ws, asset):
    digest = hashlib.sha256()
    with store.open_blob(ws, asset['storage_key']) as stream:
        for data in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(data)
    return digest.hexdigest()


def read_json(store, ws, aid):
    asset = R.get_asset(store, ws, aid)
    if asset.get('mime') != 'application/json':
        raise GateRefused(f'{aid} must be a JSON asset')
    with store.open_blob(ws, asset['storage_key']) as stream:
        return json.load(stream)


def read_plan(store, ws, aid):
    asset = R.get_asset(store, ws, aid)
    if asset.get('kind') != 'edit_plan':
        raise GateRefused('Review requires the validated acceptance edit-plan asset')
    envelope = read_json(store, ws, aid)
    for rid, sha in envelope['analysis_fingerprints'].items():
        current = R.get_reference(store, ws, rid).get('manifest') or {}
        if E.fingerprint(current) != sha:
            raise GateRefused('Acceptance plan analysis is stale; resolve the changed source first')
    E.validate_handoff(envelope['plan'], envelope['analysis'])
    return envelope


def snapshot(store, ws, plan_id, reference_id, render_id, timeline_id):
    envelope = read_plan(store, ws, plan_id)
    role_ids = {'edit_plan': plan_id, 'reference': reference_id, 'render': render_id, 'timeline': timeline_id}
    if reference_id not in {m['video_asset_id'] for m in envelope['analysis'].values()}:
        raise GateRefused('Style reference must be an explicit reference in the acceptance plan evidence')
    for role in ('reference', 'render'):
        if not (R.get_asset(store, ws, role_ids[role]).get('mime') or '').startswith('video/'):
            raise GateRefused(f'{role} must be an actual video asset, not a storyboard or description')
    timeline = read_json(store, ws, timeline_id)
    with open(settings.packages_path('timeline', 'schema', 'project.schema.json')) as stream:
        schema = json.load(stream)
    try:
        jsonschema.validate(timeline, schema)
    except jsonschema.ValidationError as exc:
        raise GateRefused('Executed timeline is not an internal-editor Project', {'error': exc.message}) from exc
    ids = set(role_ids.values()) | {a['id'] for a in envelope['assets']}
    hashes = {aid: asset_hash(store, ws, R.get_asset(store, ws, aid)) for aid in sorted(ids)}
    rubric = load_rubric('edit_style')
    return {'role_ids': role_ids, 'hashes': hashes, 'rubric': rubric,
            'rubric_hash': E.fingerprint(rubric), 'timeline_version': timeline['version'],
            'timeline_execution_hash': timeline_execution_hash(timeline)}


def timeline_execution_hash(timeline):
    # Review notes, names and version counters cannot masquerade as an edit.
    execution = json.loads(json.dumps(timeline))
    for field in ('id','name','version','markers','meta'):
        execution.pop(field,None)
    for track in execution.get('tracks',[]):
        for field in ('name','locked'):
            track.pop(field,None)
        for clip in track['clips']:
            clip.pop('name',None)
    return E.fingerprint(execution)


def assert_current(store, ws, pinned):
    for aid, sha in pinned['hashes'].items():
        if asset_hash(store, ws, R.get_asset(store, ws, aid)) != sha:
            raise GateRefused('Review evidence changed; old grades cannot apply to new media')
    if E.fingerprint(pinned['rubric']) != pinned['rubric_hash']:
        raise GateRefused('Pinned rubric was modified')
    read_plan(store, ws, pinned['role_ids']['edit_plan'])


def enqueue_review(store, ws, *, plan_id, reference_id, render_id, timeline_id,
                   creator_id, previous_job_id=None, max_rounds=8):
    if type(max_rounds) is not int or max_rounds < 1 or max_rounds > 100:
        raise GateRefused('max_rounds must be an integer from 1 to 100')
    pinned = snapshot(store, ws, plan_id, reference_id, render_id, timeline_id)
    number = 1
    if previous_job_id:
        previous = R.get_job(store, ws, previous_job_id)
        if previous['kind'] != KIND or previous['status'] != R.COMPLETED:
            raise GateRefused('Previous review must be a completed edit-style review')
        prior = previous['input']
        if previous.get('output', {}).get('status') == 'pass':
            raise GateRefused('This render already passed; do not keep grading to seek a higher score')
        assert_current(store, ws, prior['snapshot'])
        if (pinned['role_ids']['edit_plan'] != prior['snapshot']['role_ids']['edit_plan'] or
            pinned['role_ids']['reference'] != prior['snapshot']['role_ids']['reference'] or
            pinned['rubric_hash'] != prior['snapshot']['rubric_hash']):
            raise GateRefused('Revision cannot change the acceptance plan, style reference or rubric')
        old_render = prior['snapshot']['role_ids']['render']
        old_timeline = prior['snapshot']['role_ids']['timeline']
        if (pinned['hashes'][render_id] == prior['snapshot']['hashes'][old_render] or
            pinned['timeline_execution_hash'] == prior['snapshot']['timeline_execution_hash']):
            raise GateRefused('Revision needs changed timeline content and a newly rendered video; no score fishing')
        number = prior['round'] + 1
        max_rounds = prior['max_rounds']
        if number > max_rounds:
            raise GateRefused('Edit-style round limit reached without passing; result remains unfinished')
    # One durable root per acceptance target and one child per round. Atomic on
    # both stores; new IDs/remuxes/metadata cannot reset the series or buy grades.
    identity = [ws, previous_job_id] if previous_job_id else [ws,
        pinned['hashes'][plan_id],pinned['hashes'][reference_id],pinned['rubric_hash']]
    jid = 'job_style_' + E.fingerprint(identity)[:32]
    now = time.time()
    candidate = {'id':jid,'workspace_id':ws,'kind':KIND,'status':R.QUEUED,
        'input':{'snapshot':pinned,'round':number,'max_rounds':max_rounds,
                 'creator_id':creator_id,'previous_job_id':previous_job_id},
        'provider':'openai','parent_id':previous_job_id,'created':now,'updated':now}
    existing = store.put_once('job',candidate)
    if existing['input']['snapshot'] != pinned:
        raise GateRefused('This acceptance target already has a review; continue its latest round instead of starting another grade')
    return existing


def plan_timeline_mismatches(plan, timeline):
    """Check expected execution against the actual Project, not an editor's claim."""
    mismatches = []
    entries = [(t,c) for t in timeline['tracks'] for c in t['clips']]
    clips = {c['id']: c for _,c in entries}
    tracks = {c['id']:t for t,c in entries}
    if len(clips) != len(entries) or len({t['id'] for t in timeline['tracks']}) != len(timeline['tracks']):
        mismatches.append('Duplicate clip or track ids in executed timeline')
    if timeline.get('tickRate') != 6000:
        mismatches.append('Executed timeline has the wrong tick rate')
    if any(t.get('captions') for t in timeline.get('captions',[])):
        mismatches.append('Unplanned caption tracks in executed timeline')
    tick = lambda value: round(value * 6000)
    tolerance = max(1, round(6000 / plan['fps']))
    if any(timeline[k] != plan[k] for k in ('width', 'height', 'fps')):
        mismatches.append('Project delivery dimensions/FPS differ from plan')
    if abs(timeline['duration'] - tick(plan['duration_s'])) > tolerance:
        mismatches.append('Project duration differs from plan')
    expected_ids = {p['id'] for p in plan['clips']}
    if set(clips) != expected_ids:
        mismatches.append('Executed clip set differs from the acceptance plan')
    for p in plan['clips']:
        actual = clips.get(p['id'])
        if actual is None:
            continue
        track = tracks[p['id']]
        if track['id'] != p['track_id'] or track['kind'] != p['kind'] or track.get('muted'):
            mismatches.append(f"{p['id']}: wrong or muted parent track")
        defaults = {'reverse':False,'transform':{'x':0,'y':0,'scale':1,'rotation':0,'opacity':1,'anchor':{'x':.5,'y':.5}},
                    'crop':{'left':0,'top':0,'right':0,'bottom':0},'blend':'normal','effects':[]}
        for field,expected in defaults.items():
            if actual.get(field) != expected:
                mismatches.append(f"{p['id']}.{field} is an unplanned execution change")
        for field in ('freeze','mask','chroma','text','transitionIn'):
            if field in actual:
                mismatches.append(f"{p['id']}.{field} is not in the acceptance plan")
        for field, expected in {'assetId':p['asset_id'], 'kind':p['kind'], 'speed':p['speed']}.items():
            if actual.get(field) != expected:
                mismatches.append(f"{p['id']}.{field} differs from plan")
        for field, expected in {'start':p['timeline_start_s'], 'duration':p['timeline_end_s']-p['timeline_start_s'],
                                'in':p['source_in_s'], 'out':p['source_out_s']}.items():
            if abs(actual[field] - tick(expected)) > tolerance:
                mismatches.append(f"{p['id']}.{field} differs by more than one output frame")
        keys = {a['property']:[{'at':tick(k['at_s']), 'value':k['value'], 'easing':k['easing']}
                              for k in a['keyframes']] for a in p['animations']}
        if actual.get('keyframes', {}) != keys:
            mismatches.append(f"{p['id']}.keyframes differ from planned motion")
        tr = p['transition_out']
        expected = {'kind':tr['kind'], 'duration':tick(tr['duration_s'])} if tr else None
        if actual.get('transitionOut') != expected:
            mismatches.append(f"{p['id']}.transitionOut differs from plan")
        audio = p['audio']
        expected = {'gain':audio['gain_db'], 'fadeIn':tick(audio['fade_in_s']), 'fadeOut':tick(audio['fade_out_s'])} if audio else None
        if actual.get('audio') != expected:
            mismatches.append(f"{p['id']}.audio differs from plan")
    return mismatches


def probe_delivery(video, plan):
    from fractions import Fraction
    result = shell.run([settings.ffprobe,'-v','error','-select_streams','v:0',
        '-show_entries','stream=width,height,avg_frame_rate,r_frame_rate',
        '-of','json',video],timeout=60,check=True)
    streams = json.loads(result.stdout).get('streams',[])
    if not streams:
        raise ProviderError('Rendered video has no decodable video stream')
    stream = streams[0]
    try:
        fps = float(Fraction(stream.get('avg_frame_rate','0/1')))
    except (ValueError,ZeroDivisionError):
        fps = 0
    mismatches = []
    if stream.get('width') != plan['width'] or stream.get('height') != plan['height']:
        mismatches.append('Actual rendered dimensions do not match acceptance plan')
    if abs(fps-plan['fps']) > .001:
        mismatches.append('Actual rendered frame rate does not match acceptance plan')
    return {'width':stream.get('width'),'height':stream.get('height'),'fps':fps},mismatches


def event_frames(video, role, times, work):
    """Native decoded frames bracketing each requested event; no time resampling."""
    probe = shell.run([settings.ffprobe, '-v','error','-select_streams','v:0','-show_frames',
        '-show_entries','frame=best_effort_timestamp_time','-of','json',video], timeout=900, check=True)
    rows = json.loads(probe.stdout).get('frames', [])
    if not rows or any('best_effort_timestamp_time' not in r for r in rows):
        raise ProviderError('Native frame timestamps are unavailable')
    origin = float(rows[0]['best_effort_timestamp_time'])
    stamps = [float(r['best_effort_timestamp_time'])-origin for r in rows]
    indices = set()
    for t in times:
        index = min(range(len(stamps)), key=lambda i: abs(stamps[i]-t))
        indices.update(i for i in (index-1,index,index+1) if 0 <= i < len(stamps))
    indices = sorted(indices)
    if len(indices) > MAX_EVENT_FRAMES:
        raise ProviderError(f'{role} needs {len(indices)} event frames; exceeds {MAX_EVENT_FRAMES}. Split the review; no frames discarded.')
    expression = '+'.join(f'eq(n,{i})' for i in indices)
    folder = os.path.join(work, role); os.makedirs(folder)
    shell.run([settings.ffmpeg,'-y','-i',video,'-vf',f"select='{expression}',scale=960:-2",
               '-vsync','0','-q:v','2',os.path.join(folder,'%05d.jpg')], timeout=900, check=True)
    paths = sorted(Path(folder).glob('*.jpg'))
    if len(paths) != len(indices):
        raise ProviderError('Frame extraction count does not match native timestamp ledger')
    return [{'id':f'{role}_frame_{index}', 'role':role, 'frame_index':index,
             't':stamps[index], 'path':str(path)} for index,path in zip(indices,paths)]


def evaluate(packet, comparison, grading, *, reviewer_id, creator_id):
    """Astra assigns scores; code verifies coverage, citations, gates and repairs."""
    rubric = packet['rubric']; roles = packet['role_ids']; plan = packet['plan']
    missing, blockers = [], []
    expected_criteria = {c['id'] for c in rubric['criteria']}
    clip_ids = {c['id'] for c in plan['clips']}
    frames = {f['id']: f for f in packet['frames']}
    if not all(comparison.get(k) is True for k in ('reference_watched','render_watched','audio_compared')):
        missing.append('Actual reference, render and audio comparison must all be complete')
    if set(comparison.get('inspected_plan_clip_ids', [])) != clip_ids:
        missing.append('Perception must inspect every plan clip')
    missing.extend(comparison.get('unresolved', []))
    observations = {}
    for obs in comparison.get('observations', []):
        oid = obs['id']
        if not oid or oid in observations or obs['criterion_id'] not in expected_criteria:
            raise GateRefused('Invalid/duplicate observation identity or rubric criterion')
        if (not obs['plan_clip_ids'] or not set(obs['plan_clip_ids']) <= clip_ids or
            not obs['frame_ids'] or not set(obs['frame_ids']) <= set(frames)):
            raise GateRefused('Observation cites unknown or missing plan/frame evidence')
        for role in ('reference','render'):
            start,end = obs[role+'_start_s'],obs[role+'_end_s']
            if not all(math.isfinite(v) for v in (start,end)) or not 0 <= start <= end <= packet['durations'][role]:
                raise GateRefused('Observation timecode is outside the actual source')
            matching = [frames[fid] for fid in obs['frame_ids'] if frames[fid]['role'] == role]
            if not matching or not any(start-.1 <= f['t'] <= end+.1 for f in matching):
                raise GateRefused('Observation requires paired reference/render frames at the cited interval')
        if obs['confidence'] < .8 or obs['needs_frame_review']:
            missing.append(f'{oid}: insufficient confidence or temporal evidence')
        if obs['severity'] in ('major','critical'):
            blockers.append(f"{oid}: {obs['severity']} mismatch: {obs['difference']}")
        observations[oid] = obs
    if {o['criterion_id'] for o in observations.values()} != expected_criteria:
        missing.append('Paired source observations are required for every rubric criterion')
    for cid in ('reference_rhythm','transitions_motion','graphics_composition'):
        cited = [frames[fid] for o in observations.values() if o['criterion_id']==cid for fid in o['frame_ids']]
        for role in ('reference','render'):
            duration = packet['durations'][role]
            for target in (0,duration/2,duration):
                if not any(f['role']==role and abs(f['t']-target)<=max(.1,duration*.05) for f in cited):
                    missing.append(f'{cid}: {role} opening/middle/ending style evidence missing')
    # Self-reported inspected ids are insufficient. Require actual per-clip
    # source/render frames across the selected ranges, including ending holds.
    tolerance = 1.5 / plan['fps']
    for clip in plan['clips']:
        evidence = [o for o in observations.values() if o['criterion_id']=='plan_execution'
                    and o['plan_clip_ids']==[clip['id']]
                    and o['render_start_s'] <= clip['timeline_start_s']+tolerance
                    and o['render_end_s'] >= clip['timeline_end_s']-tolerance]
        complete = False
        for obs in evidence:
            cited = [frames[fid] for fid in obs['frame_ids']]
            render_times = (clip['timeline_start_s'],(clip['timeline_start_s']+clip['timeline_end_s'])/2,clip['timeline_end_s'])
            source_times = (clip['source_in_s'],(clip['source_in_s']+clip['source_out_s'])/2,clip['source_out_s'])
            if (all(any(f['role']=='render' and abs(f['t']-t)<=tolerance for f in cited) for t in render_times) and
                all(any(f.get('source_asset_id')==clip['asset_id'] and f['role'].startswith('source_') and
                        abs(f['t']-t)<=tolerance for f in cited) for t in source_times)):
                complete = True
        if not complete:
            missing.append(f"{clip['id']}: beginning/middle/end render-to-selected-source evidence missing")
    criteria = {}
    for assessment in grading['assessments']:
        cid = assessment['criterion_id']
        if cid in criteria or cid not in expected_criteria:
            raise GateRefused('Astra returned duplicate/unknown rubric criteria')
        selected = [observations.get(oid) for oid in assessment['evidence_ids']]
        if not selected or any(o is None or o['criterion_id'] != cid for o in selected):
            raise GateRefused('Astra must cite real observations for this criterion')
        if cid=='plan_execution' and {p for o in selected for p in o['plan_clip_ids']} != clip_ids:
            missing.append('Astra plan-execution grade must cite every clip')
        evidence = []
        for obs in selected:
            for role in ('reference','render','edit_plan','timeline'):
                locator = (f"{obs[role+'_start_s']}..{obs[role+'_end_s']}s" if role in ('reference','render')
                           else 'clips:'+','.join(obs['plan_clip_ids']))
                evidence.append({'kind':role,'path':roles[role], 'locator':locator,
                    'observation':f"{obs['id']}: expected {obs['expected']}; observed {obs['observed']}; {obs['difference']}"})
        criteria[cid] = {'score':assessment['score'], 'critical_failure':assessment['critical_failure'],
                        'feedback':assessment['rationale'], 'evidence':evidence}
    review = {'rubric_id':rubric['id'],'rubric_version':rubric['version'],
        'artifact_hash':packet['render_hash'],'reviewer_id':reviewer_id,'criteria':criteria}
    result = evaluate_review(rubric,review,artifact_hash=packet['render_hash'],artifact_kind='render',creator_id=creator_id)
    blockers.extend(packet['timeline_mismatches'])
    missing.extend(grading['unresolved'])
    for repair in grading['repairs']:
        if (repair['criterion_id'] not in expected_criteria or not repair['evidence_ids'] or
            not set(repair['evidence_ids']) <= set(observations) or not repair['clip_ids'] or
            not set(repair['clip_ids']) <= clip_ids or
            not 0 <= repair['render_start_s'] <= repair['render_end_s'] <= packet['durations']['render'] or
            not repair['action'].strip() or not repair['verification'].strip()):
            raise GateRefused('Astra repair lacks valid timecoded source evidence and verification')
        if any(observations[oid]['criterion_id'] != repair['criterion_id'] or
               not set(repair['clip_ids']) & set(observations[oid]['plan_clip_ids'])
               for oid in repair['evidence_ids']):
            raise GateRefused('Repair evidence must support its criterion and selected clips')
    if (result['status'] != 'pass' or blockers) and not grading['repairs']:
        missing.append('A failing review requires actionable editor repair instructions')
    result['blockers'].extend(blockers); result['missing_evidence'].extend(missing)
    result['status'] = 'revise' if result['blockers'] else 'needs_evidence' if result['missing_evidence'] else 'pass'
    result.update(required_score=8, score_max=10, repairs=grading['repairs'],
                  delivery_ready=result['status']=='pass',
                  next_action='deliver_reviewed_render' if result['status']=='pass' else 'edit_in_internal_editor_then_render_and_resubmit')
    return result


def run_revision_loop(initial, *, review, edit_and_render=None, max_rounds=8):
    """Host adapter: executes review -> internal-editor repair/render -> fresh review.

    The host supplies its actual editor/render adapter. Missing support, unchanged
    evidence, or limits stop unfinished. Never replace the internal editor with a
    rendering framework or label a timeline document a rendered video.
    """
    if type(max_rounds) is not int or max_rounds < 1:
        raise ValueError('max_rounds must be positive')
    current = initial; history = []; seen = set()
    for _ in range(max_rounds):
        signature = (current['render_hash'], current['timeline_hash'])
        if signature in seen:
            return {'status':'no_progress','delivery_ready':False,'history':history}
        seen.add(signature)
        result = review(current); history.append(result)
        if result['status'] == 'pass' and result.get('delivery_ready') and result.get('score',0) >= 8:
            return {'status':'pass','delivery_ready':True,'final':current,'history':history}
        if edit_and_render is None:
            return {'status':'needs_editor_adapter','delivery_ready':False,'history':history}
        if len(history) >= max_rounds:
            break
        repaired = edit_and_render(current,result)
        if any(repaired.get(k) != initial.get(k) for k in ('plan_hash','reference_hash','rubric_hash')):
            raise GateRefused('Editor adapter changed the acceptance targets')
        if repaired['render_hash'] == current['render_hash'] or repaired['timeline_hash'] == current['timeline_hash']:
            return {'status':'no_progress','delivery_ready':False,'history':history}
        current = repaired
    return {'status':'round_limit','delivery_ready':False,'history':history}


def run_grade(store: Store, job: dict):
    from adengine.engines.credentials import get_key
    import shutil
    ws = job['workspace_id']; inp = job['input']; pinned = inp['snapshot']; roles = pinned['role_ids']
    assert_current(store, ws, pinned)
    gemini_key = get_key('gemini', ws, store)
    astra_key = get_key('openai', ws, store)
    envelope = read_plan(store, ws, roles['edit_plan']); plan = envelope['plan']
    timeline = read_json(store, ws, roles['timeline'])
    reference = R.asset_path(store, R.get_asset(store, ws, roles['reference']))
    render = R.asset_path(store, R.get_asset(store, ws, roles['render']))
    durations = {'reference':watch.probe_duration(reference),'render':watch.probe_duration(render)}
    if any(not math.isfinite(d) or d <= 0 for d in durations.values()):
        raise ProviderError('Both reference and render must be decodable videos of positive duration')
    render_events = {0,durations['render']/2,durations['render']}
    for clip in plan['clips']:
        render_events.update((clip['timeline_start_s'],clip['timeline_end_s'],
                              (clip['timeline_start_s']+clip['timeline_end_s'])/2))
        for animation in clip['animations']:
            render_events.update(clip['timeline_start_s']+k['at_s'] for k in animation['keyframes'])
        if clip['transition_out']:
            render_events.add(clip['timeline_end_s']-clip['transition_out']['duration_s'])
    reference_events = set(watch.detect_scenes(reference)) | {0,durations['reference']/2,durations['reference']}
    work = shell.workdir('edit-style-review')
    try:
        frames = event_frames(reference,'reference',reference_events,work) + event_frames(render,'render',render_events,work)
        sources = {}; source_roles = {}
        mime_types = {'REFERENCE':R.get_asset(store,ws,roles['reference'])['mime'],
                      'RENDER':R.get_asset(store,ws,roles['render'])['mime']}
        for aid in {c['asset_id'] for c in plan['clips']}:
            source = R.get_asset(store,ws,aid)
            source_path = R.asset_path(store,source)
            role = 'source_'+aid; source_roles[role] = aid
            events = {t for c in plan['clips'] if c['asset_id']==aid
                      for t in (c['source_in_s'],(c['source_in_s']+c['source_out_s'])/2,c['source_out_s'])}
            source_frames = event_frames(source_path,role,events,work)
            for f in source_frames:
                f['source_asset_id'] = aid
            frames.extend(source_frames)
            if source_path != reference:
                sources[aid] = source_path
                mime_types['SOURCE_'+aid] = source['mime']
        public_frames = []
        for frame in frames:
            source_id = source_roles.get(frame['role']) or roles[frame['role']]
            saved = R.put_file_asset(store,ws,frame['path'],f"jobs/{job['id']}/{frame['id']}.jpg",
                kind='frame',mime='image/jpeg',job_id=job['id'],
                meta={'source_asset_id':source_id, 'source_sha256':pinned['hashes'][source_id],
                      'frame_index':frame['frame_index'],'t':frame['t']})
            public_frames.append({k:v for k,v in frame.items() if k!='path'} | {'asset_id':saved['id'],'url':saved['url']})
        packet = {'role_ids':roles,'hashes':pinned['hashes'],'rubric':pinned['rubric'],
            'rubric_hash':pinned['rubric_hash'],'plan':plan,'timeline':timeline,
            'render_hash':pinned['hashes'][roles['render']], 'durations':durations,
            'frames':public_frames,'timeline_mismatches':plan_timeline_mismatches(plan,timeline),
            'coverage_method':'full videos plus native frames bracketing plan/cut events; not exhaustive every-frame coverage'}
        if abs(durations['render']-plan['duration_s']) > 1/plan['fps']:
            packet['timeline_mismatches'].append('Actual render duration differs from plan by more than one output frame')
        delivery,delivery_mismatches = probe_delivery(render,plan)
        packet['actual_delivery'] = delivery
        packet['timeline_mismatches'].extend(delivery_mismatches)
        perception = edit_grader.compare_media(reference,render,packet,frames,gemini_key,
                                               source_paths=sources,mime_types=mime_types)
        packet['perception'] = perception
        # Persist the exact evidence package before the independent grader sees it.
        evidence = R.put_bytes_asset(store,ws,json.dumps(packet,allow_nan=False).encode(),
            f"jobs/{job['id']}/evidence.json",kind='edit_style_evidence',mime='application/json',job_id=job['id'])
        grading = edit_grader.grade_comparison(packet,frames,astra_key)
        reviewer_id = 'astra:' + grading['response_id']
        result = evaluate(packet,perception['comparison'],grading['grade'],reviewer_id=reviewer_id,creator_id=inp['creator_id'])
        assert_current(store,ws,pinned)
        result.update(review_job_id=job['id'],round=inp['round'],
            reference_asset_id=roles['reference'],render_asset_id=roles['render'],
            edit_plan_asset_id=roles['edit_plan'],timeline_asset_id=roles['timeline'],
            reviewer_id=reviewer_id,grader_model=grading['model'],reasoning_effort=grading['reasoning_effort'],
            perception_model=perception['model'],evidence_asset_id=evidence['id'],
            evidence_hash=E.fingerprint(packet),rubric_hash=pinned['rubric_hash'],hashes=pinned['hashes'])
        if result['status'] != 'pass' and inp['round'] >= inp['max_rounds']:
            result['next_action'] = 'round_limit_unfinished'
        report = R.put_bytes_asset(store,ws,json.dumps({'result':result,'grading':grading},allow_nan=False).encode(),
            f"jobs/{job['id']}/report.json",kind='edit_style_review',mime='application/json',job_id=job['id'])
        result['review_asset_id'] = report['id']
        for provider,response in (('gemini',perception),('openai',grading)):
            usage = response.get('usage') or {}
            count = usage.get('total_tokens',usage.get('total_token_count'))
            R.record_cost(store,ws,job['id'],provider,count,'tokens',None,
                          note='Edit-style review; usage recorded, USD not inferred without a configured rate')
        return result
    finally:
        shutil.rmtree(work,ignore_errors=True)


def get_status(store, ws, job_id):
    job = R.get_job(store,ws,job_id)
    if job['kind'] != KIND:
        raise GateRefused('Job is not an edit-style review')
    assert_current(store,ws,job['input']['snapshot'])
    children = store.find('job',ws,kind=KIND,parent_id=job_id)
    if children:
        return {'status':'superseded','delivery_ready':False,'next_review_job_id':children[0]['id']}
    if job['status'] != R.COMPLETED:
        return {'status':job['status'],'delivery_ready':False,'review_job_id':job_id,'error':job.get('error')}
    return job['output']
