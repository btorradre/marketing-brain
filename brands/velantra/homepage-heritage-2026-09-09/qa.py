import json
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

ROOT=Path(__file__).resolve().parent
THEME=json.loads((ROOT/'draft-theme.json').read_text())['id'].split('/')[-1]
BASE='https://velantrafashion.com'
URL=BASE+'/?preview_theme_id='+THEME
results=[]

with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True)
    for width,height in [(1440,1000),(768,1024),(390,844)]:
        context=browser.new_context(viewport={'width':width,'height':height},reduced_motion='reduce')
        page=context.new_page()
        errors=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.goto(URL,wait_until='domcontentloaded')
        expect(page.locator('main h1')).to_have_count(1)
        expect(page.locator('main h1')).to_have_text('A Life Well Carried')
        expect(page.locator('main .heritage-campaign')).to_have_count(3)
        expect(page.locator('.heritage-world__card')).to_have_count(2)
        assert not page.locator('main video').count()
        for image in page.locator('main img').all():
            image.scroll_into_view_if_needed()
            page.wait_for_function('(img)=>img.complete && img.naturalWidth>0',arg=image.element_handle())
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
        image_report=page.locator('main img').evaluate_all('(els)=>els.map(e=>({alt:e.alt,source:e.currentSrc,width:e.naturalWidth,height:e.naturalHeight}))')
        if width<768:
            assert 'mobile' in image_report[0]['source']
        page.locator('.heritage-world').scroll_into_view_if_needed()
        expect(page.locator('[data-site-header]')).to_have_class(__import__('re').compile('is-heritage-scrolled'))
        if width>1100:
            page.locator('[data-dialog-open="SearchDialog"]').click()
            expect(page.locator('#SearchDialog')).to_be_visible()
            page.locator('#HeaderSearch').fill('Vivienne')
            page.locator('#SearchDialog [data-dialog-close]').click()
            expect(page.locator('#SearchDialog')).not_to_be_visible()
        else:
            page.locator('.mobile-menu').click()
            expect(page.locator('#NavigationDrawer')).to_be_visible()
            expect(page.locator('#NavigationDrawer nav>a').first).to_be_visible()
            expect(page.locator('#NavigationDrawer').get_by_role('link',name='Search',exact=True)).to_have_attribute('href','/search')
            page.locator('#NavigationDrawer [data-dialog-close]').click()
            expect(page.locator('#NavigationDrawer')).not_to_be_visible()
        page.locator('header [data-dialog-open="CartDrawer"]').click()
        expect(page.get_by_text('Your cart is empty',exact=True)).to_be_in_viewport(timeout=15000)
        page.get_by_role('button',name='Close cart',exact=True).click()
        expect(page.get_by_text('Your cart is empty',exact=True)).not_to_be_in_viewport()
        newsletter=page.locator('.newsletter input[type=email]')
        expect(newsletter).to_have_attribute('required','')
        expect(page.locator('.newsletter input[type=checkbox]')).to_have_attribute('required','')
        for i,section in enumerate(page.locator('.heritage-campaign,.heritage-world,.heritage-closing').all()):
            section.scroll_into_view_if_needed()
            section.screenshot(path=str(ROOT/f'qa/final-section-{width}-{i}.png'),style='#preview-bar-iframe,#PBarNextFrame{display:none!important}')
        page.evaluate('window.scrollTo(0,0)')
        page.wait_for_function('!document.querySelector("[data-site-header]").classList.contains("is-heritage-scrolled")')
        page.screenshot(path=str(ROOT/f'qa/final-hero-{width}.png'),style='#preview-bar-iframe,#PBarNextFrame{display:none!important}')
        page.screenshot(path=str(ROOT/f'qa/final-homepage-{width}.png'),full_page=True,style='#preview-bar-iframe,#PBarNextFrame{display:none!important}')
        links=page.locator('main a').evaluate_all('(els)=>els.map(e=>({text:e.textContent.trim()||e.getAttribute("aria-label"),href:e.href}))')
        results.append({'width':width,'height':height,'one_h1':True,'overflow':False,'header_menu_search_cart':True,'newsletter_required_fields':True,'images':image_report,'links':links,'page_errors':list(errors)})
        assert not errors,errors
        context.close()

    context=browser.new_context(viewport={'width':390,'height':844})
    page=context.new_page();page.goto(URL,wait_until='domcontentloaded')
    page.locator('.heritage-campaign--hero .heritage-links a').nth(1).click()
    page.wait_for_load_state('load')
    expect(page.locator('form[action*="/cart/add"] [name=id]')).to_have_value('44462686830657')
    quantity=page.locator('[data-product-quantity] input')
    expect(quantity).to_be_visible()
    page.locator('[data-product-quantity] button').nth(1).click()
    expect(quantity).to_have_value('2')
    with page.expect_response(lambda r:'/cart/add' in r.url and r.request.method=='POST') as add:
        page.locator('form[action*="/cart/add"] [name=add]').click()
    assert add.value.ok
    cart=context.request.get(BASE+'/cart.js').json()
    assert any(str(i['variant_id'])=='44462686830657' and i['quantity']==2 for i in cart['items'])
    context.request.post(BASE+'/cart/clear.js')
    page.goto(BASE+'/products/velantra-horse-charm?preview_theme_id='+THEME,wait_until='domcontentloaded')
    expect(page.locator('[data-gallery]')).to_have_attribute('data-color-only','true')
    expect(page.locator('[data-media-id]:not([hidden])')).to_have_count(1)
    expect(page.locator('[data-media-id]:not([hidden])')).to_have_attribute('data-color','brown')
    context.close();browser.close()

(ROOT/'qa/report.json').write_text(json.dumps({'viewports':results,'purchase':{'variant':'44462686830657','quantity':2,'cart_cleared':True},'accessory_gallery_fix_preserved':True},indent=2))
print('PASS: desktop, tablet and mobile layouts; menus, search, cart, links, images; quantity and accessory gallery regression')
