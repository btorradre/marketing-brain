local r=fu:GetResolve();local pm=r:GetProjectManager();local p=pm:GetCurrentProject();local mp=p:GetMediaPool();local final=p:GetCurrentTimeline();local base='/Users/brooksorradre2/Documents/marketing brain/brands/motilli/creative/podcast-DVHp-2FDHAJ/production/v5/';local jobs={}
assert(not p:IsRenderingInProgress())
for _,role in ipairs({'host','guest'}) do
 local tl=mp:CreateEmptyTimeline('Master '..role..' clean framing');assert(tl);p:SetCurrentTimeline(tl);tl:SetStartTimecode('00:00:00:00')
 local a=mp:ImportMedia({base..'normalized/'..role..'-30fps.mp4',base..'normalized/'..role..'-audio.wav'});assert(a and #a==2);local frames=role=='host' and 907 or 5040
 local v=mp:AppendToTimeline({{mediaPoolItem=a[1],startFrame=0,endFrame=frames,recordFrame=0,trackIndex=1,mediaType=1}})[1];assert(v:SetProperty({ZoomX=1.12,ZoomY=1.12}));local audio=mp:AppendToTimeline({{mediaPoolItem=a[2],startFrame=0,endFrame=frames,recordFrame=0,trackIndex=1,mediaType=2}})[1];assert(tl:GetEndFrame()==frames)
 p:SetCurrentRenderMode(1);p:SetCurrentRenderFormatAndCodec('mp4','H264');p:SetRenderSettings({TargetDir=base..'deliverables',CustomName='Motilli-'..role..'-AvatarV-Master',SelectAllFrames=true,FormatWidth=1080,FormatHeight=1920,FrameRate=30,ExportVideo=true,ExportAudio=true,VideoQuality=14000,AudioCodec='aac',AudioSampleRate=48000})
 local id=p:AddRenderJob();jobs[#jobs+1]=id;print('MASTER_JOB',role,id)
end
p:SetCurrentTimeline(final);print('RENDER_MASTERS',p:StartRendering(jobs));pm:SaveProject()
