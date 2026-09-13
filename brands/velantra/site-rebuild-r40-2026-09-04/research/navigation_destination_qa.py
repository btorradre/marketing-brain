from pathlib import Path
import json,re,traceback
from playwright.sync_api import sync_playwright
OUT=Path(__file__).resolve().parent
report={'as_of':'2026-09-05','theme_id':151337074753,'checks':[],'page_errors':[],'external_mutations':False,'forms_submitted':False}
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True)
  ctx=browser.new_context(viewport={'width':1440,'height':1000})
  page=ctx.new_page();page.on('pageerror',lambda e:report['page_errors'].append({'path':page.url.split('?')[0],'message':str(e)}))
  page.goto('https://velantrafashion.com/?preview_theme_id=151337074753',wait_until='domcontentloaded')
  for path in ['/collections/accessories','/pages/contact','/pages/track-your-order','/apps/parcel']:
   response=page.goto('https://velantrafashion.com'+path,wait_until='domcontentloaded');page.wait_for_timeout(1500 if path.startswith('/apps') else 250)
   main=page.locator('main');text=main.inner_text() if main.count() else page.locator('body').inner_text()
   result={'path':path,'status':response.status,'resolved_url':page.url,'title':page.title(),'main_text':text[:5000],'heading':page.locator('h1').all_text_contents(),'inputs':page.locator('main input, main textarea, #app input, #pp-container input').evaluate_all('els=>els.map(e=>({tag:e.tagName,type:e.type,name:e.name,placeholder:e.placeholder,required:e.required,visible:!!e.getClientRects().length}))'),'forms':page.locator('main form').evaluate_all('els=>els.map(e=>({action:e.getAttribute("action"),method:e.getAttribute("method")}))'),'main_links':main.locator('a').evaluate_all('els=>els.map(e=>({label:e.textContent.trim(),href:e.getAttribute("href")}))') if main.count() else [],'theme':page.evaluate('window.Shopify?.theme?.id'),'overflow':page.evaluate('document.documentElement.scrollWidth>innerWidth+1')}
   if path.startswith('/collections'):result['product_links']=page.locator('.product-card h3 a').evaluate_all('els=>els.map(e=>({title:e.textContent,href:e.getAttribute("href")}))')
   if path.startswith('/apps'):
    result['all_visible_inputs']=page.locator('input').evaluate_all('els=>els.filter(e=>!!e.getClientRects().length).map(e=>({type:e.type,name:e.name,placeholder:e.placeholder,required:e.required}))')
    result['frame_urls']=[f.url for f in page.frames]
    result['scripts']=page.locator('script[src]').evaluate_all('els=>els.map(e=>new URL(e.src).origin+new URL(e.src).pathname).filter(u=>/parcel|track/i.test(u))')
   screenshot='navigation-destination-'+path.rstrip('/').split('/')[-1]+'.png';page.screenshot(path=str(OUT/screenshot),full_page=False);result['screenshot']=screenshot
   report['checks'].append(result);print(json.dumps(result),flush=True)
  browser.close()
except Exception:report['failure']=traceback.format_exc();print(report['failure'],flush=True)
finally:(OUT/'navigation-destination-qa.json').write_text(json.dumps(report,indent=2)+'\n')
