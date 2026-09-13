"""Playbooks + brand context — the judgment layer, served as data.

The DR OS skills are SOPs meant to be executed by whatever model is driving
this server (Claude locally, or an external agent over MCP). This module
serves them live from disk so the skills stay the single source of truth —
nothing is copied into the server.
"""

import time

from paths import BRANDS, DR_OS_SKILL, LAWS, SKILL_ROOTS, find_skill

MAX_CHARS = 60_000

# step name -> (candidate skill dirs tried in order) or an explicit file path
_MODULES = DR_OS_SKILL / "modules"

PLAYBOOKS: dict[str, dict] = {
    "router":            {"skills": ["direct-response-os"], "role": "The DR OS router — which skill to run, in what order, cold start vs warm loop."},
    "laws":              {"file": _MODULES / "laws.md", "role": "The twelve laws. Load before writing ANY copy, angle, or brief."},
    "house-laws":        {"file": LAWS / "house-laws.md", "role": "Every judgment law Brooks has ruled, by pipeline stage and brand. Migrated from memory 2026-09-03. Load the sections for the stages you touch."},
    "angle-schema":      {"file": _MODULES / "angle-schema.md", "role": "The one record format the whole system shares."},
    "artifact-contract": {"file": _MODULES / "artifacts.md", "role": "Where every artifact lives and who reads what."},
    "voc-mining":        {"skills": ["dr-voc-mining"], "role": "Raw reviews/Reddit/comments -> voc-index.md."},
    "survey-designer":   {"skills": ["dr-survey-designer"], "role": "Design the post-purchase survey instrument."},
    "market-intel":      {"skills": ["dr-market-intel"], "role": "Competitor scan / winner documentation -> market-gaps.md, winners/."},
    "angle-bank":        {"skills": ["dr-angle-bank"], "role": "Merge research into the durable angle bank."},
    "awareness-audit":   {"skills": ["dr-awareness-audit"], "role": "Which awareness level the account is starved at."},
    "hook-lab":          {"skills": ["dr-hook-lab"], "role": "Hooks for one angle record."},
    "ugc-brief":         {"skills": ["dr-ugc-brief"], "role": "Creator-facing brief from one angle + hooks."},
    "funnel-strategy":   {"skills": ["dr-funnel-strategy"], "role": "Architecture + 90-day roadmap."},
    "strategize":        {"skills": ["strategize-ad-adaptation"], "role": "Watched-reference manifest -> scene-by-scene adaptation plan (the strategist layer)."},
    "brief-board":       {"skills": ["cutroom", "brief-board"], "role": "Turn beats + frames into a visual Cutroom storyboard spec for the editor."},
    "cutroom":           {"skills": ["cutroom", "brief-board"], "role": "Alias of brief-board — Cutroom is the internal whiteboard's current name."},
    "editor-brief":      {"skills": ["video-editor-brief"], "role": "Script + scene assets -> written editor brief with timeline."},
    "long-form-copy":    {"skills": ["long-form-copy"], "role": "Laws for long-form / spoken copy, incl. the script naturalizer."},
    "ad-watcher":        {"skills": ["ad-watcher"], "role": "The psychological teardown layer applied on top of a watch manifest."},
}


def list_playbooks() -> dict:
    steps = {}
    for name, entry in PLAYBOOKS.items():
        path = _resolve(entry)
        steps[name] = {"role": entry["role"], "available": path is not None}
    all_skills = sorted({p.name for root in SKILL_ROOTS if root.is_dir()
                         for p in root.iterdir() if (p / "SKILL.md").is_file()})
    return {"pipeline_steps": steps,
            "note": "dr_get_playbook also accepts any raw skill name below (e.g. a product-truth skill like 'velantra-weekender').",
            "all_skills": all_skills}


def get_playbook(name: str) -> dict:
    entry = PLAYBOOKS.get(name)
    path = _resolve(entry) if entry else find_skill(name)
    if path is None:
        return {"error": f"no playbook or skill named '{name}'",
                "known_steps": sorted(PLAYBOOKS)}
    content = path.read_text(errors="replace")
    truncated = len(content) > MAX_CHARS
    return {"name": name, "path": str(path),
            "content": content[:MAX_CHARS],
            "truncated": truncated}


def _resolve(entry: dict | None):
    if not entry:
        return None
    if "file" in entry:
        return entry["file"] if entry["file"].is_file() else None
    for skill in entry.get("skills", []):
        p = find_skill(skill)
        if p:
            return p
    return None


# ---------------------------------------------------------------------------
# Brand context
# ---------------------------------------------------------------------------

def _read_capped(path, cap=20_000):
    if not path.is_file():
        return None
    text = path.read_text(errors="replace")
    return text[:cap] + ("\n\n[TRUNCATED — read the file for the rest]" if len(text) > cap else "")


def load_brand(brand: str) -> dict:
    brand_dir = BRANDS / brand
    if not brand_dir.is_dir():
        available = sorted(p.name for p in BRANDS.iterdir() if p.is_dir() and not p.name.startswith("_"))
        return {"error": f"unknown brand '{brand}'", "available": available}

    dr_os = brand_dir / "research" / "dr-os"
    inventory = []
    if dr_os.is_dir():
        for p in sorted(dr_os.rglob("*.md")):
            st = p.stat()
            inventory.append({"path": str(p.relative_to(brand_dir)),
                              "size": st.st_size,
                              "updated": time.strftime("%Y-%m-%d", time.localtime(st.st_mtime))})

    product_truth = sorted({p.name for root in SKILL_ROOTS if root.is_dir()
                            for p in root.iterdir()
                            if (p / "SKILL.md").is_file()
                            and (p.name == brand or p.name.startswith(brand + "-"))})

    return {
        "brand": brand,
        "brand_dir": str(brand_dir),
        "brief": _read_capped(brand_dir / "00-brief.md"),
        "house_laws": _read_capped(brand_dir / "ops" / "claude-project-instructions.md"),
        "global_laws": _read_capped(_MODULES / "laws.md"),
        "house_laws_data": _read_capped(LAWS / "house-laws.md", cap=40_000),
        "house_laws_data_note": "Judgment laws as data, sectioned by stage (## Research and strategy ... ## Brand-specific: <brand>). Authoritative over older skill text where they conflict.",
        "angle_bank": _read_capped(dr_os / "angle-bank.md", cap=25_000),
        "dr_os_artifacts": inventory,
        "product_truth_skills": product_truth,
        "product_truth_note": ("Load the relevant product-truth skill via dr_get_playbook(<skill name>) "
                               "BEFORE writing any adaptation instruction, script, or prompt that shows the product. "
                               "Identity/mechanism blocks in those skills are verbatim and mandatory."),
        "top_level": sorted(p.name for p in brand_dir.iterdir() if not p.name.startswith(".")),
    }
