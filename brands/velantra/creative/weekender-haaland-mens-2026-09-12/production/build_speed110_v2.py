from pathlib import Path
import json,sys
P=Path(__file__).resolve().parent;R=P/'resolve-speed110';sys.path.insert(0,str(P/'resolve-gringo-aligned'));from run_lua import run
m=json.loads((R/'time-map-plan.json').read_text())
def lua(v):
 if isinstance(v,str):return '[=['+v+']=]'
 if isinstance(v,bool):return 'true' if v else 'false'
 if isinstance(v,(int,float)):return str(v)
 if isinstance(v,list):return '{'+','.join(lua(x) for x in v)+'}'
 if isinstance(v,dict):return '{'+','.join('[ '+lua(k)+' ]='+lua(x) for k,x in v.items())+'}'
s='local ranges='+lua(m['keep'])+'\nlocal output='+lua(str(R))+'\n'+r'''
local pm=r:GetProjectManager();local p=pm:GetCurrentProject();assert(p:GetName()=="VEL_Weekender_Haaland_20260912");assert(not p:IsRenderingInProgress());assert(pm:SaveProject())
local src;for i=1,p:GetTimelineCount() do local t=p:GetTimelineByIndex(i);assert(t:GetName()~="Weekender-Haaland-Gringo-PausesClosed-v2");assert(t:GetName()~="Weekender-Haaland-Gringo-Natural-AvatarV-110-v2");if t:GetName()=="Weekender-Haaland-Gringo-Natural-AvatarV-v2" then src=t end end;assert(src and src:GetEndFrame()==1431)
local pool=p:GetMediaPool();local t=pool:CreateEmptyTimeline("Weekender-Haaland-Gringo-PausesClosed-v2");assert(t);assert(p:SetCurrentTimeline(t));assert(t:SetStartTimecode("00:00:00:00"))
for i,k in ipairs(ranges) do
 local items=pool:AppendToTimeline({{mediaPoolItem=src:GetMediaPoolItem(),startFrame=k.source_start,endFrame=k.source_end,recordFrame=k.record_start}});assert(items)
end
local vs=t:GetItemListInTrack("video",1);local aa=t:GetItemListInTrack("audio",1);assert(#vs==#ranges and #aa==#ranges)
for i,k in ipairs(ranges) do
 for _,x in ipairs({vs[i],aa[i]}) do assert(x:GetStart()==k.record_start and x:GetEnd()==k.record_end,"Native range does not match plan: "..i) end
 assert(t:SetClipsLinked({vs[i],aa[i]},true));assert(t:AddMarker(k.record_start,"Cyan","Speech section "..i,"Synchronized picture, presenter, captions and voice from source frames "..k.source_start.."–"..k.source_end,1))
end
assert(t:GetEndFrame()==1139)
local final=pool:CreateEmptyTimeline("Weekender-Haaland-Gringo-Natural-AvatarV-110-v2");assert(final);assert(p:SetCurrentTimeline(final));assert(final:SetStartTimecode("00:00:00:00"));assert(pool:AppendToTimeline({{mediaPoolItem=t:GetMediaPoolItem(),startFrame=0,endFrame=1139,recordFrame=0}}))
local v=final:GetItemListInTrack("video",1)[1];local a=final:GetItemListInTrack("audio",1)[1];assert(v and a);assert(final:SetClipsLinked({v,a},true));assert(v:SetSpeed({Percentage=110,PitchCorrection=true,RippleTimeline=true}));assert(math.abs(v:GetSpeed().Percentage-110)<0.0001 and math.abs(a:GetSpeed().Percentage-110)<0.0001);assert(v:GetEnd()==a:GetEnd());assert(v:GetSpeed().PitchCorrection and a:GetSpeed().PitchCorrection)
assert(pm:SaveProject());assert(final:Export(output.."/Weekender-Haaland-Gringo-Natural-AvatarV-110-v2.drt",r.EXPORT_DRT));assert(t:Export(output.."/Weekender-Haaland-Gringo-PausesClosed-v2.drt",r.EXPORT_DRT));assert(pm:ExportProject(p:GetName(),output.."/VEL-Weekender-Haaland-Gringo-Speed110-v2.drp",true));r:OpenPage("edit")
return {project=p:GetName(),source=src:GetName(),source_frames=src:GetEndFrame(),trimmed=t:GetName(),kept_frames=t:GetEndFrame(),sections=#vs,timeline=final:GetName(),frames=final:GetEndFrame(),video={start=v:GetStart(),finish=v:GetEnd(),speed=v:GetSpeed()},audio={start=a:GetStart(),finish=a:GetEnd(),speed=a:GetSpeed()},saved=true}
'''
(R/'build.lua').write_text(s)
o=run(s,30);(R/'build-v2-receipt.json').write_text(json.dumps(o,indent=2));print(o);assert o['ok'],o
