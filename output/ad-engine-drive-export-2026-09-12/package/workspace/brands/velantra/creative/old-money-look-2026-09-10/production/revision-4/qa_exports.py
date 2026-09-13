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
 name=ad['name'];h=ad['hook'];src=R/'exports'/(name+'.mp4')
 if len(sys.argv)>1 and name!=sys.argv[1]:continue
 cap=cv2.VideoCapture(str(src));n=int(cap.get(cv2.CAP_PROP_FRAME_COUNT));fps=cap.get(cv2.CAP_PROP_FPS)
 assert (n,fps,int(cap.get(3)),int(cap.get(4)))==(ad['duration_frames'],30,1080,1920),(name,n,fps)
 frames=[]
 while True:
  ok,f=cap.read()
  if not ok:break
  frames.append(cv2.cvtColor(cv2.resize(f,(216,384)),cv2.COLOR_BGR2RGB))
 frames=np.array(frames);assert len(frames)==n
 black=np.flatnonzero(frames.mean(axis=(1,2,3))<8).tolist();assert not black
 rows=beats[h]['rows'];picks={0,n-1}
 for row in rows:picks.update([max(0,row['in']-1),row['in'],row['out']-1,(row['in']+row['out'])//2])
 for c in ad['captions']:picks.update([max(0,c['in']-1),c['in']])
 records=[]
 for j,start in enumerate(range(0,len(picks),24)):
  chosen=sorted(picks)[start:start+24];im=Image.new('RGB',(1296,1632),'#111');dr=ImageDraw.Draw(im)
  for i,f in enumerate(chosen):
   x=i%6*216;y=i//6*408;im.paste(Image.fromarray(frames[f]),(x,y+24));dr.text((x+3,y+4),f'{f} / {f/30:.3f}s',fill='white')
  out=Q/(name+f'-boundaries-{j}.jpg');im.save(out,quality=93);records.append({'file':str(out),'frames':chosen,'visually_inspected':False})
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
 a=audio(src);orig=audio(P/'voice'/h/'narration.wav');rat=[]
 for t in np.arange(.15,n/30-.15,.04):
  x=pitch(orig,source_sec(t*30,h));y=pitch(a,t)
  if x and y and .8<y/x<1.25:rat.append(y/x)
 pitchratio=float(np.median(rat));assert .97<pitchratio<1.03,(name,pitchratio)
 # All three presenter variations must render the same selected narration.
 ahash=hashlib.sha256(a.tobytes()).hexdigest()
 other=next((e for nm,e in report.items() if nm.startswith('VEL-OM-'+h) and nm!=name),None)
 audio_match=None
 if other:
  other_name=next(nm for nm,e in report.items() if e is other);refaudio=audio(R/'exports'/(other_name+'.mp4'));size=min(len(a),len(refaudio))//320*320
  env1=np.sqrt(np.mean(a[:size].reshape(-1,320)**2,axis=1));env2=np.sqrt(np.mean(refaudio[:size].reshape(-1,320)**2,axis=1));audio_match=float(np.corrcoef(env1,env2)[0,1]);assert audio_match>.998,(name,audio_match)

 silence=subprocess.run(['ffmpeg','-v','info','-i',str(src),'-af','silencedetect=noise=-44dB:d=0.22','-f','null','-'],capture_output=True,text=True,check=True)
 detected=[x for x in silence.stderr.splitlines() if 'silence_duration:' in x]
 photo(cap,0,B/(name+'-hook.jpg'))
 if ad['avatar']=='A1':photo(cap,beats[h]['reveal'],B/(h+'-bridge.jpg'))
 if ad['id']=='VEL-OM-H1-A1':
  for row in rows[1:]:photo(cap,row['in'],B/(row['id']+'.jpg'))
 cap.release()
 entry={'frames':n,'fps':fps,'resolution':[1080,1920],'black_frames':black,'decoded_every_frame':True,'source_presenter_checks':checks,'source_check_min_correlation':min(v['correlation'] for v in checks),'native_speed':1.1,'pitch_ratio_median':pitchratio,'pitch_samples':len(rat),'decoded_audio_sha256':ahash,'same_hook_audio_envelope_correlation':audio_match,'remaining_quiet_intervals_over_220ms':detected,'boundary_sheets':records,'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'bytes':src.stat().st_size,'reveal_frame':beats[h]['reveal']}
 report[name]=entry;(Q/'report.json').write_text(json.dumps(report,indent=2));print(name,'decoded; pitch',pitchratio,'presenter min',entry['source_check_min_correlation'],'quiet',len(detected),flush=True)
