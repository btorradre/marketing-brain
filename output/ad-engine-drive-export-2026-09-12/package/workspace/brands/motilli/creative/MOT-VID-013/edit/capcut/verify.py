import json,subprocess,io,hashlib,base64
from pathlib import Path
from PIL import Image,ImageDraw
import requests
p=Path(__file__).resolve().parent;root=p.parents[5];src=p/'exports/MOT-VID-013-A.mp4';qa=p/'qa';qa.mkdir(exist_ok=True)
caps=json.loads((p/'captions.json').read_text())
for page in range(4):
 sub=caps[page*24:(page+1)*24];sheet=Image.new('RGB',(270*6,510*4),'#202020');dr=ImageDraw.Draw(sheet)
 for i,c in enumerate(sub):
  t=(c['start']+c['end'])/2;data=subprocess.check_output(['ffmpeg','-v','error','-ss',str(t),'-i',str(src),'-frames:v','1','-vf','scale=270:480','-f','image2pipe','-vcodec','mjpeg','-']);x=i%6*270;y=i//6*510;sheet.paste(Image.open(io.BytesIO(data)),(x,y));dr.text((x+8,y+485),f'{page*24+i+1}  {t:.2f}s',fill='white')
 sheet.save(qa/f'captions-{page+1}.jpg',quality=94)
 print('Caption sheet '+str(page+1),flush=True)
# Consecutive output frames around all four effect boundaries.
for index,t in enumerate([4.533333,52.8,65.5,78.866667]):
 sheet=Image.new('RGB',(240*7,456*2),'#202020');dr=ImageDraw.Draw(sheet)
 for i in range(14):
  at=t+(i-7)/30;data=subprocess.check_output(['ffmpeg','-v','error','-ss',str(at),'-i',str(src),'-frames:v','1','-vf','scale=240:426','-f','image2pipe','-vcodec','mjpeg','-']);x=i%7*240;y=i//7*456;sheet.paste(Image.open(io.BytesIO(data)),(x,y));dr.text((x+5,y+432),f'{at:.3f}s',fill='white')
 sheet.save(qa/f'blur-{index+1}.jpg',quality=93)
preview=qa/'A-analysis.mp4';subprocess.run(['ffmpeg','-v','error','-y','-i',str(src),'-vf','scale=480:854','-c:v','libx264','-preset','fast','-crf','29','-c:a','aac','-b:a','96k',str(preview)],check=True)
print('Full-video QA submitting',flush=True)
key=next(l.split('=',1)[1].strip().strip('"').strip("'") for l in (root/'.env').read_text().splitlines() if l.startswith('GEMINI_API_KEY='))
prompt='Review this actual final edited 96.63-second vertical Motilli ad end to end. You are reviewing execution, not inventing medical validation or licensing. Science illustrations should cover body/ingredient explanation, people should occur only for the imagined everyday-life payoff. Inspect scene-to-spoken-line matching, caption synchronization/legibility/cropping, organ geometry/cut continuity, product visibility, packaging consistency, exactly two green heart gummies in main pack shots, missing-media/black frames, cut/transition glitches, audio and the CTA ending. On-screen text is intentionally short phrase captions plus labels; do not call a caption omitted merely because one sampled frame misses its timing. Reference style uses brief horizontal blur resets, otherwise hard cuts. Return JSON: verdict(pass/revise), strongest_execution_points, issues[{time_s,description,severity,evidence}], caption_review, picture_audio_matching, transitions, product_and_CTA_review, audio_review, limitations. Report only observable problems with timestamps, no speculative compliance warnings.'
r=requests.post('https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent',headers={'x-goog-api-key':key},json={'contents':[{'role':'user','parts':[{'text':prompt},{'inlineData':{'mimeType':'video/mp4','data':base64.b64encode(preview.read_bytes()).decode()},'videoMetadata':{'fps':4}}]}],'generationConfig':{'responseMimeType':'application/json'}},timeout=240)
if r.status_code!=200:raise RuntimeError('Video QA HTTP '+str(r.status_code))
d=r.json();j=json.loads(''.join(x.get('text','') for x in d['candidates'][0]['content']['parts']));(qa/'full-video-review.json').write_text(json.dumps(j,indent=2));print(json.dumps(j),flush=True)
