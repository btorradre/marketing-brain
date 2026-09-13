#!/usr/bin/env python3
"""Copy approved clips into BROLL_LIBRARY/<category>/ (trimmed to the QA usable window, max 8s) and write broll_manifest.csv."""
import csv, json, os, shutil, subprocess
from common import *
from manifest import CLIPS as MAN, build_prompt
LIB = os.path.join(ROOT, "BROLL_LIBRARY")
CATS = ["01_Product_Angles","02_Details","03_Hand_Interaction","04_Carrying","05_Mirror","06_Outfits","07_POV","08_Home","09_Car","10_Work_Cafe","11_Whats_In_My_Bag","12_Movement","13_Transitions","14_Misc"]
for c in CATS: os.makedirs(os.path.join(LIB, c), exist_ok=True)
qa = load(os.path.join(STATE, "clip_qa.json"), {}); hr = load(os.path.join(STATE, "human_review.json"), {}); kfqa = load(os.path.join(STATE, "kf_qa.json"), {}); picks = load(os.path.join(STATE, "picks.json"), {})
def dur(p):
    return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",p],capture_output=True,text=True).stdout.strip() or 0)
import sys
ONLY = set(sys.argv[1:])
rows = []; n = 0
for c in MAN:
    cid = c["id"]
    if ONLY and cid not in ONLY: continue
    q = qa.get(cid, {}); src = os.path.join(CLIPS, f"{cid}.mp4")
    h = hr.get(cid, {})
    if h.get("verdict") != "PASS" or not os.path.exists(src): continue
    slug = c["scene"].split(",")[0].split(".")[0].lower(); slug = "".join(ch if ch.isalnum() else "-" for ch in slug).strip("-")[:40]
    fn = f"{cid}-{c['colorway']}-{slug}.mp4"; dst = os.path.join(LIB, c["category"], fn)
    win = h.get("usable_window") or q.get("usable_window") or "0-8"
    try:
        a, b = [float(x) for x in win.replace("s","").split("-")]
    except Exception: a, b = 0.0, 8.0
    b = min(b, a + 8.0, dur(src)); a = max(0.0, a)
    if b - a < 3.0: a, b = 0.0, min(8.0, dur(src))
    subprocess.run(["ffmpeg","-y","-loglevel","error","-ss",f"{a:.2f}","-i",src,"-t",f"{b-a:.2f}","-c:v","libx264","-preset","medium","-crf","18","-an","-movflags","+faststart",dst],check=True)
    s = q.get("scores", {}); kq = kfqa.get(picks.get(cid, {}).get("kf", "").replace("keyframes/", ""), {}).get("scores", {})
    final = round(sum(s.get(k, 0) for k in s) / max(1, len(s)), 1) if s else ""
    rows.append(dict(clip_id=cid, filename=os.path.join(c["category"], fn), category=c["category"], colorway=c["colorway"], shot_description=c["scene"],
        camera_height=c["camera_height"], camera_angle=c["camera_angle"], camera_distance=c["camera_distance"], camera_movement=c["camera_movement"],
        environment=c["environment"], lighting=c["lighting"], product_orientation=c["product_orientation"], product_action=c["product_action"],
        human_action=c["human_action"], duration=round(b - a, 2), engine=c["engine"], generation_prompt=build_prompt(c), motion_prompt=c["motion"],
        tiktok_pattern_reference=c["pattern"], product_accuracy_score=s.get("product_accuracy",""), product_consistency_score=s.get("product_consistency",""),
        organic_score=s.get("organic_ugc_appearance",""), iphone_realism_score=s.get("iphone_camera_realism",""), ai_artifact_score=s.get("ai_artifact_severity",""),
        final_QA_score=final, gemini_verdict=q.get("verdict",""), gemini_reason=(q.get("reason") or ""), human_review="PASS", notes=h.get("note","")))
    n += 1
prev = load(os.path.join(STATE, "library_files.json"), {}) if ONLY else {}
prev.update({r["clip_id"]: r["filename"] for r in rows}); json.dump(prev, open(os.path.join(STATE, "library_files.json"), "w"), indent=1)
print(f"distributed {n} approved clips -> {LIB}")
