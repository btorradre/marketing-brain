from pathlib import Path
import json,subprocess,numpy as np
from PIL import Image,ImageDraw,ImageOps
O=Path(__file__).resolve().parent;Q=O/'qa';Q.mkdir(exist_ok=True);V=O/'deliverables/Motilli-Unbranded-VSL-v16.mp4';old=O.parent/'production-v12/deliverables/Motilli-Unbranded-VSL-v12.mp4'
meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(V)]));(Q/'metadata.json').write_text(json.dumps(meta,indent=2));v=next(s for s in meta['streams'] if s['codec_type']=='video');a=next(s for s in meta['streams'] if s['codec_type']=='audio');assert int(v['nb_frames'])==8327 and v['width']==1080 and v['height']==1920 and v['r_frame_rate']=='30/1';assert a['codec_name']=='aac'
frames=[0,1,48,96,97,120,143,144,145,1424,1425,1458,1490,1491,7255,7256,7301,7345,7346]
for f in frames:subprocess.run(['ffmpeg','-v','error','-y','-ss',f'{f/30:.9f}','-i',str(V),'-frames:v','1','-q:v','2',str(Q/f'frame-{f}.jpg')],check=True)
im=Image.new('RGB',(1200,2590),'#eee');d=ImageDraw.Draw(im)
for i,f in enumerate(frames):
 x=i%3*400;y=i//3*370;im.paste(ImageOps.contain(Image.open(Q/f'frame-{f}.jpg'),(195,346)),(x+100,y+20));d.text((x+90,y+3),f'Frame {f} / {f/30:.3f}s',fill='black')
im.save(Q/'square-overlays-in-context.jpg')
def pcm(f):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(f),'-vn','-ac','1','-ar','8000','-f','f32le','-']),np.float32)
a=pcm(old);b=pcm(V);assert len(a)==len(b);err=float(np.max(np.abs(a-b)));corr=float(np.corrcoef(a,b)[0,1]);assert corr>.99999
report={'duration_seconds':v['duration'],'frames':8327,'resolution':[1080,1920],'fps':30,'audio_correlation_to_v12':corr,'max_pcm_difference':err,'replacement_frames':[[0,97],[97,144],[1425,1491],[7256,7346]],'review_frames':frames,'unchanged_audio_verified':True};(Q/'revision-qa.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2),flush=True)
