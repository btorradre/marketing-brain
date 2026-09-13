local output="/Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/weekender/concepts/2026-09-13-old-money-four-colors/production/qa"

local pm=r:GetProjectManager() local p=pm:GetCurrentProject() assert(p:GetName()=="VEL_Weekender_OldMoney_FourColors_20260913") local t=p:GetCurrentTimeline() assert(t:GetName()=="Weekender-OldMoney-FourColors") assert(not p:IsRenderingInProgress()) assert(t:GetEndFrame()==1539)
assert(p:SetCurrentRenderFormatAndCodec("mp4","H264")) assert(p:SetCurrentRenderMode(1))
assert(p:SetRenderSettings({SelectAllFrames=true,TargetDir=output,CustomName="Weekender-OldMoney-FourColors-Probe",ExportVideo=true,ExportAudio=true,FormatWidth=1080,FormatHeight=1920,FrameRate=30,VideoQuality=12000,AudioCodec="aac",AudioSampleRate=48000,NetworkOptimization=true}))
local id=p:AddRenderJob() assert(id) assert(pm:SaveProject()) local started=p:StartRendering({id}) return {job=id,started=started,project=p:GetName(),timeline=t:GetName(),frames=t:GetEndFrame()}
