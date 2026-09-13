local pm=r:GetProjectManager()
local old=pm:GetCurrentProject()
local oldName=old and old:GetName() or "none"
if old then assert(pm:SaveProject(),"Could not save existing project") end
local base="VEL_Eleanor_OldMoney_9Ads_2026-09-11"
local names=pm:GetProjectListInCurrentFolder()
local used={} for _,name in pairs(names) do used[name]=true end
local name=base local n=2 while used[name] do name=base.."_"..n n=n+1 end
local p=pm:CreateProject(name) assert(p,"Create project failed")
assert(p:SetSettings({timelineResolutionWidth="1080",timelineResolutionHeight="1920",timelineFrameRate="30"}),"Settings failed")
assert(pm:SaveProject(),"Save failed")
return {project=name,previous_saved=oldName,formats=p:GetRenderFormats(),codecs=p:GetRenderCodecs("mp4")}
