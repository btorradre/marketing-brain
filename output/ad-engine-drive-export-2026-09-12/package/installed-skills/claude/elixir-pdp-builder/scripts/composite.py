#!/usr/bin/env python3
"""
composite.py — build product clusters for the PDP custom sections.

Modes:
  transparent : N product copies on a transparent canvas (floating — for rv-compare / rv-core hero)
  onbg        : N product copies on a brand-colored radial backdrop (matches a dark panel)

Usage:
  python composite.py transparent <bottle-transparent.png> out.png
  python composite.py onbg <bottle-transparent.png> out.jpg --bg1 5e2417 --bg2 2a0e08
Deps: pillow
"""
import sys, argparse, math
from PIL import Image

def place(canvas, bottle, scale, cxr, cyr, W, H):
    bw, bh = bottle.size
    h = int(H * scale); w = int(bw * h / bh)
    r = bottle.resize((w, h), Image.LANCZOS)
    canvas.alpha_composite(r, (int(W*cxr - w/2), int(H*cyr - h/2)))

def gradient_bg(W, H, c1, c2):
    bg = Image.new('RGBA', (W, H)); px = bg.load()
    cx, cy = W*0.82, H*0.18; maxd = math.hypot(W, H)
    for y in range(H):
        for x in range(W):
            t = min(1.0, (math.hypot(x-cx, y-cy)/(maxd*0.78))**0.9)
            px[x, y] = (int(c1[0]+(c2[0]-c1[0])*t), int(c1[1]+(c2[1]-c1[1])*t),
                        int(c1[2]+(c2[2]-c1[2])*t), 255)
    return bg

def hx(s): s = s.lstrip('#'); return tuple(int(s[i:i+2], 16) for i in (0, 2, 4))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('mode', choices=['transparent', 'onbg'])
    ap.add_argument('bottle'); ap.add_argument('out')
    ap.add_argument('--bg1', default='5e2417'); ap.add_argument('--bg2', default='2a0e08')
    ap.add_argument('--w', type=int, default=1100); ap.add_argument('--h', type=int, default=720)
    a = ap.parse_args()
    b = Image.open(a.bottle).convert('RGBA')
    W, H = a.w, a.h
    canvas = (gradient_bg(W, H, hx(a.bg1), hx(a.bg2)) if a.mode == 'onbg'
              else Image.new('RGBA', (W, H), (0, 0, 0, 0)))
    place(canvas, b, 0.82, 0.32, 0.42, W, H)   # back-left
    place(canvas, b, 0.82, 0.68, 0.42, W, H)   # back-right
    place(canvas, b, 1.00, 0.50, 0.54, W, H)   # front-center
    if a.mode == 'onbg':
        canvas.convert('RGB').save(a.out, quality=90)
    else:
        canvas.save(a.out)
    print('wrote', a.out, canvas.size)

if __name__ == '__main__':
    main()
