# /// script
# dependencies = ["pyobjc-framework-ApplicationServices", "pyobjc-framework-Quartz", "pyobjc-framework-Cocoa"]
# ///
import importlib.util,json,time,sys,runpy
from pathlib import Path
from AppKit import NSWorkspace,NSApplicationActivateIgnoringOtherApps,NSApplicationActivateAllWindows
from ApplicationServices import AXUIElementPerformAction,AXUIElementSetAttributeValue
R=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('b',Path('_engine/mcp/capcut-kit/capcut-bridge.py'));b=importlib.util.module_from_spec(sp);sp.loader.exec_module(b)
projects={x['variant']:x for x in json.loads((R/'capcut/projects.json').read_text())}
def front():
 for a in NSWorkspace.sharedWorkspace().runningApplications():
  if a.localizedName()=='CapCut':a.activateWithOptions_(NSApplicationActivateIgnoringOtherApps|NSApplicationActivateAllWindows)
 time.sleep(3);b._fronted=True
 for key in ['AXManualAccessibility','AXEnhancedUserInterface']:AXUIElementSetAttributeValue(b.ax_app(),key,True)
 time.sleep(2)
for v in list(sys.argv[1:] or 'BC'):
 if b.app_pid():
  front()
  for label in ['automationcancel','automationcloseBtn']:
   hit=b.find_one(label)
   if hit:b.click_element(label);time.sleep(1)
  b.send_key('cmd+s');time.sleep(1);b.quit_app()
 b.cmd_open(projects[v]['name']);front()
 sys.argv=['export_native_current.py',v];runpy.run_path(str(R/'export_native_current.py'),run_name='__main__')
