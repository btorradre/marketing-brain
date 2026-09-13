"""Read-only provider-video verification and diagnostic layout crops."""
import argparse,hashlib,json,re,subprocess
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
p=argparse.ArgumentParser();p.add_argument('video');p.add_argument('output');a=p.parse_args()
video=Path(a.video).resolve();out=Path(a.output).resolve();out.mkdir(parents=True,exist_ok=True)
sha=hashlib.sha256(video.read_bytes()).hexdigest()
probe=json.loads(subprocess.run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)],capture_output=True,text=True,check=True).stdout)
v=next(s for s in probe['streams'] if s['codec_type']=='video')
scene=subprocess.run(['ffmpeg','-hide_banner','-i',str(video),'-an','-vf',"select='gt(scene,0.20)',showinfo",'-f','null','-'],capture_output=True,text=True,check=True).stderr
(out/'scene-detection.txt').write_text(scene)
cuts=[float(s) for s in re.findall(r'pts_time:([\d.]+)',scene)]
sound=subprocess.run(['ffmpeg','-hide_banner','-i',str(video),'-vn','-af','volumedetect','-f','null','-'],capture_output=True,text=True).stderr
(out/'audio-inspection.txt').write_text(sound)
levels=dict(re.findall(r'(mean_volume|max_volume): ([^\n]+)',sound))
poster=out/'detail-poster.jpg'
subprocess.run(['ffmpeg','-v','error','-i',str(video),'-frames:v','1','-q:v','2','-y',str(poster)],check=True)
source_frames=json.loads((out/'frames.json').read_text())['frames']
for name,size in [('desktop',(478,250)),('mobile',(390,420))]:
 cols=3;w,h=size;sheet=Image.new('RGB',(cols*w,((len(source_frames)+cols-1)//cols)*(h+25)),'white');draw=ImageDraw.Draw(sheet)
 for i,row in enumerate(source_frames):
  im=Image.open(row['frame']);im=ImageOps.fit(im,size,method=Image.Resampling.LANCZOS,centering=(.5,.65))
  x=i%cols*w;y=i//cols*(h+25);sheet.paste(im,(x,y));draw.text((x+7,y+h+4),str(row['time'])+'s',fill='black')
 sheet.save(out/(name+'-crop-contact.jpg'),quality=94)
result={'source_video':str(video),'source_bytes':video.stat().st_size,'source_sha256':sha,'source_unchanged_after_inspection':sha==hashlib.sha256(video.read_bytes()).hexdigest(),'video_duration':float(v['duration']),'container_duration':float(probe['format']['duration']),'frames':int(v['nb_frames']),'fps':v['avg_frame_rate'],'dimensions':[v['width'],v['height']],'scene_detector_threshold':.20,'detected_cut_candidates':cuts,'audio_volume':levels,'poster':str(poster),'poster_processing':'Read-only first-frame JPEG extraction, no MP4 changes','diagnostic_crop_only':True,'crop_ratios':{'desktop':'1434/750','mobile':'390/420'},'object_position':'50% 65%'}
(out/'inspection.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
