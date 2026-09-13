"""Strict style gates, real provider request shape and fail/edit/rerender/pass protocol."""
import copy
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from adengine.core.auth import AuthContext, set_auth_context
from adengine.core.errors import GateRefused, NotFound, ProviderError
from adengine.core.store import LocalStore
from adengine.engines import edit_grader as G, credentials
from adengine.gen import edit_review as S, registry as R, server
from adengine.quality import load_rubric, evaluate_review
from adengine.workers import run

ROOT = Path(__file__).resolve().parents[3]


def comparison(plan, rubric):
    result = {'reference_watched':True,'render_watched':True,'audio_compared':True,
        'inspected_plan_clip_ids':[c['id'] for c in plan['clips']], 'unresolved':[],
        'observations':[{'id':c['id']+'-obs','criterion_id':c['id'],
            'reference_start_s':0,'reference_end_s':12,'render_start_s':0,'render_end_s':4,
            'plan_clip_ids':[p['id'] for p in plan['clips']],
            'frame_ids':['reference_frame_0','render_frame_0','reference_at_0','reference_at_6','reference_at_12','render_at_0','render_at_2','render_at_4'],
            'expected':'same timing and style','observed':'matched timing and style','difference':'none',
            'confidence':.98,'severity':'none','needs_frame_review':False} for c in rubric['criteria']]}
    base=next(o for o in result['observations'] if o['criterion_id']=='plan_execution')
    result['observations']=[o for o in result['observations'] if o['criterion_id']!='plan_execution']
    for clip in plan['clips']:
        frames=['reference_frame_0']
        for t in (clip['timeline_start_s'],(clip['timeline_start_s']+clip['timeline_end_s'])/2,clip['timeline_end_s']):
            frames.append(f'render_at_{t:g}')
        for t in (clip['source_in_s'],(clip['source_in_s']+clip['source_out_s'])/2,clip['source_out_s']):
            frames.append(f"source_{clip['asset_id']}_at_{t:g}")
        result['observations'].append({**base,'id':'plan_execution-'+clip['id'],
            'plan_clip_ids':[clip['id']], 'frame_ids':frames,
            'render_start_s':clip['timeline_start_s'],'render_end_s':clip['timeline_end_s']})
    return result


def source_frames(plan):
    frames=[{'id':r+'_frame_0','role':r,'t':0,'frame_index':0} for r in ('reference','render')]
    frames += [{'id':f'reference_at_{t:g}','role':'reference','t':t,'frame_index':round(t*30)} for t in (0,6,12)]
    for clip in plan['clips']:
        for role,start,end in [('render',clip['timeline_start_s'],clip['timeline_end_s']),
                              ('source_'+clip['asset_id'],clip['source_in_s'],clip['source_out_s'])]:
            for t in (start,(start+end)/2,end):
                frames.append({'id':f'{role}_at_{t:g}','role':role,'t':t,'frame_index':round(t*30),
                    **({'source_asset_id':clip['asset_id']} if role.startswith('source_') else {})})
    return list({f['id']:f for f in frames}.values())



def grade(rubric, score=8):
    return {'assessments':[{'criterion_id':c['id'],'score':score,'critical_failure':False,
        'evidence_ids':(['plan_execution-'+cid for cid in ('opening','detail','sound')] if c['id']=='plan_execution' else [c['id']+'-obs']),'rationale':'Paired reference and rendered evidence supports the score'}
        for c in rubric['criteria']], 'repairs':[], 'unresolved':[]}


def repair(rubric):
    cid=rubric['criteria'][0]['id']
    return {'criterion_id':cid,'evidence_ids':[cid+'-obs'],'clip_ids':['opening'],
            'render_start_s':0,'render_end_s':2,'action':'Restore the planned opening hold',
            'verification':'Inspect the first cut against reference and plan'}


@pytest.fixture
def packet():
    handoff=json.loads((ROOT/'packages/timeline/test/fixtures/edit-plan.json').read_text())
    return {'rubric':load_rubric('edit_style'),'role_ids':{k:'asset_'+k for k in ('reference','render','edit_plan','timeline')},
        'plan':handoff['plan'],'durations':{'reference':12,'render':4},'render_hash':'a'*64,
        'frames':source_frames(handoff['plan']),
        'timeline_mismatches':[]}


def evaluate(packet, obs=None, report=None):
    return S.evaluate(packet,obs or comparison(packet['plan'],packet['rubric']),
        report or grade(packet['rubric']),reviewer_id='astra:resp_test',creator_id='editor')


def test_exact_8_passes(packet):
    result=evaluate(packet)
    assert result['score']==8 and result['status']=='pass' and result['delivery_ready']


def test_below_8_and_core_floors_fail(packet):
    report=grade(packet['rubric'],10); report['assessments'][0]['score']=7
    report['repairs']=[repair(packet['rubric'])]
    result=evaluate(packet,report=report)
    assert result['score']>8 and result['status']=='revise' and not result['delivery_ready']
    result=evaluate(packet,report=grade(packet['rubric'],7))
    assert result['score']==7 and result['status']=='revise'


def test_unrounded_score_is_used_for_gate():
    rubric=load_rubric('edit_style')
    rubric['criteria']=copy.deepcopy(rubric['criteria'][:2])
    rubric['criteria'][0].update(weight=.4,minimum_score=0)
    rubric['criteria'][1].update(weight=99.6,minimum_score=0)
    criteria={c['id']:{'score':7 if i==0 else 8,'critical_failure':False,'feedback':'rationale',
        'evidence':[{'kind':k,'path':k,'locator':'0s','observation':'observed'} for k in c['required_evidence']]}
        for i,c in enumerate(rubric['criteria'])}
    result=evaluate_review(rubric,{'rubric_id':'edit_style','rubric_version':'1.0.0','artifact_hash':'a'*64,
        'reviewer_id':'astra','criteria':criteria},artifact_hash='a'*64,artifact_kind='render',creator_id='editor')
    assert result['score']==8.0 and result['status']=='revise'


@pytest.mark.parametrize('failure',['reference','render','audio','coverage','confidence','temporal','critical','major','timeline','unknown_frame','wrong_time','unknown_criterion','wrong_evidence'])
def test_no_false_pass_from_missing_or_wrong_evidence(packet,failure):
    obs=comparison(packet['plan'],packet['rubric']); report=grade(packet['rubric'],10)
    if failure in ('reference','render'): obs[failure+'_watched']=False
    if failure=='audio': obs['audio_compared']=False
    if failure=='coverage': obs['inspected_plan_clip_ids'].pop()
    if failure=='confidence': obs['observations'][0]['confidence']=.5
    if failure=='temporal': obs['observations'][0]['needs_frame_review']=True
    if failure in ('critical','major'): obs['observations'][0]['severity']=failure
    if failure=='timeline': packet['timeline_mismatches']=['Wrong source trim']
    if failure=='unknown_frame': obs['observations'][0]['frame_ids']=['invented']
    if failure=='wrong_time': obs['observations'][0]['render_end_s']=20
    if failure=='unknown_criterion': report['assessments'][0]['criterion_id']='invented'
    if failure=='wrong_evidence': report['assessments'][0]['evidence_ids']=['made-up']
    try:
        result=evaluate(packet,obs,report)
        assert result['status']!='pass' and not result['delivery_ready']
    except GateRefused:
        assert failure in ('unknown_frame','wrong_time','unknown_criterion','wrong_evidence')


def test_actual_timeline_comparison_catches_omitted_effect_and_wrong_trim(packet):
    timeline=json.loads((ROOT/'packages/timeline/test/fixtures/edit-timeline.json').read_text())
    assert S.plan_timeline_mismatches(packet['plan'],timeline)==[]
    clip=next(c for t in timeline['tracks'] for c in t['clips'] if c['id']=='opening')
    clip.pop('transitionOut'); clip['in']=18000; clip['keyframes']={}
    failures=S.plan_timeline_mismatches(packet['plan'],timeline)
    assert any('transitionOut' in f for f in failures)
    assert any('.in ' in f for f in failures) and any('keyframes' in f for f in failures)


@pytest.fixture
def env(tmp_path,monkeypatch):
    store=LocalStore(str(tmp_path/'store')); ws='ws_style'
    set_auth_context(AuthContext(ws,'editor','editor'))
    monkeypatch.setattr(server,'_store',lambda:store); monkeypatch.setattr(server,'_ws',lambda:ws)
    fixture=json.loads((ROOT/'packages/timeline/test/fixtures/edit-plan.json').read_text())
    source=R.put_bytes_asset(store,ws,b'reference','reference.mp4','video','video/mp4')
    ref=R.create_reference(store,ws,source['id'],asset_id=source['id'])
    manifest=fixture['analysis']['ref_a']; manifest['video_asset_id']=source['id']
    R.update_reference(store,ws,ref['id'],manifest=manifest,status='watched')
    for clip in fixture['plan']['clips']:
        clip['asset_id']=source['id']; clip['evidence'][0]['reference_id']=ref['id']
    plan=server.save_edit_plan(fixture['plan'],[ref['id']])
    timeline=json.loads((ROOT/'packages/timeline/test/fixtures/edit-timeline.json').read_text().replace('asset_a',source['id']))
    tl=R.put_bytes_asset(store,ws,json.dumps(timeline).encode(),'timeline.json','timeline','application/json')
    render=R.put_bytes_asset(store,ws,b'render1','render1.mp4','video','video/mp4')
    yield store,ws,{'edit_plan_asset_id':plan['asset_id'],'reference_asset_id':source['id'],
        'render_asset_id':render['id'],'timeline_asset_id':tl['id']},timeline
    set_auth_context(AuthContext('ws_test','dev','owner'))


def mock_providers(monkeypatch,tmp_path,score=8):
    monkeypatch.setattr(S.watch,'probe_duration',lambda p:12 if p.endswith('reference.mp4') else 4)
    monkeypatch.setattr(S.watch,'detect_scenes',lambda p:[0,2])
    def event_frames(video,role,times,work):
        path=tmp_path/(role+'.jpg'); path.write_bytes(b'jpg')
        return [{'id':f'{role}_at_{t:g}','role':role,'t':t,'frame_index':round(t*30),'path':str(path)} for t in sorted(times)] + ([{'id':role+'_frame_0','role':role,'t':0,'frame_index':0,'path':str(path)}] if role in ('reference','render') else [])
    monkeypatch.setattr(S,'event_frames',event_frames)
    monkeypatch.setattr(S,'probe_delivery',lambda video,plan:({'width':1080,'height':1920,'fps':30},[]))
    monkeypatch.setattr(G,'compare_media',lambda ref,render,packet,frames,key,**kw:{'model':'gemini-3.8-flash',
        'comparison':comparison(packet['plan'],packet['rubric']),'usage':{'total_token_count':20}})
    def grading(packet,frames,key):
        report=grade(packet['rubric'],score)
        if score<8: report['repairs']=[repair(packet['rubric'])]
        return {'model':'gpt-6-astra','response_id':'resp_test','reasoning_effort':'high','grade':report,'usage':{'total_tokens':30}}
    monkeypatch.setattr(G,'grade_comparison',grading)


def test_queue_worker_pins_actual_inputs_and_persists_authoritative_grade(env,monkeypatch,tmp_path):
    store,ws,inputs,_=env
    credentials.save_key('gemini','fake',ws,store);credentials.save_key('openai','fake',ws,store)
    mock_providers(monkeypatch,tmp_path)
    submitted=server.start_edit_style_review(**inputs)
    assert submitted==server.start_edit_style_review(**inputs)
    job=run.run_once(store,[S.KIND]); assert job['status']=='completed',job.get('error')
    result=server.get_edit_style_review(submitted['review_job_id'])
    assert result['score']==8 and result['delivery_ready'] and result['grader_model']=='gpt-6-astra'
    assert R.get_asset(store,ws,result['evidence_asset_id'])['kind']=='edit_style_evidence'
    with pytest.raises(NotFound): S.get_status(store,'other',job['id'])
    asset=R.get_asset(store,ws,inputs['render_asset_id']);store.put_blob(ws,asset['storage_key'],b'changed')
    with pytest.raises(GateRefused,match='changed'): server.get_edit_style_review(job['id'])


def test_fail_revision_new_render_fresh_grade_pass(env,monkeypatch,tmp_path):
    store,ws,inputs,timeline=env
    credentials.save_key('gemini','fake',ws,store);credentials.save_key('openai','fake',ws,store)
    mock_providers(monkeypatch,tmp_path,score=7)
    broken=copy.deepcopy(timeline); broken['tracks'][0]['clips'][0]['keyframes']={}
    stored=R.get_asset(store,ws,inputs['timeline_asset_id'])
    store.put_blob(ws,stored['storage_key'],json.dumps(broken).encode())
    first=server.start_edit_style_review(**inputs);job=run.run_once(store,[S.KIND])
    assert job['output']['status']=='revise'
    with pytest.raises(GateRefused,match='newly rendered'):
        server.start_edit_style_review(**inputs,previous_review_job_id=first['review_job_id'])
    render=R.put_bytes_asset(store,ws,b'render2','render2.mp4','video','video/mp4')
    timeline['version']+=1
    timeline['markers'][0]['body']='Repair verification added'
    tl=R.put_bytes_asset(store,ws,json.dumps(timeline).encode(),'timeline2.json','timeline','application/json')
    new={**inputs,'render_asset_id':render['id'],'timeline_asset_id':tl['id']}
    second=server.start_edit_style_review(**new,previous_review_job_id=first['review_job_id'])
    assert server.get_edit_style_review(first['review_job_id'])['status']=='superseded'
    mock_providers(monkeypatch,tmp_path,score=8)
    job=run.run_once(store,[S.KIND])
    assert job['id']==second['review_job_id'] and job['output']['delivery_ready']


def test_adapter_loop_edits_rerenders_and_regrades():
    initial={'render_hash':'r1','timeline_hash':'t1','plan_hash':'p','reference_hash':'ref','rubric_hash':'rubric'}
    calls=[]
    def review(item):
        calls.append(('review',item['render_hash']))
        passed=item['render_hash']=='r2'
        return {'status':'pass' if passed else 'revise','delivery_ready':passed,'score':8 if passed else 7,'repairs':['fix']}
    def editor(item,result):
        calls.append(('edit_and_render',item['render_hash']))
        return {**item,'render_hash':'r2','timeline_hash':'t2'}
    out=S.run_revision_loop(initial,review=review,edit_and_render=editor)
    assert out['status']=='pass' and calls==[('review','r1'),('edit_and_render','r1'),('review','r2')]
    assert S.run_revision_loop(initial,review=review)['status']=='needs_editor_adapter'
    assert S.run_revision_loop(initial,review=review,edit_and_render=lambda x,y:x)['status']=='no_progress'
    assert S.run_revision_loop(initial,review=review,edit_and_render=editor,max_rounds=1)['status']=='round_limit'
    with pytest.raises(GateRefused):
        S.run_revision_loop(initial,review=review,edit_and_render=lambda x,y:{**editor(x,y),'plan_hash':'changed'})


def test_astra_request_is_pinned_independent_and_structured(packet,tmp_path):
    path=tmp_path/'frame.jpg';path.write_bytes(b'jpg');sent=[]
    def post(url,**kwargs):
        sent.append(kwargs['json'])
        return SimpleNamespace(status_code=200,json=lambda:{'id':'resp_real_transport','status':'completed',
            'model':'gpt-6-astra','output':[{'type':'message','content':[{'type':'output_text','text':json.dumps(grade(packet['rubric']))}]}]})
    out=G.grade_comparison(packet,[{'id':'f','role':'render','frame_index':0,'t':0,'path':str(path)}],'fake',post=post)
    request=sent[0]
    assert request['model']=='gpt-6-astra' and request['reasoning']=={'effort':'high'}
    assert request['store'] is False and 'previous_response_id' not in request
    assert request['text']['format']['strict'] is True and 'temperature' not in request
    assert out['response_id']=='resp_real_transport'
    assert any(p['type']=='input_image' for p in request['input'][0]['content'])


@pytest.mark.parametrize('status,model',[('incomplete','gpt-6-astra'),('completed','other-model')])
def test_incomplete_or_non_astra_provider_cannot_grade(packet,status,model):
    def post(*a,**kw):return SimpleNamespace(status_code=200,json=lambda:{'id':'response','model':model,'status':status})
    with pytest.raises(ProviderError):G.grade_comparison(packet,[],'fake',post=post)


def test_gemini_receives_both_full_videos(packet,tmp_path):
    uploaded=[]; deleted=[]; requests=[]
    class Client:
        def upload(self,file):
            uploaded.append(file);return SimpleNamespace(name=file,uri='gs://'+file)
        def get(self,name):return SimpleNamespace(state='ACTIVE')
        def delete(self,name):deleted.append(name)
        def generate_content(self,**kwargs):
            requests.append(kwargs);return SimpleNamespace(text=json.dumps(comparison(packet['plan'],packet['rubric'])))
    client=Client();client.files=client;client.models=client
    out=G.compare_media('reference.mp4','actual-render.mp4',packet,[],'fake',client=client)
    assert uploaded==deleted==['reference.mp4','actual-render.mp4']
    assert len([p for p in requests[0]['contents'][0].parts if p.file_data])==2
    assert requests[0]['model']==out['model']=='gemini-3.8-flash'


def test_claimed_full_coverage_with_only_opening_observations_fails(packet):
    obs=comparison(packet['plan'],packet['rubric'])
    for observation in obs['observations']:
        observation.update(plan_clip_ids=['opening'],reference_end_s=.2,render_end_s=.2,
                           frame_ids=['reference_frame_0','render_frame_0'])
    result=evaluate(packet,obs)
    assert result['status']=='needs_evidence' and not result['delivery_ready']


@pytest.mark.parametrize('change',['duplicate','track','muted','reverse','opacity','effects','freeze'])
def test_execution_semantics_are_not_hidden_by_valid_json(packet,change):
    timeline=json.loads((ROOT/'packages/timeline/test/fixtures/edit-timeline.json').read_text())
    track=timeline['tracks'][0];clip=track['clips'][0]
    if change=='duplicate':track['clips'].append(copy.deepcopy(clip))
    if change=='track':track['id']='wrong'
    if change=='muted':track['muted']=True
    if change=='reverse':clip['reverse']=True
    if change=='opacity':clip['transform']['opacity']=0
    if change=='effects':clip['effects']=[{'id':'e','kind':'blur','params':{},'enabled':True}]
    if change=='freeze':clip['freeze']=0
    assert S.plan_timeline_mismatches(packet['plan'],timeline)


def test_provider_failure_retry_preserves_round(env,monkeypatch,tmp_path):
    store,ws,inputs,_=env
    submitted=server.start_edit_style_review(**inputs)
    failed=run.run_once(store,[S.KIND])
    assert failed['status']=='failed' and failed['input']['round']==1
    credentials.save_key('gemini','fake',ws,store);credentials.save_key('openai','fake',ws,store)
    mock_providers(monkeypatch,tmp_path)
    retry=server.retry_edit_style_review(submitted['review_job_id'])
    assert retry['status']=='queued'
    done=run.run_once(store,[S.KIND]);assert done['status']=='completed',done.get('error')
    assert done['input']['round']==1 and len(done['failed_attempts'])==1
    with pytest.raises(GateRefused):server.retry_edit_style_review(done['id'])


def test_concurrent_root_reservation_and_root_reset_are_blocked(env):
    from concurrent.futures import ThreadPoolExecutor
    store,ws,inputs,timeline=env
    def enqueue():
        return S.enqueue_review(store,ws,plan_id=inputs['edit_plan_asset_id'],reference_id=inputs['reference_asset_id'],
            render_id=inputs['render_asset_id'],timeline_id=inputs['timeline_asset_id'],creator_id='editor')
    with ThreadPoolExecutor(max_workers=4) as pool:
        jobs=list(pool.map(lambda _:enqueue(),range(8)))
    assert len({j['id'] for j in jobs})==1 and len(store.find('job',ws,kind=S.KIND))==1
    timeline['version']+=1
    new=R.put_bytes_asset(store,ws,json.dumps(timeline).encode(),'timeline-renamed.json','timeline','application/json')
    with pytest.raises(GateRefused,match='already has a review'):
        server.start_edit_style_review(**{**inputs,'timeline_asset_id':new['id']})


def test_metadata_is_not_an_editor_revision():
    timeline=json.loads((ROOT/'packages/timeline/test/fixtures/edit-timeline.json').read_text())
    changed=copy.deepcopy(timeline);changed['version']+=1;changed['name']='new name';changed['markers']=[]
    assert S.timeline_execution_hash(timeline)==S.timeline_execution_hash(changed)


def test_actual_delivery_mismatch_is_detected(monkeypatch):
    monkeypatch.setattr(S.shell,'run',lambda *a,**k:SimpleNamespace(stdout=json.dumps({'streams':[
        {'width':720,'height':1280,'avg_frame_rate':'24/1'}]})))
    actual,errors=S.probe_delivery('render',{'width':1080,'height':1920,'fps':30})
    assert actual['fps']==24 and len(errors)==2
