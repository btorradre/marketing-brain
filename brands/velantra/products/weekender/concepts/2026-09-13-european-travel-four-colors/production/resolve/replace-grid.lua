local pm=r:GetProjectManager();local p=pm:GetCurrentProject()
assert(p:GetName()=="VEL_Weekender_EuropeanTravel_FourColors_20260913")
local t=p:GetCurrentTimeline();assert(t:GetName()=="Eleanor-EuropeanTravel-FourColors")
local function snap(skipHook)
 local out={}
 for _,kind in ipairs({"video","audio"}) do
  for tr=1,t:GetTrackCount(kind) do
   local its={}
   for i,it in ipairs(t:GetItemListInTrack(kind,tr)) do
    if not(skipHook and kind=="video" and tr==1 and i==1) then
     its[i]={name=it:GetName(),start=it:GetStart(),finish=it:GetEnd(),duration=it:GetDuration(),left=it:GetLeftOffset(),right=it:GetRightOffset(),props=it:GetProperty(),fusion=it:GetFusionCompCount(),path=it:GetMediaPoolItem():GetClipProperty("File Path")}
    end
   end
   out[kind..tr]=its
  end
 end
 return encode(out)
end
local before=snap(true)
local first=t:GetItemListInTrack("video",1)[1]
assert(first:GetStart()==0 and first:GetEnd()==285 and first:GetName()=="hook-still.png","Unexpected hook")
local originalPath=first:GetMediaPoolItem():GetClipProperty("File Path")
local props=encode(first:GetProperty())
assert(first:GetMediaPoolItem():ReplaceClip([=[/Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/weekender/concepts/2026-09-13-european-travel-four-colors/storyboard/assets/fourcolorgridselected.png]=]),"Hook replacement failed")
assert(first:GetStart()==0 and first:GetEnd()==285,"Hook timing changed")
assert(props==encode(first:GetProperty()),"Hook transform changed")
assert(before==snap(true),"An unrelated clip changed")
assert(t:GetEndFrame()==2120)
assert(pm:SaveProject())
local tracks={}
for _,kind in ipairs({"video","audio"}) do for tr=1,t:GetTrackCount(kind) do tracks[kind..tr]=#t:GetItemListInTrack(kind,tr) end end
return {project=p:GetName(),timeline=t:GetName(),old_hook=originalPath,new_hook=first:GetMediaPoolItem():GetClipProperty("File Path"),hook_start=first:GetStart(),hook_end=first:GetEnd(),unrelated_items_identical=true,hook_properties_identical=true,tracks=tracks,duration=t:GetEndFrame()}
