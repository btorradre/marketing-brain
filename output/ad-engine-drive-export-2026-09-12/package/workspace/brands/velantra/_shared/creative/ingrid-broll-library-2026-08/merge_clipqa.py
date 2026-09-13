#!/usr/bin/env python3
import json, os, sys
new = json.load(open(sys.argv[1]))
vf = "state/clip-verdicts.json"
verd = json.load(open(vf)) if os.path.exists(vf) else {}
verd.update(new)
json.dump(verd, open(vf, "w"), indent=1)
omni_f = "state/omni.json"
omni = json.load(open(omni_f)) if os.path.exists(omni_f) else {}
fails = [k for k, v in new.items() if v.get("verdict") == "FAIL"]
for sid in fails:
    p = f"clips/{sid}.mp4"
    if os.path.exists(p):
        os.remove(p)
    omni.pop(sid, None)
    p2 = f"clipqa/{sid}.jpg"
    if os.path.exists(p2):
        os.remove(p2)
json.dump(omni, open(omni_f, "w"), indent=1)
npass = sum(1 for v in verd.values() if v.get("verdict") == "PASS")
print(f"verdicts {len(verd)}, pass {npass}, purged for re-roll: {fails}")
