from pathlib import Path
import json,subprocess,numpy as np
from PIL import Image,ImageDraw,ImageOps
O=Path(__file__).resolve().parent;Q=O/'qa';Q.mkdir(exist_ok=True);V=O/'deliverables/Motilli-Unbranded-VSL-v8.mp4';old=O.parent/'production-v7/deliverables/Motilli-Unbranded-VSL-v7.mp4'
meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(V)]));(Q/'metadata.json').write_text(json.dumps(meta,indent=2));v=next(s for s in meta['streams'] if s['codec_type']=='video');a=next(s for s in meta['streams'] if s['codec_type']=='audio');assert int(v['nb_frames'])==8327 and v['width']==1080 and v['height']==1920 and v['r_frame_rate']=='30/1';assert a['codec_name']=='aac'
frames=[4196,4197,4205,4257,4316,4317]
for f in frames:subprocess.run(['ffmpeg','-v','error','-y','-ss',f'{f/30:.9f}','-i',str(V),'-frames:v','1','-q:v','2',str(Q/f'frame-{f}.jpg')],check=True)
im=Image.new('RGB',(1200,740),'#eee');d=ImageDraw.Draw(im)
for i,f in enumerate(frames):
 x=i%3*400;y=i//3*370;im.paste(ImageOps.contain(Image.open(Q/f'frame-{f}.jpg'),(195,346)),(x+100,y+20));d.text((x+90,y+3),f'Frame {f} / {f/30:.3f}s',fill='black')
im.save(Q/'post-in-context.jpg')
def pcm(f):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(f),'-vn','-ac','1','-ar','8000','-f','f32le','-']),np.float32)
a=pcm(old);b=pcm(V);assert len(a)==len(b);err=float(np.max(np.abs(a-b)));corr=float(np.corrcoef(a,b)[0,1]);assert corr>.99999
report={'duration_seconds':v['duration'],'frames':8327,'resolution':[1080,1920],'fps':30,'audio_correlation_to_v7':corr,'max_pcm_difference':err,'replacement_frames':[4197,4317],'review_frames':frames,'unchanged_audio_verified':True};(Q/'revision-qa.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2),flush=True)
