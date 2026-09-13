#!/usr/bin/env python3
"""pick.py ID vN ["note"]  -> state/picks.json"""
import sys, os
from common import *
from manifest import CLIPS as MAN
picks = load(os.path.join(STATE, "picks.json"), {})
cid, v = sys.argv[1], sys.argv[2]; note = sys.argv[3] if len(sys.argv) > 3 else ""
c = next(x for x in MAN if x["id"] == cid)
picks[cid] = {"kf": f"keyframes/{cid}/{v}.png", "motion": c["motion"], "engine": c["engine"], "note": note}
save(os.path.join(STATE, "picks.json"), picks); print(cid, v, "picked", f"({len(picks)} total)")
