from pathlib import Path
from playwright.sync_api import sync_playwright
import json,traceback,re
ROOT=Path(__file__).resolve().parents[1]
catalog=json.loads((ROOT/'media/catalog-public.json').read_text())['products']
rename={'Light Chocolate':'Cognac','Dark Chocolate':'Espresso'}
report={'products':[],'page_errors':[],'context':'Fresh browser context without preview cookies','cart_or_catalog_mutations':False}
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True);context=browser.new_context(viewport={'width':1440,'height':1080})
  report['initial_cookie_count']=len(context.cookies())
  page=context.new_page();page.on('pageerror',lambda e:report['page_errors'].append({'url':page.url,'error':str(e)}))
  for handle in ['velantra-weekender','the-eleanor-weekender']:
   source=next(p for p in catalog if p['handle']==handle)
   response=page.goto(f'https://velantrafashion.com/products/{handle}',wait_until='domcontentloaded')
   page.wait_for_selector('input[data-variant-input][value="Cognac"]',state='attached')
   result={'handle':handle,'status':response.status,'theme':page.evaluate('window.Shopify.theme'),'labels':page.locator('input[data-variant-input]').evaluate_all('(els)=>els.map(e=>e.value)'),'colors':[]}
   for source_variant in source['variants']:
    name=rename.get(source_variant['option1'],source_variant['option1'])
    radio=page.locator(f'input[data-variant-input][value="{name}"]')
    label=page.locator(f'label[for="{radio.get_attribute("id")}"]')
    label.click()
    page.wait_for_function('(id)=>document.querySelector("select[data-product-select]").value===id',arg=str(source_variant['id']))
    row={'name':name,'checked':radio.is_checked(),'id':page.locator('select[data-product-select]').input_value(),'expected_id':str(source_variant['id'])}
    row['passed']=row['checked'] and row['id']==row['expected_id'];result['colors'].append(row)
    print(json.dumps({'handle':handle,**row}),flush=True)
   result['old_option_names']=page.locator('input[data-variant-input],select[data-product-select] option').evaluate_all('(els)=>els.map(e=>e.tagName==="OPTION"?e.textContent:e.value).filter(t=>/Light Chocolate|Dark Chocolate/i.test(t))')
   result['passed']=response.status==200 and result['theme']['id']==150684762177 and result['theme']['role']=='main' and result['labels']==['Cognac','Army Green','Espresso','Black'] and all(c['passed'] for c in result['colors']) and not result['old_option_names']
   report['products'].append(result)
  report['passed']=len(report['products'])==2 and all(p['passed'] for p in report['products'])
  browser.close()
except Exception:
 report['failure']=traceback.format_exc();print(report['failure'],flush=True)
finally:
 (ROOT/'research/weekender-color-live-qa.json').write_text(json.dumps(report,indent=2))
 print('Saved weekender-color-live-qa.json; passed='+str(report.get('passed')),flush=True)
