# /// script
# dependencies = ["pyobjc-framework-ApplicationServices", "pyobjc-framework-Quartz", "pyobjc-framework-Cocoa"]
# ///
import importlib.util,json,time,subprocess,shutil,sys
from pathlib import Path
from AppKit import NSWorkspace,NSApplicationActivateIgnoringOtherApps,NSApplicationActivateAllWindows
from ApplicationServices import AXUIElementPerformAction,AXUIElementSetAttributeValue
R=Path(__file__).resolve().parent;out=R/'capcut/exports';out.mkdir(exist_ok=True)
spec=importlib.util.spec_from_file_location('b',Path('_engine/mcp/capcut-kit/capcut-bridge.py'));b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
for a in NSWorkspace.sharedWorkspace().runningApplications():
 if a.localizedName()=='CapCut':a.activateWithOptions_(NSApplicationActivateIgnoringOtherApps|NSApplicationActivateAllWindows)
time.sleep(3);b._fronted=True
for key in ['AXManualAccessibility','AXEnhancedUserInterface']:AXUIElementSetAttributeValue(b.ax_app(),key,True)
time.sleep(3)
# Dismiss only the observed native folder-selection sheet, leaving export settings intact.
for e,n,g in b.elements():
 if n=='Cancel' and b.attr(e,'AXRole')=='AXButton':AXUIElementPerformAction(e,'AXPress');time.sleep(1);break
if not b.find_one('ExportOkBtn',timeout=2):
 b.click_element('MainWindowTitleBarExportBtn',timeout=20);time.sleep(5)
assert b.find_one('ExportOkBtn',timeout=20),'Export dialog not available'
b.click_element('ExportEncoderInput');time.sleep(2);assert b.find_one('H.264',timeout=12),'H264 option missing';b.click_element('H.264');time.sleep(2)
for e,n,g in b.elements('automationbackupCheckBox'):
 if b.attr(e,'AXRole')=='AXCheckBox' and b.attr(e,'AXValue')==1:AXUIElementPerformAction(e,'AXPress');time.sleep(1);break
targets=[Path(n) for _,n,_ in b.elements() if n.startswith('/Users/') and n.endswith('.mp4')];assert targets
target=targets[0];variant=sys.argv[1];assert f'HOOK-{variant}-' in target.name and target.stem.endswith('-R3');assert not target.exists(),str(target)
settings=[{'name':n,'value':b.attr(e,'AXValue')} for e,n,g in b.elements() if n in ['ExportSharpnessInput','ExportEncoderInput','FrameRateInput','automationbackupCheckBox']];(R/'capcut'/f'export-{variant}-settings.json').write_text(json.dumps(settings,indent=2))
b.click_element('ExportOkBtn');print('Export started',target,flush=True)
last=-1;stable=0
for i in range(150):
 time.sleep(2)
 if target.exists():
  size=target.stat().st_size;stable=stable+1 if size==last and size>0 else 0;last=size
  if stable>=3:
   p=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(target)],capture_output=True,text=True)
   if p.returncode==0 and abs(float(p.stdout)-95.9)<.15:break
else:raise RuntimeError('Native export did not complete')
shutil.copy2(target,out/f'MOT-VID-013-Hook-{variant}-R3.mp4');print('Export complete',variant,last,flush=True)
if b.find_one('automationcloseBtn',timeout=8):b.click_element('automationcloseBtn')
b.send_key('cmd+s')
