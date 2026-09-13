local pm=r:GetProjectManager() local p=pm:GetCurrentProject()
assert(p:GetName()=="VEL_Eleanor_OldMoney_9Ads_2026-09-11") assert(not p:IsRenderingInProgress())
local done={} local replaced={}
for i=1,p:GetTimelineCount() do local t=p:GetTimelineByIndex(i)
 if t:GetName():match("^VEL%-OM%-H") then
  for _,item in ipairs(t:GetItemListInTrack("audio",1)) do
   local media=item:GetMediaPoolItem() local id=media:GetMediaId()
   if not done[id] then
    local old=media:GetClipProperty("File Path")
    if old:match("narration%.mp3$") then local new=old:gsub("%.mp3$",".wav") assert(media:ReplaceClip(new),"Replace failed") replaced[#replaced+1]=new end
    done[id]=true
   end
  end
 end
end
assert(pm:SaveProject()) return {replaced=replaced}
