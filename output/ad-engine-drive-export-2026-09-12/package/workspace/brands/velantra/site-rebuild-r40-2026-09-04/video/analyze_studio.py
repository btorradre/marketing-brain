import importlib.util,base64,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("gen",ROOT/"generate_studio.py");gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen)
video=ROOT/"assets/vivienne-studio-raw.mp4"
ref=ROOT/"assets/vivienne-studio-keyframe.png"
prompt="""Perform strict visual QA of this generated silent studio handbag video against the supplied first-frame image. Observe real temporal behavior. Check: (1) bag silhouette, handles, inward cognac strap tails, brass center plate and paired vertical staples remain stable, (2) body and bag motion is natural with no teleporting, morphing or visible text, (3) whole bag remains in frame, (4) identify best clean source time range for a quiet hero loop, preferably 3-9 seconds. Do not infer unseen physical product properties. Return concise JSON with pass boolean, product_identity, motion, framing, issues, clean_range_seconds. Note any hardware drift honestly."""
payload={"contents":[{"role":"user","parts":[{"text":prompt},{"inlineData":{"mimeType":"image/png","data":base64.b64encode(ref.read_bytes()).decode()}},{"inlineData":{"mimeType":"video/mp4","data":base64.b64encode(video.read_bytes()).decode()}}]}],"generationConfig":{"responseMimeType":"application/json"}}
d=gen.request("https://generativelanguage.googleapis.com/v1beta/models/gemini-3.7-flash:generateContent",payload)
texts=[part.get("text","") for c in d.get("candidates",[]) for part in c.get("content",{}).get("parts",[])]
(ROOT/"qa/studio-gemini-qa.json").write_text("\n".join(texts));print("\n".join(texts))
