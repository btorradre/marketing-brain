"""Laws as data.

Regex laws: LAWS_DIR/global.json + LAWS_DIR/examples/<brand>.json (adengine
shape). Judgment laws: LAWS_DIR/house-laws.md, sectioned by pipeline stage
with `## ` headers, so a workflow can pull only the stages it touches.
"""

from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path

from . import settings

STAGE_HEADERS = {
    "research": "## Research and strategy",
    "angles": "## Angles and hooks",
    "script": "## Script and copy",
    "storyboard": "## Storyboard and keyframes",
    "generation": "## Generation (image/video/voice)",
    "editing": "## Editing and assembly",
    "delivery": "## Delivery and QA",
    "ops": "## Ops and finance",
}


def _load_json(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    try:
        data = json.loads(path.read_text())
        return data if isinstance(data, list) else []
    except json.JSONDecodeError:
        return []


@lru_cache(maxsize=None)
def regex_rules(brand: str | None) -> list[dict]:
    rules = [dict(r, brand=None) for r in _load_json(settings.LAWS_DIR / "global.json")]
    if brand:
        for p in (settings.LAWS_DIR / "examples" / f"{brand}.json",
                  settings.LAWS_DIR / f"{brand}.json"):
            rules += [dict(r, brand=brand) for r in _load_json(p)]
    compiled = []
    for r in rules:
        try:
            flags = re.I if "i" in (r.get("flags") or []) else 0
            r["_re"] = re.compile(r["regex"], flags)
            compiled.append(r)
        except re.error:
            continue
    return compiled


def lawgate(text: str, brand: str | None = None, scope: str = "all",
            speaker: str | None = None) -> dict:
    """Mirror of dr-os lawgate.check, reading the data files instead of RULES."""
    blockers, warnings = [], []
    for rule in regex_rules(brand):
        rs = rule.get("scope", "all")
        if rs != "all" and scope != "all" and rs != scope:
            continue
        if rule.get("speaker") and speaker != rule["speaker"]:
            continue
        for m in rule["_re"].finditer(text):
            s, e = max(0, m.start() - 40), min(len(text), m.end() + 40)
            hit = {"id": rule.get("id"), "law": rule.get("law"), "match": m.group(0),
                   "excerpt": text[s:e].replace("\n", " ")}
            (blockers if rule.get("severity") == "blocker" else warnings).append(hit)
    return {"clean": not blockers and not warnings, "blockers": blockers, "warnings": warnings}


@lru_cache(maxsize=1)
def _house_laws_sections() -> dict[str, str]:
    path = settings.LAWS_DIR / "house-laws.md"
    if not path.is_file():
        return {}
    sections, current, buf = {}, None, []
    for line in path.read_text().splitlines():
        if line.startswith("## "):
            if current:
                sections[current] = "\n".join(buf).strip()
            current, buf = line.strip(), []
        else:
            buf.append(line)
    if current:
        sections[current] = "\n".join(buf).strip()
    return sections


def house_laws(stages: list[str], brand: str | None) -> str:
    """Judgment laws for the given stages plus the brand's section, as markdown."""
    sections = _house_laws_sections()
    out = []
    for stage in stages:
        header = STAGE_HEADERS.get(stage, f"## {stage}")
        body = sections.get(header)
        if body:
            out.append(f"{header}\n{body}")
    if brand:
        for header, body in sections.items():
            if header.lower().startswith("## brand-specific:") and brand.lower() in header.lower():
                out.append(f"{header}\n{body}")
    return "\n\n".join(out)


def status() -> dict:
    return {"laws_dir": str(settings.LAWS_DIR),
            "global_rules": len(_load_json(settings.LAWS_DIR / "global.json")),
            "brand_files": sorted(p.stem for p in (settings.LAWS_DIR / "examples").glob("*.json"))
            if (settings.LAWS_DIR / "examples").is_dir() else [],
            "house_law_sections": sorted(_house_laws_sections())}
