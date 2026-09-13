local ad={[ [=[name]=] ]=[=[VEL-OM-H1-A1-R2]=],[ [=[original_id]=] ]=[=[VEL-OM-H1-A1]=],[ [=[hook_id]=] ]=[=[H1]=],[ [=[duration_frames]=] ]=1539,[ [=[otio]=] ]=[=[/Users/brooksorradre2/Documents/marketing brain/brands/velantra/creative/old-money-look-2026-09-10/production/revision-2/resolve/VEL-OM-H1-A1-R2.otio]=],[ [=[visual_clips]=] ]=15,[ [=[audio_clips]=] ]=11}
local pm=r:GetProjectManager() local p=pm:GetCurrentProject() assert(p:GetName()=="VEL_Eleanor_OldMoney_RawPhone_R2_2026-09-11") local pool=p:GetMediaPool()
local old=p:GetCurrentTimeline() assert(old:GetName()==ad.name) assert(old:SetName(ad.name.."-IMPORT-CHECK"))
local t=pool:ImportTimelineFromFile(ad.otio,{timelineName=ad.name}) assert(t,"Import failed") p:SetCurrentTimeline(t)
local v=t:GetItemListInTrack("video",1) local props=v[1]:GetMediaPoolItem():GetClipProperty()
assert(pm:SaveProject()) return {name=t:GetName(),finish=t:GetEndFrame(),first=props,clipprops=v[1]:GetProperty() }