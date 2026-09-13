import pathlib,json,subprocess,concurrent.futures
from PIL import Image,ImageDraw,ImageFont
O=pathlib.Path(__file__).resolve().parent;G=O/'graphics';G.mkdir(exist_ok=True);caps=json.loads((O/'caption-cues.json').read_text());font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',52)
jobs=[]
for c in caps:
 im=Image.new('RGBA',(1080,1920));d=ImageDraw.Draw(im);lines=[];line=''
 for word in c['text'].split():
  s=(line+' '+word).strip()
  if d.textlength(s,font=font)>760 and line:lines.append(line);line=word
  else:line=s
 if line:lines.append(line)
 assert len(lines)<=2,c
 for i,line in enumerate(lines):
  y=1350+i*65;w=d.textlength(line,font=font);d.rounded_rectangle((540-w/2-15,y-8,540+w/2+15,y+54),radius=5,fill=(255,255,255,255));d.text((540,y),line,font=font,anchor='mt',fill=(5,5,5,255))
 src=G/f"caption-{c['id']:03d}.png";im.save(src);dst=src.with_suffix('.mov');n=c['end_frame']-c['start_frame'];c.update(image_path=str(src),path=str(dst));jobs.append((src,dst,n))
for ins in json.loads((O/'aligned-inserts.json').read_text()):
 if ins['type']=='overlay':jobs.append((pathlib.Path(ins['path']),G/(ins['asset']+'.mov'),ins['end_frame']-ins['start_frame']))
def encode(job):
 src,dst,n=job
 if dst.exists():return
 subprocess.run(['ffmpeg','-v','error','-y','-loop','1','-framerate','30','-i',str(src),'-frames:v',str(n),'-an','-c:v','qtrle','-pix_fmt','argb','-threads','1',str(dst)],check=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:list(ex.map(encode,jobs))
(O/'caption-cues.json').write_text(json.dumps(caps,indent=2,ensure_ascii=False));print('Prepared',len(caps),'caption media and six static overlays',flush=True)
