#!/usr/bin/env python3
"""export_board.py — render a board to ONE self-contained read-only HTML file.

Images are inlined as data URIs, so the file can be emailed, dropped in Slack,
or published as an artifact. Viewer supports pan + zoom only (no editing).

Usage:  python3 export_board.py <board-slug> [-o out.html]
"""
import argparse
import base64
import json
import mimetypes
import os

ROOT = os.path.dirname(os.path.abspath(__file__))


def inline(src):
    if not src.startswith("/assets/"):
        return src
    p = os.path.join(ROOT, "assets", src[len("/assets/"):])
    if not os.path.isfile(p):
        return src
    ctype = mimetypes.guess_type(p)[0] or "image/jpeg"
    with open(p, "rb") as f:
        return f"data:{ctype};base64," + base64.b64encode(f.read()).decode()


TEMPLATE = """<!doctype html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%;overflow:hidden;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:#1e2126;color:#e8eaed}
#viewport{position:absolute;inset:0;overflow:hidden;cursor:grab;background-image:radial-gradient(#2b2f36 1.2px, transparent 1.2px);background-size:26px 26px}
#world{position:absolute;top:0;left:0;transform-origin:0 0}
.card{position:absolute;border-radius:10px;box-shadow:0 2px 10px rgba(0,0,0,.35)}
.card.note{background:#f7f5ee;color:#26282c;padding:12px 14px;overflow:hidden}
.card.note .ctitle{font-weight:700;font-size:13px;margin-bottom:6px}
.card.note .ctext{font-size:12.5px;line-height:1.45;white-space:pre-wrap;word-wrap:break-word}
.card.image{background:#111;overflow:hidden;display:flex;flex-direction:column}
.card.image img{flex:1;width:100%;object-fit:cover;min-height:0}
.card.image .cap{background:#15171b;color:#cfd5dc;font-size:11px;padding:6px 9px;line-height:1.35}
.card.image .cap:empty{display:none}
.card.label{background:transparent;box-shadow:none;color:#e8eaed;font-weight:800;display:flex;align-items:flex-end;padding:4px 2px}
.card.lane{background:rgba(255,255,255,.028);border:1px dashed #444b56;box-shadow:none;border-radius:14px}
.card.lane .lane-title{position:absolute;top:-11px;left:18px;background:#1e2126;padding:2px 10px;font-size:12px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#9aa3ad}
#bar{position:fixed;top:12px;left:14px;z-index:10;background:rgba(38,42,49,.9);border:1px solid #3a4049;border-radius:10px;padding:8px 14px;font-size:13px;font-weight:600}
</style></head><body>
<div id="bar">__TITLE__ · scroll to pan, pinch/ctrl-scroll to zoom</div>
<div id="viewport"><div id="world"></div></div>
<script>
const board = __BOARD__;
const world = document.getElementById('world'), viewport = document.getElementById('viewport');
let view = {x:60, y:60, s:1};
const order = {lane:0,label:1,image:2,note:3};
[...board.cards].sort((a,b)=>(order[a.type]??2)-(order[b.type]??2)).forEach(c=>{
  const el = document.createElement('div');
  el.className = 'card '+c.type;
  el.style.cssText = `left:${c.x}px;top:${c.y}px;width:${c.w}px;height:${c.h}px`;
  if(c.type==='note'){
    el.style.background = c.color||'#f7f5ee';
    const t=document.createElement('div'); t.className='ctitle'; t.textContent=c.title||'';
    const x=document.createElement('div'); x.className='ctext'; x.textContent=c.text||'';
    if(c.title) el.appendChild(t); el.appendChild(x);
  } else if(c.type==='image'){
    const im=document.createElement('img'); im.src=c.src;
    const cap=document.createElement('div'); cap.className='cap'; cap.textContent=c.text||'';
    el.appendChild(im); el.appendChild(cap);
  } else if(c.type==='label'){
    el.style.fontSize=(c.size||22)+'px'; if(c.color) el.style.color=c.color;
    el.textContent=c.text||'';
  } else if(c.type==='lane'){
    const t=document.createElement('div'); t.className='lane-title'; t.textContent=c.title||'';
    el.appendChild(t);
  }
  world.appendChild(el);
});
function apply(){ world.style.transform=`translate(${view.x}px,${view.y}px) scale(${view.s})`; }
function fit(){
  if(!board.cards.length) return apply();
  const xs=board.cards.map(c=>c.x), ys=board.cards.map(c=>c.y);
  const xe=board.cards.map(c=>c.x+c.w), ye=board.cards.map(c=>c.y+c.h);
  const minX=Math.min(...xs)-60, minY=Math.min(...ys)-60;
  const w=Math.max(...xe)-minX+60, h=Math.max(...ye)-minY+60;
  const r=viewport.getBoundingClientRect();
  const s=Math.min(1.6, Math.min(r.width/w, r.height/h));
  view={s, x:(r.width-w*s)/2-minX*s, y:(r.height-h*s)/2-minY*s}; apply();
}
viewport.addEventListener('pointerdown', e=>{
  const sx=e.clientX, sy=e.clientY, ox=view.x, oy=view.y;
  const mv = ev=>{ view.x=ox+ev.clientX-sx; view.y=oy+ev.clientY-sy; apply(); };
  const up = ()=>{ window.removeEventListener('pointermove',mv); window.removeEventListener('pointerup',up); };
  window.addEventListener('pointermove',mv); window.addEventListener('pointerup',up);
});
viewport.addEventListener('wheel', e=>{
  e.preventDefault();
  if(e.ctrlKey||e.metaKey){
    const ns=Math.min(2.5,Math.max(.08,view.s*Math.exp(-e.deltaY*.01)));
    const r=viewport.getBoundingClientRect();
    const px=(e.clientX-r.left-view.x)/view.s, py=(e.clientY-r.top-view.y)/view.s;
    view.s=ns; view.x=e.clientX-r.left-px*ns; view.y=e.clientY-r.top-py*ns; apply();
  } else { view.x-=e.deltaX; view.y-=e.deltaY; apply(); }
},{passive:false});
window.addEventListener('resize', fit);
fit();
</script></body></html>"""


def export(slug, out=None):
    bp = os.path.join(ROOT, "boards", slug + ".json")
    with open(bp) as f:
        board = json.load(f)
    for c in board.get("cards", []):
        if c.get("type") == "image" and c.get("src"):
            c["src"] = inline(c["src"])
    html = (TEMPLATE
            .replace("__TITLE__", (board.get("title") or slug)
                     .replace("<", "&lt;").replace(">", "&gt;"))
            .replace("__BOARD__", json.dumps(board)))
    out = out or os.path.join(ROOT, "exports", slug + ".html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f:
        f.write(html)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("-o", "--out")
    a = ap.parse_args()
    print("Exported:", export(a.slug, a.out))
