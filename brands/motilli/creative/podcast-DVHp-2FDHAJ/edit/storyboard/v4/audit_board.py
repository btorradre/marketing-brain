"""Read back the saved board, check actual served assets, and inspect rendering."""
import asyncio,json,hashlib
from pathlib import Path
from urllib.request import urlopen
from PIL import Image,ImageDraw
from playwright.async_api import async_playwright
V=Path(__file__).resolve().parent
BASE='http://localhost:8765'
SLUG='motilli-podcast-dvhp-storyboard'
board=json.load(urlopen(BASE+'/api/boards/'+SLUG))
assert board['project']=='motilli' and 'v4' in board['title']
checks=[]
for src in sorted({c['src'] for c in board['cards'] if c['type']=='image'}):
 with urlopen(BASE+src) as r:data=r.read();status=r.status
 checks.append({'src':src,'status':status,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
assert all(x['status']==200 and x['bytes']>1000 for x in checks)
coverage=json.loads((V.parent/'podcast-coverage.json').read_text())
hashes={};repeats=[]
for c in coverage:
 if 'Podcast' in c['mode']:continue
 h=hashlib.sha256(Path(c['frame']).read_bytes()).hexdigest()
 if h in hashes:repeats.append([hashes[h],c['id']])
 hashes[h]=c['id']
assert not repeats,repeats
selected=[]
for c in coverage:
 if c.get('asset_key') and c['asset_key'] not in [x['asset_key'] for x in selected]:selected.append(c)
for j in range(0,len(selected),5):
 group=selected[j:j+5];sheet=Image.new('RGB',(320*len(group),620),'#081b35');draw=ImageDraw.Draw(sheet)
 for i,c in enumerate(group):
  im=Image.open(c['frame']).convert('RGB');im.thumbnail((308,560));sheet.paste(im,(i*320+(320-im.width)//2,45));draw.text((i*320+8,8),c['id']+' '+c['asset_key'],fill='white')
 sheet.save(V/'audit'/f'selected-v4-{j//5+1}.jpg')
async def browser_check():
 async with async_playwright() as p:
  b=await p.chromium.launch(headless=True)
  page=await b.new_page(viewport={'width':1600,'height':1000},device_scale_factor=1)
  await page.goto(BASE+'/b/'+SLUG,wait_until='networkidle')
  await page.wait_for_function('Array.from(document.images).every(i => i.complete)')
  result=await page.evaluate('({title:document.title,images:document.images.length,broken:Array.from(document.images).filter(i=>!i.naturalWidth).map(i=>i.src),text:document.body.innerText.includes("S26-2")})')
  await page.screenshot(path=str(V/'audit/cutroom-v4-browser.png'),full_page=False)
  assert result['images']>0 and not result['broken'],result
  await b.close();return result
result=asyncio.run(browser_check())
(V/'audit/served-board-qa.json').write_text(json.dumps({'project':board['project'],'title':board['title'],'cards':len(board['cards']),'asset_checks':checks,'nonpresenter_exact_reuse':repeats,'browser':result},indent=2))
print(json.dumps({'title':board['title'],'cards':len(board['cards']),'unique_served_images':len(checks),'browser':result,'nonpresenter_exact_reuse':repeats}))
