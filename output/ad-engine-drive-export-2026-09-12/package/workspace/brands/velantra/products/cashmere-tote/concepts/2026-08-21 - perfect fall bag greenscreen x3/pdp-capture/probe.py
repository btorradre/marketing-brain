from playwright.sync_api import sync_playwright
import time
with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    pg = b.new_context(viewport={"width":430,"height":764},
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1").new_page()
    pg.goto("https://velantrafashion.com/products/the-colette-wool-tote", wait_until="domcontentloaded", timeout=60000)
    time.sleep(5)
    for sel in ["119.99","149.99","Save","Pre-order"]:
        for el in pg.query_selector_all(f"text={sel}")[:4]:
            try:
                bb = el.bounding_box()
                print(f"{sel!r:<12} tag={el.evaluate('e=>e.tagName')} cls={(el.get_attribute('class') or '')[:50]!r} y={bb['y'] if bb else None} txt={el.inner_text()[:60]!r}")
            except Exception as ex: print(sel, "ERR", ex)
    b.close()
