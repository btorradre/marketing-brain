import json,subprocess,io
from pathlib import Path
from PIL import Image,ImageDraw
p=Path(__file__).resolve().parent;q=p/'qa';q.mkdir(exist_ok=True);t=json.loads((p/'timing.json').read_text());src=p/'exports/MOT-VID-013-R2-A.mp4'
items=[(s['id'],(s['start_frame']+s['end_frame'])/60) for s in t['shots']]
items += [('remedy',f/30+.15) for f in t['remedy_cut_frames'][:-1]]+ [('closing',s) for s in [93.2,94.2,95.3,95.75]]
for page in range((len(items)+14)//15):
 batch=items[page*15:(page+1)*15];sheet=Image.new('RGB',(5*216,((len(batch)+4)//5)*414),'#111111');draw=ImageDraw.Draw(sheet)
 for i,(label,at) in enumerate(batch):
  data=subprocess.check_output(['ffmpeg','-v','error','-ss',str(at),'-i',str(src),'-frames:v','1','-vf','scale=216:384','-f','image2pipe','-vcodec','mjpeg','-']);x=i%5*216;y=i//5*414;sheet.paste(Image.open(io.BytesIO(data)),(x,y));draw.text((x+5,y+389),f'{label} {at:.2f}s',fill='white')
 sheet.save(q/f'contact-{page+1}.jpg')
print('Contact sheets complete',flush=True)
