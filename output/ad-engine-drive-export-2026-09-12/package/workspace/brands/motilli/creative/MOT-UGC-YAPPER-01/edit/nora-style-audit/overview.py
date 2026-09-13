from pathlib import Path
import subprocess,json
from PIL import Image,ImageDraw
O=Path(__file__).resolve().parent
for id in ['NU021','NU027','NU105']:
 p=O/(id+'.mp4');meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]));(O/(id+'-metadata.json')).write_text(json.dumps(meta,indent=2));duration=float(meta['format']['duration']);frames=O/id;frames.mkdir(exist_ok=True);step=5
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(p),'-vf',f'fps=1/{step},scale=180:320:force_original_aspect_ratio=decrease,pad=180:320:(ow-iw)/2:(oh-ih)/2','-q:v','4',str(frames/'frame-%04d.jpg')],check=True)
 ims=sorted(frames.glob('frame-*.jpg'))
 for page in range((len(ims)+23)//24):
  batch=ims[page*24:page*24+24];s=Image.new('RGB',(6*180,4*340),'#333333');d=ImageDraw.Draw(s)
  for i,f in enumerate(batch):x=i%6*180;y=i//6*340;s.paste(Image.open(f),(x,y+20));d.text((x+3,y+3),f'{id} ~{(page*24+i)*step+step/2:.1f}s',fill='white')
  s.save(O/f'{id}-overview-{page+1}.jpg')
 print(id,'duration',duration,'sheets',(len(ims)+23)//24,flush=True)
