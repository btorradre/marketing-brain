from pathlib import Path
import json,subprocess,re,math,numpy as np,shutil
O=Path(__file__).resolve().parent;F=30;N=1600;RATE=48000
for h in ['H1','H2','H3']:
 p=O/f'{h}-pause-edit.json';d=json.loads(p.read_text());shutil.copy2(p,O/f'qa/{h}-first-pass-edit.json');wav=O/f'{h}-source-48k.wav'
 r=subprocess.run(['ffmpeg','-hide_banner','-i',str(wav),'-af','silencedetect=noise=-40dB:d=0.35','-f','null','-'],capture_output=True,text=True,check=True);(O/f'qa/{h}-original-silences.txt').write_text(r.stderr)
 quiet=[];a=None
 for line in r.stderr.splitlines():
  m=re.search(r'silence_start: ([0-9.]+)',line)
  if m:a=float(m[1])
  m=re.search(r'silence_end: ([0-9.]+)',line)
  if m and a is not None:quiet.append((a,float(m[1])));a=None
 old=[tuple(x['cut_frames']) for x in d['gap_audit'] if x.get('cut_frames')];new=[]
 for a,b in quiet:
  l=math.ceil((a+.08)*F);r=math.floor((b-.08)*F)
  if r-l>=2:new.append((l,r))
 merged=[]
 for l,r in sorted(old+new):
  if merged and l<=merged[-1][1]:merged[-1][1]=max(r,merged[-1][1])
  else:merged.append([l,r])
 start=d['start_frame'];end=d['end_frame'];rows=[];pos=start;off=0
 for l,r in merged+[[end,end]]:
  l=max(start,l);r=min(end,r)
  if l>pos:rows.append({'path':str(wav),'source_start':pos,'source_end':l,'record_start':off,'record_end':off+l-pos});off+=l-pos
  pos=r
 d.update(rows=rows,output_frames=off,output_seconds=off/F,removed_seconds=d['source_seconds']-off/F,pause_cut_count=len(merged),cut_intervals_frames=merged,second_pass_waveform_quiet_intervals=quiet,maximum_remaining_interword_gap=None,revision='r2 waveform plus word-boundary checks')
 p.write_text(json.dumps(d,indent=2));print(h,'cuts',len(merged),'removed',d['removed_seconds'],'duration',off/F)
