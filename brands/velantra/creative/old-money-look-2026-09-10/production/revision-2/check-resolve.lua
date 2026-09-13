local pm=r:GetProjectManager()
local p=pm:GetCurrentProject()
return {version=r:GetVersionString(),project=p and p:GetName(),timelines=p and p:GetTimelineCount()}
