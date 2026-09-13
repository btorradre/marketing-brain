local pm=r:GetProjectManager() local old=pm:GetCurrentProject() local previous=old and old:GetName() or "none"
if old then assert(not old:IsRenderingInProgress()) if previous~="Untitled Project" then assert(pm:SaveProject()) end end
local name="VEL_Eleanor_OldMoney_ContinuousPresenter_R3_2026-09-11"
for _,n in pairs(pm:GetProjectListInCurrentFolder()) do assert(n~=name,"Already exists: inspect before reuse") end
local p=pm:CreateProject(name) assert(p) assert(p:SetSetting("timelineResolutionWidth","1080")) assert(p:SetSetting("timelineResolutionHeight","1920")) assert(p:SetSetting("timelineFrameRate","30")) assert(pm:SaveProject())
return {previous=previous,name=p:GetName()}
