"""Brand / product context and playbook access for the dr tools.

Brands and products are Store records. Global judgment laws come from
adengine.laws, playbooks from adengine.playbooks, product-truth rendering from
adengine.product_truth; each is imported lazily and degrades to a clear error
dict when the package is not in the build yet.
"""
from __future__ import annotations

from typing import Any

from adengine.core.errors import NotFound

from . import artifacts
from .deps import brand_by_slug, optional_module, product_by_slug, store, unavailable, ws

CAP = 25_000


def _cap(text: Any, cap: int = CAP) -> Any:
    if not isinstance(text, str) or len(text) <= cap:
        return text
    return text[:cap] + "\n\n[TRUNCATED]"


def judgment_laws() -> dict[str, Any]:
    laws = optional_module("adengine.laws")
    if laws is None or not hasattr(laws, "judgment_laws"):
        return unavailable("adengine.laws", {"text": None})
    try:
        return {"text": _cap(laws.judgment_laws())}
    except Exception as exc:  # noqa: BLE001
        return {"error": f"adengine.laws.judgment_laws failed: {exc}", "text": None}


def render_product(rec: dict[str, Any]) -> dict[str, Any]:
    pt = optional_module("adengine.product_truth")
    if pt is None or not hasattr(pt, "render_blocks"):
        return unavailable("adengine.product_truth", {"blocks": None, "truth": rec.get("truth") or {}})
    try:
        return {"blocks": pt.render_blocks(rec.get("truth") or rec)}
    except Exception as exc:  # noqa: BLE001
        return {"error": f"adengine.product_truth.render_blocks failed: {exc}", "blocks": None,
                "truth": rec.get("truth") or {}}


def _product_summary(p: dict[str, Any]) -> dict[str, Any]:
    return {"id": p["id"], "slug": p.get("slug"), "name": p.get("name"), "code": p.get("code")}


def load_brand(brand_slug: str) -> dict[str, Any]:
    try:
        brand = brand_by_slug(brand_slug)
    except NotFound:
        available = sorted(b.get("slug") for b in store().find("brand", ws()) if b.get("slug"))
        return {"error": f"unknown brand '{brand_slug}'", "available": available}

    products = store().find("product", ws(), brand_id=brand["id"])
    products.sort(key=lambda p: p.get("slug") or "")
    angle_bank = artifacts.find_artifact(brand, "angle-bank", "angle-bank")
    inventory = artifacts.list_artifacts(brand_slug)["artifacts"]
    laws = judgment_laws()

    return {
        "brand": brand_slug,
        "brand_id": brand["id"],
        "name": brand.get("name"),
        "code": brand.get("code"),
        "brief": brand.get("brief") or {},
        "house_laws": brand.get("house_laws") or [],
        "global_laws": laws.get("text"),
        "global_laws_status": {k: v for k, v in laws.items() if k != "text"} or "ok",
        "angle_bank": _cap(angle_bank.get("body")) if angle_bank else None,
        "angle_bank_version": angle_bank.get("version") if angle_bank else None,
        "artifacts": inventory,
        "products": [_product_summary(p) for p in products],
        "product_truth_note": ("Call load_product(brand_slug, product_slug) BEFORE writing any adaptation "
                               "instruction, script, or prompt that shows the product. The rendered blocks "
                               "are verbatim and mandatory."),
    }


def load_product(brand_slug: str, product_slug: str) -> dict[str, Any]:
    brand = brand_by_slug(brand_slug)
    try:
        rec = product_by_slug(brand, product_slug)
    except NotFound:
        available = sorted(p.get("slug") for p in store().find("product", ws(), brand_id=brand["id"]))
        return {"error": f"unknown product '{product_slug}' for brand '{brand_slug}'", "available": available}
    rendered = render_product(rec)
    return {"brand": brand_slug, "product": _product_summary(rec), "truth": rec.get("truth") or {},
            **rendered}


# Pipeline step name -> (playbook name, module file or None, role). The guide speaks in
# step names; the registry speaks in playbook names. Raw playbook names always work too.
PIPELINE_STEPS: dict[str, tuple[str, str | None, str]] = {
    "router":            ("direct-response-os", None, "The DR OS router: which playbook to run, in what order, cold start vs warm loop."),
    "laws":              ("direct-response-os", "modules/laws.md", "The twelve laws. Load before writing ANY copy, angle, or brief."),
    "angle-schema":      ("direct-response-os", "modules/angle-schema.md", "The one record format the whole system shares."),
    "artifact-contract": ("direct-response-os", "modules/artifacts.md", "Where every artifact lives and who reads what."),
    "voc-mining":        ("dr-voc-mining", None, "Raw reviews/Reddit/comments -> voc-index."),
    "survey-designer":   ("dr-survey-designer", None, "Design the post-purchase survey instrument."),
    "market-intel":      ("dr-market-intel", None, "Competitor scan / winner documentation -> market-gaps, winners."),
    "angle-bank":        ("dr-angle-bank", None, "Merge research into the durable angle bank."),
    "awareness-audit":   ("dr-awareness-audit", None, "Which awareness level the account is starved at."),
    "hook-lab":          ("dr-hook-lab", None, "Hooks for one angle record."),
    "ugc-brief":         ("dr-ugc-brief", None, "Creator-facing brief from one angle + hooks."),
    "funnel-strategy":   ("dr-funnel-strategy", None, "Architecture + 90-day roadmap."),
    "strategize":        ("strategize-ad-adaptation", None, "Watched-reference manifest -> scene-by-scene adaptation plan (the strategist layer)."),
    "brief-board":       ("video-editor-brief", None, "Turn beats + registered frame assets into an in-app storyboard spec."),
    "app-board":         ("video-editor-brief", None, "Plan the editor-facing brief that is persisted with push_board."),
    "editor-brief":      ("video-editor-brief", None, "Script + scene assets -> written editor brief with timeline."),
    "long-form-copy":    ("long-form-copy", None, "Laws for long-form / spoken copy, incl. the script naturalizer."),
    "ad-watcher":        ("ad-watcher", None, "The psychological teardown layer applied on top of a watch manifest."),
}


def _resolve_step(pb, name: str) -> tuple[str, str | None]:
    """(playbook name, module file) for a step alias or a raw playbook name."""
    try:
        pb.get(name)
        return name, None
    except Exception:  # noqa: BLE001 - not a raw name; try the alias table
        pass
    if name in PIPELINE_STEPS:
        target, rel, _ = PIPELINE_STEPS[name]
        return target, rel
    raise NotFound(f"no playbook or pipeline step named '{name}'")


def list_playbooks() -> dict[str, Any]:
    pb = optional_module("adengine.playbooks")
    if pb is None:
        return unavailable("adengine.playbooks")
    out: dict[str, Any] = {}
    try:
        out["stages"] = pb.stages() if hasattr(pb, "stages") else None
        registry = pb.registry() if hasattr(pb, "registry") else []
        out["playbooks"] = registry
        known = {p["name"] for p in registry}
        out["pipeline_steps"] = {
            step: {"role": role, "playbook": target, "file": rel, "available": target in known}
            for step, (target, rel, role) in PIPELINE_STEPS.items()}
    except Exception as exc:  # noqa: BLE001
        return {"error": f"adengine.playbooks failed: {exc}"}
    out["note"] = ("get_playbook(name, section=None) accepts a pipeline step name or any raw "
                   "playbook name and serves the full text or one section.")
    return out


def get_playbook(name: str, section: str | None = None, max_chars: int = 60_000) -> dict[str, Any]:
    pb = optional_module("adengine.playbooks")
    if pb is None:
        return unavailable("adengine.playbooks", {"name": name})
    try:
        target, rel = _resolve_step(pb, name)
        if rel is not None:
            content = pb.read_file(target, rel, max_chars=max_chars)
        elif hasattr(pb, "read"):
            content = pb.read(target, section=section, max_chars=max_chars)
        else:
            content = pb.get(target)
    except NotFound as exc:
        return {"error": str(exc), "name": name, "known_steps": sorted(PIPELINE_STEPS)}
    except Exception as exc:  # noqa: BLE001
        return {"error": f"could not read playbook '{name}': {exc}", "name": name}
    if isinstance(content, dict):
        return {"name": name, "resolved": target, "file": rel, "section": section, **content}
    text = content if isinstance(content, str) else str(content)
    return {"name": name, "resolved": target, "file": rel, "section": section,
            "content": text[:max_chars], "truncated": len(text) > max_chars}
