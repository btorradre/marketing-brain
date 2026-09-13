local output="/Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/weekender/concepts/2026-09-13-old-money-four-colors/production/exports"

local pm=r:GetProjectManager() local p=pm:GetCurrentProject() assert(p:GetName()=="VEL_Weekender_OldMoney_FourColors_20260913") local t=p:GetCurrentTimeline() assert(t:GetName()=="Weekender-OldMoney-FourColors") assert(not p:IsRenderingInProgress()) assert(t:GetEndFrame()==1539)
assert(p:SetCurrentRenderFormatAndCodec("mp4","H264")) assert(p:SetCurrentRenderMode(1))
assert(p:SetRenderSettings({SelectAllFrames=true,TargetDir=output,CustomName="Weekender-OldMoney-FourColors-Final",ExportVideo=true,ExportAudio=true,FormatWidth=1080,FormatHeight=1920,FrameRate=30,VideoQuality=16000,AudioCodec="aac",AudioSampleRate=48000,NetworkOptimization=true}))
local id=p:AddRenderJob() assert(id) assert(pm:SaveProject()) return {job=id,started=p:StartRendering({id}),project=p:GetName(),timeline=t:GetName(),frames=t:GetEndFrame()}
