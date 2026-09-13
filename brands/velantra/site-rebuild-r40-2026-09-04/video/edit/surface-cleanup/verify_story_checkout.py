import asyncio,json
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parent
THEME=151397859393
OUT=ROOT/f"qa/revision-2/story-storefront-{THEME}"
async def main():
 async with async_playwright() as p:
  browser=await p.chromium.launch()
  context=await browser.new_context(viewport={"width":1440,"height":1000})
  page=await context.new_page()
  await page.goto(f"https://velantrafashion.com/products/velantra-weekender?preview_theme_id={THEME}",wait_until="domcontentloaded")
  preview=page.frame_locator("#PBarNextFrame").get_by_role("button",name="Hide bar")
  await preview.wait_for(state="visible")
  await preview.click()
  await page.wait_for_selector("[data-product-section][data-commerce-ready]")
  await page.wait_for_function('typeof window.upcartOpenCart === "function"')
  assert await page.evaluate("Shopify.theme.id")==THEME
  await page.locator(".product-options input[type=radio]").evaluate_all('(els)=>{const e=els.find(x=>x.value==="Cognac");e.checked=true;e.dispatchEvent(new Event("change",{bubbles:true}));}')
  await page.locator("[data-add-button]").click()
  checkout=page.locator(".upcart-checkout-button")
  await checkout.wait_for(state="visible")
  cart=await page.evaluate('async()=>{const r=await fetch("/cart.js",{credentials:"same-origin"});if(!r.ok)throw new Error(`cart status ${r.status}`);return r.json()}')
  assert cart["item_count"]==1
  assert cart["items"][0]["variant_id"]==44165996544065
  report={"theme_id":THEME,"upcart_open":True,"item_count":cart["item_count"],"selected_variant":cart["items"][0]["variant_id"]}
  await checkout.scroll_into_view_if_needed()
  await page.screenshot(path=str(OUT/"upcart.png"))
  await checkout.click()
  await page.wait_for_url(lambda u:"/checkouts/" in u or "/checkout" in u,timeout=45000)
  report["shopify_checkout_reached"]=True
  await page.screenshot(path=str(OUT/"checkout.png"))
  mobile=await browser.new_context(viewport={"width":390,"height":844})
  mp=await mobile.new_page()
  await mp.goto(f"https://velantrafashion.com/products/velantra-vivienne?preview_theme_id={THEME}",wait_until="domcontentloaded")
  await mp.wait_for_selector("[data-product-section][data-commerce-ready]")
  await mp.locator(".product-option__values--colors").scroll_into_view_if_needed()
  await mp.wait_for_function('Array.from(document.querySelectorAll(".product-option__thumbnail img")).every(i=>i.complete&&i.naturalWidth>0)')
  report["mobile_color_images_loaded"]=await mp.locator(".product-option__thumbnail img").count()
  report["skip_link_focused"]=await mp.evaluate('document.activeElement?.textContent?.trim()==="Skip to content"')
  await mp.screenshot(path=str(OUT/"mobile-colors-normal-scroll.png"))
  (OUT/"checkout-report.json").write_text(json.dumps(report,indent=2))
  print(json.dumps(report))
  await browser.close()
asyncio.run(main())
