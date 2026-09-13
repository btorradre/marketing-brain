"""ad-engine MCP server — Phase 1.

Local-only, stdio transport. Exposes the kie.ai engine wrapper, the
resolve/watch front door, and the job/asset/cost registry as tools so any
Claude Code session (or subagent) can drive ad generation without shelling
out to a different one-off Python script per skill.

Phase 1 scope: kie.ai primitives + registry + reference resolution + the
watch-head (frame-by-frame breakdown). HeyGen/ElevenLabs engines and the
composite generate/animate/assemble workflow tools land in later phases.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import db
from engines import elevenlabs, heygen, kie
from workflows import plan_runner, resolve_reference, watch_reference

from mcp.server.mcpserver import MCPServer

mcp = MCPServer(name="ad-engine", version="0.1.0",
                 instructions=(
                     "Internal video-ad generation engine. ALWAYS start any "
                     "reference-based workflow with resolve_reference then "
                     "watch_reference — never generate against a reference "
                     "that hasn't been watched frame-by-frame first. Check "
                     "kie_balance before firing kie_generate; auto top-up is "
                     "broken on this account so a low balance is a hard stop, "
                     "not a warning. Two standing laws: (1) reference "
                     "adaptations MIRROR the reference — same beats, shots, "
                     "compositions, pacing, our product swapped in; (2) the "
                     "Cutroom board is the approval gate — generated keyframes "
                     "go ON the board (dr-os dr_push_brief_board), Brooks "
                     "approves them there, and only then does "
                     "plan_animate_scenes fire (it requires the approved "
                     "board's slug)."
                 ))

db.init_db()


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

@mcp.tool()
def list_jobs(status: str | None = None, brand: str | None = None,
              engine: str | None = None, limit: int = 50) -> list[dict]:
    """List jobs from the registry, most recent first. Filter by status
    (pending/running/success/fail), brand, or engine (kie/gemini/resolver)."""
    return db.list_jobs(status=status, brand=brand, engine=engine, limit=limit)


@mcp.tool()
def get_job(job_id: str) -> dict | None:
    """Fetch a single job's full record, including its output payload."""
    return db.get_job(job_id)


@mcp.tool()
def list_assets(job_id: str | None = None, brand: str | None = None,
                 kind: str | None = None, concept: str | None = None,
                 limit: int = 50) -> list[dict]:
    """List generated/downloaded assets. kind is one of
    video/image/audio/transcript/manifest/plan."""
    return db.list_assets(job_id=job_id, brand=brand, kind=kind, concept=concept, limit=limit)


@mcp.tool()
def get_asset(asset_id: str) -> dict | None:
    """Fetch a single asset's record (local path, source URL, brand/concept, meta)."""
    return db.get_asset(asset_id)


@mcp.tool()
def cost_summary(brand: str | None = None, concept: str | None = None) -> dict:
    """Roll up spend by engine, optionally filtered to a brand or concept."""
    return db.cost_summary(brand=brand, concept=concept)


# ---------------------------------------------------------------------------
# Reference resolution + watch (mandatory pipeline head)
# ---------------------------------------------------------------------------

@mcp.tool()
def resolve_reference_tool(input_str: str, brand: str | None = None,
                            concept: str | None = None) -> dict:
    """Resolves ANY reference input — a GetHookd URL/ad ID, a generic video
    URL (TikTok/IG/YouTube via yt-dlp), or a local file path — to a local
    video file registered as an asset. This is the universal front door:
    call this FIRST for any reference-based workflow, before watch_reference."""
    return resolve_reference.resolve(input_str, brand=brand, concept=concept)


@mcp.tool()
def watch_reference_tool(video_ref: str, brand: str | None = None,
                          concept: str | None = None,
                          skip_gemini: bool = False) -> dict:
    """MANDATORY second step after resolve_reference. video_ref is a local
    path OR the asset_id returned by resolve_reference. Runs ffmpeg
    scene-change detection to find every real cut, pulls the transcript, and
    a Gemini pass over the full video that describes every beat (shot_type,
    composition, subject, action, motion, on_screen_text, audio_cues,
    ad_role). The returned job's output.manifest is the frame-by-frame
    breakdown that any downstream strategizing/generation must be grounded
    in — never generate against a reference you haven't watched this way."""
    return watch_reference.watch(video_ref, brand=brand, concept=concept, skip_gemini=skip_gemini)


# ---------------------------------------------------------------------------
# kie.ai (Seedance, Kling, GPT Image 2, Nano Banana — the primary gen engine)
# ---------------------------------------------------------------------------

@mcp.tool()
def kie_balance() -> float | None:
    """Current kie.ai credit balance. Auto top-up is BROKEN on this account —
    call this before every kie_generate and treat a low balance as a hard
    stop, not a warning."""
    return kie.balance()


@mcp.tool()
def kie_upload(local_path: str, upload_path: str = "ad-engine") -> str:
    """Uploads a local image/video to kie's temp storage (~24h-3d TTL) and
    returns a downloadUrl usable as a reference_image_urls / reference_video_urls
    / image_urls entry in kie_generate's input_data."""
    return kie.upload(local_path, upload_path=upload_path)


@mcp.tool()
def kie_generate(model: str, input_data: dict, brand: str | None = None,
                  concept: str | None = None) -> dict:
    """Fires a kie.ai createTask and returns immediately (does NOT block/poll)
    with {job_id, external_task_id, status:'running'}. Poll with kie_status.

    Common models: bytedance/seedance-2-5 (video, up to 30s, flat 63cr/s,
    native audio), kling-3.0/video (video, 14cr/s, needs multi_shots bool),
    gpt-image-2-image-to-image / gpt-image-2-text-to-image (stills).
    input_data is passed through verbatim as the model's `input` object —
    see each model's own prompting docs for its shape."""
    return kie.generate(model, input_data, brand=brand, concept=concept)


@mcp.tool()
def kie_status(job_id: str) -> dict:
    """One poll of a kie_generate job. On success, downloads the result(s)
    locally, registers them as assets, and logs the actual credits consumed
    to the cost ledger. Call repeatedly (with your own backoff) until
    status is success or fail — this does not block internally."""
    return kie.status(job_id)


# ---------------------------------------------------------------------------
# ElevenLabs (voiceover — v3 Creative, one continuous take)
# ---------------------------------------------------------------------------

@mcp.tool()
def eleven_list_voices() -> dict:
    """Registered cloned voices + defaults, from the shared voice registry
    (the same one the elevenlabs-agent skill writes to)."""
    return elevenlabs.list_voices()


@mcp.tool()
def eleven_generate_vo(script: str, voice: str, brand: str | None = None,
                        concept: str | None = None,
                        with_timestamps: bool = False) -> dict:
    """Generates ONE continuous voiceover on eleven_v3 with the Creative
    preset (stability 0.0, similarity 0.85) — NOT multilingual_v2, which
    reads robotic. voice accepts a registry name or a raw voice_id.

    The one-take law is enforced: this never renders per-line clips. Over
    v3's 5,000-char cap it splits at a paragraph boundary into large takes
    and stitches them with a short pause.

    with_timestamps also returns character alignment, which you want for
    caption sync or for slicing a span out of a longer read. 'Velantra' is
    auto-respelled for TTS (it otherwise comes back 'Volantra'); the plain
    spelling stays in your script. v3 has no speed control — pace with
    ffmpeg atempo after generation."""
    return elevenlabs.generate_vo(script, voice, brand=brand, concept=concept,
                                   with_timestamps=with_timestamps)


@mcp.tool()
def eleven_clone_voice(reference_files: list[str], name: str,
                        description: str = "", brand: str = "",
                        tags: list[str] | None = None) -> dict:
    """Clones a voice from reference audio/video files and registers it for
    reuse. Clone from EVERY shipped segment of a creator's audio, not just
    the first — more reference audio measurably improves the clone."""
    return elevenlabs.clone_voice(reference_files, name, description=description,
                                   brand=brand, tags=tags)


# ---------------------------------------------------------------------------
# HeyGen (avatar video lip-synced to OUR audio)
# ---------------------------------------------------------------------------

@mcp.tool()
def heygen_check_quota() -> dict:
    """Reads HeyGen credit pools. ONLY the 'api' number matters for rendering —
    a large generative_credit balance does NOT enable API renders. Note that a
    quota read alone never triggers auto top-up."""
    return heygen.check_quota()


@mcp.tool()
def heygen_list_avatars(own_only: bool = True) -> dict:
    """Lists avatars. own_only=True returns the account's own avatar groups
    (newest first); False returns the full stock catalog."""
    return heygen.list_avatars(own_only=own_only)


@mcp.tool()
def heygen_check_avatar_v(look_id: str) -> dict:
    """Checks whether an avatar look supports the Avatar V engine — the
    quality path (1080x1920, far more natural expression and head motion).
    Verify this before submitting a render with engine='avatar_v'."""
    return heygen.check_avatar_v_eligible(look_id)


@mcp.tool()
def heygen_upload_audio(local_path: str) -> str:
    """Uploads an mp3 (typically an ElevenLabs one-take VO) and returns the
    audio_asset_id. This is the key move: HeyGen lip-syncs the avatar to that
    exact file, so the VO stays our continuous take with no re-read."""
    return heygen.upload_audio(local_path)


@mcp.tool()
def heygen_generate(avatar_look_id: str, audio_asset_id: str,
                     title: str = "ad-engine", aspect_ratio: str = "9:16",
                     resolution: str = "1080p", engine: str = "avatar_v",
                     brand: str | None = None, concept: str | None = None) -> dict:
    """Submits a v3 avatar render driven by our own uploaded audio.
    Non-blocking — poll with heygen_status.

    IMPORTANT: a credit failure does NOT surface here. Submission succeeds and
    returns a video_id even when the 'api' pool is empty; the failure only
    appears at poll time."""
    return heygen.generate(avatar_look_id, audio_asset_id, title=title,
                            aspect_ratio=aspect_ratio, resolution=resolution,
                            engine=engine, brand=brand, concept=concept)


@mcp.tool()
def heygen_status(job_id: str) -> dict:
    """One poll of a heygen_generate job; downloads the mp4 on success.
    If it fails on credits the result carries should_refire=True — auto
    top-up fires on the rejected render, so the correct response is to
    re-fire the generate call, not to report a hard block."""
    return heygen.status(job_id)


# ---------------------------------------------------------------------------
# Plan runner (consumes the strategize-ad-adaptation plan)
# ---------------------------------------------------------------------------

@mcp.tool()
def plan_preflight(plan: dict | str, video_model: str = "bytedance/seedance-2-5") -> dict:
    """Dry run of an adaptation plan: what would be generated, what is deferred
    to real-footage sourcing, estimated video seconds/credits, and whether the
    kie balance covers it. Run this BEFORE spending anything — auto top-up is
    broken on this account, so an insufficient balance is a hard stop.
    plan is the strategist's plan object or a path to its JSON file."""
    return plan_runner.preflight(plan, video_model=video_model)


@mcp.tool()
def plan_generate_anchors(plan: dict | str, reference_image_urls: list[str],
                           brand: str | None = None, concept: str | None = None,
                           aspect_ratio: str = "9:16",
                           resolution: str = "2K") -> dict:
    """Generates ONE still per continuity group in the plan. Run this before
    plan_generate_keyframes: if the plan says several beats show the same
    creator or location, this creates that asset a single time so every member
    beat can reference it instead of re-rolling an inconsistent version.
    Non-blocking — poll returned job_ids with kie_status."""
    return plan_runner.generate_anchors(plan, reference_image_urls, brand=brand,
                                         concept=concept, aspect_ratio=aspect_ratio,
                                         resolution=resolution)


@mcp.tool()
def plan_generate_keyframes(plan: dict | str, reference_image_urls: list[str],
                             anchor_urls: dict | None = None,
                             brand: str | None = None, concept: str | None = None,
                             aspect_ratio: str = "9:16",
                             resolution: str = "2K") -> dict:
    """One still per scene, each authored independently from canonical
    references — never chained off another clip's last frame, which is what
    causes compounding drift.

    anchor_urls maps continuity_group -> approved anchor image url (from
    plan_generate_anchors); members of a group get their anchor as the leading
    reference so identity holds across beats.

    Scenes the plan marked real_footage_required are NOT generated — they come
    back under deferred_to_sourcing with their sourcing notes. Non-blocking.

    After QA, place every keyframe on the concept's Cutroom storyboard board
    (dr-os dr_push_brief_board) and STOP for Brooks's approval on the board —
    plan_animate_scenes will not run without that board's slug."""
    return plan_runner.generate_keyframes(plan, reference_image_urls,
                                           anchor_urls=anchor_urls, brand=brand,
                                           concept=concept, aspect_ratio=aspect_ratio,
                                           resolution=resolution)


@mcp.tool()
def plan_animate_scenes(plan: dict | str, keyframe_urls: dict,
                         approved_board_slug: str = "",
                         brand: str | None = None, concept: str | None = None,
                         model: str = "bytedance/seedance-2-5",
                         aspect_ratio: str = "9:16", resolution: str = "720p",
                         generate_audio: bool = True) -> dict:
    """Animates each Brooks-approved keyframe independently.

    APPROVAL GATE (LAW): approved_board_slug is the Cutroom board holding
    these exact keyframes, approved by Brooks ON the board. Without it this
    tool dispatches NOTHING — never animate keyframes Brooks hasn't approved
    on the storyboard, and never invent a slug to get past the gate.

    keyframe_urls maps beat key -> approved still url; only pass stills that
    passed QA, since video costs far more than images. Each clip's duration
    comes from its own scene's t/t_end, so length follows the scene rather
    than the model cap. Non-blocking — poll with kie_status, then hand the
    clips plus VO to ChatCut for assembly."""
    return plan_runner.animate_scenes(plan, keyframe_urls,
                                       approved_board_slug=approved_board_slug,
                                       brand=brand,
                                       concept=concept, model=model,
                                       aspect_ratio=aspect_ratio,
                                       resolution=resolution,
                                       generate_audio=generate_audio)


if __name__ == "__main__":
    mcp.run(transport="stdio")
