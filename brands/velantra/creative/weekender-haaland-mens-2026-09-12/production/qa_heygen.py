from pathlib import Path
import json,subprocess
from google import genai
from google.genai import types
from dotenv import dotenv_values
p=Path(__file__).resolve().parent;root=p.parents[4];h=p/'heygen';f=h/'presenter-native.mp4'
subprocess.run(['ffmpeg','-v','error','-y','-i',str(f),'-vf','fps=1/3,scale=240:360,tile=4x4','-frames:v','1',str(h/'contact.jpg')],check=True)
c=genai.Client(api_key=dotenv_values(root/'.env')['GEMINI_API_KEY'])
r=c.models.generate_content(model='gemini-2.5-pro',contents=['Inspect this entire talking head video with its audio. Transcribe the words exactly; check lip sync against the actual audio, face consistency, distorted hands/microphone, green-screen stability, unusual motion. Return JSON with transcript, lip_sync_findings, artifacts_with_times, pass_for_ad and limitations. Do not infer lip sync merely because someone talks.',types.Part.from_bytes(data=f.read_bytes(),mime_type='video/mp4')],config=types.GenerateContentConfig(response_mime_type='application/json'))
(h/'qa-model.json').write_text(r.text+'\n');print(r.text)
