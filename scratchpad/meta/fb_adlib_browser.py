#!/usr/bin/env python3
"""Scrape Meta Ads Library with Playwright, intercepting search_ads XHR JSON."""
import json, sys, time
from playwright.sync_api import sync_playwright

def scrape(url, out_path, scrolls=12, settle=2.5):
    captured = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(
            user_agent=("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"),
            viewport={"width": 1400, "height": 950}, locale="en-US")
        page = ctx.new_page()

        def on_response(resp):
            if "async/search_ads" in resp.url or "/api/graphql" in resp.url:
                try:
                    txt = resp.text()
                    if "ad_archive_id" not in txt:
                        return
                    captured.append(txt)
                    print(f"  captured XHR #{len(captured)} ({len(txt)} bytes)", flush=True)
                except Exception as e:
                    print(f"  xhr fail: {e}", flush=True)

        page.on("response", on_response)
        page.goto(url, wait_until="domcontentloaded", timeout=90000)
        time.sleep(5)
        # dismiss cookie dialog if present
        for sel in ('div[aria-label="Allow all cookies"]', 'button:has-text("Allow all cookies")',
                    'div[aria-label="Decline optional cookies"]'):
            try:
                page.locator(sel).first.click(timeout=2000)
                break
            except Exception:
                pass
        for i in range(scrolls):
            page.mouse.wheel(0, 2600)
            time.sleep(settle)
        open(out_path, "w").write("\n<<<XHR>>>\n".join(captured))
        # also save embedded initial payload from page HTML
        html = page.content()
        open(out_path + ".html", "w").write(html)
        browser.close()
    print(f"saved {len(captured)} XHR payloads -> {out_path}")
    return captured

if __name__ == "__main__":
    scrape(sys.argv[1], sys.argv[2])
