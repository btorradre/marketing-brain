import asyncio,json,hashlib,time,re,traceback
from pathlib import Path
from urllib.parse import urlparse,unquote
from playwright.async_api import async_playwright
OUT=Path(__file__).resolve().parent
RUN_LABEL='after-queue'
BASE='https://velantrafashion.com'
REPORT={'runs':[],'errors':[],'scope':'Fresh private browser contexts only. Adds own test item, may update test quantity, never places an order. Token/cookie values recorded only as SHA256 prefixes.'}
def digest(value):return hashlib.sha256(unquote(str(value)).encode()).hexdigest()[:12] if value else None
def compact_cart(data):return {'item_count':data.get('item_count'),'total_price':data.get('total_price'),'token_hash':digest(data.get('token')),'items':[{'variant_id':i.get('variant_id'),'quantity':i.get('quantity'),'line_price':i.get('final_line_price')} for i in data.get('items',[])]}
def safe_url(url):
 u=urlparse(url)
 if '/checkouts/' in u.path:return u.scheme+'://'+u.netloc+'/checkouts/[redacted]'
 return u.scheme+'://'+u.netloc+u.path+('?' + u.query if u.path.startswith(('/products/','/cart')) else '')
async def cookies(ctx):return [{'name':c['name'],'value_hash':digest(c['value']),'domain':c['domain'],'path':c['path']} for c in await ctx.cookies() if c['name'] in ['cart','cart_sig','cart_ts','_shopify_essential','preview_theme']]
async def run(browser,mode,index):
 ctx=await browser.new_context(viewport={'width':1440,'height':900});page=await ctx.new_page();started=time.monotonic();run={'mode':mode,'index':index,'network':[],'page_errors':[],'cookies':{},'checkouts':[]};tasks=[]
 def elapsed():return round((time.monotonic()-started)*1000)
 async def log_response(res):
  u=urlparse(res.url)
  if not(u.path.startswith('/cart') or '/checkouts/' in u.path):return
  headers=await res.all_headers();rh=await res.request.all_headers();cartcookie=re.search(r'(?:^|;\s*)cart=([^;]+)',rh.get('cookie',''))
  e={'at_ms':elapsed(),'url':safe_url(res.url),'method':res.request.method,'status':res.status,'request_cart_hash':digest(cartcookie.group(1)) if cartcookie else None,'headers':{k:headers[k] for k in ['cache-control','age','cf-cache-status','x-cache','x-request-id','x-shopify-stage','location'] if k in headers and k!='location'}}
  e['set_cookies']=[]
  for h in await res.headers_array():
   if h['name'].lower()=='set-cookie':
    first=h['value'].split(';',1)[0];name,_,value=first.partition('=');e['set_cookies'].append({'name':name,'value_hash':digest(value)})
  if u.path.endswith('.js'):
   try:
    d=await res.json();e['cart']=compact_cart(d) if 'items' in d and 'item_count' in d else {'added_variant':d.get('variant_id'),'quantity':d.get('quantity')}
   except Exception as ex:e['read_error']=type(ex).__name__
  elif u.path=='/cart':
   try:
    html=await res.text();e['html_cart_lines']=len(re.findall(r'<article class="cart-line"',html));e['html_empty']='Your bag is waiting.' in html;e['html_theme_id']=re.search(r'Shopify.theme\s*=\s*(\{[^;]+\})',html).group(1)[:300] if 'Shopify.theme = ' in html else None
   except Exception as ex:e['read_error']=type(ex).__name__
  run['network'].append(e)
 page.on('response',lambda res:tasks.append(asyncio.create_task(log_response(res))))
 page.on('pageerror',lambda e:run['page_errors'].append({'url':safe_url(page.url),'message':str(e),'stack':re.sub(r'/checkouts/[^\s)]+','/checkouts/[redacted]',e.stack)}))
 try:
  await page.goto(BASE+'/products/velantra-vivienne?preview_theme_id=151337074753',wait_until='domcontentloaded')
  await page.wait_for_selector('[data-product-section][data-commerce-ready="true"]')
  run['cookies']['before_add']=await cookies(ctx)
  await page.locator('[data-add-button]').click()
  await page.locator('#CartDrawer .drawer-line').wait_for()
  await page.wait_for_function('!document.querySelector("[data-cart-checkout]").disabled')
  run['cookies']['drawer_ready']=await cookies(ctx);run['drawer_text']=(await page.locator('#CartDrawer').inner_text())[:900]
  if mode=='delay':await page.wait_for_timeout(750)
  if mode=='api_barrier':
   response=await page.request.get(BASE+'/cart.js');run['barrier_cart']=compact_cart(await response.json())
  async with page.expect_navigation(wait_until='domcontentloaded'):
   await page.locator('#CartDrawer').get_by_role('link',name='View your selection',exact=True).click()
  run['cookies']['cart_page']=await cookies(ctx)
  run['main_text']=(await page.locator('main').inner_text())[:1200]
  run['cart_lines']=await page.locator('.cart-page .cart-line').count()
  await page.screenshot(path=str(OUT/f'cart-persistence-{RUN_LABEL}-{index}-{mode}.png'))
  response=await page.request.get(BASE+'/cart.js',headers={'Cache-Control':'no-cache'});run['cart_after_page']=compact_cart(await response.json());run['cookies']['after_api']=await cookies(ctx)
  if run['cart_lines']==0 and run['cart_after_page']['item_count']:
   await page.reload(wait_until='domcontentloaded');run['reload_lines']=await page.locator('.cart-page .cart-line').count();run['cookies']['after_reload']=await cookies(ctx)
  if await page.locator('.cart-page .cart-line').count()>0 and index==0:
   await page.locator('.cart-page input[name="updates[]"]').fill('2')
   async with page.expect_navigation(wait_until='domcontentloaded'):
    await page.locator('.cart-page button[name="checkout"]').click()
   await page.wait_for_url('**/checkouts/**',wait_until='domcontentloaded',timeout=45000)
   await page.get_by_role('heading',name='Contact',exact=True).wait_for(timeout=20000)
   run['checkout_verified']=True;run['checkout_quantity_two_total']=bool(re.search(r'\$299\.98',await page.locator('body').inner_text()))
   await page.screenshot(path=str(OUT/f'cart-persistence-{RUN_LABEL}-quantity-checkout.png'))
  response=await page.request.post(BASE+'/cart/clear.js',data={});run['cleared_test_cart']=compact_cart(await response.json())
 except Exception:
  run['failure']=traceback.format_exc();run['current_url']=safe_url(page.url)
 finally:
  await asyncio.gather(*tasks,return_exceptions=True)
  REPORT['runs'].append(run);(OUT/f'cart-persistence-{RUN_LABEL}.json').write_text(json.dumps(REPORT,indent=2)+'\n')
  print(json.dumps({'index':index,'mode':mode,'lines':run.get('cart_lines'),'after_page':run.get('cart_after_page'),'reload_lines':run.get('reload_lines'),'checkout':run.get('checkout_verified'),'failure':run.get('failure')}),flush=True)
  await ctx.close()
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(headless=True)
  for i,mode in enumerate(['immediate','immediate','immediate','delay','delay','immediate']):await run(b,mode,i)
  await b.close()
asyncio.run(main())
