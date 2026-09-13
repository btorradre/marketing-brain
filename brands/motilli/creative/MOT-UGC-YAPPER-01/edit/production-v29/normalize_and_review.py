from pathlib import Path
import json,subprocess,concurrent.futures,cv2
from PIL import Image,ImageDraw
O=Path(__file__).resolve().parent;D=O.parents[1]/'assets/video-v29'
rows={r['name']:r for r in json.loads((O/'H1/timeline-spec.json').read_text())['rows'] if r['name'].startswith('N') and r['track']==2}
def run(n):
 src=D/f'{n}.mp4';dst=O/'normalized'/f'{n}-30fps.mp4'
 if not dst.exists():subprocess.run(['ffmpeg','-v','error','-y','-i',str(src),'-vf','fps=30','-an','-c:v','libx264','-crf','16','-preset','fast','-threads','2',str(dst)],check=True)
 r=rows[n];start=r['source']/30;dur=(r['end']-r['start'])/30;c=cv2.VideoCapture(str(dst));samples=[start+i*dur/7 for i in range(8)];sheet=Image.new('RGB',(8*160,310),'#202020');draw=ImageDraw.Draw(sheet)
 for i,t in enumerate(samples):
  c.set(cv2.CAP_PROP_POS_MSEC,t*1000);ok,b=c.read();assert ok;(im:=Image.fromarray(cv2.cvtColor(b,cv2.COLOR_BGR2RGB))).thumbnail((160,285));sheet.paste(im,(i*160,25));draw.text((i*160+3,4),f'{n} {t:.2f}s',fill='white')
 sheet.save(O/'qa'/f'{n}-selected-motion.jpg');return n
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:print(list(ex.map(run,sorted(rows))))
# Verify every requested source interval, including extended old clips, has frames.
checks=[]
for h in ['H1','H2','H3']:
 for r in json.loads((O/h/'timeline-spec.json').read_text())['rows']:
  if r['track']!=2:continue
  p=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=nb_frames,r_frame_rate,duration,width,height','-of','json',r['path']]))['streams'][0]
  frames=int(p.get('nb_frames',0));need=r['source']+r['end']-r['start'];assert frames>=need,(h,r['name'],frames,need);checks.append({'hook':h,'name':r['name'],'available':frames,'needed':need,'width':p['width'],'height':p['height']})
(O/'qa/source-handle-check.json').write_text(json.dumps(checks,indent=2));print('All source handles valid')
