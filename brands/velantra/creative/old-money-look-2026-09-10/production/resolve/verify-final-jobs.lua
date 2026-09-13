local jobs={[=[e9db82d3-9b21-4da0-82cf-f510b35224d6]=],[=[086600ab-b505-4b80-a665-6f521026c524]=],[=[cb7cde97-368d-4c30-bc8b-029a21bcf028]=],[=[3654b6e0-a8cf-4ef8-beb0-3e2575be1dd3]=],[=[7f6a5614-366e-41e2-9e16-64aa1a85042a]=],[=[f97eba96-a336-41f8-8750-1e1e4ac28739]=],[=[02274365-0e60-4bea-83a7-b608cda685ed]=],[=[50d4db93-41e8-4237-8106-e7459c301c96]=],[=[926ec054-4ac9-49d8-881d-220c78eaa1ff]=]}
local p=r:GetProjectManager():GetCurrentProject() local out={}
for _,id in ipairs(jobs) do out[id]=p:GetRenderJobStatus(id).JobStatus end
return {running=p:IsRenderingInProgress(),jobs=out}
