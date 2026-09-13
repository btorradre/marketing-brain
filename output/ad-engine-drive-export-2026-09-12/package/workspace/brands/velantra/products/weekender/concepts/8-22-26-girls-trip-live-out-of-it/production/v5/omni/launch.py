import os, json, base64, subprocess, pathlib, sys
ROOT="/Users/brooksorradre2/Documents/marketing brain"
KEY=[l.split("=",1)[1].strip() for l in open(os.path.join(ROOT,".env")) if l.startswith("GEMINI_API_KEY=")][0]
P=json.load(open("omni/prompts.json"))
IN=pathlib.Path("omni/in"); TMP=pathlib.Path("omni/tmp"); TMP.mkdir(exist_ok=True)
jobs={}
for slug, prompt in P.items():
    img=(IN/f"{slug}.jpg").read_bytes()
    body={"model":"models/gemini-omni-flash-preview",
          "input":[{"type":"image","data":base64.b64encode(img).decode(),"mime_type":"image/jpeg"},
                   {"type":"text","text":prompt}],
          "background":True,
          "generation_config":{"video_config":{}}}
    pf=TMP/f"{slug}.json"; pf.write_text(json.dumps(body))
    r=subprocess.run(["curl","-s","-X","POST",
        f"https://generativelanguage.googleapis.com/v1beta/interactions?key={KEY}",
        "-H","Content-Type: application/json","--data-binary",f"@{pf}"],capture_output=True,text=True)
    try:
        d=json.loads(r.stdout)
    except Exception:
        print(slug,"BAD RESPONSE",r.stdout[:300]); continue
    if "id" in d:
        jobs[slug]=d["id"]; print(slug,"->",d["id"],d.get("status"))
    else:
        print(slug,"ERROR",json.dumps(d)[:400])
    pf.unlink(missing_ok=True)
pathlib.Path("omni/jobs.json").write_text(json.dumps(jobs,indent=1))
print("launched",len(jobs),"of",len(P))
