"""Agent fleet inventory — every skill/pipeline Brooks has built.

Scans project-level (.claude/skills in the vault) and user-level
(~/.claude/skills) skill directories, pulling name + description from each
SKILL.md frontmatter.
"""
import os, re
from .common import VAULT

SKILL_DIRS = [
    ("project", os.path.join(VAULT, ".claude", "skills")),
    ("user", os.path.expanduser("~/.claude/skills")),
]


def _parse_skill_md(path):
    try:
        text = open(path, errors="replace").read(6000)
    except Exception:
        return None
    desc = ""
    m = re.search(r"^description:\s*[\"']?(.+?)[\"']?\s*$", text, re.M)
    if m:
        desc = m.group(1)
    else:
        m = re.search(r"^---.*?^---\s*(.+?)$", text, re.S | re.M)
        if m:
            desc = m.group(1).strip().splitlines()[0]
    return desc.strip()


def _category(name):
    n = name.lower()
    if n.startswith("velantra") or "strato" in n:
        return "Velantra"
    if "motilli" in n:
        return "Motilli"
    if "lunessa" in n:
        return "Lunessa"
    if n.startswith("n8n") or n.startswith("hyperframes") or n.startswith("higgsfield"):
        return "Infrastructure"
    if any(k in n for k in ("video", "ugc", "seedance", "kling", "claymation", "animated", "broll", "b-roll", "replicator", "pov", "vsl", "watch", "fashion", "omni")):
        return "Video/Creative"
    if any(k in n for k in ("copy", "advertorial", "listicle", "landing", "sales-page", "pdp", "cro", "ad-", "creative", "native", "swipe", "concept", "brief")):
        return "Copy/Funnel"
    return "Other"


def collect():
    skills = []
    for scope, d in SKILL_DIRS:
        if not os.path.isdir(d):
            continue
        for name in sorted(os.listdir(d)):
            skill_md = os.path.join(d, name, "SKILL.md")
            if not os.path.isfile(skill_md):
                continue
            desc = _parse_skill_md(skill_md) or ""
            skills.append({
                "name": name,
                "scope": scope,
                "category": _category(name),
                "description": (desc[:180] + "…") if len(desc) > 180 else desc,
            })

    by_cat = {}
    for s in skills:
        by_cat[s["category"]] = by_cat.get(s["category"], 0) + 1
    return {
        "total": len(skills),
        "by_category": dict(sorted(by_cat.items(), key=lambda kv: -kv[1])),
        "skills": skills,
    }
