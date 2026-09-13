from pathlib import Path
import asyncio,json
from playwright.async_api import async_playwright
P=Path(__file__).resolve().parents[1];OUT=P/'qa';OUT.mkdir(exist_ok=True)
async def main():
 async with async_playwright() as pw:
  browser=await pw.chromium.launch(headless=True)
  for sex in ['women','men']:
   context=await browser.new_context(viewport={'width':1440,'height':1000},locale='en-US',timezone_id='America/Chicago')
   page=await context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
   url=f'https://velantrafashion.com/products/velantra-weekender?view=wk-editorial-{sex}&preview_theme_id=151410507841'
   response=await page.goto(url,wait_until='domcontentloaded',timeout=60000)
   await page.wait_for_timeout(2500)
   (OUT/f'{sex}-initial.html').write_text(await page.content())
   (OUT/f'{sex}-initial.txt').write_text(await page.locator('body').inner_text())
   await page.screenshot(path=str(OUT/f'{sex}-desktop.png'),full_page=False)
   await page.screenshot(path=str(OUT/f'{sex}-full.png'),full_page=True)
   report={'url':page.url,'status':response.status,'errors':errors,'audience':await page.locator('[data-wk-product]').get_attribute('data-audience'),'initialized':await page.locator('[data-wk-product]').get_attribute('data-initialized'),'images':await page.locator('[data-wk-image]:visible').count(),'price':await page.locator('[data-wk-price]').inner_text(),'arrival':await page.locator('[data-wk-arrival]').inner_text(),'recommendations':await page.locator('.wk-recommendation-card').count()}
   await page.set_viewport_size({'width':390,'height':844});await page.wait_for_timeout(500);await page.screenshot(path=str(OUT/f'{sex}-mobile.png'),full_page=False)
   report['mobile_cta']=await page.locator('[data-wk-add]').bounding_box()
   report['overflow']=await page.evaluate('document.documentElement.scrollWidth > innerWidth')
   (OUT/f'{sex}-initial.json').write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True)
   await context.close()
  await browser.close()
asyncio.run(main())
