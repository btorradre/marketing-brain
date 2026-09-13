"""Jobs / assets / costs / voices / references as Store records.

Replaces the SQLite registry. Every record carries workspace_id; assets carry a
storage_key (never a local path) and a url derived from it. Workers that need a
file call store.blob_path() themselves.

Job statuses: queued -> running -> completed | failed
"""
from __future__ import annotations

import mimetypes
import os
from typing import Any

from adengine.core.errors import NotFound
from adengine.core.store import Store

QUEUED, RUNNING, COMPLETED, FAILED = "queued", "running", "completed", "failed"
JOB_STATUSES = (QUEUED, RUNNING, COMPLETED, FAILED)

MIME_KIND = {"video": "video", "image": "image", "audio": "audio", "text": "text"}


def mime_for(path_or_name: str, default: str = "application/octet-stream") -> str:
    mime, _ = mimetypes.guess_type(path_or_name)
    return mime or default


def kind_for_mime(mime: str) -> str:
    return MIME_KIND.get((mime or "").split("/")[0], "file")


# ---- jobs

def create_job(store: Store, ws: str, kind: str, provider: str | None = None,
               input: dict | None = None, parent_id: str | None = None,
               status: str = QUEUED) -> dict:
    return store.create("job", ws, "job", kind=kind, provider=provider, status=status,
                        input=input or {}, output=None, cost=None, error=None,
                        parent_id=parent_id)


def get_job(store: Store, ws: str, job_id: str) -> dict:
    return store.get("job", ws, job_id)


def update_job(store: Store, ws: str, job_id: str, **fields: Any) -> dict:
    return store.update("job", ws, job_id, **fields)


def list_jobs(store: Store, ws: str, status: str | None = None, kind: str | None = None,
              provider: str | None = None, limit: int = 50) -> list[dict]:
    eq = {k: v for k, v in (("status", status), ("kind", kind), ("provider", provider)) if v}
    rows = store.find("job", ws, **eq)
    return rows[: max(1, int(limit))]


# ---- assets

def create_asset(store: Store, ws: str, kind: str, mime: str, storage_key: str,
                 job_id: str | None = None, meta: dict | None = None) -> dict:
    return store.create("asset", ws, "asset", kind=kind, mime=mime, storage_key=storage_key,
                        url=store.url(ws, storage_key), meta=meta or {}, job_id=job_id)


def put_bytes_asset(store: Store, ws: str, data: bytes, key: str, kind: str, mime: str,
                    job_id: str | None = None, meta: dict | None = None) -> dict:
    store.put_blob(ws, key, data, mime=mime)
    return create_asset(store, ws, kind, mime, key, job_id=job_id, meta=meta)


def put_file_asset(store: Store, ws: str, path: str, key: str, kind: str | None = None,
                   mime: str | None = None, job_id: str | None = None,
                   meta: dict | None = None) -> dict:
    mime = mime or mime_for(path)
    kind = kind or kind_for_mime(mime)
    with open(path, "rb") as f:
        store.put_blob(ws, key, iter(lambda: f.read(1 << 20), b""), mime=mime)
    meta = dict(meta or {})
    meta.setdefault("bytes", os.path.getsize(path))
    return create_asset(store, ws, kind, mime, key, job_id=job_id, meta=meta)


def get_asset(store: Store, ws: str, asset_id: str) -> dict:
    return store.get("asset", ws, asset_id)


def list_assets(store: Store, ws: str, job_id: str | None = None, kind: str | None = None,
                limit: int = 50) -> list[dict]:
    eq = {k: v for k, v in (("job_id", job_id), ("kind", kind)) if v}
    return store.find("asset", ws, **eq)[: max(1, int(limit))]


def asset_url(store: Store, asset: dict) -> str:
    return store.url(asset["workspace_id"], asset["storage_key"])


def asset_path(store: Store, asset: dict) -> str:
    """Worker-side only: local path of the asset's blob."""
    return store.blob_path(asset["workspace_id"], asset["storage_key"])


def public_asset(asset: dict) -> dict:
    """The tool-facing view: ids, url, kind, meta — no storage internals."""
    return {"id": asset["id"], "kind": asset.get("kind"), "mime": asset.get("mime"),
            "url": asset.get("url"), "job_id": asset.get("job_id"), "meta": asset.get("meta") or {},
            "created": asset.get("created")}


# ---- costs

def record_cost(store: Store, ws: str, job_id: str | None, provider: str,
                units: float | None, unit_name: str, usd: float | None,
                note: str | None = None) -> dict:
    return store.create("cost", ws, "cost", job_id=job_id, provider=provider, units=units,
                        unit_name=unit_name, usd=usd, note=note)


def cost_summary(store: Store, ws: str, job_id: str | None = None) -> dict:
    rows = store.find("cost", ws, **({"job_id": job_id} if job_id else {}))
    by_provider: dict[str, dict] = {}
    total_usd = 0.0
    for r in rows:
        p = by_provider.setdefault(r["provider"], {"units": 0.0, "unit_name": r.get("unit_name"),
                                                    "usd": 0.0, "n": 0})
        p["units"] += float(r.get("units") or 0)
        p["usd"] += float(r.get("usd") or 0)
        p["n"] += 1
        total_usd += float(r.get("usd") or 0)
    for p in by_provider.values():
        p["units"] = round(p["units"], 4)
        p["usd"] = round(p["usd"], 4)
    return {"providers": by_provider, "total_usd": round(total_usd, 4), "n": len(rows)}


# ---- voices (the ElevenLabs registry, per workspace)

def register_voice(store: Store, ws: str, name: str, voice_id: str, description: str = "",
                   source_asset_ids: list[str] | None = None, tags: list[str] | None = None,
                   provider: str = "elevenlabs") -> dict:
    for existing in store.find("voice", ws, name=name):
        return store.update("voice", ws, existing["id"], voice_id=voice_id,
                            description=description, source_asset_ids=source_asset_ids or [],
                            tags=tags or [])
    return store.create("voice", ws, "voice", name=name, voice_id=voice_id, provider=provider,
                        description=description, source_asset_ids=source_asset_ids or [],
                        tags=tags or [])


def list_voices(store: Store, ws: str) -> list[dict]:
    return store.find("voice", ws)


def resolve_voice(store: Store, ws: str, name_or_id: str) -> str:
    """Registry name -> provider voice id; stock names -> stock ids; raw ids pass through."""
    from adengine.engines.elevenlabs import STOCK_VOICES
    for v in store.find("voice", ws, name=name_or_id):
        return v["voice_id"]
    for v in store.find("voice", ws):
        if v.get("id") == name_or_id or v.get("voice_id") == name_or_id:
            return v["voice_id"]
    if name_or_id.lower() in STOCK_VOICES:
        return STOCK_VOICES[name_or_id.lower()]
    return name_or_id


def pronunciation_fixes(store: Store, ws: str) -> dict[str, str]:
    """Workspace 'pronunciation' records: {plain, respelled}. TTS input only."""
    return {r["plain"]: r["respelled"] for r in store.find("pronunciation", ws)
            if r.get("plain") and r.get("respelled")}


# ---- references

def create_reference(store: Store, ws: str, source: str, asset_id: str | None = None,
                     status: str = "pending", brand_id: str | None = None,
                     manifest: dict | None = None) -> dict:
    return store.create("reference", ws, "ref", source=source, asset_id=asset_id,
                        brand_id=brand_id, manifest=manifest, status=status)


def get_reference(store: Store, ws: str, reference_id: str) -> dict:
    try:
        return store.get("reference", ws, reference_id)
    except NotFound:
        raise NotFound(f"reference {reference_id} not found")


def update_reference(store: Store, ws: str, reference_id: str, **fields: Any) -> dict:
    return store.update("reference", ws, reference_id, **fields)
