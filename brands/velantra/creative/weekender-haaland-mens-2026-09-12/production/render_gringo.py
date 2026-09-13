from pathlib import Path
import sys,json
P=Path(__file__).resolve().parent;R=P/'resolve-gringo';sys.path.insert(0,str(R));from run_lua import run
E=P/'exports';E.mkdir(exist_ok=True)
src='local output=[=['+str(E)+']=]\n'+r'''
local pm=r:GetProjectManager() local p=pm:GetCurrentProject() assert(p:GetName()=="VEL_Weekender_Haaland_20260912") assert(not p:IsRenderingInProgress())
local t=p:GetCurrentTimeline() assert(t:GetName()=="Weekender-Haaland-Gringo-Natural-AvatarV-v1")
assert(p:SetCurrentRenderFormatAndCodec("mp4","H264")) assert(p:SetCurrentRenderMode(1))
assert(p:SetRenderSettings({SelectAllFrames=true,TargetDir=output,CustomName="Weekender-Haaland-Gringo-Natural-AvatarV",ExportVideo=true,ExportAudio=true,FormatWidth=1080,FormatHeight=1920,FrameRate=30,VideoQuality=16000,AudioCodec="aac",AudioSampleRate=48000,NetworkOptimization=true}))
assert(pm:SaveProject())
local id=p:AddRenderJob() assert(id) assert(p:StartRendering({id})) return {project=p:GetName(),timeline=t:GetName(),job=id,started=true}
'''
out=run(src);(R/'review-render.json').write_text(json.dumps(out,indent=2));print(out);assert out['ok']
