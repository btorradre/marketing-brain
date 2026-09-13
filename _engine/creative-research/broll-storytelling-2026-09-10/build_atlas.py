from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import subprocess,io
p=Path(__file__).parent
spec=[('GChN9X','Human symptoms / presenter / payoff',[('source.mp4',14.5,'Agitation: shoulder action'),('source.mp4',80,'Mechanism: feeding action'),('source.mp4',187,'Payoff: comfortable waking')]),('FU7tkn','Car presenter with small inserts',[('original.mp4',45,'Agitation stays on face'),('original.mp4',75,'Inset explains process'),('original.mp4',153,'Presenter holds product')]),('99jcKo','Narrated protagonist and mechanism',[('source.mp4',35,'Specific human symptom'),('source.mp4',72,'Internal explanatory view'),('source.mp4',107,'Product-use sequence')]),('YIXBhp','Guided inside-body demonstration',[('source.mp4',19,'Human consequence insert'),('source.mp4',97,'Distinct solution action'),('source.mp4',144,'Behavioral payoff')])]
fontpath='/System/Library/Fonts/Supplemental/Arial.ttf'
try: big=ImageFont.truetype(fontpath,25);small=ImageFont.truetype(fontpath,20)
except: big=small=ImageFont.load_default()
w,h=240,426;gap=24;left=32;row=512
out=Image.new('RGB',(840,4*row+104),'#f1eee7');d=ImageDraw.Draw(out)
d.text((left,20),'REFERENCE STUDY — B-roll storytelling',font=big,fill='#171717');d.text((left,53),'Observed source frames; not a proposed storyboard',font=small,fill='#555')
for i,(id,title,frames) in enumerate(spec):
 y=94+i*row;d.text((left,y),f'{id}  |  {title}',font=small,fill='#171717')
 for j,(file,t,label) in enumerate(frames):
  b=subprocess.check_output(['ffmpeg','-v','error','-ss',str(t),'-i',str(p/id/file),'-frames:v','1','-vf',f'scale={w}:{h}','-f','image2pipe','-vcodec','mjpeg','-'])
  im=Image.open(io.BytesIO(b));x=left+j*(w+gap);out.paste(im,(x,y+34));d.text((x,y+465),f'{t:.1f}s | {label}',font=ImageFont.truetype(fontpath,14),fill='#333')
out.save(p/'reference-atlas.jpg',quality=93)
