#!/usr/bin/env python3
"""Omni's input-block is intermittent, so bounded-retry the shots that keep tripping it."""
import json, pathlib, subprocess, sys, time
HERE=pathlib.Path(__file__).parent
CLIPS=HERE/"ad4v2/clips"; STATE=HERE/"ad4v2/omni.json"
MAX=5
for sid in sys.argv[1:]:
    for attempt in range(1, MAX+1):
        if (CLIPS/f"{sid}.mp4").exists():
            print(f"{sid}: already have it"); break
        d=json.loads(STATE.read_text()); d.pop(sid, None); STATE.write_text(json.dumps(d, indent=2))
        r=subprocess.run(["python3","ad4v2_omni.py",sid],capture_output=True,text=True,cwd=str(HERE))
        ok=(CLIPS/f"{sid}.mp4").exists()
        print(f"{sid} attempt {attempt}: {'OK' if ok else 'blocked'}", flush=True)
        if ok: break
        time.sleep(15)
    else:
        print(f"{sid}: blocked {MAX}/{MAX}, keeping the keyframe push-in")
