from pathlib import Path
import sys,json
P=Path(__file__).resolve().parent;R=P/'resolve';sys.path.insert(0,str(R));from run_lua import run;from lua_data import lua
if '--heygen' in sys.argv:R=P/'heygen'
if '--tight' in sys.argv:R=P/'tight'
ad=json.loads((R/'manifest.json').read_text());name='VEL_Eleanor_EuropeanTravel_Natural110_20260912'
src='local ad='+lua(ad)+'\nlocal root='+lua(str(R))+'\nlocal name='+lua(name)+'\n'+r'''
local pm=r:GetProjectManager() local old=pm:GetCurrentProject()
assert(old and not old:IsRenderingInProgress(),"Current project rendering") assert(pm:SaveProject())
local p=nil for _,n in pairs(pm:GetProjectListInCurrentFolder()) do if n==name then p=pm:LoadProject(name) end end
if not p then p=pm:CreateProject(name) end assert(p)
local obsolete={} for i=1,p:GetTimelineCount() do local x=p:GetTimelineByIndex(i) if x:GetName()==ad.name then obsolete[#obsolete+1]=x end end if #obsolete>0 then assert(p:GetMediaPool():DeleteTimelines(obsolete)) end
p:SetSetting("timelineFrameRate","30") p:SetSetting("timelineResolutionWidth","1080") p:SetSetting("timelineResolutionHeight","1920")
local t=p:GetMediaPool():ImportTimelineFromFile(root.."/assembly.otio",{timelineName=ad.name}) assert(t) p:SetCurrentTimeline(t)
assert(t:GetEndFrame()-t:GetStartFrame()==ad.frames,"Timeline length mismatch")
local bg=t:GetItemListInTrack("video",1) assert(#bg==#ad.background)
for i,item in ipairs(bg) do item:SetProperty("RetimeProcess",0) if ad.background[i].zoom~=1 then assert(item:SetProperties({ZoomX=ad.background[i].zoom,ZoomY=ad.background[i].zoom})) end end
local presenters=t:GetItemListInTrack("video",2)
if ad.heygen then
 assert(#presenters==(ad.presenter_items or 2))
 for i,item in ipairs(presenters) do
  local c=item:AddFusionComp() assert(c) c:Lock()
  local mi=c:FindTool("MediaIn1") local mo=c:FindTool("MediaOut1") local k=c:AddTool("DeltaKeyer")
  k:SetInput("BackgroundRed",0) k:SetInput("BackgroundGreen",1) k:SetInput("BackgroundBlue",0)
  k:SetInput("LowThreshold",0.18) k:SetInput("HighThreshold",0.96) k:SetInput("CleanBackground",0.1)
  k:ConnectInput("Input",mi) mo:ConnectInput("Input",k) c:Unlock()
  local f=root.."/comps/presenter-key-"..i..".comp" assert(item:ExportFusionComp(f,1)) assert(item:ImportFusionComp(f))
  local layout=ad.presenter_layout or {zoom=0.28,pan=-375,tilt=-820}
  assert(item:SetProperties({ZoomX=layout.zoom,ZoomY=layout.zoom,Pan=layout.pan,Tilt=layout.tilt,RetimeProcess=0}))
 end
else
 assert(#presenters==1) assert(presenters[1]:SetProperties({ZoomX=0.28,ZoomY=0.28,Pan=-375,Tilt=-820}))
end
local caps=t:GetItemListInTrack("video",3) assert(#caps==#ad.captions)
for i,item in ipairs(caps) do
 local c=item:AddFusionComp() assert(c) c:Lock()
 local text=c:AddTool("TextPlus") local mo=c:FindTool("MediaOut1")
 text:SetInput("StyledText",ad.captions[i].text) text:SetInput("Font","Arial") text:SetInput("Style","Bold") text:SetInput("Size",0.058)
 text:SetInput("Center",{ad.captions[i].x,ad.captions[i].y}) text:SetInput("VerticalJustification",1) text:SetInput("HorizontalJustification",1)
 text:SetInput("Red1",1) text:SetInput("Green1",1) text:SetInput("Blue1",1)
 text:SetInput("Enabled2",1) text:SetInput("ElementShape2",1) text:SetInput("Red2",0) text:SetInput("Green2",0) text:SetInput("Blue2",0) text:SetInput("Alpha2",1) text:SetInput("Thickness2",0.045)
 mo:ConnectInput("Input",text) c:Unlock()
 local path=root.."/comps/caption-"..i..".comp" assert(item:ExportFusionComp(path,1)) assert(item:ImportFusionComp(path))
end
assert(pm:SaveProject())
return {project=p:GetName(),timeline=t:GetName(),duration=t:GetEndFrame()-t:GetStartFrame(),backgrounds=#bg,captions=#caps,presenter=ad.heygen and "HeyGen Avatar V, exact ElevenLabs audio" or "static WIP",presenter_items=#presenters,prior_project=old:GetName()}
'''
(R/'build.lua').write_text(src);out=run(src,timeout=240);(R/'build-result.json').write_text(json.dumps(out,indent=2));print(out,flush=True);assert out['ok']
