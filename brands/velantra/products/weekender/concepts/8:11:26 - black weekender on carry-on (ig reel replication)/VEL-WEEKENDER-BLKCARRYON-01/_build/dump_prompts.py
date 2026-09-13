#!/usr/bin/env python3
"""Dump every scene prompt + its reference list to prompts.json for the Higgsfield MCP.

kie is dry (114cr, auto top-up broken as of 2026-08-09); Higgsfield Ultra is the working
GPT Image 2 path. The MCP is tool-driven rather than scriptable, so this just emits the
payload the batch calls need.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from scenes import SCENES, REFS, build_prompt

VAULT = "/Users/brooksorradre2/Documents/marketing brain"
WK = os.path.join(VAULT, "brands/velantra/products/weekender")
ROOTS = {
    "black":   os.path.join(WK, "product-images/black/original-iphone-photos"),
    "lc":      os.path.join(WK, "product-references/real-product-2026-08-08"),
    "creator": os.path.join(WK, "concepts/8:07:26 - mens angle replication/VEL-WEEKENDER-MENS-01"),
    "anchor":  HERE,   # the approved S03 pick, copied in as S03-anchor.png
}

ref_paths = {k: os.path.join(ROOTS[root], fn) for k, (root, fn) in REFS.items()}
missing = {k: p for k, p in ref_paths.items() if not os.path.exists(p)}
if missing:
    print("MISSING REFS:", json.dumps(missing, indent=2))
    sys.exit(1)

out = {
    "ref_paths": ref_paths,
    "scenes": [
        {"id": s["id"], "refs": s["refs"], "target": s["target"],
         "state": s["state"], "prompt": build_prompt(s)}
        for s in SCENES
    ],
}
dest = os.path.join(HERE, "prompts.json")
json.dump(out, open(dest, "w"), indent=2)
print(f"wrote {dest}: {len(out['scenes'])} scenes, {len(ref_paths)} refs")
for k, p in ref_paths.items():
    print(f"  {k:10s} {os.path.getsize(p)//1024:>5d} kB  {p}")
