"""Registry, plan runner, gates, watcher and provider adapters — no real provider is hit."""
import base64
import json
import os
import tempfile

os.environ.setdefault("ADENGINE_DATA_DIR", tempfile.mkdtemp(prefix="adengine-test-"))
os.environ.setdefault("ADENGINE_DEV_WORKSPACE", "ws_test")
os.environ.pop("ADENGINE_GEMINI_WATCH_MODEL", None)

import pytest  # noqa: E402

from adengine.core.errors import GateRefused, ProviderError  # noqa: E402
from adengine.core.store import LocalStore  # noqa: E402
from adengine.engines import credentials, elevenlabs, heygen, kie, watch  # noqa: E402
from adengine.gen import plan as P  # noqa: E402
from adengine.gen import registry as R  # noqa: E402
from adengine.gen import server  # noqa: E402
from adengine.workers import queue, run, tasks  # noqa: E402

WS = "ws_test"


@pytest.fixture
def store(tmp_path, monkeypatch):
    s = LocalStore(str(tmp_path / "data"))
    monkeypatch.setattr(server, "_store", lambda: s)
    monkeypatch.setattr(server, "_ws", lambda: WS)
    return s


# ---------------------------------------------------------------------------
# registry
# ---------------------------------------------------------------------------

def test_registry_job_asset_cost_roundtrip(store):
    job = R.create_job(store, WS, "kie_generate", provider="kie", input={"model": "x"})
    assert job["status"] == R.QUEUED and job["workspace_id"] == WS
    asset = R.put_bytes_asset(store, WS, b"png-bytes", f"jobs/{job['id']}/result_0.png",
                              kind="image", mime="image/png", job_id=job["id"])
    assert asset["storage_key"] == f"jobs/{job['id']}/result_0.png"
    assert "path" not in asset and asset["url"].endswith(asset["storage_key"])
    assert R.asset_url(store, asset) == asset["url"]
    with open(store.blob_path(WS, asset["storage_key"]), "rb") as f:
        assert f.read() == b"png-bytes"
    R.record_cost(store, WS, job["id"], "kie", 6.0, "credits", 0.024)
    R.record_cost(store, WS, job["id"], "kie", 4.0, "credits", 0.016)
    R.record_cost(store, WS, None, "elevenlabs", 1200, "characters", None)
    s = R.cost_summary(store, WS)
    assert s["providers"]["kie"] == {"units": 10.0, "unit_name": "credits", "usd": 0.04, "n": 2}
    assert s["providers"]["elevenlabs"]["units"] == 1200 and s["total_usd"] == 0.04
    assert R.cost_summary(store, WS, job_id=job["id"])["n"] == 2
    assert [a["id"] for a in R.list_assets(store, WS, job_id=job["id"])] == [asset["id"]]
    assert R.list_jobs(store, WS, kind="kie_generate")[0]["id"] == job["id"]
    pub = R.public_asset(asset)
    assert set(pub) == {"id", "kind", "mime", "url", "job_id", "meta", "created"}


def test_voice_registry_and_pronunciation(store):
    R.register_voice(store, WS, "creator-a", "v_123", tags=["ugc"])
    assert R.resolve_voice(store, WS, "creator-a") == "v_123"
    assert R.resolve_voice(store, WS, "rachel") == elevenlabs.STOCK_VOICES["rachel"]
    assert R.resolve_voice(store, WS, "raw_id_xyz") == "raw_id_xyz"
    store.create("pronunciation", WS, "pron", plain="Brandname", respelled="Brand-Naym")
    fixes = R.pronunciation_fixes(store, WS)
    assert elevenlabs.apply_pronunciation_fixes("Hi Brandname", fixes) == "Hi Brand-Naym"


def test_credentials_record_then_env_fallback(store, monkeypatch):
    monkeypatch.delenv("ADENGINE_KIE_KEY", raising=False)
    with pytest.raises(credentials.MissingCredential):
        credentials.get_key("kie", WS, store)
    monkeypatch.setenv("ADENGINE_KIE_KEY", "env-key")
    assert credentials.get_key("kie", WS, store) == "env-key"
    credentials.save_key("kie", "record-key", WS, store)
    assert credentials.get_key("kie", WS, store) == "record-key"
    monkeypatch.setattr(credentials.settings, "auth_mode", "oauth", raising=False) if False else None
    with pytest.raises(ProviderError):
        credentials.get_key("notaprovider", WS, store)


# ---------------------------------------------------------------------------
# plan runner
# ---------------------------------------------------------------------------

PLAN = {
    "continuity_groups": {"creator": {"description": "same creator", "member_beats": ["1", "3"]}},
    "scenes": [
        {"index": 1, "t": 0, "t_end": 4, "adaptation_instructions": "creator holds product",
         "continuity_group": "creator"},
        {"index": 2, "t": 4, "t_end": 7, "adaptation_instructions": "real hands", "authenticity": "real_footage_required"},
        {"index": 3, "t": 7, "t_end": 13, "adaptation_instructions": "creator close-up", "continuity_group": "creator",
         "motion_prompt": "slow push in"},
    ],
}


def test_preflight_estimates_and_balance():
    out = P.preflight(PLAN, balance=1000.0)
    assert out["n_scenes"] == 3 and out["estimated_images"] == 3
    assert [s["beat"] for s in out["scenes_deferred_to_sourcing"]] == ["2"]
    assert out["estimated_video_seconds"] == 10.0
    assert out["estimated_video_credits"] == 630.0 and out["sufficient_balance"] is True
    assert out["estimated_video_usd"] == round(630.0 * server.settings.kie_credit_usd, 4)
    assert P.preflight(PLAN, balance=10.0)["sufficient_balance"] is False


def test_keyframe_and_animation_requests():
    inputs, deferred = P.keyframe_requests(PLAN, ["asset_ref1"], anchors={"creator": "asset_anchor"})
    assert [i["beat"] for i in inputs] == ["1", "3"] and deferred[0]["beat"] == "2"
    assert inputs[0]["asset_refs"]["input_urls"] == ["asset_anchor", "asset_ref1"]  # anchor first
    anim, skipped = P.animation_requests(PLAN, {"1": "asset_k1"})
    assert len(anim) == 1 and anim[0]["duration"] == 4
    assert anim[0]["asset_refs"] == {"first_frame_url": "asset_k1"}
    assert anim[0]["input"]["prompt"] == "creator holds product"
    assert skipped[0]["beat"] == "2"


# ---------------------------------------------------------------------------
# approval gate
# ---------------------------------------------------------------------------

def _approved_board(store, asset_ids, slug="board-1"):
    from adengine.dr.boards import layout, card_fingerprint
    for aid in asset_ids:
        try:
            store.get("asset", WS, aid)
        except Exception:
            store.put("asset", {"id": aid, "workspace_id": WS, "kind": "image"})
    laid = layout({"title": "Test board", "timelines": [
        {"role": "ours", "beats": [{"frame": aid} for aid in asset_ids]}]})
    board = store.create("board", WS, "board", slug=slug, version=1, **laid)
    for card in laid["cards"]:
        if card.get("asset_id"):
            store.create("approval", WS, "apr", board_id=board["id"], card_id=card["id"],
                         asset_id=card["asset_id"], member_id="human", state="approved", at=1,
                         fingerprint=card_fingerprint(board, card))
    return board


def test_animate_scenes_refuses_without_board_slug(store):
    with pytest.raises(GateRefused):
        server.animate_scenes(PLAN, {"1": "asset_k1"}, board_slug="")
    assert R.list_jobs(store, WS) == []


def test_animate_scenes_refuses_when_module_missing(store, monkeypatch):
    import sys
    monkeypatch.setitem(sys.modules, "adengine.dr.boards", None)
    with pytest.raises(GateRefused) as exc:
        server.animate_scenes(PLAN, {"1": "asset_k1"}, board_slug="board-1")
    assert "not approved" in str(exc.value)
    assert R.list_jobs(store, WS) == []


def test_animate_scenes_refuses_pending_board(store):
    board = _approved_board(store, ["asset_k1", "asset_k3"])
    for approval in store.find("approval", WS, board_id=board["id"]):
        store.delete("approval", WS, approval["id"])
    with pytest.raises(GateRefused) as exc:
        server.animate_scenes(PLAN, {"1": "asset_k1"}, board_slug="board-1")
    assert len(exc.value.details["pending"]) == 2
    assert R.list_jobs(store, WS) == []


def test_animate_scenes_refuses_keyframe_not_on_board(store):
    _approved_board(store, ["asset_k1"])
    with pytest.raises(GateRefused) as exc:
        server.animate_scenes(PLAN, {"1": "asset_k1", "3": "asset_k3"}, board_slug="board-1")
    assert exc.value.details["missing_asset_ids"] == ["asset_k3"]
    assert R.list_jobs(store, WS) == []


def test_animate_scenes_dispatches_when_approved(store):
    _approved_board(store, ["asset_k1", "asset_k3"])
    out = server.animate_scenes(PLAN, {"1": "asset_k1", "3": "asset_k3"}, board_slug="board-1")
    assert [d["beat"] for d in out["dispatched"]] == ["1", "3"]
    assert [d["duration"] for d in out["dispatched"]] == [4, 6]
    jobs = R.list_jobs(store, WS, kind="kie_generate")
    assert len(jobs) == 2 and all(j["status"] == R.QUEUED for j in jobs)
    assert all(j["input"]["board_version"] == 1 for j in jobs)
    assert {j["input"]["asset_refs"]["first_frame_url"] for j in jobs} == {"asset_k1", "asset_k3"}


# ---------------------------------------------------------------------------
# tools enqueue only (never poll); ids/urls only
# ---------------------------------------------------------------------------

def test_resolve_reference_enqueues_ingest_then_watch(store):
    out = server.resolve_reference("https://www.tiktok.com/@x/video/123")
    ingest = R.get_job(store, WS, out["ingest_job_id"])
    w = R.get_job(store, WS, out["watch_job_id"])
    assert ingest["kind"] == "ingest_reference" and w["kind"] == "watch_reference"
    assert w["parent_id"] == ingest["id"] and w["input"]["gemini"] is True
    ref = R.get_reference(store, WS, out["reference_id"])
    assert ref["watch_job_id"] == w["id"]
    assert server.get_watch_manifest(out["reference_id"])["manifest"] is None
    # watch job cannot be claimed before ingest completes
    assert queue.claim(store, ["watch_reference"]) is None


def test_generate_tools_enqueue(store):
    a = R.put_bytes_asset(store, WS, b"x", "uploads/a.png", "image", "image/png")
    img = server.generate_image("a prompt", ref_asset_ids=[a["id"]])
    assert R.get_job(store, WS, img["job_id"])["input"]["asset_refs"] == {"input_urls": [a["id"]]}
    t2i = server.generate_image("no refs")
    assert t2i["model"] == kie.IMAGE_MODEL_T2I
    _approved_board(store, [a["id"]])
    vid = server.generate_video("motion", first_frame_asset_id=a["id"], duration=99, board_slug="board-1")
    j = R.get_job(store, WS, vid["job_id"])
    assert j["input"]["input"]["duration"] == 30 and j["input"]["asset_refs"]["first_frame_url"] == a["id"]
    vo = server.generate_vo("hello", "rachel", with_timestamps=True)
    assert R.get_job(store, WS, vo["job_id"])["kind"] == "eleven_vo"
    cl = server.clone_voice("creator", [a["id"]])
    assert R.get_job(store, WS, cl["job_id"])["kind"] == "eleven_clone"
    hg = server.heygen_generate(a["id"], "look_1", board_slug="board-1")
    assert R.get_job(store, WS, hg["job_id"])["kind"] == "heygen_avatar"
    an = server.analyze_video(a["id"], "score this frame 1-10")
    assert an["model"] == "gemini-3.8-flash"
    assert R.get_job(store, WS, an["job_id"])["input"]["prompt"] == "score this frame 1-10"
    with pytest.raises(Exception):
        server.watch_reference("/local/path.mp4")
    for j in server.list_jobs():
        assert j["status"] == R.QUEUED  # nothing ran, nothing polled


def test_generate_anchors_uses_product_truth(store):
    store.create("product", WS, "prod", brand_id="b", slug="tote", name="Tote",
                 truth={"reference_asset_ids": ["asset_p1", "asset_p2"]})
    out = server.generate_anchors(PLAN, "tote")
    job = R.get_job(store, WS, out["anchor_jobs"]["creator"]["job_id"])
    assert job["input"]["asset_refs"]["input_urls"] == ["asset_p1", "asset_p2"]
    assert job["input"]["model"] == kie.IMAGE_MODEL_I2I
    kf = server.generate_keyframes(PLAN, anchors={"creator": "asset_anchor"}, product_slug="tote")
    j = R.get_job(store, WS, kf["dispatched"][0]["job_id"])
    assert j["input"]["asset_refs"]["input_urls"][0] == "asset_anchor"


# ---------------------------------------------------------------------------
# provider adapters: request construction only
# ---------------------------------------------------------------------------

class _Resp:
    def __init__(self, status=200, content=b"", js=None, text=""):
        self.status_code, self.content, self._js, self.text = status, content, js, text

    def json(self):
        return self._js


def test_kie_upload_uses_curl_multipart(monkeypatch, tmp_path):
    calls = []

    def fake_run(cmd, timeout=0, check=False):
        calls.append(cmd)
        import subprocess
        return subprocess.CompletedProcess(cmd, 0, stdout=json.dumps({"data": {"downloadUrl": "https://cdn/x.png"}}), stderr="")

    monkeypatch.setattr(kie.shell, "run", fake_run)
    f = tmp_path / "my file.png"
    f.write_bytes(b"x")
    assert kie.upload(str(f), "KEY", upload_path="adengine/ws", sleep=lambda s: None) == "https://cdn/x.png"
    cmd = calls[0]
    assert cmd[0] == kie.settings.curl and "-F" in cmd and f"file=@{f}" in cmd
    assert "Authorization: Bearer KEY" in cmd and "uploadPath=adengine/ws" in cmd


def test_kie_create_task_and_poll(monkeypatch):
    seen = []

    def fake_api(method, url, key, payload=None):
        seen.append((method, url, payload))
        if url.endswith("createTask"):
            return {"code": 200, "data": {"taskId": "t1"}}
        if "recordInfo" in url:
            return {"data": {"state": "success", "creditsConsumed": 6,
                             "resultJson": json.dumps({"resultUrls": ["https://cdn/a.png"]})}}
        if url.endswith("chat/credit"):
            return {"data": 512.5}
        raise AssertionError(url)

    monkeypatch.setattr(kie, "_api", fake_api)
    assert kie.create_task("gpt-image-2-image-to-image", {"prompt": "p"}, "K") == "t1"
    assert seen[0] == ("POST", f"{kie.KIE_API}/jobs/createTask",
                       {"model": "gpt-image-2-image-to-image", "input": {"prompt": "p"}})
    info = kie.wait_for_task("t1", "K", sleep=lambda s: None)
    assert kie.result_urls(info) == ["https://cdn/a.png"] and info["creditsConsumed"] == 6
    assert kie.balance("K") == 512.5
    assert kie.credits_to_usd(6) == round(6 * kie.settings.kie_credit_usd, 4)
    assert kie.estimate_credits("bytedance/seedance-2-5", 10) == 630.0


def test_elevenlabs_tts_request_and_split(monkeypatch):
    posted = []

    def fake_post(url, headers=None, json=None, timeout=0, **kw):
        posted.append((url, headers, json))
        if url.endswith("/with-timestamps"):
            return _Resp(200, js={"audio_base64": base64.b64encode(b"mp3").decode(), "alignment": {"chars": []}})
        return _Resp(200, content=b"mp3")

    monkeypatch.setattr(elevenlabs.requests, "post", fake_post)
    audio, al = elevenlabs.tts_one_take("hello", "v1", "KEY")
    assert audio == b"mp3" and al is None
    url, headers, payload = posted[0]
    assert url == f"{elevenlabs.BASE_URL}/text-to-speech/v1"
    assert headers["xi-api-key"] == "KEY" and headers["Accept"] == "audio/mpeg"
    assert payload == {"text": "hello", "model_id": "eleven_v3", "voice_settings": elevenlabs.CREATIVE}
    assert elevenlabs.CREATIVE["stability"] == 0.0
    audio, al = elevenlabs.tts_one_take("hello", "v1", "KEY", with_timestamps=True)
    assert audio == b"mp3" and al == {"chars": []}

    long_text = "\n\n".join(["a" * 3000, "b" * 3000, "c" * 100])
    takes = elevenlabs.split_at_paragraph(long_text)
    assert takes == ["a" * 3000, "b" * 3000 + "\n\n" + "c" * 100]
    assert elevenlabs.split_at_paragraph("short") == ["short"]


def test_elevenlabs_clone_request(monkeypatch, tmp_path):
    seen = {}

    def fake_post(url, headers=None, data=None, files=None, timeout=0):
        seen.update(url=url, headers=headers, data=data, nfiles=len(files))
        return _Resp(200, js={"voice_id": "cloned_1"})

    monkeypatch.setattr(elevenlabs.requests, "post", fake_post)
    a = tmp_path / "a.mp3"; a.write_bytes(b"1")
    b = tmp_path / "b.mp3"; b.write_bytes(b"2")
    assert elevenlabs.clone_voice("creator", [str(a), str(b)], "KEY", description="d") == "cloned_1"
    assert seen["url"] == f"{elevenlabs.BASE_URL}/voices/add" and seen["nfiles"] == 2
    assert seen["data"] == {"name": "creator", "description": "d"} and seen["headers"] == {"xi-api-key": "KEY"}


def test_heygen_goes_through_curl(monkeypatch):
    calls = []

    def fake_curl_json(args, timeout=0):
        calls.append(args)
        if "remaining_quota" in args[2]:
            return {"data": {"details": {"api": 754, "generative_credit": 33}}}
        if args[2].endswith("/v3/videos"):
            return {"data": {"video_id": "vid_1"}}
        if "/v1/asset" in args[2]:
            return {"data": {"id": "aud_1"}}
        if "/v3/videos/vid_1" in args[2]:
            return {"data": {"status": "failed", "error": {"code": "MOVIO_PAYMENT_INSUFFICIENT_CREDIT"}}}
        raise AssertionError(args)

    monkeypatch.setattr(heygen.shell, "curl_json", fake_curl_json)
    q = heygen.check_quota("K")
    assert q["api"] == 754 and q["generative_credit"] == 33
    assert calls[0][:2] == ["-X", "GET"] and "X-Api-Key: K" in calls[0]
    assert heygen.upload_audio("/blob/vo.mp3", "K") == "aud_1"
    assert "--data-binary" in calls[1] and "@/blob/vo.mp3" in calls[1]
    assert heygen.create_video("look_1", "aud_1", "K") == "vid_1"
    payload = json.loads(calls[2][calls[2].index("-d") + 1])
    assert payload["audio_asset_id"] == "aud_1" and payload["engine"] == {"type": "avatar_v"}
    assert "script" not in payload and "voice_id" not in payload
    data = heygen.wait_for_video("vid_1", "K", sleep=lambda s: None)
    assert heygen.is_credit_error(json.dumps(data["error"]))


# ---------------------------------------------------------------------------
# watcher: Gemini + Whisper mocked, model default, transcript_source, analyze_video
# ---------------------------------------------------------------------------

class _FakeFile:
    name, uri, state = "files/abc", "gs://abc", "ACTIVE"


class _FakeGeminiClient:
    def __init__(self, reply, log):
        self._reply, self.log = reply, log
        self.files = self
        self.models = self

    def upload(self, file):
        self.log.append(("upload", file)); return _FakeFile()

    def get(self, name):
        return _FakeFile()

    def delete(self, name):
        self.log.append(("delete", name))

    def generate_content(self, model, contents, config):
        self.log.append(("generate", model, contents[0].parts[1].text, config.system_instruction))

        class _R:
            text = self._reply
        return _R()


def test_gemini_model_defaults_to_3_8_flash():
    assert watch.DEFAULT_GEMINI_MODEL == "gemini-3.8-flash"
    assert watch.gemini_model() == "gemini-3.8-flash"
    assert watch.gemini_model("gemini-3.8-flash") == "gemini-3.8-flash"
    with pytest.raises(ProviderError, match="Visual analysis requires gemini-3.8-flash"):
        watch.gemini_model("gemini-3.7-flash")


def test_visual_model_rejects_stale_environment_override(monkeypatch):
    monkeypatch.setattr(watch, "GEMINI_MODEL", "gemini-3.7-flash")
    with pytest.raises(ProviderError, match="ADENGINE_GEMINI_WATCH_MODEL"):
        watch.gemini_model()


def test_gemini_pass_uploads_full_video_and_parses(monkeypatch, tmp_path):
    log = []
    reply = json.dumps({"overall": {"format": "Founder UGC"}, "beats": [{"index": 1, "ad_role": "hook"}]})
    client = _FakeGeminiClient(reply, log)
    video = tmp_path / "source.mp4"; video.write_bytes(b"vid")
    beats = [{"index": 1, "t": 0.0, "t_end": 2.0, "duration": 2.0}]
    out = watch.gemini_pass(str(video), beats, "captions (source.en.srt)", "KEY", client=client)
    assert out["beats"][0]["ad_role"] == "hook"
    kinds = [e[0] for e in log]
    assert kinds == ["upload", "generate", "delete"]
    _, model, user_prompt, system = log[1]
    assert model == "gemini-3.8-flash"
    assert "index=1 t=0.00s duration=2.00s" in user_prompt and "captions (source.en.srt)" in user_prompt
    assert system == watch.GEMINI_SYSTEM_PROMPT and '"ad_role"' in system
    assert log[0][1] == str(video)


def test_whisper_request_and_transcript_source(monkeypatch, tmp_path):
    posted = []

    def fake_post(url, headers=None, data=None, files=None, timeout=0):
        posted.append((url, headers, data))
        return _Resp(200, js={"segments": [{"start": 0.0, "end": 1.5, "text": " hi "}]})

    monkeypatch.setattr(watch.requests, "post", fake_post)
    monkeypatch.setattr(watch, "demux_audio", lambda v, w: str(tmp_path / "audio.mp3"))
    (tmp_path / "audio.mp3").write_bytes(b"a" * 2048)
    entries, label = watch.get_transcript("v.mp4", str(tmp_path), openai_key="OK")
    assert entries == [{"start": 0.0, "end": 1.5, "text": "hi"}] and label == "whisper (openai)"
    url, headers, data = posted[0]
    assert url == watch.WHISPER_BACKENDS["openai"][0] and data["model"] == "whisper-1"
    assert data["response_format"] == "verbose_json" and headers == {"Authorization": "Bearer OK"}
    _, label = watch.get_transcript("v.mp4", str(tmp_path), groq_key="GK")
    assert label == "whisper (groq)" and posted[1][2]["model"] == "whisper-large-v3"
    _, label = watch.get_transcript("v.mp4", str(tmp_path))
    assert label.startswith("none (no whisper credential")
    monkeypatch.setattr(watch, "demux_audio", lambda v, w: None)
    assert watch.get_transcript("v.mp4", str(tmp_path))[1] == "none (no audio track)"
    # captions win when present
    (tmp_path / "source.en.srt").write_text("1\n00:00:00,000 --> 00:00:01,000\nHello there\n")
    entries, label = watch.get_transcript("v.mp4", str(tmp_path))
    assert entries[0]["text"] == "Hello there" and label == "captions (source.en.srt)"


def test_watch_job_end_to_end_with_mocks(store, monkeypatch, tmp_path):
    video = R.put_bytes_asset(store, WS, b"vid", "references/r/source.mp4", "video", "video/mp4")
    frame = tmp_path / "beat_001.jpg"; frame.write_bytes(b"jpg")
    monkeypatch.setattr(watch, "extract_beats", lambda v, w, threshold=0.28: [
        {"index": 1, "t": 0.0, "t_end": 2.0, "duration": 2.0, "frame": str(frame), "clip": None}])
    monkeypatch.setattr(watch, "get_transcript", lambda *a, **k: (
        [{"start": 0.0, "end": 1.0, "text": "hello"}], "whisper (openai)"))
    reply = json.dumps({"overall": {"format": "VSL"}, "beats": [{"index": 1, "shot_type": "CU", "ad_role": "hook"}]})
    monkeypatch.setattr(watch, "_make_client", lambda key: _FakeGeminiClient(reply, []))
    credentials.save_key("gemini", "GKEY", WS, store)

    out = server.watch_reference(video["id"])
    done = run.run_once(store, ["watch_reference"])
    assert done["status"] == R.COMPLETED, done.get("error")
    man = server.get_watch_manifest(out["reference_id"])["manifest"]
    assert man["transcript_source"] == "whisper (openai)" and man["gemini_model"] == "gemini-3.8-flash"
    beat = man["beats"][0]
    assert beat["vo"] == "hello" and beat["gemini"]["ad_role"] == "hook"
    assert beat["frame_asset_id"].startswith("asset_") and beat["frame_url"]
    assert "frame" not in beat and "clip" not in beat  # no local paths leak
    assert man["overall"]["format"] == "VSL"
    assert R.get_asset(store, WS, done["output"]["manifest_asset_id"])["kind"] == "manifest"


def test_analyze_video_job_completes_with_mocked_json(store, monkeypatch):
    asset = R.put_bytes_asset(store, WS, b"img", "uploads/k.png", "image", "image/png")
    log = []
    reply = json.dumps({"score": 8, "defects": []})
    monkeypatch.setattr(watch, "_make_client", lambda key: _FakeGeminiClient(reply, log))
    credentials.save_key("gemini", "GKEY", WS, store)
    out = server.analyze_video(asset["id"], "Score this keyframe 1-10 and list defects.")
    done = run.run_once(store, ["analyze_video"])
    assert done["id"] == out["job_id"] and done["status"] == R.COMPLETED, done.get("error")
    assert done["output"]["result"] == {"score": 8, "defects": []}
    assert done["output"]["model"] == "gemini-3.8-flash"
    assert log[1][1] == "gemini-3.8-flash" and log[1][2].startswith("Score this keyframe")


def test_kie_worker_end_to_end_with_mocks(store, monkeypatch, tmp_path):
    ref = R.put_bytes_asset(store, WS, b"ref", "uploads/ref.png", "image", "image/png")
    credentials.save_key("kie", "KKEY", WS, store)
    monkeypatch.setattr(kie, "upload", lambda path, key, upload_path="": "https://kie/tmp/ref.png")
    fired = {}

    def create_task(model, inp, key):
        fired.update(model=model, input=inp); return "task_9"

    monkeypatch.setattr(kie, "create_task", create_task)
    monkeypatch.setattr(kie, "wait_for_task", lambda tid, key, **kw: {
        "state": "success", "creditsConsumed": 6,
        "resultJson": json.dumps({"resultUrls": ["https://cdn/out.png"]})})

    def dl(url, dest):
        with open(dest, "wb") as f:
            f.write(b"png")
        return dest

    monkeypatch.setattr(kie, "download", dl)
    out = server.generate_image("p", ref_asset_ids=[ref["id"]])
    done = run.run_once(store, ["kie_generate"])
    assert done["status"] == R.COMPLETED, done.get("error")
    assert fired["input"]["input_urls"] == ["https://kie/tmp/ref.png"]
    a = R.get_asset(store, WS, done["output"]["asset_ids"][0])
    assert a["kind"] == "image" and a["storage_key"] == f"jobs/{done['id']}/result_0.png"
    assert R.cost_summary(store, WS)["providers"]["kie"]["units"] == 6.0
    assert done["output"]["usd"] == round(6 * kie.settings.kie_credit_usd, 4)
