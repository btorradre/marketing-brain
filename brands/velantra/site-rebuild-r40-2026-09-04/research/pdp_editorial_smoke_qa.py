import json,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright
OUT=Path(__file__).resolve().parent
URL='https://velantrafashion.com'
PRODUCTS=[('velantra-vivienne','VIVIENNE'),('velantra-weekender','ELEANOR'),('the-eleanor-weekender','ELEANOR'),('velantra-margot-tote','MERIDIAN'),('velantra-boat-tote-2','CAMILLE'),('the-colette-wool-tote','COLETTE'),('velantra-delphine','DELPHINE'),('velantra-juliette','JULIETTE')]
report={'theme_id':151364960321,'rows':[],'failures':[]}
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True)
 for width in [1440,390]:
  context=browser.new_context(viewport={'width':width,'height':1000},device_scale_factor=1)
  page=context.new_page();page.goto(URL+'/?preview_theme_id=151364960321',wait_until='domcontentloaded')
  for handle,title in PRODUCTS:
   errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
   try:
    response=page.goto(URL+'/products/'+handle,wait_until='domcontentloaded');page.wait_for_selector('[data-commerce-ready]');page.evaluate('document.fonts.ready')
    for frame in page.frames:
     if frame.name=='PBarNextFrame':
      try:frame.get_by_role('button',name='Hide bar',exact=True).click(timeout=1500)
      except Exception:pass
    assert page.locator('h1').inner_text()==title
    assert response.status==200
    assert 'Liquid error' not in page.content()
    assert 'translation missing' not in page.content().lower()
    timeline=page.locator('.craft-timeline');assert timeline.count()==1
    assert timeline.locator('.craft-card').count()==4
    assert timeline.locator('h2').inner_text()=='THE RHYTHM OF MAKING'
    for image in timeline.locator('img').all():image.scroll_into_view_if_needed()
    page.wait_for_function('()=>Array.from(document.querySelectorAll(".craft-media img")).every(i=>i.complete&&i.naturalWidth>0)',timeout=45000)
    value=page.locator('.value-breakdown');value.scroll_into_view_if_needed()
    page.wait_for_function('()=>Array.from(document.querySelectorAll(".value-breakdown img")).every(i=>i.complete&&i.naturalWidth>0)',timeout=45000)
    assert value.locator('tbody tr').count()==6
    perspectives=page.locator('.client-perspectives');perspectives.scroll_into_view_if_needed()
    assert perspectives.count()==1
    assert perspectives.locator('h2').inner_text()=='Client Perspectives'
    assert 'Customer reviews are not available here yet.' in perspectives.inner_text()
    film=page.locator('velantra-detail-film')
    if handle=='velantra-vivienne':
     assert film.count()==1;film.scroll_into_view_if_needed()
     page.wait_for_function('()=>{const v=document.querySelector("velantra-detail-film video");return v&&v.readyState>=2&&v.currentTime>0}',timeout=90000)
     assert 'One hide, one finish' not in page.locator('.product-description').inner_text()
     assert 'October' in page.locator('.product-description').inner_text()
     page.screenshot(path=str(OUT/f'pdp-editorial-vivienne-film-{width}.png'))
    variant_id=page.locator('[data-variant-select]').input_value()
    selected=next(v for v in json.loads(page.locator('[data-product-variants]').text_content()) if str(v['id'])==variant_id)
    if selected['price']==0 or not selected['available']:assert page.locator('[data-add-button]').is_disabled()
    assert 'Free shipping over $75' in page.locator('.product-tax-note').text_content()
    assert page.locator('.product-tax-note a').count()==0
    assert not page.evaluate('document.documentElement.scrollWidth>innerWidth')
    labels=page.locator('[data-color-option] label')
    if labels.count()>1:
     last=labels.last;last.click();chosen=last.get_attribute('title')
     page.wait_for_function('(name)=>document.querySelector("[data-selected-option]").textContent===name',arg=chosen)
     new_id=page.locator('[data-variant-select]').input_value()
     new_variant=next(v for v in json.loads(page.locator('[data-product-variants]').text_content()) if str(v['id'])==new_id)
     assert str(new_variant['featured_media_id'])==page.locator('[data-first-visible]').get_attribute('data-media-id')
     assert page.locator('[data-media-id]:visible').count()>0
     if new_variant['price']==0 or not new_variant['available']:assert page.locator('[data-add-button]').is_disabled()
    details=page.locator('.product-accordion').first
    if details.count():
     summary=details.locator('summary');summary.click();assert details.get_attribute('open') is not None;summary.click();assert details.get_attribute('open') is None
    craft_images=timeline.locator('img').evaluate_all('(els)=>els.map(i=>({src:i.currentSrc,alt:i.alt,w:i.naturalWidth,h:i.naturalHeight}))')
    order=page.locator('#MainContent>.shopify-section').evaluate_all('(els)=>els.map(e=>e.id)')
    row={'handle':handle,'width':width,'title':title,'passed':True,'craft_images':craft_images,'film_count':film.count(),'selected_price':selected['price'],'purchase_disabled':page.locator('[data-add-button]').is_disabled(),'section_order':order,'page_errors':errors}
    report['rows'].append(row)
    if handle in ['velantra-vivienne','the-colette-wool-tote']:
     timeline.scroll_into_view_if_needed();timeline.locator('.craft-strip').focus();timeline.locator('.craft-strip').press('Home');page.wait_for_timeout(250);timeline.screenshot(path=str(OUT/f'pdp-editorial-{handle}-craft-{width}.png'))
     value.scroll_into_view_if_needed();value.screenshot(path=str(OUT/f'pdp-editorial-{handle}-value-{width}.png'))
     perspectives.scroll_into_view_if_needed();perspectives.screenshot(path=str(OUT/f'pdp-editorial-{handle}-reviews-{width}.png'))
    print(json.dumps({'handle':handle,'width':width,'passed':True,'films':film.count(),'page_errors':errors}),flush=True)
   except Exception:
    failure={'handle':handle,'width':width,'error':traceback.format_exc()};report['failures'].append(failure);print(json.dumps(failure),flush=True)
   (OUT/'pdp-editorial-smoke-qa.json').write_text(json.dumps(report,indent=2)+'\n')
  context.close()
 browser.close()
report['passed']=len(report['rows'])==16 and not report['failures']
(OUT/'pdp-editorial-smoke-qa.json').write_text(json.dumps(report,indent=2)+'\n')
