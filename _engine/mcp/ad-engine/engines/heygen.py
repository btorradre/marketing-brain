"""HeyGen wrapper — avatar video driven by OUR OWN audio.

Two hard-won constraints shape this whole module (learned on the FerraVital
nurse replica run, 2026-08-08/09):

1. EVERY CALL GOES THROUGH curl. Python's SSL store on this machine cannot
   verify HeyGen's hosts. Do not "clean this up" into requests.

2. CREDIT POOLS ARE SPLIT AND THIS IS THE #1 GOTCHA. API rendering consumes
   `api` credits ONLY. A fat `generative_credit` balance does nothing — the
   render fails with MOVIO_PAYMENT_INSUFFICIENT_CREDIT. Worse, the failure
   surfaces at POLL time, not submit time: /v2/video/generate hands back a
   video_id happily and only the status poll reports failed.
   Auto top-up fires on a REJECTED RENDER, never on a quota read — so a
   credit failure means RE-FIRE, not "hard blocked". check_quota() reads the
   right pool and status() flags the re-fire case explicitly.

Preferred path is v3 + Avatar V: 1080x1920, far more natural expression and
head motion than the v2 talking-photo path. The key move is `audio_asset_id` —
upload an ElevenLabs mp3 to /v1/asset and HeyGen lip-syncs the avatar to that
exact file. No HeyGen voice, no script re-read, so the VO stays the one
continuous take we generated. Mutually exclusive with script+voice_id.

v2 is legacy (sunsets 2026-10-31) and its av4 path has a separate payload
shape (image_key + video_title, NOT talking_photo_id) — not implemented here
on purpose; use v3 unless a look is ineligible.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import db

VAULT = Path(__file__).resolve().parents[4]
ENV_PATH = VAULT / ".env"
DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "heygen"

API_BASE = "https://api.heygen.com"
UPLOAD_BASE = "https://upload.heygen.com"

CREDIT_ERROR_MARKERS = ("INSUFFICIENT_CREDIT", "requires 'api' credits", "api credits")


def _api_key() -> str:
    key = os.environ.get("HEYGEN_API_KEY")
    if not key and ENV_PATH.exists():
        for line in ENV_PATH.read_text().splitlines():
            if line.strip().startswith("HEYGEN_API_KEY="):
                key = line.strip().split("=", 1)[1]
                break
    if not key:
        raise RuntimeError(f"HEYGEN_API_KEY not found in env or {ENV_PATH}")
    return key


def _curl(method: str, url: str, payload: dict | None = None,
          extra: list[str] | None = None) -> dict:
    """All HeyGen traffic goes through curl — see module docstring."""
    cmd = ["curl", "-s", "-X", method, url, "-H", f"X-Api-Key: {_api_key()}"]
    if payload is not None:
        cmd += ["-H", "Content-Type: application/json", "-d", json.dumps(payload)]
    if extra:
        cmd += extra
    out = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    try:
        return json.loads(out.stdout)
    except ValueError:
        raise RuntimeError(f"HeyGen non-JSON response: {(out.stdout or out.stderr)[:300]}")


def check_quota() -> dict:
    """Reads the credit pools. ONLY the `api` figure matters for rendering —
    generative_credit is the UI's pool and is irrelevant here. Note a quota
    read never triggers auto top-up."""
    resp = _curl("GET", f"{API_BASE}/v2/user/remaining_quota")
    details = (resp.get("data") or {}).get("details") or {}
    return {"api": details.get("api"), "seat": details.get("seat"),
            "generative_credit": details.get("generative_credit"),
            "plan_credit": details.get("plan_credit"),
            "note": "API rendering consumes 'api' credits only"}


def list_avatars(own_only: bool = True) -> dict:
    """own_only reads the account's own avatar groups (newest first);
    otherwise the full stock catalog."""
    if own_only:
        return _curl("GET", f"{API_BASE}/v2/avatar_group.list")
    return _curl("GET", f"{API_BASE}/v2/avatars")


def check_avatar_v_eligible(look_id: str) -> dict:
    """Avatar V is the quality path — verify supported_api_engines contains
    avatar_v before submitting with that engine."""
    resp = _curl("GET", f"{API_BASE}/v3/avatars/looks/{look_id}")
    engines = ((resp.get("data") or {}).get("supported_api_engines")) or []
    return {"look_id": look_id, "supported_api_engines": engines,
            "avatar_v_eligible": "avatar_v" in engines}


def upload_audio(local_path: str) -> str:
    """Uploads an mp3 (e.g. an ElevenLabs one-take VO) and returns the
    audio_asset_id HeyGen will lip-sync the avatar to."""
    out = subprocess.run(
        ["curl", "-s", "-X", "POST", f"{UPLOAD_BASE}/v1/asset",
         "-H", f"X-Api-Key: {_api_key()}", "-H", "Content-Type: audio/mpeg",
         "--data-binary", f"@{local_path}"],
        capture_output=True, text=True, timeout=300)
    try:
        resp = json.loads(out.stdout)
    except ValueError:
        raise RuntimeError(f"HeyGen upload non-JSON: {(out.stdout or out.stderr)[:300]}")
    asset_id = (resp.get("data") or {}).get("id")
    if not asset_id:
        raise RuntimeError(f"HeyGen upload returned no asset id: {str(resp)[:300]}")
    return asset_id


def generate(avatar_look_id: str, audio_asset_id: str, title: str = "ad-engine",
             aspect_ratio: str = "9:16", resolution: str = "1080p",
             engine: str = "avatar_v", brand: str | None = None,
             concept: str | None = None) -> dict:
    """Submits a v3 avatar render driven by our own audio. Non-blocking —
    poll with status(job_id). Remember a credit failure will NOT appear here;
    it appears at poll time."""
    job_id = db.create_job("heygen", "generate", model=f"v3/{engine}", brand=brand,
                            concept=concept,
                            input_data={"avatar_look_id": avatar_look_id,
                                        "audio_asset_id": audio_asset_id,
                                        "aspect_ratio": aspect_ratio,
                                        "resolution": resolution, "engine": engine})
    payload = {"type": "avatar", "avatar_id": avatar_look_id,
               "audio_asset_id": audio_asset_id, "aspect_ratio": aspect_ratio,
               "resolution": resolution, "engine": {"type": engine}, "title": title}
    resp = _curl("POST", f"{API_BASE}/v3/videos", payload)
    video_id = (resp.get("data") or {}).get("video_id") or (resp.get("data") or {}).get("id")
    if not video_id:
        db.update_job(job_id, status="fail", error=json.dumps(resp)[:500])
        return db.get_job(job_id)
    db.update_job(job_id, status="running", external_task_id=video_id)
    return db.get_job(job_id)


def status(job_id: str) -> dict:
    """One poll. Downloads the mp4 on success. On a credit failure this sets
    `should_refire: True` rather than treating it as terminal — auto top-up
    fires on the rejected render, so the correct response is to re-fire."""
    job = db.get_job(job_id)
    if job is None:
        raise ValueError(f"unknown job_id {job_id}")
    if job["status"] in ("success", "fail"):
        return job

    resp = _curl("GET", f"{API_BASE}/v3/videos/{job['external_task_id']}")
    data = resp.get("data") or {}
    state = data.get("status")

    if state == "completed":
        url = data.get("video_url")
        dest = DATA_DIR / job_id / "avatar.mp4"
        dest.parent.mkdir(parents=True, exist_ok=True)
        local_path = None
        if url:
            subprocess.run(["curl", "-sL", "-o", str(dest), url], check=True,
                            capture_output=True, timeout=600)
            if dest.exists() and dest.stat().st_size > 0:
                local_path = str(dest)
        asset_id = db.create_asset(job_id, "video", path=local_path, source_url=url,
                                    brand=job["brand"], concept=job["concept"])
        db.update_job(job_id, status="success",
                       output_data={"asset_id": asset_id, "video_url": url})
    elif state == "failed":
        err = json.dumps(data.get("error") or data)[:500]
        is_credit = any(marker in err for marker in CREDIT_ERROR_MARKERS)
        db.update_job(job_id, status="fail", error=err)
        result = db.get_job(job_id)
        result["should_refire"] = is_credit
        if is_credit:
            result["refire_note"] = (
                "Credit failure. Auto top-up fires on a rejected render (not on a "
                "quota read), so re-fire this generate call rather than reporting "
                "a hard block.")
        return result

    return db.get_job(job_id)
