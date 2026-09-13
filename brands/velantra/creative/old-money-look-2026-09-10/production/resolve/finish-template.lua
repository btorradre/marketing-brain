local pm=r:GetProjectManager() local p=pm:GetCurrentProject()
assert(p:GetName()=="VEL_Eleanor_OldMoney_9Ads_2026-09-11","Wrong project")
local pool=p:GetMediaPool()
local t=pool:ImportTimelineFromFile(ad.otio,{timelineName=ad.ad_id}) assert(t,"Import failed")
p:SetCurrentTimeline(t)
local items=t:GetItemListInTrack("video",2)
assert(#items==#ad.presenter_layout,"Presenter clip count mismatch "..#items.." vs "..#ad.presenter_layout)
for i,item in ipairs(items) do
 local layout=ad.presenter_layout[i]
 local c=item:AddFusionComp() assert(c,"No comp") c:Lock()
 local mi=c:FindTool("MediaIn1") local mo=c:FindTool("MediaOut1") assert(mi and mo,"Missing media nodes")
 local subject=mi
 if ad.avatar_id~="A1" then
  local k=c:AddTool("DeltaKeyer") assert(k)
  k:SetInput("BackgroundRed",ad.green[1]) k:SetInput("BackgroundGreen",ad.green[2]) k:SetInput("BackgroundBlue",ad.green[3])
  k:SetInput("LowThreshold",0.04) k:SetInput("HighThreshold",0.96)
  k:ConnectInput("Input",mi) subject=k
 end
 if layout.mode=="presenter_hold" then
  local b=c:AddTool("Background") b:SetInput("TopLeftRed",0.88) b:SetInput("TopLeftGreen",0.86) b:SetInput("TopLeftBlue",0.81) b:SetInput("Width",1080) b:SetInput("Height",1920)
  local m=c:AddTool("Merge") m:ConnectInput("Background",b) m:ConnectInput("Foreground",subject) subject=m
 end
 mo:ConnectInput("Input",subject) c:Unlock()
 local compPath=[=[/Users/brooksorradre2/Documents/marketing brain/brands/velantra/creative/old-money-look-2026-09-10/production/resolve/comps/]=]..ad.ad_id.."-"..i..".comp"
 assert(item:ExportFusionComp(compPath,1),"Comp serialization failed")
 assert(item:ImportFusionComp(compPath),"Comp activation failed")
 if layout.mode=="overlay" then
  local pan=320 if layout.pretrim_start<180 then pan=0 end
  assert(item:SetProperties({ZoomX=0.34,ZoomY=0.34,Pan=pan,Tilt=-633.6,RetimeProcess=0}),"Transform failed")
 else assert(item:SetProperties({ZoomX=1,ZoomY=1,Pan=0,Tilt=0,RetimeProcess=0}),"Hold transform failed") end
end
assert(pm:SaveProject(),"Save failed")
return {name=t:GetName(),id=t:GetUniqueId(),start=t:GetStartFrame(),end_frame=t:GetEndFrame(),video_tracks=t:GetTrackCount("video"),audio_tracks=t:GetTrackCount("audio"),presenter_clips=#items}
