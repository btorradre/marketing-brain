"""Launch a headed, persistent Chromium window at the Trybe login page.

Profile lives in the vault so the Trybe session survives across Claude sessions.
Exposes CDP on port 9333 so follow-up scripts can connect and drive the page.
Process stays alive until killed.
"""
import time
from playwright.sync_api import sync_playwright

PROFILE_DIR = "/Users/brooksorradre2/Documents/marketing brain/auth/trybe-browser-profile"
CDP_PORT = 9333

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
    page.goto("https://jointrybe.com/auth/login", wait_until="domcontentloaded")
    print("BROWSER_READY", flush=True)
    # Keep alive until the process is killed; survive user closing a tab.
    while True:
        time.sleep(5)
        if not ctx.pages:
            # keep at least one page so CDP stays inspectable
            try:
                ctx.new_page()
            except Exception:
                break
