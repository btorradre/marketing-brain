r=fu:GetResolve(); p=r:GetProjectManager():GetCurrentProject(); t=p:GetCurrentTimeline(); mp=p:GetMediaPool()
print('PROJECT',p:GetName(),t:GetName(),t:GetSetting('timelineFrameRate'),t:GetSetting('timelineResolutionWidth'))
print('IMPORT')
local x=mp:ImportMedia({'/Users/brooksorradre2/Documents/marketing brain/brands/motilli/creative/podcast-DVHp-2FDHAJ/production/v5/host-avatar-master.mp4'})
print(x and #x); if x and x[1] then for k,v in pairs(x[1]:GetClipProperty()) do print(k,v) end end
print('CODECS'); for k,v in pairs(p:GetRenderCodecs('mp4')) do print(k,v) end
