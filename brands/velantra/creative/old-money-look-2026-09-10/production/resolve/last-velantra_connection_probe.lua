local result = {}
local ok, err = pcall(function()
 local r = resolve or (bmd and bmd.scriptapp("Resolve"))
 table.insert(result, "resolve=" .. tostring(r ~= nil))
 if r then
  table.insert(result, "product=" .. tostring(r:GetProductName()))
  table.insert(result, "version=" .. tostring(r:GetVersionString()))
  local pm = r:GetProjectManager()
  local p = pm and pm:GetCurrentProject()
  table.insert(result, "project=" .. (p and p:GetName() or "none"))
 end
end)
if not ok then table.insert(result, "error=" .. tostring(err)) end
print("VELANTRA_PROBE_BEGIN")
print(table.concat(result,"\n"))
print("VELANTRA_PROBE_END")

error("VELANTRA_PROBE " .. table.concat(result, " | "))
