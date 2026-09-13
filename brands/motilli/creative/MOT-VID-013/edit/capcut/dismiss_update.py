# /// script
# dependencies = ["pyobjc-framework-ApplicationServices", "pyobjc-framework-Quartz"]
# ///
import importlib.util
from pathlib import Path
from ApplicationServices import AXUIElementPerformAction
spec=importlib.util.spec_from_file_location('b',Path('_engine/mcp/capcut-kit/capcut-bridge.py'));b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
for w in b.attr(b.ax_app(),'AXWindows') or []:
 if b.attr(w,'AXTitle')=='Version update':
  for e in b.attr(w,'AXChildren') or []:
   if b.attr(e,'AXRole')=='AXButton':print('Dismiss update dialog',AXUIElementPerformAction(e,'AXPress'))
