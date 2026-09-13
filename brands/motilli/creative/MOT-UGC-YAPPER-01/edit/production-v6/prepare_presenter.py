import pathlib,json,subprocess,math
import numpy as np
from scipy.signal import correlate,correlation_lags
O=pathlib.Path(__file__).resolve().parent;P=O.parents[1];src=P/'assets/video-v6/presenter-avatar-v.mp4';N=O/'normalized';Q=O/'qa';assert src.exists()
def run(args):subprocess.run(args,check=True)
meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(src)]));(Q/'presenter-original-metadata.json').write_text(json.dumps(meta,indent=2));print('Original video',[(x['codec_type'],x.get('width'),x.get('height'),x.get('r_frame_rate'),x.get('duration')) for x in meta['streams']],flush=True)
# Preserve source; conform FPS only, never alter playback speed.
out=N/'presenter-avatar-v-30fps.mp4'
if not out.exists():run(['ffmpeg','-v','error','-y','-i',str(src),'-an','-vf','fps=30','-c:v','libx264','-crf','16','-preset','fast','-threads','3',str(out)])
def pcm(path):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-vn','-ac','1','-ar','8000','-f','f32le','-']),dtype=np.float32)
a=pcm(O/'narration.mp3');b=pcm(src);offsets=[]
for t in [3,80,160,240,320]:
 lo=t*8000;ref=a[lo:lo+5*8000];bstart=max(0,lo-8000);sample=b[bstart:lo+6*8000];c=correlate(sample,ref,mode='valid',method='fft');lag=int(np.argmax(c));offset=(bstart+lag-lo)/8000;fit=float(c[lag]/np.sqrt(np.sum(ref*ref)*np.sum(sample[lag:lag+len(ref)]**2)));offsets.append({'source_second':t,'avatar_audio_lag_seconds':offset,'correlation':fit})
print('Audio sync',offsets,flush=True);(Q/'presenter-audio-sync.json').write_text(json.dumps(offsets,indent=2));assert max(abs(x['avatar_audio_lag_seconds']) for x in offsets)<0.08,'Inspect audio/video offset before assembly'
counts=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=nb_frames,duration,width,height','-of','json',str(out)]))['streams'][0];frames=int(counts['nb_frames']);spoken=10055;assert frames>=spoken-2,('Avatar ended too soon',frames)
last=min(spoken,frames)-1;still=Q/'presenter-end.png';run(['ffmpeg','-v','error','-y','-i',str(out),'-vf',f'select=eq(n\\,{last})','-frames:v','1',str(still)])
hold=N/'presenter-end-hold.mov';run(['ffmpeg','-v','error','-y','-loop','1','-framerate','30','-i',str(still),'-frames:v',str(10145-min(spoken,frames)),'-an','-c:v','qtrle','-pix_fmt','argb','-threads','2',str(hold)])
(O/'presenter-ready.json').write_text(json.dumps({'video':str(out),'provider_original':str(src),'source_frames':frames,'spoken_video_frames':min(spoken,frames),'hold':str(hold),'total_frames':10145,'audio_sync':offsets},indent=2));print('Presenter prepared',flush=True)
