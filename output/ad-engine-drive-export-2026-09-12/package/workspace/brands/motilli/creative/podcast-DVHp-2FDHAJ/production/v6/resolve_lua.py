import json,sys,subprocess,time
from pathlib import Path
P=Path(__file__).resolve().parent
path=Path(sys.argv[1]).resolve();cmd='dofile('+json.dumps(str(path))+')'
s='''tell application "DaVinci Resolve" to activate
delay 0.4
tell application "System Events" to tell process "Resolve"
set frontmost to true
if (count of text areas of window 1) < 2 then click menu item "Console" of menu "Workspace" of menu bar item "Workspace" of menu bar 1
delay 0.4
perform action "AXRaise" of window 1
click text area 1 of window 1
set value of text area 1 of window 1 to CMD
set focused of text area 1 of window 1 to true
delay 0.3
key code 36
end tell
delay 1
'''.replace('CMD',json.dumps(cmd))
subprocess.run(['osascript','-e',s],check=True)
try:
 out=subprocess.check_output(['osascript','-e','tell application "System Events" to tell process "Resolve" to get value of text area 2 of window 1']).decode();out=out.rsplit('Lua> ',1)[-1];(P/(path.stem+'-console.txt')).write_text(out);print(out)
except subprocess.CalledProcessError:print('Console hid after command; inspect state before rerunning.')
