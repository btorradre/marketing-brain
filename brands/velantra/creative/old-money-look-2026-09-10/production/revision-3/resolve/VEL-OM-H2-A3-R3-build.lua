local ad={[ [=[name]=] ]=[=[VEL-OM-H2-A3-R3]=],[ [=[id]=] ]=[=[VEL-OM-H2-A3]=],[ [=[hook]=] ]=[=[H2]=],[ [=[avatar]=] ]=[=[A3]=],[ [=[otio]=] ]=[=[/Users/brooksorradre2/Documents/marketing brain/brands/velantra/creative/old-money-look-2026-09-10/production/revision-3/resolve/VEL-OM-H2-A3-R3.otio]=],[ [=[duration_frames]=] ]=1644,[ [=[green]=] ]={0.06666666666666667,0.5803921568627451,0.21176470588235294},[ [=[overlay_clips]=] ]=10,[ [=[final_hold_frames]=] ]=3,[ [=[captions]=] ]={{[ [=[in]=] ]=0,[ [=[out]=] ]=74,[ [=[text]=] ]=[=[Before you buy another outfit
to get that old money]=],[ [=[verbatim]=] ]=[=[Before you buy another outfit to get that old money]=]},{[ [=[in]=] ]=74,[ [=[out]=] ]=139,[ [=[text]=] ]=[=[look, try changing your bag.]=],[ [=[verbatim]=] ]=[=[look, try changing your bag.]=]},{[ [=[in]=] ]=139,[ [=[out]=] ]=176,[ [=[text]=] ]=[=[Keep the clothes.]=],[ [=[verbatim]=] ]=[=[Keep the clothes.]=]},{[ [=[in]=] ]=176,[ [=[out]=] ]=204,[ [=[text]=] ]=[=[Keep the shoes.]=],[ [=[verbatim]=] ]=[=[Keep the shoes.]=]},{[ [=[in]=] ]=204,[ [=[out]=] ]=290,[ [=[text]=] ]=[=[Just swap this in and look at
the difference.]=],[ [=[verbatim]=] ]=[=[Just swap this in and look at the difference.]=]},{[ [=[in]=] ]=290,[ [=[out]=] ]=362,[ [=[text]=] ]=[=[Suddenly, the same outfit
feels a whole lot more]=],[ [=[verbatim]=] ]=[=[Suddenly, the same outfit feels a whole lot more]=]},{[ [=[in]=] ]=362,[ [=[out]=] ]=462,[ [=[text]=] ]=[=[expensive. This is the
Eleanor Weekender from
Velantra.]=],[ [=[verbatim]=] ]=[=[expensive. This is the Eleanor Weekender from Velantra.]=]},{[ [=[in]=] ]=462,[ [=[out]=] ]=510,[ [=[text]=] ]=[=[It's perfect for travel,]=],[ [=[verbatim]=] ]=[=[It's perfect for travel,]=]},{[ [=[in]=] ]=510,[ [=[out]=] ]=588,[ [=[text]=] ]=[=[or just upgrading your
everyday outfit with that old]=],[ [=[verbatim]=] ]=[=[or just upgrading your everyday outfit with that old]=]},{[ [=[in]=] ]=588,[ [=[out]=] ]=651,[ [=[text]=] ]=[=[money look. It's
Birkin-inspired,]=],[ [=[verbatim]=] ]=[=[money look. It's Birkin-inspired,]=]},{[ [=[in]=] ]=651,[ [=[out]=] ]=699,[ [=[text]=] ]=[=[with that classic shape,]=],[ [=[verbatim]=] ]=[=[with that classic shape,]=]},{[ [=[in]=] ]=699,[ [=[out]=] ]=794,[ [=[text]=] ]=[=[top handles, and gold-tone
details that make the whole]=],[ [=[verbatim]=] ]=[=[top handles, and gold-tone details that make the whole]=]},{[ [=[in]=] ]=794,[ [=[out]=] ]=852,[ [=[text]=] ]=[=[outfit feel more expensive.]=],[ [=[verbatim]=] ]=[=[outfit feel more expensive.]=]},{[ [=[in]=] ]=852,[ [=[out]=] ]=912,[ [=[text]=] ]=[=[You don't need a whole new
wardrobe to look put]=],[ [=[verbatim]=] ]=[=[You don't need a whole new wardrobe to look put]=]},{[ [=[in]=] ]=912,[ [=[out]=] ]=993,[ [=[text]=] ]=[=[together. You need that one
piece that makes what you]=],[ [=[verbatim]=] ]=[=[together. You need that one piece that makes what you]=]},{[ [=[in]=] ]=993,[ [=[out]=] ]=1049,[ [=[text]=] ]=[=[already own work harder.]=],[ [=[verbatim]=] ]=[=[already own work harder.]=]},{[ [=[in]=] ]=1049,[ [=[out]=] ]=1090,[ [=[text]=] ]=[=[Throw on a white shirt,]=],[ [=[verbatim]=] ]=[=[Throw on a white shirt,]=]},{[ [=[in]=] ]=1090,[ [=[out]=] ]=1119,[ [=[text]=] ]=[=[your favorite jeans,]=],[ [=[verbatim]=] ]=[=[your favorite jeans,]=]},{[ [=[in]=] ]=1119,[ [=[out]=] ]=1171,[ [=[text]=] ]=[=[and grab this on your way
out.]=],[ [=[verbatim]=] ]=[=[and grab this on your way out.]=]},{[ [=[in]=] ]=1171,[ [=[out]=] ]=1252,[ [=[text]=] ]=[=[Suddenly, an outfit you
barely thought about looks]=],[ [=[verbatim]=] ]=[=[Suddenly, an outfit you barely thought about looks]=]},{[ [=[in]=] ]=1252,[ [=[out]=] ]=1346,[ [=[text]=] ]=[=[intentional. If you keep
saving old money outfits but]=],[ [=[verbatim]=] ]=[=[intentional. If you keep saving old money outfits but]=]},{[ [=[in]=] ]=1346,[ [=[out]=] ]=1409,[ [=[text]=] ]=[=[feel like yours are missing
something,]=],[ [=[verbatim]=] ]=[=[feel like yours are missing something,]=]},{[ [=[in]=] ]=1409,[ [=[out]=] ]=1451,[ [=[text]=] ]=[=[try starting with the bag.]=],[ [=[verbatim]=] ]=[=[try starting with the bag.]=]},{[ [=[in]=] ]=1451,[ [=[out]=] ]=1529,[ [=[text]=] ]=[=[So if you want that old money
look without spending]=],[ [=[verbatim]=] ]=[=[So if you want that old money look without spending]=]},{[ [=[in]=] ]=1529,[ [=[out]=] ]=1571,[ [=[text]=] ]=[=[like you inherited it,]=],[ [=[verbatim]=] ]=[=[like you inherited it,]=]},{[ [=[in]=] ]=1571,[ [=[out]=] ]=1644,[ [=[text]=] ]=[=[tap the link and get your
Eleanor Weekender.]=],[ [=[verbatim]=] ]=[=[tap the link and get your Eleanor Weekender.]=]}}}
local compdir=[=[/Users/brooksorradre2/Documents/marketing brain/brands/velantra/creative/old-money-look-2026-09-10/production/revision-3/resolve/comps/]=]

local pm=r:GetProjectManager() local p=pm:GetCurrentProject()
assert(p:GetName()=="VEL_Eleanor_OldMoney_ContinuousPresenter_R3_2026-09-11","Wrong project")
assert(not p:IsRenderingInProgress())
for n=1,p:GetTimelineCount() do assert(p:GetTimelineByIndex(n):GetName()~=ad.name,"Timeline already exists; inspect") end
local t=p:GetMediaPool():ImportTimelineFromFile(ad.otio,{timelineName=ad.name}) assert(t)
p:SetCurrentTimeline(t)
assert(t:GetEndFrame()-t:GetStartFrame()==ad.duration_frames)
local presenters=t:GetItemListInTrack("video",2) assert(#presenters==ad.overlay_clips)
local function commit(item,c,path)
 c:Unlock() assert(item:ExportFusionComp(path,1)) assert(item:ImportFusionComp(path))
end
for i,item in ipairs(presenters) do
 if ad.avatar~="A1" then
  local c=item:AddFusionComp() assert(c) c:Lock()
  local mi=c:FindTool("MediaIn1") local mo=c:FindTool("MediaOut1") local k=c:AddTool("DeltaKeyer")
  k:SetInput("BackgroundRed",ad.green[1]) k:SetInput("BackgroundGreen",ad.green[2]) k:SetInput("BackgroundBlue",ad.green[3])
  k:SetInput("LowThreshold",0.04) k:SetInput("HighThreshold",0.96)
  k:ConnectInput("Input",mi) mo:ConnectInput("Input",k)
  commit(item,c,compdir..ad.name.."-presenter-"..i..".comp")
 end
 local zoom=0.46 local tilt=-550 local pan=-291.6
 if ad.avatar=="A3" then zoom=0.54 tilt=-485 pan=-248.4 end
 assert(item:SetProperties({ZoomX=zoom,ZoomY=zoom,Pan=pan,Tilt=tilt,RetimeProcess=0}))
end
local caps=t:GetItemListInTrack("video",3) assert(#caps==#ad.captions)
for i,item in ipairs(caps) do
 local c=item:AddFusionComp() assert(c) c:Lock()
 local text=c:AddTool("TextPlus") local mo=c:FindTool("MediaOut1")
 text:SetInput("StyledText",ad.captions[i].text)
 text:SetInput("Font","Arial") text:SetInput("Style","Regular") text:SetInput("Size",0.047)
 text:SetInput("Center",{0.5,0.12}) text:SetInput("VerticalJustification",1) text:SetInput("HorizontalJustification",1)
 text:SetInput("Red1",1) text:SetInput("Green1",1) text:SetInput("Blue1",1)
 text:SetInput("Enabled2",1) text:SetInput("ElementShape2",1)
 text:SetInput("Red2",0) text:SetInput("Green2",0) text:SetInput("Blue2",0) text:SetInput("Alpha2",1)
 text:SetInput("Thickness2",0.03)
 mo:ConnectInput("Input",text)
 commit(item,c,compdir..ad.name.."-caption-"..i..".comp")
end
for _,c in ipairs(t:GetItemListInTrack("video",1)) do assert(c:SetProperty("RetimeProcess",0)) end
assert(pm:SaveProject())
return {project=p:GetName(),timeline=t:GetName(),frames=t:GetEndFrame()-t:GetStartFrame(),presenters=#presenters,captions=#caps}
