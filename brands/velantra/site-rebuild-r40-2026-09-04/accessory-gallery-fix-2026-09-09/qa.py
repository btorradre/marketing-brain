import json
from pathlib import Path
import requests
from playwright.sync_api import sync_playwright, expect

OUT = Path(__file__).resolve().parent
BASE = 'https://velantrafashion.com'
ACCESSORIES = ['velantra-horse-charm', 'velantra-cherry-charm', 'bag-scarf', 'boat-tote-keychain']
products = requests.get(BASE + '/products.json?limit=250').json()['products']
report = {'catalog': [], 'galleries': [], 'cart': []}

with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=True)
    for width in [1440, 390]:
        context = browser.new_context(viewport={'width': width, 'height': 1000 if width == 1440 else 844}, reduced_motion='reduce')
        page = context.new_page()
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        for product in products:
            handle = product['handle']
            page.goto(BASE + '/products/' + handle, wait_until='domcontentloaded')
            quantity = page.locator('[data-product-quantity] input')
            expect(quantity).to_be_visible()
            expect(quantity).to_have_value('1')
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), handle
            report['catalog'].append({'handle': handle, 'width': width, 'quantity': True, 'no_overflow': True})
            if handle not in ACCESSORIES:
                continue
            labels = page.locator('fieldset[data-color-option] label')
            count = labels.count()
            for index in range(count):
                label = labels.nth(index)
                color_name = label.get_attribute('title')
                label.click()
                expect(page.locator('fieldset[data-color-option] input:checked')).to_have_value(color_name)
                gallery = page.locator('[data-gallery]')
                expect(gallery).to_have_attribute('data-color-only', 'true')
                visible = gallery.locator('[data-media-id]:not([hidden])')
                assert visible.count() > 0, (handle, color_name)
                all_colors = visible.evaluate_all('(els) => els.map(e => e.dataset.color)')
                assert len(set(all_colors)) == 1 and all_colors[0], (handle, color_name, all_colors)
                selected = page.locator('form[action*="/cart/add"] [name="id"]').input_value()
                variant = next(v for v in product['variants'] if str(v['id']) == selected)
                assert variant['option1'] == color_name
                featured_id = str(variant['featured_image']['id'])
                urls = visible.locator('img').evaluate_all('(els) => els.map(e => e.currentSrc || e.src)')
                assert any(featured_id in url for url in urls), (handle, color_name, featured_id, urls)
                assert all('/r40-36065269973057-' not in u and '/r40-36093867262017-' not in u for u in urls)
                for image in visible.locator('img').all():
                    image.scroll_into_view_if_needed()
                    expect(image).to_be_visible()
                    page.wait_for_function('(img) => img.complete && img.naturalWidth > 0', arg=image.element_handle())
                report['galleries'].append({'handle': handle, 'width': width, 'color': color_name, 'media_count': visible.count(), 'colors': all_colors, 'urls': urls})
            if handle in ['velantra-horse-charm', 'velantra-cherry-charm']:
                labels.nth(0).click()
                quantity.scroll_into_view_if_needed()
                page.screenshot(path=str(OUT / f'{handle}-{width}.png'), full_page=width == 390)
                visible = page.locator('[data-gallery] [data-media-id]:not([hidden])')
                visible.locator('[data-zoom-image]').click()
                expect(page.locator('[data-product-lightbox]')).to_be_visible()
                page.locator('[data-lightbox-close]').click()
                expect(page.locator('[data-product-lightbox]')).not_to_be_visible()
            print('Gallery passed', handle, width, count, flush=True)

        page.goto(BASE + '/products/velantra-horse-charm', wait_until='domcontentloaded')
        quantity = page.locator('[data-product-quantity] input')
        more = page.get_by_role('button', name='Increase quantity', exact=True)
        less = page.get_by_role('button', name='Decrease quantity', exact=True)
        more.click()
        expect(quantity).to_have_value('2')
        less.click()
        less.click()
        expect(quantity).to_have_value('1')
        quantity.fill('3')
        quantity.press('Tab')
        expect(quantity).to_have_value('3')
        quantity.fill('0')
        quantity.press('Tab')
        expect(quantity).to_have_value('1')
        more.click()
        page.locator('fieldset[data-color-option] label[title="Dark Brown"]').click()
        expect(quantity).to_have_value('2')
        form = page.locator('form[action*="/cart/add"]')
        selected = form.locator('[name="id"]').input_value()
        with page.expect_response(lambda r: '/cart/add' in r.url and r.request.method == 'POST') as response:
            form.locator('[name="add"]').click()
        assert response.value.ok
        cart = context.request.get(BASE + '/cart.js').json()
        item = next(i for i in cart['items'] if str(i['variant_id']) == selected)
        assert item['quantity'] == 2
        report['cart'].append({'width': width, 'variant': selected, 'quantity': item['quantity'], 'minimum': True, 'direct_entry': True, 'color_preserves_quantity': True})
        context.request.post(BASE + '/cart/clear.js')
        assert not errors, errors
        context.close()
    browser.close()

(OUT / 'browser-qa.json').write_text(json.dumps(report, indent=2))
print('PASS', len(report['catalog']), 'product pages;', len(report['galleries']), 'accessory color checks;', len(report['cart']), 'cart checks')
