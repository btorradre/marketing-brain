"""Run a task-specific Lua script through Resolve's supported Scripts menu.

Uses a tagged Lua diagnostic to retrieve results from ResolveDebug.txt because
the safe internal Lua environment has no io module. Never touches other projects
unless the supplied operation explicitly saves them before creating our project.
"""
import argparse
import json
import subprocess
import time
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPT = Path.home() / 'Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/Utility/weekender_haaland_build.lua'
LOG = Path.home() / 'Library/Application Support/Blackmagic Design/DaVinci Resolve/logs/ResolveDebug.txt'

def run(source, timeout=90):
    tag = 'VELANTRA_' + uuid.uuid4().hex
    wrapper = '''local function encode(x)
 if x == nil then return "null" end
 if type(x) == "boolean" or type(x) == "number" then return tostring(x) end
 if type(x) == "string" then return '"' .. x:gsub('\\\\','\\\\\\\\'):gsub('"','\\\\"'):gsub('\\n','\\\\n'):gsub('\\r','\\\\r') .. '"' end
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
''' + source + '\nend)\nerror("' + tag + ' " .. encode({ok=ok,result=result}))\n'
    SCRIPT.parent.mkdir(parents=True, exist_ok=True)
    SCRIPT.write_text(wrapper)
    offset = LOG.stat().st_size
    apple = '''tell application "System Events" to tell process "Resolve"
set frontmost to true
click menu bar item "Workspace" of menu bar 1
click menu item "weekender_haaland_build" of menu 1 of menu item "Scripts" of menu "Workspace" of menu bar 1
end tell'''
    subprocess.run(['osascript', '-e', apple], capture_output=True, text=True, check=True)
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        with LOG.open() as f:
            f.seek(offset)
            data = f.read()
        for line in data.splitlines():
            if tag + ' ' in line:
                result = json.loads(line.split(tag + ' ', 1)[1])
                (HERE / 'lua-last-result.json').write_text(json.dumps(result, indent=2)+'\n')
                return result
        time.sleep(.3)
    raise TimeoutError('No tagged Lua result; inspect Resolve before retrying mutations.')

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('script', type=Path)
    p.add_argument('--timeout', type=int, default=90)
    args = p.parse_args()
    print(json.dumps(run(args.script.read_text(), args.timeout), indent=2))
