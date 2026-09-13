import json, time
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT=Path(__file__).resolve().parent
URL='https://velantrafashion.com/?preview_theme_id=151364960321'
report={'passed':False,'viewports':[]}
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True)
 for width in (1440,390):
  context=browser.new_context(viewport={'width':width,'height':900},device_scale_factor=1)
  page=context.new_page(); errors=[];page.on('pageerror',lambda error:errors.append(str(error)))
  page.goto(URL,wait_until='domcontentloaded');page.locator('velantra-detail-film').wait_for()
  page.evaluate('document.fonts.ready');page.wait_for_timeout(500)
  assert page.locator('h2',has_text='THE EVERYDAY COLLECTION').count()==0
  assert page.locator('h2',has_text='THE SIGNATURE COLLECTION').count()==1
  assert page.locator('.craft-card').count()==4
  assert page.locator('.craft-day').all_text_contents()[:2]==['Day 1','Day 4–8']
  order=page.locator('#MainContent > .shopify-section').evaluate_all('(els)=>els.map(el=>el.id)')
  film_index=next(i for i,x in enumerate(order) if x.endswith('__macro'))
  assert order[film_index+1].endswith('__craftsmanship'),order
  video=page.locator('velantra-detail-film video')
  video.scroll_into_view_if_needed()
  page.wait_for_function('()=>{const v=document.querySelector("velantra-detail-film video");return v.readyState>=2 && v.currentTime>0 && !v.paused}',timeout=90000)
  state=video.evaluate('(v)=>({duration:v.duration,width:v.videoWidth,height:v.videoHeight,src:v.currentSrc,muted:v.muted,loop:v.loop})')
  assert state['duration']>=18,state
  assert state['muted'] and state['loop']
  toggle=page.locator('.detail-film-toggle');toggle.click();page.wait_for_function('document.querySelector("velantra-detail-film video").paused')
  page.wait_for_function("document.querySelector('.detail-film-toggle').getAttribute('aria-label')==='Play film'")
  toggle.click();page.wait_for_function('!document.querySelector("velantra-detail-film video").paused')
  page.wait_for_function("document.querySelector('.detail-film-toggle').getAttribute('aria-label')==='Pause film'")
  video.screenshot(path=str(OUT/f'vivienne-detail-film-{width}.png'))
  page.locator('.craft-timeline').scroll_into_view_if_needed()
  page.wait_for_function('()=>Array.from(document.querySelectorAll(".craft-media img")).every(i=>i.complete&&i.naturalWidth>0)',timeout=45000)
  page.locator('.craft-timeline').screenshot(path=str(OUT/f'vivienne-leather-timeline-{width}.png'))
  strip=page.locator('.craft-strip')
  geom=strip.evaluate('(e)=>({width:e.clientWidth,scrollWidth:e.scrollWidth})')
  if width<1024:
   assert geom['scrollWidth']>geom['width']
   strip.focus();strip.press('End');page.wait_for_timeout(350)
   assert strip.evaluate('(e)=>e.scrollLeft')>0
   page.locator('.craft-timeline').screenshot(path=str(OUT/f'vivienne-leather-timeline-{width}-last.png'))
  else:assert geom['scrollWidth']<=geom['width']+1
  page.locator('.value-breakdown').scroll_into_view_if_needed()
  page.locator('.value-breakdown').screenshot(path=str(OUT/f'vivienne-value-details-{width}.png'))
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'), 'Page overflow'
  assert not errors,errors
  report['viewports'].append({'width':width,'single_collection':True,'film':state,'controls':True,'timeline_after_film':True,'timeline_scroll':geom,'page_errors':errors,'no_overflow':True,'section_order':order})
  context.close()
 context=browser.new_context(viewport={'width':390,'height':900},reduced_motion='reduce')
 page=context.new_page();page.goto(URL,wait_until='domcontentloaded');video=page.locator('velantra-detail-film video');video.scroll_into_view_if_needed();page.wait_for_timeout(1000)
 assert video.evaluate('(v)=>v.paused')
 page.locator('.detail-film-toggle').click();page.wait_for_function('()=>{const v=document.querySelector("velantra-detail-film video");return !v.paused&&v.currentTime>0}',timeout=45000)
 report['reduced_motion']={'autoplay_disabled':True,'manual_play_works':True}
 context.close();browser.close()
report['passed']=True
(OUT/'home-detail-followup-qa.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
