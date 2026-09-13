local p=r:GetProjectManager():GetCurrentProject() local t=p:GetCurrentTimeline()
local item=t:GetItemListInTrack("video",2)[1] local comps={}
for i=1,item:GetFusionCompCount() do local c=item:GetFusionCompByIndex(i) local nodes={} for _,v in pairs(c:GetToolList(false)) do nodes[v:GetAttrs().TOOLS_Name]=v:GetAttrs().TOOLS_RegID end comps[tostring(i)]={nodes=nodes,name=c:GetAttrs().COMPS_Name} end
local list=t:GetItemListInTrack("video",1) local last=list[#list]
return {comp_names=item:GetFusionCompNameList(),comps=comps,last={name=last:GetName(),start=last:GetStart(),duration=last:GetDuration(),file=last:GetMediaPoolItem():GetClipProperty("File Path"),frames=last:GetMediaPoolItem():GetClipProperty("Frames"),type=last:GetMediaPoolItem():GetClipProperty("Type")}}
