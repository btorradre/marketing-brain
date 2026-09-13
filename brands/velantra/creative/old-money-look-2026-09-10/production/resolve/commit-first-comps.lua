local p=r:GetProjectManager():GetCurrentProject() local t=p:GetCurrentTimeline()
assert(t:GetName()=="VEL-OM-H1-A2")
local count=0 for i,item in ipairs(t:GetItemListInTrack("video",2)) do
 local path=[=[/Users/brooksorradre2/Documents/marketing brain/brands/velantra/creative/old-money-look-2026-09-10/production/resolve/comps/]=].."VEL-OM-H1-A2-"..i..".comp"
 assert(item:ExportFusionComp(path,1)) assert(item:ImportFusionComp(path)) count=count+1
end
assert(r:GetProjectManager():SaveProject())
t:SetCurrentTimecode("00:00:05:00")
return {committed=count,still=p:ExportCurrentFrameAsStill([=[/Users/brooksorradre2/Documents/marketing brain/brands/velantra/creative/old-money-look-2026-09-10/production/qa/committed-hold.jpg]=])}
