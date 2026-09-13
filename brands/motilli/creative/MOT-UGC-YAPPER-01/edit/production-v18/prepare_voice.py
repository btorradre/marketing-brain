from pathlib import Path
import json,re,subprocess,math,difflib,numpy as np
O=Path(__file__).resolve().parent;F=30;rows=[];offset=0;actual=[];cuts=[];audit=[];duration=0
norm=lambda t:re.findall(r'[a-z0-9]+',t.lower().replace('thirty','30').replace('three','3').replace('two','2').replace('first','1st').replace('second','2nd').replace('third','3rd'))
for i in [1,2]:
 s=json.loads((O/f'part-{i}-scribe.json').read_text());e=norm((O/f'part-{i}-exact.txt').read_text());h=norm(s['text']);diff=[{'op':tag,'expected':e[a:b],'heard':h[c:d]} for tag,a,b,c,d in difflib.SequenceMatcher(None,e,h,autojunk=False).get_opcodes() if tag!='equal'];audit.append({'part':i,'differences':diff});words=[w for w in s['words'] if w['type']=='word'];wav=O/f'part-{i}-48k.wav';subprocess.run(['ffmpeg','-v','error','-i',str(O/f'part-{i}.mp3'),'-ar','48000','-ac','1','-c:a','pcm_s24le','-y',str(wav)],check=True);dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(wav)]));duration+=dur
 start=max(0,math.floor((words[0]['start']-.12)*F));end=min(math.floor(dur*F),math.ceil((words[-1]['end']+.16)*F));log=(O/f'part-{i}-silences.txt').read_text();ss=[];current=None
 for line in log.splitlines():
  m=re.search(r'silence_start: ([0-9.]+)',line)
  if m:current=float(m[1])
  m=re.search(r'silence_end: ([0-9.]+)',line)
  if m and current is not None:ss.append((current,float(m[1])));current=None
 remove=[]
 pcm=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(wav),'-f','f32le','-ac','1','-ar','8000','-']),np.float32)
 for w,n in zip(words,words[1:]):
  a,b=w['end'],n['start']
  if b-a<=.65:continue
  l=math.ceil((a+.17)*F);r=math.floor((b-.17)*F)
  if r-l<4:continue
  z=pcm[int(l/F*8000):int(r/F*8000)];rms=20*np.log10(np.sqrt(np.mean(z*z))+1e-9)
  if rms>-38:continue
  remove.append((l,r));cuts.append({'part':i,'speech_gap':[a,b],'removed_frames':[l,r],'retained_gap':(b-a)-(r-l)/F,'cut_rms_db':float(rms)})
 last=start;pr=[]
 for l,r in remove+[(end,end)]:
  if l>last:row={'part':i,'path':str(wav),'source_start':last,'source_end':l,'record_start':offset,'record_end':offset+l-last};rows.append(row);pr.append(row);offset+=l-last
  last=r
 for w in words:
  matches=[r for r in pr if r['source_start']/F<=w['start']+.035 and r['source_end']/F>=w['end']-.035];assert matches,(i,w);r=matches[0];shift=(r['record_start']-r['source_start'])/F;actual.append({**w,'part':i,'start':w['start']+shift,'end':w['end']+shift})
spec={'fps':F,'frames':offset,'edited_duration':offset/F,'source_duration':duration,'removed_seconds':duration-offset/F,'pause_edits':len(cuts),'pause_cuts':cuts,'rows':rows,'asr_audit':audit};(O/'pause-edit-spec.json').write_text(json.dumps(spec,indent=2));(O/'edited-scribe-words.json').write_text(json.dumps(actual,indent=2));print(json.dumps({k:v for k,v in spec.items() if k not in ['rows','pause_cuts']},indent=2),flush=True)
def lua(x):
 if isinstance(x,str):return json.dumps(x)
 if isinstance(x,(int,float)):return str(x)
 if isinstance(x,list):return '{'+','.join(lua(v) for v in x)+'}'
 return '{'+','.join('['+lua(k)+']='+lua(v) for k,v in x.items())+'}'
code="""local r=fu:GetResolve();local pm=r:GetProjectManager();local p=pm:GetCurrentProject();assert(p:GetName()=='MOT-UGC-YAPPER-01 v7 V3 20260910');assert(not p:IsRenderingInProgress());for i=1,p:GetTimelineCount() do assert(p:GetTimelineByIndex(i):GetName()~='v18 Michelle V3 - final voice master','Already exists; inspect') end;local mp=p:GetMediaPool();local t=mp:CreateEmptyTimeline('v18 Michelle V3 - final voice master');assert(t);p:SetCurrentTimeline(t);t:SetStartTimecode('00:00:00:00');local rows=__ROWS__;local media={};for _,s in ipairs(rows) do if not media[s.path] then media[s.path]=mp:ImportMedia({s.path})[1] end;local c=mp:AppendToTimeline({{mediaPoolItem=media[s.path],startFrame=s.source_start,endFrame=s.source_end,recordFrame=s.record_start,trackIndex=1,mediaType=2}})[1];assert(c and c:GetStart()==s.record_start and c:GetEnd()==s.record_end) end;assert(t:GetEndFrame()==__FRAMES__);pm:SaveProject();p:SetCurrentRenderMode(1);assert(p:SetCurrentRenderFormatAndCodec('mov','H264'));assert(p:SetRenderSettings({TargetDir=__OUT__,CustomName='narration-master-resolve',SelectAllFrames=true,ExportVideo=false,ExportAudio=true,AudioCodec='LinearPCM',AudioBitDepth=24,AudioSampleRate=48000}));local id=p:AddRenderJob();assert(id);print('V18_VOICE_JOB',id);assert(p:StartRendering(id));pm:SaveProject()""".replace('__ROWS__',lua(rows)).replace('__FRAMES__',str(offset)).replace('__OUT__',lua(str(O)))
(O/'assemble-voice.lua').write_text(code)
