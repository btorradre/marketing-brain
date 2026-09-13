local r=fu:GetResolve();local p=r:GetProjectManager():GetCurrentProject();print('CURRENT_PROJECT',p and p:GetName() or 'NONE');if p then print('RENDERING',p:IsRenderingInProgress()) end
