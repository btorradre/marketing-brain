local name="VEL_Weekender_OldMoney_FourColors_20260913" local path="/Users/brooksorradre2/Documents/marketing brain/brands/velantra/creative/old-money-look-2026-09-10/production/final-nine-ads/Eleanor-OldMoney-R3.drp"

local pm=r:GetProjectManager() local outgoing=pm:GetCurrentProject() assert(not outgoing:IsRenderingInProgress()) assert(pm:SaveProject())
for _,n in pairs(pm:GetProjectListInCurrentFolder()) do assert(n~=name,"Isolated project already exists; inspect instead") end
assert(pm:ImportProject(path,name),"ImportProject failed")
local p=pm:LoadProject(name) assert(p and p:GetName()==name)
local original=nil for i=1,p:GetTimelineCount() do local t=p:GetTimelineByIndex(i) if t:GetName()=="VEL-OM-H1-A3-R3" then original=t end end assert(original,"Exact source timeline not found")
local t=original:DuplicateTimeline("Weekender-OldMoney-FourColors") assert(t) assert(p:SetCurrentTimeline(t)) assert(pm:SaveProject())
local info={} for i,c in ipairs(t:GetItemListInTrack("video",1)) do info[i]={name=c:GetName(),start=c:GetStart(),ending=c:GetEnd(),media=c:GetMediaPoolItem():GetClipProperty("File Path")} end
return {project=p:GetName(),timeline=t:GetName(),start=t:GetStartFrame(),ending=t:GetEndFrame(),track1=info}
