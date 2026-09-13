from pathlib import Path
import json,subprocess,hashlib,math
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P/'resolve-speed110';Q=P/'qa-speed110-final';Q.mkdir(exist_ok=True);F=Q/'frames';F.mkdir(exist_ok=True)
v=P/'exports/Weekender-Haaland-Gringo-Natural-AvatarV-110-NoGaps-Final.mp4';old=P/'exports/Weekender-Haaland-Gringo-Natural-AvatarV-Final.mp4';m=json.loads((R/'time-map-plan.json').read_text());K=m['keep']
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(v)]));(Q/'export-probe.json').write_text(json.dumps(probe,indent=2))
r=subprocess.run(['ffmpeg','-v','error','-i',str(v),'-f','null','-'],capture_output=True,text=True);assert r.returncode==0 and not r.stderr,r.stderr

def raw(p,w=108,h=192):
 b=subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-an','-vf',f'scale={w}:{h}','-pix_fmt','rgb24','-f','rawvideo','-']);return np.frombuffer(b,np.uint8).reshape(-1,h,w,3)
a=raw(v);b=raw(old);assert len(a)==1035
red=(a[:,:,:,0]>100)&(a[:,:,:,0]>2*a[:,:,:,1].astype(float))&(a[:,:,:,0]>2*a[:,:,:,2].astype(float));green=(a[:,:,:,1]>150)&(a[:,:,:,0]<60)&(a[:,:,:,2]<60)
scan={'frames':len(a),'sha256':hashlib.sha256(v.read_bytes()).hexdigest(),'black_frames':np.where((a.max(axis=3)<8).mean(axis=(1,2))>.98)[0].tolist(),'offline_red_frames':np.where(red.mean(axis=(1,2))>.75)[0].tolist(),'green_screen_frames':np.where(green.mean(axis=(1,2))>.15)[0].tolist(),'decode_errors':r.stderr}
(Q/'frame-scan.json').write_text(json.dumps(scan,indent=2))
def source(n):
 f=math.floor(n*1.1+.5)
 for k in K:
  if f<k['record_end']:return k['source_start']+f-k['record_start']
 return 1430
# Verify nested retime picture against previously reviewed layered export at expected source time.
rows=[]
for n,im in enumerate(a):
 expected=source(n);candidates=range(max(0,math.floor(expected)-2),min(len(b),math.ceil(expected)+3));scores=[float(np.mean((im.astype(float)-b[k])**2)) for k in candidates];j=int(np.argmin(scores));rows.append({'frame':n,'expected_source':expected,'matched_source':list(candidates)[j],'mse':scores[j]})
(Q/'source-picture-map.json').write_text(json.dumps(rows,indent=2));print('picture MSE mean/max',np.mean([x['mse'] for x in rows]),max(x['mse'] for x in rows),flush=True)
# Source scene cuts must remain sharp under retime. Expected frame is ceil(cumulative kept frames/1.1).
def mapped(f):return max(0,sum(max(0,min(f,k['source_end'])-k['source_start']) for k in K)-.5)/1.1
scenes=json.loads((P/'resolve-gringo-aligned/aligned-scenes.json').read_text())
for s in scenes:
 s['source_start']=s['start'];s['source_end']=s['end'];s['start']=math.ceil(mapped(s['start']));s['end']=math.ceil(mapped(s['end']));s['speech_end']=mapped(s['speech_end'])
scenes[-1]['end']=len(a)
(R/'aligned-scenes.json').write_text(json.dumps(scenes,indent=2))
caps=json.loads((P/'resolve-gringo-aligned/manifest.json').read_text())['captions']
for c in caps:
 c['source_start']=c['start'];c['source_end']=c['end'];c['start']=math.ceil(mapped(c['start']));c['end']=math.ceil(mapped(c['end']))
(R/'captions.json').write_text(json.dumps(caps,indent=2))

def frame(n):
 f=F/f'{n:05}.jpg'
 if not f.exists():subprocess.run(['ffmpeg','-v','error','-y','-ss',str(n/30),'-i',str(v),'-frames:v','1','-q:v','2',str(f)],check=True)
 return Image.open(f).convert('RGB')
bounds={s['start']:s['id'] for s in scenes[1:]}
for i,k in enumerate(K[1:]):
 f=math.ceil((k['record_start']-.5)/1.1);bounds[f]=bounds.get(f,'')+f' pause{i+1}'
for g in range(math.ceil(len(bounds)/6)):
 entries=list(sorted(bounds.items()))[g*6:(g+1)*6];sheet=Image.new('RGB',(540,505*len(entries)));d=ImageDraw.Draw(sheet)
 for i,(f,label) in enumerate(entries):
  for j,n in enumerate([f-1,f]):
   im=frame(n);im.thumbnail((270,480));sheet.paste(im,(j*270,i*505+25));d.text((j*270+4,i*505+4),f'{label} f{n} {n/30:.3f}s',fill='white')
 sheet.save(Q/f'cut-pairs-{g}.jpg')
frame(1034).save(Q/'last-frame.jpg')
# Every preserved caption midpoint in the new time map.
sheet=Image.new('RGB',(1080,100*len(caps)));d=ImageDraw.Draw(sheet)
for i,c in enumerate(caps):
 n=(c['start']+c['end'])//2;im=frame(n);cy=(1-c['y'])*1920;sheet.paste(im.crop((0,int(cy-42),1080,int(cy+42))),(0,i*100+16));d.text((4,i*100),f"{c['scene']} {n} {c['text']}",fill='yellow')
sheet.save(Q/'caption-strips.jpg')
# RMS silence analysis (20ms windows), treats breath noise separately from articulation gaps.
audio=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(v),'-vn','-ac','1','-ar','16000','-f','f32le','-']),np.float32);N=320;rms=np.sqrt(np.mean(audio[:len(audio)//N*N].reshape(-1,N)**2,axis=1));quiet=20*np.log10(np.maximum(rms,1e-9)) < -38;spans=[];start=None
for i,q in enumerate(np.r_[quiet,False]):
 if q and start is None:start=i
 if not q and start is not None:
  if i-start>=8:spans.append({'start':start*.02,'end':i*.02,'duration':(i-start)*.02})
  start=None
(Q/'silence-rms.json').write_text(json.dumps({'threshold_dbfs':-38,'window_ms':20,'spans_over_160ms':spans,'max_peak':float(abs(audio).max())},indent=2))
print({'scan':scan,'quiet_spans':spans,'scenes':len(scenes),'captions':len(caps)},flush=True)
