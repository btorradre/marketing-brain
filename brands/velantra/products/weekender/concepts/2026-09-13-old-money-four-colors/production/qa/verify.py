from pathlib import Path
import json,subprocess,numpy as np,hashlib
from PIL import Image,ImageDraw
b=Path(__file__).resolve().parents[2];q=b/'production/qa';f=b/'production/exports/Weekender-OldMoney-FourColors-Final.mp4';m=b/'production/source/original-master.mp4'
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(f)]));(q/'final-probe.json').write_text(json.dumps(probe,indent=2));vs=next(s for s in probe['streams'] if s['codec_type']=='video');assert int(vs['nb_frames'])==1539,vs.get('nb_frames')
def frames(p):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-vf','scale=180:320','-pix_fmt','rgb24','-f','rawvideo','-']),dtype=np.uint8).reshape(-1,320,180,3)
x=frames(f);y=frames(m);e=np.abs(x[358:].astype(float)-y[358:].astype(float)).mean((1,2,3));assert e.max()<3,float(e.max())
def audio(p):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-vn','-ac','1','-ar','16000','-f','f32le','-']),dtype=np.float32)
a=audio(f);c=audio(m);n=min(len(a),len(c));corr=float(np.corrcoef(a[:n],c[:n])[0,1]);assert corr>.999,corr
black=(x.mean((1,2,3))<3).nonzero()[0].tolist();assert not black
ids=[0,82,83,109,110,162,163,234,235,302,303,357,358,427,467,566,664,788,856,965,1037,1060,1084,1193,1353,1468,1534,1538]
for batch,start in enumerate(range(0,len(ids),12)):
 part=ids[start:start+12];im=Image.new('RGB',(720,1035),'#161616');draw=ImageDraw.Draw(im)
 for j,i in enumerate(part):
  ox=(j%4)*180;oy=(j//4)*345;im.paste(Image.fromarray(x[i]),(ox,oy+25));draw.text((ox+3,oy+6),f'f{i} / {i/30:.3f}s',fill='white')
 im.save(q/f'final-audit-{batch}.jpg',quality=94)
receipt={'frames':len(x),'fps':30,'duration':len(x)/30,'resolution':[vs['width'],vs['height']],'body_frames_compared':len(x)-358,'body_mae_mean_255':float(e.mean()),'body_mae_max_255':float(e.max()),'audio_correlation':corr,'audio_samples':len(a),'source_audio_samples':len(c),'black_frames':black,'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'decode':'all1539 frames decoded','scope':'All frame comparison plus separate manual composite/boundary review; metrics are not a listening assessment.'};(q/'final-qa.json').write_text(json.dumps(receipt,indent=2));print(json.dumps(receipt,indent=2),flush=True)
beats=json.load(open(b/'edit/beats.json'));dest=b/'storyboard/final-composites';dest.mkdir(exist_ok=True)
for z in beats:
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(f),'-vf',f"select=eq(n\\,{z['in']})",'-frames:v','1','-q:v','2',str(dest/(z['id']+'.jpg'))],check=True)
subprocess.run(['ffmpeg','-v','error','-y','-i',str(f),'-frames:v','1',str(q/'final-first-frame.png')],check=True)
print('14 final composites and opening PNG extracted',flush=True)
