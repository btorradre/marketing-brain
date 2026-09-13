from pathlib import Path
import asyncio,json
from playwright.async_api import async_playwright
P=Path(__file__).resolve().parents[1];OUT=P/'qa'
async def main():
 async with async_playwright() as pw:
  browser=await pw.chromium.launch();reports=[]
  for sex in ['women','men']:
   context=await browser.new_context(viewport={'width':1440,'height':1000},locale='en-US');page=await context.new_page()
   url=f'https://velantrafashion.com/products/velantra-weekender?view=wk-editorial-{sex}&preview_theme_id=151410507841'
   await page.goto(url,wait_until='domcontentloaded');await page.wait_for_selector('[data-initialized="true"]')
   try:await page.frame_locator('#PBarNextFrame').get_by_role('button',name='Hide bar',exact=True).click(timeout=2000)
   except Exception:pass
   for img in await page.locator('[data-wk-image]:not([hidden]) img').all():await img.scroll_into_view_if_needed()
   await page.locator('.wk-recommendations').scroll_into_view_if_needed();await page.wait_for_timeout(500)
   boxes=await page.locator('.wk-recommendation-card img').evaluate_all('(imgs)=>imgs.map(i=>({width:i.clientWidth,height:i.clientHeight,loaded:i.complete&&i.naturalWidth>0}))')
   assert all(abs(i['width']-i['height'])<=1 and i['loaded'] for i in boxes),boxes
   await page.screenshot(path=str(OUT/f'{sex}-recommendations-final.png'))
   links=set(await page.locator('.wk-header a,.wk-footer a,.wk-recommendation-card').evaluate_all('(links)=>links.map(a=>a.href)'))
   link_report=[]
   for link in links:
    r=await context.request.get(link);link_report.append({'url':link,'status':r.status});assert r.status<400,(link,r.status)
   await page.evaluate('scrollTo(0,0)');await page.wait_for_timeout(300)
   await page.screenshot(path=str(OUT/f'{sex}-desktop-final.png'));await page.screenshot(path=str(OUT/f'{sex}-full-final.png'),full_page=True)
   await page.set_viewport_size({'width':390,'height':844});await page.wait_for_timeout(300);await page.screenshot(path=str(OUT/f'{sex}-mobile-final.png'))
   report={'audience':sex,'recommendation_boxes':boxes,'links':link_report};reports.append(report)
   print(sex,'visual and link checks passed',flush=True);await context.close()
  await browser.close()
 (OUT/'final-visual-check.json').write_text(json.dumps(reports,indent=2))
asyncio.run(main())
