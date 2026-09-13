"""Evidence-backed analysis -> edit plan contract for the internal timeline editor.

This validates the handoff, not creative quality or render support. Observations
remain separate from proposed editing decisions. No provider or renderer runs here.
"""
from __future__ import annotations

import hashlib
import json
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator

from adengine.core.errors import GateRefused

CATEGORIES = ("rushes", "cuts", "transitions", "pacing", "animations")
TICK_RATE = 6000


def assess_analysis(beats: list[dict], result: dict) -> dict:
    """Fail closed on absent, malformed, duplicate or incomplete model evidence."""
    issues = []
    expected = {b["index"] for b in beats}
    described = result.get("beats")
    indexes = [b.get("index") for b in described if isinstance(b, dict)] if isinstance(described, list) else []
    if (not beats or any(type(i) is not int for i in indexes) or
        len(indexes) != len(expected) or set(indexes) != expected):
        issues.append("Model must describe every review window exactly once")
    if any(k in result for k in ("_error", "_skipped", "_raw_gemini", "_parse_error")):
        issues.append("Model analysis failed, was skipped, or could not be parsed")
    duration = max((b["t_end"] for b in beats), default=0)
    editorial = result.get("editorial")
    editorial = editorial if isinstance(editorial, dict) else {}
    seen = set()
    for category in CATEGORIES:
        item = editorial.get(category)
        if not isinstance(item, dict):
            issues.append(f"Missing {category} analysis")
            continue
        status = item.get("status")
        observations = item.get("observations")
        if status not in ("reviewed", "not_present") or not str(item.get("summary") or "").strip():
            issues.append(f"{category}: review or explicit absence with explanation required")
        if category in ("rushes", "pacing") and status != "reviewed":
            issues.append(f"{category}: even a continuous source needs select/hold analysis")
        if not isinstance(observations, list):
            issues.append(f"{category}: observations must be a list")
            continue
        if status == "reviewed" and not observations:
            issues.append(f"{category}: reviewed requires timed observations")
        if status == "not_present" and observations:
            issues.append(f"{category}: absence conflicts with observations")
        for obs in observations:
            try:
                parsed = Observation.model_validate(obs)
                if parsed.id in seen or parsed.end_s > duration:
                    raise ValueError("duplicate id or time outside source")
                seen.add(parsed.id)
            except (ValidationError, ValueError) as exc:
                issues.append(f"{category}: invalid observation ({str(exc)[:180]})")
    return {
        "status": "complete" if not issues else "incomplete",
        "method": "scene_candidates_plus_full_video_model_pass",
        "every_frame_verified": False,
        "timing_basis": "source seconds; model event times are estimates until frame review",
        "issues": issues,
    }


class Contract(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)


class Observation(Contract):
    id: str = Field(min_length=1)
    start_s: float = Field(ge=0)
    end_s: float = Field(ge=0)
    description: str = Field(min_length=1)
    confidence: float = Field(ge=0, le=1)
    details: dict

    @model_validator(mode="after")
    def ordered(self):
        if self.end_s < self.start_s:
            raise ValueError("end_s must be >= start_s")
        return self


class Evidence(Contract):
    reference_id: str = Field(min_length=1)
    observation_id: str = Field(min_length=1)


class AnimationKey(Contract):
    at_s: float = Field(ge=0)
    value: float
    easing: Literal["linear", "easeIn", "easeOut", "easeInOut", "hold"]


class Animation(Contract):
    property: Literal["x", "y", "scale", "rotation", "opacity"]
    keyframes: list[AnimationKey] = Field(min_length=2)
    rationale: str = Field(min_length=1)


class Transition(Contract):
    kind: str = Field(min_length=1)
    duration_s: float = Field(gt=0)
    rationale: str = Field(min_length=1)


class Audio(Contract):
    gain_db: float
    fade_in_s: float = Field(ge=0)
    fade_out_s: float = Field(ge=0)


class EditClip(Contract):
    id: str = Field(min_length=1)
    asset_id: str = Field(min_length=1)
    track_id: str = Field(min_length=1)
    kind: Literal["video", "audio"]
    timeline_start_s: float = Field(ge=0)
    timeline_end_s: float = Field(gt=0)
    source_in_s: float = Field(ge=0)
    source_out_s: float = Field(gt=0)
    speed: float = Field(gt=0)
    # Required, even when empty: absence must be a conscious decision.
    animations: list[Animation]
    transition_out: Transition | None
    audio: Audio | None
    evidence: list[Evidence] = Field(min_length=1)
    rationale: str = Field(min_length=1)
    qa_checks: list[str] = Field(min_length=1)

    @model_validator(mode="after")
    def timing(self):
        duration = self.timeline_end_s - self.timeline_start_s
        if duration <= 0 or self.source_out_s <= self.source_in_s:
            raise ValueError("source and timeline ranges must be positive, end exclusive")
        if abs((self.source_out_s - self.source_in_s) / self.speed - duration) > 1 / TICK_RATE:
            raise ValueError("source duration / speed must equal timeline duration")
        if self.transition_out and self.transition_out.duration_s > duration:
            raise ValueError("transition exceeds outgoing clip")
        props = set()
        for anim in self.animations:
            if anim.property in props:
                raise ValueError("duplicate animation property")
            props.add(anim.property)
            times = [round(k.at_s * TICK_RATE) for k in anim.keyframes]
            if times != sorted(set(times)) or anim.keyframes[-1].at_s >= duration:
                raise ValueError("keyframes must be unique, ordered and inside clip (relative seconds)")
            for key in anim.keyframes:
                if anim.property == "opacity" and not 0 <= key.value <= 1:
                    raise ValueError("opacity must be 0..1")
                if anim.property == "scale" and key.value <= 0:
                    raise ValueError("scale must be positive")
        if self.audio and max(self.audio.fade_in_s, self.audio.fade_out_s) > duration:
            raise ValueError("audio fade exceeds clip")
        return self


class EditPlan(Contract):
    schema_version: Literal[1]
    title: str = Field(min_length=1)
    fps: float = Field(gt=0)
    width: int = Field(gt=0, strict=True)
    height: int = Field(gt=0, strict=True)
    duration_s: float = Field(gt=0)
    # Rationale by category covers deliberate absence as well as selected effects.
    analysis_to_edit: dict[str, str]
    clips: list[EditClip] = Field(min_length=1)
    unresolved: list[str]
    acceptance_checks: list[str] = Field(min_length=1)

    @model_validator(mode="after")
    def coverage(self):
        if set(self.analysis_to_edit) != set(CATEGORIES) or any(
            not value.strip() for value in self.analysis_to_edit.values()
        ):
            raise ValueError("analysis_to_edit must explain decisions for all five categories")
        ids = [clip.id for clip in self.clips]
        if len(set(ids)) != len(ids):
            raise ValueError("duplicate clip ids")
        tracks = {}
        for clip in self.clips:
            tracks.setdefault(clip.track_id, []).append(clip)
            if clip.timeline_end_s > self.duration_s + 1 / TICK_RATE:
                raise ValueError("clip exceeds plan duration")
        for clips in tracks.values():
            clips.sort(key=lambda clip: clip.timeline_start_s)
            if len({clip.kind for clip in clips}) != 1:
                raise ValueError("track cannot mix audio and video clips")
            for i, clip in enumerate(clips):
                nxt = clips[i + 1] if i + 1 < len(clips) else None
                if nxt and round(clip.timeline_end_s * TICK_RATE) > round(nxt.timeline_start_s * TICK_RATE):
                    raise ValueError("clips overlap on the same track")
                if clip.transition_out and (not nxt or
                    round(clip.timeline_end_s * TICK_RATE) != round(nxt.timeline_start_s * TICK_RATE) or
                    clip.transition_out.duration_s > nxt.timeline_end_s - nxt.timeline_start_s):
                    raise ValueError("transition requires an adjacent incoming clip with sufficient duration")
        spans = sorted((c.timeline_start_s, c.timeline_end_s) for c in self.clips if c.kind == "video")
        end = 0
        for start, stop in spans:
            if round(start * TICK_RATE) > round(end * TICK_RATE):
                raise ValueError("unplanned gap in visual coverage")
            end = max(end, stop)
        if round(end * TICK_RATE) != round(self.duration_s * TICK_RATE):
            raise ValueError("video must cover full plan duration")
        return self


def fingerprint(manifest: dict) -> str:
    return hashlib.sha256(json.dumps(manifest, sort_keys=True, separators=(",", ":"),
                                     allow_nan=False).encode()).hexdigest()


def validate_handoff(plan: dict, manifests: dict[str, dict]) -> EditPlan:
    try:
        parsed = EditPlan.model_validate(plan)
    except ValidationError as exc:
        raise GateRefused("Invalid edit plan", {"errors": exc.errors(include_context=False)}) from exc
    if parsed.unresolved:
        raise GateRefused("Resolve edit-plan blockers before handoff", {"unresolved": parsed.unresolved})
    observations = {}
    source_durations = {}
    for ref_id, manifest in manifests.items():
        review = assess_analysis(manifest.get("beats", []), {
            "beats": [b.get("gemini", {}) for b in manifest.get("beats", [])],
            "editorial": manifest.get("editorial"),
            **{k: v for k, v in manifest.items() if k.startswith("_")},
        })
        if review["status"] != "complete":
            raise GateRefused(f"Reference {ref_id} needs complete editorial analysis", review)
        for category in CATEGORIES:
            for observation in manifest["editorial"][category]["observations"]:
                observations[(ref_id, observation["id"])] = observation
        source_durations[manifest["video_asset_id"]] = max(b["t_end"] for b in manifest["beats"])
    for clip in parsed.clips:
        if clip.asset_id not in source_durations:
            raise GateRefused(f"Clip {clip.id}: watch the selected source asset before planning its trims")
        if clip.source_out_s > source_durations[clip.asset_id] + 1 / TICK_RATE:
            raise GateRefused(f"Clip {clip.id}: source trim exceeds inspected media")
        selected_source_evidence = False
        for evidence in clip.evidence:
            if (evidence.reference_id, evidence.observation_id) not in observations:
                raise GateRefused(f"Clip {clip.id}: missing observation {evidence.observation_id}")
            observation = observations[(evidence.reference_id, evidence.observation_id)]
            if (manifests[evidence.reference_id]["video_asset_id"] == clip.asset_id and
                observation["start_s"] < clip.source_out_s and observation["end_s"] > clip.source_in_s):
                selected_source_evidence = True
        if not selected_source_evidence:
            raise GateRefused(f"Clip {clip.id}: cite an observation covering its selected source range")
    return parsed
