"""Read-only video frame extraction and diagnostic contact sheet; no video edits."""
from pathlib import Path
import argparse,json,subprocess
from PIL import Image,ImageDraw
parser=argparse.ArgumentParser();parser.add_argument('video');parser.add_argument('output');parser.add_argument('--times');args=parser.parse_args()
video=Path(args.video).resolve();out=Path(args.output).resolve();out.mkdir(parents=True,exist_ok=True)
probe=json.loads(subprocess.run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)],capture_output=True,text=True,check=True).stdout)
stream=next(s for s in probe['streams'] if s['codec_type']=='video');duration=float(stream['duration'])
times=[float(t) for t in args.times.split(',')] if args.times else [i*.75 for i in range(int(duration/.75)+1)]
times=[t for t in times if t<duration]+[duration-1/24]
cols=3;tw=480;th=295;canvas=Image.new('RGB',(cols*tw,((len(times)+cols-1)//cols)*th),'white');draw=ImageDraw.Draw(canvas)
rows=[]
for i,t in enumerate(times):
 frame=out/f'frame-{i:02d}-{t:.3f}.jpg'
 subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i',str(video),'-frames:v','1','-q:v','2','-y',str(frame)],check=True)
 im=Image.open(frame);im.thumbnail((tw,270));x=i%cols*tw;y=i//cols*th;canvas.paste(im,(x,y));draw.text((x+7,y+273),f'{t:.3f}s',fill='black')
 rows.append({'time':t,'frame':str(frame)})
canvas.save(out/'contact.jpg',quality=94)
(out/'frames.json').write_text(json.dumps({'source_video':str(video),'source_duration':duration,'frames':rows,'diagnostic_only':True},indent=2)+'\n')
print(json.dumps({'video':str(video),'duration':duration,'contact':str(out/'contact.jpg'),'frames':len(rows)}))
