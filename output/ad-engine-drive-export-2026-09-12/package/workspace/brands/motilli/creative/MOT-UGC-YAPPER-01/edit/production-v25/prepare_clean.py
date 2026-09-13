from pathlib import Path
import json,subprocess,re,math
O=Path(__file__).resolve().parent;F=30
specs=[]
for h in ['H1','H2','H3']:
 src=O/f'deliverables/Motilli-V25-{h}-Woman-Over-40-Natural-1.2x-source.mp3';wav=O/f'{h}-source-48k.wav'
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(src),'-ar','48000','-ac','1','-c:a','pcm_s24le',str(wav)],check=True)
 dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(wav)]));end=math.floor(dur*F)
 r=subprocess.run(['ffmpeg','-hide_banner','-i',str(wav),'-af','silencedetect=noise=-40dB:d=0.35','-f','null','-'],capture_output=True,text=True,check=True);(O/f'qa/{h}-source-silences.txt').write_text(r.stderr)
 quiet=[];a=None
 for line in r.stderr.splitlines():
  m=re.search(r'silence_start: ([0-9.]+)',line)
  if m:a=float(m[1])
  m=re.search(r'silence_end: ([0-9.]+)',line)
  if m and a is not None:quiet.append((a,float(m[1])));a=None
 cuts=[]
 for a,b in quiet:
  l=max(0,math.ceil((a+.08)*F));r=min(end,math.floor((b-.08)*F))
  if r-l>=2:cuts.append([l,r])
 rows=[];pos=0;off=0
 for l,r in cuts+[[end,end]]:
  if l>pos:rows.append(dict(path=str(wav),source_start=pos,source_end=l,record_start=off,record_end=off+l-pos));off+=l-pos
  pos=r
 d=dict(source_seconds=dur,start_frame=0,end_frame=end,rows=rows,output_frames=off,output_seconds=off/F,removed_seconds=dur-off/F,cut_intervals_frames=cuts,quiet_intervals=quiet)
 (O/f'{h}-pause-edit.json').write_text(json.dumps(d,indent=2));print(h,len(cuts),'cuts;',round(d['removed_seconds'],2),'seconds removed;',round(off/F,2),'duration')
 specs.append(dict(hook=h,rows=rows,frames=off,name=f'v25 {h} Woman Over 40 Natural - cleaned voice'))
def lua(v):
 if isinstance(v,str):return json.dumps(v)
 if isinstance(v,list):return '{'+','.join(map(lua,v))+'}'
 if isinstance(v,dict):return '{'+','.join('['+lua(k)+']='+lua(x) for k,x in v.items())+'}'
 return str(v)
old=(O.parent/'production-v24/assemble-waveform-clean.lua').read_text();start=old.index('local mp=');a=old.index('local specs=')+len('local specs=');b=old.index(';local ids={}',a)
code=old[:a]+lua(specs)+old[b:];code=code.replace('production-v24','production-v25').replace('V24','V25').replace("'-clean-master-resolve-r2'","'-clean-master-resolve'")
(O/'assemble-clean.lua').write_text(code)
