import base64, json, os, pathlib, subprocess, time, urllib.request, certifi, ssl
HERE=pathlib.Path(__file__).parent; OUT=HERE/"vo"
ROOT=pathlib.Path("/Users/brooksorradre2/Documents/marketing brain")
for l in (ROOT/".env").read_text().splitlines():
    if "=" in l and not l.strip().startswith("#"):
        k,v=l.split("=",1); os.environ.setdefault(k.strip(),v.strip().strip('"').strip("'"))
os.environ["SSL_CERT_FILE"]=certifi.where()
K=os.environ["GEMINI_API_KEY"]; B="https://generativelanguage.googleapis.com"; M="gemini-3.1-pro-preview"
P="""This is a voiceover for a handbag ad, read by a woman in her early forties talking like a friend recommending something she found.

Score it and be strict. Output only these lines:

NATURALNESS /10 - does it sound like a person talking or like text to speech being read. Name the specific tell if there is one.
PRONUNCIATION - transcribe exactly how she says "Colette" and "Loro Piana" phonetically. Correct is "co-LET" and "LOR-oh pee-AH-nah".
PACE - too fast, right, or too slow. Any place she rushes or drags.
ENERGY - does energy hold to the final word or fade in the back half. Name the timestamp if it fades.
DEAD AIR - any unnatural gaps or clipped words, with timestamps.
ANNOUNCER - does she ever slip into advertisement voice. Where.
VERDICT - one sentence, would you ship it."""
def up(p):
    d=p.read_bytes()
    req=urllib.request.Request(f"{B}/upload/v1beta/files?key={K}",data=json.dumps({"file":{"display_name":p.name}}).encode(),
      headers={"X-Goog-Upload-Protocol":"resumable","X-Goog-Upload-Command":"start","X-Goog-Upload-Header-Content-Length":str(len(d)),
               "X-Goog-Upload-Header-Content-Type":"audio/mpeg","Content-Type":"application/json"},method="POST")
    u=urllib.request.urlopen(req).headers["X-Goog-Upload-URL"]
    r2=urllib.request.Request(u,data=d,headers={"Content-Length":str(len(d)),"X-Goog-Upload-Offset":"0","X-Goog-Upload-Command":"upload, finalize"},method="POST")
    f=json.loads(urllib.request.urlopen(r2).read())["file"]
    while f.get("state")=="PROCESSING":
        time.sleep(2); f=json.loads(urllib.request.urlopen(f"{B}/v1beta/{f['name']}?key={K}").read())
    return f
for tag in ("D","E","F"):
    p=OUT/f"cand-{tag}.mp3"
    f=up(p)
    body={"contents":[{"parts":[{"file_data":{"mime_type":f["mimeType"],"file_uri":f["uri"]}},{"text":P}]}],
          "generationConfig":{"temperature":0.2,"maxOutputTokens":4000}}
    req=urllib.request.Request(f"{B}/v1beta/models/{M}:generateContent?key={K}",data=json.dumps(body).encode(),
        headers={"Content-Type":"application/json"},method="POST")
    r=json.loads(urllib.request.urlopen(req,timeout=600).read())
    print(f"═══════ CANDIDATE {tag}")
    print("".join(x.get("text","") for x in r["candidates"][0]["content"]["parts"]))
