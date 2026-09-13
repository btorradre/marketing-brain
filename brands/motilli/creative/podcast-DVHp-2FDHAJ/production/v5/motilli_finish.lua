local r=fu:GetResolve();local pm=r:GetProjectManager();local p=pm:GetCurrentProject();local t=p:GetCurrentTimeline();print('CURRENT',t:GetName(),t:GetEndFrame());print('RENDERING',p:IsRenderingInProgress());local jobs=p:GetRenderJobList();local j=jobs[#jobs];print('LATEST_JOB',j.JobId);for k,v in pairs(p:GetRenderJobStatus(j.JobId)) do print(k,v) end
if not p:IsRenderingInProgress() and t:GetName()=='Motilli Podcast v5 Final 04' then
 local d='/Users/brooksorradre2/Documents/marketing brain/brands/motilli/creative/podcast-DVHp-2FDHAJ/production/v5/deliverables/';print('DRP',pm:ExportProject(p:GetName(),d..'Motilli-Podcast-Final.drp',false));print('DRT',t:Export(d..'Motilli-Podcast-Final.drt',r.EXPORT_DRT));pm:SaveProject()
end
