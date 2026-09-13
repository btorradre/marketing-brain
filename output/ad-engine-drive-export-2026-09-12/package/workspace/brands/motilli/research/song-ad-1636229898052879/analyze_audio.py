from pathlib import Path
import json,os
from google import genai
from google.genai import types
p=Path(__file__).resolve().parent
for line in Path('.env').read_text().splitlines():
 if '=' in line and not line.lstrip().startswith('#'):
  k,v=line.split('=',1)
  if k.strip() in ('GEMINI_API_KEY','GOOGLE_API_KEY'):os.environ.setdefault(k.strip(),v.strip().strip('"').strip("'"))
client=genai.Client(api_key=os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_API_KEY'))
prompt="""Analyze this exact 223.6-second ad video. Return JSON only. This is evidence gathering, not a claim it converts. Listen to ALL audio. Provide (1) timestamped sung/spoken transcript for internal checking, segment each line or couplet with start/end seconds, distinguish singing vs speech and narrator/speaker; (2) audio_observations: singer voice, genre, melodic repetition/chorus, tempo estimates only if measurable, instrumental arrangement changes, rhyme patterns, shifts between musical and spoken sections, sound effects; (3) narrative_sections with start/end, factual visual summary, paraphrased story content and open questions raised or resolved; (4) exact opening and ending events, product first appearance versus first naming, ex-husband story payoff timing, whether hook promise really closes; (5) visible evidence/offer/CTA and claims, clearly distinguish advertiser claims from verified facts. Do not invent lyrics if uncertain, mark uncertainty. Timestamp estimates are not frame boundaries. Do not assume weight loss or medical causation from a smile. Do not overclaim psychological effects. Do not omit the final minute."""
r=client.models.generate_content(model='gemini-2.5-pro',contents=[types.Part.from_bytes(data=(p/'source.mp4').read_bytes(),mime_type='video/mp4'),prompt],config=types.GenerateContentConfig(response_mime_type='application/json'))
(p/'audio-video-model-review.json').write_text(r.text)
print('Saved secondary full-video/audio review',len(r.text),'characters',flush=True)
