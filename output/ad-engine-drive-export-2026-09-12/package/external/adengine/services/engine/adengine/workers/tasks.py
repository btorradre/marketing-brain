"""Job handlers, dispatched by kind. Each handler is `fn(store, job) -> output`
and may raise; the runner turns exceptions into fail(job). Polling providers
happens HERE, never in an MCP tool.

Kinds:
  noop              tests
  ingest_reference  URL (GetHookd / yt-dlp / direct) -> blob -> video asset on a reference
  watch_reference   ffmpeg beats + frames as blobs + transcript + Gemini pass -> manifest
  analyze_video     any asset + caller prompt -> Gemini 3.8 Flash structured JSON
  kie_generate      upload ref assets -> createTask -> poll -> download -> assets + cost
  eleven_vo         one-take v3 Creative VO -> audio asset (+ alignment asset)
  eleven_clone      clone a voice from audio/video assets -> 'voice' record
  heygen_avatar     upload VO -> v3 render -> poll -> mp4 asset
"""
from __future__ import annotations

import json
import os
import shutil

from adengine.core.errors import GateRefused, NotFound, ProviderError
from adengine.core.store import Store
from adengine.engines import elevenlabs, gethookd, heygen, kie, shell, watch, ytdlp
from adengine.engines.credentials import get_key, try_get_key
from adengine.gen import registry as R
from adengine.gen import edit_review
from adengine.gen.approval import require_job_board

Output = dict


def _ws(job: dict) -> str:
    return job["workspace_id"]


def _asset(store: Store, job: dict, asset_id: str) -> dict:
    try:
        return R.get_asset(store, _ws(job), asset_id)
    except NotFound:
        raise NotFound(f"asset {asset_id} not found in this workspace")


def _cleanup(path: str) -> None:
    shutil.rmtree(path, ignore_errors=True)


# ---------------------------------------------------------------------------

def noop(store: Store, job: dict) -> Output:
    return {"echo": job.get("input", {})}


# ---------------------------------------------------------------------------

def ingest_reference(store: Store, job: dict) -> Output:
    """input: {url, reference_id?}. Resolves a GetHookd URL/id or any video URL
    into a blob and registers it as the reference's video asset."""
    ws = _ws(job)
    inp = job.get("input") or {}
    url = inp.get("url") or ""
    ref_id = inp.get("reference_id")
    ref = R.get_reference(store, ws, ref_id) if ref_id else R.create_reference(store, ws, url)
    ref_id = ref["id"]
    R.update_reference(store, ws, ref_id, status="ingesting")

    work = shell.workdir("ingest")
    try:
        meta: dict = {}
        subtitle_keys: list[str] = []
        if gethookd.is_gethookd_url(url):
            video_url, meta = gethookd.resolve(url, get_key("gethookd", ws, store))
            local = shell.curl_download(video_url, os.path.join(work, "source.mp4"))
        elif ytdlp.is_url(url):
            try:
                local = ytdlp.download(url, work)
            except ProviderError:
                # not a page yt-dlp understands: try it as a direct media URL
                local = shell.curl_download(url, os.path.join(work, "source.mp4"))
            for sub in ytdlp.subtitle_files(work):
                key = f"references/{ref_id}/{os.path.basename(sub)}"
                with open(sub, "rb") as f:
                    store.put_blob(ws, key, f.read(), mime="text/plain")
                subtitle_keys.append(key)
        else:
            raise ProviderError("ingest_reference needs a URL or GetHookd id; local paths are not accepted")

        ext = os.path.splitext(local)[1] or ".mp4"
        asset = R.put_file_asset(store, ws, local, f"references/{ref_id}/source{ext}", kind="video",
                                 job_id=job["id"], meta={"source": url, "reference_id": ref_id,
                                                        "gethookd": meta or None,
                                                        "subtitle_keys": subtitle_keys})
        R.update_reference(store, ws, ref_id, asset_id=asset["id"], status="ingested",
                           metadata=meta or None, subtitle_keys=subtitle_keys)
        return {"reference_id": ref_id, "asset_id": asset["id"], "asset_url": asset["url"],
                "metadata": meta or None}
    except Exception:
        R.update_reference(store, ws, ref_id, status="ingest_failed")
        raise
    finally:
        _cleanup(work)


# ---------------------------------------------------------------------------

def watch_reference(store: Store, job: dict) -> Output:
    """input: {reference_id | asset_id, gemini=True, scene_threshold?, gemini_model?,
    whisper_backend?}. Writes the manifest onto the reference record."""
    ws = _ws(job)
    inp = job.get("input") or {}
    ref_id = inp.get("reference_id")
    if ref_id:
        ref = R.get_reference(store, ws, ref_id)
        if not ref.get("asset_id"):
            raise ProviderError(f"reference {ref_id} has no video asset yet (ingest first)")
        asset = _asset(store, job, ref["asset_id"])
    else:
        asset = _asset(store, job, inp["asset_id"])
        ref = R.create_reference(store, ws, asset.get("url") or asset["id"], asset_id=asset["id"],
                                 status="ingested")
        ref_id = ref["id"]
    R.update_reference(store, ws, ref_id, status="watching")

    video = R.asset_path(store, asset)
    work = shell.workdir("watch")
    try:
        # captions saved at ingest live next to the source blob; copy them into the work dir
        for key in (ref.get("subtitle_keys") or (asset.get("meta") or {}).get("subtitle_keys") or []):
            try:
                shutil.copy(store.blob_path(ws, key), os.path.join(work, os.path.basename(key)))
            except OSError:
                pass

        beats = watch.extract_beats(video, work, threshold=float(inp.get("scene_threshold") or watch.SCENE_THRESHOLD))
        transcript, label = watch.get_transcript(
            video, work,
            openai_key=try_get_key("openai", ws, store),
            groq_key=try_get_key("groq", ws, store),
            prefer=inp.get("whisper_backend") or "openai")

        use_gemini = inp.get("gemini", True) and not inp.get("skip_gemini", False)
        model = inp.get("gemini_model")
        if not use_gemini:
            gemini = {"overall": {}, "beats": [], "_skipped": "gemini disabled for this job"}
        else:
            gkey = try_get_key("gemini", ws, store)
            if not gkey:
                gemini = {"overall": {}, "beats": [], "_error": "no gemini credential in workspace"}
            else:
                try:
                    gemini = watch.gemini_pass(video, beats, label, gkey, model=model,
                                               media_role=inp.get("media_role", "reference"))
                except Exception as exc:  # noqa: BLE001 — keep frames/transcript, surface the error
                    gemini = {"overall": {}, "beats": [], "_error": f"gemini pass failed: {exc}"}

        manifest = watch.build_manifest(ref.get("source") or asset["id"], beats, transcript, label,
                                        gemini, model=model)
        manifest["reference_id"] = ref_id
        manifest["media_role"] = inp.get("media_role", "reference")
        manifest["video_asset_id"] = asset["id"]
        manifest["video_url"] = asset.get("url")

        frame_assets = []
        for b, entry in zip(beats, manifest["beats"]):
            num = f"{b['index']:03d}"
            if b.get("frame"):
                fa = R.put_file_asset(store, ws, b["frame"], f"references/{ref_id}/frames/beat_{num}.jpg",
                                      kind="frame", mime="image/jpeg", job_id=job["id"],
                                      meta={"reference_id": ref_id, "beat": b["index"], "t": b["t"]})
                entry["frame_asset_id"] = fa["id"]
                entry["frame_url"] = fa["url"]
                frame_assets.append(fa["id"])
            if b.get("clip"):
                ck = f"references/{ref_id}/clips/beat_{num}.mp4"
                with open(b["clip"], "rb") as f:
                    store.put_blob(ws, ck, iter(lambda: f.read(1 << 20), b""), mime="video/mp4")
                entry["clip_url"] = store.url(ws, ck)

        man_asset = R.put_bytes_asset(store, ws, json.dumps(manifest, indent=1).encode(),
                                      f"references/{ref_id}/manifest.json", kind="manifest",
                                      mime="application/json", job_id=job["id"],
                                      meta={"reference_id": ref_id, "n_beats": len(beats),
                                            "transcript_source": label})
        manifest["manifest_asset_id"] = man_asset["id"]
        R.update_reference(store, ws, ref_id, manifest=manifest, status="watched",
                           manifest_asset_id=man_asset["id"])
        return {"reference_id": ref_id, "manifest_asset_id": man_asset["id"],
                "analysis": manifest["analysis"],
                "n_beats": len(beats), "transcript_source": label,
                "gemini_model": manifest.get("gemini_model"),
                "frame_asset_ids": frame_assets, "overall": manifest.get("overall", {})}
    except Exception:
        R.update_reference(store, ws, ref_id, status="watch_failed")
        raise
    finally:
        _cleanup(work)


# ---------------------------------------------------------------------------

def analyze_video(store: Store, job: dict) -> Output:
    """input: {asset_id, prompt, model?, system_instruction?}. Any video/image asset
    -> Gemini 3.8 Flash -> structured JSON in output.result."""
    ws = _ws(job)
    inp = job.get("input") or {}
    asset = _asset(store, job, inp["asset_id"])
    key = get_key("gemini", ws, store)
    model = watch.gemini_model(inp.get("model"))
    result = watch.analyze_video(R.asset_path(store, asset), inp.get("prompt") or "Describe this media.",
                                 key, model=model, mime_type=asset.get("mime") or "video/mp4",
                                 system_instruction=inp.get("system_instruction"))
    return {"asset_id": asset["id"], "model": model, "result": result}


def review_video_frames(store: Store, job: dict) -> Output:
    """Supply every decoded frame in a bounded source window to the analyst."""
    ws, inp = _ws(job), job["input"]
    asset = _asset(store, job, inp["asset_id"])
    key = get_key("gemini", ws, store)
    work = shell.workdir("frame-review")
    try:
        frames = watch.extract_frame_window(R.asset_path(store, asset), work,
                                            inp["start_s"], inp["end_s"])
        result = watch.review_frame_window(frames, inp["prompt"], key)
        evidence = []
        for frame in frames:
            saved = R.put_file_asset(store, ws, frame["path"],
                f"jobs/{job['id']}/frame_{frame['frame_index']}.jpg", kind="frame",
                mime="image/jpeg", job_id=job["id"],
                meta={"source_asset_id": asset["id"], "frame_index": frame["frame_index"], "t": frame["t"]})
            evidence.append({"frame_index": frame["frame_index"], "t": frame["t"],
                             "asset_id": saved["id"], "url": saved["url"]})
        return {**result, "asset_id": asset["id"], "start_s": inp["start_s"],
                "end_s": inp["end_s"], "frames": evidence}
    finally:
        _cleanup(work)


# ---------------------------------------------------------------------------

def _resolve_asset_refs(store: Store, job: dict, key: str) -> dict:
    """Upload each referenced asset to kie temp storage and substitute the URLs
    into the provider input. asset_refs: {field: asset_id | [asset_ids]} —
    a string yields a single URL, a list yields a list."""
    inp = job.get("input") or {}
    provider_input = dict(inp.get("input") or {})
    ws = _ws(job)
    uploaded: dict[str, str] = {}
    for field, refs in (inp.get("asset_refs") or {}).items():
        single = isinstance(refs, str)
        ids = [refs] if single else list(refs or [])
        urls = []
        for aid in ids:
            if aid in uploaded:
                urls.append(uploaded[aid])
                continue
            asset = _asset(store, job, aid)
            url = kie.upload(R.asset_path(store, asset), key, upload_path=f"adengine/{ws}")
            uploaded[aid] = url
            urls.append(url)
        provider_input[field] = urls[0] if single else urls
    return provider_input


def kie_generate(store: Store, job: dict) -> Output:
    """input: {model, input, asset_refs?, purpose?, beat?, group?}. createTask,
    poll until terminal, download results to blobs, register assets + cost."""
    ws = _ws(job)
    inp = job.get("input") or {}
    model = inp["model"]
    if model not in kie.IMAGE_MODELS and not kie.is_video_model(model):
        raise ProviderError(f"unsupported model '{model}'; register its media type before use")
    video_job = kie.is_video_model(model) or inp.get("purpose") in ("video", "animation")
    if video_job:
        frame = (inp.get("asset_refs") or {}).get("first_frame_url")
        if not isinstance(frame, str) or not frame:
            raise GateRefused("approval gate: video job requires an approved first frame")
        require_job_board(store, job, [frame])
    key = get_key("kie", ws, store)
    provider_input = _resolve_asset_refs(store, job, key)
    if video_job:
        require_job_board(store, job, [frame])  # uploads can outlive a human's approval
    task_id = kie.create_task(model, provider_input, key)
    R.update_job(store, ws, job["id"], external_task_id=task_id)

    info = kie.wait_for_task(task_id, key)
    if info.get("state") != "success":
        raise ProviderError(f"kie task {task_id} failed: {info.get('failCode')}: {info.get('failMsg')}")

    is_video = kie.is_video_model(model)
    ext, kind, mime = (".mp4", "video", "video/mp4") if is_video else (".png", "image", "image/png")
    work = shell.workdir("kie")
    asset_ids, urls = [], []
    try:
        for i, url in enumerate(kie.result_urls(info)):
            dest = os.path.join(work, f"result_{i}{ext}")
            meta = {"model": model, "source_url": url, "purpose": inp.get("purpose"),
                    "beat": inp.get("beat"), "group": inp.get("group"), "task_id": task_id}
            try:
                kie.download(url, dest)
            except Exception as exc:  # noqa: BLE001 — CDN block / transient: keep the provider url
                meta["download_error"] = str(exc)[:200]
                asset = R.create_asset(store, ws, kind, mime, f"jobs/{job['id']}/missing_{i}{ext}",
                                       job_id=job["id"], meta=meta)
                asset = store.update("asset", ws, asset["id"], url=url)
            else:
                asset = R.put_file_asset(store, ws, dest, f"jobs/{job['id']}/result_{i}{ext}",
                                         kind=kind, mime=mime, job_id=job["id"], meta=meta)
            asset_ids.append(asset["id"])
            urls.append(asset["url"])
    finally:
        _cleanup(work)

    credits = info.get("creditsConsumed")
    R.record_cost(store, ws, job["id"], "kie", credits, "credits", kie.credits_to_usd(credits),
                  note=model)
    return {"asset_ids": asset_ids, "asset_urls": urls, "credits_consumed": credits,
            "usd": kie.credits_to_usd(credits), "task_id": task_id,
            "purpose": inp.get("purpose"), "beat": inp.get("beat"), "group": inp.get("group")}


# ---------------------------------------------------------------------------

def eleven_vo(store: Store, job: dict) -> Output:
    """input: {text, voice (name|id), with_timestamps?, pronunciation_fixes?}.
    ONE continuous take; over 5k chars it splits at a paragraph boundary and
    stitches with ffmpeg. Never per-line."""
    ws = _ws(job)
    inp = job.get("input") or {}
    key = get_key("elevenlabs", ws, store)
    voice_id = R.resolve_voice(store, ws, inp.get("voice") or inp.get("voice_id") or "")
    if not voice_id:
        raise ProviderError("eleven_vo needs a voice name or voice_id")
    fixes = {**R.pronunciation_fixes(store, ws), **(inp.get("pronunciation_fixes") or {})}
    text = elevenlabs.apply_pronunciation_fixes(inp.get("text") or "", fixes)
    if not text.strip():
        raise ProviderError("eleven_vo needs non-empty text")
    with_ts = bool(inp.get("with_timestamps"))

    work = shell.workdir("vo")
    try:
        takes = elevenlabs.split_at_paragraph(text)
        alignment = None
        final = os.path.join(work, "voiceover.mp3")
        if len(takes) == 1:
            audio, alignment = elevenlabs.tts_one_take(takes[0], voice_id, key, with_timestamps=with_ts)
            with open(final, "wb") as f:
                f.write(audio)
        else:
            paths = []
            for i, chunk in enumerate(takes):
                p = os.path.join(work, f"take_{i + 1:02d}.mp3")
                audio, _ = elevenlabs.tts_one_take(chunk, voice_id, key, with_timestamps=False)
                with open(p, "wb") as f:
                    f.write(audio)
                paths.append(p)
            elevenlabs.stitch(paths, final)

        asset = R.put_file_asset(store, ws, final, f"jobs/{job['id']}/voiceover.mp3", kind="audio",
                                 mime="audio/mpeg", job_id=job["id"],
                                 meta={"voice_id": voice_id, "model": elevenlabs.MODEL_V3,
                                       "n_takes": len(takes), "settings": elevenlabs.CREATIVE,
                                       "chars": len(text)})
        out = {"asset_id": asset["id"], "asset_url": asset["url"], "voice_id": voice_id,
               "n_takes": len(takes), "chars": len(text), "alignment_asset_id": None}
        if alignment is not None:
            al = R.put_bytes_asset(store, ws, json.dumps(alignment).encode(),
                                   f"jobs/{job['id']}/alignment.json", kind="alignment",
                                   mime="application/json", job_id=job["id"],
                                   meta={"audio_asset_id": asset["id"]})
            out["alignment_asset_id"] = al["id"]
        R.record_cost(store, ws, job["id"], "elevenlabs", len(text), "characters", None,
                      note=elevenlabs.MODEL_V3)
        return out
    finally:
        _cleanup(work)


def eleven_clone(store: Store, job: dict) -> Output:
    """input: {name, asset_ids, description?, tags?}. Clones from every asset
    (video assets are demuxed to mp3 first) and registers a 'voice' record."""
    ws = _ws(job)
    inp = job.get("input") or {}
    name = inp.get("name") or ""
    if not name:
        raise ProviderError("eleven_clone needs a name")
    for v in store.find("voice", ws, name=name):
        return {"voice_id": v["voice_id"], "voice_record_id": v["id"], "name": name, "existing": True}
    key = get_key("elevenlabs", ws, store)
    work = shell.workdir("clone")
    try:
        audio_paths = []
        for aid in inp.get("asset_ids") or []:
            asset = _asset(store, job, aid)
            path = R.asset_path(store, asset)
            ext = os.path.splitext(asset.get("storage_key") or "")[1].lower()
            if (asset.get("mime") or "").startswith("video/") or ext in elevenlabs.VIDEO_EXTENSIONS:
                audio_paths.append(elevenlabs.extract_audio(path, work))
            else:
                audio_paths.append(path)
        voice_id = elevenlabs.clone_voice(name, audio_paths, key, description=inp.get("description", ""))
        rec = R.register_voice(store, ws, name, voice_id, description=inp.get("description", ""),
                               source_asset_ids=list(inp.get("asset_ids") or []),
                               tags=list(inp.get("tags") or []))
        return {"voice_id": voice_id, "voice_record_id": rec["id"], "name": name, "existing": False}
    finally:
        _cleanup(work)


# ---------------------------------------------------------------------------

def heygen_avatar(store: Store, job: dict) -> Output:
    """input: {audio_asset_id, avatar_id, title?, aspect_ratio?, resolution?, engine?}.
    Uploads OUR audio, submits a v3 render, polls, downloads the mp4."""
    require_job_board(store, job)
    ws = _ws(job)
    inp = job.get("input") or {}
    key = get_key("heygen", ws, store)
    audio = _asset(store, job, inp["audio_asset_id"])
    audio_asset_id = heygen.upload_audio(R.asset_path(store, audio), key)
    require_job_board(store, job)
    video_id = heygen.create_video(inp["avatar_id"], audio_asset_id, key,
                                   title=inp.get("title") or "adengine",
                                   aspect_ratio=inp.get("aspect_ratio") or "9:16",
                                   resolution=inp.get("resolution") or "1080p",
                                   engine=inp.get("engine") or "avatar_v")
    R.update_job(store, ws, job["id"], external_task_id=video_id,
                 output={"heygen_audio_asset_id": audio_asset_id, "video_id": video_id})
    data = heygen.wait_for_video(video_id, key)
    if data.get("status") != "completed":
        err = json.dumps(data.get("error") or data)[:500]
        if heygen.is_credit_error(err):
            raise CreditRefire(err)
        raise ProviderError(f"HeyGen render failed: {err}")

    url = data.get("video_url")
    work = shell.workdir("heygen")
    try:
        meta = {"video_id": video_id, "avatar_id": inp["avatar_id"], "source_url": url,
                "engine": inp.get("engine") or "avatar_v"}
        if url:
            dest = heygen.download(url, os.path.join(work, "avatar.mp4"))
            asset = R.put_file_asset(store, ws, dest, f"jobs/{job['id']}/avatar.mp4", kind="video",
                                     mime="video/mp4", job_id=job["id"], meta=meta)
        else:
            raise ProviderError("HeyGen completed without a video_url")
    finally:
        _cleanup(work)
    R.record_cost(store, ws, job["id"], "heygen", None, "api_credits", None, note="v3 render")
    return {"asset_id": asset["id"], "asset_url": asset["url"], "video_id": video_id,
            "heygen_audio_asset_id": audio_asset_id}


class CreditRefire(ProviderError):
    """HeyGen credit failure: automatic top-up fires on the rejected render, so
    the right response is to re-fire the job, not to report a hard block."""
    should_refire = True


HANDLERS = {
    "grade_edit_style": edit_review.run_grade,
    "review_video_frames": review_video_frames,
    "noop": noop,
    "ingest_reference": ingest_reference,
    "watch_reference": watch_reference,
    "analyze_video": analyze_video,
    "kie_generate": kie_generate,
    "eleven_vo": eleven_vo,
    "eleven_clone": eleven_clone,
    "heygen_avatar": heygen_avatar,
}
