r=fu:GetResolve();pm=r:GetProjectManager();p=pm:GetCurrentProject();mp=p:GetMediaPool();local base='/Users/brooksorradre2/Documents/marketing brain/brands/motilli/creative/podcast-DVHp-2FDHAJ/production/v5/'
local tl=mp:CreateEmptyTimeline('QA Framing 01'); assert(tl);p:SetCurrentTimeline(tl);tl:SetStartTimecode('00:00:00:00');tl:AddTrack('video');local clips=mp:ImportMedia({base..'normalized/host-30fps.mp4',base..'normalized/guest-30fps.mp4'})
assert(clips and #clips==2)
local a=mp:AppendToTimeline({{mediaPoolItem=clips[1],startFrame=30,endFrame=149,recordFrame=0,trackIndex=1,mediaType=1}})[1]
local b=mp:AppendToTimeline({{mediaPoolItem=clips[2],startFrame=300,endFrame=419,recordFrame=0,trackIndex=2,mediaType=1}})[1]
print('HOST',a:SetProperty({CropTop=320,CropBottom=640,Pan=0,Tilt=320}))
print('GUEST',b:SetProperty({CropTop=220,CropBottom=740,Pan=0,Tilt=-740}))
for k,v in pairs(a:GetProperty()) do print(k,v) end
p:SetCurrentRenderFormatAndCodec('mp4','H264');p:SetCurrentRenderMode(0)
print('SETTINGS',p:SetRenderSettings({TargetDir=base..'qa',CustomName='framing-01',SelectAllFrames=true,FormatWidth=1080,FormatHeight=1920,FrameRate=30,ExportVideo=true,ExportAudio=false,VideoQuality=12000}))
local id=p:AddRenderJob();print('JOB',id);print('START',p:StartRendering(id));pm:SaveProject()
