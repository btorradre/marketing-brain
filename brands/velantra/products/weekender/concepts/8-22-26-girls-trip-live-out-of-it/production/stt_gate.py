import os, json, ssl, certifi, pathlib, urllib.request, uuid
ROOT="/Users/brooksorradre2/Documents/marketing brain"
KEY=[l.split("=",1)[1].strip() for l in open(os.path.join(ROOT,".env")) if l.startswith("ELEVENLABS_API_KEY=")][0]
CTX=ssl.create_default_context(cafile=certifi.where())

def post_multipart(url, fields, files):
    b="----"+uuid.uuid4().hex; body=b""
    for k,v in fields.items():
        body += f"--{b}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode()
    for k,(fn,data) in files.items():
        body += f"--{b}\r\nContent-Disposition: form-data; name=\"{k}\"; filename=\"{fn}\"\r\nContent-Type: audio/mpeg\r\n\r\n".encode()+data+b"\r\n"
    body += f"--{b}--\r\n".encode()
    req=urllib.request.Request(url, data=body, headers={"xi-api-key":KEY,"Content-Type":f"multipart/form-data; boundary={b}"})
    with urllib.request.urlopen(req, timeout=300, context=CTX) as r: return json.load(r)

for t in (1,2,3):
    f=pathlib.Path(f"vo/take{t}.mp3")
    d=post_multipart("https://api.elevenlabs.io/v1/speech-to-text",
        {"model_id":"scribe_v1","timestamps_granularity":"word"},
        {"file":(f.name, f.read_bytes())})
    words=[w["text"] for w in d.get("words",[]) if w.get("type")=="word"]
    txt=" ".join(words)
    pathlib.Path(f"vo/take{t}_stt.json").write_text(json.dumps(d))
    brand=[w for w in words if w.lower().startswith(("vel","vol","val","vay"))]
    print(f"--- take{t} | brand tokens: {brand}")
    print(txt)
    print()
