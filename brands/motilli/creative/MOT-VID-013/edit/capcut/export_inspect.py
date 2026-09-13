# /// script
# dependencies = ["pyobjc-framework-ApplicationServices", "pyobjc-framework-Quartz"]
# ///
exec(open('brands/motilli/creative/MOT-VID-013/edit/capcut/dismiss_update.py').read().split('for w in')[0])
for el,n,g in b.elements():
 if n in ['ExportSharpnessInput','ExportbitRateInput','ExportEncoderInput','ExportFormatInput','FrameRateInput','automationbackupCheckBox','automationvideoEnhanceCheckBtn','automationcompleteFrameCheckBtn','ExportFileNameInput']:
  def v(e,dep):
   print(n,' '*dep,b.attr(e,'AXRole'),b.attr(e,'AXTitle'),b.attr(e,'AXDescription'),b.attr(e,'AXValue'))
  b.walk(el,v)
