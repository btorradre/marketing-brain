import base64, json, os, pathlib, subprocess
HERE=pathlib.Path(__file__).parent; OUT=HERE/"vo"; OUT.mkdir(exist_ok=True)
ROOT=pathlib.Path("/Users/brooksorradre2/Documents/marketing brain")
for l in (ROOT/".env").read_text().splitlines():
    if "=" in l and not l.strip().startswith("#"):
        k,v=l.split("=",1); os.environ.setdefault(k.strip(),v.strip().strip('"').strip("'"))
KEY=os.environ["ELEVENLABS_API_KEY"]; VOICE="5VJqyR650KC1jubNlVCG"

# Phonetic respell fed to the model only. Captions still spell both correctly.
BASE=("Girls, if you want one bag that gets you through the school run, the coffee run "
 "and everything after, this is it. This is the Ko-LETT from Velantra, in cashmere feel "
 "brushed wool. It's Loh-roh pee-AH-nah inspired, so the belted front holds it upright "
 "instead of slumping. Twenty inches across, and it fits a thirteen inch laptop with room "
 "left over. Leather wrapped handles, aged gold hardware, and no logo on it anywhere. "
 "Caramel or espresso. They're running a pre-order right now, thirty dollars off before "
 "it ships. So go get one, girls, and thank me later.")
# E adds a light delivery cue only where the back half went flat.
TAGGED=BASE.replace("Caramel or espresso.","[warmly] Caramel or espresso.")

VARIANTS={"D":(BASE,11),"E":(TAGGED,27),"F":(BASE,88)}

for tag,(text,seed) in VARIANTS.items():
    dest=OUT/f"cand-{tag}.mp3"; words=OUT/f"cand-{tag}-words.json"
    if dest.exists(): print(f"  cached {tag}"); continue
    body={"text":text,"model_id":"eleven_v3","seed":seed,
          "voice_settings":{"stability":0.0,"similarity_boost":0.85,"use_speaker_boost":True}}
    pf=OUT/f"_body-{tag}.json"; pf.write_text(json.dumps(body))
    r=subprocess.run(["curl","-s","--max-time","600",
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps?output_format=mp3_44100_128",
        "-H",f"xi-api-key: {KEY}","-H","Content-Type: application/json","--data-binary",f"@{pf}"],
        capture_output=True,text=True)
    try: d=json.loads(r.stdout)
    except Exception: print(f"  {tag} FAIL {r.stdout[:300]}"); continue
    if "audio_base64" not in d: print(f"  {tag} ERR {json.dumps(d)[:300]}"); continue
    dest.write_bytes(base64.b64decode(d["audio_base64"]))
    words.write_text(json.dumps(d.get("alignment") or d.get("normalized_alignment"),indent=1))
    dur=subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(dest)],
        capture_output=True,text=True).stdout.strip()
    print(f"  {tag}: {dur}s  {len(text.split())}w  {len(text.split())/float(dur):.2f} w/s")
