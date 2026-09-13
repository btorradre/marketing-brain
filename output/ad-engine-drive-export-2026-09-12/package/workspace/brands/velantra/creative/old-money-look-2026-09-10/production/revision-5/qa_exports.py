"""Caption revision QA: full decode, audio preservation and actual scene frames."""
from pathlib import Path
import json,subprocess,hashlib,time
import cv2,numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent;Q=R/'qa/final';Q.mkdir(exist_ok=True)
B=R/'board-assets';B.mkdir(exist_ok=True)
ads=json.loads((R/'resolve/manifest.json').read_text())
old=json.loads((R.parent/'revision-4/resolve/manifest.json').read_text())
beats=json.loads((R/'resolve/beat-map.json').read_text());report={}
def audio(p):
 return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-vn','-ac','1','-ar','16000','-f','f32le','-']),np.float32)
for ad,prior in zip(ads,old):
 assert ad['captions']==prior['captions']
 name=ad['name'];h=ad['hook'];path=R/'exports'/(name+'.mp4')
 deadline=time.monotonic()+1800
 while True:
  probe=subprocess.run(['ffprobe','-v','error','-show_entries','stream=nb_frames','-of','json',str(path)],capture_output=True,text=True)
  if probe.returncode==0:
   streams=json.loads(probe.stdout).get('streams',[])
   if streams and streams[0].get('nb_frames')==str(ad['duration_frames']):break
  assert time.monotonic()<deadline,'Export wait exceeded'
  time.sleep(5)
 cap=cv2.VideoCapture(str(path));n=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
 assert (n,cap.get(5),int(cap.get(3)),int(cap.get(4)))==(ad['duration_frames'],30,1080,1920)
 picks={0,n-1,beats[h]['reveal']-1,beats[h]['reveal']}
 for row in beats[h]['rows']:picks.update([row['in'],(row['in']+row['out'])//2])
 for c in ad['captions']:picks.add((c['in']+c['out'])//2)
 thumbs={};black=[];count=0
 while True:
  ok,f=cap.read()
  if not ok:break
  small=cv2.cvtColor(cv2.resize(f,(216,384)),cv2.COLOR_BGR2RGB)
  if small.mean()<8:black.append(count)
  if count in picks:thumbs[count]=small
  count+=1
 assert count==n and not black
 sheets=[]
 for page,start in enumerate(range(0,len(picks),24)):
  chosen=sorted(picks)[start:start+24];im=Image.new('RGB',(1296,1632),'#151515');draw=ImageDraw.Draw(im)
  for j,f in enumerate(chosen):
   x=j%6*216;y=j//6*408;im.paste(Image.fromarray(thumbs[f]),(x,y+24));draw.text((x+4,y+4),f'{f} / {f/30:.3f}s',fill='white')
  p=Q/(name+f'-scenes-{page}.jpg');im.save(p,quality=94);sheets.append(str(p))
 def photo(f,name):
  cap.set(cv2.CAP_PROP_POS_FRAMES,f);ok,frame=cap.read();assert ok
  cv2.imwrite(str(B/name),frame,[cv2.IMWRITE_JPEG_QUALITY,96])
 photo(0,name+'-hook.jpg')
 if ad['avatar']=='A1':photo(beats[h]['reveal'],h+'-bridge.jpg')
 if ad['id']=='VEL-OM-H1-A1':
  for row in beats[h]['rows'][1:]:photo(row['in'],row['id']+'.jpg')
 a=audio(path);b=audio(R.parent/'revision-4/exports'/(prior['name']+'.mp4'))
 assert abs(len(a)-len(b))<=1024
 size=min(len(a),len(b))//320*320
 ea=np.sqrt(np.mean(a[:size].reshape(-1,320)**2,axis=1));eb=np.sqrt(np.mean(b[:size].reshape(-1,320)**2,axis=1))
 corr=float(np.corrcoef(ea,eb)[0,1]);assert corr>.998,(name,corr)
 comps=sorted((R/'resolve/comps').glob(name+'-caption-*.comp'));assert len(comps)==len(ad['captions'])
 for p in comps:
  s=p.read_text();assert 'TextPlus {' in s and 'Thickness2 = Input { Value = 0.055' in s
  assert 'Size = Input { Value = 0.09' in s
  assert all(x not in s for x in ['Background {','RectangleMask {','Merge {','DropShadow {'])
 cap.release()
 report[name]={'frames':n,'resolution':[1080,1920],'fps':30,'decoded_every_frame':True,'black_frames':black,'r4_audio_envelope_correlation':corr,'exact_r4_caption_timing_and_wording':True,'outline_only_graphs_verified':len(comps),'scene_sheets':sheets,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'visual_review_complete':False}
 (Q/'report.json').write_text(json.dumps(report,indent=2));print(name,'PASS audio',corr,flush=True)
