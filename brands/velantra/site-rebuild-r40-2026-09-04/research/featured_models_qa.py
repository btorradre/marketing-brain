from pathlib import Path
import json,re,traceback
from playwright.sync_api import sync_playwright
OUT=Path(__file__).parent
report={'checks':[],'errors':[]}
def note(name,**data):
 report['checks'].append(dict(name=name,**data));print(json.dumps(report['checks'][-1]),flush=True)
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True)
  for width in [1440,390]:
   ctx=browser.new_context(viewport={'width':width,'height':1000 if width==1440 else 844})
   page=ctx.new_page();page.on('pageerror',lambda e:report['errors'].append(str(e)))
   page.goto('https://velantrafashion.com/?preview_theme_id=151337074753',wait_until='domcontentloaded')
   section=page.locator('.featured-model-collection');section.scroll_into_view_if_needed()
   section.locator('img').evaluate_all('(images)=>Promise.all(images.map(i=>i.decode()))')
   page.evaluate('document.fonts.ready')
   cards=section.locator('.featured-model-collection__item')
   data=cards.evaluate_all('''cards=>cards.map(c=>({title:c.querySelector('h3').textContent.trim(),href:c.querySelector('a').getAttribute('href'),image:c.querySelector('img').currentSrc,alt:c.querySelector('img').alt,fit:getComputedStyle(c.querySelector('img')).objectFit,current:c.querySelector('[data-price-current]').textContent.trim(),compare:c.querySelector('[data-price-compare]').textContent.trim()}))''')
   assert [c['title'] for c in data]==['VIVIENNE','WEEKENDER','MERIDIAN'],data
   assert len(set(c['image'] for c in data))==3
   assert data[1]['fit']=='contain'
   assert page.locator('#shopify-section-wide').count()==0
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
   assert not re.search(r'Liquid (?:error|syntax error)|Translation missing',page.content(),re.I)
   section.screenshot(path=str(OUT/f'featured-models-{width}.png'))
   note('layout_'+str(width),cards=data,no_overflow=True,repeated_wide_section_absent=True)
   if width==1440:
    for card in data:
     link=section.locator('.featured-model-collection__media').filter(has=page.locator('img[alt="'+card['alt']+'"]'))
     link.click();page.wait_for_selector('[data-product-section][data-commerce-ready="true"]')
     assert page.url.split('?')[0].endswith(card['href'].split('?')[0])
     expected=card['href'].split('variant=')[1]
     assert page.locator('[data-variant-select]').input_value()==expected
     note('pdp_link_'+card['title'],product=page.locator('h1').inner_text(),variant=expected)
     page.go_back(wait_until='domcontentloaded');section=page.locator('.featured-model-collection')
   else:
    section.locator('.featured-model-collection__grid').evaluate('(el)=>el.scrollTo({left:el.scrollWidth,behavior:"instant"})')
    page.wait_for_function('document.querySelector(".featured-model-collection__grid").scrollLeft>0')
    section.screenshot(path=str(OUT/'featured-models-mobile-meridian.png'))
    note('mobile_scroll',all_three_accessible=True)
   ctx.close()
  browser.close()
except Exception:
 report['failure']=traceback.format_exc();print(report['failure'],flush=True)
finally:
 (OUT/'featured-models-qa.json').write_text(json.dumps(report,indent=2))
