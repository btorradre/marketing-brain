"""kie.ai wrapper — the canonical gen platform (Seedance, Kling, GPT Image 2, Nano Banana).

Non-blocking by design: generate() fires createTask and returns immediately with
a job_id; status() does ONE poll and updates the registry. The caller (an MCP
tool call from Claude) decides its own polling cadence instead of a single tool
call blocking for minutes on a 30s Seedance render.

Hard-won quirks baked in here so no downstream code has to relearn them
(see reference_kie_api.md):
  - createTask pre-auths ~3x the eventual charge for seedance-2 (not 2.5) —
    ALWAYS check balance() before firing.
  - AUTO TOP-UP IS BROKEN on this account. A low balance is a hard blocker,
    not a warning.
  - Upload MUST go through curl -F, never a hand-rolled urllib multipart body
    (that gets a flat 403 from kie's WAF).
  - recordInfo echoes the prompt with raw control chars -> json.loads(strict=False).
  - Failed tasks are not charged.
"""

import json
import os
import ssl
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import db
import cost_ledger

try:  # macOS python.org builds lack system CAs — use certifi
    import certifi
    SSL_CTX = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    SSL_CTX = ssl.create_default_context()

VAULT = Path(__file__).resolve().parents[4]
ENV_PATH = VAULT / ".env"
DOWNLOAD_DIR = Path(__file__).resolve().parent.parent / "data" / "downloads"

KIE_API = "https://api.kie.ai/api/v1"
KIE_UPLOAD_URL = "https://kieai.redpandaai.co/api/file-stream-upload"

VIDEO_MODELS = {"bytedance/seedance-2", "bytedance/seedance-2-5", "kling-3.0/video"}


def _env_key(name: str = "KIE_API_KEY") -> str:
    key = os.environ.get(name)
    if not key and ENV_PATH.exists():
        for line in ENV_PATH.read_text().splitlines():
            if line.strip().startswith(name + "="):
                key = line.strip().split("=", 1)[1]
                break
    if not key:
        raise RuntimeError(f"{name} not found in env or {ENV_PATH}")
    return key


def _api(method: str, url: str, payload: dict | None = None) -> dict:
    key = _env_key()
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {key}")
    if data:
        req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=120, context=SSL_CTX) as r:
        # strict=False: kie echoes prompts back with raw control chars
        return json.loads(r.read().decode("utf-8", "replace"), strict=False)


def balance() -> float | None:
    """Current kie.ai credit balance. Check this before every generate() —
    auto top-up is broken on this account, so a low balance is a hard stop."""
    try:
        resp = _api("GET", f"{KIE_API}/chat/credit")
        return resp.get("data")
    except (urllib.error.URLError, OSError, ValueError):
        return None


def upload(local_path: str, upload_path: str = "ad-engine") -> str:
    """Uploads a local file to kie's temp storage (~24h-3d TTL). Returns a
    downloadUrl to pass as a reference_*_url. curl -F only — see module docstring."""
    key = _env_key()
    last = ""
    for attempt in range(4):
        if attempt:
            time.sleep(30 * attempt)
        out = subprocess.run(
            ["curl", "-s", "-X", "POST", KIE_UPLOAD_URL,
             "-H", f"Authorization: Bearer {key}",
             "-F", f"file=@{local_path}",
             "-F", f"uploadPath={upload_path}",
             "-F", f"fileName={int(time.time())}-{Path(local_path).name.replace(' ', '_')}"],
            capture_output=True, text=True,
        )
        try:
            resp = json.loads(out.stdout)
        except ValueError:
            last = out.stdout or out.stderr
            continue
        if resp.get("data", {}).get("downloadUrl"):
            return resp["data"]["downloadUrl"]
        last = out.stdout
    raise RuntimeError(f"kie upload failed for {local_path} after 4 attempts: {last[:300]}")


def _download(url: str, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["curl", "-sL", "-o", str(dest), url], check=True,
                    capture_output=True, timeout=120)
    if dest.stat().st_size == 0:
        raise RuntimeError(f"downloaded 0 bytes from {url}")
    return dest


def generate(model: str, input_data: dict, brand: str | None = None,
             concept: str | None = None) -> dict:
    """Fires createTask, does NOT wait. Returns {job_id, external_task_id, status}.
    Poll with status(job_id)."""
    job_id = db.create_job("kie", "generate", model=model, brand=brand,
                            concept=concept, input_data=input_data)
    resp = _api("POST", f"{KIE_API}/jobs/createTask", {"model": model, "input": input_data})
    if resp.get("code") != 200:
        db.update_job(job_id, status="fail", error=json.dumps(resp))
        return {"job_id": job_id, "status": "fail", "error": resp}
    task_id = resp["data"]["taskId"]
    db.update_job(job_id, status="running", external_task_id=task_id)
    return {"job_id": job_id, "external_task_id": task_id, "status": "running"}


def status(job_id: str) -> dict:
    """One poll. Downloads results and logs actual cost on first success."""
    job = db.get_job(job_id)
    if job is None:
        raise ValueError(f"unknown job_id {job_id}")
    if job["status"] in ("success", "fail"):
        return job

    resp = _api("GET", f"{KIE_API}/jobs/recordInfo?taskId={job['external_task_id']}")
    d = resp.get("data", {})
    state = d.get("state")

    if state == "success":
        result = json.loads(d.get("resultJson") or "{}", strict=False)
        urls = result.get("resultUrls") or []
        asset_ids = []
        for i, url in enumerate(urls):
            ext = ".mp4" if job["model"] in VIDEO_MODELS else ".png"
            dest = DOWNLOAD_DIR / job_id / f"result_{i}{ext}"
            try:
                _download(url, dest)
                local_path = str(dest)
            except (subprocess.CalledProcessError, subprocess.TimeoutExpired, RuntimeError):
                local_path = None  # kie CDN block or transient failure — url still in meta
            kind = "video" if job["model"] in VIDEO_MODELS else "image"
            asset_id = db.create_asset(job_id, kind, path=local_path, source_url=url,
                                        brand=job["brand"], concept=job["concept"])
            asset_ids.append(asset_id)
        credits = d.get("creditsConsumed")
        cost_ledger.log_cost(job_id, "kie", credits=credits, note=job["model"])
        db.update_job(job_id, status="success",
                       output_data={"asset_ids": asset_ids, "credits_consumed": credits})
    elif state == "fail":
        db.update_job(job_id, status="fail",
                       error=f"{d.get('failCode')}: {d.get('failMsg')}")
    # else: still waiting/queuing/generating — leave as running, caller polls again

    return db.get_job(job_id)
