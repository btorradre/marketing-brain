local p=r:GetProjectManager():GetCurrentProject() local t=p:GetCurrentTimeline()
local item=t:GetItemListInTrack("video",2)[1] local c=item:GetFusionCompByIndex(1)
local k=c:FindTool("DeltaKeyer1") local mo=c:FindTool("MediaOut1")
return {keyin=k.Input:GetConnectedOutput():GetTool():GetAttrs().TOOLS_Name,outin=mo.Input:GetConnectedOutput():GetTool():GetAttrs().TOOLS_Name,red=k:GetInput("BackgroundRed"),green=k:GetInput("BackgroundGreen"),blue=k:GetInput("BackgroundBlue"),low=k:GetInput("LowThreshold"),high=k:GetInput("HighThreshold"),attrs={keypass=k:GetAttrs().TOOLB_PassThrough,compglobal=c:GetAttrs().COMPN_GlobalStart,compend=c:GetAttrs().COMPN_GlobalEnd}}
