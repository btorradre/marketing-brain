from pathlib import Path
import sys,json
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P/'resolve'));from run_lua import run;from lua_data import lua
src='local output='+lua(str(P/'exports'))+'\n'+r'''
local pm=r:GetProjectManager() local p=pm:GetCurrentProject() assert(p:GetName()=="VEL_Eleanor_EuropeanTravel_Natural110_20260912") assert(not p:IsRenderingInProgress())
local t=p:GetCurrentTimeline() assert(t:GetName()=="Eleanor-EuropeanTravel-WIP")
assert(p:SetCurrentRenderFormatAndCodec("mp4","H264")) assert(p:SetCurrentRenderMode(1))
assert(p:SetRenderSettings({SelectAllFrames=true,TargetDir=output,CustomName="Eleanor-EuropeanTravel-WIP",ExportVideo=true,ExportAudio=true,FormatWidth=1080,FormatHeight=1920,FrameRate=30,VideoQuality=16000,AudioCodec="aac",AudioSampleRate=48000,NetworkOptimization=true}))
assert(pm:SaveProject()) assert(pm:ExportProject(p:GetName(),output.."/Eleanor-EuropeanTravel-WIP.drp"))
local id=p:AddRenderJob() assert(id) assert(p:StartRendering({id})) return {project=p:GetName(),timeline=t:GetName(),job=id,started=true}
'''
out=run(src);(P/'resolve/render-wip.json').write_text(json.dumps(out,indent=2));print(out,flush=True);assert out['ok']
