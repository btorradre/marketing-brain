local path="/Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/weekender/concepts/2026-09-13-old-money-four-colors/storyboard/assets/fourcolorgrid.png"

local pm=r:GetProjectManager() local p=pm:GetCurrentProject() assert(p:GetName()=="VEL_Weekender_OldMoney_FourColors_20260913")
local bad=p:GetCurrentTimeline() assert(bad:GetName()=="Weekender-OldMoney-FourColors") assert(bad:SetName("Weekender-OldMoney-TakeProbe-Rejected"))
local original=nil for i=1,p:GetTimelineCount() do local t=p:GetTimelineByIndex(i) if t:GetName()=="VEL-OM-H1-A3-R3" then original=t end end assert(original)
local t=original:DuplicateTimeline("Weekender-OldMoney-FourColors") assert(p:SetCurrentTimeline(t))
local c=t:GetItemListInTrack("video",1)[1] assert(c:GetStart()==0 and c:GetEnd()==358)
local replaced=c:GetMediaPoolItem():ReplaceClip(path) assert(replaced,"ReplaceClip failed")
assert(c:GetStart()==0 and c:GetEnd()==358,"Duration changed") assert(t:GetEndFrame()==1539)
assert(pm:SaveProject())
return {project=p:GetName(),timeline=t:GetName(),start=c:GetStart(),ending=c:GetEnd(),source=c:GetMediaPoolItem():GetClipProperty("File Path"),track1clips=#t:GetItemListInTrack("video",1),timelineEnd=t:GetEndFrame()}
