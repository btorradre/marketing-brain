from pathlib import Path
import json
from google import genai
from google.genai import types
from dotenv import dotenv_values
v=Path(__file__).resolve().parent;b=v.parents[1];root=b.parents[3]
c=genai.Client(api_key=dotenv_values(root/'.env')['GEMINI_API_KEY'])
prompt='Listen to the two supplied audio recordings. First is reference speaker; second is synthesized new narration in the permitted clone. Transcribe ONLY the second recording exactly as heard. Then assess omitted/repeated words, unnatural glitches, clarity, voice similarity and natural pace. Specifically note pronunciation of Erling Haaland, Birkin, Velantra, Cognac. Do not infer quality from the provided script. Return JSON with transcript, quality_findings, similarity_observation, limitations. No invented times.'
r=c.models.generate_content(model='gemini-2.5-pro',contents=[prompt,types.Part.from_bytes(data=(v/'reference-source.wav').read_bytes(),mime_type='audio/wav'),types.Part.from_bytes(data=(v/'narration-original.mp3').read_bytes(),mime_type='audio/mpeg')],config=types.GenerateContentConfig(response_mime_type='application/json'))
(v/'audio-qa-model.json').write_text(r.text+'\n');print(r.text)
