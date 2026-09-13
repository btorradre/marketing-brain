from pathlib import Path
import sys,json
P=Path(__file__).resolve().parent;R=P/'resolve';sys.path.insert(0,str(R));from run_lua import run
sys.path.insert(0,str(P.parents[1]/'eleanor-european-travel-2026-09-11/production/resolve'))
def lua(x):
 if isinstance(x,str):return '[=['+x+']=]'
 if isinstance(x,bool):return str(x).lower()
 if isinstance(x,(int,float)):return str(x)
 if isinstance(x,list):return '{'+','.join(lua(v) for v in x)+'}'
 if isinstance(x,dict):return '{'+','.join('[ '+lua(k)+' ]='+lua(v) for k,v in x.items())+'}'
 raise TypeError(type(x))
ad=json.loads((R/'manifest.json').read_text());name='VEL_Weekender_Haaland_20260912'
src='local ad='+lua(ad)+'\nlocal root='+lua(str(R))+'\nlocal name='+lua(name)+'\n'+r'''
local pm=r:GetProjectManager() local old=pm:GetCurrentProject()
if old then assert(not old:IsRenderingInProgress(),"Current project rendering") assert(pm:SaveProject()) end
local p=nil for _,n in pairs(pm:GetProjectListInCurrentFolder()) do if n==name then p=pm:LoadProject(name) end end
if not p then p=pm:CreateProject(name) end assert(p)
for i=1,p:GetTimelineCount() do assert(p:GetTimelineByIndex(i):GetName()~=ad.name,"Timeline exists; inspect before mutation") end
assert(p:SetSetting("timelineFrameRate","30")) assert(p:SetSetting("timelineResolutionWidth","1080")) assert(p:SetSetting("timelineResolutionHeight","1920"))
local t=p:GetMediaPool():ImportTimelineFromFile(root.."/assembly.otio",{timelineName=ad.name}) assert(t) assert(p:SetCurrentTimeline(t))
assert(t:GetEndFrame()-t:GetStartFrame()==ad.frames,"Duration mismatch")
local bg=t:GetItemListInTrack("video",1) assert(#bg==13)
for i,it in ipairs(bg) do
 it:SetProperty("RetimeProcess",0)
 local s=ad.scenes[i] assert(t:AddMarker(s.start,"Blue",s.id,s.script.."\n"..s.visual.."\n"..s.note,s["end"]-s.start))
 if i==1 then assert(it:SetProperties({ZoomX=1.3,ZoomY=1.3,Tilt=280})) end
end
local function persist(item,c,label)
 c:Unlock() local f=root.."/comps/"..label..".comp" assert(item:ExportFusionComp(f,1)) assert(item:ImportFusionComp(f))
end
local prs=t:GetItemListInTrack("video",2) assert(#prs==12)
for i,item in ipairs(prs) do
 local props={ZoomX=0.42,ZoomY=0.42,Pan=-290,Tilt=-300,CropBottom=670,RetimeProcess=0}
 if i==1 then props={ZoomX=0.60,ZoomY=0.60,Pan=-270,Tilt=-590,RetimeProcess=0} end
 if i==2 then props={ZoomX=0.53,ZoomY=0.53,Pan=285,Tilt=-595,RetimeProcess=0} end
 if i==5 then props.Tilt=130 props.ZoomX=0.34 props.ZoomY=0.34 end
 if i==11 then props.Pan=290 props.Tilt=-360 end
 assert(item:SetProperties(props))
end
local function textbar(c,copy,size,x,y,r,g,b,tr,tg,tb,width,height)
 local text=c:AddTool("TextPlus") local back=c:AddTool("Background") local rect=c:AddTool("RectangleMask") local merge=c:AddTool("Merge")
 back:SetInput("UseFrameFormatSettings",0) back:SetInput("Width",1080) back:SetInput("Height",1920)
 back:SetInput("TopLeftRed",r) back:SetInput("TopLeftGreen",g) back:SetInput("TopLeftBlue",b) back:SetInput("TopLeftAlpha",1)
 rect:SetInput("Center",{x,y}) rect:SetInput("Width",width) rect:SetInput("Height",height) rect:SetInput("CornerRadius",0.04)
 back:ConnectInput("EffectMask",rect)
 text:SetInput("UseFrameFormatSettings",0) text:SetInput("Width",1080) text:SetInput("Height",1920)
 text:SetInput("StyledText",copy) text:SetInput("Font","Impact") text:SetInput("Style","Regular") text:SetInput("Size",size)
 text:SetInput("Center",{x,y}) text:SetInput("VerticalJustification",1) text:SetInput("HorizontalJustification",1)
 text:SetInput("Red1",tr) text:SetInput("Green1",tg) text:SetInput("Blue1",tb)
 merge:ConnectInput("Background",back) merge:ConnectInput("Foreground",text) return merge
end
local caps=t:GetItemListInTrack("video",3) assert(#caps==#ad.captions)
for i,item in ipairs(caps) do
 local a=ad.captions[i] local c=item:AddFusionComp() assert(c) c:Lock()
 local m=textbar(c,a.text,a.size,a.x,a.y,0,0,0,1,1,1,math.min(0.94,0.08+#a.text*a.size*0.33),0.032)
 c:FindTool("MediaOut1"):ConnectInput("Input",m) persist(item,c,"caption-"..i)
end
local hooks=t:GetItemListInTrack("video",4) assert(#hooks==2)
for i,item in ipairs(hooks) do
 local c=item:AddFusionComp() assert(c) c:Lock()
 local y=i==1 and 0.55 or 0.64
 local a=textbar(c,"ATHLETE",0.11,0.5,y,0.78,0.01,0.03,1,1,1,0.36,0.055)
 local b=textbar(c,"WEEKENDER BAG",0.14,0.5,y-0.075,1,1,1,0,0,0,0.69,0.075)
 local m=c:AddTool("Merge") m:ConnectInput("Background",a) m:ConnectInput("Foreground",b)
 c:FindTool("MediaOut1"):ConnectInput("Input",m) persist(item,c,"hook-"..i)
end
assert(#t:GetItemListInTrack("audio",1)==1) assert(pm:SaveProject()) r:OpenPage("edit")
return {project=p:GetName(),timeline=t:GetName(),frames=ad.frames,seconds=ad.frames/30,picture_clips=#bg,presenter_clips=#prs,captions=#caps,prior_project=old and old:GetName(),heygen=ad.presenter_ready}
'''
(R/'build.lua').write_text(src);out=run(src,timeout=90);(R/'build-result.json').write_text(json.dumps(out,indent=2)+'\n');print(out);assert out['ok']
