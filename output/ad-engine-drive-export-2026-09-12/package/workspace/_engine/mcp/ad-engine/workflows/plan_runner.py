"""Plan runner — turns a strategist adaptation plan into generated assets.

This module is deliberately DUMB about creative judgment. Every decision about
what a scene needs (its adaptation_type, whether it can be generated at all,
which scenes share an asset) was already made by the strategize-ad-adaptation
reasoning pass and travels IN the plan. There is no brand switch, no
concept-type branch, and no format special-casing in here — adding one would
move judgment out of the strategist and into code that cannot reason.

What this module DOES own is mechanical correctness:

  KEYFRAME-FIRST, NEVER CHAINED. One still per scene, each authored
  independently from canonical references. No clip is ever seeded from another
  clip's last frame — chaining makes every generation inherit the previous
  one's errors (this is how a bag's belts multiplied into a lattice across
  segments). Independent stills conditioned on shared references cannot
  compound. The trade: continuity must be restated in every prompt, which is
  what continuity groups are for.

  CONTINUITY GROUPS GENERATE ONCE. If the plan says beats 2, 5 and 8 are the
  same creator, that anchor is generated a single time and its image is passed
  as a reference into every member scene, rather than re-rolling a fresh (and
  different-looking) person per beat.

  AUTHENTICITY IS HONORED. Scenes marked real_footage_required are never
  generated — they are emitted as sourcing tasks. Faking a genuine physical
  action is the exact failure mode that reads as AI.

  STILLS BEFORE VIDEO CREDIT. Keyframes are auditable before any (much more
  expensive) animation spend.

  CUTROOM APPROVAL GATE (Brooks, 2026-08-18). Generated keyframes must be
  placed on the concept's Cutroom storyboard board (dr-os
  dr_push_brief_board) and approved by Brooks ON the board before any
  animation fires. animate_scenes enforces this mechanically: it requires
  the approved board's slug and refuses to dispatch without one.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import cost_ledger
import db
from engines import kie

IMAGE_MODEL = "gpt-image-2-image-to-image"
DEFAULT_VIDEO_MODEL = "bytedance/seedance-2-5"

# Plan-declared types that must never be sent to a photoreal generator.
NON_GENERATED_AUTHENTICITY = {"real_footage_required", "source_existing"}


def _load_plan(plan: dict | str) -> dict:
    if isinstance(plan, str):
        p = Path(plan).expanduser()
        if not p.exists():
            raise FileNotFoundError(f"plan file not found: {p}")
        return json.loads(p.read_text())
    return plan


def _scene_key(scene: dict) -> str:
    return str(scene.get("source_beat_index", scene.get("index", "?")))


def preflight(plan: dict | str, video_model: str = DEFAULT_VIDEO_MODEL) -> dict:
    """Dry run. Reports what WOULD be generated, what is deferred to sourcing,
    and the estimated credit cost — before a single credit is spent.

    kie auto top-up is broken on this account, so an over-budget plan is a hard
    stop, not a warning. Always run this before generate_keyframes."""
    plan = _load_plan(plan)
    scenes = plan.get("scenes", [])
    groups = plan.get("continuity_groups", {})

    to_generate, to_source, anchors = [], [], []
    for scene in scenes:
        auth = scene.get("authenticity", "generate")
        entry = {"beat": _scene_key(scene),
                 "adaptation_type": scene.get("adaptation_type"),
                 "authenticity": auth,
                 "continuity_group": scene.get("continuity_group")}
        (to_source if auth in NON_GENERATED_AUTHENTICITY else to_generate).append(entry)

    for name, group in groups.items():
        anchors.append({"group": name, "description": group.get("description"),
                         "member_beats": group.get("member_beats", [])})

    n_images = len(to_generate) + len(anchors)
    video_seconds = sum(
        max(0.0, float(s.get("t_end", 0)) - float(s.get("t", 0)))
        for s in scenes
        if s.get("authenticity", "generate") not in NON_GENERATED_AUTHENTICITY
    )
    video_credits = cost_ledger.estimate_credits("kie", video_model, video_seconds)

    balance = kie.balance()
    return {
        "n_scenes": len(scenes),
        "anchors_to_generate": anchors,
        "scenes_to_generate": to_generate,
        "scenes_deferred_to_sourcing": to_source,
        "estimated_images": n_images,
        "estimated_video_seconds": round(video_seconds, 2),
        "estimated_video_credits": video_credits,
        "kie_balance": balance,
        "sufficient_balance": (
            None if (video_credits is None or balance is None)
            else balance >= video_credits),
        "note": ("Video credits are the dominant cost; image cost is not "
                 "estimated here. kie auto top-up is broken — treat an "
                 "insufficient balance as a hard stop."),
    }


def generate_anchors(plan: dict | str, reference_image_urls: list[str],
                      brand: str | None = None, concept: str | None = None,
                      aspect_ratio: str = "9:16", resolution: str = "2K") -> dict:
    """Generates ONE still per continuity group. Run this BEFORE
    generate_keyframes so member scenes can reference their anchor and stay
    visually consistent. Non-blocking: returns job ids to poll with kie_status."""
    plan = _load_plan(plan)
    groups = plan.get("continuity_groups", {})
    brand = brand or plan.get("brand")
    concept = concept or plan.get("concept")

    dispatched = {}
    for name, group in groups.items():
        prompt = group.get("prompt") or group.get("description")
        if not prompt:
            dispatched[name] = {"error": "continuity group has no description/prompt"}
            continue
        result = kie.generate(
            IMAGE_MODEL,
            {"prompt": prompt, "input_urls": reference_image_urls,
             "aspect_ratio": aspect_ratio, "resolution": resolution},
            brand=brand, concept=concept)
        dispatched[name] = {**result, "member_beats": group.get("member_beats", [])}
    return {"anchors": dispatched,
            "next": "Poll each job_id with kie_status, QA every anchor image, then "
                     "call generate_keyframes with anchor_urls mapping group -> image url."}


def generate_keyframes(plan: dict | str, reference_image_urls: list[str],
                        anchor_urls: dict | None = None,
                        brand: str | None = None, concept: str | None = None,
                        aspect_ratio: str = "9:16", resolution: str = "2K") -> dict:
    """One still per scene, each authored independently (never chained).

    reference_image_urls: canonical product/brand refs, passed into EVERY scene.
    anchor_urls: {continuity_group_name: image_url} from generate_anchors —
    a scene in a group gets its anchor prepended to its references so the same
    avatar/location carries across all its beats.

    Scenes the plan marked real_footage_required or source_existing are NOT
    generated; they come back under `deferred_to_sourcing` with their notes.
    Non-blocking — poll each returned job_id with kie_status."""
    plan = _load_plan(plan)
    anchor_urls = anchor_urls or {}
    brand = brand or plan.get("brand")
    concept = concept or plan.get("concept")

    dispatched, deferred = [], []
    for scene in plan.get("scenes", []):
        key = _scene_key(scene)
        auth = scene.get("authenticity", "generate")
        if auth in NON_GENERATED_AUTHENTICITY:
            deferred.append({
                "beat": key, "authenticity": auth,
                "adaptation_type": scene.get("adaptation_type"),
                "sourcing_note": scene.get("adaptation_instructions"),
            })
            continue

        prompt = scene.get("adaptation_instructions")
        if not prompt:
            deferred.append({"beat": key, "error": "scene has no adaptation_instructions"})
            continue

        group = scene.get("continuity_group")
        urls = list(reference_image_urls)
        if group and group in anchor_urls:
            urls = [anchor_urls[group]] + urls  # anchor first = strongest identity signal

        result = kie.generate(
            IMAGE_MODEL,
            {"prompt": prompt, "input_urls": urls,
             "aspect_ratio": aspect_ratio, "resolution": resolution},
            brand=brand, concept=concept)
        dispatched.append({"beat": key, "continuity_group": group, **result})

    return {
        "dispatched": dispatched,
        "deferred_to_sourcing": deferred,
        "next": ("Poll each job_id with kie_status and QA every still (re-roll "
                  "fails). Then place every keyframe on the concept's Cutroom "
                  "storyboard board (dr-os dr_push_brief_board) and STOP — "
                  "Brooks approves the keyframes ON the board. Only then call "
                  "animate_scenes with the approved board's slug."),
    }


def animate_scenes(plan: dict | str, keyframe_urls: dict,
                    approved_board_slug: str = "",
                    brand: str | None = None, concept: str | None = None,
                    model: str = DEFAULT_VIDEO_MODEL,
                    aspect_ratio: str = "9:16", resolution: str = "720p",
                    generate_audio: bool = True) -> dict:
    """Animates each approved keyframe INDEPENDENTLY (no chaining).

    APPROVAL GATE (LAW): approved_board_slug is the Cutroom board that holds
    these exact keyframes, which Brooks has approved on the board. Without
    it nothing is dispatched — rendering is the expensive irreversible step
    and approval happens at the still-image stage, on the board.

    keyframe_urls: {beat_key: image_url} — only pass stills that passed QA.
    Each scene's duration comes from its own t/t_end in the plan, rounded to
    the model's supported range, so segment length follows the SCENE rather
    than the model's max duration.

    Non-blocking — poll each job_id with kie_status."""
    if not (approved_board_slug or "").strip():
        return {
            "error": "approval gate: no approved_board_slug supplied",
            "law": ("Keyframes must be placed on the Cutroom storyboard "
                     "board (dr-os dr_push_brief_board) and approved by "
                     "Brooks ON the board before animation. Pass that "
                     "board's slug as approved_board_slug once he has."),
            "dispatched": [],
        }
    plan = _load_plan(plan)
    brand = brand or plan.get("brand")
    concept = concept or plan.get("concept")

    balance = kie.balance()
    dispatched, skipped = [], []
    for scene in plan.get("scenes", []):
        key = _scene_key(scene)
        if key not in keyframe_urls:
            skipped.append({"beat": key, "reason": "no approved keyframe url supplied"})
            continue

        duration = max(0.0, float(scene.get("t_end", 0)) - float(scene.get("t", 0)))
        duration = max(4, min(round(duration) or 4, 30))  # model-supported range

        motion = (scene.get("motion_prompt") or scene.get("adaptation_instructions") or "")
        payload = {"prompt": motion, "first_frame_url": keyframe_urls[key],
                    "aspect_ratio": aspect_ratio, "resolution": resolution,
                    "duration": duration, "generate_audio": generate_audio}
        result = kie.generate(model, payload, brand=brand, concept=concept)
        dispatched.append({"beat": key, "duration": duration, **result})

    return {
        "dispatched": dispatched,
        "skipped": skipped,
        "approved_board_slug": approved_board_slug,
        "kie_balance_before": balance,
        "next": ("Poll each job_id with kie_status, then hand the finished clips "
                  "plus the VO to ChatCut for assembly."),
    }
