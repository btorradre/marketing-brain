local p=r:GetProjectManager():GetCurrentProject()
local t=p:GetCurrentTimeline() local item=t:GetItemListInTrack("video",1)[1]
local c=item:GetFusionCompByIndex(1) local k=c:FindTool("DeltaKeyer1")
local out={} for _,v in pairs(k:GetInputList()) do local a=v:GetAttrs() if a.INPS_ID:match("Background") or a.INPS_ID:match("Threshold") or a.INPS_ID:match("Clean") or a.INPS_ID:match("Pre") or a.INPS_ID:match("Erode") then out[a.INPS_ID]={name=a.INPS_Name,type=a.INPS_DataType,value=tostring(v[0])} end end
return {inputs=out,nodes=c:GetToolList(false) and "yes",properties=item:GetProperties()}
