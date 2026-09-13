#!/usr/bin/env python3
"""review.py ID PASS|FAIL START-END ["note"]  -> state/human_review.json (drift-strip review at 0.5/3/6/9.5s + full-res checks)"""
import sys, os
from common import *
r = load(os.path.join(STATE, "human_review.json"), {})
cid, verdict, win = sys.argv[1:4]; note = sys.argv[4] if len(sys.argv) > 4 else ""
r[cid] = {"verdict": verdict, "usable_window": win, "note": note}
save(os.path.join(STATE, "human_review.json"), r); print(cid, verdict, win, f"({sum(1 for v in r.values() if v['verdict']=='PASS')} passed)")
