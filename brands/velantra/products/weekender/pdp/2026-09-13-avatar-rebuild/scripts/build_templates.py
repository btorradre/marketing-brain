from pathlib import Path
import json,re
P=Path(__file__).resolve().parents[1]
selected=json.loads((P/'edit/selected-media.json').read_text())
receipts=json.loads((P/'shopify/asset-upload-receipts.json').read_text())
def url(key):return receipts[selected[key]['asset']]['public_url']
captions={'hero-v2':'The Cognac Eleanor Weekender styled with a wool coat','touch-v2':'Cognac canvas, leather and gold-tone details, held close','outdoor-v2':'The Cognac Eleanor Weekender carried by its rolled handles','car':'Cognac Eleanor Weekender on a leather passenger seat; accessories shown separately','cognac-front':'Cognac Eleanor Weekender — front view','cognac-quarter':'Cognac Eleanor Weekender — three-quarter view','cognac-handle-detail':'Cognac rolled handle, flap cutout and stitched leather detail','cognac-clasp-detail':'Cognac horizontal oval closure and contoured flap','cognac-interior':'Cognac caramel interior and wide slip pocket','cognac-architecture':'Cognac Eleanor Weekender in natural light against textured concrete'}
for sex in ['women','men']:
 sequence=[f'{sex}-hero-v2','cognac-front','cognac-quarter',f'{sex}-touch-v2',f'{sex}-outdoor-v2',f'{sex}-car','cognac-handle-detail','cognac-clasp-detail','cognac-interior','cognac-architecture']
 blocks={};order=[]
 def add(key,color,kind,caption):
  block_id=f'image_{len(order)+1}'
  blocks[block_id]={'type':'image','settings':{'url':url(key),'color':color,'caption':caption,'kind':kind,'focus_y':50}}
  order.append(block_id)
 for key in sequence:
  suffix=key.removeprefix(sex+'-');kind='hero' if suffix=='hero-v2' else 'packshot' if key=='cognac-front' else 'detail'
  add(key,'Cognac',kind,captions.get(key,captions.get(suffix,'')))
 for color,name in [('army','Army Green'),('espresso','Espresso'),('black','Black')]:
  views=[(f'{sex}-{color}-hero','hero','styled with a wool coat'),
   (f'{color}-front','packshot','front view'),
   (f'{color}-quarter','detail','three-quarter view'),
   (f'{sex}-{color}-touch','detail','material and gold-tone details, held close'),
   (f'{sex}-{color}-outdoor','detail','carried by its rolled handles'),
   (f'{sex}-{color}-car','detail','on a leather passenger seat; accessories shown separately'),
   (f'{color}-handle-detail','detail','rolled handle, flap cutout and stitched leather detail'),
   (f'{color}-clasp-detail','detail','horizontal oval closure and contoured flap'),
   (f'{color}-corner-detail','detail','lower front corner and material detail'),
   (f'{color}-architecture','detail','in natural light against textured concrete')]
  for key,kind,caption in views:add(key,name,kind,f'{name} Eleanor Weekender — {caption}')
 settings={'audience':sex,'eyebrow':'The Weekender Edit · For Her' if sex=='women' else 'The Weekender Edit · For Him',
 'intro':'The finishing touch to a beautifully put-together outfit. A sculpted silhouette, warm leather details and room for your day.' if sex=='women' else 'A considered companion to a well-dressed day. Clean structure, distinctive leather details and an easy sense of purpose.',
 'details':'A statement in the details: the Eleanor brings together rolled handles, a contoured flap and a generous, structured silhouette. Choose Cognac, Army Green, Espresso or all-leather Black.',
 'fit_copy':'A generous, open interior for the pieces you like to keep close. One nominal size, with a wide slip pocket for smaller belongings. Compare the dimensions below with your essentials before ordering.',
 'offer_heading':'Your next signature piece.','offer_caption':'Choose your color and make it part of your everyday wardrobe. No code needed.',
 'closing_heading':'A little polish. Everywhere you go.' if sex=='women' else 'Good style goes with you.',
 'closing_body':'Soft knits. A beautiful coat. The bag that brings it all together. Eleanor makes getting dressed feel considered, wherever the day takes you.' if sex=='women' else 'Over a weekend knit or beside a tailored coat, Eleanor is an understated finishing touch for the way you move through the day.',
 'dispatch_days':10,'transit_min':7,'transit_max':10,'black_preorder':True,'recommendation_collection':'handbags'}
 data={'layout':'wk-editorial','sections':{'main':{'type':'wk-editorial-product','settings':settings,'blocks':blocks,'block_order':order}},'order':['main']}
 (P/'theme/templates'/f'product.wk-editorial-{sex}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
layout=P/'theme/layout/wk-editorial.liquid';s=layout.read_text().replace('__MEN_HERO_URL__',url('men-hero-v2')).replace('__WOMEN_HERO_URL__',url('women-hero-v2'));s=re.sub(r'https://cdn.shopify.com/[^\"]*/wk-editorial-men-hero-v2.webp[^\"]*',url('men-hero-v2'),s);s=re.sub(r'https://cdn.shopify.com/[^\"]*/wk-editorial-women-hero-v2.webp[^\"]*',url('women-hero-v2'),s);layout.write_text(s)
print('Built both Shopify product templates')
