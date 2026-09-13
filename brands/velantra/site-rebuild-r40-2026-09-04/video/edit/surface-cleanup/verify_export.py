"""Verify rendered frames against every intended source frame and cut boundary."""
import argparse,hashlib,json
from pathlib import Path
import cv2,numpy as np

p=argparse.ArgumentParser();p.add_argument('family');a=p.parse_args()
row=next(r for r in json.loads(Path('shots.json').read_text()) if r['family']==a.family)
path=Path('exports')/f'{a.family}-surface-clean.mp4'
render=cv2.VideoCapture(str(path));count=int(render.get(cv2.CAP_PROP_FRAME_COUNT));fps=render.get(cv2.CAP_PROP_FPS)
assert count==row['frames'],(count,row['frames'])
assert abs(fps-24)<.001,fps
assert (int(render.get(cv2.CAP_PROP_FRAME_WIDTH)),int(render.get(cv2.CAP_PROP_FRAME_HEIGHT)))==(1920,1080)
out=Path('qa')/(a.family+'-export');out.mkdir(exist_ok=True)
errors=[];samples=[];boundaries=[]
for shot in row['shots']:
 if shot['retouch']:
  source=Path('plates')/a.family/f"shot-{shot['number']:02d}"/'shot.mp4';offset=0
 else:source=Path(row['video']);offset=shot['start']
 cap=cv2.VideoCapture(str(source));cap.set(cv2.CAP_PROP_POS_FRAMES,offset)
 for i in range(shot['start'],shot['end']):
  ok,actual=render.read();ok2,expected=cap.read();assert ok and ok2,(i,ok,ok2)
  small_actual=cv2.resize(actual,(240,135),interpolation=cv2.INTER_AREA)
  small_expected=cv2.resize(expected,(240,135),interpolation=cv2.INTER_AREA)
  mae=float(cv2.absdiff(small_actual,small_expected).mean());errors.append([i,mae])
  if i in {shot['start'],shot['anchor'],shot['end']-1}:
   cv2.imwrite(str(out/f'shot-{shot["number"]:02d}-frame-{i:04d}.jpg'),actual,[cv2.IMWRITE_JPEG_QUALITY,96]);samples.append(i)
  if i in {shot['start'],shot['end']-1}:boundaries.append({'frame':i,'mae':mae})
  if i==0:cv2.imwrite(str(out/'poster.jpg'),actual,[cv2.IMWRITE_JPEG_QUALITY,96])
 cap.release()
render.release()
receipt={'family':a.family,'path':str(path),'frames':count,'fps':fps,'duration':count/fps,
 'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bytes':path.stat().st_size,
 'per_frame_mean_absolute_error':float(np.mean([x[1] for x in errors])),
 'worst_frames':sorted(errors,key=lambda x:x[1],reverse=True)[:10],'cut_boundaries':boundaries,
 'samples':samples,'every_intended_frame_verified':max(x[1] for x in errors)<5,
 'visual_review':'pending'}
(out/'verification.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k not in ['cut_boundaries','samples']}))
