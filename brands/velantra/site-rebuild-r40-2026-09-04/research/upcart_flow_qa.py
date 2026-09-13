from pathlib import Path
from playwright.sync_api import sync_playwright
import json,time,re
out=Path('/Users/brooksorradre2/Documents/marketing brain/brands/velantra/site-rebuild-r40-2026-09-04/research')
report=json.loads((out/'upcart-flow-qa.json').read_text())
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True)
 for width in [390]:
  context=browser.new_context(viewport={'width':width,'height':1000});page=context.new_page();errors=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('https://velantrafashion.com/products/velantra-vivienne?preview_theme_id=151364960321',wait_until='domcontentloaded');page.wait_for_function("typeof window.upcartOpenCart==='function'");page.wait_for_timeout(800)
  if page.locator('#PBarNextFrame').count(): page.frame_locator('#PBarNextFrame').get_by_role('button',name='Hide bar',exact=True).evaluate('(e)=>e.click()')
  page.locator('[data-dialog-open="CartDrawer"]').first.click();page.wait_for_timeout(500)
  assert not page.locator('#CartDrawer').evaluate('(e)=>e.open'),'native drawer opened instead of UpCart'
  assert page.get_by_text('Your cart is empty',exact=True).is_visible()
  page.get_by_role('button',name='Close cart',exact=True).click();page.locator('[data-add-button]').click()
  page.get_by_role('spinbutton',name='Product quantity').wait_for();page.wait_for_timeout(900)
  assert page.get_by_role('spinbutton',name='Product quantity').input_value()=='1'
  assert not page.locator('#CartDrawer').evaluate('(e)=>e.open')
  page.get_by_role('button',name='Increase quantity',exact=True).click();page.wait_for_timeout(1200)
  assert page.get_by_role('spinbutton',name='Product quantity').input_value()=='2'
  assert page.locator('[data-cart-count]').first.inner_text()=='2'
  page.get_by_role('button',name='Decrease quantity',exact=True).click();page.wait_for_timeout(1200)
  assert page.get_by_role('spinbutton',name='Product quantity').input_value()=='1'
  upsell=page.locator('.slide.selected .upcart-upsells-button').first;upsell.click();page.wait_for_timeout(1500)
  assert page.get_by_role('spinbutton',name='Product quantity').count()==2
  assert page.locator('[data-cart-count]').first.inner_text()=='2'
  page.screenshot(path=str(out/f'upcart-flow-{width}.png'))
  page.locator("[class*='TrashButton__deleteButton']").first.click();page.wait_for_timeout(1200)
  assert page.get_by_role('spinbutton',name='Product quantity').count()==1
  assert page.locator('[data-cart-count]').first.inner_text()=='1'
  page.get_by_role('button',name='Close cart',exact=True).click();page.locator('[data-dialog-open="CartDrawer"]').first.click();page.wait_for_timeout(500)
  assert not page.locator('#CartDrawer').evaluate('(e)=>e.open')
  checkout=page.locator('.upcart-checkout-button');checkout.scroll_into_view_if_needed();checkout.click();page.wait_for_timeout(4500)
  assert '/checkouts/' in page.url, 'Checkout failed: '+page.url.split('?')[0]
  page.wait_for_timeout(4000)
  if width<768: page.get_by_role('button',name=re.compile('Order summary')).first.click();page.wait_for_timeout(500)
  page.screenshot(path=str(out/f'upcart-checkout-{width}.png'));(out/f'upcart-checkout-{width}.txt').write_text(page.inner_text('body'));assert 'Vivienne' in page.inner_text('body'), page.inner_text('body')[:2500]
  row={'width':width,'header_opens_upcart':True,'single_add':True,'quantity_increase_decrease':True,'upsell_add_remove':True,'badge_sync':True,'one_drawer':True,'shopify_checkout':True,'checkout_path':page.url.split('?')[0],'errors':errors,'no_order_placed':True}
  report.append(row);(out/'upcart-flow-qa.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(row));context.close()
 browser.close()
