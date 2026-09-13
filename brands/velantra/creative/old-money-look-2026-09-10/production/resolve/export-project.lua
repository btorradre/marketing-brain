local pm=r:GetProjectManager() local p=pm:GetCurrentProject()
assert(p:GetName()=="VEL_Eleanor_OldMoney_9Ads_2026-09-11") assert(not p:IsRenderingInProgress())
assert(pm:SaveProject())
local path=[=[/Users/brooksorradre2/Documents/marketing brain/brands/velantra/creative/old-money-look-2026-09-10/production/exports/Eleanor-OldMoney-9Ads.drp]=]
local ok=pm:ExportProject(p:GetName(),path,false)
return {exported=ok,path=path,project=p:GetName()}
