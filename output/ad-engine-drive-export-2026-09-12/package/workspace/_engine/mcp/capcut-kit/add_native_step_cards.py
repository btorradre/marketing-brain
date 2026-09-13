#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "pyobjc-framework-ApplicationServices",
#   "pyobjc-framework-Quartz",
# ]
# ///
"""One-off: add 3 native CapCut text title cards (STEP ONE/TWO/THREE) with a
real background box, reusing capcut-bridge.py's own template + edit_draft
machinery so the quit/write/relaunch safety dance stays identical to the CLI."""
import importlib.util
import json
import sys
from pathlib import Path

BRIDGE_PATH = Path(__file__).resolve().parent / "capcut-bridge.py"
spec = importlib.util.spec_from_file_location("capcut_bridge", BRIDGE_PATH)
cb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cb)

DRAFT = "Example Clip - Cut"
CARDS = [
    (4.26, "STEP ONE"),
    (15.70, "STEP TWO"),
    (34.41, "STEP THREE"),
]
DURATION = 1.8

tm_path = cb.TEMPLATES / "text-material.json"
seg_path = cb.TEMPLATES / "text-segment.json"
anim_path = cb.TEMPLATES / "text-ref-material_animations.json"


def mutate(d, folder):
    track = next((t for t in d["tracks"] if t["type"] == "text"), None)
    if track is None:
        track = {"id": cb.uid(), "type": "text", "segments": [], "flag": 1,
                  "attribute": 0, "name": "", "is_default_name": True}
        d["tracks"].append(track)

    for at, text in CARDS:
        tm = json.loads(tm_path.read_text())
        content = json.loads(tm["content"])
        content["text"] = text
        for style in content.get("styles", []):
            style["range"] = [0, len(text)]
        tm["id"] = cb.uid()
        tm["content"] = json.dumps(content, ensure_ascii=False)

        # native background box (CapCut's own text-background feature)
        tm["background_color"] = "#0A0E14"
        tm["background_style"] = 1
        tm["background_alpha"] = 0.92
        tm["background_round_radius"] = 0.12
        tm["background_width"] = 0.32
        tm["background_height"] = 0.24
        tm["background_horizontal_offset"] = 0.0
        tm["background_vertical_offset"] = 0.0
        d["materials"]["texts"].append(tm)

        anim = json.loads(anim_path.read_text())
        anim["id"] = cb.uid()
        d["materials"]["material_animations"].append(anim)

        seg = json.loads(seg_path.read_text())
        seg["id"] = cb.uid()
        seg["material_id"] = tm["id"]
        seg["extra_material_refs"] = [anim["id"]]
        seg["source_timerange"] = {"start": 0, "duration": round(DURATION * 1e6)}
        seg["target_timerange"] = {"start": round(at * 1e6),
                                    "duration": round(DURATION * 1e6)}
        # dead-center, bigger than the template's default lower-third size
        seg["clip"]["scale"] = {"x": 1.35, "y": 1.35}
        seg["clip"]["transform"] = {"x": 0.0, "y": 0.0}
        track["segments"].append(seg)
        print(f"native text: {text!r} at {at:.2f}s for {DURATION:.2f}s (with background)")


cb.edit_draft(DRAFT, mutate)
