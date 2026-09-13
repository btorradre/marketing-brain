from pathlib import Path
import subprocess,json,hashlib
import numpy as np
from PIL import Image,ImageDraw
p=Path(__file__).parent
p.joinpath('frames').mkdir(exist_ok=True);p.joinpath('sheets').mkdir(exist_ok=True)
meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p/'source.mp4')]))
(p/'probe.json').write_text(json.dumps(meta,indent=2))
w,h=180,320;fps=25
proc=subprocess.Popen(['ffmpeg','-v','error','-i',str(p/'source.mp4'),'-vf',f'scale={w}:{h}','-pix_fmt','rgb24','-f','rawvideo','-'],stdout=subprocess.PIPE)
prev=None;scores=[];i=0
while True:
 b=proc.stdout.read(w*h*3)
 if len(b)!=w*h*3:break
 a=np.frombuffer(b,np.uint8).reshape(h,w,3)
 if prev is not None:
  d=np.abs(a.astype(float)-prev.astype(float));scores.append({'frame':i,'diff':round(float(d.mean()),2),'top':round(float(d[:150].mean()),2),'bottom':round(float(d[250:].mean()),2)})
 Image.fromarray(a).save(p/'frames'/f'{i:05}.jpg',quality=88)
 prev=a;i+=1
proc.wait()
(p/'scores.json').write_text(json.dumps(scores))
ids=list(range(0,i,25))
for st in range(0,len(ids),40):
 img=Image.new('RGB',(w*8,(h+22)*5),'#151515');dr=ImageDraw.Draw(img)
 for j,n in enumerate(ids[st:st+40]):
  x=j%8*w;y=j//8*(h+22);img.paste(Image.open(p/'frames'/f'{n:05}.jpg'),(x,y));dr.text((x+3,y+h+3),f'{n/fps:.2f}s f{n}',fill='white')
 img.save(p/'sheets'/f'overview-{st//40+1:02}.jpg',quality=92)
c=[s for s in scores if s['diff']>17 or s['top']>22 or s['bottom']>28]
(p/'candidates.json').write_text(json.dumps(c,indent=2))
for st in range(0,len(c),20):
 img=Image.new('RGB',(w*8,(h+22)*5),'#151515');dr=ImageDraw.Draw(img)
 for j,s in enumerate(c[st:st+20]):
  for z,n in enumerate([s['frame']-1,s['frame']]):
   x=(j%4*2+z)*w;y=j//4*(h+22);img.paste(Image.open(p/'frames'/f'{n:05}.jpg'),(x,y));dr.text((x+3,y+h+3),f'{n/fps:.2f} f{n}',fill='white')
 img.save(p/'sheets'/f'boundaries-{st//20+1:02}.jpg',quality=92)
(p/'provenance.json').write_text(json.dumps({'source':'https://app.trendtrack.io/share/ads/resilia-GChN9X','frames':i,'fps':fps,'sha256':hashlib.sha256((p/'source.mp4').read_bytes()).hexdigest(),'candidate_count':len(c),'review':'All frames decoded; manual review scope recorded separately in analysis.md'},indent=2))
print(i,len(c),flush=True)
