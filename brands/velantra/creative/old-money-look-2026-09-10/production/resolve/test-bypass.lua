r:OpenPage("edit") local p=r:GetProjectManager():GetCurrentProject() local t=p:GetCurrentTimeline()
t:SetCurrentTimecode("00:00:01:00")
return {export=p:ExportCurrentFrameAsStill([=[/Users/brooksorradre2/Documents/marketing brain/brands/velantra/creative/old-money-look-2026-09-10/production/qa/bypass-check.jpg]=])}
