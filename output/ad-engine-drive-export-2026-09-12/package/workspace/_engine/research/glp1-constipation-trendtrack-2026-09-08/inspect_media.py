import json,pathlib,urllib.request,ssl,certifi,concurrent.futures,subprocess
from PIL import Image,ImageOps,ImageDraw
ROOT=pathlib.Path(__file__).resolve().parent
(ROOT/'media').mkdir(exist_ok=True)
def work(f):
 s=json.loads(f.read_text())['result']['structuredContent'];a=s['data'];id=a['id'].replace('facebook_','');v=a['media'];ext='mp4' if v['type']=='video' else 'jpg';out=ROOT/'media'/f'{id}.{ext}'
 if not out.exists():
  subprocess.run(['curl','-f','-sS','-L','--max-time','90','-A','Mozilla/5.0',v['mediaUrl'],'-o',str(out)],check=True)
 if ext=='mp4':
  info=json.loads(subprocess.check_output(['ffprobe','-v','quiet','-show_format','-show_streams','-of','json',str(out)]));dur=float(info['format']['duration']);(ROOT/'media'/f'{id}-probe.json').write_text(json.dumps(info,indent=2))
  frames=[]
  for i,t in enumerate([0.5,3,dur*.25,dur*.5,dur*.75,max(0,dur-2)]):
   frame=ROOT/'media'/f'{id}-frame-{i}.jpg';subprocess.run(['ffmpeg','-y','-v','error','-ss',str(t),'-i',str(out),'-frames:v','1',str(frame)],check=True)
   im=ImageOps.contain(Image.open(frame).convert('RGB'),(300,440));tile=Image.new('RGB',(320,480),'white');tile.paste(im,((320-im.width)//2,25));ImageDraw.Draw(tile).text((10,460),f'{t:.1f}s',fill='black');frames.append(tile)
  sheet=Image.new('RGB',(960,960),'white')
  for i,im in enumerate(frames):sheet.paste(im,((i%3)*320,(i//3)*480))
  sheet.save(ROOT/'media'/f'{id}-sheet.jpg')
 else:dur=None
 print(id,a['advertiser']['name'],'seconds',dur,'days',a['daysRunning'],'members',s['memberAdsCount'],'active',s['activeAdsCount'],'metrics',a['metrics'],'analysis',s['analysis'],'transcript',str(a.get('transcript'))[:300],flush=True)
files=[f for f in (ROOT/'raw').glob('scan-*.json') if 'request' not in f.name]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:list(ex.map(work,files))
