import pathlib,json,subprocess,concurrent.futures,sys
from fractions import Fraction
import numpy as np
from PIL import Image,ImageDraw
R=pathlib.Path(__file__).resolve().parent

def run(cid):
 d=R/'media'/cid;meta=json.loads((d/'probe.json').read_text());v=next(x for x in meta['streams'] if x['codec_type']=='video');fps=float(Fraction(v['r_frame_rate']))
 w=144;h=round(w*v['height']/v['width']/2)*2
 raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(d/'source.mp4'),'-an','-vf',f'scale={w}:{h}','-pix_fmt','rgb24','-f','rawvideo','-'])
 frames=np.frombuffer(raw,dtype=np.uint8).reshape(-1,h,w,3);n=len(frames);scores=np.zeros(n);roi=np.zeros(n)
 for i in range(1,n):
  diff=np.abs(frames[i].astype(np.float32)-frames[i-1]);scores[i]=diff.mean();roi[i]=diff[h//3:5*h//6].mean()
 candidates=[]
 for i in range(1,n-1):
  baseline=float(np.median(scores[max(1,i-10):i])) if i>1 else 0.0
  if (scores[i]>11 or (scores[i]>4 and scores[i]>max(1.1,baseline)*3.5) or (roi[i]>9 and scores[i]>2.7 and scores[i]>max(.8,baseline)*2.5)) and scores[i]>=scores[i-1] and scores[i]>=scores[i+1]:
   if not candidates or i-candidates[-1]>2:candidates.append(i)
 (d/'candidate-frames.json').write_text(json.dumps({'fps':v['r_frame_rate'],'frame_count':n,'candidates':candidates,'note':'Unverified detector candidates; not accepted shot boundaries.'},indent=2))
 ev=d/'evidence';ev.mkdir(exist_ok=True)
 samples=sorted(set([round(t*fps) for t in np.arange(0,n/fps,.5) if round(t*fps)<n]+[n-1]))
 def sheet(indices,path,cols=6):
  ch=h+22;rows=(len(indices)+cols-1)//cols;im=Image.new('RGB',(cols*w,rows*ch),'#17191d');draw=ImageDraw.Draw(im)
  for j,f in enumerate(indices):
   x=j%cols*w;y=j//cols*ch;im.paste(Image.fromarray(frames[f]),(x,y));draw.text((x+2,y+h+2),f'{f} / {f/fps:.3f}s',fill='white')
  im.save(path,quality=88)
 for start in range(0,len(samples),36):sheet(samples[start:start+36],ev/f'dense-{start//36+1:02}.jpg')
 # Each candidate gets the immediate outgoing/incoming pair, with no sampling gap.
 for start in range(0,len(candidates),12):sheet([f for c in candidates[start:start+12] for f in [c-1,c]],ev/f'cuts-{start//12+1:02}.jpg')
 (d/'review-scope.json').write_text(json.dumps({'decoded_frames':n,'fps':v['r_frame_rate'],'dense_samples':samples,'boundary_candidates':candidates,'manual_review':[],'audio_audition':False,'exhaustive_individual_frame_review':False},indent=2))
 # Export source transcript if returned by MCP; never replace a missing transcript with ad body.
 scan=R/'raw'/f'scan-{cid}.json'
 if scan.exists():
  data=json.loads(scan.read_text())['result']['structuredContent']['data'];tr=data.get('transcript')
  if not tr and data.get('content',{}).get('transcript'):
   tr=data['content']['transcript'];tr=json.loads(tr) if isinstance(tr,str) else tr
  if tr:
   (d/'transcript.json').write_text(json.dumps(tr,indent=2));(d/'transcript.txt').write_text('\n'.join(f"{s['start']:.2f}-{s['end']:.2f} {s['text']}" for s in tr.get('segments',[])))
 print(cid,n,len(samples),len(candidates),flush=True)
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
  for f in concurrent.futures.as_completed([ex.submit(run,c) for c in sys.argv[1:]]):f.result()
