import json
from pathlib import Path
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parent
catalog=json.loads((R/'catalog-before.json').read_text());report=[]
with sync_playwright() as p:
 b=p.chromium.launch(headless=True)
 for width in [1440,390]:
  context=b.new_context(viewport={'width':width,'height':1000},reduced_motion='reduce');page=context.new_page()
  for product in catalog:
   handle=product['handle'];page.goto('https://velantrafashion.com/products/'+handle+'?preview_theme_id=151389143105',wait_until='domcontentloaded');page.locator('.product-description').wait_for()
   facts=page.locator('.product-facts').inner_text();labels=page.locator('.product-accordion>summary').all_inner_texts();metrics=page.locator('.product-accordion').evaluate_all('(els)=>els.map(e=>({height:e.getBoundingClientRect().height,margin:getComputedStyle(e.querySelector("summary")).margin,padding:getComputedStyle(e.querySelector("summary")).padding}))')
   assert len(labels)==4,(handle,labels)
   assert [x.replace('\n+','').strip().upper() for x in labels]==['DETAILS','CARE','SHIPPING & DELIVERY','RETURNS']
   assert all(44<=m['height']<=46 for m in metrics),(handle,metrics)
   assert all(m['margin']=='0px' and m['padding']=='0px' for m in metrics)
   assert page.locator('.product-description li').count()==0
   assert '10 days before dispatch' in facts
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),handle
   for i in range(4):
    row=page.locator('.product-accordion').nth(i);row.locator('summary').click();assert row.get_attribute('open') is not None;assert row.locator('.rte').is_visible();row.locator('summary').click()
   if handle=='velantra-weekender':
    page.locator('.product-option__value label[title="Black"]').click();assert 'Vegetable-tanned leather' in page.locator('[data-material-fact]').inner_text();assert '10 days before dispatch' in page.locator('[data-lead-time]').inner_text()
   report.append({'handle':handle,'width':width,'passed':True,'accordion_heights':[m['height'] for m in metrics]})
   if handle in ['the-colette-wool-tote','velantra-vivienne','bag-organizer']:
    page.locator('.product-buybox').screenshot(path=str(R/f'{handle}-{width}-buybox.png'))
   print(handle,width,'passed',flush=True)
  context.close()
 b.close()
(R/'pdp-qa.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS',len(report),'desktop/mobile PDP checks')
