from pathlib import Path
import cv2,json,numpy as np
from PIL import Image,ImageDraw
O=Path(__file__).resolve().parent
for id in ['NU021','NU027','NU105']:
 cap=cv2.VideoCapture(str(O/(id+'.mp4')));fps=cap.get(cv2.CAP_PROP_FPS);scores=[];prev=None;i=0
 while True:
  ok,frame=cap.read()
  if not ok:break
  im=cv2.resize(frame,(90,160));g=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY).astype(float)
  if prev is not None:
   diff=np.abs(g-prev);score=float(np.mean(diff));frac=float(np.mean(diff>35));
   if score>24 and frac>.28:scores.append({'frame':i,'time':i/fps,'difference':score,'fraction':frac})
  prev=g;i+=1
 cap.release();filtered=[]
 for r in scores:
  if not filtered or r['frame']-filtered[-1]['frame']>3:filtered.append(r)
  elif r['difference']>filtered[-1]['difference']:filtered[-1]=r
 (O/f'{id}-cut-candidates.json').write_text(json.dumps({'fps':fps,'total_frames':i,'candidates':filtered},indent=2));cap=cv2.VideoCapture(str(O/(id+'.mp4')))
 for page in range((len(filtered)+11)//12):
  s=Image.new('RGB',(6*180,4*180),'#333333');d=ImageDraw.Draw(s)
  for k,r in enumerate(filtered[page*12:page*12+12]):
   for j,f in enumerate([r['frame']-1,r['frame']]):
    cap.set(cv2.CAP_PROP_POS_FRAMES,f);ok,im=cap.read();assert ok;im=cv2.cvtColor(im,cv2.COLOR_BGR2RGB);im=Image.fromarray(im);im.thumbnail((90,160));x=k%6*180+j*90;y=k//6*180;s.paste(im,(x,y+20));d.text((x+2,y+2),str(f),fill='white')
  s.crop((0,0,1080,360)).save(O/f'{id}-boundaries-{page+1}.jpg')
 cap.release();print(id,'candidates',len(filtered),flush=True)
