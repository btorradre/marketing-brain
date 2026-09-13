from pathlib import Path
import subprocess,base64,httpx,json
O=Path(__file__).resolve().parent;ROOT=O.parents[5];key=next(l.split('=',1)[1].strip().strip('"').strip("'") for l in (ROOT/'.env').read_text().splitlines() if l.startswith('GEMINI_API_KEY='))
parts=[]
for label,p,start in [('A',O.parent/'production-v18/narration.mp3',10),('B',O/'qa/natural-1x-audition.mp3',0)]:
 f=O/f'qa/compare-{label}.mp3';subprocess.run(['ffmpeg','-v','error','-y','-ss',str(start),'-i',str(p),'-t','25',str(f)],check=True);parts.extend([{'text':'Sample '+label},{'inline_data':{'mime_type':'audio/mpeg','data':base64.b64encode(f.read_bytes()).decode()}}])
parts.append({'text':'Listen to these two speech samples and describe their audible voice quality independently. Assess perceived gender presentation and age range with appropriate uncertainty, timbre, pitch and naturalness for each. Then assess whether they could be the same speaker and whether B has distracting distortion, unnatural robotic rhythm or wrong pitch. Do not infer identity from filenames or assume a target gender. JSON only: sample_A, sample_B, same_speaker_plausible, B_usable_for_conversational_narration, concrete_issues.'})
r=httpx.post('https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-pro-preview:generateContent',headers={'x-goog-api-key':key},json={'contents':[{'parts':parts}],'generationConfig':{'temperature':.1,'responseMimeType':'application/json'}},timeout=240)
if not r.is_success:print('QA status',r.status_code,r.text[:300]);r.raise_for_status()
j=r.json();z=''.join(t.get('text','') for a in j['candidates'] for t in a['content']['parts']);(O/'qa/natural-1x-comparison.json').write_text(z);print(z,flush=True)
