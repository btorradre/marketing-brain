from pathlib import Path
import json,subprocess,numpy as np
from scipy.signal import correlate,correlation_lags
from google import genai
from google.genai import types
from dotenv import dotenv_values
P=Path(__file__).resolve().parent;Q=P/'qa-gringo-aligned';root=P.parents[4];v=P/'exports/Weekender-Haaland-Gringo-Natural-AvatarV-Final.mp4'
assert v.exists()
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(v)]));(Q/'export-probe.json').write_text(json.dumps(probe,indent=2))
r=subprocess.run(['ffmpeg','-v','error','-i',str(v),'-f','null','-'],capture_output=True,text=True);assert r.returncode==0 and not r.stderr,r.stderr
# Decode and compare identical selected speech; normalization accommodates AAC encoding.
def audio(path):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-vn','-ac','1','-ar','8000','-f','f32le','-']),np.float32)
a=audio(P/'voice-gringo-natural/narration-natural.mp3');b=audio(v);c=correlate(b,a,method='fft');lag=int(correlation_lags(len(b),len(a))[np.argmax(c)]);n=min(len(a),len(b)-max(0,lag));corr=float(np.corrcoef(a[:n],b[max(0,lag):max(0,lag)+n])[0,1]);(Q/'export-audio-sync.json').write_text(json.dumps({'lag_samples_8000hz':lag,'lag_ms':lag/8,'correlation':corr,'decode_errors':r.stderr},indent=2));print('audio lag ms',lag/8,'correlation',corr,flush=True)
# Three lip windows from the actual final export, at original playback speed.
parts=['These clips are from the finished Velantra ad. Check the presenter inset mouth against actual speech at 24fps. Inspect opening 0–3s (inset changes left to right and back), middle 18–21s and end 40–43s (left inset). Report concrete phoneme observations, any sustained lead/lag, whether captions match speech when present, visual artifacts, and acceptable_for_review. Presenter is synthetic; that alone is not a defect. Do not claim exhaustive human listening. Return JSON.']
for label,start in [('opening',0),('middle',18),('end',40)]:
 f=Q/f'export-sync-{label}.mp4';subprocess.run(['ffmpeg','-v','error','-y','-ss',str(start),'-i',str(v),'-t','3','-vf','scale=720:1280','-c:v','libx264','-crf','18','-c:a','aac',str(f)],check=True)
 part=types.Part.from_bytes(data=f.read_bytes(),mime_type='video/mp4');part.video_metadata=types.VideoMetadata(fps=24);parts.extend([label,part])
c=genai.Client(api_key=dotenv_values(root/'.env')['GEMINI_API_KEY']);res=c.models.generate_content(model='gemini-2.5-pro',contents=parts,config=types.GenerateContentConfig(response_mime_type='application/json'));(Q/'export-sync-model.json').write_text(res.text+'\n');print(res.text,flush=True)
# Whole export review for cuts, caption placement, missing media, variety and product continuity.
f=Q/'export-review-small.mp4';subprocess.run(['ffmpeg','-v','error','-y','-i',str(v),'-vf','scale=540:960','-c:v','libx264','-crf','23','-c:a','aac',str(f)],check=True)
part=types.Part.from_bytes(data=f.read_bytes(),mime_type='video/mp4');part.video_metadata=types.VideoMetadata(fps=3)
res=c.models.generate_content(model='gemini-2.5-pro',contents=['Review this 47.7s finished portrait fashion ad. Check the ENTIRE video for Media Offline frames, unintended black/green areas, frozen presenter during speech, captions mismatched to words, text over face/product details, repeated visual scenes and malformed product motion. Bag should have two rolled handles and two horizontal front closure straps with gold end fittings in visible closed-front views (detail crops may not show both; interior should have one wide slip pocket). Athlete photos are intentional stills, distinct wardrobe shots are intentional stills, final clean bag hero intentionally has no captions/presenter and ends with the narration; there is no added silent hold. Do not penalize those choices. Report time-specific concrete problems, severity and review verdict. Distinguish actual observation from inference; do not call 3fps sampling a consecutive frame audit. Return JSON.',part],config=types.GenerateContentConfig(response_mime_type='application/json'));(Q/'export-whole-model.json').write_text(res.text+'\n');print(res.text)
