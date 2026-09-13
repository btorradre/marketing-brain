#!/usr/bin/env python3
"""Real screen recording of the live Vivienne PDP: one continuous downward scroll that
eases out and HOLDS on the pre-order / October block. 1080x1920, 24fps.

Viewport is 500 CSS px wide — 390 and 430 clip the Velantra theme's title. DPR 3 gives a
1500x2667 shot that downscales cleanly to 1080x1920.
"""
import math, subprocess, tempfile
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image

HERE = Path(__file__).resolve().parent
URL  = "https://velantrafashion.com/products/velantra-vivienne"
FPS, DUR = 30, 5.5
SCROLL_FRAC = 0.72          # scrolling occupies the first 72%, then it holds
Y0, Y1 = 640, 975           # CSS scroll offsets: price/swatch block -> pre-order + October centred

def ease_out(t):            # decelerate into the hold, no hard stop
    return 1 - (1 - t) ** 3

def main():
    n = int(FPS * DUR)
    tmp = Path(tempfile.mkdtemp())
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 500, "height": 889}, device_scale_factor=3)
        pg.goto(URL, wait_until="domcontentloaded", timeout=90000)
        pg.wait_for_timeout(6000)
        pg.evaluate("document.querySelectorAll('video').forEach(v=>{v.pause();v.currentTime=0})")
        for i in range(n):
            t = i / (n - 1)
            s = min(t / SCROLL_FRAC, 1.0)
            y = Y0 + (Y1 - Y0) * ease_out(s)
            pg.evaluate(f"window.scrollTo(0, {y:.1f})")
            pg.wait_for_timeout(35)
            pg.screenshot(path=str(tmp / f"f{i:04d}.png"))
        b.close()
    for f in sorted(tmp.glob("*.png")):
        Image.open(f).convert("RGB").resize((1080, 1920), Image.LANCZOS).save(f)
    out = HERE / "PDP-scroll.mp4"
    subprocess.run(["ffmpeg","-y","-v","error","-framerate",str(FPS),
        "-i",str(tmp/"f%04d.png"),"-c:v","libx264","-pix_fmt","yuv420p","-crf","16",str(out)],check=True)
    print("OK", out, f"{n} frames")

main()
