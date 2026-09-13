from pathlib import Path
from playwright.sync_api import sync_playwright
import json,re,traceback
ROOT=Path(__file__).resolve().parents[1]
catalog=json.loads((ROOT/'media/catalog-public.json').read_text())['products']
expected_titles={'velantra-vivienne':'VIVIENNE','velantra-juliette':'JULIETTE','velantra-delphine':'DELPHINE','the-colette-wool-tote':'COLETTE','velantra-weekender':'ELEANOR','the-eleanor-weekender':'ELEANOR','velantra-margot-tote':'MERIDIAN','velantra-boat-tote-2':'CAMILLE'}
report={'products':[],'page_errors':[],'screenshots':[]}
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True)
  context=browser.new_context(viewport={'width':1440,'height':1080})
  page=context.new_page()
  page.on('pageerror',lambda error:report['page_errors'].append({'url':page.url,'error':str(error)}))
  for product in catalog:
   handle=product['handle']
   response=page.goto(f'https://velantrafashion.com/products/{handle}?preview_theme_id=151337074753',wait_until='domcontentloaded')
   page.wait_for_selector('[data-commerce-ready]')
   page.evaluate('document.fonts.ready')
   html=page.content()
   media=page.locator('[data-media-id] img').evaluate_all('(images)=>images.map(i=>({id:i.closest("[data-media-id]").dataset.mediaId,src:i.getAttribute("src")}))')
   result={'handle':handle,'http_status':response.status,'h1':page.locator('h1').inner_text(),'expected_h1':expected_titles.get(handle,product['title']),'media_count':len(media),'expected_media_count':len(product['images']),'unmapped_media':[i for i in media if '/assets/r40-' not in i['src'] or '-white-studio.webp' not in i['src']],'liquid_errors':re.findall(r'Liquid (?:error|syntax error)[^<\n]*',html),'missing_translations':re.findall(r'Translation missing[^<\n]*',html,re.I),'broken_images':[],'lazy_loaded_ids':[]}
   loaded=set()
   labels=page.locator('[data-color-option] label').evaluate_all('(nodes)=>nodes.map(l=>l.title)') or [None]
   for label in labels:
    if label is not None:page.locator('[data-color-option] label[title="'+label.replace('"','\\"')+'"]').click()
    images=page.locator('[data-media-id]:visible img')
    for index in range(images.count()):
     image=images.nth(index)
     media_id=image.locator('xpath=..').locator('xpath=..').get_attribute('data-media-id')
     if media_id in loaded:continue
     image.scroll_into_view_if_needed()
     try:image.evaluate('(image)=>image.decode()')
     except Exception as error:result['broken_images'].append({'media_id':media_id,'src':image.get_attribute('src'),'error':str(error)[:200]})
     metrics=image.evaluate('(i)=>({complete:i.complete,width:i.naturalWidth,height:i.naturalHeight})')
     if not metrics['complete'] or metrics['width']==0:result['broken_images'].append({'media_id':media_id,'src':image.get_attribute('src'),'metrics':metrics})
     loaded.add(media_id)
   result['lazy_loaded_ids']=sorted(loaded)
   result['all_gallery_images_loaded']=len(loaded)==len(media)
   result['horizontal_overflow']=page.evaluate('document.documentElement.scrollWidth>innerWidth+1')
   result['passed']=response.status==200 and result['h1']==result['expected_h1'] and len(media)==result['expected_media_count'] and not any(result[k] for k in ['unmapped_media','liquid_errors','missing_translations','broken_images','horizontal_overflow']) and result['all_gallery_images_loaded']
   report['products'].append(result)
   print(json.dumps({k:v for k,v in result.items() if k!='lazy_loaded_ids'}),flush=True)
  page.goto('https://velantrafashion.com/products/velantra-vivienne?preview_theme_id=151337074753',wait_until='domcontentloaded')
  page.wait_for_selector('[data-commerce-ready]');page.evaluate('document.fonts.ready');page.locator('[data-first-visible] img').evaluate('(image)=>image.decode()')
  frame=page.frame(name='PBarNextFrame')
  if frame:
   try:frame.get_by_role('button',name='Hide bar',exact=True).click(timeout=5000)
   except Exception:pass
  page.screenshot(path=str(ROOT/'research/commerce-final-vivienne-desktop.png'),full_page=False);report['screenshots'].append('commerce-final-vivienne-desktop.png')
  page.set_viewport_size({'width':390,'height':844});page.locator('[data-first-visible] img').scroll_into_view_if_needed();page.keyboard.press('Control+Home')
  page.screenshot(path=str(ROOT/'research/commerce-final-vivienne-mobile.png'),full_page=False);report['screenshots'].append('commerce-final-vivienne-mobile.png')
  report['mobile_overflow']=page.evaluate('document.documentElement.scrollWidth>innerWidth+1')
  page.set_viewport_size({'width':1440,'height':1080});page.goto('https://velantrafashion.com/collections/all?preview_theme_id=151337074753',wait_until='domcontentloaded');page.evaluate('document.fonts.ready')
  images=page.locator('.product-card__media img')
  for index in range(images.count()):
   images.nth(index).scroll_into_view_if_needed();images.nth(index).evaluate('(image)=>image.decode()')
  report['collection']={'cards':page.locator('.product-card').count(),'broken_images':page.locator('.product-card img').evaluate_all('(images)=>images.filter(i=>i.complete&&i.naturalWidth===0).map(i=>i.src)'),'unmapped_images':page.locator('.product-card__media img').evaluate_all('(images)=>images.filter(i=>!i.src.includes("/assets/r40-")).map(i=>i.src)'),'horizontal_overflow':page.evaluate('document.documentElement.scrollWidth>innerWidth+1')}
  page.locator('.site-header').scroll_into_view_if_needed();page.wait_for_function('scrollY===0');page.screenshot(path=str(ROOT/'research/commerce-final-collection.png'),full_page=False);report['screenshots'].append('commerce-final-collection.png')
  report['passed']=all(x['passed'] for x in report['products']) and len(report['products'])==13 and not report['page_errors'] and not report['mobile_overflow'] and not report['collection']['broken_images'] and not report['collection']['unmapped_images'] and not report['collection']['horizontal_overflow']
  browser.close()
except Exception:
 report['failure']=traceback.format_exc();print(report['failure'],flush=True)
finally:
 (ROOT/'research/commerce-final-catalog-smoke.json').write_text(json.dumps(report,indent=2));print('Saved commerce-final-catalog-smoke.json; passed='+str(report.get('passed')),flush=True)
