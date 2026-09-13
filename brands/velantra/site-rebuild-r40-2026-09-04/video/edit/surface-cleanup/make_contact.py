"""Build first, middle and last frame review sheets from completed film renders."""
import argparse,json
from pathlib import Path
from PIL import Image,ImageDraw
p=argparse.ArgumentParser();p.add_argument('family');a=p.parse_args()
r=next(r for r in json.loads(Path('shots.json').read_text()) if r['family']==a.family)
root=Path('qa')/(a.family+'-export')
for offset in range(0,len(r['shots']),4):
 shots=r['shots'][offset:offset+4]
 out=Image.new('RGB',(1920,382*len(shots)),'white');d=ImageDraw.Draw(out)
 for row,s in enumerate(shots):
  for col,i in enumerate([s['start'],s['anchor'],s['end']-1]):
   f=root/f"shot-{s['number']:02d}-frame-{i:04d}.jpg"
   im=Image.open(f);im.thumbnail((640,360));out.paste(im,(col*640,row*382+22))
   d.text((col*640+6,row*382+4),f"{a.family} shot {s['number']} frame {i}",fill='black')
 out.save(Path('qa')/f'{a.family}-contact-{offset//4+1}.jpg',quality=94)
