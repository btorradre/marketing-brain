import asyncio,json,re,os
from pathlib import Path
from playwright.async_api import async_playwright,expect
ROOT=Path(__file__).resolve().parent;BASE='https://velantrafashion.com';T='151519330369';HIDE='#PBarNextFrame,#preview-bar-iframe{display:none!important}'
products=[x for x in json.loads((ROOT/'products.json').read_text()) if x['published_at']]
report={'pages':[],'variants':[],'failures':[]};lock=asyncio.Semaphore(2)
async def check(browser,path,width,product=None):
 async with lock:
  context=await browser.new_context(viewport={'width':width,'height':1000 if width>1000 else 844},reduced_motion='reduce');page=await context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  name=(product['handle'] if product else path.strip('/').replace('/','-').split('?')[0] or 'home')
  try:
   if path=='/apps/parcel':await page.goto(BASE+'/?preview_theme_id='+T,wait_until='load',timeout=60000)
   response=await page.goto(BASE+path+('&' if '?' in path else '?')+'preview_theme_id='+T,wait_until='load',timeout=60000)
   await expect(page.locator('body')).to_have_class(re.compile('heritage-site'))
   await expect(page.locator('.heritage-service')).to_be_visible()
   await expect(page.locator('main h1')).to_have_count(1)
   await page.evaluate('document.fonts.ready')
   styles=await page.evaluate('''()=>{const s=q=>{let x=getComputedStyle(document.querySelector(q));return {bg:x.backgroundColor,color:x.color,font:x.fontFamily}};return {body:s('body'),header:s('.site-header'),footer:s('.site-footer'),h1:s('main h1')}}''')
   assert styles['body']['bg']=='rgb(247, 245, 239)',styles
   assert styles['header']['color']=='rgb(19, 32, 57)',styles
   assert styles['footer']['bg']=='rgb(19, 32, 57)',styles
   assert await page.evaluate('document.documentElement.scrollWidth<=innerWidth'), 'horizontal overflow'
   await page.screenshot(path=str(ROOT/f'qa/{name}-{width}.png'),style=HIDE)
   if product:
    quantity=page.locator('[data-product-quantity] input');await expect(quantity).to_have_value('1')
    await page.locator('.product-buybox').screenshot(path=str(ROOT/f'qa/{name}-buybox-{width}.png'),style=HIDE)
    if width==390:
     labels=page.locator('fieldset[data-color-option] label')
     for i in range(await labels.count()):
      label=labels.nth(i);color=await label.get_attribute('title');await label.click()
      await expect(page.locator('fieldset[data-color-option] input:checked')).to_have_value(color)
      selected=await page.locator('form[action*="/cart/add"] [name=id]').input_value();variant=next(v for v in product['variants'] if str(v['id'])==selected);assert variant['option1']==color
      visible=page.locator('[data-gallery] [data-media-id]:not([hidden])');assert await visible.count()>0
      if product['handle'] in ['velantra-horse-charm','velantra-cherry-charm','bag-scarf','boat-tote-keychain']:
       await expect(page.locator('[data-gallery]')).to_have_attribute('data-color-only','true')
       colors=await visible.evaluate_all('(els)=>els.map(e=>e.dataset.color)');assert len(set(colors))==1 and colors[0]
      img=visible.locator('img').first;await img.scroll_into_view_if_needed();await page.wait_for_function('(img)=>img.complete && img.naturalWidth>0',arg=await img.element_handle())
      report['variants'].append({'handle':name,'color':color,'variant':selected,'visible_images':await visible.count()})
    for section in ['.craft-intro','.value-breakdown__content','.product-recommendations','.client-perspectives']:
     loc=page.locator(section)
     if await loc.count() and await loc.is_visible() and name=='velantra-vivienne':
      await loc.scroll_into_view_if_needed();await loc.screenshot(path=str(ROOT/f'qa/vivienne-{section[1:]}-{width}.png'),style=HIDE)
   if path=='/apps/parcel':
    await expect(page.locator('#pp-tracking-page-app input:visible').first).to_be_visible()
    await expect(page.locator('#pp-tracking-page-app h1')).to_have_css('color','rgb(19, 32, 57)')
    if width==390:
     await page.get_by_role('tab',name='Tracking Number',exact=True).click();await expect(page.locator('#pp-tracking-page-app input[name=nums]:visible')).to_be_visible()
   assert not errors,errors
   report['pages'].append({'path':path,'width':width,'status':response.status,'styles':styles,'no_overflow':True,'one_h1':True,'page_errors':errors})
   print('PASS',name,width,flush=True)
  except Exception as e:
   report['failures'].append({'path':path,'width':width,'error':str(e)});print('FAIL',name,width,str(e)[:220],flush=True)
   await page.screenshot(path=str(ROOT/f'qa/FAIL-{name}-{width}.png'),style=HIDE)
  finally:await context.close();(ROOT/('browser-recheck.json' if os.getenv('HERITAGE_RECHECK') else 'browser-qa.json')).write_text(json.dumps(report,indent=2))
async def main():
 async with async_playwright() as pw:
  browser=await pw.chromium.launch()
  routes=['/','/collections/handbags','/collections/accessories','/collections/all','/collections','/search?q=Vivienne','/search?q=zznonexistentzz','/pages/contact','/apps/parcel','/policies/shipping-policy','/policies/refund-policy','/policies/privacy-policy','/policies/terms-of-service','/cart','/heritage-missing-page']
  if os.getenv('HERITAGE_RECHECK'):
   global products
   products=[p for p in products if p['handle']=='velantra-vivienne']
   routes=['/apps/parcel','/collections','/collections/handbags','/','/pages/contact']
  tasks=[check(browser,'/products/'+p['handle'],w,p) for p in products for w in [1440,390]]+[check(browser,r,w) for r in routes for w in [1440,390]]+[check(browser,'/products/velantra-vivienne',w,next(p for p in products if p['handle']=='velantra-vivienne')) for w in [768,320]]
  await asyncio.gather(*tasks);await browser.close()
 print('RESULT',len(report['pages']),'pages',len(report['variants']),'colors',len(report['failures']),'failures')
asyncio.run(main())
