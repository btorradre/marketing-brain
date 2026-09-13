from pathlib import Path
import sys,json
R=Path(__file__).resolve().parent;P=R.parent;sys.path.insert(0,str(P/'resolve'));from run_lua import run
from lua_data import lua
ads=json.loads((R/'resolve/manifest.json').read_text())
source='local ads='+lua([{'name':a['name'],'duration':a['duration_frames'],'captions':len(a['captions'])} for a in ads])+'\nlocal output='+lua(str(R/'exports/Eleanor-OldMoney-R4.drp'))+'\n'+'''
local pm=r:GetProjectManager() local p=pm:GetCurrentProject() assert(not p:IsRenderingInProgress()) assert(pm:SaveProject())
local previous=p:GetName() p=pm:LoadProject("VEL_Eleanor_OldMoney_R4_110pct_2026-09-11") assert(p)
local probes={} for i=1,p:GetTimelineCount() do local t=p:GetTimelineByIndex(i) if t:GetName()=="R4-110pct-native-probe" then probes[#probes+1]=t end end
if #probes>0 then assert(p:GetMediaPool():DeleteTimelines(probes)) end
assert(p:GetTimelineCount()==9)
local result={}
for _,ad in ipairs(ads) do
 local t=nil for i=1,p:GetTimelineCount() do local x=p:GetTimelineByIndex(i) if x:GetName()==ad.name then t=x end end assert(t)
 assert(t:GetEndFrame()-t:GetStartFrame()==ad.duration) assert(t:GetTrackCount("video")==3) assert(t:GetTrackCount("audio")==1)
 assert(#t:GetItemListInTrack("video",3)==ad.captions)
 local errors={} local cursor=t:GetStartFrame()
 for i,item in ipairs(t:GetItemListInTrack("audio",1)) do
  assert(item:GetStart()==cursor,"Audio gap") cursor=item:GetEnd()
  local duration=item:GetDuration() local span=item:GetSourceEndFrame()-item:GetSourceStartFrame()
  local ratio=span/duration if math.abs(span-duration*1.1)>1.1 then errors[#errors+1]={index=i,ratio=ratio} end
 end
 assert(cursor==t:GetEndFrame()) assert(#errors==0,"Audio retime mismatch")
 result[#result+1]={name=ad.name,frames=ad.duration,captions=ad.captions,native_audio_110=true,audio_gaps=0}
end
assert(pm:SaveProject()) assert(pm:ExportProject(p:GetName(),output))
if previous~=p:GetName() then assert(pm:LoadProject(previous)) end
return {verified=result,project="VEL_Eleanor_OldMoney_R4_110pct_2026-09-11",timelines=9,exported=true}
'''
out=run(source);(R/'qa/resolve-final-verification.json').write_text(json.dumps(out,indent=2));print(out);assert out['ok']
