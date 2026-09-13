"""The dr MCP server: tool registration + HTTP app factory.

Tools return plain dicts (or a string for pipeline_guide / export_board).
AdEngineError subclasses become {"error": <class>, "message": ...} so the calling
model always gets something it can act on; unexpected exceptions propagate to
the SDK, which reports them as tool errors.
"""
from __future__ import annotations

from adengine.core.auth import require_write
from adengine.core import capabilities

import functools
import os
from typing import Any

from mcp.server.mcpserver import MCPServer

from adengine.core.auth import current
from adengine.core.errors import AdEngineError
from adengine.core.settings import settings

from . import artifacts as artifacts_mod
from . import boards, context, deps, tracker
from . import lawgate as _lawgate
from .guide import PIPELINE_GUIDE

mcp = MCPServer(
    name="adengine-dr",
    version="0.2.0",
    instructions=(
        "The Direct Response OS: turns a reference ad or raw research into "
        "law-compliant angles, scripts, briefs, and a visual storyboard board for "
        "the editor. FIRST CALL in any session: pipeline_guide, then load_brand. "
        "For footage analysis and edit planning, load the video-edit-analysis agent "
        "capability. The analysis agent produces a validated edit plan for the editing "
        "agent; scene descriptions alone do not complete that task. "
        "The playbooks served by get_playbook are the SOPs you must follow for every "
        "judgment step; lawgate/save_artifact enforce the mechanical house laws. "
        "Never write copy before loading the brand and the laws. The board is the "
        "human approval gate: approve_card is for approvers with editor rights only."
    ),
)


def _safe(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except AdEngineError as exc:
            out = {"error": type(exc).__name__, "message": str(exc)}
            details = getattr(exc, "details", None)
            if details:
                out["details"] = details
            return out
    return wrapper


@mcp.tool()
def pipeline_guide() -> str:
    """The canonical DR OS order of operations. Call this FIRST in any session,
    before any other tool. It defines which tool follows which and which laws
    you (the calling model) are responsible for enforcing."""
    return PIPELINE_GUIDE


@mcp.tool()
@_safe
def list_agent_capabilities(agent_role: str | None = None) -> list[dict]:
    """Discover agent capabilities with explicit outputs and handoff requirements."""
    return capabilities.list_capabilities(agent_role)


@mcp.tool()
@_safe
def get_agent_capability(capability_id: str) -> dict:
    """Load a capability's agent instructions, tools, completion and handoff contract."""
    return capabilities.get_capability(capability_id)


@mcp.tool()
@_safe
def load_brand(brand_slug: str) -> dict:
    """Loads the full brand context bundle: brief, house laws, global judgment
    laws, the angle bank, the artifact inventory, and the product list.
    MANDATORY before writing any copy, angle, script, or adaptation
    instruction for the brand. Follow with load_product for the product shown."""
    return context.load_brand(brand_slug)


@mcp.tool()
@_safe
def load_product(brand_slug: str, product_slug: str) -> dict:
    """The product record with its rendered product-truth blocks. Those blocks
    are verbatim-mandatory in every prompt, script, or brief that shows the
    product."""
    return context.load_product(brand_slug, product_slug)


@mcp.tool()
@_safe
def list_playbooks() -> dict:
    """Lists the pipeline stages and every playbook (SOP) get_playbook can serve."""
    return context.list_playbooks()


@mcp.tool()
@_safe
def get_playbook(name: str, section: str | None = None) -> dict:
    """Fetches a playbook (SOP) to execute, whole or one section. Pipeline
    steps include router, laws, angle-schema, artifact-contract, voc-mining,
    market-intel, angle-bank, awareness-audit, hook-lab, ugc-brief,
    funnel-strategy, survey-designer, strategize, brief-board, app-board, editor-brief,
    long-form-copy, ad-watcher."""
    return context.get_playbook(name, section=section)


@mcp.tool()
@_safe
def lawgate(text: str, brand_slug: str | None = None, speaker: str | None = None) -> dict:
    """Deterministic law check on any copy/script/plan text: global rules plus
    the brand's house laws. Returns blockers (hard laws) and warnings
    (verify-this flags). speaker='creator' additionally enforces the
    creator-never-speaks-as-brand law. Run on EVERY script and brief before
    presenting or saving. Judgment laws still live in get_playbook('laws')."""
    return _lawgate.check(text, brand_slug=brand_slug, speaker=speaker)


@mcp.tool()
@_safe
def list_artifacts(brand_slug: str) -> dict:
    """Inventory of the brand's artifacts (voc-index, angle-bank, hooks, briefs,
    adaptation-plans, ...) with versions."""
    return artifacts_mod.list_artifacts(brand_slug)


@mcp.tool()
@_safe
def read_artifact(brand_slug: str, kind: str, name: str | None = None) -> dict:
    """Reads one artifact. Singletons: voc-index, angle-bank, awareness-map,
    market-gaps, funnel-strategy. Collections (pass name, or omit to list):
    survey, winner, hooks, brief, adaptation-plan. ALWAYS read angle-bank
    before proposing new angles: merge, never duplicate."""
    return artifacts_mod.read_artifact(brand_slug, kind, name=name)


@mcp.tool()
@_safe
def save_artifact(brand_slug: str, kind: str, body: str, name: str | None = None,
                  force: bool = False, speaker: str | None = None,
                  sources: list[str] | None = None) -> dict:
    """Saves an artifact record with frontmatter {brand, artifact, generated_by,
    updated, sources}, running the law gate first: blockers stop the save
    (force=True only for provable false positives). Saving the same
    (kind, name) again overwrites in place and bumps the version. Collection
    kinds need a name, e.g. '2026-08-17-ACM-12-ugc'."""
    return artifacts_mod.save_artifact(brand_slug, kind, body, name=name, force=force,
                                       speaker=speaker, sources=sources)


@mcp.tool()
@_safe
def push_board(brand_slug: str, spec: dict, slug: str | None = None) -> dict:
    """Builds/updates a visual storyboard board from a semantic spec and returns
    its URL for the editor. spec: {title, summary, timelines: [{label, source,
    role: 'reference'|'ours', beats: [{t, script, frame, visual, emotion,
    note}]}], notes, moodboard}. frame values are ASSET IDS (or {asset_id,
    width, height}); never paths. Same slug (default: slugified title)
    overwrites in place and bumps the version, so iterate freely."""
    return boards.push_board(brand_slug, spec, slug=slug)


@mcp.tool()
@_safe
def get_board(brand_slug: str, slug: str) -> dict:
    """The board with lanes, cards, and each card's latest approval state."""
    return boards.get_board(brand_slug, slug)


@mcp.tool()
@_safe
def list_boards(brand_slug: str | None = None) -> list[dict]:
    """Lists boards in the workspace (optionally one brand), newest first."""
    return boards.list_boards(brand_slug)


@mcp.tool()
@_safe
def approve_card(slug: str, card_id: str, state: str, note: str | None = None) -> dict:
    """THE HUMAN GATE. Records approved|rejected for one card on the board. Only
    an approver with editor rights (owner/editor) may call this; an agent role
    is refused. Never call it on behalf of a human."""
    return boards.approve_card(slug, card_id, state, note=note)


@mcp.tool()
@_safe
def board_approval_status(slug: str) -> dict:
    """{approved, total, approved_count, rejected[], pending[], missing[]}. Every
    OUR VERSION beat needs media; its cards need approval for their current content. animate_scenes
    verifies this state server-side before rendering."""
    return boards.approval_status(deps.store(), deps.ws(), slug)


@mcp.tool()
@_safe
def export_board(slug: str) -> str:
    """Exports the board as one self-contained read-only HTML page (pan/zoom
    viewer; images reference their asset urls) for sharing outside the app."""
    return boards.export_board(slug)


@mcp.tool()
@_safe
def push_concept(brand_slug: str, product: str, concept: str, angle: str, thesis: str,
                 format: str = "video", type: str = "net-new",
                 source: str | None = None, notes: str | None = None) -> dict:
    """Registers an agreed concept BEFORE production starts and mints its
    asset_code ({BRAND}-{PRODUCT}-{CONCEPT}-{TYPE}{NN}, NN increments per
    brand/product/concept/type). angle = '<angle id> <angle name>' from the
    angle bank; thesis = one sentence; format video|image|dynamic; type
    net-new|iteration. Write the asset_code into the angle record's
    tested_assets and name the ad exactly that."""
    return tracker.push_concept(brand_slug, product, concept, angle, thesis,
                                format=format, type=type, source=source, notes=notes)


@mcp.tool()
@_safe
@require_write
def ingest_reference(url: str, brand_slug: str | None = None, concept: str | None = None) -> dict:
    """Queues a reference ingest job (download + frame-by-frame watch) for a
    public URL and returns the job id. Poll the job; its output manifest is the
    ground truth every downstream step is grounded in. Minutes, not seconds."""
    if not isinstance(url, str) or not url.lower().startswith(("http://", "https://")):
        return {"error": "url must be a public http(s) URL; local paths are not accepted"}
    brand_id = deps.brand_by_slug(brand_slug)["id"] if brand_slug else None
    job = deps.store().create("job", deps.ws(), "job", kind="ingest_reference", provider=None,
                              status="queued", input={"url": url, "brand_id": brand_id, "concept": concept},
                              output=None, cost=0.0, parent_id=None)
    return {"job_id": job["id"], "kind": "ingest_reference", "status": "queued",
            "next": "Poll the job until status == 'done'; then get_playbook('strategize')."}


@mcp.tool()
@_safe
def status() -> dict:
    """Workspace health: who you are, record counts per collection, store
    backend, and which engine packages are present in this build."""
    ctx = current()
    st, workspace = deps.store(), ctx.workspace_id
    counts = {}
    for coll in deps.COLLECTIONS:
        try:
            counts[coll] = len(st.find(coll, workspace))
        except Exception as exc:  # noqa: BLE001 - a backend without that table is a fact, not a failure
            counts[coll] = f"unavailable: {exc}"
    packages = {name: deps.optional_module(name) is not None for name in deps.SIBLING_PACKAGES}
    return {"workspace": workspace, "member_id": ctx.member_id, "role": ctx.role,
            "auth_mode": settings.auth_mode, "store_backend": settings.store_backend,
            "public_base_url": settings.public_base_url, "counts": counts, "packages": packages,
            "server": {"name": mcp.name, "version": mcp.version}}


# ---------------------------------------------------------------------------
# transports
# ---------------------------------------------------------------------------

def build_http_app(bind: str | None = None):
    """Starlette app for the streamable-HTTP transport (/mcp), wrapped with the
    auth middleware. Runs stateless in oauth mode so per-request AuthContext
    reaches the tool handlers."""
    from .authmw import AuthMiddleware
    bind = bind or os.environ.get("ADENGINE_BIND") or "0.0.0.0"
    app = mcp.streamable_http_app(host=bind, stateless_http=(settings.auth_mode == "oauth"))
    return AuthMiddleware(app)


def run_http(port: int = 8770, bind: str | None = None) -> None:
    import uvicorn
    bind = bind or os.environ.get("ADENGINE_BIND") or "0.0.0.0"
    uvicorn.run(build_http_app(bind), host=bind, port=port, log_level="info")


def run_stdio() -> None:
    mcp.run(transport="stdio")
