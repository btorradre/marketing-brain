from playwright.sync_api import sync_playwright
from pathlib import Path
from urllib.parse import urlparse,parse_qs
import json,sys,re,datetime
P=Path(__file__).resolve().parent
preview='preview' in sys.argv
url='https://getmotilli.com/products/motilli-3-bottle-90day-reset'+('?view=motilli-regularity' if preview else '')
label='preview' if preview else 'live'
results={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'url':url,'synthetic_carts':True,'cases':[]}
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True)
 for width,qty in [(390,3),(390,1),(1440,5)]:
  ctx=browser.new_context(viewport={'width':width,'height':900 if width>500 else 844},is_mobile=width<500,has_touch=width<500,user_agent=pw.devices['iPhone 13']['user_agent'] if width<500 else f'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{browser.version} Safari/537.36')
  page=ctx.new_page();page.set_default_timeout(12000)
  events=[];errors=[];failed=[]
  def response(r):
   req=r.request
   if 'facebook.com' in r.url:
    fields=parse_qs(urlparse(r.url).query)
    if req.post_data:fields.update(parse_qs(req.post_data))
    if fields.get('ev'):events.append({'source':'meta','event':fields.get('ev'),'pixel':fields.get('id'),'status':r.status,'value':fields.get('cd[value]'),'currency':fields.get('cd[currency]')})
   if 'monorail' in r.url and req.post_data:
    names=sorted(set(re.findall(r'"(?:event_name|eventName)"\s*:\s*"([^"]+)"',req.post_data)))
    if names:events.append({'source':'shopify-telemetry','events':names,'status':r.status})
  ctx.on('response',response)
  page.on('pageerror',lambda e:errors.append(str(e)[:300]))
  page.on('requestfailed',lambda r:failed.append({'url':r.url.split('?')[0],'failure':r.failure}))
  page.goto(url,wait_until='domcontentloaded',timeout=45000)
  page.locator('kaching-bundle').wait_for(timeout=20000)
  page.wait_for_timeout(1800)
  assert page.locator('.motilli-regularity').count()==1,'New product template not rendered'
  assert page.locator('h1').inner_text()=='Motilli Celery Juice Gummies'
  title={1:'Buy One',3:'Buy 2 Get 1 Free',5:'Buy 3 Get 2 Free'}[qty]
  page.locator('.kaching-bundles__bar-main').filter(has=page.locator('.kaching-bundles__bar-title',has_text=re.compile('^'+re.escape(title)+'$'))).click()
  page.wait_for_timeout(500)
  form=page.locator('form[action="/cart/add"]');submit=form.locator('button[type="submit"]')
  assert form.locator('input[name="quantity"]').input_value()==str(qty)
  before={'button':submit.inner_text(),'quantity':qty,'shipping':page.locator('[data-motilli-shipping]').inner_text(),'horizontal_overflow':page.evaluate('document.documentElement.scrollWidth>innerWidth'),'button_y':submit.bounding_box()['y']}
  assert str(qty) in before['button'],'Selected quantity missing from button'
  assert not before['horizontal_overflow'],'Horizontal overflow'
  page.evaluate('scrollTo(0,0)')
  page.screenshot(path=str(P/f'{label}-{width}-{qty}-top.png'),full_page=False)
  if width==390 and qty==3:
   page.screenshot(path=str(P/f'{label}-mobile-full.png'),full_page=True)
   (P/f'{label}-visible-text.txt').write_text(page.locator('body').inner_text())
   page.locator('.motilli-explainer').scroll_into_view_if_needed()
   page.wait_for_timeout(250)
   assert page.locator('.motilli-sticky').is_visible(),'Mobile return-to-buy control missing'
   page.locator('[data-motilli-sticky-button]').click()
  else:
   submit.click()
  page.locator('cart-drawer.active').wait_for(timeout=12000)
  page.wait_for_timeout(2500)
  cart=page.request.get('https://getmotilli.com/cart.js').json()
  expected={1:2999,3:5998,5:8997}[qty]
  assert cart['item_count']==qty,(cart['item_count'],qty)
  assert cart['total_price']==expected,(cart['total_price'],expected)
  assert all(i['variant_id']==53033648750959 for i in cart['items'])
  assert all(not i.get('selling_plan_allocation') for i in cart['items']),'Unexpected subscription'
  assert not page.locator('.motilli-sticky').is_visible(),'Sticky control overlaps cart'
  page.screenshot(path=str(P/f'{label}-{width}-{qty}-cart.png'),full_page=False)
  result={'width':width,**before,'cart_items':cart['item_count'],'cart_total_cents':cart['total_price'],'one_time_purchase':True,'events':events,'errors':errors,'failed_requests':failed}
  if width==390 and qty==1:
   checkout=page.locator('cart-drawer.active button[name="checkout"]')
   print('checkout-buttons',checkout.count(),flush=True)
   if checkout.count()==1:
    checkout.click();page.wait_for_url(re.compile(r'.*/checkouts?/.*'),timeout=25000);page.wait_for_timeout(1800)
    result['checkout_url_path']=urlparse(page.url).path
    result['checkout_loaded']=page.get_by_role('textbox',name=re.compile('Email',re.I)).count()>0
    page.screenshot(path=str(P/f'{label}-checkout.png'),full_page=False)
  results['cases'].append(result)
  (P/f'{label}-verification.json').write_text(json.dumps(results,indent=2))
  print(json.dumps({k:v for k,v in result.items() if k not in ['failed_requests','events']}),flush=True)
  ctx.close()
 browser.close()
