from pathlib import Path
from playwright.sync_api import sync_playwright
import json
out=Path('/Users/brooksorradre2/Documents/marketing brain/brands/velantra/site-rebuild-r40-2026-09-04/research')
with sync_playwright() as p:
 b=p.chromium.launch(headless=True);page=b.new_page(viewport={'width':1440,'height':1000});page.goto('https://velantrafashion.com/products/velantra-vivienne?preview_theme_id=151364960321',wait_until='domcontentloaded');page.wait_for_timeout(1800)
 if page.locator('#PBarNextFrame').count():page.frame_locator('#PBarNextFrame').get_by_role('button',name='Hide bar',exact=True).evaluate('(e)=>e.click()')
 page.locator('[data-add-button]').click();page.wait_for_function("()=>Array.from(window.upcartDocumentOrShadowRoot.querySelectorAll('img')).length>1 && Array.from(window.upcartDocumentOrShadowRoot.querySelectorAll('img')).every(i=>i.complete&&i.naturalWidth>0)",timeout=45000)
 images=page.evaluate('''()=>[...window.upcartDocumentOrShadowRoot.querySelectorAll('img')].map(i=>({src:i.src,loaded:i.complete&&i.naturalWidth>0}))''')
 assert images and all('white-studio.webp' in i['src'] and i['loaded'] for i in images),images
 card=page.locator('.slide.selected .upcart-upsell-item-card').first
 selector=card.locator('select');options=selector.locator('option').count();selected=selector.input_value()
 if options>1:selector.select_option(index=1 if selector.locator('option').first.get_attribute('value')==selected else 0)
 page.wait_for_timeout(400);variant=selector.input_value();src=card.locator('img').get_attribute('src');assert 'white-studio.webp' in src
 card.locator('.upcart-upsells-button').click();page.wait_for_timeout(1300);assert page.get_by_role('spinbutton',name='Product quantity').count()==2
 page.get_by_role('button',name='Increase quantity',exact=True).first.click();page.wait_for_timeout(900);assert page.locator('[data-cart-count]').first.inner_text()=='3'
 assert not page.locator('#CartDrawer').evaluate('(e)=>e.open')
 page.screenshot(path=str(out/'upcart-white-studio.png'))
 d={'passed':True,'all_rendered_product_images_are_studio':True,'rendered_image_count':len(images),'upsell_variant_selection':variant,'variant_specific_image':src,'upsell_add':True,'quantity_update':True,'header_count':3,'native_cart_unchanged':True};(out/'upcart-studio-image-qa.json').write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(d));b.close()
