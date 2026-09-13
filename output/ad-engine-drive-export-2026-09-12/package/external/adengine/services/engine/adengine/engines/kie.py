"""kie.ai adapter — Seedance / Kling / GPT Image 2 / Nano Banana.

Pure provider layer: it builds requests and interprets responses. The worker
(adengine.workers.tasks.kie_generate) owns job state, polling, downloads and
cost rows. Nothing here touches the Store.

Hard-won quirks baked in so no caller relearns them:
  - createTask pre-authorises ~3x the eventual charge for seedance-2 (not 2.5).
    Always read balance() before firing.
  - LOW BALANCE IS A HARD STOP. kie's automatic top-up cannot be relied on: a
    task fired against an insufficient balance fails rather than topping up,
    so preflight treats an insufficient balance as blocking, never as a warning.
  - Upload MUST go through `curl -F`. A hand-rolled urllib multipart body gets a
    flat 403 from kie's WAF.
  - recordInfo echoes the prompt with raw control chars -> json.loads(strict=False).
  - python.org macOS builds lack system CAs -> SSL context from certifi.
  - Failed tasks are not charged.
"""
from __future__ import annotations

import json
import os
import ssl
import time
import urllib.error
import urllib.request

from adengine.core.errors import ProviderError
from adengine.core.settings import settings
from adengine.engines import shell

try:  # macOS python.org builds lack system CAs — use certifi
    import certifi
    SSL_CTX = ssl.create_default_context(cafile=certifi.where())
except ImportError:  # pragma: no cover
    SSL_CTX = ssl.create_default_context()

KIE_API = "https://api.kie.ai/api/v1"
KIE_UPLOAD_URL = "https://kieai.redpandaai.co/api/file-stream-upload"

VIDEO_MODELS = {"bytedance/seedance-2", "bytedance/seedance-2-5", "kling-3.0/video"}
IMAGE_MODEL_I2I = "gpt-image-2-image-to-image"
IMAGE_MODEL_T2I = "gpt-image-2-text-to-image"
IMAGE_MODELS = {IMAGE_MODEL_I2I, IMAGE_MODEL_T2I}
DEFAULT_VIDEO_MODEL = "bytedance/seedance-2-5"

# credits per second of generated video, for PRE-FLIGHT budget checks only.
# Prefer the provider's reported creditsConsumed for the ledger.
KNOWN_RATES_PER_SECOND = {
    "bytedance/seedance-2-5": 63.0,   # flat, 720p + audio
    "bytedance/seedance-2": 41.0,     # actual charge; pre-auth reserves ~3x this
    "kling-3.0/video": 14.0,
}

TERMINAL_STATES = {"success", "fail"}


def is_video_model(model: str) -> bool:
    return model in VIDEO_MODELS or "/video" in model or "seedance" in model or "kling" in model


def estimate_credits(model: str, duration_s: float | None) -> float | None:
    if duration_s is None:
        return None
    rate = KNOWN_RATES_PER_SECOND.get(model)
    return round(rate * duration_s, 2) if rate is not None else None


def credits_to_usd(credits: float | None) -> float | None:
    return None if credits is None else round(credits * settings.kie_credit_usd, 4)


def _api(method: str, url: str, key: str, payload: dict | None = None) -> dict:
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {key}")
    if data:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=120, context=SSL_CTX) as r:
            # strict=False: kie echoes prompts back with raw control chars
            return json.loads(r.read().decode("utf-8", "replace"), strict=False)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")[:300] if exc.fp else ""
        raise ProviderError(f"kie HTTP {exc.code}: {body}")
    except urllib.error.URLError as exc:
        raise ProviderError(f"kie unreachable: {exc.reason}")


def balance(key: str) -> float | None:
    """Current credit balance, or None if the read failed. Read before every
    generate: an insufficient balance is a hard stop."""
    try:
        return _api("GET", f"{KIE_API}/chat/credit", key).get("data")
    except (ProviderError, OSError, ValueError):
        return None


def upload(local_path: str, key: str, upload_path: str = "adengine",
           attempts: int = 4, sleep=time.sleep) -> str:
    """Upload a file to kie's temp storage (~24h-3d TTL) and return its
    downloadUrl. curl -F only — see the module docstring."""
    last = ""
    name = os.path.basename(local_path).replace(" ", "_")
    for attempt in range(attempts):
        if attempt:
            sleep(30 * attempt)
        out = shell.run([
            settings.curl, "-s", "-X", "POST", KIE_UPLOAD_URL,
            "-H", f"Authorization: Bearer {key}",
            "-F", f"file=@{local_path}",
            "-F", f"uploadPath={upload_path}",
            "-F", f"fileName={int(time.time())}-{name}",
        ], timeout=600)
        try:
            resp = json.loads(out.stdout)
        except ValueError:
            last = out.stdout or out.stderr
            continue
        url = (resp.get("data") or {}).get("downloadUrl")
        if url:
            return url
        last = out.stdout
    raise ProviderError(f"kie upload failed after {attempts} attempts: {last[:300]}")


def create_task(model: str, input_data: dict, key: str) -> str:
    """POST createTask. Returns the provider taskId. Does not wait."""
    resp = _api("POST", f"{KIE_API}/jobs/createTask", key, {"model": model, "input": input_data})
    if resp.get("code") != 200:
        raise ProviderError(f"kie createTask refused: {json.dumps(resp)[:400]}")
    return resp["data"]["taskId"]


def record_info(task_id: str, key: str) -> dict:
    """One poll. Returns the raw `data` object: state, resultJson, creditsConsumed, failCode, failMsg."""
    resp = _api("GET", f"{KIE_API}/jobs/recordInfo?taskId={task_id}", key)
    return resp.get("data") or {}


def result_urls(info: dict) -> list[str]:
    result = json.loads(info.get("resultJson") or "{}", strict=False)
    return list(result.get("resultUrls") or [])


def wait_for_task(task_id: str, key: str, poll_s: float = 10.0, timeout_s: float = 1800.0,
                  sleep=time.sleep) -> dict:
    """Poll recordInfo until a terminal state (worker-side only; tools never poll)."""
    deadline = time.monotonic() + timeout_s
    while True:
        info = record_info(task_id, key)
        if info.get("state") in TERMINAL_STATES:
            return info
        if time.monotonic() >= deadline:
            raise ProviderError(f"kie task {task_id} still {info.get('state')} after {timeout_s:.0f}s")
        sleep(poll_s)


def download(url: str, dest: str) -> str:
    return shell.curl_download(url, dest, timeout=600)
