"""Decoded export QA and actual-frame storyboard previews; never changes the edit."""
from pathlib import Path
import sys,json,subprocess,hashlib
import cv2,numpy as np
from PIL import Image,ImageDraw
from scipy.signal import correlate,correlation_lags
R=Path(__file__).resolve().parent;P=R.parent;Q=R/'qa/final';Q.mkdir(exist_ok=True)
B=R/'board-assets';B.mkdir(exist_ok=True)
ads=json.loads((R/'resolve/manifest.json').read_text())
maps=json.loads((P/'resolve/deadspace-applied-map.json').read_text())
def audio(path):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-vn','-ac','1','-ar','12000','-f','f32le','-']),np.float32)
def photo(cap,n,path):
 cap.set(cv2.CAP_PROP_POS_FRAMES,n);ok,f=cap.read();assert ok;cv2.imwrite(str(path),f,[cv2.IMWRITE_JPEG_QUALITY,94])
report=json.loads((Q/'report.json').read_text()) if (Q/'report.json').exists() else {}
for ad in ads:
 name=ad['name']
 if len(sys.argv)>1 and name!=sys.argv[1]:continue
 src=R/'exports'/(name+'.mp4');cap=cv2.VideoCapture(str(src))
 n=int(cap.get(cv2.CAP_PROP_FRAME_COUNT));fps=cap.get(cv2.CAP_PROP_FPS)
 assert (n,fps,int(cap.get(3)),int(cap.get(4)))==(ad['duration_frames'],30,1080,1920),(name,n,fps)
 d=json.loads(Path(ad['otio']).read_text());bg=d['tracks']['children'][0]['children'];frames=[]
 while True:
  ok,f=cap.read()
  if not ok:break
  frames.append(cv2.cvtColor(cv2.resize(f,(216,384)),cv2.COLOR_BGR2RGB))
 frames=np.array(frames);assert len(frames)==n
 black=np.flatnonzero(frames.mean(axis=(1,2,3))<8).tolist();assert not black
 picks={0,n-1}
 for c in bg:
  a=c['metadata']['record_in'];b=c['metadata']['record_out'];picks.update([a,max(a,b-1),(a+b)//2])
 for c in ad['captions']:picks.update([max(0,c['in']-1),c['in']])
 # One sheet per 24 actual export frames; every base/caption boundary sampled.
 records=[]
 for j,start in enumerate(range(0,len(picks),24)):
  chosen=sorted(picks)[start:start+24];im=Image.new('RGB',(1296,1632),'#111');dr=ImageDraw.Draw(im)
  for i,f in enumerate(chosen):
   x=i%6*216;y=i//6*408;im.paste(Image.fromarray(frames[f]),(x,y+24));dr.text((x+3,y+4),f'{f} / {f/30:.3f}s',fill='white')
  out=Q/(name+f'-boundaries-{j}.jpg');im.save(out,quality=94);records.append({'file':str(out),'frames':chosen,'visually_inspected':False})
 # Exact regenerated source correspondence around each retained interval and each base cut.
 native=cv2.VideoCapture(str(R/'avatars'/ad['id']/'avatar-native.mp4'));nativefps=native.get(cv2.CAP_PROP_FPS)
 samples=sorted({0,n-2,*[c['metadata']['record_in'] for c in bg],*[min(n-2,c['metadata']['record_out']) for c in bg]})
 z,pan,tilt=(.54,-248.4,-485) if ad['avatar']=='A3' else (.46,-291.6,-550)
 ox=540+pan-540*z;oy=960-tilt-960*z
 sy1,sy2=(700,1100) if ad['avatar']=='A3' else (500,1000);sx1,sx2=400,700
 dx1,dx2=round(ox+sx1*z),round(ox+sx2*z);dy1,dy2=round(oy+sy1*z),round(oy+sy2*z)
 checks=[]
 for f in samples:
  cursor=0;expected=None
  for a,b in maps[ad['hook']]['keep']:
   if cursor<=f<cursor+b-a:expected=(a+f-cursor)/30;break
   cursor+=b-a
  assert expected is not None
  cap.set(cv2.CAP_PROP_POS_FRAMES,f);ok,render=cap.read();assert ok
  wanted=cv2.resize(cv2.cvtColor(render[dy1:dy2,dx1:dx2],cv2.COLOR_BGR2GRAY),(60,80))
  best=(-1,None)
  for sn in range(max(0,round(expected*nativefps)-3),round(expected*nativefps)+4):
   native.set(cv2.CAP_PROP_POS_FRAMES,sn);ok,frame=native.read()
   if not ok:continue
   got=cv2.resize(cv2.cvtColor(frame[sy1:sy2,sx1:sx2],cv2.COLOR_BGR2GRAY),(60,80))
   score=float(cv2.matchTemplate(got,wanted,cv2.TM_CCOEFF_NORMED)[0,0])
   if score>best[0]:best=(score,sn)
  checks.append({'frame':f,'expected_source_s':expected,'best_source_frame':best[1],'correlation':best[0],'matched_offset_s':best[1]/nativefps-expected})
 native.release()
 # Selected narration unchanged versus completed prior approved output.
 a=audio(src);b=audio(P/'revision-2/exports'/(ad['id']+'-R2.mp4'));acs=[]
 for sec in [1,10,20,30,40,47]:
  x=a[sec*12000:(sec+2)*12000];y=b[sec*12000:(sec+2)*12000];size=min(len(x),len(y));x=x[:size]-x[:size].mean();y=y[:size]-y[:size].mean();c=correlate(x,y,method='fft');lags=correlation_lags(size,size);ix=np.flatnonzero(np.abs(lags)<600);i=ix[np.argmax(c[ix])];val=float(c[i]/(np.linalg.norm(x)*np.linalg.norm(y)));lag=float(lags[i]/12000);acs.append({'seconds':sec,'correlation':val,'offset_s':lag});assert val>.98 and abs(lag)<.003,(name,acs[-1])
 photo(cap,0,B/(name+'-hook.jpg'))
 if ad['avatar']=='A1':
  bridge={'H1':110,'H2':139,'H3':137}[ad['hook']];photo(cap,bridge,B/(ad['hook']+'-bridge.jpg'))
 if ad['id']=='VEL-OM-H1-A1':
  for c in bg[1:]:photo(cap,c['metadata']['record_in'],B/(c['metadata']['beat_id']+'.jpg'))
 cap.release()
 entry={'frames':n,'fps':fps,'resolution':[1080,1920],'black_frames':black,'decoded_every_frame':True,'source_presenter_checks':checks,'source_check_min_correlation':min(v['correlation'] for v in checks),'audio_vs_approved':acs,'boundary_sheets':records,'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'bytes':src.stat().st_size,'music':'Selected voice retained; reference bed not copied; no qualified alternate bed found.'}
 report[name]=entry;(Q/'report.json').write_text(json.dumps(report,indent=2));print(name,'decoded/audio pass; presenter min',entry['source_check_min_correlation'],flush=True)
