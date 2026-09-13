import json,os,pathlib,time,urllib.request,certifi
HERE=pathlib.Path(__file__).parent; OUT=HERE/"vo"
ROOT=pathlib.Path("/Users/brooksorradre2/Documents/marketing brain")
for l in (ROOT/".env").read_text().splitlines():
    if "=" in l and not l.strip().startswith("#"):
        k,v=l.split("=",1); os.environ.setdefault(k.strip(),v.strip().strip('"').strip("'"))
os.environ["SSL_CERT_FILE"]=certifi.where()
K=os.environ["GEMINI_API_KEY"]; B="https://generativelanguage.googleapis.com"; M="gemini-3.1-pro-preview"
def up(p):
    d=p.read_bytes()
    r=urllib.request.Request(f"{B}/upload/v1beta/files?key={K}",data=json.dumps({"file":{"display_name":p.name}}).encode(),
      headers={"X-Goog-Upload-Protocol":"resumable","X-Goog-Upload-Command":"start","X-Goog-Upload-Header-Content-Length":str(len(d)),
      "X-Goog-Upload-Header-Content-Type":"audio/mpeg","Content-Type":"application/json"},method="POST")
    u=urllib.request.urlopen(r).headers["X-Goog-Upload-URL"]
    f=json.loads(urllib.request.urlopen(urllib.request.Request(u,data=d,
      headers={"Content-Length":str(len(d)),"X-Goog-Upload-Offset":"0","X-Goog-Upload-Command":"upload, finalize"},method="POST")).read())["file"]
    while f.get("state")=="PROCESSING":
        time.sleep(2); f=json.loads(urllib.request.urlopen(f"{B}/v1beta/{f['name']}?key={K}").read())
    return f
P=("This audio clip is about one and a half seconds long and contains one or two spoken words. "
   "Write ONLY what you hear, syllable by syllable, with the stressed syllable in CAPITALS. "
   "If you cannot hear any speech, write exactly: NO SPEECH. Do not add any other text.")
for name in ("slice-colette-A","slice-lp-A","slice-colette-D","slice-lp-D"):
    f=up(OUT/f"{name}.mp3")
    body={"contents":[{"parts":[{"file_data":{"mime_type":f["mimeType"],"file_uri":f["uri"]}},{"text":P}]}],
          "generationConfig":{"temperature":0.0,"maxOutputTokens":200}}
    r=json.loads(urllib.request.urlopen(urllib.request.Request(f"{B}/v1beta/models/{M}:generateContent?key={K}",
      data=json.dumps(body).encode(),headers={"Content-Type":"application/json"},method="POST"),timeout=300).read())
    t="".join(x.get("text","") for x in r["candidates"][0]["content"]["parts"]).strip()
    print(f"{name:22s} -> {t}")
