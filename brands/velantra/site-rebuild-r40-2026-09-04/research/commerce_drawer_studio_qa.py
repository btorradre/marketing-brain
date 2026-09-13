from pathlib import Path
from playwright.sync_api import sync_playwright
import json,traceback
ROOT=Path(__file__).resolve().parents[1]
report={'page_errors':[]}
try:
 with sync_playwright() as p:
  b=p.chromium.launch(headless=True)
  context=b.new_context(viewport={'width':1440,'height':1080})
  page=context.new_page()
  page.on('pageerror',lambda error:report['page_errors'].append(str(error)))
  page.goto('https://velantrafashion.com/products/velantra-vivienne?preview_theme_id=151337074753',wait_until='domcontentloaded')
  page.wait_for_selector('[data-commerce-ready]');page.evaluate('document.fonts.ready')
  page.locator('[data-option-picker] label[title="Cognac"]').click()
  report['selected_variant']=page.locator('[data-variant-select]').input_value()
  page.locator('[data-add-button]').click()
  page.wait_for_selector('#CartDrawer[open] .drawer-line img')
  image=page.locator('#CartDrawer .drawer-line img')
  image.evaluate('(image)=>image.decode()')
  report['image']=image.get_attribute('src')
  report['image_loaded']=image.evaluate('i=>i.complete&&i.naturalWidth>0')
  report['drawer_text']=page.locator('#CartDrawer').inner_text()
  report['studio_url']='/assets/r40-' in report['image'] and '-white-studio.webp' in report['image']
  frame=page.frame(name='PBarNextFrame')
  if frame:
   try:frame.get_by_role('button',name='Hide bar',exact=True).click(timeout=3000)
   except Exception:pass
  page.screenshot(path=str(ROOT/'research/commerce-final-cart-drawer.png'),full_page=False)
  page.locator('#CartDrawer').get_by_role('button',name='Remove',exact=True).click()
  page.wait_for_function('document.querySelectorAll("#CartDrawer .drawer-line").length===0')
  report['final_cart_item_count']=page.evaluate('async()=>{const r=await fetch(window.Shopify.routes.root+"cart.js");return(await r.json()).item_count}')
  report['passed']=report['studio_url'] and report['image_loaded'] and 'Cognac' in report['drawer_text'] and 'October' in report['drawer_text'] and report['final_cart_item_count']==0 and not report['page_errors']
  b.close()
except Exception:
 report['failure']=traceback.format_exc()
finally:
 (ROOT/'research/commerce-drawer-studio-qa.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
