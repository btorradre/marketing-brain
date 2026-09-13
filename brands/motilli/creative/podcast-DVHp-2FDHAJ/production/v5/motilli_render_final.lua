local r=fu:GetResolve();local pm=r:GetProjectManager();local p=pm:GetCurrentProject();local t=p:GetCurrentTimeline();assert(t:GetName()=='Motilli Podcast v5 Final 02');assert(t:GetEndFrame()==5917)
local base='/Users/brooksorradre2/Documents/marketing brain/brands/motilli/creative/podcast-DVHp-2FDHAJ/production/v5/'
p:SetCurrentRenderMode(1);assert(p:SetCurrentRenderFormatAndCodec('mp4','H264'))
assert(p:SetRenderSettings({TargetDir=base..'deliverables',CustomName='Motilli-Podcast-HeyGen-v5',SelectAllFrames=true,FormatWidth=1080,FormatHeight=1920,FrameRate=30,ExportVideo=true,ExportAudio=true,AudioCodec='aac',AudioSampleRate=48000,VideoQuality=14000,NetworkOptimization=true}))
local id=p:AddRenderJob();print('FINAL_RENDER_JOB',id);print('STARTED',p:StartRendering(id));pm:SaveProject()
