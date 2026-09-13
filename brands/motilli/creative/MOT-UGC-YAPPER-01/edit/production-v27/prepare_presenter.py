from pathlib import Path
import json,subprocess,numpy as np,sys
from scipy.signal import correlate
O=Path(__file__).resolve().parent
for h in sys.argv[1:] or ['H1','H2','H3']:
 S=O/h;src=S/'presenter-avatar-v-original.mp4';out=S/'presenter-avatar-v-30fps.mp4';expected=json.loads((S/'timeline-spec.json').read_text())['frames'];assert src.exists();meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(src)]));(S/'presenter-original-metadata.json').write_text(json.dumps(meta,indent=2))
 if not out.exists():subprocess.run(['ffmpeg','-v','error','-y','-i',str(src),'-an','-vf','fps=30:round=up','-c:v','h264_videotoolbox','-b:v','14M','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],check=True)
 def pcm(p):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-vn','-ac','1','-ar','8000','-f','f32le','-']),np.float32)
 a=pcm(O/f'deliverables/Motilli-V27-{h}-Woman-Over-40-Natural-Resolve-1.1x.mp3');b=pcm(src);offsets=[]
 for t in [3,50,100,150,210]:
  lo=t*8000;ref=a[lo:lo+5*8000];bs=max(0,lo-8000);sample=b[bs:lo+6*8000];c=correlate(sample,ref,mode='valid',method='fft');lag=int(np.argmax(c));fit=float(c[lag]/np.sqrt(np.sum(ref*ref)*np.sum(sample[lag:lag+len(ref)]**2)));offsets.append(dict(source_second=t,avatar_audio_lag_seconds=(bs+lag-lo)/8000,correlation=fit))
 (S/'presenter-audio-sync.json').write_text(json.dumps(offsets,indent=2));assert max(abs(x['avatar_audio_lag_seconds']) for x in offsets)<.08;assert min(x['correlation'] for x in offsets)>.94
 v=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=nb_frames,duration,width,height','-of','json',str(out)]))['streams'][0];assert v['width']==1080 and v['height']==1920;frames=int(v['nb_frames']);assert frames>=expected,(h,frames,expected)
 (S/'presenter-ready.json').write_text(json.dumps(dict(video=str(out),provider_original=str(src),source_frames=frames,total_frames=expected,audio_sync=offsets),indent=2));print(h,'presenter ready',frames,'frames; expected',expected,'audio sync',offsets,flush=True)
