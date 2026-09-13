"""Creative-tracker bridge — the loop-closer.

A concept that is agreed goes to the tracker BEFORE production starts; the
asset_id that comes back belongs in the angle record's tested_assets so the
30-day verdict has somewhere to land.
"""

import re
import subprocess

from paths import CREATIVE_TRACKER


def push_concept(product: str, concept: str, angle: str, thesis: str,
                 format: str = "video", type: str = "net-new",
                 source: str = "dr-os-mcp", notes: str | None = None) -> dict:
    cmd = ["python3", str(CREATIVE_TRACKER / "push_concept.py"),
           "--product", product, "--concept", concept, "--angle", angle,
           "--thesis", thesis, "--format", format, "--type", type,
           "--source", source]
    if notes:
        cmd += ["--notes", notes]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    out = (proc.stdout + proc.stderr).strip()
    m = re.search(r"\b[A-Z]{2,4}-\d+-\d+\b", out)
    return {"ok": proc.returncode == 0,
            "asset_id": m.group(0) if m else None,
            "output": out[-2000:],
            "next": "Write this asset_id into the angle record's tested_assets (dr_read_artifact / dr_save_artifact on angle-bank)."}
