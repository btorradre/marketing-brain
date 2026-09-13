from pathlib import Path
import json,subprocess,concurrent.futures
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;V=P/'deliverables/Motilli-Podcast-No-Dead-Space.mp4';Q=P/'qa';K=json.load(open(P/'keep-ranges.json'))
def run(args):return subprocess.run(args,capture_output=True,check=True)
def technical():
 r=json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(V)]).stdout);v=next(x for x in r['streams'] if x['codec_type']=='video');assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==(1080,1920,'30/1',4882);z=run(['ffmpeg','-v','error','-i',str(V),'-f','null','-']);assert not z.stderr;(Q/'technical-qa.json').write_text(json.dumps(r,indent=2));print('4882 frames / 162.733 seconds, full decode passed',flush=True)
def audio():
 def load(v):return np.frombuffer(run(['ffmpeg','-v','error','-i',str(v),'-vn','-ar','48000','-ac','1','-f','f32le','-']).stdout,np.float32)
 a=load(P/'intermediate/title-corrected-110-percent.mp4');b=load(V);parts=[a[c['source_start']*1600:c['source_end']*1600] for c in K];x=np.concatenate(parts);n=min(len(x),len(b));corr=float(np.corrcoef(x[:n],b[:n])[0,1]);assert corr>.97,corr
 # Find residual contiguous low-level pauses, excluding leading/trailing padding.
 f=b[:4882*1600].reshape(4882,1600);db=20*np.log10(np.maximum(np.sqrt(np.mean(f*f,axis=1)),1e-9));quiet=db<-34;st=None;long=[]
 for i,q in enumerate(np.append(quiet,False)):
  if q and st is None:st=i
  if not q and st is not None:
   if i-st>=7:long.append([st/30,i/30,(i-st)/30])
   st=None
 r={'source_keep_range_audio_correlation':corr,'residual_quiet_gaps_over_233ms':long,'cut_count':75,'removed_seconds':497/30};(Q/'audio-qa.json').write_text(json.dumps(r,indent=2));print('Audio correlation',corr,'residual long quiet gaps',long,flush=True)
def pictures():
 (P/'board-frames').mkdir(exist_ok=True);cards=json.load(open(P/'final-coverage.json'))
 def frame(c):
  t=(c.get('insert_start',c['start'])+c.get('insert_end',c['end']))/2;run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(V),'-frames:v','1',str(P/'board-frames'/(c['id']+'.jpg'))])
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:list(ex.map(frame,cards))
 bd=Q/'boundaries';bd.mkdir(exist_ok=True);cuts=[r['start'] for r in K[1:]]
 def cutframe(cut):run(['ffmpeg','-v','error','-y','-ss',str((cut-1)/30),'-i',str(V),'-frames:v','3',str(bd/f'{cut}-%02d.jpg')])
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:list(ex.map(cutframe,cuts))
 for off in range(0,len(cuts),12):
  group=cuts[off:off+12];sheet=Image.new('RGB',(1080,math.ceil(len(group)/3)*215),'#101721');d=ImageDraw.Draw(sheet)
  for j,cut in enumerate(group):
   x=(j%3)*360;y=(j//3)*215;d.text((x+4,y+2),f'Join {cut} / {cut/30:.2f}s',fill='white')
   for z in range(3):
    im=Image.open(bd/f'{cut}-{z+1:02d}.jpg');im.thumbnail((110,195));sheet.paste(im,(x+z*115,y+18))
  sheet.save(Q/f'cut-review-{off//12}.jpg')
 print('62 board frames and 74 consecutive cut triplets saved',flush=True)
import math
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
 jobs=[ex.submit(f) for f in [technical,audio,pictures]]
 for j in jobs:j.result()
