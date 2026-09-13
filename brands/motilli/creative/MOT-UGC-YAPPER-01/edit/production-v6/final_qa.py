import pathlib,json,subprocess,concurrent.futures
from PIL import Image,ImageDraw,ImageOps
O=pathlib.Path(__file__).resolve().parent;V=O/'deliverables/Motilli-Unbranded-VSL-v6.mp4';Q=O/'qa/final';Q.mkdir(parents=True,exist_ok=True)
meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(V)]));(Q/'metadata.json').write_text(json.dumps(meta,indent=2));v=next(s for s in meta['streams'] if s['codec_type']=='video');assert (v['width'],v['height'])==(1080,1920);assert v['r_frame_rate']=='30/1';assert int(v['nb_frames'])==10145;assert any(s['codec_type']=='audio' for s in meta['streams']);print('Final metadata verified',v['nb_frames'],meta['format']['duration'],flush=True)
ins=json.loads((O/'aligned-inserts.json').read_text());frames={0,1,60,10000,10054,10055,10144}
for x in ins:frames.update([x['start_frame']-1,x['start_frame'],x['end_frame']-1,x['end_frame']])
frames=sorted(frames)
def extract(f):
 dst=Q/f'frame-{f:05d}.jpg'
 if not dst.exists():subprocess.run(['ffmpeg','-v','error','-y','-ss',f'{f/30:.9f}','-i',str(V),'-frames:v','1','-q:v','2',str(dst)],check=True)
 return dst
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:list(ex.map(extract,frames))
for page in range(5):
 batch=ins[page*4:(page+1)*4];im=Image.new('RGB',(800,4*380),'#ececec');d=ImageDraw.Draw(im)
 for row,x in enumerate(batch):
  fs=[x['start_frame']-1,x['start_frame'],x['end_frame']-1,x['end_frame']];d.text((6,row*380+3),f"{x['id']} {x['asset']} | before / first / last / after",fill='black')
  for col,f in enumerate(fs):
   thumb=ImageOps.contain(Image.open(Q/f'frame-{f:05d}.jpg'),(192,342));im.paste(thumb,(col*200,row*380+23));d.text((col*200+5,row*380+363),str(f),fill='black')
 im.save(Q/f'boundaries-{page+1}.jpg')
# Probe first, last words and the actual hold independently of the covering sheets.
fs=[0,60,10000,10054,10055,10144];im=Image.new('RGB',(1200,380),'#eee');d=ImageDraw.Draw(im)
for i,f in enumerate(fs):im.paste(ImageOps.contain(Image.open(Q/f'frame-{f:05d}.jpg'),(195,346)),(i*200,20));d.text((i*200+4,3),str(f),fill='black')
im.save(Q/'opening-and-ending.jpg');print('Extracted',len(frames),'exact frame samples; five consecutive-boundary sheets',flush=True)
with (Q/'audio-levels.txt').open('w') as out:subprocess.run(['ffmpeg','-hide_banner','-i',str(V),'-af','loudnorm=I=-14:TP=-1:LRA=11:print_format=json','-f','null','-'],stderr=out,stdout=subprocess.DEVNULL,check=True)
with (Q/'black-silence-scan.txt').open('w') as out:subprocess.run(['ffmpeg','-hide_banner','-i',str(V),'-vf','blackdetect=d=0.08:pix_th=0.06','-af','silencedetect=noise=-45dB:d=1.5','-f','null','-'],stderr=out,stdout=subprocess.DEVNULL,check=True)
print('Final technical QA complete',flush=True)
