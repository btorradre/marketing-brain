local p=fu:GetResolve():GetProjectManager():GetCurrentProject()
print('RENDERING',p:IsRenderingInProgress());for _,j in ipairs(p:GetRenderJobList()) do for k,v in pairs(j) do print(k,v) end end
