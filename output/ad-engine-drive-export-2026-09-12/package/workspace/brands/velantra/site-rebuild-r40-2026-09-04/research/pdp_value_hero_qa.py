from pathlib import Path
from playwright.sync_api import sync_playwright
import json,sys
out=Path(__file__).resolve().parent
families=sys.argv[1:] or ['delphine']
report=[]
with sync_playwright() as p:
 b=p.chromium.launch(headless=True)
 for width in [1440,390]:
  c=b.new_context(viewport={'width':width,'height':1000});page=c.new_page();page.goto('https://velantrafashion.com/?preview_theme_id=151364960321',wait_until='domcontentloaded')
  for family in families:
   page.goto('https://velantrafashion.com/products/velantra-'+family,wait_until='domcontentloaded');value=page.locator('.value-breakdown');value.scroll_into_view_if_needed();page.evaluate('document.fonts.ready')
   for frame in page.frames:
    if frame.name=='PBarNextFrame':
     try:frame.get_by_role('button',name='Hide bar',exact=True).click(timeout=1500)
     except Exception:pass
   page.wait_for_function('(family)=>{const i=document.querySelector(".value-breakdown img");return i&&i.complete&&i.naturalWidth>0&&i.currentSrc.includes(family+"-value-hero")}',arg=family,timeout=60000)
   data=value.locator('img').evaluate('(i)=>({src:i.currentSrc,natural:[i.naturalWidth,i.naturalHeight],box:[i.getBoundingClientRect().width,i.getBoundingClientRect().height],fit:getComputedStyle(i).objectFit,alt:i.alt})')
   assert data['fit']=='contain';assert data['natural']==[768,1024];assert not page.evaluate('document.documentElement.scrollWidth>innerWidth')
   value.screenshot(path=str(out/f'pdp-{family}-value-hero-{width}-final.png'));report.append({'family':family,'width':width,'passed':True,**data});print(json.dumps(report[-1]),flush=True)
  c.close()
 b.close()
(out/('pdp-value-hero-qa-'+'-'.join(families)+'.json')).write_text(json.dumps(report,indent=2)+'\n')
