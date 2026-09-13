from pathlib import Path
import json,subprocess,numpy as np,math
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;Q=P/'qa-speed110-final';R=P/'resolve-speed110';v=P/'exports/Weekender-Haaland-Gringo-Natural-AvatarV-110-NoGaps-Final.mp4'
a=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(v),'-an','-vf','scale=108:192','-pix_fmt','rgb24','-f','rawvideo','-']),np.uint8).reshape(-1,192,108,3).astype(float)
S=json.loads((R/'aligned-scenes.json').read_text());rows=[]
for s in S[1:]:
 n=s['start'];cand=list(range(n-2,n+3));scores=[float(np.mean((a[i]-a[i-1])**2)) for i in cand];actual=cand[int(np.argmax(scores))];rows.append({'scene':s['id'],'predicted_frame':n,'actual_export_cut_frame':actual,'scene_change_mse':max(scores)});s['start']=actual
for i,s in enumerate(S):s['end']=S[i+1]['start'] if i+1<len(S) else len(a)
(R/'aligned-scenes.json').write_text(json.dumps(S,indent=2));(Q/'actual-scene-boundaries.json').write_text(json.dumps(rows,indent=2));print(rows)
for g in range(3):
 items=S[1+g*4:1+(g+1)*4];sheet=Image.new('RGB',(540,505*len(items)));d=ImageDraw.Draw(sheet)
 for i,s in enumerate(items):
  for j,n in enumerate([s['start']-1,s['start']]):
   f=Q/'frames'/f'{n:05}.jpg'
   if not f.exists():subprocess.run(['ffmpeg','-v','error','-y','-ss',str(n/30),'-i',str(v),'-frames:v','1','-q:v','2',str(f)],check=True)
   im=Image.open(f);im.thumbnail((270,480));sheet.paste(im,(j*270,i*505+25));d.text((j*270+3,i*505+4),f"{s['id']} actual boundary f{n}",fill='white')
 sheet.save(Q/f'actual-scene-pairs-{g}.jpg')
