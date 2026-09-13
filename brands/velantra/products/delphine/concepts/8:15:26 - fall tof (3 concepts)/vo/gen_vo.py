#!/usr/bin/env python3
"""Delphine fall TOF — 5 VO tracks, one seamless take each.

v2 (8/15): rescripted onto Brooks's framework —
  hook / "This is the Delphine from Velantra. It's Birkin inspired." (VERBATIM, never reworded)
  / mechanism stated as a CONSEQUENCE, phrased differently in every ad, never "rigid" or "box"
  / concrete fit proof / "if you're looking for X this is the one for you" / sale + colors CTA.

Voice: Velantra Voice #2 (25-30). The Eden-ref clone that shipped the goeswith winner has been
deleted from the account; voice-registry.json is stale on it.
Model: eleven_v3, Creative preset (stability 0.0).
"""
import pathlib, json, ssl, urllib.request

HERE = pathlib.Path(__file__).parent
ENV = pathlib.Path("/Users/brooksorradre2/Documents/marketing brain/.env")
for line in ENV.read_text().splitlines():
    if line.startswith("ELEVENLABS_API_KEY="):
        KEY = line.split("=", 1)[1].strip().strip('"').strip("'")

VOICE = "ILMJn7ldIJifKqv4WLiL"  # Velantra Voice #2 (25-30)

ID = "This is the Delphine from Velantra. It's Birkin inspired."
CLOSE = ("If you're looking for a small cute bag that fits your everyday essentials, this is the "
         "one for you. End of summer sale's on and the colors are going fast so I'd hurry.")

SCRIPTS = {
 # hook | ID line | mechanism-as-consequence (unique per ad) | fit proof | close
 "VO-01": f"Okay, it's officially that time of year where I look at my summer bag and go, yeah, you're done. {ID} The problem with small bags is they go flat and soft and nothing really fits. This one keeps its shape, so the room is actually there. My wallet's in there, sunglasses, keys, and it still shuts. {CLOSE}",
 "VO-02": f"Every fall I realize I don't own a single bag that actually works for fall. {ID} Most small bags just cave in on themselves so the space kind of disappears. This one doesn't. Everything goes in and it still closes. {CLOSE}",
 "VO-03": f"I have like twelve handbags and not one of them fits a normal day out. {ID} Most small bags are so soft they fold in half the second you put them down. This one holds itself up. Phone, wallet, sunglasses in the case, keys, and it shuts. {CLOSE}",
 "VO-04": f"You know when your bag's too small so you end up just carrying your phone and your keys in your actual hands? {ID} Most small bags go flat and soft and there's just no actual room in them. This one stays open, so everything goes in. I get my hands back and I can shut my own front door. {CLOSE}",
 "VO-05": f"Nobody tells you the hardest bag to find is a small one that actually holds stuff. {ID} Most small bags are so soft they tip over and everything slides into one corner. This one won't. It sits upright and everything stays exactly where I put it. {CLOSE}",
}

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

for name, text in SCRIPTS.items():
    body = json.dumps({
        "text": text,
        "model_id": "eleven_v3",
        "voice_settings": {"stability": 0.0, "similarity_boost": 0.75, "use_speaker_boost": True},
    }).encode()
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}",
        data=body,
        headers={"xi-api-key": KEY, "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=180) as r:
            out = HERE / f"{name}.mp3"
            out.write_bytes(r.read())
            print(f"{name} -> {out.name} ({out.stat().st_size} bytes)")
    except Exception as e:
        detail = getattr(e, "read", lambda: b"")()
        print(f"{name} FAILED: {e} {detail[:300]}")
    (HERE / f"{name}.txt").write_text(text)
