from pathlib import Path
import json,shutil,sys,hashlib
from urllib.parse import urlparse
r=Path(__file__).resolve().parents[1];t=r/'theme'
m=json.loads((r/'media/production-manifest.json').read_text());ad=json.loads((r/'media/admin-image-alts.json').read_text())['data']['products']['nodes']
a={p['handle']:{Path(urlparse(i['image']['url']).path).name:i for i in p['media']['nodes'] if i.get('image')} for p in ad}
lines=['{% doc %}','Returns a white studio image URL scoped to this theme.','@param {image} image - Original Shopify image','@param {product} [product] - Product fallback','@param {number} [media_id] - Media identifier for preview images','{% enddoc %}',"{%- assign source_image = image | default: product.featured_image -%}",'{%- if settings.use_studio_catalog -%}','{%- assign source_id = source_image.id | default: media_id -%}','{%- case source_id -%}']
uploaded=json.loads((r/'research/cdn-uploads.json').read_text()) if (r/'research/cdn-uploads.json').exists() else {}
qa=json.loads((r/'media/qa/review-status.json').read_text())
count=0
mapped_assets={}
for p in m['products']:
 for item in p['images']:
  name=item['theme_asset'];src=r/'media/theme-assets'/name
  if not src.exists() or not qa.get(str(item['job']),{}).get('approved'):continue
  if '--uploaded-only' in sys.argv and uploaded.get(name,{}).get('sha256')!=hashlib.sha256(src.read_bytes()).hexdigest():continue
  shutil.copy2(src,t/'assets'/name)
  mapped_assets[item['source_image_id']]=name
  ids=[str(item['source_image_id'])];obj=a.get(p['handle'],{}).get(Path(urlparse(item['source_url']).path).name)
  if obj:
   for value in [obj.get('id'),obj['image'].get('id')]:
    if value:ids.append(value.rsplit('/',1)[-1])
  ids=list(dict.fromkeys(ids));lines+=['{%- when '+', '.join(ids)+' -%}',"{{- '"+name+"' | asset_url -}}"]
  count+=1
lines.extend(['{%- endcase -%}','{%- endif -%}']);(t/'snippets/studio-image-url.liquid').write_text('\n'.join(lines)+'\n')
print('Mapped',count,'of',m['source_image_count'],'original gallery images')
variants=[]
for product in m['products']:
 for variant in product['variants']:
  asset=mapped_assets.get(variant['source_featured_image_id'])
  if asset:variants.append('"'+str(variant['id'])+'": {{- \''+asset+'\' | asset_url | json -}}')
variant_map='{% doc %}Theme-scoped studio variant image URLs for the AJAX cart drawer.{% enddoc %}\n{%- if settings.use_studio_catalog -%}\n{'+',\n'.join(variants)+'}\n{%- else -%}{}{%- endif -%}\n'
(t/'snippets/studio-variant-map.liquid').write_text(variant_map)
print('Mapped',len(variants),'variant images for the cart drawer')
