import pathlib,json,subprocess,base64,httpx,concurrent.futures
O=pathlib.Path(__file__).resolve().parent;P=O.parents[1];root=O.parents[5];Q=O/'qa';v=P/'assets/video-v7/presenter-avatar-v.mp4';key=next(l.split('=',1)[1].strip().strip('"').strip("'") for l in (root/'.env').read_text().splitlines() if l.startswith('GEMINI_API_KEY='))
def check(t):
 f=Q/f'presenter-motion-{t}.mp4';subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(v),'-t','12','-vf','scale=720:1280','-c:v','libx264','-preset','fast','-crf','22','-threads','2','-c:a','aac',str(f)],check=True)
 prompt='Review this 12-second talking-head video with its audio as production QA. Assess lip synchronization, face/eye stability, plausible natural expression, unexpected identity/background change, and visible branding or products. Report only directly observed problems with timestamps; do not infer medical claims or judge marketing copy. Give concise JSON with usable, lipsync, visible_problems, identity_and_framing. Mild synthetic polish is acceptable; flag material distracting glitches.'
 body={'contents':[{'parts':[{'inline_data':{'mime_type':'video/mp4','data':base64.b64encode(f.read_bytes()).decode()}},{'text':prompt}]}],'generationConfig':{'temperature':0.1,'responseMimeType':'application/json'}}
 with httpx.Client(timeout=300) as c:r=c.post('https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent',headers={'x-goog-api-key':key},json=body)
 r.raise_for_status();d=r.json();text='\n'.join(x.get('text','') for c in d.get('candidates',[]) for x in c.get('content',{}).get('parts',[]));(Q/f'presenter-motion-{t}-qa.json').write_text(text);print(t,text,flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:list(ex.map(check,[0,135,267]))
