from pathlib import Path
import sys,json,copy
R=Path(__file__).resolve().parent;P=R.parent
sys.path.insert(0,str(P/'resolve'));from run_lua import run
from lua_data import lua
src=json.loads((P/'revision-3/resolve/VEL-OM-H1-A2-R3.otio').read_text())
# A short native voice/video probe, no image compositing: verify real speed and pitch.
src['name']='R4-110pct-native-probe'; src['tracks']['source_range']=None
v=copy.deepcopy(src['tracks']['children'][1]);a=copy.deepcopy(src['tracks']['children'][3]);
for track in [v,a]:
 item=track['children'][0]; item['source_range']['start_time']['value']=0;item['source_range']['duration']['value']=150
 item['effects']=[{'OTIO_SCHEMA':'LinearTimeWarp.1','name':'110%','effect_name':'LinearTimeWarp','metadata':{},'time_scalar':1.1}]
 track['children']=[item];track['source_range']['duration']['value']=150
src['tracks']['children']=[v,a]
path=R/'resolve/retime-probe.otio';path.write_text(json.dumps(src))
code='local path='+lua(str(path))+'\nlocal output='+lua(str(R/'qa'))+'\n'+'''
local pm=r:GetProjectManager() local p=pm:GetCurrentProject() assert(not p:IsRenderingInProgress()) assert(pm:SaveProject())
local target="VEL_Eleanor_OldMoney_R4_110pct_2026-09-11"
p=pm:LoadProject(target) or pm:CreateProject(target) assert(p)
p:SetSetting("timelineResolutionWidth","1080") p:SetSetting("timelineResolutionHeight","1920") p:SetSetting("timelineFrameRate","30")
local t=p:GetMediaPool():ImportTimelineFromFile(path,{timelineName="R4-110pct-native-probe"}) assert(t) p:SetCurrentTimeline(t)
local v=t:GetItemListInTrack("video",1)[1] local a=t:GetItemListInTrack("audio",1)[1]
assert(p:SetCurrentRenderFormatAndCodec("mp4","H264")) assert(p:SetCurrentRenderMode(1))
assert(p:SetRenderSettings({SelectAllFrames=true,TargetDir=output,CustomName="retime-probe",ExportVideo=true,ExportAudio=true,FormatWidth=1080,FormatHeight=1920,FrameRate=30,VideoQuality=5000,AudioCodec="aac",AudioSampleRate=48000}))
local job=p:AddRenderJob() assert(job) assert(pm:SaveProject()) assert(p:StartRendering({job}))
return {project=p:GetName(),duration=t:GetEndFrame()-t:GetStartFrame(),video_in=v:GetSourceStartFrame(),video_out=v:GetSourceEndFrame(),audio_in=a:GetSourceStartFrame(),audio_out=a:GetSourceEndFrame(),job=job}
'''
out=run(code);(R/'qa/retime-probe-result.json').write_text(json.dumps(out,indent=2));print(out)
