from pathlib import Path
import sys,json,subprocess
P=Path(__file__).resolve().parent;H=P/'heygen';sys.path.insert(0,str(P/'resolve'));from run_lua import run;from lua_data import lua
probe=json.loads((H/'probe.json').read_text());v=next(s for s in probe['streams'] if s['codec_type']=='video')
native=H/'presenter-native.mp4';last=H/'presenter-final-frame.png'
subprocess.run(['ffmpeg','-y','-v','error','-i',str(native),'-vf',f"select=eq(n\\,{int(v['nb_frames'])-1})",'-frames:v','1',str(last)],check=True)
data={'video':str(native),'last':str(last),'source_frames':int(v['nb_frames']),'compdir':str(H),'frames':2439}
src='local ad='+lua(data)+'\n'+r'''
local pm=r:GetProjectManager() local p=pm:GetCurrentProject()
assert(p:GetName()=="VEL_Eleanor_EuropeanTravel_Natural110_20260912","Wrong current project")
assert(not p:IsRenderingInProgress()) assert(pm:SaveProject())
local old=nil local existing=nil local newName="Eleanor-EuropeanTravel-HeyGen"
for i=1,p:GetTimelineCount() do local x=p:GetTimelineByIndex(i) if x:GetName()==newName then existing=x end if x:GetName()=="Eleanor-EuropeanTravel-WIP" then old=x end end
assert(old) local t=existing or old:DuplicateTimeline(newName) assert(t) assert(p:SetCurrentTimeline(t))
local pool=p:GetMediaPool() local before=t:GetItemListInTrack("video",2)
if existing then assert(#before==0,"Existing presenter items need inspection") else assert(#before==1) assert(t:DeleteClips(before,false)) end
local media=pool:ImportMedia({ad.video,ad.last}) assert(media and #media==2,"Media import failed")
local base=t:GetStartFrame()
local clips=pool:AppendToTimeline({{mediaPoolItem=media[1],startFrame=0,endFrame=ad.source_frames-1,mediaType=1,trackIndex=2,recordFrame=base}}) assert(#clips==1)
local nativeEnd=clips[1]:GetEnd()-base local tail=ad.frames-nativeEnd
assert(tail>=0 and tail<=90,"Unexpected presenter duration; inspect audio alignment")
if tail>0 then
 local hold=pool:AppendToTimeline({{mediaPoolItem=media[2],startFrame=0,endFrame=tail-1,mediaType=1,trackIndex=2,recordFrame=base+nativeEnd}}) assert(#hold==1)
end
local keyResults={}
for i,item in ipairs(t:GetItemListInTrack("video",2)) do
 local c=item:AddFusionComp() assert(c) c:Lock()
 local mi=c:FindTool("MediaIn1") local mo=c:FindTool("MediaOut1") local k=c:AddTool("DeltaKeyer") assert(mi and mo and k)
 k:SetInput("BackgroundRed",0) k:SetInput("BackgroundGreen",1) k:SetInput("BackgroundBlue",0)
 k:SetInput("LowThreshold",0.18) k:SetInput("HighThreshold",0.96) k:SetInput("CleanBackground",0.1)
 k:ConnectInput("Input",mi) mo:ConnectInput("Input",k) c:Unlock()
 local f=ad.compdir.."/presenter-key-"..i..".comp" assert(item:ExportFusionComp(f,1)) assert(item:ImportFusionComp(f))
 assert(item:SetProperties({ZoomX=0.28,ZoomY=0.28,Pan=-375,Tilt=-820,RetimeProcess=0}))
 keyResults[#keyResults+1]={start=item:GetStart()-base,duration=item:GetDuration(),source=item:GetName()}
end
assert(#t:GetItemListInTrack("video",3)==76) assert(#t:GetItemListInTrack("audio",1)==1)
assert(t:GetEndFrame()-base==ad.frames) assert(pm:SaveProject())
return {project=p:GetName(),timeline=t:GetName(),frames=ad.frames,presenter=keyResults,native_end_frame=nativeEnd,hold_frames=tail,captions=76}
'''
(H/'build.lua').write_text(src);out=run(src,timeout=90);(H/'build-result.json').write_text(json.dumps(out,indent=2));print(out,flush=True);assert out['ok']
