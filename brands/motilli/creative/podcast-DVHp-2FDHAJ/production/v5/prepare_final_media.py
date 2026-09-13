from pathlib import Path
import subprocess,concurrent.futures,json
P=Path(__file__).resolve().parent

def norm(role):
 src=P/f'{role}-paced.mp3';dst=P/'normalized'/f'{role}-audio.wav'
 if dst.exists():return
 proc=subprocess.run(['ffmpeg','-hide_banner','-i',str(src),'-af','loudnorm=I=-16:TP=-1:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
 stats=json.JSONDecoder().raw_decode(proc.stderr[proc.stderr.rfind('{'):])[0];(P/'qa'/f'{role}-loudness.json').write_text(json.dumps(stats,indent=2))
 filt=f"loudnorm=I=-16:TP=-1:LRA=11:measured_I={stats['input_i']}:measured_TP={stats['input_tp']}:measured_LRA={stats['input_lra']}:measured_thresh={stats['input_thresh']}:offset={stats['target_offset']}:linear=true"
 subprocess.run(['ffmpeg','-y','-v','error','-i',str(src),'-af',filt,'-ar','48000','-ac','2','-c:a','pcm_s24le',str(dst)],check=True);print(role,'normalized',flush=True)
def video(key):
 src=P/'broll'/key/'original.mp4';dst=P/'normalized'/(key+'-30fps.mp4')
 if not dst.exists():subprocess.run(['ffmpeg','-v','error','-y','-i',str(src),'-an','-vf','fps=30','-c:v','h264_videotoolbox','-b:v','10000000',str(dst)],check=True)
 print(key,'normalized',flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
 jobs=[ex.submit(norm,r) for r in ('host','guest')]+[ex.submit(video,k) for k in ('product-jar','product-gummies','stomach-reveal-final')]
 for f in jobs:f.result()
