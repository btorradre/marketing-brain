from pathlib import Path
import json,traceback,re
from playwright.sync_api import sync_playwright
OUT=Path(__file__).parent
report=json.loads((OUT/'commerce-preview-qa.json').read_text())
report.pop('failure',None)
def note(name,**data):
    report['checks'].append({'name':name,**data});print(json.dumps(report['checks'][-1]),flush=True)
def product(page,handle):
    page.goto(f'https://velantrafashion.com/products/{handle}?preview_theme_id=151337074753',wait_until='domcontentloaded')
    page.wait_for_selector('[data-commerce-ready]')
    page.evaluate('document.fonts.ready')
try:
 with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    ctx=browser.new_context(viewport={'width':1440,'height':1000})
    page=ctx.new_page();page.on('pageerror',lambda e:report['page_errors'].append(str(e)))
    product(page,'velantra-vivienne')
    frame=page.frame(name='PBarNextFrame')
    if frame:
      hide=frame.get_by_role('button',name='Hide bar',exact=True)
      hide.wait_for(timeout=10000);hide.click()
    page.set_viewport_size({'width':390,'height':844})
    page.locator('[data-option-picker] label[title="Olive"]').click()
    assert page.locator('[data-selected-option]').text_content()=='Olive'
    assert set(page.locator('[data-media-id]:visible').evaluate_all('(items)=>items.map(x=>x.dataset.color)'))=={'olive'}
    page.locator('.product-accordions').scroll_into_view_if_needed();page.mouse.wheel(0,900)
    page.wait_for_function('document.querySelector("[data-add-button]").getBoundingClientRect().bottom<0')
    page.locator('[data-product-sticky]:visible').wait_for()
    note('mobile_sticky',visible=True,button=page.locator('[data-sticky-add]').inner_text(),selected=page.locator('[data-selected-option]').text_content())
    page.screenshot(path=str(OUT/'commerce-preview-pdp-mobile-sticky.png'),full_page=False)
    page.route('**/cart/add.js',lambda route:route.fulfill(status=422,content_type='application/json',body=json.dumps({'status':422,'description':'This item is currently unavailable. Please try another color.'})))
    page.locator('[data-sticky-add]').focus()
    page.keyboard.press('Enter')
    page.locator('[data-product-error]:visible').wait_for()
    assert 'currently unavailable' in page.locator('[data-product-error]').inner_text()
    assert page.locator('[data-add-button]').is_enabled()
    note('ajax_error_recovery',error=page.locator('[data-product-error]').inner_text(),button_reenabled=True)
    page.unroute('**/cart/add.js')
    product(page,'the-colette-wool-tote')
    assert 'early October' in page.locator('[data-preorder-notice]').text_content()
    note('colette_preorder',notice=page.locator('[data-preorder-notice]').text_content().strip())
    nojs=browser.new_context(viewport={'width':1440,'height':1000},java_script_enabled=False)
    np=nojs.new_page();np.goto('https://velantrafashion.com/products/velantra-vivienne?preview_theme_id=151337074753',wait_until='domcontentloaded')
    assert np.locator('[data-variant-fallback]').is_visible()
    assert np.locator('[data-add-button]').is_enabled()
    assert np.locator('[data-product-form]').get_attribute('method').lower()=='post'
    np.locator('[data-variant-select]').select_option(value=np.locator('[data-variant-select] option').filter(has_text='Black').get_attribute('value'))
    note('native_no_js_form',variant=np.locator('[data-variant-select]').input_value(),method=np.locator('[data-product-form]').get_attribute('method'),action=np.locator('[data-product-form]').get_attribute('action'))
    np.goto('https://velantrafashion.com/products/velantra-juliette?preview_theme_id=151337074753',wait_until='domcontentloaded')
    assert np.locator('[data-add-button]').is_disabled()
    note('native_no_js_zero_guard',disabled=True)
    report['passed']=True
    browser.close()
except Exception:
    report['failure']=traceback.format_exc();print(report['failure'],flush=True)
finally:
    (OUT/'commerce-preview-qa.json').write_text(json.dumps(report,indent=2));print('Saved commerce-preview-qa.json',flush=True)
