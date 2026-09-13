from pathlib import Path
import json
from playwright.sync_api import sync_playwright
out=Path(__file__).resolve().parent
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True);context=browser.new_context(viewport={'width':1440,'height':1000});page=context.new_page();requests=[]
 page.on('request',lambda r:requests.append(r.url) if any(x in r.url.lower() for x in ['upcart','aftersell']) else None)
 page.goto('https://velantrafashion.com/products/velantra-vivienne?preview_theme_id=151364960321',wait_until='domcontentloaded');page.wait_for_timeout(6000)
 data=page.evaluate('''()=>({scripts:Array.from(document.scripts).map(s=>s.src).filter(s=>/upcart|aftersell/i.test(s)),upcartKeys:Object.keys(window).filter(k=>/upcart/i.test(k)),upcartElements:Array.from(document.querySelectorAll('[id*="upcart" i],[id*="upCart"]')).map(e=>({tag:e.tagName,id:e.id,classes:e.className})),embedBlocks:window.Shopify?.theme})''')
 data['requests']=requests
 (out/'upcart-inspection.json').write_text(json.dumps(data,indent=2)+'\n');(out/'upcart-inspection-source.html').write_text(page.content())
 print(json.dumps(data,indent=2)[:18000]);browser.close()
