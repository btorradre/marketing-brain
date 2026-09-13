local drp="/Users/brooksorradre2/Documents/marketing brain/brands/velantra/creative/old-money-look-2026-09-10/production/final-nine-ads/Eleanor-OldMoney-R3.drp" local image="/Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/weekender/concepts/2026-09-13-old-money-four-colors/storyboard/assets/fourcolorgridselected.png" local master="/Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/weekender/concepts/2026-09-13-old-money-four-colors/production/source/original-master.mp4"

local pm=r:GetProjectManager() local p=pm:GetCurrentProject() assert(not p:IsRenderingInProgress()) assert(pm:SaveProject())
local name="VEL_Weekender_OldMoney_FourColors_Final_20260913"
for _,n in pairs(pm:GetProjectListInCurrentFolder()) do assert(n~=name,"Final project already exists") end
assert(pm:ImportProject(drp,name)) p=pm:LoadProject(name) assert(p)
local t=nil for i=1,p:GetTimelineCount() do local candidate=p:GetTimelineByIndex(i) if candidate:GetName()=="VEL-OM-H1-A3-R3" then t=candidate end end assert(t) assert(p:SetCurrentTimeline(t)) assert(t:SetName("Weekender-OldMoney-FourColors-Final"))
local remove={} for track=1,3 do for _,c in ipairs(t:GetItemListInTrack("video",track)) do if c:GetStart()>=358 then table.insert(remove,c) else assert(c:GetEnd()<=358) end end end assert(#remove==41) assert(t:DeleteClips(remove,false))
local imported=p:GetMediaPool():ImportMedia({master}) assert(imported and #imported==1)
local clips=p:GetMediaPool():AppendToTimeline({{mediaPoolItem=imported[1],startFrame=358,endFrame=1539,mediaType=1,trackIndex=1,recordFrame=358}}) assert(clips and #clips==1) assert(clips[1]:GetStart()==358 and clips[1]:GetEnd()==1539)
local first=t:GetItemListInTrack("video",1)[1] assert(first:GetMediaPoolItem():ReplaceClip(image)) assert(first:GetStart()==0 and first:GetEnd()==358)
local others={} for i=1,p:GetTimelineCount() do local x=p:GetTimelineByIndex(i) if x:GetName()~=t:GetName() then table.insert(others,x) end end assert(#others==8) assert(p:GetMediaPool():DeleteTimelines(others))
assert(pm:SaveProject())
return {project=p:GetName(),timeline=t:GetName(),timelines=p:GetTimelineCount(),frames=t:GetEndFrame(),presenter=t:GetItemListInTrack("video",2)[1]:GetMediaPoolItem():GetClipProperty("File Path"),caption=t:GetItemListInTrack("video",3)[1]:GetMediaPoolItem():GetClipProperty("File Path")}
