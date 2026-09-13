from pathlib import Path
import json,subprocess,concurrent.futures
from google import genai
from google.genai import types
from dotenv import dotenv_values
p=Path(__file__).resolve().parent;root=p.parents[4];q=p/'qa';q.mkdir(exist_ok=True)
c=genai.Client(api_key=dotenv_values(root/'.env')['GEMINI_API_KEY'])
def job(sid):
 f=p/'omni'/f'{sid}-native.mp4'
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(f),'-vf','fps=2,scale=216:384,tile=4x4','-frames:v','1',str(q/f'{sid}-contact.jpg')],check=True)
 prompt='Inspect this entire short product video for visual defects and describe the actual action. Compare to supplied first-frame image. Check bag silhouette, leather/canvas boundary, rolled handles, horizontal front closure straps and gold fittings wherever visible, hand anatomy, texture shimmer, background warping, extra text or inset people. For the open interior view do not demand closed-front straps; instead check one wide slip pocket and stable lining. Do not claim physical dimensions. Return JSON with actual_action, visible_identity_changes, artifacts_with_times, usable_interval_seconds, pass_for_ad and limitations. Be critical; do not approve a fabricated feature.'
 r=c.models.generate_content(model='gemini-2.5-pro',contents=[prompt,types.Part.from_bytes(data=(p/'plates'/f'{sid}-clean.png').read_bytes(),mime_type='image/png'),types.Part.from_bytes(data=f.read_bytes(),mime_type='video/mp4')],config=types.GenerateContentConfig(response_mime_type='application/json'))
 (q/f'{sid}-model-qa.json').write_text(r.text+'\n');print(sid,r.text,flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:list(ex.map(job,['S04','S07','S11','S12']))
