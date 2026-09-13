from pathlib import Path
import json,subprocess,math
import numpy as np
O=Path(__file__).resolve().parent;B=O.parent/'production-v23';F=30;RATE=48000;N=RATE//F
for h in ['H1','H2','H3']:
 src=B/f'deliverables/Motilli-V23-{h}-Eleven-v3-Natural-1.2x.mp3';wav=O/f'{h}-source-48k.wav';subprocess.run(['ffmpeg','-v','error','-y','-i',str(src),'-ar','48000','-ac','1','-c:a','pcm_s24le',str(wav)],check=True)
 pcm=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(wav),'-f','f32le','-ac','1','-ar',str(RATE),'-']),np.float32);nf=len(pcm)//N;chunks=pcm[:nf*N].reshape(-1,N);rms=20*np.log10(np.sqrt(np.mean(chunks*chunks,axis=1))+1e-10);peaks=20*np.log10(np.max(abs(chunks),axis=1)+1e-10)
 words=[w for w in json.loads((B/f'qa/{h}-scribe.json').read_text())['words'] if w['type']=='word'];start=max(0,math.floor((words[0]['start']-.07)*F));end=min(nf,math.ceil((words[-1]['end']+.07)*F));cuts=[];audit=[]
 for w,n in zip(words,words[1:]):
  a,b=w['end'],n['start'];gap=b-a
  if gap<=.35:continue
  l=max(start,math.ceil((a+.06)*F));r=min(end,math.floor((b-.06)*F));runs=[];rs=None
  for i in range(l,r+1):
   quiet=i<r and rms[i]<-40 and peaks[i]<-25
   if quiet and rs is None:rs=i
   if not quiet and rs is not None:runs.append((rs,i));rs=None
  longest=max(runs,key=lambda x:x[1]-x[0],default=(0,0));amount=min(longest[1]-longest[0],max(0,math.floor((gap-.22)*F)))
  rec={'after':w['text'],'before':n['text'],'start':a,'end':b,'source_gap':gap,'quiet_run_frames':longest}
  if amount>=2:
   cs=longest[0]+(longest[1]-longest[0]-amount)//2;ce=cs+amount;cuts.append((cs,ce));rec.update(cut_frames=[cs,ce],removed_seconds=amount/F,remaining_gap=gap-amount/F)
  else:rec.update(removed_seconds=0,remaining_gap=gap,reason='No sufficiently long quiet interval; protect speech/breath')
  audit.append(rec)
 rows=[];pos=start;off=0
 for l,r in cuts+[(end,end)]:
  if l>pos:rows.append({'path':str(wav),'source_start':pos,'source_end':l,'record_start':off,'record_end':off+l-pos});off+=l-pos
  pos=r
 def mapped(t):
  for row in rows:
   if row['source_start']/F-.0001<=t<=row['source_end']/F+.0001:return t+(row['record_start']-row['source_start'])/F
  raise ValueError(('Time falls in removed silence',h,t))
 outwords=[]
 for w in words:outwords.append({**w,'start':mapped(w['start']),'end':mapped(w['end'])})
 spec={'hook':h,'fps':F,'source':str(src),'source_frames':nf,'start_frame':start,'end_frame':end,'output_frames':off,'source_seconds':len(pcm)/RATE,'output_seconds':off/F,'removed_seconds':len(pcm)/RATE-off/F,'pause_cut_count':len(cuts),'rows':rows,'gap_audit':audit,'maximum_remaining_interword_gap':max(n['start']-w['end'] for w,n in zip(outwords,outwords[1:]))}
 (O/f'{h}-pause-edit.json').write_text(json.dumps(spec,indent=2));(O/f'{h}-clean-aligned-words.json').write_text(json.dumps(outwords,indent=2));print(h, {k:spec[k] for k in ['output_seconds','removed_seconds','pause_cut_count','maximum_remaining_interword_gap']})
