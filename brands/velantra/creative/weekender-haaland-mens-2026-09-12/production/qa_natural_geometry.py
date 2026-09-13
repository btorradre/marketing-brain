from pathlib import Path
import json,subprocess,io,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.signal import correlate,correlation_lags
P=Path(__file__).resolve().parent;R=P/'resolve-natural';Q=P/'qa-natural';Q.mkdir(exist_ok=True);v=P/'exports/Weekender-Haaland-Natural-AvatarV.mp4';M=json.loads((R/'manifest.json').read_text());S=M['scenes'];C=M['captions'];F=Q/'frames';F.mkdir(exist_ok=True)
def frame(n):
 p=F/f'{n:05d}.png'
 if not p.exists():subprocess.run(['ffmpeg','-v','error','-y','-ss',str(n/30),'-i',str(v),'-frames:v','1',str(p)],check=True)
 return Image.open(p).convert('RGB')
# Whole-file decode and every-frame low-resolution offline scan.
r=subprocess.run(['ffmpeg','-v','error','-i',str(v),'-f','null','-'],capture_output=True,text=True);assert r.returncode==0 and not r.stderr,r.stderr
raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(v),'-an','-vf','scale=64:114','-pix_fmt','rgb24','-f','rawvideo','-']);a=np.frombuffer(raw,np.uint8).reshape(-1,114,64,3);red=(a[:,:,:,0]>100)&(a[:,:,:,0]>2*a[:,:,:,1].astype(float))&(a[:,:,:,0]>2*a[:,:,:,2].astype(float));green=(a[:,:,:,1]>150)&(a[:,:,:,0]<60)&(a[:,:,:,2]<60)
scan={'file':str(v),'sha256':hashlib.sha256(v.read_bytes()).hexdigest(),'frames':len(a),'expected_frames':M['frames'],'black_frames':np.where((a.max(axis=3)<8).mean(axis=(1,2))>.98)[0].tolist(),'offline_red_frames':np.where(red.mean(axis=(1,2))>.75)[0].tolist(),'green_screen_frames':np.where(green.mean(axis=(1,2))>.15)[0].tolist()};assert len(a)==M['frames'];(Q/'frame-scan.json').write_text(json.dumps(scan,indent=2))
# Actual rendered glyph extent vs known native rectangle center, every caption + both titles.
items=[];rows=[]
for c in C:
 items.append(dict(c,frame=(c['start']+c['end'])//2,width=min(.94,.08+len(c['text'])*c['size']*.33),height=.032,dark=False))
for i,s in enumerate(S[:2]):
 y=.55 if i==0 else .64
 for text,y,width,height,dark in [('ATHLETE',y,.36,.055,False),('WEEKENDER BAG',y-.075,.69,.075,True)]:items.append({'text':text,'frame':(s['start']+s['end'])//2,'x':.5,'y':y,'width':width,'height':height,'dark':dark,'scene':s['id']})
sheet=Image.new('RGB',(1080,100*len(items)));draw=ImageDraw.Draw(sheet)
for i,c in enumerate(items):
 im=frame(c['frame']);cx=c['x']*1080;cy=(1-c['y'])*1920;w=c['width']*1080;h=c['height']*1920
 box=(round(cx-w/2)+4,round(cy-h/2)+4,round(cx+w/2)-4,round(cy+h/2)-4);a=np.asarray(im.crop(box));mask=(a.max(axis=2)<55) if c['dark'] else (a.min(axis=2)>210);yy,xx=np.where(mask);assert len(xx)>0,c
 x0,x1=box[0]+int(xx.min()),box[0]+int(xx.max());y0,y1=box[1]+int(yy.min()),box[1]+int(yy.max());dx=(x0+x1)/2-cx;dy=(y0+y1)/2-cy
 rows.append({'scene':c['scene'],'text':c['text'],'frame':c['frame'],'dx_px':round(dx,2),'dy_px':round(dy,2),'left_padding_px':round(x0-(cx-w/2),1),'right_padding_px':round(cx+w/2-x1,1),'top_padding_px':round(y0-(cy-h/2),1),'bottom_padding_px':round(cy+h/2-y1,1),'center_within_6px':abs(dx)<=6 and abs(dy)<=6})
 crop=im.crop((0,int(cy-42),1080,int(cy+42)));sheet.paste(crop,(0,i*100+16));draw.text((4,i*100),f"{c['scene']} f{c['frame']} dx={dx:.1f} dy={dy:.1f}",fill='yellow')
sheet.save(Q/'all-caption-strips.jpg');(Q/'caption-centers.json').write_text(json.dumps(rows,indent=2))
# Each actual adjacent picture frame pair, with source cue timing recorded.
for group in range(3):
 scenes=S[1+group*4:1+(group+1)*4];sheet=Image.new('RGB',(1080,500*len(scenes)));draw=ImageDraw.Draw(sheet)
 for i,s in enumerate(scenes):
  for j,n in enumerate([s['start']-1,s['start']]):
   im=frame(n);im.thumbnail((270,480));sheet.paste(im,(j*540,i*500+20));draw.text((j*540,i*500),f"{s['id']} frame {n} / {n/30:.3f}s",fill='white')
 sheet.save(Q/f'cut-pairs-{group}.jpg')
# Exact audio waveform timing compared with selected original TTS output.
def audio(p):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-vn','-ac','1','-ar','8000','-f','f32le','-']),np.float32)
a=audio(P/'voice-natural-corrected/narration-natural.mp3');b=audio(v);corr=correlate(b,a,method='fft');lag=int(correlation_lags(len(b),len(a))[np.argmax(corr)]);audioqa={'lag_ms':lag/8,'correlation':float(np.corrcoef(a,b[:len(a)])[0,1]),'speech_end':json.loads((P/'voice-natural-corrected/words.json').read_text())[-1]['end'],'picture_end':M['frames']/30};(Q/'audio-sync.json').write_text(json.dumps(audioqa,indent=2))
print({'scan':scan,'audio':audioqa,'caption_count':len(C),'title_count':4,'centering_flags':[r for r in rows if not r['center_within_6px']]})
