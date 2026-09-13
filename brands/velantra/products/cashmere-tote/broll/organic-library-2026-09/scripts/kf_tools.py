#!/usr/bin/env python3
"""Keyframe helpers for the Higgsfield GPT Image 2 path (generation itself runs through the MCP connector).
  python3 kf_tools.py batch ID [ID ...]         -> prints the generate_image_batch requests JSON (index = manifest index)
  python3 kf_tools.py save results.json          -> downloads {index/job_id: url} into keyframes/<id>/vN.png
  python3 kf_tools.py sheet ID [ID ...]          -> contact sheet of variants for eyeballing
  python3 kf_tools.py missing                    -> ids with no keyframe yet"""
import json, os, subprocess, sys
from common import *
from manifest import CLIPS as MAN, build_prompt, refs_for
IDX = {c["id"]: i for i, c in enumerate(MAN)}
def cmd_batch(ids):
    reqs = []
    for cid in ids:
        c = MAN[IDX[cid]]
        reqs.append({"index": IDX[cid], "params": {"model": "gpt_image_2", "aspect_ratio": "9:16", "resolution": "1k", "quality": "high",
                     "medias": [{"value": HF_IDS[r], "role": "image"} for r in refs_for(c)], "prompt": build_prompt(c)}})
    print(json.dumps(reqs))
def cmd_save(path):
    res = json.load(open(path)); log = load(os.path.join(STATE, "kf_jobs.json"), {})
    done_jobs = {v.get("job") for v in log.values()}
    for r in res:
        if r.get("job_id") in done_jobs: print("skip (already saved)", r["index"]); continue
        cid = MAN[r["index"]]["id"]; d = os.path.join(KF, cid); os.makedirs(d, exist_ok=True)
        n = len([f for f in os.listdir(d) if f.endswith(".png")]) + 1
        out = os.path.join(d, f"v{n}.png")
        subprocess.run(["curl", "-s", "-L", "-o", out, r["url"]], check=True)
        log[f"{cid}/v{n}"] = {"job": r.get("job_id"), "url": r["url"]}; print(cid, f"v{n}", os.path.getsize(out))
    save(os.path.join(STATE, "kf_jobs.json"), log)
def cmd_sheet(ids):
    from PIL import Image, ImageDraw
    tiles = []
    for cid in ids:
        d = os.path.join(KF, cid)
        for v in sorted(os.listdir(d)) if os.path.isdir(d) else []:
            if v.endswith(".png"):
                im = Image.open(os.path.join(d, v)).convert("RGB").resize((360, 640)); ImageDraw.Draw(im).text((8, 8), f"{cid} {v}", fill="yellow"); tiles.append(im)
    cols = 4; rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 360, rows * 640), "black")
    for i, t in enumerate(tiles): sheet.paste(t, ((i % cols) * 360, (i // cols) * 640))
    out = os.path.join(ROOT, "probes", "sheet_" + ids[0] + ".jpg"); sheet.save(out, quality=85); print(out)
def cmd_missing():
    print(" ".join(c["id"] for c in MAN if not os.path.isdir(os.path.join(KF, c["id"])) or not os.listdir(os.path.join(KF, c["id"]))))
if __name__ == "__main__":
    c = sys.argv[1]
    {"batch": lambda: cmd_batch(sys.argv[2:]), "save": lambda: cmd_save(sys.argv[2]), "sheet": lambda: cmd_sheet(sys.argv[2:]), "missing": cmd_missing}.get(c, lambda: None)()

def cmd_scenes(ids):
    """Compact view: index | id | colorway | open | ref media ids | substituted scene (fixed blocks omitted)."""
    from manifest import CREATORS
    for cid in ids:
        c = MAN[IDX[cid]]; p = build_prompt(c); scene = p.split("\n\n")[1]
        print(f"{IDX[cid]}|{cid}|{c['colorway']}|{'OPEN' if c['open_bag'] else 'closed'}|{','.join(HF_IDS[r] for r in refs_for(c))}|{scene}")
if __name__ == "__main__" and sys.argv[1] == "scenes": cmd_scenes(sys.argv[2:])
