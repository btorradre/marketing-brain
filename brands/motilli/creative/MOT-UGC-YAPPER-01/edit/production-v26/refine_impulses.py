from pathlib import Path
import json,re,math,subprocess,shutil
O=Path(__file__).resolve().parent;F=30

def lua(v):
 if isinstance(v,str):return json.dumps(v)
 if isinstance(v,list):return '{'+','.join(map(lua,v))+'}'
 if isinstance(v,dict):return '{'+','.join('['+lua(k)+']='+lua(x) for k,x in v.items())+'}'
 return str(v)
for h in ['H1','H2','H3']:
 p=O/f'{h}-clean-edit.json';d=json.loads(p.read_text());shutil.copy2(p,O/f'qa/{h}-r2-clean-edit.json');f=O/f'{h}-clean100-r2-master.mov';r=subprocess.run(['ffmpeg','-hide_banner','-i',str(f),'-af','silencedetect=noise=-40dB:d=0.08','-f','null','-'],capture_output=True,text=True,check=True);cuts=[];quiet=[];a=None
 for line in r.stderr.splitlines():
  m=re.search(r'silence_start: ([0-9.]+)',line)
  if m:a=float(m[1])
  m=re.search(r'silence_end: ([0-9.]+)',line)
  if m and a is not None:
   b=float(m[1]);
   if quiet and a-quiet[-1][1]<=.005:quiet[-1][1]=b
   else:quiet.append([a,b])
   a=None
 cuts=[[math.ceil((a+.08)*F),math.floor((b-.08)*F)] for a,b in quiet if b-a>=.35]
 rows=[]
 for row in d['rows']:
  intervals=[[row['record_start'],row['record_end']]]
  for l,r in cuts:
   keep=[]
   for a,b in intervals:
    if r<=a or l>=b:keep.append([a,b])
    else:
     if a<l:keep.append([a,l])
     if r<b:keep.append([r,b])
   intervals=keep
  for a,b in intervals:
   z=dict(row);z['source_start']=row['source_start']+a-row['record_start'];z['source_end']=row['source_start']+b-row['record_start'];rows.append(z)
 off=0
 for row in rows:row['record_start']=off;off+=row['source_end']-row['source_start'];row['record_end']=off
 old=d['output_frames'];d.update(rows=rows,output_frames=off,output_seconds=off/F,final_expected_frames=round(off/1.2),r2_cuts_on_original_clean_frames=cuts);p.write_text(json.dumps(d,indent=2));print(h,old,'->',off,cuts)
 for stage in ['clean','speed']:
  s=(O/f'{h}-{stage}-r2.lua').read_text().replace(f'local frames={old};',f'local frames={off};').replace('cleaned 100 percent r2','cleaned 100 percent r3').replace("stage='clean100-r2'","stage='clean100-r3'").replace('FINAL 120 percent','FINAL 120 percent r3').replace("stage='final120'","stage='final120-r3'")
  if stage=='clean':
   a=s.index('local rows=')+len('local rows=');b=s.index(';local name=',a);s=s[:a]+lua(rows)+s[b:]
  (O/f'{h}-{stage}-r3.lua').write_text(s)
s=(O/'verify_clean.py').read_text().replace('clean100-master','clean100-r3-master');(O/'verify_clean_r3.py').write_text(s)
