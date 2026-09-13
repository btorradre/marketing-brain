import json
from pathlib import Path
from playwright.sync_api import sync_playwright
out=Path(__file__).resolve().parent
report=[]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True)
 for width in [1440,390]:
  page=browser.new_page(viewport={'width':width,'height':1000})
  page.goto('https://velantrafashion.com/?preview_theme_id=151364960321',wait_until='domcontentloaded')
  page.locator('.craft-timeline').wait_for();page.evaluate('document.fonts.ready')
  page.locator('.craft-timeline').scroll_into_view_if_needed()
  page.wait_for_function('()=>Array.from(document.querySelectorAll(".craft-media img")).every(i=>i.complete&&i.naturalWidth>0)',timeout=60000)
  cards=page.locator('.craft-card').count();assert cards==4
  assert page.locator('h2',has_text='THE EVERYDAY COLLECTION').count()==0
  assert page.locator('h2',has_text='THE SIGNATURE COLLECTION').count()==1
  page.locator('.craft-timeline').screenshot(path=str(out/f'vivienne-leather-timeline-{width}.png'))
  geom=page.locator('.craft-strip').evaluate('(e)=>({width:e.clientWidth,scrollWidth:e.scrollWidth})')
  if width==390:
   assert geom['scrollWidth']>geom['width'];page.locator('.craft-strip').focus();page.locator('.craft-strip').press('End');page.wait_for_timeout(500);assert page.locator('.craft-strip').evaluate('(e)=>e.scrollLeft')>0
  page.locator('.value-breakdown').scroll_into_view_if_needed();page.locator('.value-breakdown').screenshot(path=str(out/f'vivienne-value-details-{width}.png'))
  assert page.locator('.value-breakdown tbody tr').count()==6
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  report.append({'width':width,'cards':cards,'timeline':geom,'one_signature_collection':True,'value_rows':6,'no_overflow':True})
  page.close()
 browser.close()
(out/'home-craft-layout-qa.json').write_text(json.dumps({'passed':True,'checks':report},indent=2)+'\n')
print(json.dumps(report))
