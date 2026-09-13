import pathlib,json,requests,concurrent.futures,subprocess,hashlib
from PIL import Image,ImageDraw,ImageOps
R=pathlib.Path(__file__).resolve().parent

def run(a):
 d=R/'media'/a['candidate_id'];d.mkdir(parents=True,exist_ok=True);p=d/'source.mp4'
 if not p.exists():
  q=requests.get(a['media']['mediaUrl'],timeout=90);q.raise_for_status();p.write_bytes(q.content)
 meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]));(d/'probe.json').write_text(json.dumps(meta,indent=2))
 (d/'provenance.json').write_text(json.dumps({'candidate':a,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()},indent=2))
 duration=float(meta['format']['duration']);ss=Image.new('RGB',(1200,800),'#15181c');draw=ImageDraw.Draw(ss)
 for i in range(12):
  t=min(duration-.1,i*duration/12);f=d/f'overview-{i:02}.jpg'
  subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i',str(p),'-frames:v','1','-vf','scale=196:340:force_original_aspect_ratio=decrease','-y',str(f)],check=True)
  im=Image.open(f);x=(i%6)*200;y=(i//6)*400;ss.paste(im,(x,y));draw.text((x+3,y+345),f"{a['candidate_id']} {t:.2f}s",fill='white')
 ss.save(d/'overview.jpg');print(a['candidate_id'],round(duration,2),flush=True)
 return a['candidate_id']
if __name__=='__main__':
 rows=json.loads((R/'shortlist.json').read_text())
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
  for f in concurrent.futures.as_completed([ex.submit(run,a) for a in rows]):
   try:f.result()
   except Exception as e:print(type(e).__name__,str(e)[:200],flush=True)
