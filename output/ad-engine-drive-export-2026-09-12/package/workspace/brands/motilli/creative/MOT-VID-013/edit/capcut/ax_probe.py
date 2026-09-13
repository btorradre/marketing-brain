# /// script
# dependencies = ["pyobjc-framework-ApplicationServices", "pyobjc-framework-Quartz"]
# ///
import importlib.util
from pathlib import Path
from ApplicationServices import AXUIElementCopyActionNames,AXIsProcessTrusted
from Quartz import CGPreflightScreenCaptureAccess,CGPreflightPostEventAccess
spec=importlib.util.spec_from_file_location('b',Path('_engine/mcp/capcut-kit/capcut-bridge.py'));b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
print('Accessibility trusted',AXIsProcessTrusted(),'Screen recording allowed',CGPreflightScreenCaptureAccess(),'Post events allowed',CGPreflightPostEventAccess())
for w in b.attr(b.ax_app(),'AXWindows') or []:
 print('WINDOW',b.attr(w,'AXTitle'))
 if b.attr(w,'AXTitle')!='CapCut':
  def visit(e,dep):
   print(' '*dep,b.attr(e,'AXRole'),b.attr(e,'AXTitle'),b.attr(e,'AXDescription'),str(b.attr(e,'AXValue'))[:100],b.geometry(e),AXUIElementCopyActionNames(e,None))
  b.walk(w,visit)
