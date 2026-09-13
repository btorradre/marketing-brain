#!/usr/bin/env python3
import json, os, sys
new = json.load(open(sys.argv[1]))
picks = json.load(open("state/picks.json")) if os.path.exists("state/picks.json") else {}
qa = json.load(open("state/qa-verdicts.json")) if os.path.exists("state/qa-verdicts.json") else {}
qa.update(new)
for sid, v in new.items():
    if not v.get("fail_all"):
        picks[sid] = v["pick"]
json.dump(picks, open("state/picks.json", "w"), indent=1)
json.dump(qa, open("state/qa-verdicts.json", "w"), indent=1)
fails = [k for k, v in qa.items() if v.get("fail_all")]
print(f"picks {len(picks)}, verdicts {len(qa)}, fail_all {fails}")
