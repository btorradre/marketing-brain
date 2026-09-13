local pm=r:GetProjectManager() local p=pm:GetCurrentProject() local t=p:GetCurrentTimeline()
assert(t:GetName()=="VEL-OM-H1-A2")
local list=t:GetItemListInTrack("video",1) local last=list[#list]
local replaced=last:GetMediaPoolItem():ReplaceClip([=[/Users/brooksorradre2/Documents/marketing brain/brands/velantra/creative/old-money-look-2026-09-10/production/resolve/end-hold-one.jpg]=])
assert(replaced,"Could not replace still")
local loaded=0 for _,item in ipairs(t:GetItemListInTrack("video",2)) do
 if item:LoadFusionCompByName("Composition 1") then loaded=loaded+1 end
end
assert(pm:SaveProject())
assert(p:SetCurrentRenderFormatAndCodec("mp4","H264"))
assert(p:SetRenderSettings({SelectAllFrames=true,TargetDir=[=[/Users/brooksorradre2/Documents/marketing brain/brands/velantra/creative/old-money-look-2026-09-10/production/qa]=],CustomName="H1-A2-review",ExportVideo=true,ExportAudio=true,FormatWidth=1080,FormatHeight=1920,FrameRate=30,VideoQuality=12000,AudioCodec="aac",AudioSampleRate=48000,NetworkOptimization=true}))
local id=p:AddRenderJob() assert(id) local started=p:StartRendering({id})
return {job=id,started=started,loaded=loaded,replaced=replaced,stilltype=last:GetMediaPoolItem():GetClipProperty("Type")}
