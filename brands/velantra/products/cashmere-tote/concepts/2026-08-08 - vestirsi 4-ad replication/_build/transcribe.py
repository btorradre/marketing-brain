import json,os,pathlib,subprocess,time,urllib.request,certifi
ROOT=pathlib.Path("/Users/brooksorradre2/Documents/marketing brain")
for l in (ROOT/".env").read_text().splitlines():
    if "=" in l and not l.strip().startswith("#"):
        k,v=l.split("=",1); os.environ.setdefault(k.strip(),v.strip().strip('"').strip("'"))
os.environ["SSL_CERT_FILE"]=certifi.where()
K=os.environ["GEMINI_API_KEY"]; B="https://generativelanguage.googleapis.com"; M="gemini-3.1-pro-preview"
import sys; src=pathlib.Path(sys.argv[1])
d=src.read_bytes()
r=urllib.request.Request(f"{B}/upload/v1beta/files?key={K}",data=json.dumps({"file":{"display_name":src.name}}).encode(),
  headers={"X-Goog-Upload-Protocol":"resumable","X-Goog-Upload-Command":"start","X-Goog-Upload-Header-Content-Length":str(len(d)),
  "X-Goog-Upload-Header-Content-Type":"video/mp4","Content-Type":"application/json"},method="POST")
u=urllib.request.urlopen(r).headers["X-Goog-Upload-URL"]
f=json.loads(urllib.request.urlopen(urllib.request.Request(u,data=d,
  headers={"Content-Length":str(len(d)),"X-Goog-Upload-Offset":"0","X-Goog-Upload-Command":"upload, finalize"},method="POST")).read())["file"]
while f.get("state")=="PROCESSING":
    time.sleep(3); f=json.loads(urllib.request.urlopen(f"{B}/v1beta/{f['name']}?key={K}").read())
P="""Answer only these, one per line:
SPEAKERS: how many distinct voices, and is any of them off camera.
TRANSCRIPT: the exact words spoken, verbatim.
LIP SYNC: do her lips match the words. yes / slightly off / clearly off.
VOICE: gender, rough age, accent, and does it sound like a real person talking to a friend or like text to speech.
OTHER AUDIO: any music, narration, or a second voice. yes/no with detail.
DELIVERY: does energy hold to the final word or fade."""
body={"contents":[{"parts":[{"file_data":{"mime_type":f["mimeType"],"file_uri":f["uri"]}},{"text":P}]}],
      "generationConfig":{"temperature":0.1,"maxOutputTokens":1000}}
r=json.loads(urllib.request.urlopen(urllib.request.Request(f"{B}/v1beta/models/{M}:generateContent?key={K}",
  data=json.dumps(body).encode(),headers={"Content-Type":"application/json"},method="POST"),timeout=600).read())
print("".join(x.get("text","") for x in r["candidates"][0]["content"]["parts"]))
