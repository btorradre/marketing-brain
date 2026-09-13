"""Shared approval checks for tools and workers. No provider calls occur here."""
from adengine.core.errors import GateRefused, NotFound


def require_board(store, workspace: str, slug: str | None, asset_ids=(), version=None) -> dict:
    if not slug or not slug.strip():
        raise GateRefused("approval gate: board_slug is required")
    try:
        from adengine.dr.boards import approval_status
    except ImportError as exc:
        raise GateRefused("approval gate: board is not approved; approval service unavailable") from exc
    try:
        status = approval_status(store, workspace, slug)
    except NotFound as exc:
        raise GateRefused(f"approval gate: board '{slug}' is not approved") from exc
    if not status.get("approved"):
        raise GateRefused(f"approval gate: board '{slug}' is not approved "
                          f"(pending: {status.get('pending', [])}, rejected: {status.get('rejected', [])}, "
                          f"missing: {status.get('missing', [])})", status)
    if version is not None and version != status.get("version"):
        raise GateRefused("approval gate: board changed after this job was queued; enqueue again",
                          {"queued_version": version, "current_version": status.get("version")})
    approved_ids = {c["asset_id"] for c in status.get("approved_cards", [])}
    missing = sorted(set(asset_ids) - approved_ids)
    if missing:
        raise GateRefused("approval gate: keyframes must be on approved OUR VERSION cards",
                          {"missing_asset_ids": missing})
    return status


def require_job_board(store, job: dict, asset_ids=()) -> dict:
    inp = job.get("input") or {}
    if inp.get("board_version") is None:
        raise GateRefused("approval gate: job has no approved board version; enqueue again")
    return require_board(store, job["workspace_id"], inp.get("board_slug"), asset_ids,
                         version=inp["board_version"])
