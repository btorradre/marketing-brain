from pathlib import Path
from playwright.sync_api import sync_playwright
import json
O=Path(__file__).resolve().parent;A=O.parent.parent/'assets/images-v9'
with sync_playwright() as p:
 b=p.chromium.launch(headless=True)
 page=b.new_page(viewport={'width':850,'height':1700},device_scale_factor=2)
 page.goto('https://pmc.ncbi.nlm.nih.gov/articles/PMC6152273/',wait_until='networkidle',timeout=60000)
 h=page.get_by_role('heading',name='Apigenin Impacts the Growth of the Gut Microbiota and Alters the Gene Expression of Enterococcus',exact=True)
 box=h.bounding_box();print('TITLE',box)
 page.evaluate('(y)=>window.scrollTo(0,y)',max(0,box['y']-140))
 page.screenshot(path=str(A/'apigenin-research-page.png'))
 (O/'article-visible-text.txt').write_text(page.locator('body').inner_text())
 (O/'screenshot-provenance.json').write_text(json.dumps({'url':page.url,'title':page.title(),'viewport':[850,1700],'device_scale_factor':2,'scrollY':page.evaluate('window.scrollY'),'method':'Actual Chromium screenshot of the public PMC article; no altered page text or styling','study_type':'In vitro microbiota study','capture':'assets/images-v9/apigenin-research-page.png'},indent=2))
 b.close()
