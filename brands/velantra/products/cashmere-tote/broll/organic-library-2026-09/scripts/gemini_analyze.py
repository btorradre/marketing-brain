#!/usr/bin/env python3
"""Gemini visual analysis of every downloaded reference TikTok (video itself, not caption).
Writes research/gemini_analysis.jsonl (one JSON per video) and research/pattern_stats.json (aggregate)."""
import json, os, sys, time, re, collections
from concurrent.futures import ThreadPoolExecutor, as_completed
from google import genai
HERE = os.path.dirname(os.path.abspath(__file__)); RES = os.path.join(HERE, "..", "research")
VID = os.path.join(RES, "videos"); OUT = os.path.join(RES, "gemini_analysis.jsonl")
ENV = {}
for l in open(os.path.expanduser("~/Documents/marketing brain/.env")):
    l = l.strip()
    if "=" in l and not l.startswith("#"):
        k, v = l.split("=", 1); ENV[k] = v.strip().strip('"').strip("'")
client = genai.Client(api_key=ENV["GEMINI_API_KEY"])
MODEL = os.environ.get("GEMINI_VIDEO_MODEL", "gemini-3.7-flash")

PROMPT = """You are analysing an organic TikTok video for a study of how real creators film handbags and totes on their phones. Watch the whole video. Ignore the caption and the audio; only what is visible matters.

Return ONLY valid JSON with these fields:
{
 "relevant": true/false,   // true only if a handbag / tote / purse is physically on screen for a meaningful part of the video
 "bag_type": "tote | shoulder bag | top handle | crossbody | clutch | backpack | multiple | none",
 "creator_shot": true/false,  // looks self-shot by a person on a phone, not a brand/pro production
 "pro_production": true/false,
 "content_format": "outfit check | what's in my bag | review to camera | unboxing | haul | GRWM | styling multiple outfits | day in the life | collection tour | packing | comparison | other",
 "first_2s_hook": "what is literally on screen in the first 2 seconds, one sentence",
 "shots": [   // one entry per distinct shot/setup, in order, max 12
   {"t": "MM:SS", "camera_height": "eye|chest|waist|floor|overhead|top-down|low angle|high angle",
    "camera_angle": "front|three-quarter|side profile|behind subject|POV|top-down",
    "distance": "macro|extreme close-up|close-up|medium|full product|full body|environmental wide",
    "movement": "static|handheld|pan|tilt|push-in|pull-back|tracking|orbit|reveal|whip pan|natural hand movement|walking camera|mirror filming",
    "product_orientation": "front|back|left side|right side|three-quarter|top|bottom|interior|open|closed|not visible",
    "interaction": "none|picking up|putting down|carrying in hand|carrying on forearm|carrying on shoulder|opening|closing|reaching inside|removing items|packing items|adjusting strap|holding handles|putting over shoulder|taking off shoulder|walking|turning|swinging|on lap|placing on chair|grabbing from car seat|touching material|showing to camera|other",
    "environment": "bedroom|closet|bathroom|living room|kitchen|hallway|apartment other|hotel|office|cafe|restaurant|car|sidewalk|elevator|lobby|airport|store|outdoors other|studio backdrop|other",
    "lighting": "window light|warm indoor|cool indoor|bathroom lighting|overcast daylight|direct sunlight|golden hour|mixed|low light|ring light|studio",
    "face_visible": "full|partial|hidden by phone|cropped out|back of head|none",
    "human_present": true/false,
    "mirror": true/false,
    "desc": "one plain sentence of what happens"}
 ],
 "phone_realism_cues": ["list the imperfections you actually saw: hand shake, autofocus hunting, focus breathing, exposure shift, off-centre framing, motion blur, phone sharpening, blown window, background clipping, camera roll, reframing, subject leaves frame, awkward composition, imperfect move start/end"],
 "transitions": ["any transitions seen: hard cut, hand covers lens, whip pan, bag passes camera, walk into frame, walk out, set-down into frame, zoom cut, none"],
 "text_overlay_heavy": true/false,
 "notable_or_uncommon": "one sentence on anything unusual worth testing, or empty"
}"""

def analyze(path, vid, tries=2):
    for a in range(tries):
        try:
            f = client.files.upload(file=path)
            while f.state.name == "PROCESSING":
                time.sleep(3); f = client.files.get(name=f.name)
            if f.state.name != "ACTIVE": raise RuntimeError(f.state.name)
            r = client.models.generate_content(model=MODEL, contents=[f, PROMPT])
            txt = re.sub(r"^```(?:json)?\s*|\s*```$", "", r.text.strip(), flags=re.S)
            m = re.search(r"\{.*\}", txt, flags=re.S)
            d = json.loads(m.group(0)); d["video_id"] = vid
            try: client.files.delete(name=f.name)
            except Exception: pass
            return d
        except Exception as e:
            err = e; time.sleep(6 * (a + 1))
    return {"video_id": vid, "error": str(err)[:300]}

def cmd_run(workers=5):
    done = set()
    if os.path.exists(OUT):
        for l in open(OUT):
            try: done.add(json.loads(l)["video_id"])
            except Exception: pass
    todo = [f[:-4] for f in sorted(os.listdir(VID)) if f.endswith(".mp4") and f[:-4] not in done]
    print(f"{len(todo)} videos to analyse ({len(done)} done)", flush=True)
    with ThreadPoolExecutor(max_workers=workers) as ex, open(OUT, "a") as out:
        for fut in as_completed([ex.submit(analyze, os.path.join(VID, v + ".mp4"), v) for v in todo]):
            d = fut.result(); out.write(json.dumps(d) + "\n"); out.flush()
            print(d["video_id"], "ERR" if "error" in d else ("rel" if d.get("relevant") else "irrel"), flush=True)

def cmd_stats():
    rows = [json.loads(l) for l in open(OUT)]
    rel = [r for r in rows if r.get("relevant") and not r.get("error")]
    C = lambda: collections.Counter()
    st = {"videos_analysed": len(rows), "relevant": len(rel), "errors": sum(1 for r in rows if r.get("error")),
          "creator_shot": sum(1 for r in rel if r.get("creator_shot")), "pro_production": sum(1 for r in rel if r.get("pro_production"))}
    cnt = {k: C() for k in ["content_format", "bag_type", "camera_height", "camera_angle", "distance", "movement",
                            "product_orientation", "interaction", "environment", "lighting", "face_visible", "cues", "transitions"]}
    vid_level = {k: C() for k in ["mirror", "any_car", "any_walking", "any_open_interior", "text_overlay_heavy", "human_present"]}
    hooks = []
    for r in rel:
        cnt["content_format"][r.get("content_format")] += 1; cnt["bag_type"][r.get("bag_type")] += 1
        for c in r.get("phone_realism_cues") or []: cnt["cues"][c.lower().strip()] += 1
        for t in r.get("transitions") or []: cnt["transitions"][t.lower().strip()] += 1
        shots = r.get("shots") or []
        flags = {"mirror": any(s.get("mirror") for s in shots), "any_car": any(s.get("environment") == "car" for s in shots),
                 "any_walking": any("walk" in str(s.get("interaction")) + str(s.get("movement")) for s in shots),
                 "any_open_interior": any(s.get("product_orientation") in ("interior", "open") or s.get("interaction") in ("reaching inside", "removing items", "packing items", "opening") for s in shots),
                 "text_overlay_heavy": bool(r.get("text_overlay_heavy")), "human_present": any(s.get("human_present") for s in shots)}
        for k, v in flags.items(): vid_level[k][v] += 1
        for s in shots:
            for k in ["camera_height", "camera_angle", "distance", "movement", "product_orientation", "interaction", "environment", "lighting", "face_visible"]:
                cnt[k][s.get(k)] += 1
        hooks.append(r.get("first_2s_hook"))
    st["shot_counts"] = {k: v.most_common(25) for k, v in cnt.items()}
    st["video_flags"] = {k: dict(v) for k, v in vid_level.items()}
    st["total_shots"] = sum(len(r.get("shots") or []) for r in rel)
    st["hooks_sample"] = hooks[:120]
    st["notable"] = [r.get("notable_or_uncommon") for r in rel if r.get("notable_or_uncommon")]
    json.dump(st, open(os.path.join(RES, "pattern_stats.json"), "w"), indent=1)
    print(json.dumps({k: st[k] for k in ["videos_analysed", "relevant", "errors", "creator_shot", "pro_production", "total_shots"]}))

if __name__ == "__main__":
    {"run": cmd_run, "stats": cmd_stats}[sys.argv[1] if len(sys.argv) > 1 else "run"]()
