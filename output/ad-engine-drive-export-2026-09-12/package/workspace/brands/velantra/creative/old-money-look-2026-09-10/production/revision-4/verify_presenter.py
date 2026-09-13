"""Read-only full decode, retime/source verification, caption/cut contact sheets."""
from pathlib import Path
import sys,json,subprocess,hashlib
import cv2,numpy as np
from PIL import Image,ImageDraw
from scipy.signal import correlate,find_peaks
R=Path(__file__).resolve().parent;P=R.parent;Q=R/'qa/final';Q.mkdir(exist_ok=True);B=R/'board-assets';B.mkdir(exist_ok=True)
ads=json.loads((R/'resolve/manifest.json').read_text());maps=json.loads((R/'resolve/deadspace-applied-map.json').read_text());beats=json.loads((R/'resolve/beat-map.json').read_text())
def audio(path):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-vn','-ac','1','-ar','16000','-f','f32le','-']),np.float32)
def pitch(x,t):
 s=x[max(0,int((t-.03)*16000)):int((t+.03)*16000)]
 if len(s)<800:return None
 s=s-s.mean();y=correlate(s,s,mode='full',method='fft')[len(s)-1:];peaks=find_peaks(y[40:180])[0]+40
 if not len(peaks) or np.sqrt(np.mean(s*s))<.025:return None
 lag=max(peaks,key=lambda i:y[i]);return 16000/lag if y[lag]/y[0]>.6 else None
def source_sec(f,h):
 for s in maps[h]['segments']:
  if s['in']<=f<s['out']:return (s['source_in']+(f-s['in'])*1.1)/30
 raise ValueError(f)
def photo(cap,n,path):
 cap.set(cv2.CAP_PROP_POS_FRAMES,n);ok,f=cap.read();assert ok;cv2.imwrite(str(path),f,[cv2.IMWRITE_JPEG_QUALITY,94])
report=json.loads((Q/'report.json').read_text()) if (Q/'report.json').exists() else {}
for ad in ads:
 name=ad['name'];h=ad['hook'];src=R/'exports'/(name+'.mp4');cap=cv2.VideoCapture(str(src));n=ad['duration_frames'];rows=beats[h]['rows']
 native=cv2.VideoCapture(str(P/'revision-3/avatars'/ad['id']/'avatar-native.mp4'));nativefps=native.get(cv2.CAP_PROP_FPS)
 samples=sorted({0,n-2,*[v['in'] for v in rows],*[min(n-2,v['in']) for v in maps[h]['segments']]})
 checks=[]
 for f in samples:
  expected=source_sec(f,h)
  z,pan,tilt=(.54,-248.4,-485) if ad['avatar']=='A3' else (.46,-291.6,-550)
  if f<beats[h]['reveal']:z,pan,tilt=(.30,-378,-710) if ad['avatar']=='A3' else (.28,-388.8,-691.2)
  ox=540+pan-540*z;oy=960-tilt-960*z
  # Forehead/eye/mouth region ends before the bottom caption backing.
  sy1,sy2=(700,1100) if ad['avatar']=='A3' else (500,1000);sx1,sx2=400,700
  dx1,dx2=round(ox+sx1*z),round(ox+sx2*z);dy1,dy2=round(oy+sy1*z),round(oy+sy2*z)
  cap.set(cv2.CAP_PROP_POS_FRAMES,f);ok,render=cap.read();assert ok
  wanted=cv2.resize(cv2.cvtColor(render[dy1:dy2,dx1:dx2],cv2.COLOR_BGR2GRAY),(60,80));best=(-1,None)
  for sn in range(max(0,round(expected*nativefps)-3),round(expected*nativefps)+4):
   native.set(cv2.CAP_PROP_POS_FRAMES,sn);ok,frame=native.read()
   if not ok:continue
   got=cv2.resize(cv2.cvtColor(frame[sy1:sy2,sx1:sx2],cv2.COLOR_BGR2GRAY),(60,80));score=float(cv2.matchTemplate(got,wanted,cv2.TM_CCOEFF_NORMED)[0,0])
   if score>best[0]:best=(score,sn)
  checks.append({'frame':f,'expected_source_s':expected,'best_source_frame':best[1],'correlation':best[0],'matched_offset_s':best[1]/nativefps-expected})
 native.release()

 cap.release();report[name]['source_presenter_checks']=checks;report[name]['source_check_min_correlation']=min(v['correlation'] for v in checks)
 print(name,report[name]['source_check_min_correlation'],flush=True)
(Q/'report.json').write_text(json.dumps(report,indent=2))
