local r=fu:GetResolve();local pm=r:GetProjectManager();local p=pm:GetCurrentProject();print('RENDERING',p:IsRenderingInProgress());local status=p:GetRenderJobStatus('21a27bf6-0eac-447a-9192-ec4a1389ffc3');for k,v in pairs(status) do print(k,v) end
if not p:IsRenderingInProgress() then
 local base='/Users/brooksorradre2/Documents/marketing brain/brands/motilli/creative/podcast-DVHp-2FDHAJ/production/v5/deliverables/'
 print('PROJECT_EXPORT',pm:ExportProject(p:GetName(),base..'Motilli-Podcast-HeyGen-v5.drp',false))
 local t=p:GetCurrentTimeline();print('TIMELINE_EXPORT',t:Export(base..'Motilli-Podcast-HeyGen-v5.drt',r.EXPORT_DRT))
 pm:SaveProject()
end
