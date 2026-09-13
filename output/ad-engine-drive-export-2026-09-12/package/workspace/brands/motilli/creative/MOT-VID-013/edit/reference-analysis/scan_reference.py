import subprocess,json,hashlib
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;ROOT=P.parents[5];SRC=ROOT/'_engine/mcp/ad-engine/data/downloads/job_d78559811694/source.mp4'
frames=P/'frames';frames.mkdir(exist_ok=True);sheets=P/'sheets';sheets.mkdir(exist_ok=True)
W,H=240,426;proc=subprocess.Popen(['ffmpeg','-v','error','-i',str(SRC),'-vf',f'scale={W}:{H}','-pix_fmt','rgb24','-f','rawvideo','-'],stdout=subprocess.PIPE)
prev=None;scores=[];index=0;samples=[]
while True:
 data=proc.stdout.read(W*H*3)
 if len(data)!=W*H*3:break
 a=np.frombuffer(data,dtype=np.uint8).reshape(H,W,3)
 if prev is not None:
  delta=np.abs(a.astype(np.float32)-prev.astype(np.float32)).mean(axis=2)
  scores.append({'frame':index,'time_s':index/25,'diff':round(float(delta.mean()),3),'upper_diff':round(float(delta[:220].mean()),3),'lower_diff':round(float(delta[335:].mean()),3)})
 Image.fromarray(a).save(frames/f'{index:04d}.jpg',quality=88)
 if index%12==0:samples.append(index)
 prev=a.copy();index+=1
proc.wait()
for offset in range(0,len(samples),16):
 ids=samples[offset:offset+16];sheet=Image.new('RGB',(W*4,(H+26)*4),'#151515');draw=ImageDraw.Draw(sheet)
 for n,i in enumerate(ids):
  x=n%4*W;y=n//4*(H+26);sheet.paste(Image.open(frames/f'{i:04d}.jpg'),(x,y));draw.text((x+5,y+H+5),f'{i/25:.2f}s / f{i}',fill='white')
 sheet.save(sheets/f'overview-{offset//16+1:02d}.jpg',quality=90)
(P/'frame-differences.json').write_text(json.dumps(scores,indent=2))
(P/'source-probe.json').write_bytes(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(SRC)]))
(P/'provenance.json').write_text(json.dumps({'source':str(SRC),'sha256':hashlib.sha256(SRC.read_bytes()).hexdigest(),'frames_decoded':index,'fps':25,'video_duration_s':index/25,'overview_sample_interval_frames':12,'method':'Every source frame decoded and differenced; visual overview every 12 frames; cut boundary frames inspected separately.'},indent=2))
print(json.dumps({'frames':index,'sheets':len(list(sheets.glob('overview*'))),'candidates':[s for s in scores if s['diff']>20 or s['upper_diff']>25]}),flush=True)
