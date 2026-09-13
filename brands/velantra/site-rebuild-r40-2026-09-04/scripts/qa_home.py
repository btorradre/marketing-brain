from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parents[1]; URL='https://velantrafashion.com/?preview_theme_id=151337074753'
results=[];errors=[]
with sync_playwright() as p:
 b=p.chromium.launch(headless=True)
 context=b.new_context(viewport={'width':1440,'height':1000});page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)));page.goto(URL,wait_until='domcontentloaded');page.wait_for_timeout(1500)
 def check(name):
  d=page.evaluate('''()=>({url:location.href,width:innerWidth,scrollWidth:document.documentElement.scrollWidth,brokenImages:[...document.querySelectorAll('img')].filter(i=>i.complete&&!i.naturalWidth).map(i=>i.src),font:getComputedStyle(document.body).fontFamily,headingFont:getComputedStyle(document.querySelector('h2')).fontFamily,videos:[...document.querySelectorAll('video')].map(v=>({src:v.currentSrc,muted:v.muted,paused:v.paused,ready:v.readyState})),emptyLinks:[...document.querySelectorAll('a[href]')].filter(a=>a.getAttribute('href')==='').map(a=>a.innerText)})''');d['name']=name;d['liquid_errors']='Liquid error' in page.content();assert not d['liquid_errors'];assert not d['brokenImages'];assert d['width']==d['scrollWidth'];assert not d['emptyLinks'];results.append(d)
 check('desktop_home')
 page.locator('[data-dialog-open="SearchDialog"]').click();assert page.locator('#SearchDialog').is_visible();page.locator('#HeaderSearch').fill('Vivienne');page.keyboard.press('Escape');page.locator('#SearchDialog').wait_for(state='hidden',timeout=3000);results.append({'name':'search_dialog_keyboard','pass':True})
 page.locator('.nav-dropdown summary').click();assert page.locator('.nav-flyout').is_visible();page.locator('.nav-dropdown summary').click();results.append({'name':'collection_dropdown','pass':True})
 page.locator('[data-dialog-open="LocaleDialog"]').filter(visible=True).click();assert page.locator('#Country option').count()>1;page.keyboard.press('Escape');results.append({'name':'region_dialog','countries':page.locator('#Country option').count()})
 page.locator('[data-video-toggle]').click();assert page.locator('.hero-video').evaluate('(v)=>v.paused');page.locator('[data-video-toggle]').click();results.append({'name':'video_pause_play','pass':True})
 page.set_viewport_size({'width':900,'height':1000});page.reload(wait_until='domcontentloaded');page.locator('.mobile-menu').click();assert page.locator('#NavigationDrawer').is_visible();assert page.locator('#NavigationDrawer').get_by_role('link',name='Search',exact=True).is_visible();page.keyboard.press('Escape');check('tablet_home_navigation')
 page.set_viewport_size({'width':390,'height':844});page.reload(wait_until='domcontentloaded');page.wait_for_timeout(600);check('mobile_home');page.locator('.mobile-menu').click();assert page.locator('#NavigationDrawer').is_visible();page.keyboard.press('Escape');assert page.locator('.mobile-menu').evaluate('(e)=>e===document.activeElement');results.append({'name':'mobile_menu_focus','pass':True})
 context2=b.new_context(viewport={'width':390,'height':844},reduced_motion='reduce');reduced=context2.new_page();reduced.goto(URL,wait_until='domcontentloaded');reduced.wait_for_timeout(800);paused=reduced.locator('video').evaluate_all('(vs)=>vs.every(v=>v.paused)');assert paused;results.append({'name':'reduced_motion','all_videos_paused':paused});b.close()
(R/'research/home-preview-qa.json').write_text(json.dumps({'checks':results,'page_errors':errors,'passed':not errors},indent=2));print('Home QA checks',len(results),'page errors',errors)
