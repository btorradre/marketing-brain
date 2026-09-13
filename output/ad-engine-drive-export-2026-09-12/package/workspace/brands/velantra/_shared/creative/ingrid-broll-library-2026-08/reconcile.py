#!/usr/bin/env python3
"""Merge a re-QA verdict file into picks, purging clips whose pick changed or now fails.

Usage: python3 reconcile.py state/reqa-cognac-1.json
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
new = json.load(open(sys.argv[1]))
picks = json.load(open("state/picks.json")) if os.path.exists("state/picks.json") else {}
qa = json.load(open("state/qa-verdicts.json")) if os.path.exists("state/qa-verdicts.json") else {}
omni = json.load(open("state/omni.json")) if os.path.exists("state/omni.json") else {}

purged, changed, newly_ok, newly_fail = [], [], [], []
for sid, v in new.items():
    old_pick = picks.get(sid)
    old_fail = qa.get(sid, {}).get("fail_all")
    qa[sid] = v
    if v.get("fail_all"):
        if old_pick:
            picks.pop(sid, None)
            newly_fail.append(sid)
    else:
        if old_fail:
            newly_ok.append(sid)
        if old_pick and old_pick != v["pick"]:
            changed.append(sid)
        picks[sid] = v["pick"]
    # purge stale clip if the pick moved or the scene now fails
    if (v.get("fail_all") and old_pick) or (old_pick and not v.get("fail_all") and old_pick != v["pick"]):
        for p in (f"clips/{sid}.mp4", f"clipqa/{sid}.jpg"):
            if os.path.exists(p):
                os.remove(p)
                purged.append(p)
        omni.pop(sid, None)

json.dump(picks, open("state/picks.json", "w"), indent=1)
json.dump(qa, open("state/qa-verdicts.json", "w"), indent=1)
json.dump(omni, open("state/omni.json", "w"), indent=1)
fails = [k for k, v in qa.items() if v.get("fail_all")]
print(f"picks {len(picks)}, verdicts {len(qa)}, fail_all now {len(fails)}: {fails}")
print(f"pick changed: {changed}")
print(f"newly ok (was fail_all): {newly_ok}")
print(f"newly fail (was pick): {newly_fail}")
print(f"purged files: {purged}")
