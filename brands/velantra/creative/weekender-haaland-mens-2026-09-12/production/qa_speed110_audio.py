from pathlib import Path
import json,subprocess,re,requests
from dotenv import dotenv_values
from google import genai
from google.genai import types
P=Path(__file__).resolve().parent;B=P.parent;root=P.parents[4];Q=P/'qa-speed110';Q.mkdir(exist_ok=True);v=P/'exports/Weekender-Haaland-Gringo-Natural-AvatarV-110-NoGaps.mp4';env=dotenv_values(root/'.env')
# PCM extraction for inspection/transcription, not a production edit.
f=Q/'export-audio.wav';subprocess.run(['ffmpeg','-v','error','-y','-i',str(v),'-vn','-ac','1','-ar','24000',str(f)],check=True)
with f.open('rb') as fp:
 res=requests.post('https://api.elevenlabs.io/v1/speech-to-text',headers={'xi-api-key':env['ELEVENLABS_API_KEY']},data={'model_id':'scribe_v2','language_code':'eng','tag_audio_events':'true','timestamps_granularity':'word'},files={'file':('audio.wav',fp,'audio/wav')},timeout=90)
res.raise_for_status();j=res.json();(Q/'export-scribe.json').write_text(json.dumps(j,indent=2));print('ACTUAL TRANSCRIPT',j['text'],flush=True)
words=[w for w in j['words'] if w['type']=='word'];gaps=[{'after':a['text'],'before':b['text'],'start':a['end'],'end':b['start'],'duration':round(b['start']-a['end'],3)} for a,b in zip(words,words[1:]) if b['start']-a['end']>.26];print('TRANSCRIBED GAPS',gaps,flush=True)
(Q/'transcribed-gaps.json').write_text(json.dumps(gaps,indent=2))
parts=['Review these exact exported clips at 1.1x, with pauses deliberately shortened. Inspect presenter mouth/audio sync, first/last consonant clipping at joins, audible clicks/glitches, remaining dead space and unnatural joins. Synthetic presenter alone is not a defect. Captions need matching phrases and clean scene transitions. Final hero intentionally has no presenter/text and ends with CTA. Return JSON with concrete time-specific observations, severity and acceptable_for_review. Do not claim human listening or exhaustive frame review.']
for label,start,duration in [('opening',0,4),('middle',13.5,4),('late_presenter',27.5,4),('ending',31.5,3.1667)]:
 p=Q/f'sync-{label}.mp4';subprocess.run(['ffmpeg','-v','error','-y','-ss',str(start),'-i',str(v),'-t',str(duration),'-vf','scale=720:1280','-c:v','libx264','-crf','18','-c:a','aac',str(p)],check=True)
 part=types.Part.from_bytes(data=p.read_bytes(),mime_type='video/mp4');part.video_metadata=types.VideoMetadata(fps=24);parts.extend([f'{label} original global start{start}s',part])
parts.extend(['Also listen to the whole exported audio below and check every join for intelligibility, any word loss/repeats and dead spaces. Approved exact script: '+(B/'storyboard/narration.txt').read_text(),types.Part.from_bytes(data=f.read_bytes(),mime_type='audio/wav')])
c=genai.Client(api_key=env['GEMINI_API_KEY']);res=c.models.generate_content(model='gemini-2.5-pro',contents=parts,config=types.GenerateContentConfig(response_mime_type='application/json'));(Q/'sync-model.json').write_text(res.text+'\n');print(res.text,flush=True)
