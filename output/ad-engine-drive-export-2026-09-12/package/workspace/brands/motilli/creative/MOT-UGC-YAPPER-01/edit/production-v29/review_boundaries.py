from pathlib import Path
import cv2,json
from PIL import Image,ImageDraw
O=Path(__file__).resolve().parent;h='H1';s=json.loads((O/h/'timeline-spec.json').read_text());v=O/f'deliverables/Motilli-VSL-V29-{h}-NUORA-STYLE-1.2x.mp4';c=cv2.VideoCapture(str(v));events=[]
for r in s['rows']:
 if r['track']==2 and (r['name'].startswith('N') or r['name'] in ['HOOK-couch-hook','B11-group-post','B12-apigenin-research']):
  events.extend([{'name':r['name']+' in','frame':r['start']},{'name':r['name']+' out','frame':r['end']}])
for page in range((len(events)+7)//8):
 batch=events[page*8:page*8+8];im=Image.new('RGB',(960,570),'#222222');d=ImageDraw.Draw(im)
 for i,e in enumerate(batch):
  x=i%4*240;y=i//4*285;d.text((x+2,y+4),e['name']+' '+str(e['frame']),fill='white')
  for j,f in enumerate([e['frame']-1,e['frame']]):
   c.set(cv2.CAP_PROP_POS_FRAMES,f);ok,b=c.read();assert ok;pic=Image.fromarray(cv2.cvtColor(b,cv2.COLOR_BGR2RGB));pic.thumbnail((120,250));im.paste(pic,(x+j*120,y+25))
 im.save(O/'qa'/f'final-cut-pairs-{page+1}.jpg')
(O/'qa/final-cut-pairs.json').write_text(json.dumps(events,indent=2));print('Saved',len(events),'consecutive-frame boundary pairs')
