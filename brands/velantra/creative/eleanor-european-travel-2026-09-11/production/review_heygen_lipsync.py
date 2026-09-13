from pathlib import Path
import json,subprocess,base64,requests
P=Path(__file__).resolve().parent;H=P/'heygen';Q=H/'qa';parts=[]
for t in [0,35,72]:
 f=Q/f'lip-window-{t}.mp4'
 subprocess.run(['ffmpeg','-y','-v','error','-ss',str(t),'-i',str(H/'presenter-native.mp4'),'-t','6','-vf','scale=540:810','-c:v','libx264','-crf','25','-c:a','aac',str(f)],check=True)
 parts.extend([{'text':f'This six-second window starts at source time {t}s.'},{'inlineData':{'mimeType':'video/mp4','data':base64.b64encode(f.read_bytes()).decode()},'videoMetadata':{'fps':15}}])
parts.append({'text':'Critically inspect these three actual talking-presenter windows with their audio at 15fps. Assess coarse lip sync, naturalness, visible mouth or hand artifacts. Do not claim perfect sync or measured milliseconds. Green background is intentional source footage and has NOT been keyed. Do not evaluate keying. Return JSON: windows (each with source_start_seconds, specific observed speech/mouth relationship, obvious_sync_drift, artifacts), acceptable_for_small_inset_presenter, must_fix, limits. This is machine perceptual review, not human approval.'})
root=next(p for p in P.parents if (p/'.env').exists());env=dict(l.split('=',1) for l in (root/'.env').read_text().splitlines() if '=' in l and not l.startswith('#'));key=env['GEMINI_API_KEY'].strip().strip('"').strip("'")
r=requests.post('https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent',headers={'x-goog-api-key':key},json={'contents':[{'role':'user','parts':parts}],'generationConfig':{'responseMimeType':'application/json'}},timeout=240);r.raise_for_status()
d=json.loads(''.join(x.get('text','') for x in r.json()['candidates'][0]['content']['parts']));(Q/'lipsync-windows-review.json').write_text(json.dumps(d,indent=2));print(json.dumps(d,indent=2),flush=True)
