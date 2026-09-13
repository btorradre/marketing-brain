import cv2,sys,json,math
from pathlib import Path
from PIL import Image,ImageDraw
src=Path(sys.argv[1]); out=Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=True)
cap=cv2.VideoCapture(str(src)); fps=cap.get(cv2.CAP_PROP_FPS); n=0; sheet=None; records=[]
while True:
 ok,f=cap.read()
 if not ok:break
 if n%36==0:
  sheet=Image.new('RGB',(1440,2688),'#111111'); d=ImageDraw.Draw(sheet)
 im=Image.fromarray(cv2.cvtColor(f,cv2.COLOR_BGR2RGB)); im.thumbnail((240,426))
 k=n%36; x=k%6*240;y=k//6*448
 sheet.paste(im,(x,y+22));d.text((x+4,y+4),f'{n:04d} | {n/fps:.3f}s',fill='white')
 n+=1
 if n%36==0:
  p=out/f'batch-{(n-1)//36:03d}.jpg';sheet.save(p,quality=90);records.append({'path':str(p),'in':n-36,'out':n,'inspected':False})
if n%36:
 p=out/f'batch-{n//36:03d}.jpg';sheet.save(p,quality=90);records.append({'path':str(p),'in':n//36*36,'out':n,'inspected':False})
(out/'coverage.json').write_text(json.dumps({'source':str(src),'fps':fps,'frames':n,'batches':records},indent=2));print(n,len(records))
