local function encode(x)
 if x == nil then return "null" end
 if type(x) == "boolean" or type(x) == "number" then return tostring(x) end
 if type(x) == "string" then return '"' .. x:gsub('\\','\\\\'):gsub('"','\\"'):gsub('\n','\\n'):gsub('\r','\\r') .. '"' end
 if type(x) == "table" then
  local parts = {}
  for k,v in pairs(x) do table.insert(parts, encode(tostring(k)) .. ":" .. encode(v)) end
  return "{" .. table.concat(parts, ",") .. "}"
 end
 return encode(tostring(x))
end
local ok, result = pcall(function()
local r = resolve or bmd.scriptapp("Resolve")
assert(r, "No Resolve object")
local pm=r:GetProjectManager() local p=pm:GetCurrentProject()
assert(p:GetName()=="VEL_Eleanor_OldMoney_9Ads_2026-09-11") assert(not p:IsRenderingInProgress())
assert(pm:SaveProject())
local path=[=[/Users/brooksorradre2/Documents/marketing brain/brands/velantra/creative/old-money-look-2026-09-10/production/exports/Eleanor-OldMoney-9Ads.drp]=]
local ok=pm:ExportProject(p:GetName(),path,false)
return {exported=ok,path=path,project=p:GetName()}

end)
error("VELANTRA_862253f5131f415f91247e82bc592a1c " .. encode({ok=ok,result=result}))
