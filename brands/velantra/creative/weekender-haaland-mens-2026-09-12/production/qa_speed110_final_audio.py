from pathlib import Path
import json,subprocess,re,requests
from dotenv import dotenv_values
from google import genai
from google.genai import types
P=Path(__file__).resolve().parent;B=P.parent;root=P.parents[4];Q=P/'qa-speed110-final';Q.mkdir(exist_ok=True);v=P/'exports/Weekender-Haaland-Gringo-Natural-AvatarV-110-NoGaps-Final.mp4';env=dotenv_values(root/'.env')
f=Q/'export-audio.wav';subprocess.run(['ffmpeg','-v','error','-y','-i',str(v),'-vn','-ac','1','-ar','24000',str(f)],check=True)
with f.open('rb') as fp:
 res=requests.post('https://api.elevenlabs.io/v1/speech-to-text',headers={'xi-api-key':env['ELEVENLABS_API_KEY']},data={'model_id':'scribe_v2','language_code':'eng','tag_audio_events':'true','timestamps_granularity':'word'},files={'file':('audio.wav',fp,'audio/wav')},timeout=90)
res.raise_for_status();j=res.json();(Q/'export-scribe.json').write_text(json.dumps(j,indent=2));print('ACTUAL TRANSCRIPT',j['text'],flush=True)
words=[w for w in j['words'] if w['type']=='word'];gaps=[{'after':a['text'],'before':b['text'],'start':a['end'],'end':b['start'],'duration':round(b['start']-a['end'],3)} for a,b in zip(words,words[1:]) if b['start']-a['end']>.26];print('TRANSCRIBED GAPS',gaps,flush=True);(Q/'transcribed-gaps.json').write_text(json.dumps(gaps,indent=2))
# Dedicated full audio review with explicit coverage and no unrelated editorial opinions.
prompt='''Listen to the entire attached34.5second narration. It is deliberately110% pitch-corrected playback with sentence pauses shortened. Check every sentence transition for chopped consonants, missing/repeated words, clicks, glitches, unnatural pitch wobble and dead space. Short articulation gaps under0.25s are intentional, not dead space. Compare to exact approved script below, allowing brand pronunciation and ASR ambiguities but flag true missing words. Return a JSON object with keys full_audio_reviewed, exact_word_errors, audible_edit_defects, long_dead_spaces, pitch_quality, pacing, ending_complete, acceptable_for_review, limitations. Provide timestamps for each actual defect and empty arrays if none. Do not discuss captions or visuals, which are not attached. Do not claim human listening. Approved script:\n'''+(B/'storyboard/narration.txt').read_text()
c=genai.Client(api_key=env['GEMINI_API_KEY']);res=c.models.generate_content(model='gemini-2.5-pro',contents=[prompt,types.Part.from_bytes(data=f.read_bytes(),mime_type='audio/wav')],config=types.GenerateContentConfig(response_mime_type='application/json'));(Q/'whole-audio-model.json').write_text(res.text+'\n');print(res.text,flush=True)
