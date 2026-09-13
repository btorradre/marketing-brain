local p=r:GetProjectManager():GetCurrentProject() local t=p:GetCurrentTimeline()
assert(t:GetName()=="VEL-OM-H1-A2") t:SetCurrentTimecode("00:00:01:00")
r:OpenPage("fusion")
local c=t:GetItemListInTrack("video",2)[1]:GetFusionCompByIndex(1)
local keys={} for k,v in pairs(p:GetSettings()) do if k:lower():match("bypass") or k:lower():match("fusion") then keys[k]=v end end
local still=p:ExportCurrentFrameAsStill([=[/Users/brooksorradre2/Documents/marketing brain/brands/velantra/creative/old-money-look-2026-09-10/production/qa/fusion-view-check.jpg]=])
return {settings=keys,still=still,page=r:GetCurrentPage()}
