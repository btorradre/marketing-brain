#!/usr/bin/env python3
"""
Harvest an msToken cookie from an anonymous tiktok.com visit via Playwright.
Prints MS_TOKEN=<value> on success. A token from a logged-in browser cookie
is stronger; this is the zero-setup path.

Usage: venv/bin/python get_ms_token.py [--browser webkit|chromium] [--headless]
"""
import argparse
import asyncio
import sys

from playwright.async_api import async_playwright


async def harvest(browser_name, headless):
    async with async_playwright() as p:
        browser = await getattr(p, browser_name).launch(headless=headless)
        ctx = await browser.new_context()
        page = await ctx.new_page()
        await page.goto("https://www.tiktok.com/foryou", wait_until="domcontentloaded")
        token = None
        for _ in range(20):
            await asyncio.sleep(1.5)
            try:
                await page.mouse.wheel(0, 400)
            except Exception:
                pass
            cookies = await ctx.cookies()
            for c in cookies:
                if c["name"] == "msToken" and len(c.get("value", "")) > 40:
                    token = c["value"]
                    break
            if token:
                break
        await browser.close()
        return token


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--browser", default="webkit")
    ap.add_argument("--headless", action="store_true")
    args = ap.parse_args()
    token = asyncio.run(harvest(args.browser, args.headless))
    if token:
        print(f"MS_TOKEN={token}")
    else:
        print("no msToken cookie found", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
