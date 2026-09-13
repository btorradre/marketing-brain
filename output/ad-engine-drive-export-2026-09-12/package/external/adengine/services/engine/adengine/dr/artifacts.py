"""The DR OS artifact contract, enforced at the write boundary, on Store records.

Artifact record: id, workspace_id, brand_id, kind, name, body,
frontmatter {brand, artifact, generated_by, updated, sources}, version.
Singletons are keyed (kind, name=kind); collections need a name. Saving the
same (kind, name) again overwrites in place and bumps version. Every save runs
the law gate; blockers stop the save unless force=True.
"""
from __future__ import annotations

from adengine.core.auth import require_write

import datetime
import re
from typing import Any

from . import lawgate
from .deps import brand_by_slug, store, ws

SINGLETONS = ("voc-index", "angle-bank", "awareness-map", "market-gaps", "funnel-strategy")
COLLECTIONS = ("survey", "winner", "hooks", "brief", "adaptation-plan")


def slugify(s: str) -> str:
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", (s or "").lower())).strip("-")


def _resolve_name(kind: str, name: str | None) -> tuple[str | None, dict | None]:
    """Returns (record name, error dict)."""
    if kind in SINGLETONS:
        return kind, None
    if kind in COLLECTIONS or name:
        if not name:
            return None, {"error": f"'{kind}' is a collection; pass name (e.g. '2026-08-17-VEL-12-ugc')"}
        return slugify(name), None
    return None, {"error": f"unknown artifact kind '{kind}'",
                  "known": {"singletons": list(SINGLETONS), "collections": list(COLLECTIONS)},
                  "hint": "Unknown kinds are accepted as collections when a name is passed."}


def _summary(rec: dict[str, Any]) -> dict[str, Any]:
    return {"id": rec["id"], "kind": rec["kind"], "name": rec["name"],
            "version": rec.get("version", 1), "size": len(rec.get("body") or ""),
            "updated": (rec.get("frontmatter") or {}).get("updated"),
            "generated_by": (rec.get("frontmatter") or {}).get("generated_by")}


def list_artifacts(brand_slug: str) -> dict[str, Any]:
    brand = brand_by_slug(brand_slug)
    rows = store().find("artifact", ws(), brand_id=brand["id"])
    rows.sort(key=lambda r: (r["kind"], r["name"]))
    return {"brand": brand_slug, "artifacts": [_summary(r) for r in rows],
            "artifact_types": {"singletons": list(SINGLETONS), "collections": list(COLLECTIONS)}}


def find_artifact(brand: dict[str, Any], kind: str, name: str) -> dict[str, Any] | None:
    rows = store().find("artifact", ws(), brand_id=brand["id"], kind=kind, name=name)
    return rows[0] if rows else None


def read_artifact(brand_slug: str, kind: str, name: str | None = None) -> dict[str, Any]:
    brand = brand_by_slug(brand_slug)
    if kind not in SINGLETONS and name is None:
        rows = store().find("artifact", ws(), brand_id=brand["id"], kind=kind)
        if kind not in COLLECTIONS and not rows:
            return {"error": f"unknown artifact kind '{kind}'",
                    "known": {"singletons": list(SINGLETONS), "collections": list(COLLECTIONS)}}
        return {"kind": kind, "listing": True,
                "available": sorted(r["name"] for r in rows),
                "hint": f"'{kind}' is a collection; pass name to read one."}
    rec_name, err = _resolve_name(kind, name)
    if err:
        return err
    rec = find_artifact(brand, kind, rec_name)
    if rec is None:
        return {"error": f"not written yet: {kind}/{rec_name}", "brand": brand_slug}
    return {"id": rec["id"], "brand": brand_slug, "kind": kind, "name": rec_name,
            "version": rec.get("version", 1), "frontmatter": rec.get("frontmatter") or {},
            "body": rec.get("body") or ""}


@require_write
def save_artifact(brand_slug: str, kind: str, body: str, name: str | None = None,
                  force: bool = False, speaker: str | None = None,
                  sources: list[str] | None = None,
                  generated_by: str = "adengine-dr") -> dict[str, Any]:
    brand = brand_by_slug(brand_slug)
    rec_name, err = _resolve_name(kind, name)
    if err:
        return err

    gate = lawgate.check(body, brand_slug=brand_slug, speaker=speaker)
    if gate["blockers"] and not force:
        return {"saved": False, "kind": kind, "name": rec_name, "lawgate": gate,
                "hint": ("Fix the blockers (they are house laws, not style notes). "
                         "force=True only if a match is a provable false positive.")}

    frontmatter = {"brand": brand_slug, "artifact": kind, "generated_by": generated_by,
                   "updated": datetime.date.today().isoformat(),
                   "sources": list(sources or [])}
    existing = find_artifact(brand, kind, rec_name)
    if existing is None:
        rec = store().create("artifact", ws(), "art", brand_id=brand["id"], kind=kind,
                             name=rec_name, body=body, frontmatter=frontmatter, version=1)
    else:
        rec = store().update("artifact", ws(), existing["id"], body=body, frontmatter=frontmatter,
                             version=int(existing.get("version", 1)) + 1)
    return {"saved": True, "id": rec["id"], "brand": brand_slug, "kind": kind, "name": rec_name,
            "version": rec["version"], "forced": bool(force and gate["blockers"]),
            "frontmatter": frontmatter, "lawgate": gate}
