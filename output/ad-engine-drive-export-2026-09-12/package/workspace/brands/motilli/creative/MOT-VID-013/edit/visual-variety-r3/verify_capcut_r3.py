from pathlib import Path
import json,subprocess,hashlib,concurrent.futures
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent;C=R/'capcut';Q=C/'qa';Q.mkdir(exist_ok=True)
projects=json.loads((C/'projects.json').read_text());schedule=json.loads((R/'native-picture-segments.json').read_text())
def frame(src,at,w=216,h=384):
 return subprocess.check_output(['ffmpeg','-v','error','-ss',f'{at:.6f}','-i',str(src),'-frames:v','1','-vf',f'scale={w}:{h}','-f','rawvideo','-pix_fmt','rgb24','-'])
def pcm(src):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(src),'-vn','-ac','1','-ar','16000','-f','f32le','-']),dtype=np.float32)
report=[]
for pr in projects:
 v=pr['variant'];src=C/'exports'/f'MOT-VID-013-Hook-{v}-R3.mp4'
 if not src.exists():continue
 ref=R.parent/'hook-variations/exports'/f'MOT-VID-013-Hook-{v}.mp4'
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(src)]));video=next(s for s in probe['streams'] if s['codec_type']=='video')
 assert (video['codec_name'],video['width'],video['height'],video['nb_frames'],video['r_frame_rate'])==('h264',1080,1920,'2877','30/1'),video
 dec=subprocess.run(['ffmpeg','-v','error','-i',str(src),'-f','null','-'],capture_output=True,text=True);assert dec.returncode==0 and not dec.stderr,dec.stderr
 a=pcm(src);b=pcm(ref);assert len(a)==len(b),(len(a),len(b));corr=float(np.corrcoef(a,b)[0,1]);assert corr>.999
 err=float(np.max(np.abs(a-b)));hook=[]
 for at in [.5,3.5]:
  f=np.frombuffer(frame(src,at),np.uint8).astype(float);g=np.frombuffer(frame(ref,at),np.uint8).astype(float);mae=float(np.mean(np.abs(f-g)));assert mae<1.5,(v,at,mae);hook.append({'time':at,'mean_rgb_difference':mae})
 r={'variant':v,'file':str(src.resolve()),'frames':video['nb_frames'],'duration_seconds':float(video['duration']),'full_decode':'pass','audio_correlation_with_original':corr,'audio_max_abs_sample_delta':err,'hook_comparisons':hook,'sha256':hashlib.sha256(src.read_bytes()).hexdigest()};report.append(r);print(v,'technical QA passed',flush=True)
 if v=='A':
  def sample(item):
   i,s=item;at=(s['start']+s['end'])/2;im=Image.frombytes('RGB',(216,384),frame(src,at));return i,s,im
  with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:samples=list(ex.map(sample,enumerate(schedule)))
  for pg in range(5):
   canvas=Image.new('RGB',(864,828),'#111111');draw=ImageDraw.Draw(canvas)
   for j,(i,s,im) in enumerate(samples[pg*8:(pg+1)*8]):
    x=(j%4)*216;y=(j//4)*414;canvas.paste(im,(x,y));draw.text((x+5,y+388),f'{i+1:02} {s["start"]:.2f}-{s["end"]:.2f}s',fill='white')
   canvas.save(Q/f'A-scenes-{pg+1}.jpg')
  # Consecutive output frames at every cut. Actual decoded native output, not source proxies.
  boundaries=[]
  def pair(item):
   i,s=item;f=round(s['start']*30);times=[(f-1)/30,f/30];ims=[Image.frombytes('RGB',(144,256),frame(src,t,144,256)) for t in times];return i,s,ims
  with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:boundaries=list(ex.map(pair,list(enumerate(schedule))[1:]))
  for pg in range(5):
   canvas=Image.new('RGB',(1152,572),'#111111');draw=ImageDraw.Draw(canvas)
   for j,(i,s,ims) in enumerate(boundaries[pg*8:(pg+1)*8]):
    x=(j%4)*288;y=(j//4)*286
    for k,im in enumerate(ims):canvas.paste(im,(x+k*144,y))
    draw.text((x+4,y+260),f'Cut {i}: {s["start"]:.3f}s',fill='white')
   canvas.save(Q/f'A-boundaries-{pg+1}.jpg')
(Q/'technical-qa.json').write_text(json.dumps(report,indent=2));print('Saved technical QA and actual-export scene/boundary sheets.',flush=True)
