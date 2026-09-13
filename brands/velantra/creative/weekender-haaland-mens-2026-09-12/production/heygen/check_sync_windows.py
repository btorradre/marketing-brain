from pathlib import Path
import json
from google import genai
from google.genai import types
from dotenv import dotenv_values
h=Path(__file__).resolve().parent;p=h.parent;root=p.parents[4]
c=genai.Client(api_key=dotenv_values(root/'.env')['GEMINI_API_KEY']);parts=['Inspect these three cropped native HeyGen video/audio windows at 24fps (opening0s,middle18s,end35s). Evaluate specific visible lip closures for B/P/M and vowel timing against actual speech, and any persistent lead/lag. It is an intentionally synthetic small inset presenter; do not reject it merely for being AI. Report observed concrete phoneme examples with local times, obvious_sync_drift, artifact severity, acceptable_for_inset, limitations. Do not claim every phoneme is checked. Return JSON.']
for n in ['opening','middle','end']:
 part=types.Part.from_bytes(data=(h/f'qa-{n}.mp4').read_bytes(),mime_type='video/mp4');part.video_metadata=types.VideoMetadata(fps=24);parts.extend([n,part])
r=c.models.generate_content(model='gemini-2.5-pro',contents=parts,config=types.GenerateContentConfig(response_mime_type='application/json'));(h/'sync-windows.json').write_text(r.text+'\n');print(r.text)
