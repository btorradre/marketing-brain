from pathlib import Path
import json,subprocess,io,hashlib
import numpy as np
from PIL import Image,ImageDraw
p=Path(__file__).resolve().parent;qa=p/'qa';qa.mkdir(exist_ok=True);report=[];sheet=Image.new('RGB',(972,602*3),'#111111');draw=ImageDraw.Draw(sheet)
def frame(src,at,w,h):return subprocess.check_output(['ffmpeg','-v','error','-ss',str(at),'-i',str(src),'-frames:v','1','-vf',f'scale={w}:{h}','-f','rawvideo','-pix_fmt','rgb24','-'])
def pcm(src):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(src),'-vn','-ac','1','-ar','16000','-f','f32le','-']),dtype=np.float32)
for row,pr in enumerate(json.loads((p/'projects.json').read_text())):
 v=pr['variant'];src=p/'exports'/f'MOT-VID-013-Hook-{v}.mp4';ref=p.parent/'capcut-r2/exports'/f'MOT-VID-013-R2-{v}.mp4';probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(src)]));video=next(s for s in probe['streams'] if s['codec_type']=='video');assert (video['codec_name'],video['width'],video['height'],video['nb_frames'],video['r_frame_rate'])==('h264',1080,1920,'2877','30/1');subprocess.run(['ffmpeg','-v','error','-i',str(src),'-f','null','-'],check=True,capture_output=True)
 a=pcm(src);b=pcm(ref);assert len(a)==len(b);corr=float(np.corrcoef(a,b)[0,1]);assert corr>.999
 comparisons=[]
 for at in [.5,3.5,5.1,18,35,54,68,84,94.1]:
  f=frame(src,at,108,192);g=frame(ref,at,108,192);err=float(np.mean(np.abs(np.frombuffer(f,dtype=np.uint8).astype(float)-np.frombuffer(g,dtype=np.uint8).astype(float))));assert err<1,(v,at,err);comparisons.append({'time':at,'mean_rgb_error_255':err})
 for col,at in enumerate([.5,3.5,5.1]):
  im=Image.frombytes('RGB',(324,576),frame(src,at,324,576));sheet.paste(im,(col*324,row*602));draw.text((col*324+8,row*602+580),f'{v} · {at:.1f}s · '+('Shared body' if col==2 else f'Hook shot {col+1}'),fill='white')
 r={'variant':v,'project':pr['name'],'file':str(src),'picture_duration':float(video['duration']),'full_decode':'pass','audio_correlation_with_approved_R2':corr,'picture_comparisons':comparisons,'sha256':hashlib.sha256(src.read_bytes()).hexdigest()};report.append(r);print(v,'verified',flush=True)
sheet.save(qa/'hook-comparison.jpg');(qa/'verification.json').write_text(json.dumps(report,indent=2));print('All hook duplicates match accepted R2 edits',flush=True)
