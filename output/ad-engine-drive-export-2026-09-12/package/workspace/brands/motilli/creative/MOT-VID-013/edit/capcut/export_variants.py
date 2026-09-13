# /// script
# dependencies = ["pyobjc-framework-ApplicationServices", "pyobjc-framework-Quartz"]
# ///
import importlib.util,json,time,subprocess,shutil
from pathlib import Path
spec=importlib.util.spec_from_file_location('b',Path('_engine/mcp/capcut-kit/capcut-bridge.py'));b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
here=Path('brands/motilli/creative/MOT-VID-013/edit/capcut');out=here/'exports';out.mkdir(exist_ok=True)
for variant in 'ABC':
 if b.app_pid():
  if b.find_one('automationcloseBtn'):b.click_element('automationcloseBtn')
  b.send_key('cmd+s');time.sleep(.5);b.quit_app()
 b.cmd_open('MOT-VID-013-science-CapCut-'+variant)
 b.click_element('MainWindowTitleBarExportBtn');assert b.find_one('ExportOkBtn',timeout=12),'Missing native export controls'
 for el,n,g in b.elements('automationbackupCheckBox'):
  if b.attr(el,'AXRole')=='AXCheckBox' and b.attr(el,'AXValue')==1:b.click_at(g[0]+g[2]/2,g[1]+g[3]/2);break
 b.click_element('ExportEncoderInput');time.sleep(.4);b.click_element('H.264');time.sleep(.4)
 targets=[Path(n) for _,n,_ in b.elements() if n.startswith('/Users/') and n.endswith('.mp4')]
 assert targets,'No verified export path in AX tree'
 target=targets[0];assert not target.exists(),str(target)+' exists'
 b.click_element('ExportOkBtn');print('Export started '+variant,flush=True)
 last=-1;stable=0;done=False
 for tick in range(90):
  time.sleep(2)
  if target.exists():
   sz=target.stat().st_size;stable=stable+1 if sz==last and sz>0 else 0;last=sz
   if stable>=3:
    pr=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(target)],capture_output=True,text=True)
    if pr.returncode==0 and float(pr.stdout)>96:done=True;break
 assert done,'Export did not finish '+variant
 shutil.copy2(target,out/f'MOT-VID-013-{variant}.mp4');print('Export complete '+variant+' '+str(last)+' bytes',flush=True)
b.click_element('automationcloseBtn');b.send_key('cmd+s');print('All three native CapCut exports delivered to '+str(out),flush=True)
