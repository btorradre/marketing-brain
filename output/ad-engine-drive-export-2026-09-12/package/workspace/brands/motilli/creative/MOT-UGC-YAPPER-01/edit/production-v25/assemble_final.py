from pathlib import Path
import json,subprocess,re,math
O=Path(__file__).resolve().parent;F=30
wav=O/'CTA-source-48k.wav';src=O/'deliverables/Motilli-V25-CTA-Woman-Over-40-Natural-1.2x-source.mp3'
subprocess.run(['ffmpeg','-v','error','-y','-i',str(src),'-ar','48000','-ac','1','-c:a','pcm_s24le',str(wav)],check=True)
r=subprocess.run(['ffmpeg','-hide_banner','-i',str(wav),'-af','silencedetect=noise=-40dB:d=0.35','-f','null','-'],capture_output=True,text=True,check=True);(O/'qa/CTA-source-silences.txt').write_text(r.stderr)
dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(wav)]));cuts=[];a=None
for line in r.stderr.splitlines():
 m=re.search(r'silence_start: ([0-9.]+)',line)
 if m:a=float(m[1])
 m=re.search(r'silence_end: ([0-9.]+)',line)
 if m and a is not None:
  b=float(m[1]);l=math.ceil((a+.08)*F);r=math.floor((b-.08)*F)
  if r-l>=2:cuts.append([l,r])
  a=None
ca=json.loads((O/'CTA-alignment.json').read_text())['alignment'];cs=max(0,math.floor((ca['character_start_times_seconds'][0]-.08)*F));ce=min(math.floor(dur*F),math.ceil((ca['character_end_times_seconds'][-1]+.08)*F))
rows=[];pos=cs
for l,r in cuts+[[ce,ce]]:
 l=min(l,ce);r=min(r,ce)
 if l>pos:rows.append(dict(path=str(wav),source_start=pos,source_end=l))
 pos=max(pos,r)
cta=rows
specs=[]
def select(h,start,end):
 d=json.loads((O/f'{h}-pause-edit.json').read_text());out=[]
 for r in d['rows']:
  a=max(start,r['source_start']);b=min(end,r['source_end'])
  if b>a:out.append(dict(path=r['path'],source_start=a,source_end=b))
 return out
for h,hookend in [('H1',333),('H2',552),('H3',459)]:
 rows=select(h,0,hookend)+select('H2',565,8060)+cta;off=0
 for r in rows:r['record_start']=off;off+=r['source_end']-r['source_start'];r['record_end']=off
 d=dict(rows=rows,output_frames=off,output_seconds=off/F,revision='r2 selected H2 common body plus exact CTA pickup',voice_id='NBIPq5xdnIg9kaBH5Ape')
 (O/f'{h}-final-edit.json').write_text(json.dumps(d,indent=2));specs.append(dict(hook=h,rows=rows,frames=off,name=f'v25 {h} Woman Over 40 Natural - final r2'));print(h,off/F,len(rows))
def lua(v):
 if isinstance(v,str):return json.dumps(v)
 if isinstance(v,list):return '{'+','.join(map(lua,v))+'}'
 if isinstance(v,dict):return '{'+','.join('['+lua(k)+']='+lua(x) for k,x in v.items())+'}'
 return str(v)
old=(O/'assemble-clean.lua').read_text();a=old.index('local specs=')+len('local specs=');b=old.index(';local ids={}',a);code=old[:a]+lua(specs)+old[b:]
code=code.replace("local media=mp:ImportMedia({s.rows[1].path})[1];assert(media)","local cache={}")
code=code.replace('for _,row in ipairs(s.rows) do local clip=',"for _,row in ipairs(s.rows) do local media=cache[row.path];if not media then media=mp:ImportMedia({row.path})[1];assert(media);cache[row.path]=media end;local clip=")
code=code.replace("'-clean-master-resolve'","'-final-master-resolve'").replace('waveform-clean','Woman-Over-40-final')
(O/'assemble-final.lua').write_text(code)
