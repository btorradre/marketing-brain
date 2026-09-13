"""Record the live Eleanor Weekender PDP scrolling on a clean mobile viewport.
Output: f13/pdp-scroll-raw.webm -> f13/F13-pdp-scroll-1080x1920.mp4
"""
import asyncio, os, glob, subprocess
from playwright.async_api import async_playwright

URL = "https://velantrafashion.com/products/the-eleanor-weekender"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "f13")
W, H = 390, 844  # iPhone 15 CSS px; recorded at 3x below

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(
            viewport={"width": W, "height": H}, device_scale_factor=3, is_mobile=True, has_touch=True,
            user_agent=("Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 "
                        "(KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1"),
            record_video_dir=OUT, record_video_size={"width": W*3, "height": H*3},
        )
        page = await ctx.new_page()

        # generic popup killer: every 200ms remove any body-level node (or shadow host) containing the popup copy
        await page.add_init_script("""
          (function(){
            const BAD=/Designer look|designer price|GET 10|Unlock|Sign up and save/i;
            const nuke=()=>{
              const walk=(root)=>{ for(const e of root.querySelectorAll('*')){
                  if(e.shadowRoot) walk(e.shadowRoot);
                  if(e.children.length===0 && BAD.test(e.textContent||'')){
                    let n=e; while(n && n.parentElement && n.parentElement!==document.body) n=n.parentElement;
                    if(n && n!==document.body) n.remove();
                    const host=e.getRootNode().host; if(host) host.remove();
                  }}};
              try{ walk(document);}catch(_){}
              document.body && (document.body.style.overflow='auto');
              document.documentElement.style.overflow='auto';
            };
            setInterval(nuke,200);
          })();
        """)
        # kill popups at the source: block Klaviyo + common popup vendors, hide any overlay
        async def _block(route):
            await route.abort()
        for pat in ["**/*klaviyo*/**", "**/*klaviyo.com/**", "**/*privy*/**", "**/*justuno*/**", "**/*optimonk*/**"]:
            await page.route(pat, _block)
        await page.add_init_script("""
          const css = `[class*="kl-private"], [class*="klaviyo"], .needsclick, [id*="klaviyo"],
                       [class*="popup"], [class*="modal"][aria-modal="true"], [class*="newsletter"] { display:none !important; }
                       body { overflow: auto !important; }`;
          const st = document.createElement('style'); st.textContent = css;
          document.addEventListener('DOMContentLoaded', () => document.head.appendChild(st));
        """)
        await page.goto(URL, wait_until="load", timeout=60000)
        await page.wait_for_timeout(3500)
        # dismiss common popups if present
        for sel in ["button[aria-label='Close']", "button:has-text('Close')", ".klaviyo-close-form", "[class*='close']"]:
            try:
                el = page.locator(sel).first
                if await el.is_visible(timeout=800):
                    await el.click(timeout=800); await page.wait_for_timeout(400)
            except Exception:
                pass
        await page.wait_for_timeout(1500)  # hold on hero + price
        # smooth scroll: small steps, ~9s total
        total = await page.evaluate("document.body.scrollHeight")
        y = 0
        target = min(total, 3600)
        while y < target:
            y += 18
            await page.evaluate(f"window.scrollTo(0,{y})")
            await page.wait_for_timeout(22)
        await page.wait_for_timeout(3500)
        # scroll back up to the buy box and hold
        while y > 0:
            y -= 60
            await page.evaluate(f"window.scrollTo(0,{max(y,0)})")
            await page.wait_for_timeout(16)
        await page.wait_for_timeout(1800)
        await ctx.close(); await browser.close()

asyncio.run(main())
vids = sorted(glob.glob(os.path.join(OUT, "*.webm")), key=os.path.getmtime)
raw = vids[-1]
final = os.path.join(OUT, "F13-pdp-scroll-1080x1920.mp4")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw,
                "-vf", "scale=1080:1920:flags=lanczos,format=yuv420p", "-r", "30",
                "-c:v", "libx264", "-crf", "18", "-an", final], check=True)
print("raw:", raw); print("final:", final)
