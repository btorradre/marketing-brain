local p=r:GetProjectManager():GetCurrentProject() assert(p:GetName()=="VEL_Eleanor_OldMoney_9Ads_2026-09-11")
local pool=p:GetMediaPool()
local t=pool:CreateEmptyTimeline("_compositing_probe") assert(t) p:SetCurrentTimeline(t)
local clips=pool:ImportMedia({[=[/Users/brooksorradre2/Documents/marketing brain/brands/velantra/creative/old-money-look-2026-09-10/production/avatars/VEL-OM-H1-A2/avatar-native.mp4]=]})
local items=pool:AppendToTimeline({{mediaPoolItem=clips[1],startFrame=0,endFrame=74,mediaType=1}}) assert(items and items[1])
local c=items[1]:AddFusionComp() assert(c)
local k=c:AddTool("DeltaKeyer") assert(k)
local inputs={} for _,v in pairs(k:GetInputList()) do local a=v:GetAttrs() inputs[a.INPS_ID]={name=a.INPS_Name,type=a.INPS_DataType,value=tostring(v[0])} end
local nodes={} for _,v in pairs(c:GetToolList(false)) do nodes[v:GetAttrs().TOOLS_Name]=v:GetAttrs().TOOLS_RegID end
r:GetProjectManager():SaveProject()
return {inputs=inputs,nodes=nodes,properties=items[1]:GetProperties()}
