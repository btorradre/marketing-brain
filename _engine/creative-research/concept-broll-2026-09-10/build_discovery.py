import pathlib,json,requests,concurrent.futures,io
from PIL import Image,ImageDraw,ImageOps
R=pathlib.Path(__file__).resolve().parent
(R/'discovery').mkdir(exist_ok=True)
files=list((R/'raw').glob('domain-*.json'))+[R/'raw'/f'{x}.json' for x in ['focused-lymph','focused-bloating','query-animation','query-podcast','shopify-growth']]
ads={}
for f in sorted(files):
 if f.name.endswith('-request.json') or not f.exists():continue
 for a in json.loads(f.read_text()).get('result',{}).get('structuredContent',{}).get('data',[]):
  if not a.get('media',{}).get('thumbnailUrl'):continue
  key=a.get('collationId') or a['id']
  if key not in ads: a['discovered_by']=[];ads[key]=a
  ads[key]['discovered_by'].append(f.stem)
rows=list(ads.values())
for i,a in enumerate(rows):a['candidate_id']=f'C{i+1:03}'
(R/'candidates.json').write_text(json.dumps(rows,indent=2))
def get(a):
 p=R/'discovery'/(a['id']+'.jpg')
 if not p.exists():
  try:
   q=requests.get(a['media']['thumbnailUrl'],timeout=30);q.raise_for_status();im=Image.open(io.BytesIO(q.content)).convert('RGB');im.save(p)
  except Exception as e:print(a['id'],type(e).__name__)
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:list(ex.map(get,rows))
for start in range(0,len(rows),25):
 sheet=Image.new('RGB',(1000,1500),'#17191d');d=ImageDraw.Draw(sheet)
 for j,a in enumerate(rows[start:start+25]):
  x=(j%5)*200;y=(j//5)*300
  p=R/'discovery'/(a['id']+'.jpg')
  if p.exists(): sheet.paste(ImageOps.contain(Image.open(p),(196,245)),(x,y))
  m=a['metrics'];txt=f"{a['candidate_id']} {a['advertiser']['name'][:21]}\nreach {m.get('reach')} / {a.get('daysRunning')}d\n7d {m.get('reachDelta7d')}"
  d.text((x+3,y+246),txt,fill='white')
 p=R/'discovery'/f'sheet-{start//25+1:02}.jpg';sheet.save(p);print(p)
print('CANDIDATES',len(rows))
