"""fal.ai lip-sync backend — Sync.so's lipsync model, hosted on fal.

Drives the avatar's mouth from the ElevenLabs waveform. Uses the FAL_API_KEY
already in the vault .env and raw REST (no fal SDK needed), matching the pattern
the fabric-talking-head skill uses. Model is overridable via env
UGC_FAL_LIPSYNC_MODEL (default fal-ai/sync-lipsync).

Flow: upload silent (already audio-conformed) video + the audio stem to fal
storage -> queue the lipsync job -> poll -> download -> re-mux OUR audio stem so
the delivered audio is exactly the ElevenLabs stem (pristine, untouched).
"""
import os
import time

import requests

from util import RetryableError, log, with_backoff
from video_ops import mux_audio

INITIATE_URL = "https://rest.alpha.fal.ai/storage/upload/initiate"
DEFAULT_MODEL = "fal-ai/sync-lipsync"
MIME = {".mp4": "video/mp4", ".mov": "video/quicktime", ".webm": "video/webm",
        ".mp3": "audio/mpeg", ".wav": "audio/wav", ".m4a": "audio/mp4",
        ".aac": "audio/aac", ".flac": "audio/flac", ".ogg": "audio/ogg"}


def _key():
    k = os.environ.get("FAL_API_KEY")
    if not k:
        raise SystemExit("[ugc-forge] FAL_API_KEY not set — needed for the fal lip-sync backend.")
    return k


def _headers():
    return {"Authorization": f"Key {_key()}"}


def upload(path) -> str:
    """Two-step fal storage upload: initiate -> PUT bytes -> return file_url."""
    ext = os.path.splitext(path)[1].lower()
    mime = MIME.get(ext, "application/octet-stream")
    name = os.path.basename(path)

    def _initiate():
        resp = requests.post(INITIATE_URL,
                             headers={**_headers(), "Content-Type": "application/json"},
                             json={"content_type": mime, "file_name": name}, timeout=60)
        if resp.status_code == 429 or resp.status_code >= 500:
            raise RetryableError(f"fal initiate HTTP {resp.status_code}")
        if resp.status_code != 200:
            raise SystemExit(f"[ugc-forge] fal upload initiate failed {resp.status_code}: {resp.text[:200]}")
        d = resp.json()
        return d["upload_url"], d["file_url"]

    upload_url, file_url = with_backoff(_initiate, label="fal.initiate")

    def _put():
        with open(path, "rb") as f:
            resp = requests.put(upload_url, data=f.read(),
                                headers={"Content-Type": mime}, timeout=300)
        if resp.status_code in (429,) or resp.status_code >= 500:
            raise RetryableError(f"fal put HTTP {resp.status_code}")
        if resp.status_code not in (200, 201, 204):
            raise SystemExit(f"[ugc-forge] fal upload PUT failed {resp.status_code}: {resp.text[:200]}")
        return True

    with_backoff(_put, label="fal.put")
    return file_url


def _submit(model, payload):
    queue = f"https://queue.fal.run/{model}"

    def _do():
        resp = requests.post(queue, headers=_headers(), json=payload, timeout=60)
        if resp.status_code == 429 or resp.status_code >= 500:
            raise RetryableError(f"fal submit HTTP {resp.status_code}")
        if resp.status_code != 200:
            raise SystemExit(f"[ugc-forge] fal submit failed {resp.status_code}: {resp.text[:200]}")
        return resp.json().get("request_id")

    return with_backoff(_do, label="fal.submit")


def _poll(model, request_id, *, max_wait=900, interval=8):
    status_url = f"https://queue.fal.run/{model}/requests/{request_id}/status"
    result_url = f"https://queue.fal.run/{model}/requests/{request_id}"
    start = time.time()
    while time.time() - start < max_wait:
        r = requests.get(status_url, headers=_headers(), timeout=30)
        if r.status_code == 200:
            status = r.json().get("status", "")
            if status == "COMPLETED":
                res = requests.get(result_url, headers=_headers(), timeout=60).json()
                vid = res.get("video") or {}
                url = vid.get("url") if isinstance(vid, dict) else None
                if not url:
                    raise SystemExit(f"[ugc-forge] fal lipsync: no video in result {res}")
                return url
            if status == "FAILED":
                raise RuntimeError(f"fal lipsync FAILED: {r.json()}")
        time.sleep(interval)
    raise RuntimeError("fal lipsync timed out")


def _download(url, out_path):
    r = requests.get(url, timeout=300)
    r.raise_for_status()
    with open(out_path, "wb") as f:
        f.write(r.content)
    return out_path


def lipsync(video_path, audio_path, out_path):
    """Lip-sync `video_path` to `audio_path` via fal; deliver with OUR audio."""
    model = os.environ.get("UGC_FAL_LIPSYNC_MODEL", DEFAULT_MODEL)
    log(f"fal lipsync ({model}): uploading…")
    video_url = upload(video_path)
    audio_url = upload(audio_path)
    payload = {"video_url": video_url, "audio_url": audio_url, "sync_mode": "cut_off"}
    rid = _submit(model, payload)
    log(f"fal lipsync: job {rid} queued; polling…")
    result_url = _poll(model, rid)
    tmp = str(out_path) + ".fal.mp4"
    _download(result_url, tmp)
    # Re-mux our exact ElevenLabs stem so the delivered audio is pristine.
    mux_audio(tmp, audio_path, out_path)
    try:
        os.remove(tmp)
    except OSError:
        pass
    log(f"fal lipsync -> {os.path.basename(str(out_path))}")
    return str(out_path)
