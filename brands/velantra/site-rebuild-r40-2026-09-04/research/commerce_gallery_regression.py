from pathlib import Path
import json,re,traceback
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).parent
URL='https://velantrafashion.com'
report={'checks':[],'page_errors':[]}
def record(name,**data):
 row={'name':name,**data};report['checks'].append(row);print(json.dumps(row),flush=True)
def go(page,handle):
 page.goto(f'{URL}/products/{handle}?preview_theme_id=151337074753',wait_until='domcontentloaded')
 page.wait_for_selector('[data-commerce-ready]')
 page.evaluate('document.fonts.ready')
 assert 'Liquid error' not in page.content()
 assert 'translation missing' not in page.content().lower()
def check_selection(page,label):
 previous_id=page.locator('[data-variant-select]').input_value()
 page.locator(f'[data-option-picker] label[title="{label}"]').click()
 page.wait_for_function('(name)=>document.querySelector("[data-selected-option]").textContent===name',arg=label)
 selected_id=page.locator('[data-variant-select]').input_value()
 variants=json.loads(page.locator('[data-product-variants]').text_content())
 variant=next(v for v in variants if str(v['id'])==selected_id)
 media=page.locator('[data-media-id]:visible').evaluate_all('(items)=>items.map(m=>({id:m.dataset.mediaId,color:m.dataset.color,first:m.hasAttribute("data-first-visible"),src:m.querySelector("img")?.getAttribute("src"),left:m.getBoundingClientRect().left}))')
 assert str(variant['featured_media_id'])==media[0]['id'],(label,variant,media)
 assert media[0]['first']
 assert sum(i['first'] for i in media)==1
 if selected_id!=previous_id:assert selected_id in page.url
 record('selected_first',label=label,id=selected_id,first_media=media[0]['id'],visible_media=len(media),shared_media=[m['id'] for m in media if not m['color']],first_image=media[0]['src'])
 return media
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True)
  ctx=browser.new_context(viewport={'width':1440,'height':1080});page=ctx.new_page();page.on('pageerror',lambda e:report['page_errors'].append(str(e)))
  go(page,'velantra-vivienne')
  report['title_override_passed']=page.locator('h1').inner_text()=='VIVIENNE'
  assert 'The Vivienne Top Handle Bag' in page.title()
  record('display_title',heading=page.locator('h1').inner_text(),seo_title=page.title())
  for color in ['Cognac','Black','Olive','Chocolate']:
   media=check_selection(page,color)
   assert all(m['color']==color.lower() for m in media)
   assert 'white-studio.webp' in media[0]['src']
  frame=page.frame(name='PBarNextFrame')
  if frame:
   try:frame.get_by_role('button',name='Hide bar',exact=True).click(timeout=5000)
   except Exception:pass
  page.screenshot(path=str(ROOT/'commerce-preview-gallery-regression-desktop.png'),full_page=False)
  go(page,'velantra-cherry-charm')
  for color in ['Cherry Red','Lady Pink','Midnight Black']:
   check_selection(page,color)
  go(page,'velantra-horse-charm')
  for color in ['Matte','Verdant','Brown']:
   media=check_selection(page,color)
   assert any(not m['color'] for m in media),'Unassigned source image must stay shared'
  page.set_viewport_size({'width':390,'height':844})
  go(page,'velantra-vivienne')
  check_selection(page,'Cognac')
  page.locator('[data-gallery-next]').click()
  page.wait_for_function('document.querySelector("[data-gallery-count]").textContent==="2 / 3"')
  record('mobile_next',count=page.locator('[data-gallery-count]').inner_text())
  check_selection(page,'Olive')
  assert page.locator('[data-gallery-count]').text_content()=='1 / 3'
  page.locator('[data-media-id]:visible [data-zoom-image]').first.click()
  page.wait_for_selector('[data-product-lightbox][open]')
  page.keyboard.press('Escape')
  assert not page.locator('[data-product-lightbox]').is_visible()
  assert page.evaluate('document.activeElement.hasAttribute("data-zoom-image")')
  record('mobile_switch_lightbox',gallery_reset=True,escape_closes=True,focus_restored=True)
  page.keyboard.press('Home')
  page.locator('h1').scroll_into_view_if_needed()
  page.screenshot(path=str(ROOT/'commerce-preview-gallery-regression-mobile.png'),full_page=False)
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
  report['passed']=not report['page_errors']
  browser.close()
except Exception:
 report['failure']=traceback.format_exc();print(report['failure'],flush=True)
finally:
 (ROOT/'commerce-gallery-regression.json').write_text(json.dumps(report,indent=2))
 print('Saved commerce-gallery-regression.json',flush=True)
