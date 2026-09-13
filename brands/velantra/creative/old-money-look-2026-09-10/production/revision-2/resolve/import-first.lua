local ad={[ [=[name]=] ]=[=[VEL-OM-H1-A1-R2]=],[ [=[original_id]=] ]=[=[VEL-OM-H1-A1]=],[ [=[hook_id]=] ]=[=[H1]=],[ [=[duration_frames]=] ]=1539,[ [=[otio]=] ]=[=[/Users/brooksorradre2/Documents/marketing brain/brands/velantra/creative/old-money-look-2026-09-10/production/revision-2/resolve/VEL-OM-H1-A1-R2.otio]=],[ [=[visual_clips]=] ]=15,[ [=[audio_clips]=] ]=11}
local pm=r:GetProjectManager() local p=pm:GetCurrentProject() assert(p:GetName()=="VEL_Eleanor_OldMoney_RawPhone_R2_2026-09-11")
local pool=p:GetMediaPool() assert(p:GetTimelineCount()==0,"Inspect existing timeline before importing")
local t=pool:ImportTimelineFromFile(ad.otio,{timelineName=ad.name}) assert(t,"Import failed") p:SetCurrentTimeline(t)
local v=t:GetItemListInTrack("video",1) local report={}
for i,c in ipairs(v) do report[#report+1]={name=c:GetName(),start=c:GetStart(),finish=c:GetEnd(),duration=c:GetDuration(),source=c:GetMediaPoolItem():GetClipProperty("File Path")} end
assert(pm:SaveProject()) return {name=t:GetName(),start=t:GetStartFrame(),finish=t:GetEndFrame(),video_tracks=t:GetTrackCount("video"),audio_tracks=t:GetTrackCount("audio"),clips=report}