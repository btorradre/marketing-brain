#!/usr/bin/env python3
"""Gemini QA of generated clips (or keyframes) against the product references.
  python3 qa_clip.py clips [ID ...]   -> state/clip_qa.json
  python3 qa_clip.py frames [ID ...]  -> state/kf_qa.json  (every keyframe variant)"""
import json, os, re, sys, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from google import genai
from PIL import Image
from common import *
client = genai.Client(api_key=ENV["GEMINI_API_KEY"]); MODEL = os.environ.get("QA_MODEL","gemini-3.7-flash")

RUBRIC = """You are the QA gate for an AI-generated organic B-roll library of ONE handbag. The first three images are the ground-truth product references (3/4 hero, side profile, interior top-down). Then comes the generated {kind}.

GROUND TRUTH (from the references): oatmeal-greige brushed wool FELT tote, wider than tall (about 2:1), softly structured, open top with no flap and no zipper (only a small centre snap tab on the inner rims). TWO rolled top handles, leather-wrapped on the grip, felt below. On each face: TWO wide vertical felt straps and ONE slim leather belt crossing horizontally through them, its two ends curving outward and downward and hanging free, each tipped with a small round aged-gold DISC cap. Side gussets are clean felt with nothing attached. Metal is aged gold only. NO logo, NO lettering, NO embossing. Trim colour is {trim}. The felt is smooth brushed felt, not knitted.

Note: a true side-profile view shows the 18 cm deep gusset, which reads as a tall portrait shape; that is correct, so judge width-to-height proportions only in front or three-quarter views. Minor proportion softness (down to about 1.5:1) is a NOTE, not a fail; only a clearly square or upright bag fails.

Construction facts that are CORRECT and must not be flagged: each felt strap runs up the face and continues into the handle loop (strap and handle are one piece); the second handle (on the far face) is often visible behind or beside the near one; in a close-up or macro, parts of the bag are naturally cropped out of frame, so judge ONLY what is visible and never fail a frame for a part that is simply outside the crop. Score honestly on the absolute 1-10 scale; do not compress scores toward the middle.

COUNT before you judge (for a video, count at the start, middle and end): visible handles, visible belt ends, visible disc caps, visible felt straps, any metal that is not a disc cap or snap stud, any logo or lettering.

Structural failures are FAILS, never notes: a missing or extra handle, a belt that fuses into the strap or the side, disc caps that become buckles/loops/tabs/punch holes, a zipper or flap appearing, a strap attached to the side gusset, a logo or text appearing on the bag, knit texture instead of felt, a second identical bag, the bag changing proportions or construction between frames.

Score 1-10 each, honestly, on the absolute scale (a frame with no defects deserves 9 or 10; do not compress toward the middle):
product_accuracy, product_consistency (through motion; for a still, internal consistency), photorealism, organic_ugc_appearance, iphone_camera_realism, human_motion_realism (10 if no human), product_motion_realism (10 if static), advertising_usefulness, uniqueness_of_shot, ai_artifact_severity (10 = no artifacts at all).
Binary: text_added, product_morphed, construction_changed, extra_hardware, missing_hardware, extra_handles, added_logo, face_uncanny (a visible human face that looks AI), impossible_interaction, floating_artifact (a detached or unexplained piece of leather, felt or metal).

Also: usable_window: "start-end seconds" of the cleanest continuous stretch (video only), and counts: {{"handles":n,"belt_ends":n,"disc_caps":n,"straps":n}}.

THE VERDICT IS DECIDED ONLY BY STRUCTURE: verdict is FAIL if any binary flag is true, if any structural failure listed above is present, if the bag is clearly square or upright in a front or three-quarter view, or if there is a visible AI artifact on the bag or the hand. Otherwise the verdict is PASS. Do not fail a frame because of a numeric score.

Return ONLY JSON:
{{"scores":{{...}}, "binary":{{...}}, "counts":{{...}}, "usable_window":"0-8", "verdict":"PASS|FAIL", "reason":"one or two sentences naming the exact defect if FAIL"}}
"""

def refs(trim):
    k = "espresso" if trim == "espresso" else "caramel"
    return [Image.open(REF[f"{k}_hero"]).convert("RGB").resize((768, 768)),
            Image.open(REF[f"{k}_side"]).convert("RGB").resize((768, 768)),
            Image.open(REF[f"{k}_interior"]).convert("RGB").resize((768, 768))]

def qa(path, trim, kind):
    prompt = RUBRIC.format(kind=kind, trim="dark espresso brown leather" if trim == "espresso" else "warm cognac tan leather")
    for a in range(3):
        try:
            if kind == "video clip":
                f = client.files.upload(file=path)
                while f.state.name == "PROCESSING": time.sleep(3); f = client.files.get(name=f.name)
                media = f
            else:
                media = Image.open(path).convert("RGB")
            r = client.models.generate_content(model=MODEL, contents=[*refs(trim), media, prompt])
            txt = re.sub(r"^```(?:json)?\s*|\s*```$", "", r.text.strip(), flags=re.S)
            d = json.loads(re.search(r"\{.*\}", txt, flags=re.S).group(0))
            if kind == "video clip":
                try: client.files.delete(name=f.name)
                except Exception: pass
            return d
        except Exception as e:
            err = e; time.sleep(5 * (a + 1))
    return {"verdict": "ERROR", "reason": str(err)[:200]}

def main():
    from manifest import CLIPS as MAN
    mode = sys.argv[1]; ids = sys.argv[2:]
    trim_of = {c["id"]: c["colorway"] for c in MAN}
    if mode == "library":
        out = os.path.join(STATE, "library_qa.json"); res = load(out, {})
        files = load(os.path.join(STATE, "library_files.json"), {})
        jobs = [(cid, os.path.join(ROOT, "BROLL_LIBRARY", fn)) for cid, fn in sorted(files.items()) if (not ids or cid in ids) and (ids or cid not in res)]
        kind = "video clip"
    elif mode == "clips":
        out = os.path.join(STATE, "clip_qa.json"); res = load(out, {})
        jobs = [(cid, os.path.join(CLIPS, f"{cid}.mp4")) for cid in sorted(trim_of) if os.path.exists(os.path.join(CLIPS, f"{cid}.mp4")) and (not ids or cid in ids)]
        jobs = [(c, p) for c, p in jobs if ids or c not in res]
        kind = "video clip"
    else:
        out = os.path.join(STATE, "kf_qa.json"); res = load(out, {})
        jobs = []
        for cid in sorted(trim_of):
            d = os.path.join(KF, cid)
            if not os.path.isdir(d): continue
            for v in sorted(os.listdir(d)):
                if v.endswith(".png"):
                    key = f"{cid}/{v}"
                    if (not ids or cid in ids) and (ids or key not in res): jobs.append((key, os.path.join(d, v)))
        kind = "still image"
    print(f"{len(jobs)} to QA", flush=True)
    with ThreadPoolExecutor(max_workers=5) as ex:
        futs = {ex.submit(qa, p, trim_of[k.split("/")[0]], kind): k for k, p in jobs}
        for f in as_completed(futs):
            k = futs[f]; res[k] = f.result(); save(out, res)
            print(k, res[k].get("verdict"), (res[k].get("reason") or "")[:90], flush=True)

if __name__ == "__main__": main()
