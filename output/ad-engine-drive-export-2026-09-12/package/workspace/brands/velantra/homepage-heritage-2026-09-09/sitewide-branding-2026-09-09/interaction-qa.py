import json
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parent;BASE='https://velantrafashion.com';T='151519330369';HIDE='#PBarNextFrame,#preview-bar-iframe{display:none!important}';report=[]
with sync_playwright() as pw:
 browser=pw.chromium.launch()
 for width in [1440,390]:
  c=browser.new_context(viewport={'width':width,'height':1000 if width>1000 else 844},reduced_motion='reduce');page=c.new_page();page.goto(BASE+'/?preview_theme_id='+T,wait_until='load')
  if width>1100:
   page.locator('[data-dialog-open="SearchDialog"]').click();expect(page.locator('#SearchDialog')).to_be_visible();page.locator('#HeaderSearch').fill('Vivienne');page.locator('#SearchDialog [data-dialog-close]').click();expect(page.locator('#SearchDialog')).not_to_be_visible()
  else:
   page.locator('.mobile-menu').click();expect(page.locator('#NavigationDrawer')).to_be_visible();page.locator('#NavigationDrawer').screenshot(path=str(ROOT/f'qa/navigation-{width}.png'),style=HIDE);page.locator('#NavigationDrawer [data-dialog-close]').click()
  page.goto(BASE+'/products/velantra-vivienne?preview_theme_id='+T,wait_until='load');q=page.locator('[data-product-quantity] input');page.locator('[data-product-quantity] button').nth(1).click();expect(q).to_have_value('2')
  page.locator('fieldset[data-color-option] label[title="Cognac"]').click();expect(q).to_have_value('2');variant=page.locator('form[action*="/cart/add"] [name=id]').input_value()
  with page.expect_response(lambda r:'/cart/add' in r.url and r.request.method=='POST') as response:page.locator('form[action*="/cart/add"] [name=add]').click()
  assert response.value.ok;cart=c.request.get(BASE+'/cart.js').json();assert any(str(i['variant_id'])==variant and i['quantity']==2 for i in cart['items'])
  expect(page.locator('#CartPopup')).to_be_in_viewport(timeout=15000);expect(page.locator('#CartPopup').get_by_role('spinbutton',name='Product quantity',exact=True)).to_have_value('2',timeout=20000);expect(page.locator('#CartPopup .upcart-checkout-button')).to_be_visible();expect(page.locator('#CartPopup')).to_have_css('background-color','rgb(247, 245, 239)');page.screenshot(path=str(ROOT/f'qa/cart-populated-{width}.png'),style=HIDE)
  (ROOT/f'upcart-populated-{width}.html').write_text(page.locator('#CartPopup').evaluate('(e)=>e.getRootNode().innerHTML'))
  page.get_by_role('button',name='Close cart',exact=True).click();expect(page.locator('#CartPopup')).not_to_be_in_viewport()
  page.goto(BASE+'/cart?preview_theme_id='+T,wait_until='load');expect(page.locator('.cart-line')).to_have_count(1);page.screenshot(path=str(ROOT/f'qa/cart-page-populated-{width}.png'),full_page=True,style=HIDE)
  page.locator('.cart-line__quantity input').fill('3');page.locator('button[name=update]').click();page.wait_for_load_state('load');expect(page.locator('.cart-line__quantity input')).to_have_value('3');cart=c.request.get(BASE+'/cart.js').json();assert cart['items'][0]['quantity']==3
  c.request.post(BASE+'/cart/clear.js');page.goto(BASE+'/?preview_theme_id='+T,wait_until='load');page.locator('header [data-dialog-open="CartDrawer"]').click();expect(page.get_by_text('Your cart is empty',exact=True)).to_be_in_viewport();page.screenshot(path=str(ROOT/f'qa/cart-empty-{width}.png'),style=HIDE)
  report.append({'width':width,'menu_search':True,'add_quantity':2,'variant':variant,'quantity_preserved_on_color_change':True,'cart_update_quantity':3,'cart_theme_verified':True,'cart_cleared':True});(ROOT/'interaction-qa.json').write_text(json.dumps(report,indent=2));c.close();print('PASS purchase flow',width,flush=True)
 browser.close()
