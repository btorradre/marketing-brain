from pathlib import Path
from playwright.sync_api import sync_playwright
import json,traceback,re
ROOT=Path(__file__).resolve().parents[1]
rename={'Light Chocolate':'Cognac','Dark Chocolate':'Espresso'}
slugs={'Cognac':'cognac','Army Green':'army-green','Espresso':'espresso','Black':'black'}
catalog=json.loads((ROOT/'media/catalog-public.json').read_text())['products']
admin=json.loads((ROOT/'media/admin-image-alts.json').read_text())['data']['products']['nodes']
assets=json.loads((ROOT/'media/studio-image-map.json').read_text())['by_source_image_id']
report={'products':[],'page_errors':[],'snapshots_preserved':True,'cart_or_catalog_mutations':False}
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True)
  context=browser.new_context(viewport={'width':1440,'height':1080})
  page=context.new_page();page.on('pageerror',lambda e:report['page_errors'].append(str(e)))
  for handle in ['velantra-weekender','the-eleanor-weekender']:
   source=next(p for p in catalog if p['handle']==handle)
   source_media=next(p for p in admin if p['handle']==handle)['media']['nodes']
   shared=[m['id'].split('/')[-1] for m in source_media if '#color_' not in m['alt']]
   response=page.goto(f'https://velantrafashion.com/products/{handle}?preview_theme_id=151337074753',wait_until='domcontentloaded')
   page.wait_for_selector('[data-commerce-ready]');page.evaluate('document.fonts.ready')
   section=page.locator('[data-product-section]')
   section.locator('[data-color-option] label[title="Army Green"]').click()
   result={'handle':handle,'status':response.status,'theme':page.evaluate('window.Shopify.theme'),'h1':page.locator('h1').inner_text(),'option_labels':section.locator('[data-color-option] label').evaluate_all('(ls)=>ls.map(l=>l.title)'),'colors':[]}
   for variant in source['variants']:
    name=rename.get(variant['option1'],variant['option1']);slug=slugs[name]
    featured=next(m for m in source_media if m['image']['url'].split('?')[0]==variant['featured_image']['src'].split('?')[0])
    expected_media_id=featured['id'].split('/')[-1]
    expected_asset=assets[str(variant['featured_image']['id'])]['theme_asset']
    old_slug=variant['option1'].lower().replace(' ','-')
    expected_gallery=[m['id'].split('/')[-1] for m in source_media if '#color_'+old_slug in m['alt'] or '#color_' not in m['alt']]
    section.locator(f'[data-color-option] label[title="{name}"]').click()
    page.wait_for_function('(name)=>document.querySelector("[data-selected-option]").textContent===name',arg=name)
    selected_id=section.locator('[data-variant-select]').input_value()
    visible=section.locator('[data-media-id]:visible').evaluate_all('(ms)=>ms.map(m=>({id:m.dataset.mediaId,color:m.dataset.color,first:m.hasAttribute("data-first-visible"),src:m.querySelector("img")?.getAttribute("src")}))')
    first_image=section.locator('[data-first-visible] img');first_image.evaluate('(image)=>image.decode()')
    preorder=section.locator('[data-preorder-notice]')
    row={'name':name,'selected_variant_id':selected_id,'expected_variant_id':str(variant['id']),'first_media_id':visible[0]['id'],'expected_first_media_id':expected_media_id,'first_asset':visible[0]['src'],'expected_asset':expected_asset,'visible_media':visible,'expected_gallery_ids':expected_gallery,'shared_media_ids':shared,'first_image_decoded':first_image.evaluate('(i)=>i.complete&&i.naturalWidth>0'),'preorder_visible':preorder.is_visible(),'preorder_text':preorder.text_content().strip(),'button_label':section.locator('[data-add-button]').inner_text().strip(),'url':page.url}
    row['passed']=selected_id==str(variant['id']) and visible[0]['id']==expected_media_id and visible[0]['first'] and sum(m['first'] for m in visible)==1 and expected_asset in visible[0]['src'] and set(m['id'] for m in visible)==set(expected_gallery) and all(m['color'] in ['',slug] for m in visible) and row['first_image_decoded'] and row['preorder_visible']==(name=='Black') and (name!='Black' or ('September' in row['preorder_text'] and 'pre-order' in row['button_label'].lower())) and f'variant={variant["id"]}' in page.url
    result['colors'].append(row);print(json.dumps({'handle':handle,'color':name,'id':selected_id,'visible':len(visible),'passed':row['passed']}),flush=True)
    if name=='Espresso':
     page.locator('.site-header').scroll_into_view_if_needed();page.wait_for_function('scrollY===0')
     page.wait_for_function('!document.querySelector("[data-option-picker]").hidden && document.querySelector("[data-variant-fallback]").hidden')
     page.screenshot(path=str(ROOT/f'research/weekender-renamed-{handle}-espresso.png'),full_page=False)
   for accordion in section.locator('.product-accordion').filter(has=page.locator('summary',has_text='Care')).all():
    if accordion.get_attribute('open') is None:accordion.locator('summary').click()
   product_text=section.text_content()
   result['old_color_names_present']=re.findall(r'Light Chocolate|Dark Chocolate|light-chocolate|dark-chocolate',product_text,re.I)
   result['old_alt_names_present']=section.locator('img').evaluate_all('(images)=>images.map(i=>i.alt).filter(a=>/light chocolate|dark chocolate/i.test(a))')
   result['care_text']=section.locator('.product-accordion').filter(has=page.locator('summary',has_text='Care')).inner_text()
   result['horizontal_overflow']=page.evaluate('document.documentElement.scrollWidth>innerWidth+1')
   result['passed']=response.status==200 and result['h1']=='ELEANOR' and result['option_labels']==list(slugs.keys()) and all(c['passed'] for c in result['colors']) and not result['old_color_names_present'] and not result['old_alt_names_present'] and not result['horizontal_overflow'] and 'Cognac, Army Green, and Espresso' in result['care_text']
   report['products'].append(result)
  report['passed']=len(report['products'])==2 and all(p['passed'] for p in report['products']) and not report['page_errors']
  browser.close()
except Exception:
 report['failure']=traceback.format_exc();print(report['failure'],flush=True)
finally:
 (ROOT/'research/weekender-color-preview-qa.json').write_text(json.dumps(report,indent=2))
 print('Saved weekender-color-preview-qa.json; passed='+str(report.get('passed')),flush=True)
