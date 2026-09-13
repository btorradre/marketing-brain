local p=r:GetProjectManager():GetCurrentProject()
assert(p:GetName()=="VEL_Eleanor_OldMoney_9Ads_2026-09-11")
local t=p:GetCurrentTimeline() local item=t:GetItemListInTrack("video",1)[1]
local c=item:GetFusionCompByIndex(1) c:Lock()
local k=c:FindTool("DeltaKeyer1")
k:SetInput("BackgroundRed",0.0431) k:SetInput("BackgroundGreen",0.6902) k:SetInput("BackgroundBlue",0.1882)
k:SetInput("LowThreshold",0.04) k:SetInput("HighThreshold",0.96)
k:ConnectInput("Input",c:FindTool("MediaIn1"))
local b=c:AddTool("Background") b:SetInput("TopLeftRed",0.88) b:SetInput("TopLeftGreen",0.86) b:SetInput("TopLeftBlue",0.81) b:SetInput("Width",1080) b:SetInput("Height",1920)
local m=c:AddTool("Merge") m:ConnectInput("Background",b) m:ConnectInput("Foreground",k)
c:FindTool("MediaOut1"):ConnectInput("Input",m)
c:Unlock()
t:SetCurrentTimecode("01:00:01:00") r:GetProjectManager():SaveProject()
local path=[=[/Users/brooksorradre2/Documents/marketing brain/brands/velantra/creative/old-money-look-2026-09-10/production/qa/native-key-test.jpg]=]
local ok=p:ExportCurrentFrameAsStill(path)
return {export=ok,path=path,start=t:GetStartFrame(),nodes={key=k:GetAttrs().TOOLS_Name,merge=m:GetAttrs().TOOLS_Name}}
