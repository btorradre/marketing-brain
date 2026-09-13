from pathlib import Path
import sys,json
R=Path(__file__).resolve().parent;P=R.parent
sys.path.insert(0,str(P/'resolve'))
from run_lua import run
from lua_data import lua
ad=json.loads((R/'resolve/manifest.json').read_text())[int(sys.argv[1]) if len(sys.argv)>1 else 0]
source='local ad='+lua(ad)+'\nlocal compdir='+lua(str(R/'resolve/comps')+'/')+'\n'+r'''
local pm=r:GetProjectManager() local p=pm:GetCurrentProject()
assert(not p:IsRenderingInProgress(),"Another project rendering") assert(pm:SaveProject())
p=pm:LoadProject("VEL_Eleanor_OldMoney_R5_OutlineCaptions_2026-09-11") assert(p)
assert(not p:IsRenderingInProgress())
for n=1,p:GetTimelineCount() do assert(p:GetTimelineByIndex(n):GetName()~=ad.name,"Timeline already exists; inspect") end
local t=p:GetMediaPool():ImportTimelineFromFile(ad.otio,{timelineName=ad.name}) assert(t)
p:SetCurrentTimeline(t)
assert(t:GetEndFrame()-t:GetStartFrame()==ad.duration_frames)
local presenters=t:GetItemListInTrack("video",2) assert(#presenters==ad.overlay_clips)
local function commit(item,c,path)
 c:Unlock() assert(item:ExportFusionComp(path,1)) assert(item:ImportFusionComp(path))
end
for i,item in ipairs(presenters) do
 if ad.avatar~="A1" then
  local c=item:AddFusionComp() assert(c) c:Lock()
  local mi=c:FindTool("MediaIn1") local mo=c:FindTool("MediaOut1") local k=c:AddTool("DeltaKeyer")
  k:SetInput("BackgroundRed",ad.green[1]) k:SetInput("BackgroundGreen",ad.green[2]) k:SetInput("BackgroundBlue",ad.green[3])
  k:SetInput("LowThreshold",0.18) k:SetInput("HighThreshold",0.96) k:SetInput("CleanBackground",0.1)
  k:ConnectInput("Input",mi) mo:ConnectInput("Input",k)
  commit(item,c,compdir..ad.name.."-presenter-"..i..".comp")
 end
 local zoom=0.46 local tilt=-550 local pan=-291.6
 if ad.avatar=="A3" then zoom=0.54 tilt=-485 pan=-248.4 end
 if ad.presenter_hook_layout[i] then zoom=0.28 pan=-388.8 tilt=-691.2 if ad.avatar=="A3" then zoom=0.30 pan=-378 tilt=-710 end end
 assert(item:SetProperties({ZoomX=zoom,ZoomY=zoom,Pan=pan,Tilt=tilt,RetimeProcess=0}))
end
local caps=t:GetItemListInTrack("video",3) assert(#caps==#ad.captions)
for i,item in ipairs(caps) do
 local c=item:AddFusionComp() assert(c) c:Lock()
 local text=c:AddTool("TextPlus") local mo=c:FindTool("MediaOut1")
 text:SetInput("StyledText",ad.captions[i].text)
 text:SetInput("Font","Arial") text:SetInput("Style","Regular") text:SetInput("Size",0.090)
 local captionY=0.1125
 text:SetInput("Center",{0.5,captionY}) text:SetInput("VerticalJustification",1) text:SetInput("HorizontalJustification",1)
 text:SetInput("Red1",1) text:SetInput("Green1",1) text:SetInput("Blue1",1)
 text:SetInput("Enabled2",1) text:SetInput("ElementShape2",1)
 text:SetInput("Red2",0) text:SetInput("Green2",0) text:SetInput("Blue2",0) text:SetInput("Alpha2",1)
 text:SetInput("Thickness2",0.055)
 mo:ConnectInput("Input",text)
 commit(item,c,compdir..ad.name.."-caption-"..i..".comp")
end
for _,c in ipairs(t:GetItemListInTrack("video",1)) do assert(c:SetProperty("RetimeProcess",0)) end
assert(pm:SaveProject())
return {project=p:GetName(),timeline=t:GetName(),frames=t:GetEndFrame()-t:GetStartFrame(),presenters=#presenters,captions=#caps}
'''
(R/'resolve'/(ad['name']+'-build.lua')).write_text(source)
out=run(source,timeout=180);(R/'resolve'/(ad['name']+'-build-result.json')).write_text(json.dumps(out,indent=2));print(out,flush=True)
assert out['ok']
