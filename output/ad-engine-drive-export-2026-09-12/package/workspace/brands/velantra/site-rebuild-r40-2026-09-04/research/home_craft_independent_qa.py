import json
from pathlib import Path
from playwright.sync_api import sync_playwright
OUT=Path(__file__).resolve().parent
URL='https://velantrafashion.com/?preview_theme_id=151364960321'
report={'theme_id':151364960321,'viewports':[],'issues':[]}
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True)
 for width in (1440,390):
  context=browser.new_context(viewport={'width':width,'height':1000},device_scale_factor=1)
  page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  response=page.goto(URL,wait_until='domcontentloaded');page.locator('velantra-detail-film').wait_for();page.evaluate('document.fonts.ready')
  film=page.locator('velantra-detail-film');film.scroll_into_view_if_needed()
  page.wait_for_function('()=>{const v=document.querySelector("velantra-detail-film video");return v&&v.readyState>=2&&v.currentTime>0}',timeout=90000)
  state=film.evaluate('(e)=>{const v=e.querySelector("video");const r=e.getBoundingClientRect();return {duration:v.duration,source:v.currentSrc,native:[v.videoWidth,v.videoHeight],box:[r.width,r.height],position:getComputedStyle(v).objectPosition,fit:getComputedStyle(v).objectFit,paused:v.paused}}')
  page.locator('.detail-film-toggle').click()
  for n,t in enumerate([.6,2.4,4.2,6.2,8.4,10.5,12.5,14.5,16.8,19.7,21.2]):
   if t>=state['duration']:continue
   film.locator('video').evaluate('(v,t)=>v.currentTime=t',t)
   page.wait_for_function('(t)=>{const v=document.querySelector("velantra-detail-film video");return !v.seeking&&Math.abs(v.currentTime-t)<.15}',arg=t,timeout=30000)
   film.screenshot(path=str(OUT/f'home-independent-film-{width}-{n:02d}.png'))
  timeline=page.locator('.craft-timeline');timeline.scroll_into_view_if_needed()
  imgs=timeline.locator('img')
  for i in range(imgs.count()):imgs.nth(i).scroll_into_view_if_needed()
  timeline.scroll_into_view_if_needed();page.wait_for_function('()=>Array.from(document.querySelectorAll(".craft-media img")).every(i=>i.complete&&i.naturalWidth>0)',timeout=30000)
  timeline.screenshot(path=str(OUT/f'home-independent-timeline-{width}.png'))
  value=page.locator('.value-breakdown');value.scroll_into_view_if_needed();value.locator('img').wait_for();page.wait_for_function('()=>Array.from(document.querySelectorAll(".value-breakdown img")).every(i=>i.complete&&i.naturalWidth>0)',timeout=30000)
  value.screenshot(path=str(OUT/f'home-independent-value-{width}.png'))
  entry={'width':width,'http_status':response.status,'film':state,'craft_images':imgs.count(),'timeline_headings':timeline.locator('h2,h3').all_text_contents(),'value_rows':value.locator('tbody tr').count(),'overflow':page.evaluate('document.documentElement.scrollWidth>innerWidth'),'page_errors':errors}
  report['viewports'].append(entry);(OUT/'home-craft-independent-qa.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(entry),flush=True)
  context.close()
 browser.close()
