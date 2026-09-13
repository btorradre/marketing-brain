from pathlib import Path
import json,sys
P=Path(__file__).resolve().parent;R=P/'resolve';sys.path.insert(0,str(R));from run_lua import run
src='local root=[=['+str(P)+']=]\n'+r'''
local pm=r:GetProjectManager() local p=pm:GetCurrentProject() assert(p:GetName()=="VEL_Weekender_Haaland_20260912") assert(not p:IsRenderingInProgress()) assert(pm:SaveProject())
local pool=p:GetMediaPool() local media=pool:ImportMedia({root.."/heygen/presenter-native.mp4"}) assert(#media==1)
local t=pool:CreateEmptyTimeline("Presenter-Key-Master") assert(t) assert(p:SetCurrentTimeline(t))
local clips=pool:AppendToTimeline({{mediaPoolItem=media[1],startFrame=0,endFrame=1031,mediaType=1,trackIndex=1,recordFrame=t:GetStartFrame()}}) assert(#clips==1)
local item=clips[1] local c=item:AddFusionComp() c:Lock() local mi=c:FindTool("MediaIn1") local mo=c:FindTool("MediaOut1") local key=c:AddTool("DeltaKeyer")
key:SetInput("BackgroundRed",0) key:SetInput("BackgroundGreen",1) key:SetInput("BackgroundBlue",0) key:SetInput("LowThreshold",0.12) key:SetInput("HighThreshold",0.95) key:SetInput("CleanBackground",0.1)
key:ConnectInput("Input",mi) mo:ConnectInput("Input",key) c:Unlock() local f=root.."/heygen/presenter-master-key.comp" assert(item:ExportFusionComp(f,1)) assert(item:ImportFusionComp(f))
assert(pm:SaveProject()) return {timeline=t:GetName(),frames=t:GetEndFrame()-t:GetStartFrame(),codecs=p:GetRenderCodecs("mov")}
'''
out=run(src);(R/'presenter-master-create.json').write_text(json.dumps(out,indent=2));print(out);assert out['ok']
