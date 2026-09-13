"""Encode generated PNGs for theme delivery and build precise catalog mappings.
No semantic image edits: RGB encoding + WebP compression only. Originals retained.
"""
import json,pathlib,hashlib,math,collections,urllib.parse
from PIL import Image,ImageDraw
BASE=pathlib.Path(__file__).resolve().parent
jobs=json.loads((BASE/'generation-jobs.json').read_text())
sources=json.loads((BASE/'source-manifest.json').read_text())
products=json.loads((BASE/'catalog-public.json').read_text())['products']
admin_path=BASE/'admin-image-alts.json'
admin_by_url={}
if admin_path.exists():
 for p in json.loads(admin_path.read_text())['data']['products']['nodes']:
  for media in p['media']['nodes']:
   if media.get('image'):
    admin_by_url[(p['handle'],urllib.parse.urlparse(media['image']['url']).path)]=media
qa_file=BASE/'qa/review-status.json'
qa=json.loads(qa_file.read_text()) if qa_file.exists() else {}
for additional_qa in sorted((BASE/'qa').glob('review-status-*.json')):
 qa.update(json.loads(additional_qa.read_text()))
(BASE/'theme-assets').mkdir(exist_ok=True)
lookup={}
for j in jobs:
 f=BASE/j['output']; j['status']='pending';j['visual_review']=qa.get(str(j['job']),{})
 if f.exists():
  out=BASE/'theme-assets'/j['theme_asset']
  im=Image.open(f).convert('RGB'); j['width'],j['height']=im.size
  if not out.exists() or out.stat().st_mtime<f.stat().st_mtime: im.save(out,'WEBP',quality=91,method=6)
  j['status']='reviewed' if j['visual_review'].get('approved') else 'generated_pending_review'
  j['theme_bytes']=out.stat().st_size
  j['sha256']=hashlib.sha256(out.read_bytes()).hexdigest()
 lookup[(j['handle'],j['source_position'])]=j
manifest={'version':1,'created':'2026-09-04','generation_method':'built-in image_gen; one edit per source view','live_catalog_modified':False,'source_product_count':len(products),'source_image_count':len(sources),'unique_generation_jobs':len(jobs),'generated_count':sum(j['status']!='pending' for j in jobs),'reviewed_count':sum(j['status']=='reviewed' for j in jobs),'duplicate_product_mapping':{'the-eleanor-weekender':'velantra-weekender'},'theme_assets_directory':'theme-assets','products':[]}
for p in products:
 handle=p['handle']; canonical='velantra-weekender' if handle=='the-eleanor-weekender' else handle
 images=[]
 for src in [s for s in sources if s['handle']==handle]:
  j=lookup[(canonical,src['position'])]
  admin=admin_by_url.get((handle,urllib.parse.urlparse(src['src']).path),{})
  images.append({'source_image_id':src['id'],'shopify_media_id':int(admin['id'].split('/')[-1]) if admin.get('id') else None,'shopify_image_source_id':int(admin['image']['id'].split('/')[-1]) if admin.get('image',{}).get('id') else None,'source_alt':admin.get('alt') or admin.get('image',{}).get('altText'),'source_position':src['position'],'source_url':src['src'],'source_variant_ids':src.get('variant_ids',[]),'job':j['job'],'theme_asset':j['theme_asset'],'color':j['color'],'status':j['status'],'width':j.get('width'),'height':j.get('height'),'output':j['output'],'visual_review':j['visual_review']})
 manifest['products'].append({'handle':handle,'product_id':p['id'],'title':p['title'],'canonical_handle':canonical,'images':images,'variants':[{'id':v['id'],'title':v['title'],'source_featured_image_id':v.get('featured_image',{}).get('id') if v.get('featured_image') else None} for v in p['variants']]})
(BASE/'production-manifest.json').write_text(json.dumps(manifest,indent=2))
flat_map={'by_source_image_id':{},'by_shopify_media_id':{},'by_shopify_image_source_id':{}}
for product in manifest['products']:
 for img in product['images']:
  value={'handle':product['handle'],'theme_asset':img['theme_asset'],'source_alt':img['source_alt'],'status':img['status']}
  flat_map['by_source_image_id'][str(img['source_image_id'])]=value
  if img.get('shopify_media_id'): flat_map['by_shopify_media_id'][str(img['shopify_media_id'])]=value
  if img.get('shopify_image_source_id'): flat_map['by_shopify_image_source_id'][str(img['shopify_image_source_id'])]=value
(BASE/'studio-image-map.json').write_text(json.dumps(flat_map,indent=2))
# Contact sheets are inspection artifacts, not product deliverables.
for handle in sorted(set(j['handle'] for j in jobs)):
 group=[j for j in jobs if j['handle']==handle and j['status']!='pending']
 for start in range(0,len(group),12):
  subset=group[start:start+12];tw,th=320,390; sheet=Image.new('RGB',(tw*4,th*math.ceil(len(subset)/4)),'#eeeeee');d=ImageDraw.Draw(sheet)
  for k,j in enumerate(subset):
   im=Image.open(BASE/j['output']).convert('RGB');im.thumbnail((305,340));x=(k%4)*tw+(tw-im.width)//2;y=(k//4)*th;sheet.paste(im,(x,y));d.text(((k%4)*tw+8,y+345),f"Job {j['job']} | Pos {j['source_position']} | {j['color'][:24]}",fill='black')
  sheet.save(BASE/f"qa/generated-{handle}-{start//12+1}.jpg",quality=90)
print(json.dumps({'generated':manifest['generated_count'],'reviewed':manifest['reviewed_count'],'jobs':len(jobs),'theme_size_mb':round(sum(j.get('theme_bytes',0) for j in jobs)/1e6,2)}))
