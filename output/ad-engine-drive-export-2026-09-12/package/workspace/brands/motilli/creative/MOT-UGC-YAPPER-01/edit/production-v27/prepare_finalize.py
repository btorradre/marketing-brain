from pathlib import Path
import json
O=Path(__file__).resolve().parent
for h in ['H1','H2','H3']:
 S=O/h;d=json.loads((S/'timeline-spec.json').read_text());total=d['frames']
 code="""local r=fu:GetResolve();local pm=r:GetProjectManager();local p=pm:GetCurrentProject();assert(not p:IsRenderingInProgress());if p:GetName()~='MOT-UGC-YAPPER-01 v7 V3 20260910' then assert(pm:SaveProject());p=pm:LoadProject('MOT-UGC-YAPPER-01 v7 V3 20260910');assert(p) end;local mp=p:GetMediaPool();local t=nil;for i=1,p:GetTimelineCount() do local q=p:GetTimelineByIndex(i);if q:GetName()==__OLDNAME__ or q:GetName()==__FINALNAME__ then t=q end end;assert(t);assert(p:SetCurrentTimeline(t));assert(t:GetEndFrame()==__FRAMES__)
local clips=t:GetItemListInTrack('video',1);if #clips==0 then local m=mp:ImportMedia({__VIDEO__})[1];assert(m);local c=mp:AppendToTimeline({{mediaPoolItem=m,startFrame=0,endFrame=__FRAMES__,recordFrame=0,trackIndex=1,mediaType=1}})[1];assert(c and c:GetStart()==0 and c:GetEnd()==__FRAMES__);assert(c:SetProperty({ZoomX=1,ZoomY=1,Pan=0,Tilt=0,CropLeft=0,CropRight=0,CropTop=0,CropBottom=0})) end
assert(#t:GetItemListInTrack('video',1)==1);assert(#t:GetItemListInTrack('video',2)==24);assert(#t:GetItemListInTrack('video',3)==__CAPS__);assert(#t:GetItemListInTrack('audio',1)==1);assert(t:GetEndFrame()==__FRAMES__);assert(t:SetName(__FINALNAME__));t:SetTrackName('video',1,'Fresh HeyGen - Woman Over40 - 1.1x');assert(pm:SaveProject());assert(t:Export(__DRT__,r.EXPORT_DRT));assert(pm:ExportProject(p:GetName(),__DRP__));print('V27_FINAL_TIMELINE',t:GetName(),t:GetEndFrame())
p:SetCurrentRenderMode(1);assert(p:SetCurrentRenderSettings==nil or true);assert(p:SetCurrentRenderFormatAndCodec('mp4','H264'));assert(p:SetRenderSettings({TargetDir=__DEST__,CustomName=__FILENAME__,SelectAllFrames=true,ExportVideo=true,ExportAudio=true,FormatWidth=1080,FormatHeight=1920,FrameRate=30,VideoQuality=16000,AudioCodec='aac',AudioBitDepth=16,AudioSampleRate=48000}));local id=p:AddRenderJob();assert(id);print('V27_FINAL_RENDER_JOB',id);p:StartRendering(id)
"""
 # Method-name comparison isn't a Lua expression; retain only documented setters.
 code=code.replace('assert(p:SetCurrentRenderSettings==nil or true);','')
 vals={'__OLDNAME__':f'v27 {h} REBUILD r2 - awaiting HeyGen','__FINALNAME__':f'v27 {h} FINAL - 1.1x Woman Over40','__FRAMES__':total,'__CAPS__':len(json.loads((S/'caption-cues.json').read_text())),'__VIDEO__':str(S/'presenter-avatar-v-30fps.mp4'),'__DRT__':str(O/f'project-files/Motilli-V27-{h}-FINAL.drt'),'__DRP__':str(O/'project-files/Motilli-V27-FINAL.drp'),'__DEST__':str(O/'deliverables'),'__FILENAME__':f'Motilli-VSL-V27-{h}-1.1x'}
 for k,v in vals.items():code=code.replace(k,json.dumps(v) if isinstance(v,str) else str(v))
 (O/f'finalize-{h}.lua').write_text("local ok,err=pcall(function()\n"+code+"\nend);print('V27_FINALIZE_RESULT',ok,err)")
print('Three finalization scripts prepared; require verified new presenter before executing.')
