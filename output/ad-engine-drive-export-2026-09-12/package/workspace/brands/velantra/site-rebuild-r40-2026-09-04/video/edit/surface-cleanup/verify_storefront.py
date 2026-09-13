"""Verify uploaded handbag films in the unpublished Shopify storefront."""
import asyncio,json,sys,traceback
from urllib.parse import urlsplit
from pathlib import Path
from playwright.async_api import async_playwright

ROOT=Path(__file__).resolve().parent
THEME=int(sys.argv[1])
OUT=ROOT/f'qa/revision-2/film-storefront-{THEME}';OUT.mkdir(exist_ok=True)
ITEMS=[('home','vivienne','/'),('vivienne','vivienne','/products/velantra-vivienne'),('weekender','weekender','/products/velantra-weekender'),('eleanor','weekender','/products/the-eleanor-weekender'),('meridian','meridian','/products/velantra-margot-tote'),('camille','camille','/products/velantra-boat-tote-2'),('colette','colette','/products/the-colette-wool-tote'),('delphine','delphine','/products/velantra-delphine'),('juliette','juliette','/products/velantra-juliette')]
UPLOADS={r['family']:r for r in json.loads((ROOT/'shopify/uploaded-files.json').read_text())['uploaded']}
report={'theme_id':THEME,'rows':[],'failures':[]}
def save():
 (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')

async def main():
 async with async_playwright() as p:
  browser=await p.chromium.launch(headless=True)
  gate=asyncio.Semaphore(3)
  async def check(item,width):
   async with gate:
    name,family,path=item
    context=await browser.new_context(viewport={'width':width,'height':1000},device_scale_factor=1)
    page=await context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    try:
     await page.goto(f'https://velantrafashion.com{path}?preview_theme_id={THEME}',wait_until='domcontentloaded')
     await page.wait_for_selector('velantra-detail-film')
     assert await page.evaluate('Shopify.theme.id')==THEME,'Wrong theme in preview'
     film=page.locator('velantra-detail-film');assert await film.count()==1
     await film.scroll_into_view_if_needed()
     await page.wait_for_function('()=>{const v=document.querySelector("velantra-detail-film video");return v&&v.readyState>=2&&v.currentTime>0&&!v.paused}',timeout=60000)
     video=film.locator('video')
     state=await video.evaluate('(v)=>({src:v.currentSrc,duration:v.duration,native:[v.videoWidth,v.videoHeight],box:[v.getBoundingClientRect().width,v.getBoundingClientRect().height],muted:v.muted,loop:v.loop,position:getComputedStyle(v).objectPosition,fit:getComputedStyle(v).objectFit})')
     delivery=UPLOADS[family]['video'];expected=delivery['duration']/1000
     assert abs(state['duration']-expected)<.1
     def media_path(url):return urlsplit(url).path.split('/videos/',1)[-1]
     assert media_path(state['src']) in [media_path(s['url']) for s in delivery['sources']],state['src']
     assert state['native']==[1920,1080] and state['muted'] and state['loop']
     button=film.locator('.detail-film-toggle');await button.click()
     await page.wait_for_function('()=>{const f=document.querySelector("velantra-detail-film");return f.querySelector("video").paused&&f.querySelector(".detail-film-toggle").getAttribute("aria-label")==="Play film"}')
     await button.click()
     await page.wait_for_function('()=>{const f=document.querySelector("velantra-detail-film");return !f.querySelector("video").paused&&f.querySelector(".detail-film-toggle").getAttribute("aria-label")==="Pause film"}')
     await button.click()
     timestamps={'vivienne':[4.54,11.29,19.29],'weekender':[8.9167,15.0],'meridian':[4.46,10.0],'camille':[6.4,15.0],'colette':[6,15.0],'delphine':[4.5,7.5],'juliette':[3,6.25]}[family]
     timestamps=[.5]+timestamps
     if width<500:timestamps=timestamps[:2]
     for i,t in enumerate(timestamps):
      await video.evaluate('(v,t)=>v.currentTime=t',t)
      await page.wait_for_function('(t)=>{const v=document.querySelector("velantra-detail-film video");return !v.seeking&&Math.abs(v.currentTime-t)<.1}',arg=t,timeout=30000)
      await film.screenshot(path=str(OUT/f'{name}-{width}-{i}.png'))
     assert not await page.evaluate('document.documentElement.scrollWidth>innerWidth')
     row={'page':name,'family':family,'width':width,'passed':True,'film':state,'controls':True,'page_errors':errors}
     report['rows'].append(row);print(json.dumps({'page':name,'width':width,'passed':True}),flush=True)
    except Exception:
     report['failures'].append({'page':name,'width':width,'error':traceback.format_exc()});print(json.dumps(report['failures'][-1]),flush=True)
    finally:
     save();await context.close()
  await asyncio.gather(*(check(item,w) for item in ITEMS for w in [1440,390]))
  await browser.close()
 report['passed']=len(report['rows'])==18 and not report['failures'];save()
 if not report['passed']:raise SystemExit(1)

asyncio.run(main())
