from pathlib import Path
import json,subprocess,re,math
O=Path(__file__).resolve().parent;F=30;parts=json.loads((O/'parts.json').read_text());allrows={}
for h in parts:
 wav=O/f'sources/{h}-48k.wav';src=O/f'sources/{h}-default-speed.mp3';subprocess.run(['ffmpeg','-v','error','-y','-i',str(src),'-ar','48000','-ac','1','-c:a','pcm_s24le',str(wav)],check=True)
 dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(wav)]));end=math.floor(dur*F);start=0
 r=subprocess.run(['ffmpeg','-hide_banner','-i',str(wav),'-af','silencedetect=noise=-40dB:d=0.35','-f','null','-'],capture_output=True,text=True,check=True);(O/f'qa/{h}-source-silences.txt').write_text(r.stderr);quiet=[];a=None
 for line in r.stderr.splitlines():
  m=re.search(r'silence_start: ([0-9.]+)',line)
  if m:a=float(m[1])
  m=re.search(r'silence_end: ([0-9.]+)',line)
  if m and a is not None:quiet.append((a,float(m[1])));a=None
 cuts=[]
 for a,b in quiet:
  if a<.03:start=max(0,math.floor((b-.08)*F));continue
  if b>=dur-.03:end=min(end,math.ceil((a+.08)*F));continue
  l=math.ceil((a+.08)*F);r=math.floor((b-.08)*F)
  if r-l>=2:cuts.append([l,r])
 rows=[];pos=start
 for l,r in cuts+[[end,end]]:
  l=min(l,end);r=min(r,end)
  if l>pos:rows.append(dict(part=h,path=str(wav),source_start=pos,source_end=l))
  pos=max(pos,r)
 allrows[h]=rows;(O/f'{h}-source-edit.json').write_text(json.dumps(dict(source_seconds=dur,quiet_intervals=quiet,cut_frames=cuts,rows=rows),indent=2));print(h,round(dur,2),len(cuts),'cuts')
def lua(v):
 if isinstance(v,str):return json.dumps(v)
 if isinstance(v,list):return '{'+','.join(map(lua,v))+'}'
 if isinstance(v,dict):return '{'+','.join('['+lua(k)+']='+lua(x) for k,x in v.items())+'}'
 return str(v)
for h in ['H1','H2','H3']:
 rows=[dict(r) for p in [h,'B1','B2','B3','B4'] for r in allrows[p]];off=0
 for r in rows:r['record_start']=off;off+=r['source_end']-r['source_start'];r['record_end']=off
 (O/f'{h}-clean-edit.json').write_text(json.dumps(dict(rows=rows,output_frames=off,output_seconds=off/F,final_expected_frames=round(off/1.2)),indent=2))
 prefix="local r=fu:GetResolve();local pm=r:GetProjectManager();local p=pm:GetCurrentProject();assert(not p:IsRenderingInProgress());if p:GetName()~='MOT-UGC-YAPPER-01 v7 V3 20260910' then assert(pm:SaveProject());p=pm:LoadProject('MOT-UGC-YAPPER-01 v7 V3 20260910');assert(p) end;local mp=p:GetMediaPool();local O="+lua(str(O))+";local h="+lua(h)+";local frames="+str(off)+";\n"
 export="""
assert(pm:SaveProject());assert(t:Export(O..'/deliverables/Motilli-V26-'..h..'-'..stage..'.drt',r.EXPORT_DRT));p:SetCurrentRenderMode(1);assert(p:SetRenderSettings({ExportVideo=false,ExportAudio=true}));assert(p:SetCurrentRenderFormatAndCodec('mov','H264'));assert(p:SetRenderSettings({TargetDir=O,CustomName=h..'-'..stage..'-master',SelectAllFrames=true,ExportVideo=false,ExportAudio=true,AudioCodec='lpcm',AudioBitDepth=24,AudioSampleRate=48000}));local id=p:AddRenderJob();assert(id);print('V26_JOB',h,stage,id,t:GetEndFrame());assert(pm:SaveProject());assert(pm:ExportProject(p:GetName(),O..'/deliverables/Motilli-V26-voices.drp'));p:StartRendering(id)
"""
 clean="local rows="+lua(rows)+";local name='v26 '..h..' Woman Over 40 - cleaned 100 percent';local stage='clean100';local t=nil;for i=1,p:GetTimelineCount() do local q=p:GetTimelineByIndex(i);if q:GetName()==name then t=q end end;\n"+"""
if not t then
 local cache={};for _,row in ipairs(rows) do if not cache[row.path] then cache[row.path]=mp:ImportMedia({row.path})[1];assert(cache[row.path]) end end
 t=mp:CreateEmptyTimeline(name);assert(t and t:GetName()==name);assert(p:SetCurrentTimeline(t));t:SetStartTimecode('00:00:00:00')
 for _,row in ipairs(rows) do assert(p:SetCurrentTimeline(t));local c=mp:AppendToTimeline({{mediaPoolItem=cache[row.path],startFrame=row.source_start,endFrame=row.source_end,recordFrame=row.record_start,trackIndex=1,mediaType=2}})[1];assert(c and c:GetStart()==row.record_start and c:GetEnd()==row.record_end,'clip position');assert(c:GetSpeed().Percentage==100) end
end
assert(p:SetCurrentTimeline(t));assert(t:GetEndFrame()==frames);assert(#t:GetItemListInTrack('audio',1)==#rows);print('V26_CLEAN_VERIFIED',h,frames)
"""
 speed="""
local base=nil;local t=nil;local name='v26 '..h..' Woman Over 40 - FINAL 120 percent';local stage='final120';for i=1,p:GetTimelineCount() do local q=p:GetTimelineByIndex(i);if q:GetName()=='v26 '..h..' Woman Over 40 - cleaned 100 percent' then base=q end;if q:GetName()==name then t=q end end;assert(base and base:GetEndFrame()==frames)
if not t then t=mp:CreateEmptyTimeline(name);assert(t and t:GetName()==name);assert(p:SetCurrentTimeline(t));t:SetStartTimecode('00:00:00:00');local c=mp:AppendToTimeline({{mediaPoolItem=base:GetMediaPoolItem(),startFrame=0,endFrame=frames,recordFrame=0,trackIndex=1,mediaType=2}})[1];assert(c and c:GetEnd()==frames);assert(c:SetSpeed({Percentage=120,PitchCorrection=true,RippleTimeline=true})) end
assert(p:SetCurrentTimeline(t));local clips=t:GetItemListInTrack('audio',1);assert(#clips==1);local c=clips[1];local speed=c:GetSpeed();assert(speed.Percentage==120 and speed.PitchCorrection==true);assert(math.abs(t:GetEndFrame()-frames/1.2)<=1);assert(base:GetEndFrame()==frames);print('V26_SPEED_VERIFIED',h,t:GetEndFrame());dump(speed)
"""
 for stage,code in [('clean',clean),('speed',speed)]:
  (O/f'{h}-{stage}.lua').write_text("local ok,err=pcall(function()\n"+prefix+code+export+"\nend);print('V26_RESULT',ok,err)")
