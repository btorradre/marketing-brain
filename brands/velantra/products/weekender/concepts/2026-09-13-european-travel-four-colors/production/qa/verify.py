from pathlib import Path
import json,subprocess,numpy as np,hashlib,re
from PIL import Image,ImageDraw
b=Path(__file__).resolve().parents[2];root=next(x for x in b.parents if (x/'AGENTS.md').exists() and (x/'brands').exists());q=b/'production/qa';f=b/'production/exports/Eleanor-EuropeanTravel-FourColors-Final.mp4';m=root/'brands/velantra/creative/eleanor-european-travel-2026-09-11/production/exports/Eleanor-EuropeanTravel-Tight.mp4'
status=json.loads((b/'production/resolve/render-status.json').read_text());assert status['result']['status']['JobStatus']=='Complete',status
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(f)]));(q/'final-probe.json').write_text(json.dumps(probe,indent=2));vs=next(s for s in probe['streams'] if s['codec_type']=='video');assert int(vs['nb_frames'])==2120,vs.get('nb_frames')
x=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(f),'-vf','scale=180:320','-pix_fmt','rgb24','-f','rawvideo','-']),dtype=np.uint8).reshape(-1,320,180,3);cache=b/'edit/reference-analysis/source-frames.npy';y=np.load(cache) if cache.exists() else np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(m),'-vf','scale=180:320','-pix_fmt','rgb24','-f','rawvideo','-']),dtype=np.uint8).reshape(-1,320,180,3);assert x.shape==y.shape
e=np.abs(x[285:].astype(float)-y[285:].astype(float)).mean((1,2,3))
def packets(p):return subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-map','0:a:0','-c','copy','-f','adts','-'])
a=packets(f);c=packets(m);audio_exact=a==c
black=(x.mean((1,2,3))<3).nonzero()[0].tolist()
silence=subprocess.run(['ffmpeg','-hide_banner','-i',str(f),'-vn','-af','silencedetect=noise=-40dB:d=0.2','-f','null','-'],capture_output=True,text=True);(q/'silence-scan.txt').write_text(silence.stderr)
bounds=json.loads((b/'edit/reference-analysis/background-intervals.json').read_text());ids=sorted({0,15,75,150,210,284,285,2119,2048,2049,*[k for z in bounds[1:] for k in [z['in']-1,z['in']]]})
for batch,start in enumerate(range(0,len(ids),12)):
 part=ids[start:start+12];im=Image.new('RGB',(720,1035),'#161616');draw=ImageDraw.Draw(im)
 for j,i in enumerate(part):
  ox=(j%4)*180;oy=(j//4)*345;im.paste(Image.fromarray(x[i]),(ox,oy+25));draw.text((ox+3,oy+6),f'f{i} / {i/30:.3f}s',fill='white')
 im.save(q/f'final-audit-{batch}.jpg',quality=94)
receipt={'frames':len(x),'fps':30,'duration':len(x)/30,'resolution':[vs['width'],vs['height']],'body_frames_compared':len(x)-285,'body_mae_mean_255':float(e.mean()),'body_mae_max_255':float(e.max()),'body_worst_frame':285+int(e.argmax()),'audio_packets_identical':audio_exact,'audio_adts_sha256':hashlib.sha256(a).hexdigest(),'source_audio_adts_sha256':hashlib.sha256(c).hexdigest(),'black_frames':black,'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'decode':'All 2120 frames decoded; 1835 unchanged-body frames compared against exact source.','scope':'Frame comparisons, native interval checks, opening and consecutive boundary inspections. No claim of human listening or campaign approval.'};(q/'final-qa.json').write_text(json.dumps(receipt,indent=2));print(json.dumps(receipt,indent=2),flush=True)
beats=json.load(open(b/'edit/beats.json'));dest=b/'storyboard/final-composites';dest.mkdir(exist_ok=True)
for z in beats:
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(f),'-vf',f"select=eq(n\\,{z['in']})",'-frames:v','1','-q:v','2',str(dest/(z['id']+'.jpg'))],check=True)
for n,t in [('final-first-frame.png',0),('final-hook-end.png',284),('final-cta.png',2119)]:
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(f),'-vf',f'select=eq(n\\,{t})','-frames:v','1',str(q/n)],check=True)
assert not black,black
assert e.max()<3,float(e.max())
assert audio_exact,'Audio packets changed; inspect before delivery'
print('Media identity checks passed; scene composites and full-size opening/end images extracted.',flush=True)
