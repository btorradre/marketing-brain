#!/usr/bin/env python3
"""Anchored 1-10 scoring pass (Gemini 3.7 Flash) on the trimmed library files -> state/library_scores.json.
Separate from the structural verdict so the scale is not compressed by the pass/fail task."""
import json, os, re, sys, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from google import genai
from PIL import Image
from common import *
client = genai.Client(api_key=ENV["GEMINI_API_KEY"]); MODEL = "gemini-3.7-flash"
PROMPT = """The first three images are ground-truth photos of a wool felt tote (3/4 hero, side, interior). Then a short AI-generated clip that is meant to look like a real customer casually filmed this exact bag on an iPhone.

Score the clip on ten scales from 1 to 10. Use the WHOLE scale with these anchors:
10 = indistinguishable from a real iPhone video of the real bag; 8 = a careful viewer would not notice anything wrong; 6 = a small flaw an attentive viewer might catch; 4 = an obvious flaw; 2 = clearly fake or clearly the wrong product.

product_accuracy: does the bag match the references (proportions, felt, two leather-wrapped handles, belt through straps with two curved free ends and gold disc caps, open top, no logo)?
product_consistency: does the bag stay the same object from first frame to last?
photorealism: does the whole frame look photographed rather than rendered?
organic_ugc_appearance: does it look like something a real creator would post, not a brand shoot?
iphone_camera_realism: phone-like exposure, focus, grain, handheld feel?
human_motion_realism (10 if no human): natural hands and body?
product_motion_realism (10 if the bag is static): does the bag move like felt and leather?
advertising_usefulness: would an editor drop this into a UGC or native ad as-is?
uniqueness_of_shot: how distinct is this framing/moment as a B-roll shot?
ai_artifact_severity: 10 = no artifacts at all, 1 = severe.

Return ONLY JSON: {"scores": {"product_accuracy": n, ...}, "note": "one sentence"}"""
def refs(trim):
    k = "espresso" if trim == "espresso" else "caramel"
    return [Image.open(REF[f"{k}_{x}"]).convert("RGB").resize((640, 640)) for x in ("hero", "side", "interior")]
def score(path, trim):
    for a in range(3):
        try:
            f = client.files.upload(file=path)
            while f.state.name == "PROCESSING": time.sleep(3); f = client.files.get(name=f.name)
            r = client.models.generate_content(model=MODEL, contents=[*refs(trim), f, PROMPT])
            txt = re.sub(r"^```(?:json)?\s*|\s*```$", "", r.text.strip(), flags=re.S)
            d = json.loads(re.search(r"\{.*\}", txt, flags=re.S).group(0))
            try: client.files.delete(name=f.name)
            except Exception: pass
            return d
        except Exception as e:
            err = e; time.sleep(5 * (a + 1))
    return {"error": str(err)[:200]}
if __name__ == "__main__":
    from manifest import CLIPS as MAN
    trim_of = {c["id"]: c["colorway"] for c in MAN}
    files = load(os.path.join(STATE, "library_files.json"), {}); out = os.path.join(STATE, "library_scores.json"); res = load(out, {})
    ids = sys.argv[1:] or [c for c in sorted(files) if c not in res]
    with ThreadPoolExecutor(max_workers=5) as ex:
        futs = {ex.submit(score, os.path.join(ROOT, "BROLL_LIBRARY", files[c]), trim_of[c]): c for c in ids}
        for fu in as_completed(futs):
            c = futs[fu]; res[c] = fu.result(); save(out, res)
            s = res[c].get("scores", {}); print(c, {k: s.get(k) for k in ("product_accuracy", "product_consistency", "organic_ugc_appearance", "ai_artifact_severity")}, flush=True)
