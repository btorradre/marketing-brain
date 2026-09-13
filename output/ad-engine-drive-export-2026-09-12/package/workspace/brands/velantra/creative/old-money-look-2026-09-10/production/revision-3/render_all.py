from pathlib import Path
import sys,json
R=Path(__file__).resolve().parent;P=R.parent;sys.path.insert(0,str(P/'resolve'))
from run_lua import run
from lua_data import lua
ads=json.loads((R/'resolve/manifest.json').read_text())
src='local names='+lua([a['name'] for a in ads])+'\nlocal output='+lua(str(R/'exports'))+'\n'+r'''
local pm=r:GetProjectManager() local p=pm:GetCurrentProject()
assert(p:GetName()=="VEL_Eleanor_OldMoney_ContinuousPresenter_R3_2026-09-11") assert(not p:IsRenderingInProgress())
assert(p:GetTimelineCount()==9,"Expected nine timelines")
local jobs={} local result={}
for _,name in ipairs(names) do
 local t=nil for i=1,p:GetTimelineCount() do local candidate=p:GetTimelineByIndex(i) if candidate:GetName()==name then t=candidate end end
 assert(t,"Missing "..name) p:SetCurrentTimeline(t)
 assert(t:GetTrackCount("video")==3)
 assert(p:SetCurrentRenderFormatAndCodec("mp4","H264")) assert(p:SetCurrentRenderMode(1))
 assert(p:SetRenderSettings({SelectAllFrames=true,TargetDir=output,CustomName=name,ExportVideo=true,ExportAudio=true,FormatWidth=1080,FormatHeight=1920,FrameRate=30,VideoQuality=12000,AudioCodec="aac",AudioSampleRate=48000,NetworkOptimization=true}))
 local id=p:AddRenderJob() assert(id) jobs[#jobs+1]=id result[#result+1]={name=name,job=id}
end
assert(pm:SaveProject())
assert(pm:ExportProject(p:GetName(),output.."/Eleanor-OldMoney-R3.drp"),"Project export failed")
return {jobs=result,started=p:StartRendering(jobs),project=p:GetName()}
'''
(R/'resolve/render-all.lua').write_text(src);out=run(src);(R/'resolve/render-jobs.json').write_text(json.dumps(out,indent=2));print(out)
