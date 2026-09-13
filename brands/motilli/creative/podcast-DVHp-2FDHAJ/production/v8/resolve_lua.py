import json,sys,subprocess,time
from pathlib import Path
P=Path(__file__).resolve().parent
path=Path(sys.argv[1]).resolve();cmd='dofile('+json.dumps(str(path))+')'
s='''tell application "DaVinci Resolve" to activate
delay 0.4
tell application "System Events" to tell process "Resolve"
set frontmost to true
set cw to missing value
repeat with w in windows
if (count of text areas of w) >= 2 then set cw to w
end repeat
if cw is missing value then
click menu item "Console" of menu "Workspace" of menu bar item "Workspace" of menu bar 1
delay 1
repeat with w in windows
if (count of text areas of w) >= 2 then set cw to w
end repeat
end if
if cw is missing value then error "Console unavailable"
perform action "AXRaise" of cw
click text area 1 of cw
set value of text area 1 of cw to CMD
set focused of text area 1 of cw to true
delay 0.3
key code 36
end tell
delay 1
'''.replace('CMD',json.dumps(cmd))
subprocess.run(['osascript','-e',s],check=True)
try:
 out=subprocess.check_output(['osascript','-e','tell application "System Events" to tell process "Resolve"\nrepeat with w in windows\nif (count of text areas of w) >= 2 then return value of text area 2 of w\nend repeat\nend tell']).decode();out=out.rsplit('Lua> ',1)[-1];(P/(path.stem+'-console.txt')).write_text(out);print(out)
except subprocess.CalledProcessError:print('Console hid after command; inspect state before rerunning.')
