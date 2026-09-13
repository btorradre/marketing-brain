from pathlib import Path
import sys,json
R=Path(__file__).resolve().parent;P=R.parent;sys.path.insert(0,str(P/'resolve'));from run_lua import run
from lua_data import lua
ads=json.loads((R/'resolve/probe-manifest.json').read_text());start=int(sys.argv[1]) if len(sys.argv)>1 else 0;end=int(sys.argv[2]) if len(sys.argv)>2 else len(ads)
src='local names='+lua([a['name'] for a in ads[start:end]])+'\nlocal output='+lua(str(R/'qa'))+'\n'+'''
local pm=r:GetProjectManager() local p=pm:GetCurrentProject() assert(not p:IsRenderingInProgress()) assert(pm:SaveProject())
p=pm:LoadProject("VEL_Eleanor_OldMoney_R5_OutlineCaptions_2026-09-11") assert(p)
local jobs={} local result={}
for _,name in ipairs(names) do
 local t=nil for i=1,p:GetTimelineCount() do local candidate=p:GetTimelineByIndex(i) if candidate:GetName()==name then t=candidate end end
 assert(t,"Missing "..name) p:SetCurrentTimeline(t)
 assert(p:SetCurrentRenderFormatAndCodec("mp4","H264")) assert(p:SetCurrentRenderMode(1))
 assert(p:SetRenderSettings({SelectAllFrames=false,MarkIn=t:GetStartFrame(),MarkOut=t:GetStartFrame()+29,TargetDir=output,CustomName=name,ExportVideo=true,ExportAudio=true,FormatWidth=1080,FormatHeight=1920,FrameRate=30,VideoQuality=12000,AudioCodec="aac",AudioSampleRate=48000,NetworkOptimization=true}))
 local id=p:AddRenderJob() assert(id) jobs[#jobs+1]=id result[#result+1]={name=name,job=id}
end
assert(pm:SaveProject()) assert(pm:ExportProject(p:GetName(),output.."/Eleanor-OldMoney-R5.drp"))
return {jobs=result,started=p:StartRendering(jobs),project=p:GetName()}
'''
out=run(src);(R/'resolve'/f'render-jobs-{start}-{end}.json').write_text(json.dumps(out,indent=2));print(out)
