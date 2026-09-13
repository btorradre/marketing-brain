from pathlib import Path
import subprocess,json,concurrent.futures
import numpy as np
from PIL import Image,ImageDraw
def ssim(a,b,**kwargs):
 a=a.astype(float);b=b.astype(float);ma=a.mean();mb=b.mean();va=a.var();vb=b.var();cov=((a-ma)*(b-mb)).mean();return ((2*ma*mb+6.5025)*(2*cov+58.5225))/((ma*ma+mb*mb+6.5025)*(va+vb+58.5225))
P=Path(__file__).resolve().parent;V6=P.parent/'v6';V=P/'deliverables/Motilli-Podcast-110-percent.mp4';Q=P/'qa'
def run(args):return subprocess.run(args,capture_output=True,check=True)
def image_at(path,t):
 raw=run(['ffmpeg','-v','error','-ss',str(t),'-i',str(path),'-frames:v','1','-vf','scale=270:480','-pix_fmt','rgb24','-f','rawvideo','-']).stdout
 return np.frombuffer(raw,np.uint8).reshape((480,270,3))
def tech():
 r=json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(V)]).stdout);v=next(x for x in r['streams'] if x['codec_type']=='video');assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==(1080,1920,'30/1',5379);z=run(['ffmpeg','-v','error','-i',str(V),'-f','null','-']);assert not z.stderr;r['full_decode_pass']=True;(Q/'technical-qa.json').write_text(json.dumps(r,indent=2));print('5379 frames / 179.3 seconds; full decode passed',flush=True)
def frames():
 rows=[];sheet=Image.new('RGB',(540,505*6),'#101721');d=ImageDraw.Draw(sheet)
 for n,t in enumerate([2,28.95,45.8,89.5,135,177.5]):
  f=round(t*30);t=f/30;a=image_at(V,t);target=f*1.1;poss=[]
  for offset in [-1,0,1]:
   source=max(0,round(target)+offset)/30;b=image_at(V6/'deliverables/Motilli-Podcast-v6-Visual-Revision.mp4',source);score=ssim(a,b,channel_axis=2,data_range=255);poss.append((score,source,b))
  score,source,b=max(poss,key=lambda x:x[0]);rows.append({'output_time':t,'matched_v6_time':source,'ssim':float(score)});sheet.paste(Image.fromarray(b),(0,n*505+25));sheet.paste(Image.fromarray(a),(270,n*505+25));d.text((5,n*505+5),f'v6 {source:.3f}s -> 110% {t:.3f}s  SSIM {score:.4f}',fill='white')
  assert score>.95,rows[-1]
 sheet.save(Q/'speed-frame-comparison.jpg');(Q/'frame-correspondence.json').write_text(json.dumps(rows,indent=2));print('Beginning/middle/end frames match 1.1x source positions',flush=True)
def boardframes():
 cards=json.load(open(P/'final-coverage.json'));dest=P/'board-frames';dest.mkdir(exist_ok=True)
 def one(c):
  t=(c.get('insert_start',c['start'])+c.get('insert_end',c['end']))/2
  run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(V),'-frames:v','1',str(dest/(c['id']+'.jpg'))])
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:list(ex.map(one,cards))
 print('Updated 62 final storyboard frames',flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
 jobs=[ex.submit(f) for f in [tech,frames,boardframes]]
 for j in jobs:j.result()
