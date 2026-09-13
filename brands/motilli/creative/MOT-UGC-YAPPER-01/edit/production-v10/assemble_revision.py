from pathlib import Path
import json,shutil,re
O=Path(__file__).resolve().parent
code='''local r=fu:GetResolve();local pm=r:GetProjectManager();local p=pm:GetCurrentProject();assert(not p:IsRenderingInProgress());if p:GetName()~='MOT-UGC-YAPPER-01 v7 V3 20260910' then assert(pm:SaveProject());p=pm:LoadProject('MOT-UGC-YAPPER-01 v7 V3 20260910');assert(p) end
local old=nil;for i=1,p:GetTimelineCount() do local t=p:GetTimelineByIndex(i);if t:GetName()=='v9 FINAL - apigenin research' then old=t end;assert(t:GetName()~='v10 FINAL - centered square overlays','V10 exists; inspect before repeating') end;assert(old);p:SetCurrentTimeline(old);local t=old:DuplicateTimeline('v10 FINAL - centered square overlays');assert(t);p:SetCurrentTimeline(t);local mp=p:GetMediaPool();local target=nil;local research=nil
for _,c in ipairs(t:GetItemListInTrack('video',2)) do if c:GetStart()==4197 and c:GetEnd()==4317 then target=c elseif c:GetStart()==4619 and c:GetEnd()==4751 then research=c end end;assert(target and research);assert(t:DeleteClips({target},false));local m=mp:ImportMedia({ASSET})[1];assert(m);local new=mp:AppendToTimeline({{mediaPoolItem=m,startFrame=0,endFrame=120,recordFrame=4197,trackIndex=2,mediaType=1}})[1];assert(new);assert(new:SetProperty({ZoomX=2/3,ZoomY=2/3,Pan=0,Tilt=-(1672-941)*720/941/2,CropTop=0,CropBottom=839,CropLeft=0,CropRight=0}));assert(new:GetStart()==4197 and new:GetEnd()==4317)
assert(research:SetProperty({ZoomX=2/3,ZoomY=2/3,Pan=0,Tilt=-280,CropTop=0,CropBottom=840,CropLeft=0,CropRight=0}));local n=0;for _,c in ipairs(t:GetItemListInTrack('video',3)) do if c:GetStart()>=4197 and c:GetEnd()<=4317 then assert(c:SetProperty('Tilt',0));n=n+1 end end;assert(n>0)
assert(t:GetEndFrame()==8327);assert(#t:GetItemListInTrack('video',1)==16);assert(#t:GetItemListInTrack('video',2)==21);assert(#t:GetItemListInTrack('video',3)==229);assert(#t:GetItemListInTrack('audio',1)==16);assert(pm:SaveProject());print('V10_ASSEMBLED',t:GetEndFrame(),'CAPTIONS_RESET',n);print('POST_GEOMETRY',new:GetProperty('CropBottom'),new:GetProperty('ZoomX'),new:GetProperty('Tilt'));print('PAPER_GEOMETRY',research:GetProperty('CropBottom'),research:GetProperty('ZoomX'),research:GetProperty('Tilt'))
'''.replace('ASSET',json.dumps(str(O/'group-post-deborah.mov')))
export=(O.parent/'production-v9/export-v9.lua').read_text().replace('v9 FINAL - apigenin research','v10 FINAL - centered square overlays').replace('production-v9','production-v10').replace('VSL-v9','VSL-v10').replace('-v9-FINAL','-v10-FINAL').replace('V9_','V10_')
(O/'export-v10.lua').write_text(export)
code+=export[export.index("print('V10_DRP'"):]
(O/'assemble-v10.lua').write_text(code)
shutil.copy2(O.parent/'production-v9/deliverables/Motilli-Unbranded-VSL-v9.srt',O/'deliverables/Motilli-Unbranded-VSL-v10.srt')
import resolve_lua
resolve_lua.run(code,'assemble-v10')
