from pathlib import Path
import json,sys
P=Path(__file__).resolve().parent;R=P/'resolve-gringo';sys.path.insert(0,str(R));from run_lua import run
def lua(x):
 if isinstance(x,str):return '[=['+x+']=]'
 if isinstance(x,bool):return str(x).lower()
 if isinstance(x,(int,float)):return str(x)
 if isinstance(x,list):return '{'+','.join(lua(v) for v in x)+'}'
 if isinstance(x,dict):return '{'+','.join('[ '+lua(k)+' ]='+lua(v) for k,v in x.items())+'}'
 raise TypeError(type(x))
ad=json.loads((R/'manifest.json').read_text())
src='local ad='+lua(ad)+'\nlocal root='+lua(str(R))+'\n'+r"""
local pm=r:GetProjectManager() local p=pm:GetCurrentProject() assert(p:GetName()=="VEL_Weekender_Haaland_20260912") assert(not p:IsRenderingInProgress()) assert(pm:SaveProject())
local donor=nil for i=1,p:GetTimelineCount() do local t=p:GetTimelineByIndex(i) if t:GetName()=="Weekender-Haaland-Natural-AvatarV-v3-EndSync" then donor=t end assert(t:GetName()~=ad.name,"New timeline already exists") end assert(donor)
local nt=p:GetMediaPool():ImportTimelineFromFile(root.."/assembly.otio",{timelineName=ad.name}) assert(nt) assert(p:SetCurrentTimeline(nt))
assert(nt:GetEndFrame()==ad.frames,"Picture endpoint mismatch")
for tr=1,4 do
 local from=donor:GetItemListInTrack("video",tr) local items=nt:GetItemListInTrack("video",tr) assert(#items==#from,"Layer count mismatch")
 for i,item in ipairs(items) do
  assert(item:SetProperties(from[i]:GetProperty()),"Copy props failed")
  if tr==1 then local s=ad.scenes[i] assert(item:GetStart()==s.start and item:GetEnd()==s["end"],"Picture placement") assert(nt:AddMarker(s.start,"Blue",s.id,s.script.."\n"..s.visual.."\nCurrent gringo-tiktok-male Natural alignment; no extra end hold.",s["end"]-s.start)) end
  if tr>=3 then assert(item:ImportFusionComp(root.."/comps/current-"..tr.."-"..i..".comp"),"Caption comp failed") end
 end
end
local a=nt:GetItemListInTrack("audio",1) assert(#a==1 and a[1]:GetEnd()==ad.frames,"Audio endpoint mismatch")
assert(pm:SaveProject()) r:OpenPage("edit") return {project=p:GetName(),timeline=nt:GetName(),preserved=donor:GetName(),frames=nt:GetEndFrame(),audio_end=a[1]:GetEnd(),background=#nt:GetItemListInTrack("video",1),presenter=#nt:GetItemListInTrack("video",2),captions=#nt:GetItemListInTrack("video",3)}
"""
(R/'build.lua').write_text(src);out=run(src,timeout=45);(R/'build-result.json').write_text(json.dumps(out,indent=2));print(out);assert out['ok']
