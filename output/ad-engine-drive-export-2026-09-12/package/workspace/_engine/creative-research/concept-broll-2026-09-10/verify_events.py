import json,subprocess,io
from pathlib import Path
from fractions import Fraction
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent
requests={'C061':5.0,'C101':5.35,'C067':4.9,'C183':10.85,'C090':7.8,'C091':4.5,'C133':62.0,'C131':41.0,'C194':54.4,'C198':92.8,'C130':4.6}
rows=[]; events=[]
for aid,t in requests.items():
 p=R/'media'/aid;d=json.loads((p/'candidate-frames.json').read_text());fps=float(Fraction(d['fps'])); n=min(d['candidates'],key=lambda n:abs(n/fps-t));start=max(0,n-4)
 cmd=['ffmpeg','-v','error','-i',str(p/'source.mp4'),'-vf',f'select=between(n\\,{start}\\,{start+7}),scale=110:196','-vsync','0','-frames:v','8','-f','image2pipe','-vcodec','mjpeg','-']
 data=subprocess.check_output(cmd); parts=data.split(b'\xff\xd8')[1:]; row=Image.new('RGB',(880,234),'#101010');draw=ImageDraw.Draw(row);draw.text((4,2),f'{aid} candidate {n}, approx {n/fps:.3f}s — unverified until inspected',fill='white')
 for i,part in enumerate(parts):
  im=Image.open(io.BytesIO(b'\xff\xd8'+part));row.paste(im,(110*i,20));draw.text((110*i+2,217),f'f{start+i}',fill='white')
 out=p/'evidence'/'selected-event.jpg';row.save(out)
 rows.append(row);events.append({'candidate':aid,'requested_seconds':t,'candidate_frame':n,'source_frames':list(range(start,start+8)),'approx_seconds':n/fps,'evidence':str(out.relative_to(R))})
for k in range(0,len(rows),6):
 sheet=Image.new('RGB',(880,234*len(rows[k:k+6])))
 for j,row in enumerate(rows[k:k+6]):sheet.paste(row,(0,234*j))
 sheet.save(R/f'selected-events-{k//6+1}.jpg')
(R/'selected-events.json').write_text(json.dumps(events,indent=2))
print('Saved',len(events),'consecutive-frame windows')
