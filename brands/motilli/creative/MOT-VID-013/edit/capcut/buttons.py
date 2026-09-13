# /// script
# dependencies = ["pyobjc-framework-ApplicationServices", "pyobjc-framework-Quartz"]
# ///
exec(open('brands/motilli/creative/MOT-VID-013/edit/capcut/dismiss_update.py').read().split('for w in')[0])
from ApplicationServices import AXUIElementCopyActionNames
for el,n,g in b.elements():
 if g and 504<=g[0]<=1224 and 259<=g[1]<=892:
  role=b.attr(el,'AXRole');acts=AXUIElementCopyActionNames(el,None)
  if role not in ['AXStaticText','AXGroup','AXSplitGroup'] or acts[1]:print(role,n,repr(b.attr(el,'AXValue')),g,acts)
