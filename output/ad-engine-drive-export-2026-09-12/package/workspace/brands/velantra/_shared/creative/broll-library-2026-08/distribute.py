#!/usr/bin/env python3
"""Copy picked keyframes + finished clips into each product's broll/ library folder."""
import json, os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from pipeline import SCENES, load

VAULT = os.path.expanduser("~/Documents/marketing brain")
DEST = {
    "colette": os.path.join(VAULT, "brands/velantra/products/cashmere-tote/broll/library-2026-08"),
    "margot": os.path.join(VAULT, "brands/velantra/products/margot/broll/library-2026-08"),
}
picks = load(os.path.join(HERE, "state/picks.json"), {})
copied = {"clips": 0, "stills": 0}
for s in SCENES:
    sid, product = s[0], s[1]
    dests = [DEST["colette"], DEST["margot"]] if product == "duo" else [DEST[product]]
    clip = os.path.join(HERE, "clips", f"{sid}.mp4")
    still = os.path.join(HERE, "keyframes", sid, f"{picks.get(sid, 'v1')}.png")
    for droot in dests:
        os.makedirs(os.path.join(droot, "clips"), exist_ok=True)
        os.makedirs(os.path.join(droot, "stills"), exist_ok=True)
        if os.path.exists(clip) and os.path.getsize(clip) > 100_000:
            shutil.copy2(clip, os.path.join(droot, "clips", f"VEL-{sid}.mp4"))
            copied["clips"] += 1
        if os.path.exists(still):
            shutil.copy2(still, os.path.join(droot, "stills", f"VEL-{sid}.png"))
            copied["stills"] += 1
print(copied)
