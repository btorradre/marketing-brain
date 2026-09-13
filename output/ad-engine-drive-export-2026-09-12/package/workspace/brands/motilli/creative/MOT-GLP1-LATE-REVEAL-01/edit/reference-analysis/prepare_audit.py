import pathlib,subprocess,json,re
from PIL import Image,ImageOps,ImageDraw
P=pathlib.Path(__file__).resolve().parent;src=pathlib.Path((P/'source-path.txt').read_text());(P/'frames').mkdir(exist_ok=True)
res=subprocess.run(['ffmpeg','-v','info','-i',str(src),'-vf',"select='gt(scene,0.16)',showinfo",'-an','-f','null','-'],capture_output=True,text=True)
(P/'scene-log.txt').write_text(res.stderr)
ts=[float(x) for x in re.findall(r'pts_time:([\d.]+)',res.stderr)];cuts=sorted(set(round(x*25) for x in ts));(P/'candidate-cuts.json').write_text(json.dumps(cuts));print('candidate cuts',len(cuts),cuts,flush=True)
subprocess.run(['ffmpeg','-y','-v','error','-i',str(src),'-vf','fps=2,scale=180:-1','-q:v','4',str(P/'frames/sample-%04d.jpg')],check=True)
fs=sorted((P/'frames').glob('sample-*.jpg'))
for start in range(0,len(fs),48):
 batch=fs[start:start+48];sheet=Image.new('RGB',(1440,6*345),'white');dr=ImageDraw.Draw(sheet)
 for j,f in enumerate(batch):
  im=ImageOps.contain(Image.open(f),(178,315));x=j%8*180;y=j//8*345;sheet.paste(im,(x,y+25));dr.text((x+4,y+4),f'{(start+j)*.5:.1f}s',fill='black')
 sheet.save(P/f'overview-{start:03d}.jpg')
for start in range(0,len(cuts),12):
 batch=cuts[start:start+12];sheet=Image.new('RGB',(1200,4*340),'white');dr=ImageDraw.Draw(sheet)
 for j,n in enumerate(batch):
  for side,fr in enumerate([n-1,n]):
   f=P/'frames'/f'cut-{n}-{side}.jpg';subprocess.run(['ffmpeg','-y','-v','error','-i',str(src),'-vf',f'select=eq(n\,{fr}),scale=190:-1','-frames:v','1',str(f)],check=True)
   im=ImageOps.contain(Image.open(f),(195,310));x=j%3*400+side*200;y=j//3*340;sheet.paste(im,(x,y+22));dr.text((x+4,y+3),f'{fr/25:.2f}s f{fr}',fill='black')
 sheet.save(P/f'boundaries-{start:03d}.jpg')
