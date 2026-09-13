from pathlib import Path
from playwright.sync_api import sync_playwright
import json,sys,traceback
OUT=Path(__file__).resolve().parent
HANDLES={'weekender':'velantra-weekender','meridian':'velantra-margot-tote','camille':'velantra-boat-tote-2','colette':'the-colette-wool-tote','delphine':'velantra-delphine','juliette':'velantra-juliette'}
families=sys.argv[1:]
if not families:raise SystemExit('Pass one or more deployed family names.')
report={'theme_id':151364960321,'families':families,'rows':[],'failures':[]}
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True)
 for width in [1440,390]:
  context=browser.new_context(viewport={'width':width,'height':1000},device_scale_factor=1)
  page=context.new_page();page.goto('https://velantrafashion.com/?preview_theme_id=151364960321',wait_until='domcontentloaded')
  for family in families:
   try:
    errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto('https://velantrafashion.com/products/'+HANDLES[family],wait_until='domcontentloaded');page.wait_for_selector('[data-commerce-ready]');film=page.locator('velantra-detail-film');assert film.count()==1
    film.scroll_into_view_if_needed();page.wait_for_function('()=>{const v=document.querySelector("velantra-detail-film video");return v&&v.readyState>=2&&v.currentTime>0&&!v.paused}',timeout=90000)
    video=film.locator('video');state=video.evaluate('(v)=>({src:v.currentSrc,duration:v.duration,native:[v.videoWidth,v.videoHeight],box:[v.getBoundingClientRect().width,v.getBoundingClientRect().height],muted:v.muted,loop:v.loop,position:getComputedStyle(v).objectPosition,fit:getComputedStyle(v).objectFit})')
    delivery=json.loads((OUT.parent/'video/pdp-handbags-followup-2026-09-05'/family/'delivery.json').read_text());expected_duration=delivery['video_duration_seconds']
    assert abs(state['duration']-expected_duration)<.1;assert state['native']==[1920,1080];assert state['muted'] and state['loop'];assert state['fit']=='cover'
    expected_height=width*(750/1434 if width>=1024 else (360 if family=='weekender' else 420)/390);assert abs(state['box'][1]-expected_height)<1
    button=film.locator('button.detail-film-toggle');button.click();page.wait_for_function('document.querySelector("velantra-detail-film video").paused');page.wait_for_function("document.querySelector('.detail-film-toggle').getAttribute('aria-label')==='Play film'")
    button.click();page.wait_for_function('!document.querySelector("velantra-detail-film video").paused');page.wait_for_function("document.querySelector('.detail-film-toggle').getAttribute('aria-label')==='Pause film'");button.click()
    samples=[.6,2.5,4.6,6.5,8.3,10.1,12.1,14.1,state['duration']-1] if state['duration']>=14 else [.6,2.5,4.6,6.5,state['duration']-1]
    for i,t in enumerate(samples):
     if t>=state['duration']:continue
     video.evaluate('(v,t)=>v.currentTime=t',t);page.wait_for_function('(t)=>{const v=document.querySelector("velantra-detail-film video");return !v.seeking&&Math.abs(v.currentTime-t)<.15}',arg=t,timeout=30000);film.screenshot(path=str(OUT/f'pdp-film-{family}-{width}-{i:02d}.png'))
    assert not page.evaluate('document.documentElement.scrollWidth>innerWidth');assert not errors
    report['rows'].append({'family':family,'width':width,'passed':True,'film':state,'samples':samples,'controls':True,'page_errors':errors});print(json.dumps(report['rows'][-1]),flush=True)
   except Exception:
    report['failures'].append({'family':family,'width':width,'error':traceback.format_exc()});print(json.dumps(report['failures'][-1]),flush=True)
   (OUT/('pdp-film-native-qa-'+'-'.join(families)+'.json')).write_text(json.dumps(report,indent=2)+'\n')
  context.close()
 context=browser.new_context(viewport={'width':390,'height':1000},reduced_motion='reduce');page=context.new_page();page.goto('https://velantrafashion.com/?preview_theme_id=151364960321',wait_until='domcontentloaded')
 for family in families:
  try:
   page.goto('https://velantrafashion.com/products/'+HANDLES[family],wait_until='domcontentloaded');film=page.locator('velantra-detail-film');film.scroll_into_view_if_needed();page.wait_for_timeout(800);assert film.locator('video').evaluate('(v)=>v.paused');film.locator('.detail-film-toggle').click();page.wait_for_function('()=>{const v=document.querySelector("velantra-detail-film video");return !v.paused&&v.currentTime>0}',timeout=60000);report.setdefault('reduced_motion',[]).append({'family':family,'autoplay_off':True,'manual_play':True})
  except Exception:report['failures'].append({'family':family,'check':'reduced_motion','error':traceback.format_exc()})
 context.close();browser.close()
report['passed']=len(report['rows'])==len(families)*2 and not report['failures']
(OUT/('pdp-film-native-qa-'+'-'.join(families)+'.json')).write_text(json.dumps(report,indent=2)+'\n')
