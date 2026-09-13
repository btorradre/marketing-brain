from pathlib import Path
import json,subprocess,numpy as np
from scipy.signal import correlate
O=Path(__file__).resolve().parent
for h,n in [('H1',246),('H3',458)]:
 S=O/(h+'-hook');src=S/'presenter-avatar-v-original.mp4';out=S/'presenter-avatar-v-30fps.mp4'
 if not out.exists():subprocess.run(['ffmpeg','-v','error','-y','-i',str(src),'-an','-vf','fps=30:round=up','-c:v','h264_videotoolbox','-b:v','14M','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],check=True)
 def pcm(p):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-vn','-ac','1','-ar','8000','-f','f32le','-']),np.float32)
 a=pcm(S/'hook-with-context.mp3');b=pcm(src);ref=a[8000:-8000];c=correlate(b,ref,mode='valid',method='fft');lag=int(np.argmax(c));fit=float(c[lag]/np.sqrt(np.sum(ref*ref)*np.sum(b[lag:lag+len(ref)]**2)));offset=(lag-8000)/8000;assert abs(offset)<.08 and fit>.94,(offset,fit)
 v=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=nb_frames,width,height','-of','json',str(out)]))['streams'][0];assert int(v['nb_frames'])>=n and v['width']==1080 and v['height']==1920
 (S/'presenter-ready.json').write_text(json.dumps(dict(video=str(out),frames=int(v['nb_frames']),used_frames=n,lag_seconds=offset,correlation=fit),indent=2));print(h,'READY',offset,fit)
