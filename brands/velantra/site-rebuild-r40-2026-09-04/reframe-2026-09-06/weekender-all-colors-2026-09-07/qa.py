import json
from pathlib import Path
from playwright.sync_api import sync_playwright

R = Path(__file__).resolve().parent
catalog = json.loads((R / 'catalog.json').read_text())
report = []
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for width in [1440, 390]:
        page = browser.new_page(viewport={'width':width, 'height':1000}, reduced_motion='reduce')
        for product in catalog:
            url = 'https://velantrafashion.com/products/' + product['handle'] + '?preview_theme_id=151410507841'
            page.goto(url, wait_until='domcontentloaded')
            page.locator('.product-buybox').wait_for()
            for variant in product['variants']['nodes']:
                color = variant['title']
                page.locator('.product-option__value label[title="' + color + '"]').click()
                for phase in ['switch', 'reload']:
                    if phase == 'reload':
                        page.reload(wait_until='domcontentloaded')
                        page.locator('.product-buybox').wait_for()
                    panels = page.locator('weekender-variant-details>[data-weekender-color]:visible')
                    assert panels.count() == 2
                    assert panels.evaluate_all('(els)=>els.map(e=>e.dataset.weekenderColor)') == [color.lower(), color.lower()]
                    craft = panels.first
                    value = panels.last
                    material = craft.locator('h3').first.inner_text()
                    assert material == ('Leather texture' if color == 'Black' else 'Canvas texture')
                    assert value.locator('tbody tr').first.locator('td').first.inner_text() == ('Leather body — no canvas' if color == 'Black' else 'Woven canvas body')
                    assert value.locator('tbody tr').nth(1).locator('td').first.inner_text() == 'Leather trim'
                    for panel in [craft, value]:
                        panel.locator('img').evaluate_all('(imgs)=>Promise.all(imgs.map(i=>i.decode()))')
                        assert panel.locator('img').evaluate_all('(imgs)=>imgs.every(i=>i.complete&&i.naturalWidth>0)')
                        assert all(color in alt for alt in panel.locator('img').evaluate_all('(imgs)=>imgs.map(i=>i.alt)'))
                    assert page.locator('.product-description p').count() == 1
                    assert page.locator('velantra-detail-film').count() == 0
                    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
                    assert 'Liquid error' not in page.locator('body').inner_text()
                if product['handle'] == 'velantra-weekender':
                    craft.screenshot(path=str(R / f'{color.lower().replace(" ","-")}-craft-{width}.png'))
                    if color == 'Black':
                        value.screenshot(path=str(R / f'black-value-{width}.png'))
                if width == 390:
                    strip = craft.locator('.craft-strip')
                    strip.focus()
                    strip.press('End')
                    assert strip.evaluate('(e)=>e.scrollLeft>0')
                report.append({'handle':product['handle'], 'width':width, 'color':color, 'switch':True, 'direct_variant_reload':True, 'passed':True})
                print(product['handle'], width, color, 'passed', flush=True)
        page.close()
    context = browser.new_context(java_script_enabled=False, viewport={'width':390, 'height':1000})
    for product in catalog:
        black = next(v for v in product['variants']['nodes'] if v['title']=='Black')
        variant_id = black['id'].split('/')[-1]
        page = context.new_page()
        page.goto('https://velantrafashion.com/products/' + product['handle'] + '?preview_theme_id=151410507841&variant=' + variant_id, wait_until='domcontentloaded')
        assert page.locator('weekender-variant-details>[data-weekender-color]:visible').evaluate_all('(els)=>els.map(e=>e.dataset.weekenderColor)') == ['black','black']
        report.append({'handle':product['handle'],'javascript':False,'color':'Black','passed':True})
        page.close()
    context.close()
    page = browser.new_page()
    page.goto('https://velantrafashion.com/products/velantra-margot-tote?preview_theme_id=151410507841', wait_until='domcontentloaded')
    assert page.locator('weekender-variant-details').count() == 0
    assert page.locator('.craft-card').count() == 4
    assert page.locator('[data-material-fact]').inner_text() == 'Pebbled leather'
    report.append({'handle':'velantra-margot-tote','shared_section_regression':True,'passed':True})
    browser.close()
(R / 'qa.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS',len(report),flush=True)
