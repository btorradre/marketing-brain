local pm=r:GetProjectManager();local p=pm:GetCurrentProject();assert(p:GetName()=="VEL_Weekender_EuropeanTravel_FourColors_20260913");assert(not p:IsRenderingInProgress());local t=p:GetCurrentTimeline();assert(t:GetName()=="Eleanor-EuropeanTravel-FourColors")
local duplicates={}
for i=1,p:GetTimelineCount() do local v=p:GetTimelineByIndex(i);if v:GetUniqueId()~=t:GetUniqueId() then table.insert(duplicates,v) end end
if #duplicates>0 then assert(p:GetMediaPool():DeleteTimelines(duplicates),"Cleanup isolated imported copies failed") end
assert(p:GetTimelineCount()==1)
assert(pm:SaveProject())
local dp=pm:ExportProject(p:GetName(),[=[/Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/weekender/concepts/2026-09-13-european-travel-four-colors/production/exports/Eleanor-EuropeanTravel-FourColors.drp]=]);assert(dp,"/Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/weekender/concepts/2026-09-13-european-travel-four-colors/production/exports/Eleanor-EuropeanTravel-FourColors.drp export failed")
local dt=t:Export([=[/Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/weekender/concepts/2026-09-13-european-travel-four-colors/production/exports/Eleanor-EuropeanTravel-FourColors.drt]=],r.EXPORT_DRT);assert(dt,"/Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/weekender/concepts/2026-09-13-european-travel-four-colors/production/exports/Eleanor-EuropeanTravel-FourColors.drt export failed")
return {project=p:GetName(),timeline=t:GetName(),timeline_count=p:GetTimelineCount(),duration=t:GetEndFrame(),drp=dp,drt=dt,original_external_project_preserved=true}
