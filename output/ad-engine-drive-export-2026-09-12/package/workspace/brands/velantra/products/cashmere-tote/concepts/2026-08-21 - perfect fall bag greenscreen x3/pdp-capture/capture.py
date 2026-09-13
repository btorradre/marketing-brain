#!/usr/bin/env python3
"""Record the live Colette PDP price block -> swatches -> Add to Cart -> cart drawer.
Produces the offer-beat screen recording with the REAL live price."""
from playwright.sync_api import sync_playwright
import os, time

OUT = os.path.dirname(os.path.abspath(__file__))
URL = "https://velantrafashion.com/products/the-colette-wool-tote"

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    ctx = b.new_context(
        viewport={"width": 430, "height": 764},
        record_video_dir=os.path.join(OUT, "raw"),
        record_video_size={"width": 430, "height": 764},
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    )
    pg = ctx.new_page()
    pg.goto(URL, wait_until="domcontentloaded", timeout=60000)
    time.sleep(6)
    for sel in [".klaviyo-close-form", "button[aria-label*='lose' i]", "button:has-text('No thanks')"]:
        try:
            el = pg.query_selector(sel)
            if el and el.is_visible():
                el.click(); time.sleep(0.4)
        except Exception:
            pass

    # 1. land on the price block (struck $149.99 -> $119.99, Save $30.00) and hold
    pg.evaluate("window.scrollTo({top: 560, behavior:'instant'})")
    time.sleep(1.8)
    pg.screenshot(path=os.path.join(OUT, "shot-price.png"))

    # 2. slow drift down through the swatches to Add to Cart
    for _ in range(18):
        pg.mouse.wheel(0, 18)
        time.sleep(0.07)
    time.sleep(1.2)
    pg.screenshot(path=os.path.join(OUT, "shot-atc.png"))

    # 3. add to cart, let the drawer open on the real price
    try:
        pg.click("button:has-text('ADD TO CART'), button[name='add']", timeout=8000)
    except Exception as e:
        print("ATC click failed:", e)
    time.sleep(3.0)
    pg.screenshot(path=os.path.join(OUT, "shot-cart.png"))
    time.sleep(0.8)

    ctx.close()
    b.close()
print("done")
