"""Shared path resolution for the dr-os MCP server."""

from pathlib import Path

# .../marketing brain/_engine/mcp/dr-os/paths.py -> repo root
ROOT = Path(__file__).resolve().parents[3]

SKILL_ROOTS = [
    ROOT / ".claude" / "skills",          # project skills (DR OS lives here)
    Path.home() / ".claude" / "skills",   # user skills (product truth, ad-watcher)
]

DR_OS_SKILL = ROOT / ".claude" / "skills" / "direct-response-os"
BRANDS = ROOT / "brands"
# Renamed briefboard -> cutroom on 2026-08-17; resolve whichever exists.
BRIEFBOARD = next((p for p in (ROOT / "cutroom", ROOT / "briefboard") if p.is_dir()),
                  ROOT / "cutroom")
AD_ENGINE = ROOT / "_engine" / "mcp" / "ad-engine"
CREATIVE_TRACKER = ROOT / "_engine" / "creative-tracker"
# laws-as-data (symlink to adengine packages/laws): global.json, examples/<brand>.json, house-laws.md
LAWS = ROOT / "_engine" / "laws"


def find_skill(name: str) -> Path | None:
    """Locate <name>/SKILL.md across both skill roots."""
    for root in SKILL_ROOTS:
        p = root / name / "SKILL.md"
        if p.is_file():
            return p
    return None
