from pathlib import Path
from playwright.sync_api import sync_playwright
import json,re
OUT=Path(__file__).parent
expected=[('All bags','/collections/handbags'),('Accessories','/collections/accessories'),('Track your order','/apps/parcel'),('Contact','/pages/contact')]
report={'checks':[],'errors':[]}
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True)
 for width in [1440,1101,390]:
  ctx=browser.new_context(viewport={'width':width,'height':900});page=ctx.new_page()
  page.on('pageerror',lambda e:report['errors'].append(str(e)))
  page.goto('https://velantrafashion.com/?preview_theme_id=151337074753',wait_until='domcontentloaded')
  page.evaluate('document.fonts.ready')
  if width>1100:
   nav=page.locator('.desktop-nav')
   overlaps=page.evaluate('''()=>{let a=document.querySelector('.desktop-nav').getBoundingClientRect(),b=document.querySelector('.wordmark').getBoundingClientRect();return a.right>b.left;}''')
   assert not overlaps, {'width':width,'overlap':True}
  else:
   page.get_by_role('button',name='Menu',exact=True).click();nav=page.locator('#NavigationDrawer nav')
  links=nav.locator('a').evaluate_all('(els)=>els.map(e=>({title:e.textContent.trim(),url:new URL(e.href).pathname}))')
  primary=[(x['title'],x['url']) for x in links[:4]]
  assert primary==expected,primary
  assert not any('/products/' in x['url'] for x in links)
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
  if width==1440:
   page.locator('.site-header').screenshot(path=str(OUT/'navigation-four-links-desktop.png'))
  elif width==390:
   page.locator('#NavigationDrawer').screenshot(path=str(OUT/'navigation-four-links-mobile.png'))
  report['checks'].append({'width':width,'links':links,'bag_product_links_removed':True,'no_overflow':True})
  print(json.dumps(report['checks'][-1]),flush=True)
  if width!=1101:
   for title,url in expected:
    nav.get_by_role('link',name=title,exact=True).click()
    page.wait_for_url('**'+url,wait_until='domcontentloaded')
    assert not re.search(r'Liquid (?:error|syntax error)|Translation missing',page.content(),re.I)
    if title=='Contact': assert page.locator('form[action*="/contact"]').count()>0
    if title=='Track your order': page.locator('input[name="order"]:visible').wait_for(state='visible')
    report['checks'].append({'width':width,'clicked':title,'destination':url})
    page.go_back(wait_until='domcontentloaded')
    if width<=1100:
     if not page.locator('#NavigationDrawer').is_visible():page.get_by_role('button',name='Menu',exact=True).click()
     nav=page.locator('#NavigationDrawer nav')
    else:nav=page.locator('.desktop-nav')
  ctx.close()
 browser.close()
report['passed']=True
(OUT/'navigation-four-links-qa.json').write_text(json.dumps(report,indent=2)+'\n')
print('All four menu destinations verified on desktop and mobile.',flush=True)
