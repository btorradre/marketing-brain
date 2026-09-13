from pathlib import Path
import argparse,json,re,traceback
from playwright.sync_api import sync_playwright
parser=argparse.ArgumentParser();parser.add_argument('--native',action='store_true');args=parser.parse_args()
PROJECT=Path('/Users/brooksorradre2/Documents/marketing brain/brands/velantra/site-rebuild-r40-2026-09-04')
OUT=Path('/tmp/pdp-horizontal-gallery-native' if args.native else '/tmp/pdp-horizontal-gallery-local');OUT.mkdir(exist_ok=True)
styles=(PROJECT/'theme/snippets/commerce-styles.liquid').read_text()
styles=styles[styles.index('<style>'):]
script=(PROJECT/'theme/snippets/commerce-script.liquid').read_text()
report={'mode':'native' if args.native else 'local-response-override','checks':[],'errors':[]}
def replace_between(text,start,end,replacement):
 a=text.index(start);b=text.index(end,a);return text[:a]+replacement+text[b:]
def updated_response(route):
 if route.request.resource_type!='document':return route.continue_()
 response=route.fetch();html=response.text()
 if 'function initializeProduct' not in html:return route.fulfill(response=response)
 html,n=re.subn(r'<style>\s*\.product-detail\{.*?</style>',lambda _:styles,html,count=1,flags=re.S)
 assert n==1,'Commerce style block not found'
 start='    function galleryIndex() {' if '    function galleryIndex() {' in html else '    function updateGalleryCount() {'
 new=script[script.index('    function galleryIndex() {'):script.index('    function filterGallery')]
 html=replace_between(html,start,'    function filterGallery',new)
 start='    if (viewport) {\n'
 a=script.index(start);b=script.index('    const lightbox',a)
 html=replace_between(html,start,'    const lightbox',script[a:b])
 route.fulfill(response=response,body=html)
def note(name,**data):
 check={'name':name,**data};report['checks'].append(check);print(json.dumps(check),flush=True)
def metrics(page):
 return page.locator('[data-gallery-viewport]').evaluate('''el=>({display:getComputedStyle(el).display,width:el.clientWidth,height:el.clientHeight,scrollWidth:el.scrollWidth,left:el.scrollLeft,snap:getComputedStyle(el).scrollSnapType,document:document.documentElement.scrollWidth,viewport:innerWidth,top:el.getBoundingClientRect().top,items:[...el.querySelectorAll('[data-media-id]:not([hidden])')].map(i=>({id:i.dataset.mediaId,color:i.dataset.color,left:i.getBoundingClientRect().left,top:i.getBoundingClientRect().top,width:i.clientWidth,height:i.clientHeight,fit:i.querySelector('img')?getComputedStyle(i.querySelector('img')).objectFit:null}))})''')
def settle_slide(page,index):
 page.wait_for_function('''expected=>{const v=document.querySelector('[data-gallery-viewport]');return Math.abs(v.scrollLeft-expected*v.clientWidth)<2}''',arg=index)
 page.wait_for_function('''expected=>document.querySelector('[data-gallery-count]').textContent.startsWith(String(expected+1)+' /')''',arg=index)
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True)
  for width in [1440,390]:
   context=browser.new_context(viewport={'width':width,'height':1000 if width==1440 else 844},has_touch=width==390,is_mobile=width==390)
   page=context.new_page();page.on('pageerror',lambda e:report['errors'].append(str(e)))
   if not args.native:page.route('**/products/**',updated_response)
   for product in ['velantra-vivienne','velantra-weekender','velantra-margot-tote']:
    page.goto('https://velantrafashion.com/products/'+product+'?preview_theme_id=151337074753',wait_until='domcontentloaded')
    page.wait_for_selector('[data-product-section][data-commerce-ready="true"]')
    gallery=page.locator('[data-gallery]');viewport=page.locator('[data-gallery-viewport]')
    viewport.scroll_into_view_if_needed()
    viewport.locator('[data-media-id]:not([hidden]) img').evaluate_all('(images)=>Promise.all(images.slice(0,1).map(i=>i.decode()))')
    page.evaluate('document.fonts.ready')
    before=metrics(page)
    assert before['display']=='flex' and before['snap']=='x mandatory',before
    assert before['document']<=width+1,before
    assert len(before['items'])>1,before
    assert all(abs(i['top']-before['items'][0]['top'])<1 for i in before['items']),before
    assert all(i['fit'] in [None,'contain'] for i in before['items']),before
    assert page.locator('[data-gallery-controls]').is_visible()
    assert page.locator('[data-gallery-prev]').is_disabled()
    page.locator('[data-gallery-next]').click();settle_slide(page,1)
    page.locator('[data-gallery-prev]').click();settle_slide(page,0)
    viewport.focus();page.keyboard.press('ArrowRight');settle_slide(page,1)
    viewport.hover();page.mouse.wheel(before['width'],0);settle_slide(page,2)
    viewport.focus();page.keyboard.press('ArrowLeft');settle_slide(page,1)
    zoom=viewport.locator('[data-media-id]:not([hidden]) [data-zoom-image]').nth(1)
    zoom.click();assert page.locator('[data-product-lightbox]').evaluate('(el)=>el.open')
    page.keyboard.press('Escape');assert not page.locator('[data-product-lightbox]').evaluate('(el)=>el.open')
    color=page.locator('[data-color-option] input:not(:checked)').first
    alternate=color.input_value();color_id=color.get_attribute('id')
    page.locator('label[for="'+color_id+'"]').click();settle_slide(page,0)
    changed=metrics(page)
    color_handle=re.sub(r'[^a-z0-9]+','-',alternate.lower()).strip('-')
    assert all(i['color'] in ['',color_handle] for i in changed['items']),changed
    selected=page.locator('[data-variant-select]').input_value()
    expected=page.locator('[data-product-variants]').evaluate('(el,id)=>JSON.parse(el.textContent).find(v=>String(v.id)===id)',selected)
    assert page.locator('[data-product-price] [data-price-current]').inner_text()==expected['formatted_price']
    assert str(changed['items'][0]['id'])==str(expected['featured_media_id']),changed
    assert page.locator('[data-gallery-count]').inner_text()=='1 / '+str(len(changed['items']))
    if product=='velantra-vivienne':
     viewport.scroll_into_view_if_needed()
     if width==390:
      box=viewport.bounding_box();cdp=context.new_cdp_session(page)
      x=box['x']+box['width']*.85;y=box['y']+box['height']*.55
      cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x,'y':y}]})
      for step in range(1,9):
       cdp.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':x-step*box['width']*.075,'y':y}]})
      cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
      page.wait_for_function('document.querySelector("[data-gallery-viewport]").scrollLeft>10')
      note('touch_swipe',scrollLeft=viewport.evaluate('(el)=>el.scrollLeft'))
      page.wait_for_function('''()=>{const el=document.querySelector('[data-gallery-viewport]');return el.scrollLeft>0&&Math.abs(el.scrollLeft/el.clientWidth-Math.round(el.scrollLeft/el.clientWidth))<0.003}''')
     gallery.screenshot(path=str(OUT/f'gallery-{width}.png'))
     viewport.hover();old_y=page.evaluate('scrollY');page.mouse.wheel(0,350)
     page.wait_for_function('old=>scrollY>old+50',arg=old_y)
     assert page.evaluate('document.documentElement.style.overflow')!='hidden'
     note('vertical_page_scroll_'+str(width),before=old_y,after=page.evaluate('scrollY'))
    note(product+'_'+str(width),horizontal=True,arrows=True,keyboard=True,trackpad=True,zoom=True,color_filter=alternate,matching_price=True,count=page.locator('[data-gallery-count]').inner_text(),document_width=changed['document'],frame=[changed['width'],changed['height']])
   context.close()
  browser.close()
 assert not report['errors'],report['errors']
except Exception:
 report['failure']=traceback.format_exc();print(report['failure'],flush=True)
finally:
 (OUT/'report.json').write_text(json.dumps(report,indent=2));print(str(OUT/'report.json'),flush=True)
