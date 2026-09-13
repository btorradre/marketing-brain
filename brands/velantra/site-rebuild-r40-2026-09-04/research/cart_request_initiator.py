import asyncio,json,time,re,hashlib
from pathlib import Path
from urllib.parse import urlparse,parse_qsl,unquote
from playwright.async_api import async_playwright
OUT=Path(__file__).resolve().parent
async def main():
 report={'runs':[]}
 async with async_playwright() as p:
  browser=await p.chromium.launch(headless=True)
  for index in range(2):
   context=await browser.new_context(viewport={'width':1440,'height':900});page=await context.new_page();client=await context.new_cdp_session(page);await client.send('Network.enable')
   run={'index':index,'cart_posts':[],'scripts':[]};started=time.monotonic()
   def clean_stack(stack):
    if not stack:return None
    return {'description':stack.get('description'),'frames':[{'function':f.get('functionName'),'script':urlparse(f.get('url',''))._replace(query='',fragment='').geturl(),'line':f.get('lineNumber'),'column':f.get('columnNumber')} for f in stack.get('callFrames',[])],'parent':clean_stack(stack.get('parent'))}
   def request(event):
    req=event['request'];url=urlparse(req['url'])
    if url.path=='/cart.js' and req['method']=='POST':
     body=req.get('postData','')
     try:
      parsed=json.loads(body);keys=list(parsed);nested={k:list(v) for k,v in parsed.items() if isinstance(v,dict)}
     except Exception:keys=[k for k,v in parse_qsl(body)];nested={}
     run['cart_posts'].append({'at_ms':round((time.monotonic()-started)*1000),'post_keys':keys,'nested_keys':nested,'initiator_type':event.get('initiator',{}).get('type'),'stack':clean_stack(event.get('initiator',{}).get('stack'))})
   client.on('Network.requestWillBeSent',request)
   await page.goto('https://velantrafashion.com/products/velantra-vivienne?preview_theme_id=151337074753',wait_until='domcontentloaded');await page.wait_for_selector('[data-commerce-ready="true"]')
   run['scripts']=await page.locator('script[src]').evaluate_all('nodes=>nodes.map(n=>{const u=new URL(n.src);return u.origin+u.pathname})')
   await page.locator('[data-add-button]').click();await page.wait_for_timeout(2200)
   run['drawer_count']=await page.locator('#CartDrawer .drawer-line').count()
   r=await page.request.get('https://velantrafashion.com/cart.js');d=await r.json();run['cart_count']=d['item_count'];run['cart_token_hash']=hashlib.sha256(unquote(d['token']).encode()).hexdigest()[:12]
   await page.request.post('https://velantrafashion.com/cart/clear.js',data={})
   report['runs'].append(run);await context.close()
  await browser.close()
 (OUT/'cart-request-initiator.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(report,indent=2))
asyncio.run(main())
