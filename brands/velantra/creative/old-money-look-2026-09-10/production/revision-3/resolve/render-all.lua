local names={[=[VEL-OM-H1-A1-R3]=],[=[VEL-OM-H1-A2-R3]=],[=[VEL-OM-H1-A3-R3]=],[=[VEL-OM-H2-A1-R3]=],[=[VEL-OM-H2-A2-R3]=],[=[VEL-OM-H2-A3-R3]=],[=[VEL-OM-H3-A1-R3]=],[=[VEL-OM-H3-A2-R3]=],[=[VEL-OM-H3-A3-R3]=]}
local output=[=[/Users/brooksorradre2/Documents/marketing brain/brands/velantra/creative/old-money-look-2026-09-10/production/revision-3/exports]=]

local pm=r:GetProjectManager() local p=pm:GetCurrentProject()
assert(p:GetName()=="VEL_Eleanor_OldMoney_ContinuousPresenter_R3_2026-09-11") assert(not p:IsRenderingInProgress())
assert(p:GetTimelineCount()==9,"Expected nine timelines")
local jobs={} local result={}
for _,name in ipairs(names) do
 local t=nil for i=1,p:GetTimelineCount() do local candidate=p:GetTimelineByIndex(i) if candidate:GetName()==name then t=candidate end end
 assert(t,"Missing "..name) p:SetCurrentTimeline(t)
 assert(t:GetTrackCount("video")==3)
 assert(p:SetCurrentRenderFormatAndCodec("mp4","H264")) assert(p:SetCurrentRenderMode(1))
 assert(p:SetRenderSettings({SelectAllFrames=true,TargetDir=output,CustomName=name,ExportVideo=true,ExportAudio=true,FormatWidth=1080,FormatHeight=1920,FrameRate=30,VideoQuality=12000,AudioCodec="aac",AudioSampleRate=48000,NetworkOptimization=true}))
 local id=p:AddRenderJob() assert(id) jobs[#jobs+1]=id result[#result+1]={name=name,job=id}
end
assert(pm:SaveProject())
assert(pm:ExportProject(p:GetName(),output.."/Eleanor-OldMoney-R3.drp"),"Project export failed")
return {jobs=result,started=p:StartRendering(jobs),project=p:GetName()}
