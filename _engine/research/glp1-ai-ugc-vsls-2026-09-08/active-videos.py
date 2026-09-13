import json,pathlib,subprocess,concurrent.futures
from PIL import Image,ImageOps,ImageDraw
P=pathlib.Path(__file__).resolve().parent
rows=json.loads((P/'candidates.json').read_text())
labels=['A1','A2','A3']
def work(label):
 r=next(x for x in rows if x['label']==label);out=P/'media'/(label+'.mp4')
 if not out.exists():subprocess.run(['curl','-f','-sS','-L','--max-time','90','-A','Mozilla/5.0',r['sampleAd']['mediaUrl'],'-o',str(out)],check=True)
 info=json.loads(subprocess.check_output(['ffprobe','-v','quiet','-show_format','-show_streams','-of','json',str(out)]));dur=float(info['format']['duration']);(P/'media'/(label+'-probe.json')).write_text(json.dumps(info))
 sheet=Image.new('RGB',(1200,760),'white');draw=ImageDraw.Draw(sheet)
 for i,t in enumerate([.5,3,dur*.15,dur*.3,dur*.5,dur*.7,dur*.85,dur-2]):
  f=P/'media'/f'{label}-frame{i}.jpg';subprocess.run(['ffmpeg','-y','-v','error','-ss',str(t),'-i',str(out),'-frames:v','1',str(f)],check=True)
  im=ImageOps.contain(Image.open(f).convert('RGB'),(295,340));x=i%4*300;y=i//4*380;sheet.paste(im,(x,y+25));draw.text((x+4,y+5),f'{label} {t:.1f}s',fill='black')
 sheet.save(P/'media'/(label+'-sheet.jpg'));print(label,round(dur,1),len(r['fullText'].split()),r['fullText'],flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:list(ex.map(work,labels))
