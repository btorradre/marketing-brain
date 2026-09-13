"""Match rendered face detail to native avatar frames around expected source times."""
import json
from pathlib import Path
import cv2
import numpy as np

HERE=Path(__file__).resolve().parent
manifest=json.loads((HERE/'resolve/trimmed/manifest.json').read_text())
report={}
def patch(frame):
    gray=cv2.cvtColor(frame[530:1030,330:740],cv2.COLOR_BGR2GRAY)
    return cv2.resize(gray,(82,100)).astype(np.float32)
for ad in manifest:
    source=cv2.VideoCapture(str(HERE/'avatars'/ad['ad_id']/'avatar-native.mp4'))
    dest=cv2.VideoCapture(str(HERE/'exports'/(ad['ad_id']+'.mp4')))
    holds=[l for l in ad['presenter_layout'] if l['mode']=='presenter_hold' and l['end']-l['start']>24]
    selected=sorted(holds,key=lambda l:l['end']-l['start'],reverse=True)[:5]
    checks=[]
    for l in sorted(selected,key=lambda l:l['start']):
        target=(l['start']+l['end'])//2
        expected=(l['pretrim_start']+target-l['start'])/30
        dest.set(cv2.CAP_PROP_POS_FRAMES,target);ok,frame=dest.read();assert ok
        wanted=patch(frame); scores=[]
        center=round(expected*25)
        for n in range(max(0,center-15),center+16):
            source.set(cv2.CAP_PROP_POS_FRAMES,n);ok,frame=source.read()
            if not ok: continue
            got=patch(frame)
            score=float(cv2.matchTemplate(got,wanted,cv2.TM_CCOEFF_NORMED)[0,0])
            scores.append((score,n))
        score,n=max(scores)
        checks.append({'target_seconds':target/30,'expected_source_seconds':expected,
            'matched_source_seconds':n/25,'offset_seconds':n/25-expected,'correlation':score})
    source.release();dest.release();report[ad['ad_id']]=checks
    print(ad['ad_id'],[(round(c['offset_seconds'],3),round(c['correlation'],3)) for c in checks],flush=True)
(HERE/'qa/final/presenter-frame-correspondence.json').write_text(json.dumps(report,indent=2)+'\n')
