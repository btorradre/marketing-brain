import asyncio,json,traceback,sys
from pathlib import Path
from playwright.async_api import async_playwright

ROOT=Path(__file__).resolve().parent
THEME=int(sys.argv[1]) if len(sys.argv)>1 else 151389143105
OUT=ROOT/f'qa/revision-2/story-storefront-{THEME}';OUT.mkdir(exist_ok=True)
HANDLES=json.loads((ROOT/'qa/revision-2/active-story-handles.json').read_text())
report={'theme_id':THEME,'rows':[],'failures':[]}
async def main():
 async with async_playwright() as p:
  browser=await p.chromium.launch();gate=asyncio.Semaphore(3)
  async def check(handle,width):
   async with gate:
    context=await browser.new_context(viewport={'width':width,'height':1000})
    page=await context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    try:
     await page.goto(f'https://velantrafashion.com/products/{handle}?preview_theme_id={THEME}',wait_until='domcontentloaded')
     await page.wait_for_selector('[data-product-section][data-commerce-ready]')
     assert await page.evaluate('Shopify.theme.id')==THEME
     description=page.locator('.product-description');assert await description.locator('p').count()==1
     assert await description.locator('ul,ol').count()==0
     assert len(await description.inner_text())>180
     assert await page.locator('[data-material-fact]').inner_text()
     notes=await page.locator('.product-service-notes').inner_text()
     assert 'Free shipping over $75' in notes and '30-day returns' in notes
     accordions=page.locator('.product-accordions .product-accordion');assert await accordions.count()==3
     heights=await accordions.evaluate_all('(nodes)=>nodes.map(n=>n.getBoundingClientRect().height)')
     assert max(heights)<=55,heights
     headings=await accordions.locator('summary').all_inner_texts()
     assert [x.replace('+','').strip().lower() for x in headings]==['details','materials and care','shipping and returns']
     assert await page.locator('.product-buybox a[href*="/policies/shipping-policy"]').count()==0
     assert await page.locator('.product-batch').count()==0
     for i in range(3):
      await accordions.nth(i).locator('summary').click();assert await accordions.nth(i).get_attribute('open') is not None
     shipping=await page.locator('.product-accordion--shipping').inner_text()
     assert '30-day returns from delivery' in shipping
     assert '7–10 business days' in shipping
     transitions=[]
     if handle in ['velantra-weekender','the-eleanor-weekender']:
      for color in ['Black','Cognac']:
       radio=page.locator('.product-options input[type=radio]').filter(has=None)
       await page.locator('.product-options input[type=radio]').evaluate_all('(els,c)=>{const e=els.find(x=>x.value===c);e.checked=true;e.dispatchEvent(new Event("change",{bubbles:true}));}',color)
       lead=await page.locator('[data-lead-time]').inner_text();material=await page.locator('[data-material-fact]').inner_text();label=await page.locator('[data-add-label]').inner_text()
       assert ('September' in lead)==(color=='Black'),(color,lead)
       assert (material=='All leather')==(color=='Black'),(color,material)
       assert ('PRE-ORDER' in label.upper())==(color=='Black'),(color,label)
       transitions.append({'color':color,'lead_time':lead,'material':material,'button':label})
     else:
      lead=await page.locator('[data-lead-time]').inner_text()
      assert ('October' in lead)==(handle in ['velantra-vivienne','the-colette-wool-tote']),(handle,lead)
     assert not await page.evaluate('document.documentElement.scrollWidth>innerWidth')
     if handle in ['velantra-vivienne','the-colette-wool-tote','velantra-weekender','bag-organizer']:
      await page.locator('.product-detail__content').screenshot(path=str(OUT/f'{handle}-{width}.png'))
     report['rows'].append({'handle':handle,'width':width,'passed':True,'accordion_heights':heights,'lead_time':lead,'variant_changes':transitions,'page_errors':errors})
     print(json.dumps({'handle':handle,'width':width,'passed':True}),flush=True)
    except Exception:
     report['failures'].append({'handle':handle,'width':width,'error':traceback.format_exc()});print(json.dumps(report['failures'][-1]),flush=True)
    finally:
     (OUT/'report.json').write_text(json.dumps(report,indent=2));await context.close()
  await asyncio.gather(*(check(h,w) for h in HANDLES for w in [1440,390]));await browser.close()
 report['passed']=len(report['rows'])==26 and not report['failures'];(OUT/'report.json').write_text(json.dumps(report,indent=2))
 if not report['passed']:raise SystemExit(1)
asyncio.run(main())
