local pm=r:GetProjectManager()
local old=pm:GetCurrentProject()
assert(not old:IsRenderingInProgress(),"Render active")
assert(pm:SaveProject(),"Save outgoing failed")
local name="VEL_Weekender_EuropeanTravel_FourColors_20260913"
for _,n in pairs(pm:GetProjectListInCurrentFolder()) do assert(n~=name,"Isolated project already exists") end
assert(pm:ImportProject([=[/Users/brooksorradre2/Documents/marketing brain/brands/velantra/creative/eleanor-european-travel-2026-09-11/production/exports/Eleanor-EuropeanTravel-Tight.drp]=],name),"Import failed")
local p=pm:LoadProject(name);assert(p,"Load failed")
local chosen=nil
local names={}
for i=1,p:GetTimelineCount() do local x=p:GetTimelineByIndex(i);names[i]=x:GetName();if x:GetName()=="Eleanor-EuropeanTravel-Tight" then chosen=x end end
assert(chosen,"Exact Tight timeline missing")
assert(p:SetCurrentTimeline(chosen))
local t=chosen:DuplicateTimeline("Eleanor-EuropeanTravel-FourColors");assert(t,"Duplicate timeline failed")
assert(p:SetCurrentTimeline(t))
assert(pm:SaveProject())
return {project=p:GetName(),prior=old:GetName(),timelines=names,timeline=t:GetName(),start=t:GetStartFrame(),finish=t:GetEndFrame(),video_tracks=t:GetTrackCount("video"),audio_tracks=t:GetTrackCount("audio")}
