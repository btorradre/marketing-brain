# /// script
# dependencies = ["pyobjc-framework-ApplicationServices", "pyobjc-framework-Quartz"]
# ///
import importlib.util,time,subprocess,shutil
from pathlib import Path
p=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('b',p.parents[5]/'_engine/mcp/capcut-kit/capcut-bridge.py');b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
b.ensure_front();time.sleep(2)
if not b.find_one('ExportOkBtn'):
 b.click_element('MainWindowTitleBarExportBtn');time.sleep(2);assert b.find_one('ExportOkBtn',timeout=12)
b.click_element('ExportEncoderInput');time.sleep(2);assert b.find_one('H.264',timeout=8)
b.click_element('H.264');time.sleep(2)
for el,n,g in b.elements('automationbackupCheckBox'):
 if b.attr(el,'AXRole')=='AXCheckBox' and b.attr(el,'AXValue')==1:b.click_at(g[0]+g[2]/2,g[1]+g[3]/2);break
targets=[Path(n) for _,n,_ in b.elements() if n.startswith('/Users/') and n.endswith('.mp4')];assert targets;target=targets[0];assert 'R2-1.1x-A' in target.name;assert not target.exists();b.click_element('ExportOkBtn');print('Exporting',target.name,flush=True)
last=-1;stable=0
for _ in range(90):
 time.sleep(2)
 if target.exists():
  sz=target.stat().st_size;stable=stable+1 if sz==last and sz>0 else 0;last=sz
  if stable>=3:
   r=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(target)],capture_output=True,text=True)
   if r.returncode==0 and abs(float(r.stdout)-95.9)<.15:break
else:raise RuntimeError('Export did not finish')
(p/'exports').mkdir(exist_ok=True);shutil.copy2(target,p/'exports/MOT-VID-013-R2-A.mp4')
if b.find_one('automationcloseBtn',timeout=15):b.click_element('automationcloseBtn')
print('A exported',flush=True)
