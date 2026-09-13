#!/usr/bin/env python3
"""broll_manifest.csv from manifest + picks + human review + Gemini 3.7 library QA."""
import csv, os, subprocess
from common import *
from manifest import CLIPS as MAN, build_prompt
files = load(os.path.join(STATE, "library_files.json"), {}); hr = load(os.path.join(STATE, "human_review.json"), {})
qa = load(os.path.join(STATE, "library_qa.json"), {}); picks = load(os.path.join(STATE, "picks.json"), {})
def dur(p):
    return round(float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",p],capture_output=True,text=True).stdout.strip() or 0), 2)
rows = []
for c in MAN:
    cid = c["id"]; fn = files.get(cid)
    if not fn: continue
    q = qa.get(cid, {}); s = q.get("scores", {}) or {}; h = hr.get(cid, {}); p = picks.get(cid, {})
    engine = "kenburns" if "kenburns" in (h.get("note","") + p.get("note","")) or c["engine"] == "kenburns" else ("omni-1.1-flash" if int(cid[-3:]) >= 70 or cid in ("COL-070",) else "omni-flash-preview")
    final = round(sum(float(v) for v in s.values()) / len(s), 1) if s else ""
    rows.append(dict(clip_id=cid, filename=fn, category=c["category"], colorway=c["colorway"], shot_description=c["scene"],
        camera_height=c["camera_height"], camera_angle=c["camera_angle"], camera_distance=c["camera_distance"], camera_movement=c["camera_movement"],
        environment=c["environment"], lighting=c["lighting"], product_orientation=c["product_orientation"], product_action=c["product_action"],
        human_action=c["human_action"], duration=dur(os.path.join(ROOT, "BROLL_LIBRARY", fn)), engine=engine, keyframe=p.get("kf",""),
        generation_prompt=build_prompt(c), motion_prompt=c["motion"], tiktok_pattern_reference=c["pattern"],
        product_accuracy_score=s.get("product_accuracy",""), product_consistency_score=s.get("product_consistency",""),
        photorealism_score=s.get("photorealism",""), organic_score=s.get("organic_ugc_appearance",""), iphone_realism_score=s.get("iphone_camera_realism",""),
        human_motion_score=s.get("human_motion_realism",""), product_motion_score=s.get("product_motion_realism",""), ad_usefulness_score=s.get("advertising_usefulness",""),
        uniqueness_score=s.get("uniqueness_of_shot",""), ai_artifact_score=s.get("ai_artifact_severity",""), final_QA_score=final,
        text_added=(q.get("binary",{}) or {}).get("text_added",""), product_morphed=(q.get("binary",{}) or {}).get("product_morphed",""),
        construction_changed=(q.get("binary",{}) or {}).get("construction_changed",""), extra_hardware=(q.get("binary",{}) or {}).get("extra_hardware",""),
        missing_hardware=(q.get("binary",{}) or {}).get("missing_hardware",""), extra_handles=(q.get("binary",{}) or {}).get("extra_handles",""),
        added_logo=(q.get("binary",{}) or {}).get("added_logo",""), gemini_verdict=q.get("verdict",""), gemini_reason=q.get("reason",""),
        human_review=h.get("verdict",""), usable_window=h.get("usable_window",""), notes=h.get("note","")))
with open(os.path.join(ROOT, "broll_manifest.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print(f"manifest: {len(rows)} rows; gemini PASS {sum(1 for r in rows if r['gemini_verdict']=='PASS')}, FAIL {sum(1 for r in rows if r['gemini_verdict']=='FAIL')}, unscored {sum(1 for r in rows if not r['gemini_verdict'])}")
