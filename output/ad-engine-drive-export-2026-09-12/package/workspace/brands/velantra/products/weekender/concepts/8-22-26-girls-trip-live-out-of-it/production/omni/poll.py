import os, json, base64, subprocess, pathlib
ROOT="/Users/brooksorradre2/Documents/marketing brain"
KEY=[l.split("=",1)[1].strip() for l in open(os.path.join(ROOT,".env")) if l.startswith("GEMINI_API_KEY=")][0]
jobs=json.load(open("omni/jobs.json"))
OUT=pathlib.Path("omni/out")
done=[]
for slug,jid in jobs.items():
    if (OUT/f"{slug}.mp4").exists(): done.append(slug); print(slug,"already saved"); continue
    r=subprocess.run(["curl","-s",f"https://generativelanguage.googleapis.com/v1beta/interactions/{jid}?key={KEY}"],capture_output=True,text=True)
    try: d=json.loads(r.stdout)
    except Exception: print(slug,"BAD",r.stdout[:200]); continue
    st=d.get("status")
    if st!="completed": print(slug,st, (d.get("error") or {}).get("message","")); continue
    vid=None
    for step in d.get("steps",[]):
        for c in step.get("content",[]) or []:
            if c.get("type")=="video": vid=c.get("data")
    if not vid: print(slug,"completed but no video part"); continue
    (OUT/f"{slug}.mp4").write_bytes(base64.b64decode(vid)); done.append(slug)
    print(slug,"SAVED")
print(f"{len(done)}/{len(jobs)} done")
