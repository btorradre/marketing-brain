from pathlib import Path
import asyncio,json
from playwright.async_api import async_playwright
P=Path(__file__).resolve().parents[1];OUT=P/'qa';OUT.mkdir(exist_ok=True)
COLORS=[('Cognac','44165996544065',10),('Army Green','44165996642369',10),('Espresso','44350589173825',10),('Black','44355431596097',10)]
async def main():
 async with async_playwright() as pw:
  browser=await pw.chromium.launch(headless=True)
  reports=[]
  for sex in ['women','men']:
   context=await browser.new_context(viewport={'width':1440,'height':1000},locale='en-US',timezone_id='America/Chicago')
   page=await context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
   url=f'https://velantrafashion.com/products/velantra-weekender?view=wk-editorial-{sex}&preview_theme_id=151410507841'
   await page.goto(url,wait_until='domcontentloaded',timeout=60000);await page.wait_for_selector('[data-initialized="true"]');await page.wait_for_timeout(1000)
   try:await page.frame_locator('#PBarNextFrame').get_by_role('button',name='Hide bar',exact=True).click(timeout=2000)
   except Exception:pass
   report={'audience':sex,'preview_url':url,'colors':[]}
   for color,id,count in COLORS:
    await page.locator(f'label[for="wk-color-{id}"]').click()
    assert await page.locator('[data-wk-variant-input]').input_value()==id
    assert await page.locator('[data-wk-color-name]').inner_text()==color
    images=page.locator('[data-wk-image]:not([hidden])')
    assert await images.count()==count,(sex,color,await images.count())
    assert await images.evaluate_all('(els)=>els.every(e=>e.dataset.color===els[0].dataset.color)')
    assert await page.locator('[data-wk-add]').is_enabled()
    if color=='Black':assert 'Pre-order' in await page.locator('[data-wk-add]').inner_text()
    await images.first.click();assert await page.locator('[data-wk-lightbox]').is_visible()
    await page.locator('[data-wk-lightbox-next]').click();await page.keyboard.press('Escape');assert not await page.locator('[data-wk-lightbox]').is_visible()
    report['colors'].append({'color':color,'variant':id,'photos':count,'cta':await page.locator('[data-wk-add]').inner_text()})
   selected=COLORS[0] if sex=='women' else COLORS[-1]
   await page.locator(f'label[for="wk-color-{selected[1]}"]').click()
   await page.locator('[data-wk-add]').click();await page.wait_for_selector('[data-wk-cart][open]')
   cart=await (await context.request.get('https://velantrafashion.com/cart.js?wk_editorial=qa')).json()
   assert cart['item_count']==1 and str(cart['items'][0]['variant_id'])==selected[1]
   report['cart']={'variant':selected[1],'quantity':cart['item_count'],'subtotal':cart['total_price']}
   await page.screenshot(path=str(OUT/f'{sex}-cart.png'))
   await page.locator('.wk-cart-item button').click();await page.wait_for_function('document.querySelector("[data-wk-checkout]").disabled')
   assert (await (await context.request.get('https://velantrafashion.com/cart.js?wk_editorial=qa')).json())['item_count']==0
   await page.locator('[data-wk-cart-close]').first.click()
   for i in range(await page.locator('.wk-accordions details').count()):
    detail=page.locator('.wk-accordions details').nth(i);await detail.locator('summary').click();assert await detail.get_attribute('open') is not None
   await page.get_by_role('link',name='Write a review',exact=True).click()
   assert await page.locator('#wk-review-form').get_attribute('open') is not None
   assert not await page.locator('#wk-review-contact').evaluate('(form)=>form.checkValidity()')
   assert not await page.locator('#wk-newsletter').evaluate('(form)=>form.checkValidity()')
   report['review_form_required_fields']=await page.locator('#wk-review-contact [required]').count()
   report['reviews_published']=await page.locator('.wk-review-list .wk-review').count()
   for i in range(await page.locator('.wk-accordions details[open]').count()):
    await page.locator('.wk-accordions details[open] summary').first.click()
   await page.locator('#wk-review-form>summary').click()
   await page.locator(f'label[for="wk-color-{COLORS[0][1]}"]').click()
   await page.evaluate('scrollTo(0,0)');await page.wait_for_timeout(500)
   await page.screenshot(path=str(OUT/f'{sex}-desktop-final.png'))
   for width,height in [(390,844),(375,812)]:
    await page.set_viewport_size({'width':width,'height':height});await page.evaluate('scrollTo(0,0)');await page.locator('[data-wk-gallery]').evaluate('(g)=>g.scrollLeft=0');await page.wait_for_timeout(300)
    assert not await page.evaluate('document.documentElement.scrollWidth>innerWidth')
    box=await page.locator('[data-wk-add]').bounding_box();report[f'mobile_{width}_cta']={'top':box['y'],'bottom':box['y']+box['height']}
    if width==390:await page.screenshot(path=str(OUT/f'{sex}-mobile-final.png'))
    await page.locator('[data-wk-next]').click();await page.wait_for_timeout(500);assert await page.locator('[data-wk-image-counter]').inner_text()=='2 / 10'
    await page.locator('#wk-reviews').scroll_into_view_if_needed();await page.wait_for_timeout(200);assert await page.locator('[data-wk-sticky]').is_visible()
   await page.set_viewport_size({'width':1440,'height':1000});await page.evaluate('scrollTo(0,0)')
   for img in await page.locator('[data-wk-image]:not([hidden]) img').all():await img.scroll_into_view_if_needed()
   await page.wait_for_timeout(500);report['broken_gallery_images']=await page.locator('[data-wk-image]:not([hidden]) img').evaluate_all('(imgs)=>imgs.filter(i=>!i.complete||!i.naturalWidth).map(i=>i.src)');assert not report['broken_gallery_images']
   await page.locator('.wk-recommendations').scroll_into_view_if_needed();await page.wait_for_timeout(500);await page.evaluate('scrollTo(0,0)');await page.wait_for_timeout(250);await page.screenshot(path=str(OUT/f'{sex}-full-final.png'),full_page=True)
   report['recommendations']=await page.locator('.wk-recommendation-card').count();assert report['recommendations']==4
   await page.locator(f'label[for="wk-color-{selected[1]}"]').click();await page.locator('[data-wk-add]').click();await page.wait_for_selector('[data-wk-cart][open]')
   await page.locator('[data-wk-checkout]').click();await page.wait_for_url('**/checkouts/**',timeout=45000);await page.wait_for_timeout(1000)
   text=await page.locator('body').inner_text();assert 'Eleanor' in text and selected[0] in text
   report['checkout']={'loaded':True,'matching_product':True,'matching_color':True,'order_placed':False}
   await page.screenshot(path=str(OUT/f'{sex}-checkout.png'));report['errors']=errors
   (OUT/f'{sex}-functional.json').write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True);reports.append(report)
   await context.close()
  await browser.close()
 (OUT/'functional-summary.json').write_text(json.dumps(reports,indent=2))
asyncio.run(main())
