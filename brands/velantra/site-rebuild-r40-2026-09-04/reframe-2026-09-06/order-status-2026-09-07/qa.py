import json
from pathlib import Path
from playwright.sync_api import sync_playwright

R = Path(__file__).resolve().parent
products = json.loads((R / 'before.json').read_text())['data']['products']['nodes']
report = []
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for width in [1440, 390]:
        page = browser.new_page(viewport={'width': width, 'height': 1000}, reduced_motion='reduce')
        for product in products:
            handle = product['handle']
            page.goto('https://velantrafashion.com/products/' + handle + '?preview_theme_id=151410507841', wait_until='domcontentloaded')
            page.locator('.product-buybox').wait_for()
            labels = page.locator('.product-option__value label')
            states = range(labels.count()) if handle in ['velantra-weekender', 'the-eleanor-weekender', 'velantra-margot-tote', 'the-colette-wool-tote', 'velantra-vivienne'] else [None]
            for index in states:
                if index is not None:
                    labels.nth(index).click()
                preorder = page.locator('[data-preorder-notice]').is_visible()
                status = page.locator('[data-order-status]')
                disabled = page.locator('.product-form__submit').is_disabled()
                assert status.is_visible() == (not preorder and not disabled), handle
                if status.is_visible():
                    assert 'orders open' in status.inner_text().lower(), handle
                    assert '10 days before dispatch' in status.inner_text().lower(), handle
                if handle in ['the-colette-wool-tote', 'velantra-vivienne']:
                    assert preorder and 'october 2026' in page.locator('[data-preorder-notice]').inner_text().lower(), handle
                if handle == 'velantra-margot-tote':
                    assert page.locator('[data-material-fact]').inner_text() == 'Pebbled leather'
            assert page.locator('.product-description p').count() == 1, handle
            assert page.locator('velantra-detail-film').count() == 0, handle
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), handle
            assert 'final orders' not in page.locator('.product-buybox').inner_text().lower()
            report.append({'handle': handle, 'width': width, 'passed': True})
            if handle in ['velantra-margot-tote', 'velantra-vivienne']:
                page.locator('.product-buybox').screenshot(path=str(R / f'{handle}-{width}.png'))
            print(handle, width, 'passed', flush=True)
        page.close()
    browser.close()
(R / 'qa.json').write_text(json.dumps(report, indent=2) + '\n')
print('PASS', len(report), flush=True)
