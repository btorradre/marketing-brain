from pathlib import Path
import json,subprocess,numpy as np
from scipy.signal import correlate
O=Path(__file__).resolve().parent;P=O.parents[1];src=P/'assets/video-v7/presenter-avatar-v.mp4';N=O/'normalized';Q=O/'qa';N.mkdir(exist_ok=True);Q.mkdir(exist_ok=True);expected=json.loads((O/'pause-edit-spec.json').read_text())['frames'];assert src.exists()
meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(src)]));(Q/'presenter-original-metadata.json').write_text(json.dumps(meta,indent=2));print('Original',[(s['codec_type'],s.get('width'),s.get('height'),s.get('duration')) for s in meta['streams']],flush=True)
out=N/'presenter-avatar-v-30fps.mp4'
if not out.exists():subprocess.run(['ffmpeg','-v','error','-y','-i',str(src),'-an','-vf','fps=30:round=up','-c:v','h264_videotoolbox','-b:v','18M','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],check=True)
def pcm(path):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-vn','-ac','1','-ar','8000','-f','f32le','-']),np.float32)
a=pcm(O/'narration.mp3');b=pcm(src);offsets=[]
for t in [3,70,140,210,270]:
 lo=t*8000;ref=a[lo:lo+5*8000];bstart=max(0,lo-8000);sample=b[bstart:lo+6*8000];c=correlate(sample,ref,mode='valid',method='fft');lag=int(np.argmax(c));offset=(bstart+lag-lo)/8000;fit=float(c[lag]/np.sqrt(np.sum(ref*ref)*np.sum(sample[lag:lag+len(ref)]**2)));offsets.append({'source_second':t,'avatar_audio_lag_seconds':offset,'correlation':fit})
(Q/'presenter-audio-sync.json').write_text(json.dumps(offsets,indent=2));print('Audio sync',offsets,flush=True);assert max(abs(x['avatar_audio_lag_seconds']) for x in offsets)<.08;assert min(x['correlation'] for x in offsets)>.95
v=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=nb_frames,duration,width,height','-of','json',str(out)]))['streams'][0];frames=int(v['nb_frames']);assert frames>=expected-1,(frames,expected)
# No silent ending hold. If the provider is one frame short, close at its last frame after the final spoken word.
total=min(frames,expected);(O/'presenter-ready.json').write_text(json.dumps({'video':str(out),'provider_original':str(src),'source_frames':frames,'total_frames':total,'audio_sync':offsets},indent=2));print('Presenter ready',frames,'source frames, final',total,flush=True)
subprocess.run(['ffmpeg','-v','error','-y','-ss','0.5','-i',str(out),'-frames:v','1',str(Q/'selected-presenter-v7.png')],check=True)
