local pm=r:GetProjectManager() local old=pm:GetCurrentProject() local oldname=old and old:GetName() or "none" if old then assert(not old:IsRenderingInProgress(),"Current project is rendering") assert(pm:SaveProject(),"Cannot save current project") end
local name="VEL_Eleanor_OldMoney_RawPhone_R2_2026-09-11"
local existing=pm:GetProjectListInCurrentFolder() for _,v in pairs(existing) do assert(v~=name,"R2 already exists; inspect before loading") end
local p=pm:CreateProject(name) assert(p,"Create failed")
assert(p:SetSetting("timelineResolutionWidth","1080")) assert(p:SetSetting("timelineResolutionHeight","1920")) assert(p:SetSetting("timelineFrameRate","30"))
assert(pm:SaveProject()) return {previous_project=oldname,project=p:GetName(),settings=p:GetSetting()}