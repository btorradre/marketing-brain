import os, json, base64, subprocess, pathlib, sys
ROOT="/Users/brooksorradre2/Documents/marketing brain"
KEY=[l.split("=",1)[1].strip() for l in open(os.path.join(ROOT,".env")) if l.startswith("GEMINI_API_KEY=")][0]
P=json.load(open("omni/prompts.json")); jobs=json.load(open("omni/jobs.json"))
IN=pathlib.Path("omni/in"); TMP=pathlib.Path("omni/tmp"); TMP.mkdir(exist_ok=True)
for slug in sys.argv[1:]:
    img=(IN/f"{slug}.jpg").read_bytes()
    body={"model":"models/gemini-omni-flash-preview",
          "input":[{"type":"image","data":base64.b64encode(img).decode(),"mime_type":"image/jpeg"},
                   {"type":"text","text":P[slug]}],
          "background":True,"generation_config":{"video_config":{}}}
    pf=TMP/f"{slug}.json"; pf.write_text(json.dumps(body))
    r=subprocess.run(["curl","-s","-X","POST",
        f"https://generativelanguage.googleapis.com/v1beta/interactions?key={KEY}",
        "-H","Content-Type: application/json","--data-binary",f"@{pf}"],capture_output=True,text=True)
    d=json.loads(r.stdout)
    if "id" in d: jobs[slug]=d["id"]; print(slug,"->",d["id"])
    else: print(slug,"ERROR",json.dumps(d)[:300])
    pf.unlink(missing_ok=True)
pathlib.Path("omni/jobs.json").write_text(json.dumps(jobs,indent=1))
