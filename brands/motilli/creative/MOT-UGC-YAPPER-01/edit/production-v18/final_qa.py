from pathlib import Path
import json,subprocess,re,concurrent.futures
import numpy as np
from PIL import Image,ImageDraw,ImageOps
O=Path(__file__).resolve().parent;Q=O/'qa/final';Q.mkdir(exist_ok=True);V=O/'deliverables/Motilli-Unbranded-VSL-v18.mp4'
meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(V)]));(Q/'metadata.json').write_text(json.dumps(meta,indent=2));v=next(s for s in meta['streams'] if s['codec_type']=='video');a=next(s for s in meta['streams'] if s['codec_type']=='audio');assert int(v['nb_frames'])==9431 and v['width']==1080 and v['height']==1920 and v['r_frame_rate']=='30/1';assert a['codec_name']=='aac'
ins=json.loads((O/'aligned-inserts.json').read_text());rows=[]
for i in ins:
 s=round(i['start']*30);e=round(i['end']*30);rows.append((i['id']+' '+i['asset'],[max(0,s-1),s,(s+e)//2,e-1,e]))
rows.append(('Presenter and ending',[138,2400,4500,8700,9430]))
frames=sorted(set(f for _,fs in rows for f in fs))
def grab(f):
 out=Q/f'frame-{f:05}.jpg';subprocess.run(['ffmpeg','-v','error','-y','-ss',f'{f/30:.9f}','-i',str(V),'-frames:v','1','-q:v','2','-threads','1',str(out)],check=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:list(ex.map(grab,frames))
for page in range((len(rows)+4)//5):
 rr=rows[page*5:page*5+5];im=Image.new('RGB',(1100,len(rr)*422),'#eee');d=ImageDraw.Draw(im)
 for j,(name,fs) in enumerate(rr):
  d.text((10,j*422+2),name,fill='black')
  for k,f in enumerate(fs):
   im.paste(ImageOps.contain(Image.open(Q/f'frame-{f:05}.jpg'),(215,382)),(k*220,j*422+36));d.text((k*220+5,j*422+19),f'{f} | {f/30:.3f}s',fill='black')
 im.save(Q/f'boundaries-{page+1}.jpg')
def pcm(f):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(f),'-vn','-ac','1','-ar','8000','-f','f32le','-']),np.float32)
x=pcm(O/'narration-master-resolve.mov');y=pcm(V);n=min(len(x),len(y));corr=float(np.corrcoef(x[:n],y[:n])[0,1]);assert corr>.995,corr;assert abs(len(x)-len(y))/8000<.05
srt=lambda f:[re.sub(r'\s+',' ',b.split('\n',2)[2]).strip() for b in f.read_text().strip().split('\n\n')]
old=srt(O.parent/'production-v16/deliverables/Motilli-Unbranded-VSL-v16.srt');new=srt(O/'deliverables/Motilli-Unbranded-VSL-v18.srt');assert old==new;assert len(new)==227
report={'resolution':[1080,1920],'fps':30,'frames':9431,'duration_seconds':314.366666667,'caption_phrases':len(new),'caption_wording_unchanged':True,'audio_correlation_to_native_voice_master':corr,'audio_difference_rms':float(np.sqrt(np.mean((x[:n]-y[:n])**2))),'audio_length_difference_seconds':(len(y)-len(x))/8000,'comparison_note':'Final AAC versus PCM voice master; codec differences expected, not sample identical.','covering_scenes':len(ins),'boundary_review_frames':frames,'contact_pages':(len(rows)+4)//5,'visual_review':'pending direct inspection'}
(Q/'revision-qa.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2),flush=True)
