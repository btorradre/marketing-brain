"""adengine.gen MCP server — the ad-engine tools, workspace-scoped, queue-backed.

Every tool returns ids and urls only. Nothing here polls a provider: generation
tools ENQUEUE jobs (adengine.workers runs them) and return job ids; list_jobs /
get_job report progress.

Standing laws encoded here (not in prompts):
  - Watch first. resolve_reference -> watch_reference produces the manifest every
    downstream decision is grounded in. Never generate against an unwatched reference.
  - Stills before video credit; keyframes are auditable before animation spend.
  - Board approval gate: animate_scenes refuses unless the named board is approved
    (adengine.dr.boards.approval_status) AND every keyframe asset sits on that board.
  - No chaining: each scene is animated from its own approved still.
  - One-take VO on eleven_v3 Creative.
  - Video analysis / QA runs on Gemini 3.8 Flash (analyze_video, watch_reference).
"""
from __future__ import annotations

from adengine.core.auth import require_write
from adengine.core import capabilities
from adengine.gen.approval import require_board

import io
import json
import math
from dataclasses import replace
from typing import Any

import requests
from mcp.server.mcpserver import MCPServer

from adengine.core.auth import AuthContext, current_workspace, set_auth_context
from adengine.core.errors import GateRefused, NotFound, ProviderError
from adengine.core.settings import settings
from adengine.core.store import get_store
from adengine.engines import elevenlabs, heygen, kie, ytdlp, watch
from adengine.engines.credentials import get_key, try_get_key
from adengine.gen import plan as P
from adengine.gen import registry as R
from adengine.gen import edit_plan as E
from adengine.gen import edit_review as ER
from adengine.quality import load_rubric
from adengine.workers import queue

INSTRUCTIONS = (
    "Hosted video-ad generation engine. Visual analysis and QA must use "
    "Gemini 3.8 Flash (gemini-3.8-flash). ALWAYS start any reference-based workflow with "
    "resolve_reference (enqueues ingest + watch) and read get_watch_manifest before "
    "strategizing or generating — never generate against a reference that has not been "
    "analyzed. Full-video analysis is not proof of every-frame inspection. Use "
    "review_video_frames for rapid cuts, transitions and animation timing. The analysis "
    "agent owns the video-edit-analysis capability: analyze rushes, transitions, cuts, "
    "pacing and animations, build a validated edit plan, and hand it to the editing "
    "agent. Read get_agent_capability('video-edit-analysis'); scene descriptions alone "
    "do not complete this capability. For editing, "
    "read get_edit_plan_contract, analyze reference and rushes, then save_edit_plan; "
    "the editing agent reads get_edit_plan and uses the internal timeline editor. "
    "After rendering, start_edit_style_review compares actual reference and render plus "
    "the acceptance plan. Gemini 3.8 observes; independent Astra grades heavily. Read "
    "get_edit_style_review and repair/rerender/resubmit until the style gate passes at "
    "8/10 with no blockers. A plan-ready status is not a passed rendered edit. "
    "Run preflight before spending: automatic credit top-up "
    "cannot be relied on, so an insufficient balance is a hard stop, not a warning. "
    "Generation tools enqueue jobs and return job ids; poll with get_job, never inside a tool. "
    "Two standing laws: (1) reference adaptations MIRROR the reference — same beats, shots, "
    "compositions, pacing, our product swapped in; (2) the storyboard board is the approval "
    "gate — keyframes go on the board, a member approves them there, and only then does "
    "animate_scenes fire (it requires the approved board's slug and refuses otherwise)."
)

mcp = MCPServer(name="adengine-gen", version="0.1.0", instructions=INSTRUCTIONS)


# ---------------------------------------------------------------------------
# workspace plumbing (indirected so tests can swap the store)
# ---------------------------------------------------------------------------

def _store():
    return get_store()


def _ws() -> str:
    return current_workspace()


async def workspace_middleware(ctx, call_next):
    """HTTP mode: derive the workspace from the request. In dev auth mode an
    X-Adengine-Workspace header selects it (falling back to ADENGINE_DEV_WORKSPACE).
    PHASE 1 HOOK: in oauth mode read the verified token's workspace/member/role
    from the request scope instead; never trust a header."""
    req = getattr(ctx, "request", None)
    headers = getattr(req, "headers", None)
    token = None
    if headers is not None and settings.auth_mode == "dev":
        ws = headers.get("x-adengine-workspace")
        if ws:
            token = set_auth_context(AuthContext(workspace_id=ws, member_id="dev", role="owner"))
    try:
        return await call_next(ctx)
    finally:
        if token is not None:
            from adengine.core import auth as _auth
            _auth._ctx.reset(token)


def _job_view(job: dict) -> dict[str, Any]:
    return {k: job.get(k) for k in ("id", "kind", "provider", "status", "input", "output",
                                    "cost", "error", "parent_id", "external_task_id",
                                    "created", "updated")}


def _enqueue(kind: str, input: dict, parent_id: str | None = None, provider: str | None = None) -> dict[str, Any]:
    return queue.enqueue(_store(), _ws(), kind, input, parent_id=parent_id, provider=provider)


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

@mcp.tool()
def list_agent_capabilities(agent_role: str | None = None) -> list[dict]:
    """Discover first-class agent capabilities, including their required outputs.
    Filter by analysis_agent or editing_agent to see owned/received capabilities."""
    return capabilities.list_capabilities(agent_role)


@mcp.tool()
def get_agent_capability(capability_id: str) -> dict:
    """Load the capability's agent instructions, workflow, handoff and completion
    contract. video-edit-analysis requires a validated edit-plan handoff."""
    return capabilities.get_capability(capability_id)

@mcp.tool()
def list_jobs(status: str | None = None, kind: str | None = None,
              provider: str | None = None, limit: int = 50) -> list[dict]:
    """Jobs in this workspace, most recent first. status: queued/running/completed/failed.
    kind: ingest_reference, watch_reference, analyze_video, kie_generate, eleven_vo,
    eleven_clone, heygen_avatar."""
    return [_job_view(j) for j in R.list_jobs(_store(), _ws(), status=status, kind=kind,
                                               provider=provider, limit=limit)]


@mcp.tool()
def get_job(job_id: str) -> dict[str, Any]:
    """One job with its output (asset ids/urls, credits) or error. Poll this after enqueueing."""
    return _job_view(R.get_job(_store(), _ws(), job_id))


@mcp.tool()
def list_assets(job_id: str | None = None, kind: str | None = None, limit: int = 50) -> list[dict]:
    """Assets (id, kind, url, meta). kind: video/image/audio/frame/manifest/alignment."""
    return [R.public_asset(a) for a in R.list_assets(_store(), _ws(), job_id=job_id, kind=kind, limit=limit)]


@mcp.tool()
def get_asset(asset_id: str) -> dict[str, Any]:
    """One asset: id, kind, mime, url, meta."""
    return R.public_asset(R.get_asset(_store(), _ws(), asset_id))


@mcp.tool()
def cost_summary(job_id: str | None = None) -> dict[str, Any]:
    """Spend rolled up by provider (units + USD where a rate is known), optionally for one job."""
    return R.cost_summary(_store(), _ws(), job_id=job_id)


@mcp.tool()
def provider_balance(provider: str) -> dict[str, Any]:
    """Live balance for kie (credits; read before every generate — an insufficient
    balance is a hard stop), heygen (only the 'api' pool renders) or elevenlabs
    (character quota)."""
    provider = provider.lower()
    key = get_key(provider, _ws(), _store())
    if provider == "kie":
        bal = kie.balance(key)
        return {"provider": "kie", "credits": bal, "usd_equivalent": kie.credits_to_usd(bal),
                "note": "Automatic top-up cannot be relied on: an insufficient balance blocks generation."}
    if provider == "heygen":
        return {"provider": "heygen", **heygen.check_quota(key)}
    if provider == "elevenlabs":
        return {"provider": "elevenlabs", **elevenlabs.subscription(key)}
    raise ProviderError(f"provider_balance not supported for '{provider}'")


# ---------------------------------------------------------------------------
# Reference resolution + watch (mandatory pipeline head)
# ---------------------------------------------------------------------------

@mcp.tool()
@require_write
def resolve_reference(url: str, gemini: bool = True, media_role: str = "reference") -> dict[str, Any]:
    """Universal front door for ANY reference: a GetHookd share URL / ad id or a
    TikTok/IG/YouTube/direct video URL. Creates a reference record and enqueues
    ingest_reference then watch_reference (the watch waits for the ingest).
    Returns reference_id + both job ids; read get_watch_manifest when the watch
    job is completed."""
    if media_role not in ("reference", "rushes"):
        raise GateRefused("media_role must be reference or rushes")
    store, ws = _store(), _ws()
    ref = R.create_reference(store, ws, url, status="pending")
    ingest = queue.enqueue(store, ws, "ingest_reference", {"url": url, "reference_id": ref["id"]},
                           provider="gethookd" if "gethookd" in url else "ytdlp")
    watch_job = queue.enqueue(store, ws, "watch_reference",
                              {"reference_id": ref["id"], "gemini": gemini, "media_role": media_role},
                              parent_id=ingest["id"], provider="gemini")
    R.update_reference(store, ws, ref["id"], ingest_job_id=ingest["id"], watch_job_id=watch_job["id"])
    return {"reference_id": ref["id"], "ingest_job_id": ingest["id"], "watch_job_id": watch_job["id"],
            "next": "Poll get_job(watch_job_id); when completed call get_watch_manifest(reference_id)."}


@mcp.tool()
@require_write
def watch_reference(asset_id_or_url: str, gemini: bool = True,
                    media_role: str = "reference") -> dict[str, Any]:
    """MANDATORY before strategizing against a reference. Accepts an existing video
    asset id (already in this workspace) or a URL (ingested first). Enqueues the
    watch: ffmpeg scene-change beats, one frame per beat, transcript (captions or
    Whisper), and the Gemini 3.8 Flash per-beat pass (shot_type, composition,
    subject, action, motion, on_screen_text, audio_cues, ad_role). Returns
    reference_id + job id; the manifest lands on the reference. Set media_role
    to rushes for raw source footage and take/select logging."""
    if media_role not in ("reference", "rushes"):
        raise GateRefused("media_role must be reference or rushes")
    store, ws = _store(), _ws()
    if asset_id_or_url.startswith("asset_"):
        asset = R.get_asset(store, ws, asset_id_or_url)
        ref = R.create_reference(store, ws, asset.get("url") or asset["id"], asset_id=asset["id"],
                                 status="ingested")
        job = queue.enqueue(store, ws, "watch_reference", {"reference_id": ref["id"], "gemini": gemini,
                                                           "media_role": media_role},
                            provider="gemini")
        R.update_reference(store, ws, ref["id"], watch_job_id=job["id"])
        return {"reference_id": ref["id"], "watch_job_id": job["id"]}
    if ytdlp.is_url(asset_id_or_url) or asset_id_or_url.strip().isdigit():
        return resolve_reference(asset_id_or_url, gemini=gemini, media_role=media_role)
    raise NotFound("watch_reference needs an asset id (asset_...) or a URL; local paths are not accepted")


@mcp.tool()
def get_watch_manifest(reference_id: str) -> dict[str, Any]:
    """The source analysis manifest for a watched reference: overall
    (format, emotion arc, core promise), transcript_source, and one entry per
    beat with t/t_end, frame_asset_id + frame_url, clip_url, vo snippet and the
    gemini fields, editorial analysis of rushes/cuts/transitions/pacing/animations,
    and explicit completeness/coverage. Full-video model input does not prove
    every frame was inspected. Ground every downstream decision in this."""
    ref = R.get_reference(_store(), _ws(), reference_id)
    if not ref.get("manifest"):
        return {"reference_id": reference_id, "status": ref.get("status"), "manifest": None,
                "watch_job_id": ref.get("watch_job_id"),
                "note": "not watched yet; poll get_job(watch_job_id)"}
    return {"reference_id": reference_id, "status": ref.get("status"),
            "video_asset_id": ref.get("asset_id"), "manifest": ref["manifest"]}


@mcp.tool()
@require_write
def analyze_video(asset_id: str, prompt: str, model: str | None = None) -> dict[str, Any]:
    """Send ANY video/image asset to Gemini 3.8 Flash with your own prompt and get
    structured JSON back (frame QA, clip-drift checks, keyframe scoring, product
    fidelity audits). Enqueues an analyze_video job; the JSON is in the completed
    job's output.result."""
    R.get_asset(_store(), _ws(), asset_id)  # 404 early
    job = _enqueue("analyze_video", {"asset_id": asset_id, "prompt": prompt,
                                     "model": watch.gemini_model(model)}, provider="gemini")
    return {"job_id": job["id"], "model": watch.gemini_model(model)}


@mcp.tool()
@require_write
def review_video_frames(asset_id: str, start_s: float, end_s: float,
                        prompt: str = "Locate cuts, transitions and animation phases.") -> dict:
    """Inspect EVERY decoded frame in [start_s,end_s), preserving source indices
    and timestamps (including VFR). Maximum 120 frames per job; split longer
    windows. No subsampling or silent trimming. Images are silent; use watch
    for audio. Job output includes frame asset ids/URLs and coverage status."""
    asset = R.get_asset(_store(), _ws(), asset_id)
    if not (asset.get("mime") or "").startswith("video/"):
        raise GateRefused("Frame review requires a video asset")
    if not all(math.isfinite(v) for v in (start_s, end_s)) or not 0 <= start_s < end_s:
        raise GateRefused("Frame window needs finite 0 <= start_s < end_s")
    return {"job_id": _enqueue("review_video_frames", {
        "asset_id": asset_id, "start_s": start_s, "end_s": end_s, "prompt": prompt,
    }, provider="gemini")["id"]}


@mcp.tool()
def get_edit_plan_contract() -> dict:
    """Analysis-agent output / editing-agent input schema and execution protocol."""
    return {"schema": E.EditPlan.model_json_schema(), "editor": "@adengine/timeline",
            "visual_analysis_model": watch.gemini_model(),
            "capability_id": capabilities.EDIT_ANALYSIS,
            "playbook": "video-analysis-edit-handoff",
            "entrypoint": "assembleFromEditPlan(envelope, options)",
            "steps": [
                "Watch reference and every selected rush asset; read each manifest and its analysis.issues.",
                "Review ambiguous/rapid events with review_video_frames; split windows over 120 frames.",
                "Build an edit plan with timed source selects, rationale/evidence, pacing, transitions, animation keyframes and audio.",
                "save_edit_plan validates and stores a handoff; get_edit_plan rechecks current evidence before editing.",
                "Editing agent compiles to the internal timeline ops; unsupported effects require an explicit decision.",
                "Render/playback QA checks the executed video against acceptance_checks; a valid plan is not a finished edit.",
            ], "time_convention": "seconds, end exclusive; animation keys relative to owning clip; editor uses 6000 ticks/s"}


def _edit_sources(reference_ids: list[str]) -> dict:
    if not reference_ids or len(reference_ids) != len(set(reference_ids)):
        raise GateRefused("Provide unique reference ids for reference and selected rushes")
    manifests = {}
    for rid in reference_ids:
        ref = R.get_reference(_store(), _ws(), rid)
        if not ref.get("manifest"):
            raise GateRefused(f"Reference {rid} is not analyzed")
        manifests[rid] = ref["manifest"]
    return manifests


def _frame_reviews(job_ids: list[str], manifests: dict) -> list[dict]:
    source_ids = {m["video_asset_id"] for m in manifests.values()}
    results = []
    for jid in job_ids:
        job = R.get_job(_store(), _ws(), jid)
        output = job.get("output") or {}
        if (job["kind"] != "review_video_frames" or job["status"] != R.COMPLETED or
            output.get("status") != "complete" or output.get("asset_id") not in source_ids):
            raise GateRefused(f"Frame review {jid} is incomplete or belongs to a different source")
        results.append({"job_id": jid, **output})
    return results


@mcp.tool()
@require_write
def save_edit_plan(plan: dict, reference_ids: list[str],
                   frame_review_job_ids: list[str] | None = None) -> dict:
    """Persist a validated analysis-to-editor handoff as an immutable JSON asset.
    Refuses incomplete analysis, unresolved decisions, missing evidence, invalid
    trims, timeline gaps/overlaps and out-of-range animation. Does not edit/render."""
    store, ws = _store(), _ws()
    manifests = _edit_sources(reference_ids)
    parsed = E.validate_handoff(plan, manifests)
    reviews = _frame_reviews(frame_review_job_ids or [], manifests)
    assets = []
    for aid in sorted({clip.asset_id for clip in parsed.clips}):
        asset = R.get_asset(store, ws, aid)
        duration = max(b["t_end"] for m in manifests.values() if m["video_asset_id"] == aid for b in m["beats"])
        assets.append({**R.public_asset(asset), "duration_s": duration})
    envelope = {"status": "ready_for_editor", "editor": "@adengine/timeline",
                "capability_id": capabilities.EDIT_ANALYSIS, "handoff_agent": "editing_agent",
                "plan": parsed.model_dump(), "assets": assets,
                "analysis_fingerprints": {rid: E.fingerprint(m) for rid, m in manifests.items()},
                "analysis": manifests, "frame_reviews": reviews}
    from adengine.core.ids import new_id
    saved = R.put_bytes_asset(store, ws, json.dumps(envelope, allow_nan=False).encode(),
        f"edit-plans/{new_id('plan')}.json", kind="edit_plan", mime="application/json")
    return {"asset_id": saved["id"], "url": saved["url"], "status": "ready_for_editor",
            "capability_id": capabilities.EDIT_ANALYSIS, "handoff_agent": "editing_agent",
            "next": "Editing agent: get_edit_plan(asset_id), then assembleFromEditPlan in @adengine/timeline."}


@mcp.tool()
def get_edit_plan(asset_id: str) -> dict:
    """Read the handoff, rechecking workspace ownership and stale analysis.
    Includes the plan, source assets, observations, frame reviews and acceptance checks."""
    store, ws = _store(), _ws()
    asset = R.get_asset(store, ws, asset_id)
    if asset.get("kind") != "edit_plan":
        raise GateRefused("Asset is not an edit plan")
    with store.open_blob(ws, asset["storage_key"]) as stream:
        envelope = json.load(stream)
    manifests = _edit_sources(list(envelope["analysis_fingerprints"]))
    for rid, manifest in manifests.items():
        if E.fingerprint(manifest) != envelope["analysis_fingerprints"][rid]:
            raise GateRefused(f"Edit plan is stale: reference {rid} changed; rebuild the handoff")
    for source in envelope["assets"]:
        R.get_asset(store, ws, source["id"])
    E.validate_handoff(envelope["plan"], manifests)
    _frame_reviews([r["job_id"] for r in envelope["frame_reviews"]], manifests)
    return envelope


@mcp.tool()
def get_edit_style_rubric() -> dict:
    """Strict 0-10 reference-style and edit-plan rubric. Pass requires >=8,
    criterion floors, complete evidence and no critical failures. Astra grades."""
    return load_rubric("edit_style")


@mcp.tool()
@require_write
def start_edit_style_review(edit_plan_asset_id: str, reference_asset_id: str,
                           render_asset_id: str, timeline_asset_id: str,
                           previous_review_job_id: str | None = None,
                           max_rounds: int = 8) -> dict:
    """Queue actual reference/render comparison and independent high-effort Astra
    grading. The timeline must be the executed internal-editor Project JSON asset.
    If below 8/10, edit through the internal editor, rerender, then call again
    with previous_review_job_id and changed render/timeline assets. Acceptance
    plan, reference and rubric stay pinned. Scores cannot be supplied by callers.
    Limits/unsupported editor operations remain unfinished, never passed."""
    from adengine.core.auth import current
    job = ER.enqueue_review(_store(), _ws(), plan_id=edit_plan_asset_id,
        reference_id=reference_asset_id, render_id=render_asset_id,
        timeline_id=timeline_asset_id, creator_id=current().member_id,
        previous_job_id=previous_review_job_id, max_rounds=max_rounds)
    return {"review_job_id":job["id"], "status":job["status"],
            "required_score":8, "score_max":10, "grader_model":"gpt-6-astra",
            "next":"Poll get_edit_style_review; a failed grade requires internal-editor repairs and a fresh render."}


@mcp.tool()
def get_edit_style_review(review_job_id: str) -> dict:
    """Return the current style grade, evidence and concrete repair instructions.
    Changed evidence or a newer revision invalidates the old delivery status.
    Only status=pass AND delivery_ready=true completes this rendered-edit gate."""
    return ER.get_status(_store(), _ws(), review_job_id)


@mcp.tool()
@require_write
def retry_edit_style_review(review_job_id: str) -> dict:
    """Retry a failed provider attempt in the same immutable review round.
    A completed grade cannot be rerolled. Evidence and round limits stay pinned."""
    store,ws = _store(),_ws()
    job = R.get_job(store,ws,review_job_id)
    if job['kind'] != ER.KIND or job['status'] != R.FAILED:
        raise GateRefused('Only a failed edit-style provider attempt may be retried')
    ER.assert_current(store,ws,job['input']['snapshot'])
    reports = R.list_assets(store,ws,job_id=job['id'],kind='edit_style_review')
    if reports:
        report = ER.read_json(store,ws,reports[0]['id'])
        result = {**report['result'],'review_asset_id':reports[0]['id']}
        queue.complete(store,job,result)
        return {'review_job_id':job['id'],'status':'completed','note':'Recovered committed grade without regrading'}
    updated = store.retry_failed_job(ws,job['id'])
    return {'review_job_id':job['id'],'status':updated['status']}


# ---------------------------------------------------------------------------
# Plan runner
# ---------------------------------------------------------------------------

@mcp.tool()
def preflight(plan: dict, video_model: str = P.DEFAULT_VIDEO_MODEL) -> dict[str, Any]:
    """Dry run of an adaptation plan: what would be generated, what defers to
    real-footage sourcing, estimated video seconds / credits / USD, and whether
    the kie balance covers it. Run BEFORE spending anything — an insufficient
    balance is a hard stop."""
    key = try_get_key("kie", _ws(), _store())
    balance = kie.balance(key) if key else None
    return P.preflight(plan, video_model=video_model, balance=balance)


@mcp.tool()
@require_write
def generate_anchors(plan: dict, product_slug: str, ref_asset_ids: list[str] | None = None,
                     aspect_ratio: str = "9:16", resolution: str = "2K") -> dict[str, Any]:
    """ONE still per continuity group so identity holds across its beats.
    ref_asset_ids are the canonical product reference images (asset ids); if
    omitted, the product record's truth.reference_asset_ids are used. Enqueues
    one kie_generate job per group; QA every anchor when its job completes."""
    store, ws = _store(), _ws()
    refs = list(ref_asset_ids or _product_refs(store, ws, product_slug))
    inputs, errors = P.anchor_requests(plan, refs, aspect_ratio=aspect_ratio, resolution=resolution)
    jobs = {}
    for inp in inputs:
        inp["product_slug"] = product_slug
        job = queue.enqueue(store, ws, "kie_generate", inp, provider="kie")
        jobs[inp["group"]] = {"job_id": job["id"], "member_beats": inp["member_beats"]}
    return {"anchor_jobs": jobs, "errors": errors, "ref_asset_ids": refs,
            "next": "Poll each job_id; QA every anchor image; then generate_keyframes with "
                    "anchors mapping group -> approved anchor asset id."}


@mcp.tool()
@require_write
def generate_keyframes(plan: dict, anchors: dict[str, str] | None = None,
                       ref_asset_ids: list[str] | None = None, product_slug: str | None = None,
                       aspect_ratio: str = "9:16", resolution: str = "2K") -> dict[str, Any]:
    """One still per scene, each authored independently from canonical references —
    never chained off another clip's last frame. anchors maps continuity_group ->
    approved anchor asset id (from generate_anchors). Scenes marked
    real_footage_required / source_existing are NOT generated; they come back
    under deferred_to_sourcing. After QA, put every keyframe on the concept's
    storyboard board and STOP for approval — animate_scenes will not run without
    that board's slug."""
    store, ws = _store(), _ws()
    refs = list(ref_asset_ids or (_product_refs(store, ws, product_slug) if product_slug else []))
    inputs, deferred = P.keyframe_requests(plan, refs, anchors=anchors,
                                           aspect_ratio=aspect_ratio, resolution=resolution)
    dispatched = []
    for inp in inputs:
        job = queue.enqueue(store, ws, "kie_generate", inp, provider="kie")
        dispatched.append({"beat": inp["beat"], "continuity_group": inp.get("group"), "job_id": job["id"]})
    return {"dispatched": dispatched, "deferred_to_sourcing": deferred,
            "next": "Poll each job_id and QA every still (re-roll fails). Place every keyframe on the "
                    "storyboard board and STOP — a member approves them ON the board. Only then call "
                    "animate_scenes with the approved board's slug."}


@mcp.tool()
@require_write
def animate_scenes(plan: dict, keyframe_asset_ids: dict[str, str], board_slug: str,
                   model: str = P.DEFAULT_VIDEO_MODEL, aspect_ratio: str = "9:16",
                   resolution: str = "720p", generate_audio: bool = True) -> dict[str, Any]:
    """Animates each APPROVED keyframe independently (no chaining).

    HARD GATE: board_slug must name the storyboard board that holds these exact
    keyframes and is approved there. If the board is not approved, or any
    keyframe asset is not on that board's cards, this refuses and dispatches
    NOTHING — never invent a slug to get past the gate.

    keyframe_asset_ids maps beat key -> approved still asset id. Each clip's
    duration follows its scene's t/t_end. Enqueues one kie_generate job per beat."""
    store, ws = _store(), _ws()
    status = require_board(store, ws, board_slug, keyframe_asset_ids.values())

    inputs, skipped = P.animation_requests(plan, keyframe_asset_ids, model=model,
                                           aspect_ratio=aspect_ratio, resolution=resolution,
                                           generate_audio=generate_audio)
    key = try_get_key("kie", ws, store)
    balance = kie.balance(key) if key else None
    dispatched = []
    for inp in inputs:
        inp["board_slug"] = board_slug
        inp["board_version"] = status["version"]
        job = queue.enqueue(store, ws, "kie_generate", inp, provider="kie")
        dispatched.append({"beat": inp["beat"], "duration": inp["duration"], "job_id": job["id"]})
    return {"dispatched": dispatched, "skipped": skipped, "board_slug": board_slug,
            "kie_balance_before": balance,
            "next": "Poll each job_id; hand the finished clips plus the VO to the editor."}


def _product_refs(store, ws: str, product_slug: str) -> list[str]:
    try:
        product = store.one("product", ws, slug=product_slug)
    except NotFound:
        raise NotFound(f"product '{product_slug}' not found in this workspace")
    truth = product.get("truth") or {}
    refs = truth.get("reference_asset_ids") or product.get("reference_asset_ids") or []
    if not refs:
        raise GateRefused(f"product '{product_slug}' has no reference_asset_ids in its truth record",
                          {"product_slug": product_slug})
    return list(refs)


# ---------------------------------------------------------------------------
# Direct generation (no plan)
# ---------------------------------------------------------------------------

@mcp.tool()
@require_write
def generate_image(prompt: str, ref_asset_ids: list[str] | None = None,
                   model: str = kie.IMAGE_MODEL_I2I, aspect_ratio: str = "9:16",
                   resolution: str = "2K") -> dict[str, Any]:
    """One still via kie (GPT Image 2 i2i by default; text-to-image if no refs).
    ref_asset_ids are uploaded to the provider by the worker. Returns job_id."""
    if model not in kie.IMAGE_MODELS:
        raise GateRefused("generate_image only accepts supported still-image models; use generate_video for video")
    refs = list(ref_asset_ids or [])
    if not refs and model == kie.IMAGE_MODEL_I2I:
        model = kie.IMAGE_MODEL_T2I
    inp = {"model": model, "input": {"prompt": prompt, "aspect_ratio": aspect_ratio,
                                      "resolution": resolution}, "purpose": "image"}
    if refs:
        inp["asset_refs"] = {"input_urls": refs}
    job = _enqueue("kie_generate", inp, provider="kie")
    return {"job_id": job["id"], "model": model}


@mcp.tool()
@require_write
def generate_video(prompt: str, ref_asset_ids: list[str] | None = None,
                   model: str = kie.DEFAULT_VIDEO_MODEL, duration: int = 8,
                   aspect_ratio: str = "9:16", resolution: str = "720p",
                   generate_audio: bool = True, first_frame_asset_id: str | None = None,
                   board_slug: str | None = None) -> dict[str, Any]:
    """One clip via kie (Seedance 2.5 by default). ref_asset_ids become
    reference_image_urls; first_frame_asset_id seeds the first frame (never a
    previous clip's last frame). Requires board_slug and a first_frame_asset_id on
    an approved OUR VERSION card. The worker rechecks approval and board version
    before submission. Check provider_balance('kie') first. Returns job_id."""
    if not first_frame_asset_id:
        raise GateRefused("approval gate: generate_video requires an approved first_frame_asset_id")
    status = require_board(_store(), _ws(), board_slug, [first_frame_asset_id])
    inp = {"board_slug": board_slug, "board_version": status["version"],
           "model": model, "input": {"prompt": prompt, "aspect_ratio": aspect_ratio,
                                      "resolution": resolution, "duration": max(4, min(int(duration), 30)),
                                      "generate_audio": generate_audio}, "purpose": "video",
           "asset_refs": {}}
    if ref_asset_ids:
        inp["asset_refs"]["reference_image_urls"] = list(ref_asset_ids)
    if first_frame_asset_id:
        inp["asset_refs"]["first_frame_url"] = first_frame_asset_id
    job = _enqueue("kie_generate", inp, provider="kie")
    return {"job_id": job["id"], "model": model}


# ---------------------------------------------------------------------------
# Voice (ElevenLabs) and avatar (HeyGen)
# ---------------------------------------------------------------------------

@mcp.tool()
@require_write
def generate_vo(text: str, voice_id: str, with_timestamps: bool = False,
                pronunciation_fixes: dict[str, str] | None = None) -> dict[str, Any]:
    """ONE continuous voiceover on eleven_v3 Creative (stability 0.0, similarity
    0.85) — never multilingual_v2, never per-line. voice_id is a registry voice
    name or a raw provider id. Over 5,000 chars it splits at a paragraph and
    stitches. with_timestamps also stores character alignment as an asset.
    pronunciation_fixes {plain: respelled} apply to TTS input only, on top of the
    workspace's pronunciation records. v3 has no speed control — pace with
    ffmpeg atempo afterwards. Returns job_id."""
    job = _enqueue("eleven_vo", {"text": text, "voice": voice_id, "with_timestamps": with_timestamps,
                                 "pronunciation_fixes": pronunciation_fixes or {}}, provider="elevenlabs")
    return {"job_id": job["id"]}


@mcp.tool()
@require_write
def clone_voice(name: str, asset_ids: list[str], description: str = "",
                tags: list[str] | None = None) -> dict[str, Any]:
    """Clones a voice (IVC) from audio/video assets and registers it under `name`
    for this workspace. Clone from EVERY shipped segment of a creator's audio, not
    just the first. Library voices read flat on v3 — clone the creator. Returns job_id."""
    for a in asset_ids:
        R.get_asset(_store(), _ws(), a)
    job = _enqueue("eleven_clone", {"name": name, "asset_ids": list(asset_ids),
                                    "description": description, "tags": tags or []},
                   provider="elevenlabs")
    return {"job_id": job["id"]}


@mcp.tool()
def list_voices() -> dict[str, Any]:
    """Voices registered in this workspace (name -> provider voice id) plus the
    provider's stock voices."""
    voices = [{"id": v["id"], "name": v["name"], "voice_id": v["voice_id"],
               "description": v.get("description", ""), "tags": v.get("tags", []),
               "source_asset_ids": v.get("source_asset_ids", [])}
              for v in R.list_voices(_store(), _ws())]
    return {"voices": voices, "stock_voices": elevenlabs.STOCK_VOICES}


@mcp.tool()
def heygen_quota() -> dict[str, Any]:
    """HeyGen credit pools. ONLY 'api' renders — a large generative_credit balance
    does NOT enable API renders. A quota read never triggers automatic top-up."""
    return heygen.check_quota(get_key("heygen", _ws(), _store()))


@mcp.tool()
def heygen_list_avatars(own_only: bool = True) -> dict[str, Any]:
    """Avatar looks. own_only=True: the account's own avatar groups (newest first);
    False: the full stock catalog."""
    return heygen.list_avatars(get_key("heygen", _ws(), _store()), own_only=own_only)


@mcp.tool()
def heygen_check_avatar_v(look_id: str) -> dict[str, Any]:
    """Whether a look supports the Avatar V engine (the quality path, 1080x1920).
    Verify before heygen_generate with engine='avatar_v'."""
    return heygen.check_avatar_v_eligible(look_id, get_key("heygen", _ws(), _store()))


@mcp.tool()
@require_write
def heygen_generate(audio_asset_id: str, avatar_id: str, title: str = "adengine",
                    aspect_ratio: str = "9:16", resolution: str = "1080p",
                    engine: str = "avatar_v", board_slug: str | None = None) -> dict[str, Any]:
    """Avatar video lip-synced to OUR audio asset (an ElevenLabs one-take VO):
    the worker uploads the mp3, submits a v3 render, polls, and stores the mp4.
    A credit failure surfaces at poll time, not submit time; the failed job then
    carries output.should_refire=True — re-enqueue rather than reporting a block.
    Requires an approved board_slug; the worker rechecks before submission.
    Returns job_id."""
    status = require_board(_store(), _ws(), board_slug)
    R.get_asset(_store(), _ws(), audio_asset_id)
    job = _enqueue("heygen_avatar", {"board_slug": board_slug, "board_version": status["version"],
                                     "audio_asset_id": audio_asset_id, "avatar_id": avatar_id,
                                     "title": title, "aspect_ratio": aspect_ratio,
                                     "resolution": resolution, "engine": engine}, provider="heygen")
    return {"job_id": job["id"]}


# ---------------------------------------------------------------------------
# Upload
# ---------------------------------------------------------------------------

MAX_UPLOAD_BYTES = 512 * 1024 * 1024


@mcp.tool()
@require_write
def upload_asset(url: str, kind: str | None = None) -> dict[str, Any]:
    """Fetches a public URL into this workspace's storage and registers it as an
    asset (no local paths — media moves by URL or asset id). Returns asset id + url."""
    if not ytdlp.is_url(url):
        raise ProviderError("upload_asset needs an http(s) URL")
    store, ws = _store(), _ws()
    resp = requests.get(url, stream=True, timeout=120)
    if resp.status_code != 200:
        raise ProviderError(f"fetch failed: HTTP {resp.status_code}")
    mime = (resp.headers.get("content-type") or "").split(";")[0].strip() or R.mime_for(url)
    buf = io.BytesIO()
    for chunk in resp.iter_content(chunk_size=1 << 20):
        buf.write(chunk)
        if buf.tell() > MAX_UPLOAD_BYTES:
            raise ProviderError("upload exceeds 512MB")
    data = buf.getvalue()
    if not data:
        raise ProviderError("fetched 0 bytes")
    name = url.split("?")[0].rstrip("/").split("/")[-1] or "upload"
    ext = "." + name.rsplit(".", 1)[1] if "." in name else ""
    import time as _t
    key = f"uploads/{int(_t.time() * 1000):x}{ext}"
    asset = R.put_bytes_asset(store, ws, data, key, kind or R.kind_for_mime(mime), mime,
                              meta={"source_url": url, "bytes": len(data)})
    return {"asset_id": asset["id"], "url": asset["url"], "kind": asset["kind"], "mime": mime}


TOOL_NAMES = [
    "list_jobs", "get_job", "list_assets", "get_asset", "cost_summary", "provider_balance",
    "resolve_reference", "watch_reference", "get_watch_manifest", "analyze_video",
    "preflight", "generate_anchors", "generate_keyframes", "animate_scenes",
    "generate_image", "generate_video", "generate_vo", "clone_voice", "list_voices",
    "heygen_quota", "heygen_list_avatars", "heygen_check_avatar_v", "heygen_generate",
    "upload_asset",
]


def serve(http_port: int | None = None, host: str = "0.0.0.0") -> None:
    if http_port is None:
        mcp.run(transport="stdio")
        return
    from mcp.server.transport_security import TransportSecuritySettings
    # Containers are reached through arbitrary Host headers (compose service names,
    # ingress); DNS-rebinding protection is handled at the edge in hosted mode.
    mcp.run(transport="streamable-http", host=host, port=http_port,
            transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False))


# register the workspace middleware on the low-level server
try:
    mcp._lowlevel_server.middleware = [workspace_middleware, *list(mcp._lowlevel_server.middleware or [])]
except AttributeError:  # pragma: no cover — SDK shape changed; fall back to dev workspace only
    pass
