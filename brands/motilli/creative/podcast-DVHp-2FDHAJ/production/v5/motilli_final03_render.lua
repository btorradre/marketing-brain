local r=fu:GetResolve();local pm=r:GetProjectManager();local p=pm:GetCurrentProject();local t=p:GetCurrentTimeline();assert(t:GetName()=='Motilli Podcast v5 Final 03');assert(t:GetEndFrame()==5917)
for i=1,6 do print('TRACK',i,#t:GetItemListInTrack('video',i)) end
p:SetCurrentRenderMode(1);assert(p:SetCurrentRenderFormatAndCodec('mp4','H264'))
assert(p:SetRenderSettings({TargetDir='/Users/brooksorradre2/Documents/marketing brain/brands/motilli/creative/podcast-DVHp-2FDHAJ/production/v5/deliverables',CustomName='Motilli-Podcast-Final',SelectAllFrames=true,FormatWidth=1080,FormatHeight=1920,FrameRate=30,ExportVideo=true,ExportAudio=true,AudioCodec='aac',AudioSampleRate=48000,VideoQuality=14000,NetworkOptimization=true}))
local id=p:AddRenderJob();print('FINAL_JOB',id,p:StartRendering(id));pm:SaveProject()
