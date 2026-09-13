from pathlib import Path
import json,time
from store_api import Store
P=Path(__file__).resolve().parent;s=Store();pid='gid://shopify/Product/14972162933103'
source=json.loads((P/'stage-image-metadata.json').read_text())['public_url']
alt='Motilli Celery Juice Gummies — product bottle'
q='''mutation ProductImage($product: ProductUpdateInput!, $media: [CreateMediaInput!]) { productUpdate(product: $product, media: $media) { product { id media(first: 15) { nodes { id alt status } } } userErrors { field message } } }'''
d=s.graphql(q,{'product':{'id':pid},'media':[{'mediaContentType':'IMAGE','originalSource':source,'alt':alt}]});(P/'product-image-create-receipt.json').write_text(json.dumps(d,indent=2))
assert not d['data']['productUpdate']['userErrors'],d['data']['productUpdate']['userErrors']
new=next(m for m in d['data']['productUpdate']['product']['media']['nodes'] if m['alt']==alt);mid=new['id'];print('Added image',mid,flush=True)
for _ in range(8):
 d=s.graphql('query($id:ID!){node(id:$id){... on MediaImage{id status image{url}}}}',{'id':mid})
 if d['data']['node']['status']=='READY':break
 time.sleep(2)
else:raise RuntimeError('Image is not ready')
q='''mutation ProductImageOrder($id: ID!, $moves: [MoveInput!]!) { productReorderMedia(id: $id, moves: $moves) { job { id done } mediaUserErrors { field message } } }'''
d=s.graphql(q,{'id':pid,'moves':[{'id':mid,'newPosition':'0'}]});(P/'product-image-reorder-receipt.json').write_text(json.dumps(d,indent=2));assert not d['data']['productReorderMedia']['mediaUserErrors']
for _ in range(8):
 prod=s.get('/products/14972162933103.json')['product']
 if prod['images'][0]['alt']==alt:break
 time.sleep(2)
else:raise RuntimeError('Image order not reflected yet')
(P/'product-after.json').write_text(json.dumps(prod,indent=2));print('Featured product image verified',prod['images'][0]['src'],flush=True)
