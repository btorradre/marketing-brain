from pathlib import Path
import subprocess,json,concurrent.futures,hashlib,re
import numpy as np
p=Path(__file__).resolve().parent

def check(v):
 f=p/'exports'/f'MOT-VID-013-{v}.mp4';meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(f)]));vid=next(s for s in meta['streams'] if s['codec_type']=='video');assert (vid['width'],vid['height'],vid['codec_name'],vid['r_frame_rate'])==(1080,1920,'h264','30/1');assert abs(float(vid['duration'])-96.633333)<.001
 scan=subprocess.run(['ffmpeg','-hide_banner','-nostats','-i',str(f),'-vf','blackdetect=d=0.02:pix_th=0.04:pic_th=0.98','-an','-f','null','-'],capture_output=True,text=True);assert scan.returncode==0
 blacks=[line for line in scan.stderr.splitlines() if 'black_start:' in line]
 audio=subprocess.check_output(['ffmpeg','-v','error','-i',str(f),'-map','0:a:0','-f','hash','-hash','sha256','-']).decode().strip()
 return {'variant':v,'file':str(f),'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'video_codec':vid['codec_name'],'width':vid['width'],'height':vid['height'],'fps':vid['r_frame_rate'],'picture_duration':float(vid['duration']),'frame_count':vid['nb_frames'],'full_decode_pass':True,'black_intervals':blacks,'decoded_audio_hash':audio}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:results=list(ex.map(check,'ABC'))
au=subprocess.run(['ffmpeg','-hide_banner','-nostats','-i',str(p/'exports/MOT-VID-013-A.mp4'),'-vn','-af','loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True)
match=re.search(r'\{\s*"input_i".*?\}',au.stderr,re.S);loud=json.loads(match.group()) if match else None
signals=[]
for v in 'ABC':
 signals.append(np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p/'exports'/f'MOT-VID-013-{v}.mp4'),'-vn','-ac','1','-ar','8000','-f','f32le','-']),dtype=np.float32))
correlations={}
for i in [1,2]:
 n=min(len(signals[0]),len(signals[i]));correlations['A_'+ 'ABC'[i]]=float(np.corrcoef(signals[0][:n],signals[i][:n])[0,1])
assert min(correlations.values())>.999,correlations
assert -21<float(loud['input_i'])<-18,loud
assert float(loud['input_tp'])<-.8,loud
report={'audio_waveform_correlations':correlations,'exports':results,'audio_identical_across_variants':len({r['decoded_audio_hash'] for r in results})==1,'audio_measurement':loud,'rendered_visual_QA':'95 caption midpoints and consecutive frames across all four blur transitions; final changed-shot checks separately','voice':'Existing ElevenLabs take 4; not reference clone'}
(p/'qa/final-validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True)
