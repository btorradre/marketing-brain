"""Plan runner — turns a strategist adaptation plan into generation job requests.

This module is deliberately DUMB about creative judgment. Every decision about
what a scene needs (its adaptation_type, whether it can be generated at all,
which scenes share an asset) was already made by the strategist reasoning pass
and travels IN the plan. There is no brand switch, no concept-type branch, and
no format special-casing in here.

What this module DOES own is mechanical correctness:

  KEYFRAME-FIRST, NEVER CHAINED. One still per scene, each authored
  independently from canonical references. No clip is ever seeded from another
  clip's last frame — chaining makes every generation inherit the previous
  one's errors. Independent stills conditioned on shared references cannot
  compound. Continuity must therefore be restated per prompt, which is what
  continuity groups are for.

  CONTINUITY GROUPS GENERATE ONCE. If the plan says beats 2, 5 and 8 are the
  same creator, that anchor is generated a single time and its image is passed
  as a reference into every member scene.

  AUTHENTICITY IS HONORED. Scenes marked real_footage_required / source_existing
  are never generated — they are emitted as sourcing tasks.

  STILLS BEFORE VIDEO CREDIT. Keyframes are auditable before animation spend.

  BOARD APPROVAL GATE. Animation only fires for keyframes that sit on an
  approved storyboard board; adengine.gen.server.animate_scenes enforces it.

The functions here build job INPUTS; the server enqueues them and the worker
uploads reference assets to the provider and fires the tasks.
"""
from __future__ import annotations

from adengine.engines import kie

IMAGE_MODEL = kie.IMAGE_MODEL_I2I
DEFAULT_VIDEO_MODEL = kie.DEFAULT_VIDEO_MODEL

# Plan-declared types that must never be sent to a photoreal generator.
NON_GENERATED_AUTHENTICITY = {"real_footage_required", "source_existing"}


def scene_key(scene: dict) -> str:
    return str(scene.get("source_beat_index", scene.get("index", "?")))


def _scenes(plan: dict) -> list[dict]:
    if not isinstance(plan, dict):
        raise ValueError("plan must be the strategist's plan object (a JSON object)")
    return list(plan.get("scenes", []))


def preflight(plan: dict, video_model: str = DEFAULT_VIDEO_MODEL,
              balance: float | None = None) -> dict:
    """Dry run. Reports what WOULD be generated, what is deferred to sourcing,
    the estimated credit cost, and whether the balance covers it — before a
    single credit is spent. An insufficient balance is a hard stop."""
    scenes = _scenes(plan)
    groups = plan.get("continuity_groups", {}) or {}

    to_generate, to_source, anchors = [], [], []
    for scene in scenes:
        auth = scene.get("authenticity", "generate")
        entry = {"beat": scene_key(scene),
                 "adaptation_type": scene.get("adaptation_type"),
                 "authenticity": auth,
                 "continuity_group": scene.get("continuity_group")}
        (to_source if auth in NON_GENERATED_AUTHENTICITY else to_generate).append(entry)
    for name, group in groups.items():
        anchors.append({"group": name, "description": group.get("description"),
                        "member_beats": group.get("member_beats", [])})

    video_seconds = sum(
        max(0.0, float(s.get("t_end", 0)) - float(s.get("t", 0)))
        for s in scenes if s.get("authenticity", "generate") not in NON_GENERATED_AUTHENTICITY)
    video_credits = kie.estimate_credits(video_model, video_seconds)
    return {
        "n_scenes": len(scenes),
        "anchors_to_generate": anchors,
        "scenes_to_generate": to_generate,
        "scenes_deferred_to_sourcing": to_source,
        "estimated_images": len(to_generate) + len(anchors),
        "estimated_video_seconds": round(video_seconds, 2),
        "estimated_video_credits": video_credits,
        "estimated_video_usd": kie.credits_to_usd(video_credits),
        "video_model": video_model,
        "provider_balance": balance,
        "sufficient_balance": (None if (video_credits is None or balance is None)
                               else balance >= video_credits),
        "note": ("Video credits are the dominant cost; image cost is not estimated here. "
                 "Automatic top-up cannot be relied on — treat an insufficient balance as a "
                 "hard stop."),
    }


def anchor_requests(plan: dict, ref_asset_ids: list[str], aspect_ratio: str = "9:16",
                    resolution: str = "2K") -> tuple[list[dict], list[dict]]:
    """ONE still per continuity group. Returns (job_inputs, errors)."""
    groups = plan.get("continuity_groups", {}) or {}
    inputs, errors = [], []
    for name, group in groups.items():
        prompt = group.get("prompt") or group.get("description")
        if not prompt:
            errors.append({"group": name, "error": "continuity group has no description/prompt"})
            continue
        inputs.append({
            "model": IMAGE_MODEL,
            "input": {"prompt": prompt, "aspect_ratio": aspect_ratio, "resolution": resolution},
            "asset_refs": {"input_urls": list(ref_asset_ids)},
            "purpose": "anchor", "group": name,
            "member_beats": group.get("member_beats", []),
        })
    return inputs, errors


def keyframe_requests(plan: dict, ref_asset_ids: list[str], anchors: dict[str, str] | None = None,
                      aspect_ratio: str = "9:16", resolution: str = "2K") -> tuple[list[dict], list[dict]]:
    """One still per scene, each authored independently (never chained).
    anchors maps continuity_group -> approved anchor ASSET id; members get it
    prepended to their references (anchor first = strongest identity signal).
    Returns (job_inputs, deferred_to_sourcing)."""
    anchors = anchors or {}
    inputs, deferred = [], []
    for scene in _scenes(plan):
        key = scene_key(scene)
        auth = scene.get("authenticity", "generate")
        if auth in NON_GENERATED_AUTHENTICITY:
            deferred.append({"beat": key, "authenticity": auth,
                             "adaptation_type": scene.get("adaptation_type"),
                             "sourcing_note": scene.get("adaptation_instructions")})
            continue
        prompt = scene.get("adaptation_instructions")
        if not prompt:
            deferred.append({"beat": key, "error": "scene has no adaptation_instructions"})
            continue
        group = scene.get("continuity_group")
        refs = list(ref_asset_ids)
        if group and group in anchors:
            refs = [anchors[group]] + refs
        inputs.append({
            "model": IMAGE_MODEL,
            "input": {"prompt": prompt, "aspect_ratio": aspect_ratio, "resolution": resolution},
            "asset_refs": {"input_urls": refs},
            "purpose": "keyframe", "beat": key, "group": group,
        })
    return inputs, deferred


def animation_requests(plan: dict, keyframes: dict[str, str], model: str = DEFAULT_VIDEO_MODEL,
                       aspect_ratio: str = "9:16", resolution: str = "720p",
                       generate_audio: bool = True) -> tuple[list[dict], list[dict]]:
    """Each approved keyframe animated INDEPENDENTLY. keyframes maps beat key ->
    approved keyframe ASSET id. Duration follows the scene's own t/t_end,
    clamped to the model's supported range. Returns (job_inputs, skipped)."""
    inputs, skipped = [], []
    for scene in _scenes(plan):
        key = scene_key(scene)
        if key not in keyframes:
            skipped.append({"beat": key, "reason": "no approved keyframe asset supplied"})
            continue
        duration = max(0.0, float(scene.get("t_end", 0)) - float(scene.get("t", 0)))
        duration = max(4, min(round(duration) or 4, 30))
        motion = scene.get("motion_prompt") or scene.get("adaptation_instructions") or ""
        inputs.append({
            "model": model,
            "input": {"prompt": motion, "aspect_ratio": aspect_ratio, "resolution": resolution,
                      "duration": duration, "generate_audio": generate_audio},
            "asset_refs": {"first_frame_url": keyframes[key]},
            "purpose": "animation", "beat": key, "duration": duration,
        })
    return inputs, skipped
