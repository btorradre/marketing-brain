import subprocess,pathlib,numpy as np,json,re
from PIL import Image,ImageDraw
p=pathlib.Path(__file__).parent
proc=subprocess.Popen(['ffmpeg','-loglevel','error','-i',str(p/'source.mp4'),'-vf','scale=180:320','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
frames=[];diffs=[];prev=None
while True:
 b=proc.stdout.read(180*320*3)
 if len(b)<180*320*3:break
 a=np.frombuffer(b,dtype=np.uint8).reshape(320,180,3).copy()
 if prev is not None:
  diffs.append({'frame':len(frames),'time':len(frames)/30,'mad':float(np.abs(a.astype(float)-prev).mean()),'top':float(np.abs(a[:200].astype(float)-prev[:200]).mean()),'bottom':float(np.abs(a[200:].astype(float)-prev[200:]).mean())})
 frames.append(a);prev=a
proc.wait();(p/'all-frame-diff.json').write_text(json.dumps(diffs))
np.save(p/'frames-small.npy',np.array(frames))
(p/'decode-summary.json').write_text(json.dumps({'frames':len(frames),'fps':30,'sampling':'every frame decoded at 180x320; dense contact sheets 0.5s; candidate consecutive frames separately'},indent=2))
for page,start in enumerate(range(0,len(frames),15*30)):
 inds=list(range(start,min(start+15*30,len(frames)),15));sheet=Image.new('RGB',(6*180,5*344),'#171717');d=ImageDraw.Draw(sheet)
 for i,n in enumerate(inds):
  x=i%6*180;y=i//6*344;sheet.paste(Image.fromarray(frames[n]),(x,y+24));d.text((x+4,y+5),f'{n/30:07.3f}s  f{n}',fill='white')
 sheet.save(p/f'dense-{page+1:02d}.jpg',quality=92)
# Union official scene detector and robust temporal discontinuity; suppress nearby duplicates only for sheet compactness.
t=(p/'cut-candidates.txt').read_text();cs=[int(round(float(s)*30)) for s in re.findall(r'pts_time:([\d.]+)',t)]
cs+= [x['frame'] for x in diffs if x['mad']>22 or x['top']>27 or x['bottom']>32]
cs=sorted(set(cs));cs2=[]
for n in cs:
 if cs2 and n-cs2[-1]<5:
  if diffs[n-1]['mad']>diffs[cs2[-1]-1]['mad']:cs2[-1]=n
 else:cs2.append(n)
(p/'candidate-frames.json').write_text(json.dumps(cs2))
for page,start in enumerate(range(0,len(cs2),10)):
 sheet=Image.new('RGB',(6*180,10*344),'#171717');d=ImageDraw.Draw(sheet)
 for row,n in enumerate(cs2[start:start+10]):
  for col,off in enumerate([-3,-2,-1,0,1,2]):
   f=max(0,min(len(frames)-1,n+off));x=col*180;y=row*344
   sheet.paste(Image.fromarray(frames[f]),(x,y+24));d.text((x+3,y+5),f'{f/30:.3f}s f{f}',fill='yellow' if off==0 else 'white')
 sheet.save(p/f'boundaries-{page+1:02d}.jpg',quality=91)
print(len(frames),'frames;',len(cs2),'candidates;',cs2)
