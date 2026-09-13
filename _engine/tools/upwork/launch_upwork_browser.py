"""Launch a headed, persistent Chromium window at the Upwork login page.

Dedicated Upwork profile (separate from Trybe) so the session persists across
Claude sessions and never touches the Trybe login. Exposes CDP on port 9334 so
follow-up driver scripts can connect and drive the page. Stays alive until killed.
"""
import time
from playwright.sync_api import sync_playwright

PROFILE_DIR = "/Users/brooksorradre2/Documents/marketing brain/auth/upwork-browser-profile"
CDP_PORT = 9334
LOGIN_URL = "https://www.upwork.com/ab/account-security/login"

with sync_playwright() as p:
    ctx = p.chromium.launch_persistent_context(
        PROFILE_DIR,
        headless=False,
        args=[
            f"--remote-debugging-port={CDP_PORT}",
            "--no-first-run",
            "--no-default-browser-check",
            "--window-size=1440,900",
        ],
        viewport=None,
    )
    page = ctx.pages[0] if ctx.pages else ctx.new_page()
    try:
        page.goto(LOGIN_URL, wait_until="domcontentloaded")
    except Exception as e:
        print("GOTO_WARN", e, flush=True)
    print("BROWSER_READY", flush=True)
    while True:
        time.sleep(5)
        if not ctx.pages:
            try:
                ctx.new_page()
            except Exception:
                break
