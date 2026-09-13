"""Timing, coverage and evidence gates; no provider network calls."""
import copy
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from adengine.core.auth import AuthContext, set_auth_context
from adengine.core.errors import GateRefused, NotFound, ProviderError
from adengine.core.store import LocalStore
from adengine.engines import watch
from adengine.gen import edit_plan as E, registry as R, server
from adengine.workers import tasks, queue, run

FIXTURE = Path(__file__).resolve().parents[3] / 'packages/timeline/test/fixtures/edit-plan.json'

@pytest.fixture
def handoff():
    return json.loads(FIXTURE.read_text())


def test_handoff_accepts_shared_editor_fixture(handoff):
    parsed = E.validate_handoff(handoff['plan'], handoff['analysis'])
    assert parsed.clips[1].speed == 2
    assert E.EditPlan.model_json_schema()['additionalProperties'] is False


@pytest.mark.parametrize('mutate', [
    lambda p: p['unresolved'].append('Unknown transition'),
    lambda p: p['clips'][0].update(source_out_s=100),
    lambda p: p['clips'][1].update(timeline_start_s=2.5, source_in_s=6),
    lambda p: p['clips'][1].update(track_id='audio'),
    lambda p: p['clips'][1].update(id='opening'),
    lambda p: p['clips'][0]['evidence'][0].update(observation_id='invented'),
    lambda p: p['clips'][0].update(asset_id='asset_unwatched'),
    lambda p: p['clips'][0]['animations'][0]['keyframes'][1].update(at_s=2),
    lambda p: p['clips'][0]['animations'][0]['keyframes'][1].update(at_s=0.00001),
    lambda p: p['clips'][0].update(speed=float('nan')),
    lambda p: p['clips'][0].update(transition_out={'kind':'dissolve', 'duration_s':3, 'rationale':'x'}),
    lambda p: p['clips'][1].update(transition_out={'kind':'dissolve', 'duration_s':0.2, 'rationale':'x'}),
    lambda p: p['analysis_to_edit'].pop('pacing'),
    lambda p: p['clips'][0].update(mystery_effect='ignored?'),
])
def test_invalid_handoff_is_blocked(handoff, mutate):
    mutate(handoff['plan'])
    with pytest.raises(GateRefused):
        E.validate_handoff(handoff['plan'], handoff['analysis'])


@pytest.mark.parametrize('change', ['missing', 'unknown', 'empty', 'duplicate', 'outside', 'nan', 'missing_beat'])
def test_incomplete_analysis_cannot_reach_editor(handoff, change):
    m = handoff['analysis']['ref_a']
    if change == 'missing': m['editorial'].pop('animations')
    if change == 'unknown': m['editorial']['animations']['status'] = 'unknown'
    if change == 'empty': m['editorial']['rushes']['observations'] = []
    if change == 'duplicate': m['editorial']['cuts']['observations'][0]['id'] = 'rushes-1'
    if change == 'outside': m['editorial']['cuts']['observations'][0]['end_s'] = 13
    if change == 'nan': m['editorial']['cuts']['observations'][0]['confidence'] = float('nan')
    if change == 'missing_beat': m['beats'][0]['gemini'] = {}
    with pytest.raises(GateRefused): E.validate_handoff(handoff['plan'], handoff['analysis'])


def test_watch_partial_manifest_is_honest():
    beats = [{'index':1, 't':0, 't_end':2, 'duration':2}]
    manifest = watch.build_manifest('asset_x', beats, [], 'none', {'_skipped':'disabled'})
    assert manifest['analysis']['status'] == 'incomplete'
    assert manifest['analysis']['every_frame_verified'] is False
    assert len(manifest['analysis']['issues']) >= 5


def test_detect_scenes_keeps_sub_half_second_cuts(monkeypatch):
    monkeypatch.setattr(watch.shell, 'run', lambda *a, **k: SimpleNamespace(
        stderr='pts_time:0.1\npts_time:0.2\npts_time:0.25\npts_time:0.9'))
    assert watch.detect_scenes('source') == [0, 0.1, 0.2, 0.25, 0.9]


def test_beats_have_full_duration_and_preview_never_crosses_cut(monkeypatch, tmp_path):
    monkeypatch.setattr(watch, 'probe_duration', lambda v: 12)
    monkeypatch.setattr(watch, 'detect_scenes', lambda *a: [0, 0.2, 1])
    monkeypatch.setattr(watch.shell, 'run', lambda *a, **k: None)
    beats = watch.extract_beats('source', str(tmp_path))
    assert [(b['t'],b['t_end']) for b in beats] == [(0,0.2),(0.2,1),(1,12)]
    assert beats[-1]['duration'] == 11 and beats[-1]['preview_duration'] == 4
    assert all(b['preview_t_end'] <= b['t_end'] for b in beats)
    with pytest.raises(ProviderError, match='no cut candidates were discarded'):
        watch.extract_beats('source', str(tmp_path), max_beats=2)


def test_sampling_does_not_invent_or_erase_cuts(monkeypatch, tmp_path):
    monkeypatch.setattr(watch, 'probe_duration', lambda v: 12)
    monkeypatch.setattr(watch, 'detect_scenes', lambda *a: [0, 7.1])
    monkeypatch.setattr(watch.shell, 'run', lambda *a, **k: None)
    beats = watch.extract_beats('source', str(tmp_path))
    assert next(b for b in beats if b['t'] == 7.1)['boundary_origin'] == 'scene_change_candidate'
    assert next(b for b in beats if b['t'] == 2.5)['boundary_origin'] == 'sampling_window'
    assert beats[-1]['t_end'] == 12


def test_transcript_half_open_ranges():
    transcript = [{'start':0,'end':1,'text':'left'}, {'start':1,'end':2,'text':'right'}]
    assert watch.transcript_for_beat(transcript, 1, 2) == 'right'


@pytest.fixture
def saved(handoff, tmp_path, monkeypatch):
    store = LocalStore(str(tmp_path / 'store'))
    set_auth_context(AuthContext(workspace_id='ws_test', role='editor', member_id='member'))
    monkeypatch.setattr(server, '_store', lambda: store)
    monkeypatch.setattr(server, '_ws', lambda: 'ws_test')
    asset = R.put_bytes_asset(store, 'ws_test', b'fake', 'source.mp4', 'video', 'video/mp4')
    m = handoff['analysis']['ref_a']; m['video_asset_id'] = asset['id']
    ref = R.create_reference(store, 'ws_test', asset['id'], asset_id=asset['id'])
    R.update_reference(store, 'ws_test', ref['id'], manifest=m, status='watched')
    for clip in handoff['plan']['clips']:
        clip['asset_id'] = asset['id']; clip['evidence'][0]['reference_id'] = ref['id']
    return store, ref['id'], handoff['plan']


def test_save_read_stale_and_workspace_gate(saved, monkeypatch):
    store, rid, plan = saved
    out = server.save_edit_plan(plan, [rid])
    capability = server.get_agent_capability('video-edit-analysis')
    assert set(capability['completion']['required_result_fields']) <= out.keys()
    assert out['capability_id'] == capability['id']
    assert out['handoff_agent'] == capability['handoff_agent']
    envelope = server.get_edit_plan(out['asset_id'])
    assert envelope['plan'] == plan and envelope['editor'] == '@adengine/timeline'
    assert envelope['assets'][0]['duration_s'] == 12
    monkeypatch.setattr(server, '_ws', lambda: 'ws_other')
    with pytest.raises(NotFound): server.get_edit_plan(out['asset_id'])
    monkeypatch.setattr(server, '_ws', lambda: 'ws_test')
    manifest = R.get_reference(store, 'ws_test', rid)['manifest']
    manifest['editorial']['pacing']['summary'] = 'Revised timing'
    R.update_reference(store, 'ws_test', rid, manifest=manifest)
    with pytest.raises(GateRefused, match='stale'): server.get_edit_plan(out['asset_id'])


def test_viewer_cannot_save_handoff(saved):
    _, rid, plan = saved
    set_auth_context(AuthContext(workspace_id='ws_test', role='viewer', member_id='viewer'))
    try:
        from adengine.core.errors import Forbidden
        with pytest.raises(Forbidden): server.save_edit_plan(plan, [rid])
    finally:
        set_auth_context(AuthContext(workspace_id='ws_test', role='editor', member_id='member'))


def test_missing_frame_review_is_blocked(saved):
    store, rid, plan = saved
    job = queue.enqueue(store, 'ws_test', 'review_video_frames', {})
    with pytest.raises(GateRefused): server.save_edit_plan(plan, [rid], [job['id']])


def test_frame_window_retains_variable_timestamps(monkeypatch, tmp_path):
    monkeypatch.setattr(watch, 'probe_duration', lambda v: 1)
    def run_cmd(cmd, **kw):
        if '-show_frames' in cmd:
            return SimpleNamespace(stdout=json.dumps({'frames': [
                {'best_effort_timestamp_time': str(t)} for t in [2, 2.033, 2.09, 2.1]]}))
        for i in range(1, 4): (tmp_path / f'detail_{i:04d}.jpg').write_bytes(b'jpg')
        return SimpleNamespace(stdout='')
    monkeypatch.setattr(watch.shell, 'run', run_cmd)
    frames = watch.extract_frame_window('source', str(tmp_path), 0, .1)
    assert [f['frame_index'] for f in frames] == [0,1,2]
    assert [f['t'] for f in frames] == pytest.approx([0,.033,.09])
    monkeypatch.setattr(watch, 'MAX_REVIEW_FRAMES', 2)
    with pytest.raises(ProviderError, match='No frames are silently subsampled'):
        watch.extract_frame_window('source', str(tmp_path), 0, .1)


def test_frame_review_rejects_claimed_coverage_gaps(tmp_path):
    frame = tmp_path / 'frame.jpg'; frame.write_bytes(b'jpg')
    frames = [{'frame_index':i, 't':i / 30, 'path':str(frame)} for i in range(3)]
    seen = []
    class Client:
        models = None
        def generate_content(self, **kw):
            seen.append(kw)
            return SimpleNamespace(text=json.dumps({'covered_frame_indices':[0,2],
                'observations':[{'description':'cut'}], 'unresolved':[]}))
    client = Client(); client.models = client
    out = watch.review_frame_window(frames, 'Review', 'unused', client=client)
    assert seen[0]['model'] == out['model'] == 'gemini-3.8-flash'
    assert out['status'] == 'incomplete' and out['every_frame_supplied'] is True
    parts = seen[0]['contents'][0].parts
    assert len([p for p in parts if p.inline_data]) == 3
    assert out['audio_reviewed'] is False


def test_selected_source_evidence_must_overlap_trim(handoff):
    handoff['analysis']['ref_a']['editorial']['rushes']['observations'][0].update(start_s=10, end_s=12)
    with pytest.raises(GateRefused, match='selected source range'):
        E.validate_handoff(handoff['plan'], handoff['analysis'])


def test_frame_review_worker_persists_evidence(saved, monkeypatch, tmp_path):
    from adengine.engines import credentials
    store, rid, _ = saved
    asset_id = R.get_reference(store, 'ws_test', rid)['asset_id']
    image = tmp_path / 'frame.jpg'; image.write_bytes(b'frame')
    monkeypatch.setattr(watch, 'extract_frame_window', lambda *args: [
        {'frame_index': 2, 't': 2/30, 'path': str(image)}])
    monkeypatch.setattr(watch, 'review_frame_window', lambda *args: {
        'status':'complete', 'every_frame_supplied':True, 'result':{'covered_frame_indices':[2]}})
    credentials.save_key('gemini', 'fake-test-key', 'ws_test', store)
    submitted = server.review_video_frames(asset_id, 0, 0.1)
    completed = run.run_once(store, ['review_video_frames'])
    assert completed['id'] == submitted['job_id'] and completed['status'] == 'completed'
    output = completed['output']; frame = output['frames'][0]
    assert frame['frame_index'] == 2 and 'path' not in frame
    assert R.get_asset(store, 'ws_test', frame['asset_id'])['meta']['source_asset_id'] == asset_id


def test_actual_ffmpeg_frame_extraction_and_fast_cuts(tmp_path):
    """Exercise real decoding on synthetic footage, with no model or generated media."""
    import shutil
    from adengine.core.settings import settings
    if not shutil.which(settings.ffmpeg) or not shutil.which(settings.ffprobe):
        pytest.skip('ffmpeg/ffprobe not installed')
    video = str(tmp_path / 'fixture.mp4')
    watch.shell.run([settings.ffmpeg, '-y', '-f','lavfi', '-i','color=black:s=64x64:r=30:d=0.2',
        '-f','lavfi','-i','color=white:s=64x64:r=30:d=0.2',
        '-f','lavfi','-i','color=black:s=64x64:r=30:d=0.2',
        '-filter_complex','[0:v][1:v][2:v]concat=n=3:v=1:a=0[v]', '-map','[v]',
        '-c:v','libx264', '-pix_fmt','yuv420p', video], check=True)
    assert watch.detect_scenes(video) == pytest.approx([0,0.2,0.4], abs=.001)
    work = tmp_path / 'frames'; work.mkdir()
    frames = watch.extract_frame_window(video, str(work), 0, .6)
    assert len(frames) == 18
    assert [f['frame_index'] for f in frames] == list(range(18))
    assert all(Path(f['path']).stat().st_size > 0 for f in frames)
    assert frames[-1]['t'] == pytest.approx(17/30, abs=.000001)


def test_gemini_upload_failure_does_not_generate_and_is_cleaned():
    calls = []
    class Client:
        def upload(self, **kwargs): return SimpleNamespace(name='files/test', uri='test')
        def get(self, **kwargs): return SimpleNamespace(state='FAILED')
        def delete(self, **kwargs): calls.append('delete')
        def generate_content(self, **kwargs): calls.append('generate')
    client = Client(); client.files = client; client.models = client
    with pytest.raises(ProviderError, match='processing failed'):
        watch._gemini_generate('test', 'video/mp4', 'unused', 'test', '', '', client=client)
    assert calls == ['delete']
