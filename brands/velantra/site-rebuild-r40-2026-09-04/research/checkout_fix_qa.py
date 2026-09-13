from pathlib import Path
import json, traceback
from playwright.sync_api import sync_playwright
OUT=Path(__file__).parent
previous=json.loads((OUT/'checkout-fix-qa.json').read_text())
report={'checks':[x for x in previous.get('checks',[]) if x['name'] in ['pending_quantity_checkout_guard','native_checkout_drawer']],'errors':[]}
def note(name,**details):
 report['checks'].append(dict(name=name,**details)); print(json.dumps(report['checks'][-1]),flush=True)
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True)
  for mode in ['cart_page']:
   ctx=browser.new_context(viewport={'width':390 if mode=='drawer' else 1440,'height':900})
   page=ctx.new_page()
   page.on('pageerror',lambda e: report['errors'].append(str(e)))
   page.goto('https://velantrafashion.com/products/velantra-vivienne?preview_theme_id=151337074753',wait_until='domcontentloaded')
   page.wait_for_selector('[data-product-section][data-commerce-ready="true"]')
   page.locator('[data-add-button]').click()
   page.locator('#CartDrawer .drawer-line').wait_for()
   checkout=page.locator('#CartDrawer button[name=checkout]')
   checkout.wait_for(state='visible')
   page.wait_for_function('!document.querySelector("[data-cart-checkout]").disabled')
   if mode=='drawer':
    pending=[]
    def delay_change(route):
     route.continue_()
    page.on('request',lambda r: pending.append(page.locator('[data-cart-checkout]').is_disabled()) if r.url.endswith('/cart/change.js') else None)
    page.locator('#CartDrawer').get_by_role('button',name='Increase quantity',exact=True).click()
    page.wait_for_function('document.querySelector("[data-drawer-total]").textContent.includes("299.98")&&!document.querySelector("[data-cart-checkout]").disabled')
    assert pending==[True],pending
    note('pending_quantity_checkout_guard',disabled_during_request=True,total=page.locator('[data-drawer-total]').inner_text())
   else:
    page.locator('#CartDrawer').get_by_role('link',name='View your selection',exact=True).click()
    page.wait_for_load_state('domcontentloaded')
    print('CART PAGE',page.url,page.locator('main').inner_text()[:1200],flush=True)
    page.screenshot(path=str(OUT/'cart-page-checkout-inspect.png'))
    page.locator('input[name="updates[]"]').fill('2')
    checkout=page.locator('.cart-page button[name=checkout]')
   nav=[]
   page.on('request',lambda r:nav.append({'method':r.method,'is_cart':r.url.split('?')[0].endswith('/cart'),'body':r.post_data}) if r.is_navigation_request() and r.method=='POST' else None)
   checkout.click()
   page.wait_for_url('**/checkouts/**',wait_until='domcontentloaded',timeout=60000)
   page.get_by_role('heading',name='Contact',exact=True).wait_for()
   assert nav and nav[0]['is_cart'] and 'checkout=checkout' in nav[0]['body'],nav
   assert '$299.98' in page.locator('body').inner_text()
   page.screenshot(path=str(OUT/f'checkout-fixed-{mode}.png'),full_page=False)
   note('native_checkout_'+mode,shopify_checkout=True,contact_step_visible=True,cart_total='$299.98',post_to_cart=True)
   ctx.close()
  browser.close()
except Exception:
 report['failure']=traceback.format_exc();print(report['failure'],flush=True)
 print('FAILED PAGE',page.url,page.locator('main').inner_text()[:1500],flush=True)
 print('DRAWER',page.locator('#CartDrawer').inner_text(),flush=True)
finally:
 (OUT/'checkout-fix-qa.json').write_text(json.dumps(report,indent=2))
