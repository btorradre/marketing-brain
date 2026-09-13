import sys,json,subprocess
from pathlib import Path
OUT=Path(__file__).resolve().parent

def run(code,name='command'):
    path=OUT/f'{name}.lua';path.write_text(code)
    command='dofile('+json.dumps(str(path))+')'
    script='tell application "DaVinci Resolve" to activate\ntell application "System Events" to tell process "Resolve"\nif (count of text areas of window 1) < 2 then click menu item "Console" of menu "Workspace" of menu bar item "Workspace" of menu bar 1\ndelay 0.5\nset value of text area 1 of window 1 to '+json.dumps(command)+'\nset focused of text area 1 of window 1 to true\nend tell\ntell application "System Events" to key code 36\ndelay 0.5'
    subprocess.run(['osascript','-e',script],check=True)
    subprocess.run(['osascript','-e','tell application "DaVinci Resolve" to activate\ntell application "System Events" to tell process "Resolve"\nif (count of text areas of window 1) < 2 then click menu item "Console" of menu "Workspace" of menu bar item "Workspace" of menu bar 1\nend tell\ndelay 0.5'],check=True)
    response=subprocess.check_output(['osascript','-e','tell application "System Events" to tell process "Resolve" to get value of text area 2 of window 1']).decode()
    last=response.rsplit('Lua> ',1)[-1]
    (OUT/f'{name}-console.txt').write_text(last)
    print(last)
    return last
if __name__=='__main__':run(Path(sys.argv[1]).read_text(),Path(sys.argv[1]).stem)
