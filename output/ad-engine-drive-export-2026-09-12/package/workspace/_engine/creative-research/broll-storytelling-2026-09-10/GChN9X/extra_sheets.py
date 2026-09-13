from pathlib import Path
from PIL import Image,ImageDraw
p=Path(__file__).parent;w,h=180,320
sets={'intermediate':list(range(12,5900,25)),'transitions':list(range(795,863))+list(range(2220,2256))+list(range(3251,3271))+list(range(3652,3670))+list(range(4238,4263))+list(range(4280,4303))+list(range(4365,4388))}
for name,ids in sets.items():
 for st in range(0,len(ids),40):
  img=Image.new('RGB',(w*8,(h+22)*5),'#111');d=ImageDraw.Draw(img)
  for j,n in enumerate(ids[st:st+40]):
   x=j%8*w;y=j//8*(h+22);img.paste(Image.open(p/'frames'/f'{n:05}.jpg'),(x,y));d.text((x+2,y+h+2),f'{n/25:.2f}s f{n}',fill='white')
  img.save(p/'sheets'/f'{name}-{st//40+1:02}.jpg',quality=90)
