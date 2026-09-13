from pathlib import Path
import json
O=Path(__file__).resolve().parent;V=O.parent/'production-v28'
def lua(x):
 if isinstance(x,str):return json.dumps(x)
 if isinstance(x,bool):return str(x).lower()
 if isinstance(x,dict):return '{'+','.join('['+lua(k)+']='+lua(v) for k,v in x.items())+'}'
 if isinstance(x,list):return '{'+','.join(lua(v) for v in x)+'}'
 return str(x)
code="""local r=fu:GetResolve();local pm=r:GetProjectManager();local p=pm:GetCurrentProject();assert(not p:IsRenderingInProgress());assert(pm:SaveProject());if p:GetName()~='MOT-UGC-YAPPER-01 v7 V3 20260910' then p=pm:LoadProject('MOT-UGC-YAPPER-01 v7 V3 20260910');assert(p) end;local mp=p:GetMediaPool();local jobs={};local function find(name) for i=1,p:GetTimelineCount() do local t=p:GetTimelineByIndex(i);if t:GetName()==name then return t end end end
"""
for h,oldtotal in [('H1',6700),('H2',6850),('H3',6911)]:
 s=json.loads((O/h/'timeline-spec.json').read_text());total=s['frames'];rows=s['rows'];num=len([r for r in rows if r['track']==3]);name=f'v29 {h} FINAL NUORA STYLE - 1.2x Woman Over40';audio=str(V/f'deliverables/Motilli-VSL-V28-{h}-UPDATED-SCRIPT-1.2x.mp4')
 code+=f'''do local name={lua(name)};local t=find(name);local stage=find('v28 {h} presenter source 110');assert(stage);local rows={lua(rows)};
if not t then t=mp:CreateEmptyTimeline(name);assert(t);assert(p:SetCurrentTimeline(t));t:SetStartTimecode('00:00:00:00');assert(t:AddTrack('video'));assert(t:AddTrack('video'));local v=mp:AppendToTimeline({{{{mediaPoolItem=stage:GetMediaPoolItem(),startFrame=0,endFrame={oldtotal},recordFrame=0,trackIndex=1,mediaType=1}}}})[1];assert(v);assert(v:SetSpeed({{Percentage={120/110*100},RippleTimeline=false}}));assert(v:GetEnd()=={total});local am=mp:ImportMedia({{{lua(audio)}}})[1];assert(am);local a=mp:AppendToTimeline({{{{mediaPoolItem=am,startFrame=0,endFrame={total},recordFrame=0,trackIndex=1,mediaType=2}}}})[1];assert(a and a:GetEnd()=={total});local cache={{}};for _,s in ipairs(rows) do if not cache[s.path] then cache[s.path]=mp:ImportMedia({{s.path}})[1];assert(cache[s.path],s.path) end;local c=mp:AppendToTimeline({{{{mediaPoolItem=cache[s.path],startFrame=s.source,endFrame=s.source+s['end']-s.start,recordFrame=s.start,trackIndex=s.track,mediaType=1}}}})[1];assert(c,s.name);if next(s.props) then assert(c:SetProperty(s.props),s.name) end;assert(c:GetStart()==s.start and c:GetEnd()==s['end'],s.name) end end
assert(p:SetCurrentTimeline(t));assert(t:GetEndFrame()=={total});assert(#t:GetItemListInTrack('video',1)==1);assert(#t:GetItemListInTrack('video',2)==32);assert(#t:GetItemListInTrack('video',3)=={num});assert(#t:GetItemListInTrack('audio',1)==1);t:SetTrackName('video',1,'HeyGen synchronized 120 percent');t:SetTrackName('video',2,'Nuora style story-linked direct cuts');t:SetTrackName('video',3,'Exact script large phrase captions');t:SetTrackName('audio',1,'Verified Woman Over40 Natural 120 percent V28 master');assert(pm:SaveProject());assert(t:Export({lua(str(O/f'project-files/Motilli-V29-{h}-FINAL.drt'))},r.EXPORT_DRT));print('V29_NATIVE_VERIFIED','{h}',t:GetEndFrame(),#t:GetItemListInTrack('video',2),#t:GetItemListInTrack('video',3));
p:SetCurrentRenderMode(1);assert(p:SetCurrentRenderFormatAndCodec('mp4','H264'));assert(p:SetRenderSettings({{TargetDir={lua(str(O/'deliverables'))},CustomName='Motilli-VSL-V29-{h}-NUORA-STYLE-1.2x',SelectAllFrames=true,ExportVideo=true,ExportAudio=true,FormatWidth=1080,FormatHeight=1920,FrameRate=30,VideoQuality=16000,AudioCodec='aac',AudioBitDepth=16,AudioSampleRate=48000}}));local id=p:AddRenderJob();assert(id);table.insert(jobs,id);print('V29_JOB','{h}',id) end\n'''
code+=f"assert(pm:SaveProject());assert(pm:ExportProject(p:GetName(),{lua(str(O/'project-files/Motilli-V29-FINAL.drp'))}));assert(p:StartRendering(jobs));print('V29_RENDER_STARTED')"
(O/'build-and-render.lua').write_text('local ok,e=pcall(function()\n'+code+"\nend);print('V29_RESULT',ok,e)")
print('Native assembly prepared')
