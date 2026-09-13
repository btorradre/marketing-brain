from pathlib import Path
import subprocess,json,numpy as np,sys
from scipy.signal import correlate
from PIL import Image,ImageDraw
O=Path(__file__).resolve().parent
for h in sys.argv[1:]:
 S=O/h;video=O/f'deliverables/Motilli-VSL-V28-{h}-UPDATED-SCRIPT-1.2x.mp4';spec=json.loads((S/'timeline-spec.json').read_text());meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)]));v=next(s for s in meta['streams'] if s['codec_type']=='video');assert int(v['nb_frames'])==spec['frames'] and v['width']==1080 and v['height']==1920
 r=subprocess.run(['ffmpeg','-hide_banner','-i',str(video),'-vf','scale=270:480,blackdetect=d=0.06:pix_th=0.08','-an','-f','null','-'],capture_output=True,text=True);assert r.returncode==0;rlog=r.stderr;(O/f'qa/{h}-decode.txt').write_text(rlog);assert 'black_start:' not in rlog
 def pcm(p):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-vn','-ac','1','-ar','8000','-f','f32le','-']),np.float32)
 a=pcm(O.parent/f'production-v26/deliverables/Motilli-V26-{h}-Woman-Over-40-Natural-Resolve-1.2x.mp3');b=pcm(video);sync=[]
 for t in [3,45,90,140,195]:
  lo=t*8000;ref=a[lo:lo+5*8000];bs=lo-800;sample=b[bs:lo+40800];c=correlate(sample,ref,mode='valid',method='fft');lag=int(np.argmax(c));fit=float(c[lag]/np.sqrt(np.sum(ref*ref)*np.sum(sample[lag:lag+len(ref)]**2)));offset=(bs+lag-lo)/8000;sync.append(dict(t=t,lag=offset,correlation=fit))
 if min(x['correlation'] for x in sync)<=.94:
  def env(x):return np.sqrt(np.mean(x[:len(x)//80*80].reshape(-1,80)**2,axis=1))
  ea,eb=env(a),env(b);sync=[]
  for t in [3,45,90,140,195]:
   lo=t*100;ref=ea[lo:lo+500];bs=lo-10;sample=eb[bs:lo+510];c=correlate(sample,ref,mode='valid');lag=int(np.argmax(c));fit=float(c[lag]/np.sqrt(np.sum(ref*ref)*np.sum(sample[lag:lag+len(ref)]**2)));sync.append(dict(t=t,lag=(bs+lag-lo)/100,correlation=fit,method='10ms RMS envelope; pitch correction phases differ'))
 assert max(abs(x['lag']) for x in sync)<.04 and min(x['correlation'] for x in sync)>.94,sync
 outdir=O/'qa'/f'{h}-final-frames';outdir.mkdir(exist_ok=True);rows=[r for r in spec['rows'] if r['kind']=='video' and r['track']==2];rows+=[dict(name='presenter-early',start=160,end=160),dict(name='presenter-end',start=spec['frames']-15,end=spec['frames']-15)]
 for r in rows:
  dst=outdir/(r['name']+'.jpg');subprocess.run(['ffmpeg','-v','error','-y','-ss',str((r['start']+r['end'])/60),'-i',str(video),'-frames:v','1','-vf','scale=270:480',str(dst)],check=True)
 for page in range((len(rows)+7)//8):
  batch=rows[page*8:page*8+8];sheet=Image.new('RGB',(4*270,2*510),'#333333');draw=ImageDraw.Draw(sheet)
  for i,r in enumerate(batch):x=i%4*270;y=i//4*510;sheet.paste(Image.open(outdir/(r['name']+'.jpg')),(x,y+30));draw.text((x+3,y+6),r['name'],fill='white')
  sheet.save(O/f'qa/{h}-final-sheet-{page+1}.jpg')
 (O/f'qa/{h}-final-video.json').write_text(json.dumps(dict(file=str(video),frames=spec['frames'],video_seconds=spec['frames']/30,full_decode_pass=True,no_black_gaps=True,audio_sync=sync,metadata=meta),indent=2));print(h,'FINAL TECHNICAL PASS',flush=True)
