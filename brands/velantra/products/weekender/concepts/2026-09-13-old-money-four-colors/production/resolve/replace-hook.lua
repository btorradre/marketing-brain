local path="/Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/weekender/concepts/2026-09-13-old-money-four-colors/storyboard/assets/fourcolorgrid.png"

local pm=r:GetProjectManager() local p=pm:GetCurrentProject() assert(p:GetName()=="VEL_Weekender_OldMoney_FourColors_20260913") local t=p:GetCurrentTimeline() assert(t:GetName()=="Weekender-OldMoney-FourColors")
local first=t:GetItemListInTrack("video",1)[1] assert(first:GetStart()==0 and first:GetEnd()==358)
local imported=p:GetMediaPool():ImportMedia({path}) assert(imported and #imported==1)
local added=first:AddTake(imported[1],0,357) assert(added,"AddTake failed")
local count=first:GetTakesCount() assert(first:SelectTakeByIndex(count)) assert(first:FinalizeTake())
assert(first:GetStart()==0 and first:GetEnd()==358) assert(pm:SaveProject())
return {project=p:GetName(),timeline=t:GetName(),new_source=first:GetMediaPoolItem():GetClipProperty("File Path"),duration=first:GetDuration(),properties=first:GetProperty()}
