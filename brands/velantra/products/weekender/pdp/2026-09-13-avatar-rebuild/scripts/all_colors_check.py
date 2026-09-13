from pathlib import Path
import asyncio,json
from playwright.async_api import async_playwright
P=Path(__file__).resolve().parents[1];OUT=P/'qa/all-colors';OUT.mkdir(exist_ok=True)
COLORS=[('Cognac','44165996544065'),('Army Green','44165996642369'),('Espresso','44350589173825'),('Black','44355431596097')]
async def main():
 async with async_playwright() as pw:
  browser=await pw.chromium.launch();reports=[]
  for sex in ['women','men']:
   context=await browser.new_context(viewport={'width':1440,'height':1000},locale='en-US')
   page=await context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
   await page.goto(f'https://velantrafashion.com/products/velantra-weekender?view=wk-editorial-{sex}&preview_theme_id=151410507841',wait_until='domcontentloaded',timeout=60000)
   await page.wait_for_selector('[data-initialized="true"]')
   try:await page.frame_locator('#PBarNextFrame').get_by_role('button',name='Hide bar',exact=True).click(timeout=2000)
   except Exception:pass
   for color,variant in COLORS:
    await page.set_viewport_size({'width':1440,'height':1000})
    await page.locator(f'label[for="wk-color-{variant}"]').click()
    assert await page.locator('[data-wk-variant-input]').input_value()==variant
    assert await page.locator('[data-wk-color-name]').inner_text()==color
    items=page.locator('[data-wk-image]:not([hidden])');assert await items.count()==10
    assert await items.evaluate_all('(els,color)=>els.every(e=>e.dataset.color===color)',color)
    for img in await items.locator('img').all():
     await img.scroll_into_view_if_needed();await img.evaluate('(i)=>i.decode()')
    urls=await items.locator('img').evaluate_all('(els)=>els.map(i=>i.src)');assert len(set(urls))==10
    await items.first.click();assert await page.locator('[data-wk-lightbox]').is_visible()
    lightbox=page.locator('[data-wk-lightbox] img')
    for index,url in enumerate(urls):
     assert await lightbox.get_attribute('src')==url,(sex,color,index)
     await lightbox.evaluate('(i)=>i.decode()')
     await page.locator('[data-wk-lightbox-next]').click()
    assert await lightbox.get_attribute('src')==urls[0]
    await page.keyboard.press('Escape')
    await page.evaluate('scrollTo(0,0)');await page.wait_for_timeout(250)
    stem=f'{sex}-{color.lower().replace(" ","-")}'
    await page.screenshot(path=str(OUT/f'{stem}-desktop.png'))
    await page.screenshot(path=str(OUT/f'{stem}-full.png'),full_page=True)
    await page.set_viewport_size({'width':390,'height':844});await page.evaluate('scrollTo(0,0)')
    await page.locator('[data-wk-gallery]').evaluate('(g)=>g.scrollLeft=0');await page.wait_for_timeout(300)
    assert not await page.evaluate('document.documentElement.scrollWidth>innerWidth')
    await page.screenshot(path=str(OUT/f'{stem}-mobile.png'))
    for index in range(1,10):
     await page.locator('[data-wk-next]').click();await page.wait_for_timeout(400)
     assert await page.locator('[data-wk-image-counter]').inner_text()==f'{index+1} / 10'
    report={'audience':sex,'color':color,'variant':variant,'photos':10,'all_images_loaded':True,'lightbox_all_ten':True,'mobile_all_ten':True,'no_horizontal_overflow':True,'urls':urls}
    reports.append(report);print(sex,color,'passed',flush=True)
   assert not errors,errors
   await context.close()
  await browser.close()
 (OUT/'results.json').write_text(json.dumps(reports,indent=2))
asyncio.run(main())
