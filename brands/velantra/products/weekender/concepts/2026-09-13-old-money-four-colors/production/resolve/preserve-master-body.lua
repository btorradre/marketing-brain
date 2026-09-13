local image="/Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/weekender/concepts/2026-09-13-old-money-four-colors/storyboard/assets/fourcolorgridselected.png" local master="/Users/brooksorradre2/Documents/marketing brain/brands/velantra/creative/old-money-look-2026-09-10/production/revision-3/exports/VEL-OM-H1-A3-R3.mp4"

local pm=r:GetProjectManager() local p=pm:GetCurrentProject() assert(p:GetName()=="VEL_Weekender_OldMoney_FourColors_20260913") assert(not p:IsRenderingInProgress()) local t=p:GetCurrentTimeline() assert(t:GetName()=="Weekender-OldMoney-FourColors")
local remove={} for track=1,3 do for _,c in ipairs(t:GetItemListInTrack("video",track)) do if c:GetStart()>=358 then table.insert(remove,c) else assert(c:GetEnd()<=358,"Hook clip crosses locked boundary") end end end
assert(#remove==41,"Unexpected body layer count")
assert(t:DeleteClips(remove,false))
local imported=p:GetMediaPool():ImportMedia({master}) assert(imported and #imported==1)
local clips=p:GetMediaPool():AppendToTimeline({{mediaPoolItem=imported[1],startFrame=358,endFrame=1538,mediaType=1,trackIndex=1,recordFrame=358}}) assert(clips and #clips==1)
local c=clips[1] assert(c:GetStart()==358 and c:GetEnd()==1539,"Master body range differs")
local first=t:GetItemListInTrack("video",1)[1] assert(first:GetMediaPoolItem():ReplaceClip(image)) assert(first:GetStart()==0 and first:GetEnd()==358)
assert(#t:GetItemListInTrack("video",2)==3) assert(#t:GetItemListInTrack("video",3)==6) assert(t:GetEndFrame()==1539)
assert(pm:SaveProject())
return {project=p:GetName(),timeline=t:GetName(),bodyStart=c:GetStart(),bodyEnd=c:GetEnd(),hookEnd=first:GetEnd(),video1=#t:GetItemListInTrack("video",1),presenterSegments=#t:GetItemListInTrack("video",2),captionSegments=#t:GetItemListInTrack("video",3),frames=t:GetEndFrame(),audioClips=#t:GetItemListInTrack("audio",1)}
