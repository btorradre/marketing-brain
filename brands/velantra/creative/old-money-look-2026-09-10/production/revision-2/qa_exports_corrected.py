import json,subprocess,hashlib
from pathlib import Path
import numpy as np,cv2
from PIL import Image,ImageDraw
from scipy.signal import correlate,correlation_lags
p=Path('/Users/brooksorradre2/Documents/marketing brain/brands/velantra/creative/old-money-look-2026-09-10/production');r=p/'revision-2';qa=r/'qa/final';qa.mkdir(exist_ok=True)
manifest=json.loads((r/'resolve/manifest.json').read_text())
def audio(f):return np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',str(f),'-vn','-ac','1','-ar','48000','-f','f32le','-'],capture_output=True,check=True).stdout,dtype=np.float32)
report={}
for ad in manifest:
 name=ad['name'];src=r/'exports'/(name+'.mp4');cap=cv2.VideoCapture(str(src));n=int(cap.get(7));fps=cap.get(5);assert (n,fps,int(cap.get(3)),int(cap.get(4)))==(ad['duration_frames'],30,1080,1920),(name,n,fps)
 d=json.loads(Path(ad['otio']).read_text());clips=d['tracks']['children'][0]['children'];frames=[]
 while True:
  ok,f=cap.read()
  if not ok:break
  frames.append(cv2.cvtColor(cv2.resize(f,(192,342)),cv2.COLOR_BGR2RGB))
 frames=np.array(frames);assert len(frames)==n
 black=np.flatnonzero(frames.mean(axis=(1,2,3))<8).tolist();assert not black,(name,'black',black)
 holds=[];coverage=[]
 for c in clips:
  md=c['metadata'];a,b=md['record_in'],md['record_out'];ref=c['media_references']['DEFAULT_MEDIA']['target_url'];coverage.append([a,b,md['beat_id']])
  if ref.endswith('.png'):
   x=frames[a:b].astype(np.float32);deviations=np.abs(x-x[len(x)//2]).mean(axis=(1,2,3));mx=float(deviations.max());assert mx<4,(name,md['beat_id'],'moving/flash frame',mx)
   im=np.array(Image.open(ref).convert('RGB').resize((192,342)));err=float(np.abs(x[len(x)//2]-im).mean());holds.append({'beat':md['beat_id'],'frames':b-a,'max_change_mae':mx,'source_mae':err});assert err<22,(name,md['beat_id'],'source mismatch',err)
 # Every boundary side plus one midpoint and final frame; actual decoded render.
 picks=sorted(set([0,n-1]+[v for a,b,bid in coverage for v in [a,max(a,b-1),(a+b)//2]]));cols=8;rows=(len(picks)+cols-1)//cols;sheet=Image.new('RGB',(cols*192,rows*364),'#111');draw=ImageDraw.Draw(sheet)
 for i,f in enumerate(picks):
  x=i%cols*192;y=i//cols*364;sheet.paste(Image.fromarray(frames[f]),(x,y+22));draw.text((x+4,y+3),f'{f} / {f/30:.3f}s',fill='white')
 sheet.save(qa/(name+'-boundaries.jpg'),quality=94)
 # Per-frame bridge and sole motion insert, sheet previews for consecutive visual inspection.
 moving=[(a,b,bid) for a,b,bid in coverage if bid in ['bridge','C09']];out=qa/name;out.mkdir(exist_ok=True);records=[]
 for a,b,bid in moving:
  for j,start in enumerate(range(a,b,36)):
   end=min(start+36,b);s=Image.new('RGB',(1152,2184),'#111');dr=ImageDraw.Draw(s)
   for k,f in enumerate(range(start,end)):
    x=k%6*192;y=k//6*364;s.paste(Image.fromarray(frames[f]),(x,y+22));dr.text((x+3,y+3),str(f),fill='white')
   path=out/(bid+f'-{j:02d}.jpg');s.save(path,quality=90);records.append({'file':str(path),'in':start,'out':end,'inspected':False})
 (out/'coverage.json').write_text(json.dumps(records,indent=2))
 a=audio(src);b=audio(p/'exports'/(ad['original_id']+'.mp4'));checks=[]
 for sec in [1,10,20,30,40,47]:
  x=a[sec*48000:(sec+2)*48000:4];y=b[sec*48000:(sec+2)*48000:4];length=min(len(x),len(y));x=x[:length]-x[:length].mean();y=y[:length]-y[:length].mean();corr=correlate(x,y,method='fft');lags=correlation_lags(length,length);use=np.flatnonzero(np.abs(lags)<600);i=use[np.argmax(corr[use])];val=float(corr[i]/(np.linalg.norm(x)*np.linalg.norm(y)));lag=float(lags[i]/12000);checks.append({'seconds':sec,'correlation':val,'offset_seconds':lag});assert val>.98 and abs(lag)<.003,(name,'audio',checks[-1])
 report[name]={'frames':n,'fps':fps,'resolution':[1080,1920],'black_frames':black,'still_hold_checks':holds,'audio_vs_approved_V1':checks,'audio_peak_dbfs':float(20*np.log10(max(1e-9,np.abs(a).max()))),'bytes':src.stat().st_size,'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'machine_checked_every_frame':True,'visual_inspection':'pending contact sheets and boundary review'}
 (qa/'report.json').write_text(json.dumps(report,indent=2));print(name,'PASS',n,'frames; still holds & audio preserved',flush=True)
