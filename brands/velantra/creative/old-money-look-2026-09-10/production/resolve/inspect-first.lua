local p=r:GetProjectManager():GetCurrentProject() local t=p:GetCurrentTimeline()
assert(t:GetName()=="VEL-OM-H1-A2")
local frames={0,150,390,750,1350,1537} local out={}
for _,f in ipairs(frames) do
 local tc=string.format("%02d:%02d:%02d:%02d",math.floor(f/108000),math.floor(f/1800)%60,math.floor(f/30)%60,f%30)
 assert(t:SetCurrentTimecode(tc))
 local path=[=[/Users/brooksorradre2/Documents/marketing brain/brands/velantra/creative/old-money-look-2026-09-10/production/qa/H1-A2-native-]=]..f..".jpg"
 out[tostring(f)]=p:ExportCurrentFrameAsStill(path)
end
return out
