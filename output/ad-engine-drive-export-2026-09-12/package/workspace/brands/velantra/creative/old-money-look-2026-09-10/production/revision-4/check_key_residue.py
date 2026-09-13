"""Compare known-empty keyed-background strips against same-hook A1 render."""
from pathlib import Path
import cv2,json,numpy as np
R=Path(__file__).resolve().parent
report={}
beats=json.loads((R/'resolve/beat-map.json').read_text())
for h in ('H1','H2','H3'):
 ref=cv2.VideoCapture(str(R/'exports'/f'VEL-OM-{h}-A1-R4.mp4'));others={a:cv2.VideoCapture(str(R/'exports'/f'VEL-OM-{h}-{a}-R4.mp4')) for a in ('A2','A3')}
 values={a:[] for a in others};n=0
 while True:
  ok,base=ref.read()
  if not ok:break
  for a,cap in others.items():
   ok,got=cap.read();assert ok
   # Empty source region above presenter hair, away from captions and foreground.
   y1,y2,x1,x2=(1072,1100,10,480) if a=='A2' else (930,1020,10,540)
   if n<beats[h]['reveal']:y1,y2,x1,x2=(1382,1400,5,300) if a=='A2' else (1350,1380,5,320)
   mae=float(np.abs(got[y1:y2,x1:x2].astype(float)-base[y1:y2,x1:x2]).mean());values[a].append(mae)
  n+=1
 ref.release()
 for a,cap in others.items():
  cap.release();v=values[a];report[h+'-'+a]={'decoded_frames':n,'mean_background_mae':float(np.mean(v)),'max_background_mae':max(v),'frames_above_4_mae':np.flatnonzero(np.array(v)>4).tolist()}
 print(h,{a:round(max(v),3) for a,v in values.items()},flush=True)
(R/'qa/final/key-background-residue.json').write_text(json.dumps(report,indent=2))
assert all(v['max_background_mae']<4 for v in report.values()),report
