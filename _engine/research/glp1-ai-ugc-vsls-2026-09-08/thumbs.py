import json,pathlib,subprocess,concurrent.futures
from PIL import Image,ImageOps,ImageDraw
P=pathlib.Path(__file__).resolve().parent;(P/'media').mkdir(exist_ok=True)
s=json.loads((P/'raw/sos-transcripts-usage.json').read_text())['result']['structuredContent']['data']
l=json.loads((P/'raw/sos-transcripts-longest.json').read_text())['result']['structuredContent']['data']
rows=[dict(r,label='U'+str(i)) for i,r in enumerate(s[:18])]+[dict(l[i],label='L'+str(i)) for i in [7,8,9,11,12,14,19,20,21,26]]
(P/'candidates.json').write_text(json.dumps(rows,indent=2))
def work(r):
 f=P/'media'/(r['label']+'-thumb.jpg');subprocess.run(['curl','-f','-sS','-L','--max-time','60','-A','Mozilla/5.0',r['sampleAd']['thumbnailUrl'],'-o',str(f)],check=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:list(ex.map(work,rows))
for start in range(0,len(rows),12):
 batch=rows[start:start+12];sheet=Image.new('RGB',(1200,400*((len(batch)+3)//4)),'white');draw=ImageDraw.Draw(sheet)
 for j,r in enumerate(batch):
  im=ImageOps.contain(Image.open(P/'media'/(r['label']+'-thumb.jpg')).convert('RGB'),(295,350));x=j%4*300;y=j//4*400;sheet.paste(im,(x,y+35));draw.text((x+4,y+4),f"{r['label']} uses {r['usageCount']} days {r['longestRunning']}",fill='black')
 sheet.save(P/'media'/f'thumbs-{start}.jpg')
