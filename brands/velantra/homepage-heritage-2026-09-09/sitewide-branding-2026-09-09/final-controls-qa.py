import json
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
p=Path('/Users/brooksorradre2/Documents/marketing brain/brands/velantra/homepage-heritage-2026-09-09/sitewide-branding-2026-09-09');base='https://velantrafashion.com';result=[]
with sync_playwright() as pw:
 b=pw.chromium.launch()
 for width in [1440,390]:
  c=b.new_context(viewport={'width':width,'height':1000 if width>1000 else 844},reduced_motion='reduce');page=c.new_page();page.goto(base+'/collections/handbags?preview_theme_id=151519330369',wait_until='load')
  page.add_style_tag(content='#PBarNextFrame,#PBarNextFrameWrapper,#preview-bar-iframe{display:none!important}');page.locator('.collection-filter summary').first.click();expect(page.locator('.collection-filter__panel').first).to_be_visible();assert page.evaluate('document.documentElement.scrollWidth<=innerWidth');page.locator('.collection-filter__panel input[type=checkbox]').first.check();page.locator('.collection-filter__panel .button').first.click();page.wait_for_load_state('load');expect(page.locator('.collection-active-filters a').first).to_be_visible();page.locator('[name=sort_by]').select_option('price-ascending');page.wait_for_load_state('load');expect(page.locator('[name=sort_by]')).to_have_value('price-ascending')
  page.goto(base+'/products/velantra-vivienne?variant=44462686863425&preview_theme_id=151519330369',wait_until='load');page.locator('form[action*="/cart/add"] [name=add]').click();expect(page.locator('#CartPopup').get_by_role('spinbutton',name='Product quantity',exact=True)).to_have_value('1',timeout=20000)
  button=page.locator('#CartPopup .upcart-checkout-button');expect(button).to_have_css('font-size','11px');expect(button).to_have_css('font-weight','500');expect(button).to_have_css('background-color','rgb(19, 32, 57)');page.screenshot(path=str(p/f'qa/final-cart-{width}.png'),style='#PBarNextFrame,#preview-bar-iframe{display:none!important}')
  c.request.post(base+'/cart/clear.js');c.close();result.append({'width':width,'filter_apply':True,'sorting':True,'final_cart_typography':True,'isolated_cart_cleared':True});print('PASS final cart and collection controls',width,flush=True)
 b.close()
(p/'final-controls-qa.json').write_text(json.dumps(result,indent=2))
