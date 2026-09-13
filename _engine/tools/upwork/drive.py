"""Connect to the persistent Upwork browser over CDP and run a quick action.

Usage: python3.12 drive.py <action> [args...]
Actions:
  url                    - print current page URL + title
  shot <path>            - screenshot current page (viewport)
  goto <url>             - navigate current tab
  text                   - dump visible body text (trimmed to 6000 chars)
  loggedin               - heuristic: report whether an Upwork session looks active
"""
import sys
from playwright.sync_api import sync_playwright

CDP = "http://localhost:9334"
action = sys.argv[1] if len(sys.argv) > 1 else "url"

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(CDP)
    ctx = browser.contexts[0]
    pages = [pg for pg in ctx.pages if not pg.url.startswith("devtools")]
    page = pages[-1] if pages else ctx.new_page()

    if action == "url":
        print(page.url, "|", page.title())
    elif action == "shot":
        page.screenshot(path=sys.argv[2], full_page=False)
        print("saved", sys.argv[2], "|", page.url)
    elif action == "goto":
        page.goto(sys.argv[2], wait_until="domcontentloaded")
        page.wait_for_timeout(2500)
        print(page.url, "|", page.title())
    elif action == "text":
        print(page.evaluate("document.body.innerText")[:6000])
    elif action == "loggedin":
        # On upwork.com, a logged-out session redirects protected pages to /login.
        page.goto("https://www.upwork.com/nx/find-work/", wait_until="domcontentloaded")
        page.wait_for_timeout(3000)
        u = page.url
        print("LOGGED_IN" if "login" not in u and "signup" not in u else "LOGGED_OUT", "|", u)
