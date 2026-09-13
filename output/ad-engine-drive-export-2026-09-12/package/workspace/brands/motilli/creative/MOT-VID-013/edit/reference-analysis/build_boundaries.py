from pathlib import Path
from PIL import Image,ImageDraw
import json
p=Path(__file__).resolve().parent
cuts=[108,150,195,250,285,319,358,401,422,455,536,569,626,660,687,706,756,815,860,911,935,961,1008,1048,1130,1180,1263,1321,1385,1439,1495,1542]
for offset in range(0,len(cuts),4):
 group=cuts[offset:offset+4];sheet=Image.new('RGB',(960,4*452),'#151515');d=ImageDraw.Draw(sheet)
 for row,c in enumerate(group):
  for col,i in enumerate([c-2,c-1,c,c+1]):
   x=col*240;y=row*452;sheet.paste(Image.open(p/'frames'/f'{i:04d}.jpg'),(x,y));d.text((x+3,y+430),f'f{i} | {i/25:.2f}s',fill='white')
 sheet.save(p/'sheets'/f'boundaries-{offset//4+1:02d}.jpg',quality=90)
for c in [108,285,536,706,860,1008]:
 ids=list(range(c-5,c+9));sheet=Image.new('RGB',(7*180,2*344),'#151515');d=ImageDraw.Draw(sheet)
 for n,i in enumerate(ids):
  x=n%7*180;y=n//7*344;im=Image.open(p/'frames'/f'{i:04d}.jpg');im.thumbnail((180,320));sheet.paste(im,(x,y));d.text((x+3,y+322),f'f{i} | {i/25:.2f}s',fill='white')
 sheet.save(p/'sheets'/f'transition-{c:04d}.jpg',quality=92)
(p/'candidate-boundaries.json').write_text(json.dumps(cuts));print(len(cuts),'boundaries',len(cuts)+1,'shots')
