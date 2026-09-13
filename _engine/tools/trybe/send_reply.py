"""Send a chat reply on Trybe. Usage: python3 send_reply.py "<Name>" "<message>"
Clicks the conversation, types into the composer, sends, verifies it landed."""
import sys
from playwright.sync_api import sync_playwright

name, message = sys.argv[1], sys.argv[2]

with sync_playwright() as p:
    b = p.chromium.connect_over_cdp("http://localhost:9333")
    pg = [x for x in b.contexts[0].pages if not x.url.startswith("devtools")][-1]
    if "/brand/chat" not in pg.url:
        pg.goto("https://jointrybe.com/brand/chat", wait_until="domcontentloaded")
        pg.wait_for_timeout(3000)

    pg.get_by_text(f"{name} (DM)", exact=False).first.click()
    pg.wait_for_timeout(2000)

    # find composer: prefer visible textarea / contenteditable / role=textbox near bottom
    composer = None
    for sel in ["textarea", "[contenteditable='true']", "[role='textbox']"]:
        loc = pg.locator(sel)
        for i in range(loc.count()):
            el = loc.nth(i)
            if el.is_visible():
                box = el.bounding_box()
                if box and box["y"] > 400:
                    composer = el
    if composer is None:
        print("NO_COMPOSER_FOUND"); sys.exit(1)

    composer.click()
    pg.keyboard.type(message, delay=8)
    pg.wait_for_timeout(400)
    pg.keyboard.press("Enter")
    pg.wait_for_timeout(2000)

    body = pg.evaluate("document.body.innerText")
    probe = message[:60]
    if probe in body:
        print(f"SENT_OK to {name}")
    else:
        # maybe Enter made a newline instead; try a send button
        for label in ["Send message", "Send"]:
            btn = pg.get_by_text(label, exact=True)
            if btn.count():
                try:
                    btn.last.click(); pg.wait_for_timeout(1500); break
                except Exception: pass
        body = pg.evaluate("document.body.innerText")
        print(f"SENT_OK to {name}" if probe in body else f"SEND_UNCONFIRMED to {name}")
