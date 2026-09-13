"""dr-os MCP server — the Direct Response OS as a tool surface.

Wraps the whole reference-to-editor-brief pipeline so ANY MCP-capable agent
(a local Claude Code session, or an external agent like Sam) can run it:

  load brand -> ingest reference (resolve + frame-by-frame watch)
  -> strategize adaptation (judgment, via playbook) -> law-gate
  -> hooks/brief (judgment, via playbooks) -> save into the artifact contract
  -> push storyboard to Cutroom for the editor -> push concept to tracker.

The machinery (download, ffmpeg, Gemini watch, board layout, file contract,
law regexes) lives HERE. The judgment (golden nugget, angles, scripts,
adaptation calls) lives in the playbooks this server serves — the calling
model executes them. Nothing is duplicated: playbooks are read live from the
skill files, the watch head is imported from ad-engine, and boards go
through briefboard/board_builder.py.

Transports: stdio (default, registered in .mcp.json) or
`server.py --http [port]` for external agent hosts (default port 8770).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import artifacts as artifacts_mod
import boards
import context
import lawgate
import tracker
from paths import AD_ENGINE, BRANDS

from mcp.server.mcpserver import MCPServer

PIPELINE_GUIDE = """\
# DR OS pipeline — canonical order of operations

You (the calling model) are the judgment layer. This server gives you the
machinery, the SOPs ("playbooks"), and the guardrails. Never skip a step to
save a call — every downstream asset inherits upstream mistakes.

## Required for ALL ad work: editing plan first (Brooks, 2026-09-08)
Automatically create and save the concept's editing plan before generating
images/video/voice, assembling a timeline or exporting. Do not wait for a
separate planning prompt. Follow _engine/sops/Ad-Editing-Plan-First-SOP.md:
verify reference cuts on consecutive frames, map narration to B-roll and
scene flow, then specify every proposed line's visual/action, source/gap,
cut cue, duration, transition, captions, audio and editorial purpose. Include
hook, product reveal, CTA and QA. Save under the concept's edit/ folder and
surface the plan proactively. Update it on revisions and after final voice
alignment. No reference: plan from the brief without inventing an analysis.
Static/single-clip ads get a compact plan. This adds no new approval gate;
continue within existing authorization unless the user asked for planning
as a separate phase. The calling model enforces this workflow prerequisite.

## A. Reference -> editor brief (the main flow)
1. dr_load_brand(brand) — brand brief, house laws, angle bank, product-truth
   skill list. Then dr_get_playbook(<product-truth skill>) for the exact
   product in the ad. NON-NEGOTIABLE: brand context loads before any copy.
2. dr_ingest_reference(url_or_path, brand, concept) — resolves the reference
   (GetHookd/TikTok/IG/YouTube/local) and watches it frame by frame. The
   returned manifest (overall + beats[]) is an index into the actual source,
   not a complete frame audit. Verify cuts/transition spans on source frames
   and correct omissions or misaligned descriptions. Never invent beats.
3. dr_get_playbook("strategize") — follow it to reason beat-by-beat into an
   adaptation plan (beat job, visual-truth bucket, continuity groups,
   real_footage_required flags). MIRROR-FIDELITY LAW: the adaptation must
   look basically exactly like the reference — same beats, shots,
   compositions, pacing — with our product/brand swapped in. Trace it,
   don't re-direct it; deviate only where a standing law forces it. Save it:
   dr_save_artifact(brand, "adaptation-plan", plan_json, name=...).
4. Angle check: dr_read_artifact(brand, "angle-bank"). The concept must map
   to an angle record (angle = the PROBLEM, not a claim). If the bank lacks
   one, run dr_get_playbook("angle-bank") and add it first.
5. Script/hooks: dr_get_playbook("hook-lab") then dr_get_playbook("ugc-brief")
   (or "editor-brief" / "long-form-copy" per format). Run every script
   through dr_lawgate(text, brand, speaker="creator" for creator lines).
6. Save the editing plan above, then brief the editor visually: dr_get_playbook("cutroom"), build the spec
   (REFERENCE CREATIVE lane vs OUR VERSION lane, per-beat timecode/SCRIPT/
   frame/EMOTION cards, frames from the watch manifest), then
   dr_push_brief_board(spec, project=brand). Give the returned URL to the
   editor.
   Also dr_save_artifact(brand, "brief", ...) so the contract has the text.
7. Close the loop: dr_push_concept(...) -> asset_id -> write it into the
   angle record's tested_assets.

## A2. Production (ad-engine MCP) — the Cutroom approval gate is LAW
When the flow continues into generation, the order is fixed:
0. Confirm the saved editing plan is complete and current; create/update it
   automatically before production if missing. A script or prompt list alone
   does not satisfy this prerequisite.
1. ad-engine plan_preflight (cost gate) -> plan_generate_anchors ->
   plan_generate_keyframes. QA every still (re-roll fails).
2. Rebuild the Cutroom board with each beat's ACTUAL keyframe image placed
   on its card (dr_push_brief_board — same title overwrites in place).
3. STOP. Brooks approves the keyframes ON the Cutroom board. Never fire
   animation before this approval — rendering is the expensive
   irreversible step; keyframes are cheap.
4. Only after approval: plan_animate_scenes (it requires the approved
   board's slug and refuses to run without one).

## B. Research -> angles (no reference in hand)
dr_get_playbook("router") and follow its routing table / cold-start order:
voc-mining -> market-intel -> angle-bank -> awareness-audit ->
funnel-strategy -> hook-lab -> ugc-brief. Artifacts always go through
dr_save_artifact so each run compounds on the last.

## Hard laws (the gate enforces the mechanical ones; you enforce the rest)
- Golden nugget first: name the motive-level frame in one sentence BEFORE
  drafting. Topic is never the motive.
- Every angle needs a verbatim source. Never invent a study, N, %, or doctor.
- Demonstrate, never describe: every claim gets a demo beat.
- Creator speaks as a customer ("they're"), never as the brand ("our").
- Action b-roll = real footage, never a generation.
- Reference adaptations MIRROR the reference (see step A.3) — a reference
  from Brooks is a spec, not inspiration.
- Cutroom is the approval gate: generated keyframes go ON the board and
  Brooks approves them there BEFORE any animation/render fires (A2).
- Generation itself belongs to the ad-engine MCP / production skills, not
  this server. This server ends at the brief + board + tracker entry,
  then resumes at A2 step 2 to place keyframes for approval.
"""

mcp = MCPServer(
    name="dr-os",
    version="0.1.0",
    instructions=(
        "The Direct Response OS: turns a reference ad or raw research into "
        "law-compliant angles, scripts, briefs, and a visual Cutroom "
        "storyboard for the editor. FIRST CALL in any session: "
        "dr_pipeline_guide, then dr_load_brand. The playbooks served by "
        "dr_get_playbook are the SOPs you must follow for every judgment "
        "step; dr_lawgate/dr_save_artifact enforce the mechanical house "
        "laws. Never write copy before loading the brand and the laws."
    ),
)


@mcp.tool()
def dr_pipeline_guide() -> str:
    """The canonical DR OS order of operations. Call this FIRST in any
    session, before any other tool — it defines which tool follows which and
    which laws you (the calling model) are responsible for enforcing."""
    return PIPELINE_GUIDE


@mcp.tool()
def dr_load_brand(brand: str) -> dict:
    """Loads the full brand context bundle: brand brief, house laws, global
    laws, the angle bank, the dr-os artifact inventory, and the list of
    product-truth skills. MANDATORY before writing any copy, angle, script,
    or adaptation instruction for the brand."""
    return context.load_brand(brand)


@mcp.tool()
def dr_list_playbooks() -> dict:
    """Lists the pipeline-step playbooks (with their role in the flow) plus
    every raw skill name dr_get_playbook can serve."""
    return context.list_playbooks()


@mcp.tool()
def dr_get_playbook(name: str) -> dict:
    """Fetches a playbook (SOP) to execute. Accepts pipeline step names
    (router, laws, angle-schema, artifact-contract, voc-mining, market-intel,
    angle-bank, awareness-audit, hook-lab, ugc-brief, funnel-strategy,
    survey-designer, strategize, brief-board, editor-brief, long-form-copy,
    ad-watcher) or any raw skill name — including product-truth skills like
    'velantra-weekender' or 'motilli', whose identity/mechanism blocks are
    verbatim-mandatory in every prompt showing the product."""
    return context.get_playbook(name)


@mcp.tool()
def dr_ingest_reference(input_str: str, brand: str | None = None,
                        concept: str | None = None,
                        skip_gemini: bool = False) -> dict:
    """Resolves ANY reference input (GetHookd URL/ID, TikTok/IG/YouTube URL,
    or local file path) to a local video, then watches it frame by frame:
    ffmpeg scene-change beats, transcript, and a Gemini pass describing every
    beat (shot_type, composition, action, on_screen_text, audio_cues,
    ad_role). Returns the watch job whose output.manifest is the ground truth
    every downstream step must be grounded in. Slow (minutes) — that is
    normal. skip_gemini=True only for a quick beat/transcript pass."""
    if str(AD_ENGINE) not in sys.path:
        sys.path.insert(0, str(AD_ENGINE))
    from workflows import resolve_reference, watch_reference
    resolved = resolve_reference.resolve(input_str, brand=brand, concept=concept)
    asset_id = (resolved.get("output") or {}).get("asset_id") or resolved.get("asset_id")
    if not asset_id:
        return {"error": "reference did not resolve", "resolve_job": resolved}
    watched = watch_reference.watch(asset_id, brand=brand, concept=concept,
                                    skip_gemini=skip_gemini)
    return {"resolve_job": resolved, "watch_job": watched,
            "next": "dr_get_playbook('strategize') and reason the manifest into an adaptation plan."}


@mcp.tool()
def dr_lawgate(text: str, brand: str | None = None,
               speaker: str | None = None) -> dict:
    """Deterministic house-law check on any copy/script/plan text. Returns
    blockers (hard laws: AI-tell patterns, banned terms, brand-truth slips)
    and warnings (verify-this flags). speaker='creator' additionally enforces
    the creator-never-speaks-as-brand law. Run this on EVERY script and brief
    before presenting or saving it. Heuristic only — the judgment laws still
    live in dr_get_playbook('laws')."""
    return lawgate.check(text, brand=brand, speaker=speaker)


@mcp.tool()
def dr_list_artifacts(brand: str) -> dict:
    """Inventory of the brand's dr-os artifact tree (voc-index, angle-bank,
    hooks, briefs, adaptation-plans, ...)."""
    return artifacts_mod.list_artifacts(brand)


@mcp.tool()
def dr_read_artifact(brand: str, artifact: str, name: str | None = None) -> dict:
    """Reads one artifact. Singletons: voc-index, angle-bank, awareness-map,
    market-gaps, funnel-strategy. Collections (pass name, or omit to list):
    survey, winner, hooks, brief, adaptation-plan. ALWAYS read angle-bank
    before proposing new angles — merge, never duplicate."""
    return artifacts_mod.read_artifact(brand, artifact, name=name)


@mcp.tool()
def dr_save_artifact(brand: str, artifact: str, content: str,
                     name: str | None = None,
                     sources: list[str] | None = None,
                     speaker: str | None = None,
                     force: bool = False) -> dict:
    """Writes an artifact into the contract tree with frontmatter, running
    the law-gate first — blockers stop the save (force=True only for provable
    false positives). sources = the files/URLs this artifact was built from;
    it is load-bearing for later merge runs. Collection artifacts (survey,
    winner, hooks, brief, adaptation-plan) need name, e.g.
    '2026-08-17-VEL-12-ugc'."""
    return artifacts_mod.save_artifact(brand, artifact, content, name=name,
                                       sources=sources, speaker=speaker, force=force)


@mcp.tool()
def dr_push_brief_board(spec: dict, slug: str | None = None,
                        project: str | None = None) -> dict:
    """Builds/updates a visual storyboard board on Cutroom (the internal
    Milanote-style whiteboard, formerly BriefBoard) and returns its URL for
    the editor. spec is the semantic spec from the brief-board/cutroom
    playbook: {title, summary, timelines: [{label, source, beats: [{t,
    script, frame, visual, emotion, note}]}], notes: [{title, text}],
    moodboard}. Every beat field is a plain string and every notes entry
    is a dict with title and text (a bare string is tolerated). project
    (usually the brand name) groups the board in Cutroom's project list.
    frame values are ABSOLUTE local image paths (watch-manifest frames /
    generated keyframes) — they get copied onto the board; never put file
    paths in card text. Same title = same slug = overwrite, so iterate
    freely."""
    return boards.push_board(spec, slug=slug, project=project)


@mcp.tool()
def dr_list_boards() -> list[dict]:
    """Lists existing Cutroom boards, newest first, with URLs and projects."""
    return boards.list_boards()


@mcp.tool()
def dr_export_board(slug: str) -> dict:
    """Exports a board to one self-contained read-only HTML file (images
    inlined) for sharing outside localhost (Slack/email)."""
    return boards.export_board(slug)


@mcp.tool()
def dr_push_concept(product: str, concept: str, angle: str, thesis: str,
                    format: str = "video", type: str = "net-new",
                    source: str = "dr-os-mcp", notes: str | None = None) -> dict:
    """Registers an agreed concept in the creative tracker BEFORE production
    starts (the creative-velocity law). angle = '<angle id> <angle name>'
    from the angle bank; thesis = one sentence. Returns the asset_id — write
    it into the angle record's tested_assets so the 30-day verdict can land."""
    return tracker.push_concept(product, concept, angle, thesis,
                                format=format, type=type, source=source, notes=notes)


@mcp.tool()
def dr_status() -> dict:
    """Environment health: brands on disk, BriefBoard server state, ad-engine
    importability, and kie balance (generation budget lives with ad-engine,
    but a zero balance upstream is worth knowing before planning)."""
    status: dict = {
        "brands": sorted(p.name for p in BRANDS.iterdir()
                         if p.is_dir() and not p.name.startswith("_")),
        "cutroom_up": boards._server_up(),
        "cutroom_url": f"http://localhost:{boards.PORT}/",
    }
    try:
        if str(AD_ENGINE) not in sys.path:
            sys.path.insert(0, str(AD_ENGINE))
        from engines import kie
        status["kie_balance"] = kie.balance()
        status["ad_engine"] = "ok"
    except Exception as exc:  # noqa: BLE001 — health probe, report and move on
        status["ad_engine"] = f"unavailable: {exc}"
    return status


if __name__ == "__main__":
    if "--http" in sys.argv:
        idx = sys.argv.index("--http")
        port = 8770
        if len(sys.argv) > idx + 1 and sys.argv[idx + 1].isdigit():
            port = int(sys.argv[idx + 1])
        mcp.run(transport="streamable-http", host="127.0.0.1", port=port)
    else:
        mcp.run(transport="stdio")
