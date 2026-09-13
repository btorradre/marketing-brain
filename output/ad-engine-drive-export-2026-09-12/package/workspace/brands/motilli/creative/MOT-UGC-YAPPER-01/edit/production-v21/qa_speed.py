from pathlib import Path
import json,subprocess,concurrent.futures,re
import numpy as np
from PIL import Image,ImageDraw,ImageOps
O=Path(__file__).resolve().parent;B=O.parent/'production-v18';V=O/'deliverables/Motilli-Unbranded-VSL-v21-1.2x.mp4';old=B/'deliverables/Motilli-Unbranded-VSL-v18.mp4';Q=O/'qa';meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(V)]));(Q/'metadata.json').write_text(json.dumps(meta,indent=2));v=next(s for s in meta['streams'] if s['codec_type']=='video');assert int(v['nb_frames'])==7859 and v['width']==1080 and v['height']==1920 and v['r_frame_rate']=='30/1'
def pcm(f):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(f),'-vn','-ac','1','-ar','8000','-f','f32le','-']),np.float32)
x=pcm(old);y=pcm(V)
def envelope(a):a=a[:len(a)//80*80].reshape(-1,80);return np.sqrt(np.mean(a*a,axis=1))
a=envelope(x);b=envelope(y);ts=np.arange(len(b))*.01;best=None
for shift in np.arange(-.15,.1501,.01):
 ref=np.interp((ts+shift)*1.2,np.arange(len(a))*.01,a);c=float(np.corrcoef(ref,b)[0,1])
 if best is None or c>best['correlation']:best={'output_offset_seconds':float(shift),'correlation':c}
assert best['correlation']>.8 and abs(best['output_offset_seconds'])<.08,best
phrases=lambda f:[' '.join(b.split('\n')[2:]) for b in f.read_text().strip().split('\n\n')]
assert phrases(B/'deliverables/Motilli-Unbranded-VSL-v18.srt')==phrases(O/'deliverables/Motilli-Unbranded-VSL-v21-1.2x.srt')
ins=json.loads((B/'aligned-inserts.json').read_text());rows=[]
for i in ins:
 s=round(i['start_frame']/1.2);e=round(i['end_frame']/1.2);rows.append((i['id'],[max(0,s-1),s,(s+e)//2,e-1,e]))
rows.append(('Presenter and ending',[round(138/1.2),1500,4200,7800,7858]));frames=sorted({f for _,fs in rows for f in fs})
def grab(f):
 subprocess.run(['ffmpeg','-v','error','-y','-ss',f'{f/30:.9f}','-i',str(V),'-frames:v','1','-q:v','2','-threads','1',str(Q/f'frame-{f:05}.jpg')],check=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:list(ex.map(grab,frames))
for p in range((len(rows)+4)//5):
 rr=rows[p*5:p*5+5];im=Image.new('RGB',(1100,len(rr)*420),'#eee');d=ImageDraw.Draw(im)
 for r,(name,fs) in enumerate(rr):
  d.text((8,r*420+2),name,fill='black')
  for k,f in enumerate(fs):
   d.text((k*220+5,r*420+18),f'{f} / {f/30:.3f}s',fill='black');im.paste(ImageOps.contain(Image.open(Q/f'frame-{f:05}.jpg'),(215,380)),(k*220,r*420+36))
 im.save(Q/f'boundaries-{p+1}.jpg')
report={'fps':30,'frames':7859,'duration_seconds':7859/30,'expected_unrounded_duration':9431/30/1.2,'audio_envelope_match_to_1_2x_source':best,'caption_phrases':227,'caption_words_unchanged':True,'review_frames':frames,'visual_review':'pending','native_speed':120,'native_pitch_correction':True};(Q/'speed-qa.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
