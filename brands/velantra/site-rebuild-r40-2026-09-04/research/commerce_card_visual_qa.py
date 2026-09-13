from pathlib import Path
from playwright.sync_api import sync_playwright
import json, traceback
ROOT=Path(__file__).resolve().parents[1]
report={'viewports':[],'page_errors':[],'screenshots':[]}
URL='https://velantrafashion.com/collections/all?preview_theme_id=151337074753'
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True)
  context=browser.new_context(viewport={'width':1440,'height':1080})
  page=context.new_page()
  page.on('pageerror',lambda error:report['page_errors'].append(str(error)))
  response=page.goto(URL,wait_until='domcontentloaded')
  page.wait_for_selector('.product-card__heading')
  page.evaluate('document.fonts.ready')
  for width,height in [(1440,1080),(390,844),(320,844)]:
   page.set_viewport_size({'width':width,'height':height})
   images=page.locator('.product-card__media img')
   for i in range(images.count()):
    images.nth(i).scroll_into_view_if_needed();images.nth(i).evaluate('(image)=>image.decode()')
   metrics=page.locator('.product-card').evaluate_all('''cards=>cards.map(card=>{
    const title=card.querySelector('h3'),price=card.querySelector('.product-card__price'),row=card.querySelector('.product-card__heading');
    const r=row.getBoundingClientRect(),t=title.getBoundingClientRect(),p=price.getBoundingClientRect();
    return {title:title.textContent.trim(),price:price.textContent.trim(),titleFont:getComputedStyle(title).fontSize,priceFont:getComputedStyle(price).fontSize,gap:Math.round(p.left-t.right),titleFits:title.scrollWidth<=title.clientWidth+1,priceFits:price.scrollWidth<=price.clientWidth+1,rowFits:row.scrollWidth<=row.clientWidth+1,noOverlap:t.right<=p.left,priceWithinCard:p.right<=r.right+1,swatchLinks:[...card.querySelectorAll('.product-card__swatches a')].map(a=>a.getAttribute('href'))};
   })''')
   result={'width':width,'http_status':response.status,'heading_font':page.locator('h1').evaluate('h=>getComputedStyle(h).fontSize'),'cards':metrics,'horizontal_overflow':page.evaluate('document.documentElement.scrollWidth>innerWidth+1'),'broken_images':page.locator('.product-card__media img').evaluate_all('(images)=>images.filter(i=>!i.complete||i.naturalWidth===0).map(i=>i.src)')}
   result['passed']=len(metrics)==13 and result['heading_font']=='32px' and not result['horizontal_overflow'] and not result['broken_images'] and all(c['titleFits'] and c['priceFits'] and c['rowFits'] and c['noOverlap'] and c['priceWithinCard'] and c['gap']>=11 for c in metrics)
   report['viewports'].append(result)
   page.locator('.site-header').scroll_into_view_if_needed();page.wait_for_function('scrollY===0')
   frame=page.frame(name='PBarNextFrame')
   if frame:
    try:frame.get_by_role('button',name='Hide bar',exact=True).click(timeout=3000)
    except Exception:pass
   filename='commerce-final-collection.png' if width==1440 else f'commerce-final-collection-mobile-{width}.png'
   page.screenshot(path=str(ROOT/'research'/filename),full_page=False);report['screenshots'].append(filename)
   if width==390:
    juliette=page.locator('.product-card').filter(has=page.locator('h3',has_text='JULIETTE'))
    juliette.scroll_into_view_if_needed()
    filename='commerce-final-collection-juliette-mobile.png'
    page.screenshot(path=str(ROOT/'research'/filename),full_page=False);report['screenshots'].append(filename)
   print(json.dumps({'width':width,'passed':result['passed'],'overflow':result['horizontal_overflow'],'failed_cards':[c for c in metrics if not all(c[k] for k in ['titleFits','priceFits','rowFits','noOverlap','priceWithinCard'])]}),flush=True)
  report['passed']=all(v['passed'] for v in report['viewports']) and not report['page_errors']
  browser.close()
except Exception:
 report['failure']=traceback.format_exc();print(report['failure'],flush=True)
finally:
 (ROOT/'research/commerce-card-visual-qa.json').write_text(json.dumps(report,indent=2))
 print('Saved commerce-card-visual-qa.json; passed='+str(report.get('passed')),flush=True)
