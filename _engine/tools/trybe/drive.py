"""Connect to the persistent Trybe browser over CDP and run a quick action.

Usage: python3 drive.py <action> [args...]
Actions:
  shot <path>            - screenshot current page
  url                    - print current page URL + title
  goto <url>             - navigate
  text                   - dump visible body text (trimmed)
"""
import sys
from playwright.sync_api import sync_playwright

action = sys.argv[1]

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://localhost:9333")
    ctx = browser.contexts[0]
    pages = [pg for pg in ctx.pages if not pg.url.startswith("devtools")]
    page = pages[-1] if pages else ctx.new_page()

    if action == "shot":
        page.screenshot(path=sys.argv[2], full_page=False)
        print("saved", sys.argv[2], "|", page.url)
    elif action == "url":
        print(page.url, "|", page.title())
    elif action == "goto":
        page.goto(sys.argv[2], wait_until="domcontentloaded")
        page.wait_for_timeout(2000)
        print(page.url, "|", page.title())
    elif action == "text":
        txt = page.evaluate("document.body.innerText")
        print(txt[:4000])
