"""The DR OS artifact contract, enforced at the write boundary.

Mirrors .claude/skills/direct-response-os/modules/artifacts.md — every
artifact lands under brands/<brand>/research/dr-os/ with frontmatter, and
every save runs the law-gate. Blockers stop the save unless force=True.
"""

import datetime
import re

import lawgate
from paths import BRANDS

SINGLETONS = {
    "voc-index": "voc-index.md",
    "angle-bank": "angle-bank.md",
    "awareness-map": "awareness-map.md",
    "market-gaps": "market-gaps.md",
    "funnel-strategy": "funnel-strategy.md",
}
COLLECTIONS = {
    "survey": "surveys",
    "winner": "winners",
    "hooks": "hooks",
    "brief": "briefs",
    "adaptation-plan": "adaptation-plans",   # strategize output, so it persists
}


def _slug(s: str) -> str:
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", s.lower())).strip("-")


def _dr_os_dir(brand: str):
    return BRANDS / brand / "research" / "dr-os"


def list_artifacts(brand: str) -> dict:
    base = _dr_os_dir(brand)
    if not (BRANDS / brand).is_dir():
        return {"error": f"unknown brand '{brand}'"}
    files = []
    if base.is_dir():
        for p in sorted(base.rglob("*")):
            if p.is_file():
                files.append({"path": str(p.relative_to(base)), "size": p.stat().st_size})
    return {"brand": brand, "root": str(base), "files": files,
            "artifact_types": {"singletons": sorted(SINGLETONS), "collections": sorted(COLLECTIONS)}}


def read_artifact(brand: str, artifact: str, name: str | None = None) -> dict:
    base = _dr_os_dir(brand)
    if artifact in SINGLETONS:
        path = base / SINGLETONS[artifact]
    elif artifact in COLLECTIONS:
        folder = base / COLLECTIONS[artifact]
        if name is None:
            options = sorted(p.name for p in folder.glob("*")) if folder.is_dir() else []
            return {"error": f"'{artifact}' is a collection — pass name", "available": options}
        path = folder / (name if name.endswith((".md", ".json")) else name + ".md")
    else:
        return {"error": f"unknown artifact type '{artifact}'",
                "known": sorted(SINGLETONS) + sorted(COLLECTIONS)}
    if not path.is_file():
        return {"error": f"not written yet: {path}"}
    return {"path": str(path), "content": path.read_text(errors="replace")}


def save_artifact(brand: str, artifact: str, content: str, name: str | None = None,
                  sources: list[str] | None = None, generated_by: str = "dr-os-mcp",
                  speaker: str | None = None, force: bool = False) -> dict:
    if not (BRANDS / brand).is_dir():
        return {"error": f"unknown brand '{brand}'"}
    base = _dr_os_dir(brand)

    if artifact in SINGLETONS:
        path = base / SINGLETONS[artifact]
    elif artifact in COLLECTIONS:
        if not name:
            return {"error": f"'{artifact}' is a collection — pass name (e.g. '2026-08-17-VEL-12-ugc')"}
        fname = name if name.endswith((".md", ".json")) else _slug(name) + ".md"
        path = base / COLLECTIONS[artifact] / fname
    else:
        return {"error": f"unknown artifact type '{artifact}'",
                "known": sorted(SINGLETONS) + sorted(COLLECTIONS)}

    gate = lawgate.check(content, brand=brand, speaker=speaker)
    if gate["blockers"] and not force:
        return {"saved": False, "path": str(path), "lawgate": gate,
                "hint": "Fix the blockers (they are house laws, not style notes). force=True only if a match is a provable false positive."}

    if not content.lstrip().startswith("---") and path.suffix == ".md":
        fm = ["---", f"brand: {brand}", f"artifact: {artifact}",
              f"generated_by: {generated_by}",
              f"updated: {datetime.date.today().isoformat()}", "sources:"]
        fm += [f"  - {s}" for s in (sources or [])] or ["  - []"]
        content = "\n".join(fm) + "\n---\n\n" + content

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    return {"saved": True, "path": str(path), "lawgate": gate}
