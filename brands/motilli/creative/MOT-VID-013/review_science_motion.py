"""Review native clips using 4fps image evidence and Gemini 3.8 Flash."""
import base64, io, json, math, subprocess, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from PIL import Image, ImageDraw
import requests

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
OUT=HERE/'output/science-v2/motion'
QA=OUT/'qa';QA.mkdir(exist_ok=True)
KEY=next(l.split('=',1)[1].strip().strip('"').strip("'") for l in (ROOT/'.env').read_text().splitlines() if l.startswith('GEMINI_API_KEY='))

def review(s):
 sid=s['id']; dest=QA/(sid+'-review.json')
 if dest.exists():return json.loads(dest.read_text())
 video=OUT/(sid+'.mp4')
 if not video.exists():return {'shot':sid,'status':'not_ready'}
 meta=json.loads((OUT/(sid+'-ffprobe.json')).read_text());stream=next(x for x in meta['streams'] if x['codec_type']=='video');duration=float(stream['duration'])
 n=math.ceil(duration*4);sheet=Image.new('RGB',(1280,math.ceil(n/4)*598),'#202020');draw=ImageDraw.Draw(sheet)
 for i in range(n):
  t=i/4
  data=subprocess.check_output(['ffmpeg','-v','error','-ss',str(t),'-i',str(video),'-frames:v','1','-vf','scale=320:568','-f','image2pipe','-vcodec','mjpeg','-'])
  im=Image.open(io.BytesIO(data));x=(i%4)*320;y=(i//4)*598;sheet.paste(im,(x,y));draw.text((x+8,y+572),f'{sid} {t:.2f}s',fill='white')
 imagepath=QA/(sid+'-4fps.jpg');sheet.save(imagepath,quality=92)
 prompt='Review actual generated video motion evidence, not the medical claims. Image 1 is the source still. Image 2 is EVERY 0.25-second sample from the native video, row-major with timestamps. Check identity/body-size consistency, hands/objects/packaging and anatomy geometry stability, unwanted cuts or added objects, pronounced warping, changed typography, and whether the intended action occurs. Do not flag realistic motion blur or reflection changes as identity drift. For product labels, report legibility changes at exact times; do not claim to read letters too small. Anatomy is a schematic; do not certify clinical accuracy. Return JSON: shot, verdict (pass/minor_issue/revise), observed_motion, issues:[{time_s,description,severity}], safe_window_start_s, safe_window_end_s, confidence. Intended motion: '+s.get('motion','')+'; intended visual: '+s.get('visual','')+'. Shot id '+sid
 parts=[{'text':prompt},{'inlineData':{'mimeType':'image/png','data':base64.b64encode(Path(s['frame']).read_bytes()).decode()}},{'inlineData':{'mimeType':'image/jpeg','data':base64.b64encode(imagepath.read_bytes()).decode()}}]
 r=requests.post('https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent',headers={'x-goog-api-key':KEY},json={'contents':[{'role':'user','parts':parts}],'generationConfig':{'responseMimeType':'application/json'}},timeout=180)
 if r.status_code!=200:raise RuntimeError(sid+': review HTTP '+str(r.status_code))
 d=r.json();content=''.join(x.get('text','') for x in d['candidates'][0]['content']['parts']);result=json.loads(content);result.update(review_model='gemini-3.8-flash',sample_rate_fps=4,frames_sampled=n,native_duration_s=duration,evidence=str(imagepath));dest.write_text(json.dumps(result,indent=2));print(sid+': '+result.get('verdict','unknown'),flush=True);return result

if __name__=='__main__':
 plan=json.loads((HERE/'production-plan-science-v2.json').read_text());jobs=[s for s in plan['shots'] if (OUT/(s['id']+'.mp4')).exists()]
 motion=json.loads((HERE/'science-v2-revisions.json').read_text());by={s['id']:s['motion'] for s in motion['changed_scenes']}
 for s in jobs:s['motion']=by[s['id']]
 results=[]
 with ThreadPoolExecutor(max_workers=4) as pool:
  fs={pool.submit(review,s):s['id'] for s in jobs}
  for f in as_completed(fs):
   try:results.append(f.result())
   except Exception as e:print(fs[f]+': REVIEW ERROR '+str(e),flush=True)
 (QA/'summary.json').write_text(json.dumps(sorted(results,key=lambda x:x.get('shot','')),indent=2))
 print('Reviewed '+str(len(results))+' available clips',flush=True)
