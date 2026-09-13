from pathlib import Path
import json,subprocess,concurrent.futures
from PIL import Image,ImageOps,ImageDraw
O=Path(__file__).resolve().parent;J=O/'tiktok-sourcing';D=J/'screening';vs=[v for v in sorted((J/'candidates/B17').glob('*.mp4')) if not (D/(v.stem+'-0.jpg')).exists()]
def row(v):
 dur=float(json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(v)]))['format']['duration']);fs=[]
 for i,t in enumerate([.1,dur*.3,dur*.6,dur*.85]):
  f=D/(v.stem+f'-{i}.jpg');subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(v),'-frames:v','1','-vf','scale=180:-2','-threads','1',str(f)],check=True);fs.append(f)
 return v.stem,fs
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:rows=list(ex.map(row,vs))
for page in range((len(rows)+5)//6):
 rr=rows[page*6:page*6+6];im=Image.new('RGB',(800,360*len(rr)),'#ddd');d=ImageDraw.Draw(im)
 for k,(id,fs) in enumerate(rr):
  d.text((5,k*360+3),id,fill='black')
  for i,f in enumerate(fs):im.paste(ImageOps.contain(Image.open(f),(195,335)),(i*200,k*360+23))
 im.save(D/f'round2-page-{page+1}.jpg')
print('New screening sheets',len(rows))
