"""Frame-by-frame capture of the live PDP scrolling at 3x DPR -> crisp 1080x1920 mp4.
Playwright's video recorder paints the CSS viewport into the canvas at 1x, so instead we
screenshot every scroll step at device_scale_factor=3 and assemble at 30fps.
"""
import asyncio, os, shutil, subprocess
from playwright.async_api import async_playwright

URL = "https://velantrafashion.com/products/the-eleanor-weekender"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "f13"); FR = os.path.join(OUT, "frames")
W, H = 390, 844
KILLER = """
(function(){
  const BAD=/Designer look|designer price|GET 10|Unlock|Sign up and save/i;
  const nuke=()=>{ const walk=(root)=>{ for(const e of root.querySelectorAll('*')){
      if(e.shadowRoot) walk(e.shadowRoot);
      if(e.children.length===0 && BAD.test(e.textContent||'')){
        let n=e; while(n && n.parentElement && n.parentElement!==document.body) n=n.parentElement;
        if(n && n!==document.body) n.remove(); const host=e.getRootNode().host; if(host) host.remove(); }}};
    try{walk(document);}catch(_){}
    if(document.body){document.body.style.overflow='auto';} document.documentElement.style.overflow='auto'; };
  setInterval(nuke,150);
})();"""

async def main():
    shutil.rmtree(FR, ignore_errors=True); os.makedirs(FR)
    async with async_playwright() as p:
        b = await p.chromium.launch(headless=True)
        ctx = await b.new_context(viewport={"width": W, "height": H}, device_scale_factor=3,
            is_mobile=True, has_touch=True,
            user_agent=("Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 "
                        "(KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1"))
        page = await ctx.new_page()
        await page.add_init_script(KILLER)
        await page.goto(URL, wait_until="load", timeout=60000)
        await page.wait_for_timeout(4000)
        # hide scrollbars / smooth-scroll interference
        await page.add_style_tag(content="html{scroll-behavior:auto !important} ::-webkit-scrollbar{display:none}")
        n = 0
        async def shot(y, repeat=1):
            nonlocal n
            await page.evaluate(f"window.scrollTo(0,{y})")
            await page.wait_for_timeout(40)
            path = os.path.join(FR, f"f{n:05d}.jpg")
            await page.screenshot(path=path, type="jpeg", quality=92)
            n += 1
            for _ in range(repeat - 1):
                shutil.copy(path, os.path.join(FR, f"f{n:05d}.jpg")); n += 1
        # timeline @30fps: hold hero 1.5s, scroll to buy box (y=300) over 1.5s, hold 2s,
        # scroll down to 3000 over 9s, hold 1s, back to buy box over 2s, hold 2s
        await shot(0, repeat=45)
        for y in range(0, 300, 7):   await shot(y)          # ~43 frames
        await shot(300, repeat=60)
        for y in range(300, 3000, 10): await shot(y)        # 270 frames
        await shot(3000, repeat=30)
        for y in range(3000, 300, -45): await shot(y)       # 60 frames
        await shot(300, repeat=60)
        await b.close()
    final = os.path.join(OUT, "F13-pdp-scroll-1080x1920.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", "30", "-i", os.path.join(FR, "f%05d.jpg"),
                    "-vf", "scale=1080:1920:flags=lanczos,format=yuv420p", "-c:v", "libx264", "-crf", "17", "-an", final], check=True)
    # tight 6s CTA cut: buy-box hold + first scroll (starts at frame 45+43 = 88 -> t=2.93s)
    tight = os.path.join(OUT, "F13-pdp-cta-6s-1080x1920.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "2.93", "-t", "6", "-i", final, "-c:v", "libx264", "-crf", "17", "-an", tight], check=True)
    print("frames:", n); print(final); print(tight)

asyncio.run(main())
