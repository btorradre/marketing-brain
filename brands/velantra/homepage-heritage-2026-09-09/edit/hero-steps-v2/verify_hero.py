import json
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parent
rows = []
with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=True)
    for width, height in [(1440, 1000), (768, 1024), (390, 844)]:
        page = browser.new_page(viewport={'width': width, 'height': height})
        page.goto('https://velantrafashion.com/?preview_theme_id=151519330369', wait_until='load')
        hero = page.locator('.heritage-campaign--hero')
        expect(hero.locator('h1')).to_have_text('A Life Well Carried')
        photo = hero.locator('img')
        page.wait_for_function('(e)=>e.complete && e.naturalWidth>0', arg=photo.element_handle())
        details = photo.evaluate('(e)=>({source:e.currentSrc,width:e.naturalWidth,height:e.naturalHeight})')
        assert 'vivienne-steps-v2' in details['source']
        assert ('mobile' in details['source']) == (width < 768)
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
        expect(hero.get_by_role('link', name='Shop Handbags', exact=True)).to_be_visible()
        expect(hero.get_by_role('link', name='Discover the Vivienne', exact=True)).to_have_attribute('href', '/products/velantra-vivienne?variant=44462686830657')
        page.screenshot(path=str(ROOT / f'homepage-hero-{width}.png'), style='#PBarNextFrame,#preview-bar-iframe{display:none!important}')
        rows.append({'viewport': [width, height], 'image': details, 'overflow': False, 'copy_and_links': 'pass'})
        page.close()
    browser.close()
(ROOT / 'browser-qa.json').write_text(json.dumps(rows, indent=2))
print('PASS: new hero images, headline, links and overflow at desktop, tablet and mobile')
