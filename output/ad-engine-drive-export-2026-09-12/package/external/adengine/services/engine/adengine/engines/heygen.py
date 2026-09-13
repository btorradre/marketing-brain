"""HeyGen adapter — avatar video driven by OUR OWN audio.

Two hard-won constraints shape this whole module:

1. EVERY CALL GOES THROUGH curl. Python's SSL store cannot verify HeyGen's
   hosts on some builds. Do not "clean this up" into requests.

2. CREDIT POOLS ARE SPLIT AND THIS IS THE #1 GOTCHA. API rendering consumes
   `api` credits ONLY. A fat `generative_credit` balance does nothing — the
   render fails with MOVIO_PAYMENT_INSUFFICIENT_CREDIT. Worse, the failure
   surfaces at POLL time, not submit time: /v3/videos hands back a video_id
   happily and only the status poll reports failed. Automatic top-up fires on
   a REJECTED RENDER, never on a quota read — so a credit failure means
   RE-FIRE, not "hard blocked". check_quota() reads the right pool and
   is_credit_error() flags the re-fire case explicitly.

Preferred path is v3 + Avatar V: 1080x1920, far more natural expression and
head motion than the v2 talking-photo path. The key move is `audio_asset_id` —
upload an ElevenLabs mp3 to /v1/asset and HeyGen lip-syncs the avatar to that
exact file. No HeyGen voice, no script re-read, so the VO stays the one
continuous take we generated. Mutually exclusive with script+voice_id.

v2 is legacy (sunsets 2026-10-31); not implemented here on purpose.
"""
from __future__ import annotations

import json
import time

from adengine.core.errors import ProviderError
from adengine.core.settings import settings
from adengine.engines import shell

API_BASE = "https://api.heygen.com"
UPLOAD_BASE = "https://upload.heygen.com"

CREDIT_ERROR_MARKERS = ("INSUFFICIENT_CREDIT", "requires 'api' credits", "api credits")
REFIRE_NOTE = ("Credit failure. Automatic top-up fires on a rejected render (not on a "
               "quota read), so re-fire this generate call rather than reporting a hard block.")
TERMINAL_STATES = {"completed", "failed"}


def _curl(method: str, url: str, key: str, payload: dict | None = None,
          extra: list[str] | None = None) -> dict:
    """All HeyGen traffic goes through curl — see module docstring."""
    args = ["-X", method, url, "-H", f"X-Api-Key: {key}"]
    if payload is not None:
        args += ["-H", "Content-Type: application/json", "-d", json.dumps(payload)]
    if extra:
        args += extra
    return shell.curl_json(args, timeout=180)


def check_quota(key: str) -> dict:
    """Reads the credit pools. ONLY the `api` figure matters for rendering —
    generative_credit is the UI's pool and is irrelevant here. A quota read
    never triggers automatic top-up."""
    resp = _curl("GET", f"{API_BASE}/v2/user/remaining_quota", key)
    details = (resp.get("data") or {}).get("details") or {}
    return {"api": details.get("api"), "seat": details.get("seat"),
            "generative_credit": details.get("generative_credit"),
            "plan_credit": details.get("plan_credit"),
            "note": "API rendering consumes 'api' credits only"}


def list_avatars(key: str, own_only: bool = True) -> dict:
    """own_only reads the account's own avatar groups (newest first);
    otherwise the full stock catalog."""
    if own_only:
        return _curl("GET", f"{API_BASE}/v2/avatar_group.list", key)
    return _curl("GET", f"{API_BASE}/v2/avatars", key)


def check_avatar_v_eligible(look_id: str, key: str) -> dict:
    """Avatar V is the quality path — verify supported_api_engines contains
    avatar_v before submitting with that engine."""
    resp = _curl("GET", f"{API_BASE}/v3/avatars/looks/{look_id}", key)
    engines = ((resp.get("data") or {}).get("supported_api_engines")) or []
    return {"look_id": look_id, "supported_api_engines": engines,
            "avatar_v_eligible": "avatar_v" in engines}


def upload_audio(local_path: str, key: str) -> str:
    """Uploads an mp3 (e.g. an ElevenLabs one-take VO) and returns the
    audio_asset_id HeyGen will lip-sync the avatar to."""
    resp = shell.curl_json([
        "-X", "POST", f"{UPLOAD_BASE}/v1/asset",
        "-H", f"X-Api-Key: {key}", "-H", "Content-Type: audio/mpeg",
        "--data-binary", f"@{local_path}",
    ], timeout=300)
    asset_id = (resp.get("data") or {}).get("id")
    if not asset_id:
        raise ProviderError(f"HeyGen upload returned no asset id: {str(resp)[:300]}")
    return asset_id


def create_video(avatar_look_id: str, audio_asset_id: str, key: str, title: str = "adengine",
                 aspect_ratio: str = "9:16", resolution: str = "1080p",
                 engine: str = "avatar_v") -> str:
    """Submits a v3 avatar render driven by our own audio. Returns video_id.
    A credit failure will NOT appear here; it appears at poll time."""
    payload = {"type": "avatar", "avatar_id": avatar_look_id,
               "audio_asset_id": audio_asset_id, "aspect_ratio": aspect_ratio,
               "resolution": resolution, "engine": {"type": engine}, "title": title}
    resp = _curl("POST", f"{API_BASE}/v3/videos", key, payload)
    data = resp.get("data") or {}
    video_id = data.get("video_id") or data.get("id")
    if not video_id:
        raise ProviderError(f"HeyGen refused render: {json.dumps(resp)[:500]}")
    return video_id


def video_status(video_id: str, key: str) -> dict:
    resp = _curl("GET", f"{API_BASE}/v3/videos/{video_id}", key)
    return resp.get("data") or {}


def is_credit_error(err: str) -> bool:
    return any(marker in err for marker in CREDIT_ERROR_MARKERS)


def wait_for_video(video_id: str, key: str, poll_s: float = 15.0, timeout_s: float = 3600.0,
                   sleep=time.sleep) -> dict:
    deadline = time.monotonic() + timeout_s
    while True:
        data = video_status(video_id, key)
        if data.get("status") in TERMINAL_STATES:
            return data
        if time.monotonic() >= deadline:
            raise ProviderError(f"HeyGen video {video_id} still {data.get('status')} after {timeout_s:.0f}s")
        sleep(poll_s)


def download(url: str, dest: str) -> str:
    return shell.curl_download(url, dest, timeout=600)
