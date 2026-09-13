local p=r:GetProjectManager():GetCurrentProject() local t=p:GetCurrentTimeline() local item=t:GetItemListInTrack("video",2)[1]
local path=[=[/Users/brooksorradre2/Documents/marketing brain/brands/velantra/creative/old-money-look-2026-09-10/production/resolve/first-presenter.comp]=]
assert(item:ExportFusionComp(path,1),"export comp failed")
local comp=item:ImportFusionComp(path) assert(comp,"Import comp failed")
r:GetProjectManager():SaveProject()
t:SetCurrentTimecode("00:00:01:00")
return {still=p:ExportCurrentFrameAsStill([=[/Users/brooksorradre2/Documents/marketing brain/brands/velantra/creative/old-money-look-2026-09-10/production/qa/reimport-comp.jpg]=]),names=item:GetFusionCompNameList()}
