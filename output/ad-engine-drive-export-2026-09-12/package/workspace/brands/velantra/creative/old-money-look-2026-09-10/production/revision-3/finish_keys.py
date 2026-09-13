from pathlib import Path
import sys,json
R=Path(__file__).resolve().parent;P=R.parent;sys.path.insert(0,str(P/'resolve'))
from run_lua import run
from lua_data import lua
out=R/'exports';archive=R/'qa/before-key-cleanup';archive.mkdir(exist_ok=True)
for f in out.glob('*.mp4'):
 if '-A1-' not in f.name:f.rename(archive/f.name)
if (out/'Eleanor-OldMoney-R3.drp').exists():(out/'Eleanor-OldMoney-R3.drp').rename(archive/'Eleanor-OldMoney-R3.drp')
src='local output='+lua(str(out))+'\nlocal compdir='+lua(str(R/'resolve/comps')+'/')+'\n'+r'''
local pm=r:GetProjectManager() local current=pm:GetCurrentProject()
assert(not current:IsRenderingInProgress(),"Another render active") assert(pm:SaveProject())
local p=pm:LoadProject("VEL_Eleanor_OldMoney_ContinuousPresenter_R3_2026-09-11") assert(p)
local jobs={} local result={} local count=0
for n=1,p:GetTimelineCount() do
 local t=p:GetTimelineByIndex(n) local name=t:GetName()
 if name:match("%-A[23]%-R3$") then
  p:SetCurrentTimeline(t)
  for i,item in ipairs(t:GetItemListInTrack("video",2)) do
   local idx=item:GetFusionCompCount() local c=item:GetFusionCompByIndex(idx) assert(c)
   local k=c:FindTool("DeltaKeyer1") assert(k)
   k:SetInput("LowThreshold",0.18) k:SetInput("HighThreshold",0.96) k:SetInput("CleanBackground",0.1)
   local path=compdir..name.."-clean-"..i..".comp"
   assert(item:ExportFusionComp(path,idx)) assert(item:ImportFusionComp(path)) count=count+1
  end
  assert(p:SetCurrentRenderFormatAndCodec("mp4","H264")) assert(p:SetCurrentRenderMode(1))
  assert(p:SetRenderSettings({SelectAllFrames=true,TargetDir=output,CustomName=name,ExportVideo=true,ExportAudio=true,FormatWidth=1080,FormatHeight=1920,FrameRate=30,VideoQuality=12000,AudioCodec="aac",AudioSampleRate=48000,NetworkOptimization=true}))
  local id=p:AddRenderJob() assert(id) jobs[#jobs+1]=id result[#result+1]={name=name,job=id}
 end
end
assert(#jobs==6) assert(pm:SaveProject()) assert(pm:ExportProject(p:GetName(),output.."/Eleanor-OldMoney-R3.drp"))
return {jobs=result,keyed_clips=count,started=p:StartRendering(jobs)}
'''
(R/'resolve/finish-keys.lua').write_text(src);res=run(src,timeout=90);print(res);(R/'resolve/key-cleanup-jobs.json').write_text(json.dumps(res,indent=2));assert res['ok']
f=R/'resolve/render-jobs.json';d=json.loads(f.read_text());jobs=d['result']['jobs']
for new in res['result']['jobs'].values():
 for key,old in jobs.items():
  if old['name']==new['name']:jobs[key]=new;break
f.write_text(json.dumps(d,indent=2))
