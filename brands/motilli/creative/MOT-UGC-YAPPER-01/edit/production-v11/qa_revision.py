from pathlib import Path
import json,subprocess,numpy as np,concurrent.futures
from PIL import Image,ImageDraw,ImageOps
O=Path(__file__).resolve().parent;Q=O/'qa';V=O/'deliverables/Motilli-Unbranded-VSL-v11.mp4';old=O.parent/'production-v10/deliverables/Motilli-Unbranded-VSL-v10.mp4'
meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(V)]));(Q/'metadata.json').write_text(json.dumps(meta,indent=2));v=next(s for s in meta['streams'] if s['codec_type']=='video');a=next(s for s in meta['streams'] if s['codec_type']=='audio');assert int(v['nb_frames'])==8327 and v['width']==1080 and v['height']==1920 and v['r_frame_rate']=='30/1';assert a['codec_name']=='aac'
jobs=json.loads((O/'wardrobe-jobs.json').read_text());jobs += [{'asset':'community','start_frame':4197,'end_frame':4317},{'asset':'paper','start_frame':4619,'end_frame':4751}]
frames=sorted(set(f for j in jobs for f in [j['start_frame']-1,j['start_frame'],(j['start_frame']+j['end_frame'])//2,j['end_frame']-1,j['end_frame']]))
def extract(f):subprocess.run(['ffmpeg','-v','error','-y','-ss',f'{f/30:.9f}','-i',str(V),'-frames:v','1','-q:v','2',str(Q/f'frame-{f}.jpg')],check=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as e:list(e.map(extract,frames))
for chunk in range(3):
 subset=jobs[chunk*5:chunk*5+5];im=Image.new('RGB',(1250,len(subset)*460),'#eee');d=ImageDraw.Draw(im)
 for row,j in enumerate(subset):
  for col,f in enumerate([j['start_frame']-1,j['start_frame'],(j['start_frame']+j['end_frame'])//2,j['end_frame']-1,j['end_frame']]):
   x=col*250;y=row*460;im.paste(ImageOps.contain(Image.open(Q/f'frame-{f}.jpg'),(240,425)),(x+5,y+25));d.text((x+5,y+4),j['asset']+' '+str(f),fill='black')
 im.save(Q/f'final-boundaries-{chunk}.jpg')
im=Image.new('RGB',(1400,1200),'white');d=ImageDraw.Draw(im)
for i,j in enumerate(jobs[:13]):
 f=(j['start_frame']+j['end_frame'])//2;x=i%7*200;y=i//7*600;im.paste(ImageOps.contain(Image.open(Q/f'frame-{f}.jpg'),(195,540)),(x,y+25));d.text((x+3,y+4),j['asset'],fill='black')
im.save(Q/'final-wardrobe-contact.jpg')
def pcm(f):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(f),'-vn','-ac','1','-ar','8000','-f','f32le','-']),np.float32)
a=pcm(old);b=pcm(V);assert len(a)==len(b);err=float(np.max(np.abs(a-b)));corr=float(np.corrcoef(a,b)[0,1]);assert err==0
assert (O/'deliverables/Motilli-Unbranded-VSL-v11.srt').read_bytes()==(O.parent/'production-v10/deliverables/Motilli-Unbranded-VSL-v10.srt').read_bytes()
report={'duration_seconds':v['duration'],'frames':8327,'resolution':[1080,1920],'fps':30,'audio_correlation_to_v10':corr,'max_pcm_difference':err,'review_frames':frames,'unchanged_audio_verified':True,'unchanged_srt_verified':True,'lifestyle_clips_replaced':12,'new_square_cramping_overlay':True};(Q/'revision-qa.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2),flush=True)
