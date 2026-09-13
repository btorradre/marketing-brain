local p=r:GetProjectManager():GetCurrentProject()
local out={} for _,j in ipairs(p:GetRenderJobList()) do out[j.JobId or j.jobId or tostring(_)]=p:GetRenderJobStatus(j.JobId or j.jobId) end
return {running=p:IsRenderingInProgress(),jobs=out}
