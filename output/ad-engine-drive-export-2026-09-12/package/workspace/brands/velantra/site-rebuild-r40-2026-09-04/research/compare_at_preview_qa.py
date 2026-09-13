from pathlib import Path
from playwright.sync_api import sync_playwright
import json,re,traceback
OUT=Path(__file__).resolve().parent
BASE='https://velantrafashion.com'
THEME='151337074753'
products=json.loads((OUT/'compare-at-catalog-2026-09-05.json').read_text())['data']['products']['nodes']
report={'date':'2026-09-05','theme_id':THEME,'products':[],'cards':[],'mobile':[],'edge_cases':[],'page_errors':[],'screenshots':[],'catalog_mutations':False,'cart_mutations':False}

def start(context,path):
 page=context.new_page();page.on('pageerror',lambda e:report['page_errors'].append(str(e)))
 page.goto(BASE+path+'?preview_theme_id='+THEME,wait_until='domcontentloaded')
 return page

def ready(page):
 page.wait_for_selector('[data-product-section][data-commerce-ready="true"]')
 assert not re.search(r'Liquid (?:error|syntax error)|Translation missing',page.content(),re.I)

def displays(page):
 return page.locator('[data-product-price] [data-price-display], [data-sticky-price] [data-price-display]').evaluate_all('''nodes=>nodes.map(n=>({current:n.querySelector('[data-price-current]').textContent,compare:n.querySelector('[data-price-compare]').textContent,compareHidden:n.querySelector('[data-price-compare-group]').hidden,valuesHidden:n.querySelector('[data-price-values]').hidden,status:n.querySelector('[data-price-status]').textContent,statusHidden:n.querySelector('[data-price-status]').hidden,accessibleLabels:[...n.querySelectorAll('.visually-hidden')].map(e=>e.textContent.trim())}))''')

def screenshot(page,name):
 page.evaluate('document.fonts.ready')
 first=page.locator('[data-product-section] img, .product-card__media img').first
 try:first.evaluate('(image)=>image.decode()')
 except Exception:pass
 if name.startswith('compare-at-vivienne-mobile'):
  page.locator('[data-product-price]').evaluate('el=>el.scrollIntoView({block:"center"})')
  page.wait_for_timeout(150)
 page.screenshot(path=str(OUT/name),full_page=False);report['screenshots'].append(name)

def choose(page,variant):
 previous=page.locator('[data-variant-select]').input_value()
 page.locator('[data-option-picker] label[title='+json.dumps(variant['title'])+']').click()
 expected=variant['id'].split('/')[-1]
 page.wait_for_function('(id)=>document.querySelector("[data-variant-select]").value===id',arg=expected)
 if previous != expected:assert 'variant='+expected in page.url

try:
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True)
  ctx=browser.new_context(viewport={'width':1440,'height':1000})
  page=start(ctx,'/products/velantra-vivienne');ready(page)
  for product in products:
   page.goto(BASE+'/products/'+product['handle'],wait_until='domcontentloaded');ready(page)
   native=json.loads(page.locator('[data-product-variants]').text_content())
   assert len(native)==len(product['variants']['nodes'])
   checks=[]
   for variant in product['variants']['nodes']:
    choose(page,variant)
    data=next(v for v in native if str(v['id'])==variant['id'].split('/')[-1])
    assert data['price']==round(float(variant['price'])*100)
    expected_compare=None if variant['compareAtPrice'] is None else round(float(variant['compareAtPrice'])*100)
    assert data['compare_at_price']==expected_compare
    state=displays(page)
    priced=data['price']>0;compare=priced and expected_compare is not None and expected_compare>data['price']
    for s in state:
     assert s['valuesHidden'] != priced and s['statusHidden']==priced,s
     assert s['compareHidden'] != compare,s
     if priced:assert s['current']==data['formatted_price'],s
     else:
      assert s['status']=='Contact for availability',s
      assert page.locator('[data-add-button]').is_disabled()
     if compare:assert s['compare']==data['formatted_compare_at_price'],s
     assert s['accessibleLabels']==['Current price','Compare-at price'],s
    checks.append({'variant':variant['title'],'id':data['id'],'price':variant['price'],'compare_at':variant['compareAtPrice'],'display':state[0]})
   overflow=page.evaluate('document.documentElement.scrollWidth>innerWidth+1')
   assert not overflow,product['handle']
   report['products'].append({'handle':product['handle'],'variants':checks,'overflow':overflow,'passed':True})
   print(json.dumps({'product':product['handle'],'variants':len(checks),'passed':True}),flush=True)
   if product['handle']=='velantra-vivienne':
    choose(page,product['variants']['nodes'][0]);screenshot(page,'compare-at-vivienne-desktop.png')
  for path in ['/collections/all','/search?q=Vivienne&type=product']:
   page.goto(BASE+path,wait_until='domcontentloaded');page.wait_for_selector('.product-card [data-price-display]')
   states=page.locator('.product-card').evaluate_all('''cards=>cards.map(c=>{const n=c.querySelector('[data-price-display]');return {productId:c.dataset.productId,current:n.querySelector('[data-price-current]').textContent,compare:n.querySelector('[data-price-compare]').textContent,compareHidden:n.querySelector('[data-price-compare-group]').hidden,valuesHidden:n.querySelector('[data-price-values]').hidden,status:n.querySelector('[data-price-status]').textContent}})''')
   for state in states:
    product=next(x for x in products if x['id'].split('/')[-1]==state['productId'])
    minimum=min(product['variants']['nodes'],key=lambda v:float(v['price']))
    priced=float(minimum['price'])>0
    assert state['valuesHidden'] != priced,state
    assert state['compareHidden'] != priced,state
    if priced:
     assert minimum['price'] in state['current'] and minimum['compareAtPrice'] in state['compare'],state
    else:assert state['status']=='Contact for availability',state
   if path.startswith('/collections'):assert len(states)==13
   report['cards'].append({'path':path,'states':states,'passed':True})
   if path.startswith('/collections'):screenshot(page,'compare-at-collection-desktop.png')
  ctx.close()
  mobile=browser.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True,device_scale_factor=1)
  page=start(mobile,'/products/velantra-vivienne');ready(page)
  for width in [390,320]:
   page.set_viewport_size({'width':width,'height':844})
   for path in ['/products/velantra-vivienne','/products/velantra-juliette','/collections/all']:
    page.goto(BASE+path,wait_until='domcontentloaded')
    if path.startswith('/products'):ready(page)
    else:page.wait_for_selector('.product-card [data-price-display]')
    page.evaluate('document.fonts.ready')
    if path.endswith('vivienne'):
     page.locator('[data-product-price]').scroll_into_view_if_needed()
     screenshot(page,f'compare-at-vivienne-mobile-{width}.png')
    if path.startswith('/collections'):
     cards=page.locator('.product-card__heading').evaluate_all('''rows=>rows.map(r=>({title:r.querySelector('h3').textContent.trim(),rowFits:r.scrollWidth<=r.clientWidth+1,priceFits:r.querySelector('.product-card__price').scrollWidth<=r.querySelector('.product-card__price').clientWidth+1}))''')
     assert all(x['rowFits'] and x['priceFits'] for x in cards),cards
     page.locator('.collection-heading').scroll_into_view_if_needed();screenshot(page,f'compare-at-collection-mobile-{width}.png')
    overflow=page.evaluate('document.documentElement.scrollWidth>innerWidth+1')
    assert not overflow,(width,path)
    report['mobile'].append({'width':width,'path':path,'overflow':overflow,'passed':True})
  # Edge cases use a fresh browser context and a response fixture only; Shopify data stays unchanged.
  edge=browser.new_context(viewport={'width':390,'height':844})
  basepage=start(edge,'/products/velantra-vivienne');ready(basepage)
  html=basepage.content()
  variants=json.loads(basepage.locator('[data-product-variants]').text_content())
  for index,value in enumerate([None,variants[1]['price'],variants[2]['price']-100,variants[3]['price']+12345]):
   variants[index]['compare_at_price']=value
   variants[index]['formatted_compare_at_price']='fixture '+str(value)
  html=re.sub(r'(<script[^>]*data-product-variants[^>]*>).*?(</script>)',lambda m:m.group(1)+json.dumps(variants)+m.group(2),html,flags=re.S)
  html=html.replace('data-commerce-ready="true"','')
  fixture_url=BASE+'/products/velantra-vivienne?price_qa_fixture=1'
  basepage.route('**/*price_qa_fixture=1',lambda route:route.fulfill(status=200,content_type='text/html',body=html))
  basepage.goto(fixture_url,wait_until='domcontentloaded');ready(basepage)
  for index,v in enumerate(variants):
   basepage.locator('[data-option-picker] label[title='+json.dumps(v['options'][0])+']').click()
   states=displays(basepage);expect=index==3
   assert all(s['compareHidden']!=expect for s in states),states
   report['edge_cases'].append({'fixture_only':True,'case':['blank','equal','lower','higher'][index],'compare_visible':expect,'passed':True})
  basepage.locator('[data-price-display]').evaluate_all("nodes=>nodes.forEach(n=>n.dataset.compareEnabled='false')")
  basepage.locator('[data-option-picker] label[title='+json.dumps(variants[0]['options'][0])+']').click()
  basepage.locator('[data-option-picker] label[title='+json.dumps(variants[3]['options'][0])+']').click()
  assert all(s['compareHidden'] for s in displays(basepage))
  report['edge_cases'].append({'fixture_only':True,'case':'display_setting_false','compare_visible':False,'passed':True})
  browser.close()
 report['pricing_assertions_passed']=len(report['products'])==13 and all(v['passed'] for k in ['products','cards','mobile','edge_cases'] for v in report[k])
 report['page_error_note']='Any fbq is not defined error is reported separately as an intermittent external pixel-global error; theme sources do not reference fbq.'
 report['passed']=report['pricing_assertions_passed'] and not any(e != 'fbq is not defined' for e in report['page_errors'])
except Exception:
 report['failure']=traceback.format_exc();print(report['failure'],flush=True);report['passed']=False
finally:
 (OUT/'compare-at-preview-qa.json').write_text(json.dumps(report,indent=2)+'\n')
 print('QA passed='+str(report['passed']),flush=True)
