import sys,json,subprocess
from pathlib import Path
OUT=Path(__file__).resolve().parent
def run(code,name='command'):
 path=OUT/f'{name}.lua';path.write_text(code)
 command='dofile('+json.dumps(str(path))+')'
 template=(OUT/'resolve-console-template.applescript').read_text()
 template=template.replace('"print(\'YAPPER_LIVE\',fu:GetResolve():GetProjectManager():GetCurrentProject():GetName())"',json.dumps(command))
 result=subprocess.check_output(['osascript','-e',template]).decode()
 if len(result.strip())<3:
  import time
  time.sleep(2)
  result=subprocess.check_output(['osascript',str(OUT/'resolve-console-template.applescript')]).decode()
 last=result[result.rfind(command):] if command in result else result[-8000:];(OUT/f'{name}-console.txt').write_text(last);print(last);return last
if __name__=='__main__':run(Path(sys.argv[1]).read_text(),Path(sys.argv[1]).stem)
