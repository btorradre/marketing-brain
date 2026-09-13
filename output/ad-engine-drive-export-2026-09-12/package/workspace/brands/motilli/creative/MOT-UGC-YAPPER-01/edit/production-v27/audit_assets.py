from pathlib import Path
import json,subprocess,concurrent.futures
from PIL import Image,ImageDraw,ImageOps
O=Path(__file__).resolve().parent;assets=json.loads((O/'approved-inserts-baseline.json').read_text())
def work(a):
 p=Path(a['path']);assert p.exists(),p;m=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]));a['metadata']=m;t=(a.get('source_start_frame',0)+min(30,(a['end_frame']-a['start_frame'])//2))/30;out=O/f"qa/source-{a['asset']}.jpg";subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(p),'-frames:v','1','-vf','scale=320:-1','-threads','1',str(out)],check=True);a['audit_frame']=str(out);return a
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as e:assets=list(e.map(work,assets))
(O/'asset-audit.json').write_text(json.dumps(assets,indent=2))
for part in range(3):
 group=assets[part*9:part*9+9];im=Image.new('RGB',(960,3*400),'#ddd');d=ImageDraw.Draw(im)
 for i,a in enumerate(group):
  x=(i%3)*320;y=(i//3)*400;d.text((x+5,y+5),a['asset'],fill='black');thumb=ImageOps.contain(Image.open(a['audit_frame']),(310,370));im.paste(thumb,(x+(320-thumb.width)//2,y+25))
 im.save(O/f'qa/asset-sheet-{part+1}.jpg')
print('Verified source files and extracted',len(assets),'review frames')
