#!/usr/bin/env python3
"""Generate the three greenscreen creator keyframes for VEL-VIVIENNE-GS-EVERYTHING-01.

Text-to-image on chroma green (kie gpt-image-2-text-to-image, 2:3, 2K). The Pinterest
pins in refs/ are LOOK references only — age, hair, colouring, styling register. The
person generated is synthetic, never a copy of the real person in the pin.
Anti-polish cues are mandatory (feedback_avatar_imperfection_cues).
"""
import os, json, time, sys, urllib.request, ssl, certifi, subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ctx = ssl.create_default_context(cafile=certifi.where())
KEY = subprocess.run(["bash","-lc",'set -a; source "/Users/brooksorradre2/Documents/marketing brain/.env"; set +a; echo -n "$KIE_API_KEY"'],capture_output=True,text=True).stdout.strip()

FRAME = ("Vertical 9:16 phone-camera portrait, chest-up, subject centred and facing the lens "
 "straight on, shoulders square, both hands down and out of frame, mouth closed in a relaxed "
 "neutral-warm expression, eyes on the lens. Background is a FLAT, EVEN, PURE CHROMA-GREEN "
 "studio backdrop (#00B140), completely empty, no props, no shadow cast on the green, no "
 "gradient, no logo. Soft even front lighting like a window, no hard shadow across the face. "
 "Shot on a modern phone front camera: slight softness, faint sensor grain, NOT tack sharp, "
 "NOT airbrushed, NOT retouched. Natural skin texture with visible pores and fine lines, a few "
 "flyaway hairs out of place, a real unposed everyday look. Photorealistic, documentary, "
 "absolutely no studio beauty retouching, no glamour glow, no CGI look, no 3D render.")

CREATORS = {
 "A-diane": (
   "A 58-year-old woman. Silver-blonde hair to just below the shoulders, soft natural wave, "
   "parted slightly off-centre, a little frizz at the crown. Fair skin, real sun lines at the "
   "corners of her eyes, faint freckling across the cheekbones and nose, laugh lines. Barely "
   "any makeup: bare lips, no lash extensions. Small plain gold hoop earrings. She wears a "
   "cream chunky-knit crewneck sweater. Warm, approachable, the neighbour everybody trusts. " + FRAME),
 "B-bridget": (
   "A 53-year-old woman. Dark brown hair to the collarbone, growing out naturally with grey "
   "coming through at the temples and a few silver strands through the front, tucked behind one "
   "ear. Fair skin with faint freckles across the nose, fine lines at the eyes and mouth, a "
   "slightly ruddy natural complexion. No makeup beyond a neutral lip. Small gold hoop earrings. "
   "She wears a rust-coloured fine-gauge knit with a crew neck. Warm, practical, no-nonsense. " + FRAME),
 "C-marguerite": (
   "A 62-year-old woman. Sharp silver bob cut to the jaw, one side tucked behind the ear, a few "
   "strands loose. Pale olive skin, fine lines across the forehead and around the mouth, a "
   "slightly weathered natural complexion. No makeup except a neutral lip. One thin gold chain "
   "at the throat, no other jewellery. She wears a black fine-gauge turtleneck. Cool, precise, "
   "the friend with taste. " + FRAME),
}

def post(url, payload):
    req = urllib.request.Request(url, data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=120, context=ctx).read())

def get(url):
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {KEY}"})
    return json.loads(urllib.request.urlopen(req, timeout=120, context=ctx).read(), strict=False)

def credit():
    return get("https://api.kie.ai/api/v1/chat/credit")["data"]

if __name__ == "__main__":
    only = sys.argv[1] if len(sys.argv) > 1 else None
    tasks = {}
    print("balance before:", credit())
    for name, prompt in CREATORS.items():
        if only and name != only: continue
        r = post("https://api.kie.ai/api/v1/jobs/createTask",
                 {"model": "gpt-image-2-text-to-image",
                  "input": {"prompt": prompt, "aspect_ratio": "2:3", "resolution": "2K"}})
        tid = r.get("data", {}).get("taskId")
        print(name, "->", tid, r.get("msg"))
        if tid:
            tasks[name] = tid
            json.dump(tasks, open(HERE/"_tasks.json","w"), indent=1)
    for name, tid in tasks.items():
        for _ in range(80):
            d = get(f"https://api.kie.ai/api/v1/jobs/recordInfo?taskId={tid}")["data"]
            st = d.get("state")
            if st == "success":
                urls = json.loads(d["resultJson"])["resultUrls"]
                out = HERE / f"{name}-green.png"
                subprocess.run(["curl","-sL","-A","Mozilla/5.0","-o",str(out),urls[0]],check=True)
                print(name, "OK", out.name, "credits:", d.get("creditsConsumed"))
                break
            if st == "fail":
                print(name, "FAIL", d.get("failMsg")); break
            time.sleep(8)
    print("balance after:", credit())
