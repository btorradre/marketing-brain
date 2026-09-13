import os, json, ssl, certifi, pathlib, urllib.request, uuid
ROOT="/Users/brooksorradre2/Documents/marketing brain"
KEY=[l.split("=",1)[1].strip() for l in open(os.path.join(ROOT,".env")) if l.startswith("ELEVENLABS_API_KEY=")][0]
CTX=ssl.create_default_context(cafile=certifi.where())
f=pathlib.Path("/var/folders/6s/1n0789r93311dlllbrmg9v980000gq/T/watch-rd4omnpc/audio.mp3")
b="----"+uuid.uuid4().hex; body=b""
for k,v in {"model_id":"scribe_v1","timestamps_granularity":"word","diarize":"true"}.items():
    body += f"--{b}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode()
body += f"--{b}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{f.name}\"\r\nContent-Type: audio/mpeg\r\n\r\n".encode()+f.read_bytes()+b"\r\n"
body += f"--{b}--\r\n".encode()
req=urllib.request.Request("https://api.elevenlabs.io/v1/speech-to-text", data=body,
    headers={"xi-api-key":KEY,"Content-Type":f"multipart/form-data; boundary={b}"})
with urllib.request.urlopen(req, timeout=600, context=CTX) as r: d=json.load(r)
pathlib.Path("loom_stt.json").write_text(json.dumps(d))
ws=[w for w in d.get("words",[]) if w.get("type")=="word"]
line=[]; start=None; out=[]
for w in ws:
    if start is None: start=w["start"]
    line.append(w["text"])
    if w["end"]-start > 7:
        out.append(f"[{int(start//60):02d}:{int(start%60):02d}] "+" ".join(line)); line=[]; start=None
if line: out.append(f"[{int(start//60):02d}:{int(start%60):02d}] "+" ".join(line))
print("\n".join(out))
