local pm=r:GetProjectManager() local p=pm:GetCurrentProject()
assert(p:GetName()=="VEL_Eleanor_OldMoney_9Ads_2026-09-11") assert(not p:IsRenderingInProgress())
local jobs={}
for i=1,p:GetTimelineCount() do local t=p:GetTimelineByIndex(i)
 if t:GetName():match("^VEL%-OM%-H") then
 p:SetCurrentTimeline(t) assert(p:SetCurrentRenderFormatAndCodec("mp4","H264"))
 assert(p:SetRenderSettings({SelectAllFrames=true,TargetDir=[=[/Users/brooksorradre2/Documents/marketing brain/brands/velantra/creative/old-money-look-2026-09-10/production/exports]=],CustomName=t:GetName(),ExportVideo=true,ExportAudio=true,FormatWidth=1080,FormatHeight=1920,FrameRate=30,VideoQuality=6000,AudioCodec="aac",AudioSampleRate=48000,NetworkOptimization=true}))
 local id=p:AddRenderJob() assert(id) jobs[#jobs+1]=id
 end
end
assert(#jobs==9,"Expected nine jobs") assert(pm:SaveProject())
local started=p:StartRendering(jobs)
return {jobs=jobs,started=started}
