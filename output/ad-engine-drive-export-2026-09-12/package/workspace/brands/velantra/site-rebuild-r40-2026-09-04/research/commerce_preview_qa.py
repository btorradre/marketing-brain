from pathlib import Path
import json,re,traceback
from playwright.sync_api import sync_playwright
BASE='https://velantrafashion.com'
THEME='151337074753'
OUT=Path(__file__).parent
report={'checks':[],'page_errors':[]}
def note(name,**data):
    report['checks'].append({'name':name,**data})
    print(json.dumps(report['checks'][-1]),flush=True)
def inspect(page,name):
    html=page.content()
    failures=re.findall(r'Liquid (?:error|syntax error)[^<\n]*',html)
    missing=re.findall(r'Translation missing[^<\n]*',html,re.I)
    metrics=page.evaluate('''() => ({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,font:getComputedStyle(document.body).fontFamily,headingFont:getComputedStyle(document.querySelector('h1')).fontFamily,brokenImages:[...document.images].filter(i=>i.complete&&i.naturalWidth===0&&i.currentSrc).map(i=>i.currentSrc)})''')
    note(name,liquid_errors=failures,translations_missing=missing,**metrics)
    assert not failures, failures
    assert not missing, missing
    assert metrics['scrollWidth'] <= metrics['width']+1, metrics

def product(page,handle):
    page.goto(f'{BASE}/products/{handle}?preview_theme_id={THEME}',wait_until='domcontentloaded')
    page.wait_for_selector('[data-product-section][data-commerce-ready="true"]')
    page.evaluate('document.fonts.ready')
def color(page,name):
    page.locator(f'[data-option-picker] label[title="{name}"]').click()
    page.wait_for_function('(color)=>document.querySelector("[data-selected-option]").textContent===color',arg=name)

def add(page):
    page.locator('[data-add-button]').click()
    page.wait_for_selector('#CartDrawer[open]')
    page.locator('#CartDrawer .drawer-line').wait_for()

try:
  with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    ctx=browser.new_context(viewport={'width':1440,'height':1100})
    page=ctx.new_page()
    page.on('pageerror',lambda e:report['page_errors'].append(str(e)))
    product(page,'velantra-vivienne')
    inspect(page,'desktop_vivienne')
    assert '<span' not in page.locator('[data-product-price]').inner_text()
    assert '149.99' in page.locator('[data-product-price]').inner_text()
    color(page,'Cognac')
    cognac=page.locator('[data-variant-select]').input_value()
    gallery=page.locator('[data-media-id]:visible').evaluate_all('(items)=>items.map(x=>x.dataset.color)')
    assert set(gallery)=={'cognac'},gallery
    assert 'variant='+cognac in page.url
    note('variant_cognac',native_id=cognac,gallery=gallery,url=page.url)
    page.get_by_role('radio',name='Cognac',exact=True).focus()
    page.keyboard.press('ArrowRight')
    assert page.locator('[data-selected-option]').text_content()=='Black'
    note('keyboard_variant',selected=page.locator('[data-selected-option]').inner_text())
    color(page,'Cognac')
    page.screenshot(path=str(OUT/'commerce-preview-pdp-desktop.png'),full_page=False)
    add(page)
    drawer=page.locator('#CartDrawer')
    assert 'Cognac' in drawer.inner_text()
    assert 'October' in drawer.inner_text()
    note('ajax_add',drawer=drawer.inner_text())
    page.screenshot(path=str(OUT/'commerce-preview-cart-drawer.png'),full_page=False)
    drawer.get_by_role('button',name='Increase quantity',exact=True).click()
    page.wait_for_function('document.querySelector("[data-drawer-total]").textContent.includes("299.98")')
    note('drawer_increase',total=page.locator('[data-drawer-total]').inner_text(),focus=page.evaluate('document.activeElement.getAttribute("aria-label")'))
    drawer.get_by_role('button',name='Decrease quantity',exact=True).click()
    page.wait_for_function('document.querySelector("[data-drawer-total]").textContent.includes("149.99")')
    drawer.get_by_role('button',name='Close',exact=True).click()
    page.goto(f'{BASE}/cart',wait_until='domcontentloaded')
    inspect(page,'native_cart')
    assert 'October' in page.locator('.cart-line').inner_text()
    page.locator('input[name="updates[]"]').fill('2')
    with page.expect_navigation(wait_until='domcontentloaded'):
      page.get_by_role('button',name='Update bag',exact=True).click()
    assert '299.98' in page.locator('.cart-line__total').inner_text()
    note('native_cart_update',quantity=page.locator('input[name="updates[]"]').input_value(),line_total=page.locator('.cart-line__total').inner_text())
    with page.expect_navigation(wait_until='domcontentloaded'):
      page.locator('.cart-line').get_by_role('link',name='Remove',exact=True).click()
    assert page.locator('.cart-line').count()==0
    note('native_cart_remove',empty=True)
    product(page,'velantra-vivienne')
    add(page)
    page.locator('#CartDrawer').get_by_role('button',name='Remove',exact=True).click()
    page.wait_for_function('document.querySelectorAll("#CartDrawer .drawer-line").length===0')
    note('drawer_remove',empty=True)
    page.keyboard.press('Escape')
    product(page,'velantra-juliette')
    inspect(page,'juliette_zero_price')
    assert page.locator('[data-add-button]').is_disabled()
    assert page.locator('[data-contact-availability]').is_visible()
    color(page,'Black')
    assert page.locator('[data-add-button]').is_disabled()
    note('juliette_guard',button=page.locator('[data-add-button]').inner_text(),contact=page.locator('[data-contact-availability]').get_attribute('href'))
    product(page,'velantra-weekender')
    color(page,'Black')
    assert page.locator('[data-preorder-notice]').is_visible()
    assert 'mid September 2026' in page.locator('[data-preorder-notice]').text_content()
    assert page.locator('[data-add-button]').inner_text().strip().lower()=='pre-order'
    color(page,'Light Chocolate')
    assert not page.locator('[data-preorder-notice]').is_visible()
    assert page.locator('[data-add-button]').inner_text().strip().lower()=='add to cart'
    note('weekender_preorder',black='preorder',light_chocolate='in_stock')
    page.goto(f'{BASE}/collections/all?preview_theme_id={THEME}',wait_until='domcontentloaded')
    inspect(page,'collection')
    cards=page.locator('.product-card').count()
    assert cards>0
    page.get_by_label('Sort by',exact=True).select_option('price-ascending')
    page.wait_for_url('**sort_by=price-ascending')
    note('collection_sort',cards=cards,url=page.url)
    page.get_by_role('button',name='Search',exact=True).click()
    page.locator('#SearchDialog input[name=q]').fill('Vivienne')
    with page.expect_navigation(wait_until='domcontentloaded'):
      page.locator('#SearchDialog').get_by_role('button',name='Search →',exact=True).click()
    inspect(page,'search')
    assert page.locator('.product-card').count()>=1
    assert 'Vivienne' in page.locator('.product-card').first.inner_text()
    note('search_results',count=page.locator('.product-card').count())
    mobile=browser.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True,device_scale_factor=1)
    mp=mobile.new_page()
    mp.on('pageerror',lambda e:report['page_errors'].append(str(e)))
    product(mp,'velantra-vivienne')
    inspect(mp,'mobile_vivienne')
    mp.screenshot(path=str(OUT/'commerce-preview-pdp-mobile.png'),full_page=False)
    mp.locator('[data-gallery-next]').click()
    mp.wait_for_function('document.querySelector("[data-gallery-count]").textContent==="2 / 3"')
    note('mobile_gallery_next',count=mp.locator('[data-gallery-count]').inner_text())
    mp.locator('[data-media-id]:visible [data-zoom-image]').nth(1).click()
    mp.wait_for_selector('[data-product-lightbox][open]')
    assert mp.locator('[data-lightbox-image]').get_attribute('src')
    mp.keyboard.press('Escape')
    assert not mp.locator('[data-product-lightbox]').is_visible()
    note('mobile_lightbox',escape_closed=True,focus=mp.evaluate('document.activeElement.hasAttribute("data-zoom-image")'))
    color(mp,'Olive')
    assert set(mp.locator('[data-media-id]:visible').evaluate_all('(items)=>items.map(x=>x.dataset.color)'))=={'olive'}
    mp.locator('.product-accordions').scroll_into_view_if_needed()
    mp.mouse.wheel(0,900)
    mp.locator('[data-product-sticky]:visible').wait_for()
    note('mobile_sticky',visible=True,button=mp.locator('[data-sticky-add]').inner_text())
    mp.screenshot(path=str(OUT/'commerce-preview-pdp-mobile-sticky.png'),full_page=False)
    product(mp,'the-colette-wool-tote')
    assert 'early October' in mp.locator('[data-preorder-notice]').text_content()
    note('colette_preorder',notice=mp.locator('[data-preorder-notice]').inner_text())
    browser.close()
except Exception:
    report['failure']=traceback.format_exc()
    print(report['failure'],flush=True)
finally:
    (OUT/'commerce-preview-qa.json').write_text(json.dumps(report,indent=2))
    print('Saved',OUT/'commerce-preview-qa.json',flush=True)
