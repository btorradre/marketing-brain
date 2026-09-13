# /// script
# dependencies = ["pyobjc-framework-ApplicationServices", "pyobjc-framework-Quartz"]
# ///
import importlib.util,json,time,subprocess,shutil,sys
from pathlib import Path
spec=importlib.util.spec_from_file_location('b',Path('_engine/mcp/capcut-kit/capcut-bridge.py'));b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
here=Path(__file__).resolve().parent;out=here/'exports';out.mkdir(exist_ok=True)
for variant in (sys.argv[1:] or list('ABC')):
 if b.app_pid():
  if b.find_one('automationcloseBtn'):b.click_element('automationcloseBtn')
  b.send_key('cmd+s');time.sleep(.5);b.quit_app()
 b.cmd_open('MOT-VID-013-R2-1.1x-'+variant)
 b._fronted=False;b.ensure_front();time.sleep(2)
 b.click_element('MainWindowTitleBarExportBtn');time.sleep(2);assert b.find_one('ExportOkBtn',timeout=12),'Missing native export controls'
 for el,n,g in b.elements('automationbackupCheckBox'):
  if b.attr(el,'AXRole')=='AXCheckBox' and b.attr(el,'AXValue')==1:b.click_at(g[0]+g[2]/2,g[1]+g[3]/2);break
 b.click_element('ExportEncoderInput');time.sleep(2);assert b.find_one('H.264',timeout=8);b.click_element('H.264');time.sleep(2)
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
    if pr.returncode==0 and abs(float(pr.stdout)-95.9)<0.15:done=True;break
 assert done,'Export did not finish '+variant
 shutil.copy2(target,out/f'MOT-VID-013-R2-{variant}.mp4');print('Export complete '+variant+' '+str(last)+' bytes',flush=True)
b.click_element('automationcloseBtn');b.send_key('cmd+s');print('Requested native CapCut exports delivered to '+str(out),flush=True)
