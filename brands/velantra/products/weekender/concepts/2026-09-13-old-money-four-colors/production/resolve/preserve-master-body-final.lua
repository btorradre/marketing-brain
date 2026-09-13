local image="/Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/weekender/concepts/2026-09-13-old-money-four-colors/storyboard/assets/fourcolorgridselected.png"

local pm=r:GetProjectManager() local p=pm:GetCurrentProject() assert(p:GetName()=="VEL_Weekender_OldMoney_FourColors_20260913") local t=p:GetCurrentTimeline() local items=t:GetItemListInTrack("video",1) assert(#items==2)
local c=items[2] assert(c:GetStart()==358 and c:GetEnd()==1538,"Inspect unexpected master body range") local m=c:GetMediaPoolItem() assert(t:DeleteClips({c},false))
local clips=p:GetMediaPool():AppendToTimeline({{mediaPoolItem=m,startFrame=358,endFrame=1539,mediaType=1,trackIndex=1,recordFrame=358}}) assert(clips and #clips==1) c=clips[1] assert(c:GetStart()==358 and c:GetEnd()==1539)
local first=t:GetItemListInTrack("video",1)[1] assert(first:GetMediaPoolItem():ReplaceClip(image)) assert(first:GetStart()==0 and first:GetEnd()==358)
assert(#t:GetItemListInTrack("video",2)==3) assert(#t:GetItemListInTrack("video",3)==6) assert(t:GetEndFrame()==1539) assert(pm:SaveProject())
return {project=p:GetName(),timeline=t:GetName(),bodyStart=c:GetStart(),bodyEnd=c:GetEnd(),hookEnd=first:GetEnd(),video1=#t:GetItemListInTrack("video",1),presenterSegments=#t:GetItemListInTrack("video",2),captionSegments=#t:GetItemListInTrack("video",3),frames=t:GetEndFrame()}
