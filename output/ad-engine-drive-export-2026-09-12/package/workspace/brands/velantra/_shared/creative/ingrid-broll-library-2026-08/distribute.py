#!/usr/bin/env python3
"""Copy picked keyframes + finished clips into the Ingrid broll/ library folder."""
import json, os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from pipeline import SCENES, load

VAULT = os.path.expanduser("~/Documents/marketing brain")
DEST = os.path.join(VAULT, "brands/velantra/products/ingrid/broll/library-2026-08")
picks = load(os.path.join(HERE, "state/picks.json"), {})
copied = {"clips": 0, "stills": 0}
os.makedirs(os.path.join(DEST, "clips"), exist_ok=True)
os.makedirs(os.path.join(DEST, "stills"), exist_ok=True)
for s in SCENES:
    sid = s[0]
    clip = os.path.join(HERE, "clips", f"{sid}.mp4")
    still = os.path.join(HERE, "keyframes", sid, f"{picks.get(sid, 'v1')}.png")
    if os.path.exists(clip) and os.path.getsize(clip) > 100_000:
        shutil.copy2(clip, os.path.join(DEST, "clips", f"VEL-{sid}.mp4"))
        copied["clips"] += 1
    if os.path.exists(still):
        shutil.copy2(still, os.path.join(DEST, "stills", f"VEL-{sid}.png"))
        copied["stills"] += 1
print(copied)
