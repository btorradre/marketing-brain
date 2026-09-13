import json,base64,subprocess
from pathlib import Path
import requests
p=Path(__file__).resolve().parent;root=p.parents[5];src=Path.home()/'Downloads/MOT-VID-013-science-CapCut-A.mp4'
a=p/'export-A-audio.m4a';subprocess.run(['ffmpeg','-v','error','-y','-i',str(src),'-vn','-c:a','aac','-b:a','96k',str(a)],check=True)
key=next(l.split('=',1)[1].strip().strip('"').strip("'") for l in (root/'.env').read_text().splitlines() if l.startswith('GEMINI_API_KEY='))
prompt='Listen to the entire exported ad. Review actual audio, especially intelligibility after speed-up, abrupt edits, vocal pitch artifacts, distracting music, pauses, exact words, pronunciation of Motilli, apigenin and chlorophyllin. Do not infer from script; compare the actual sound. Return JSON with verdict(pass/revise), voice_description, pace_and_intelligibility, music_description_and_balance, pronunciation, omitted_words, extra_words, audible_issues[{time_s,issue,severity}], last_spoken_word_time_s, whether_end_fade_is_clean. Approved script: '+(p.parent.parent/'narration-script.txt').read_text()
r=requests.post('https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent',headers={'x-goog-api-key':key},json={'contents':[{'role':'user','parts':[{'text':prompt},{'inlineData':{'mimeType':'audio/mp4','data':base64.b64encode(a.read_bytes()).decode()}}]}],'generationConfig':{'responseMimeType':'application/json'}},timeout=180)
if r.status_code!=200:raise RuntimeError('Audio QA HTTP '+str(r.status_code))
d=r.json();j=json.loads(''.join(x.get('text','') for x in d['candidates'][0]['content']['parts']));(p/'export-A-audio-review.json').write_text(json.dumps(j,indent=2));print(json.dumps(j),flush=True)
