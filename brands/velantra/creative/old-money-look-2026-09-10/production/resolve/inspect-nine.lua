local p=r:GetProjectManager():GetCurrentProject() assert(p:GetName()=="VEL_Eleanor_OldMoney_9Ads_2026-09-11")
r:OpenPage("edit") local out={}
for i=1,p:GetTimelineCount() do local t=p:GetTimelineByIndex(i)
 if t:GetName():match("^VEL%-OM%-H") then
 p:SetCurrentTimeline(t) local shots={}
 for _,f in ipairs({30,180,t:GetEndFrame()-2}) do
  local tc=string.format("00:%02d:%02d:%02d",math.floor(f/1800)%60,math.floor(f/30)%60,f%30) t:SetCurrentTimecode(tc)
  local path=[=[/Users/brooksorradre2/Documents/marketing brain/brands/velantra/creative/old-money-look-2026-09-10/production/qa/]=]..t:GetName().."-native-"..f..".jpg"
  shots[tostring(f)]=p:ExportCurrentFrameAsStill(path)
 end
 local list=t:GetItemListInTrack("video",1) local last=list[#list]
 out[t:GetName()]={shots=shots,last_type=last:GetMediaPoolItem():GetClipProperty("Type"),duration=t:GetEndFrame()-t:GetStartFrame()}
 end
end
return out
