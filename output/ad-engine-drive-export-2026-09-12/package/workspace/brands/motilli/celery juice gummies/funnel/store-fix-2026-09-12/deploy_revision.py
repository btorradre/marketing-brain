import json,re,base64,sys,hashlib,datetime
from pathlib import Path
from store_api import Store
P=Path(__file__).resolve().parent
T=P/'theme';THEME=188158148975;PRODUCT=14972162933103
OPS={'ThemeFiles':'''mutation ThemeFiles($files: [OnlineStoreThemeFilesUpsertFileInput!]!, $themeId: ID!) { themeFilesUpsert(files: $files, themeId: $themeId) { upsertedThemeFiles { filename } job { id } userErrors { field message } } }''',
'ProductCopy':'''mutation ProductCopy($product: ProductUpdateInput!) { productUpdate(product: $product) { product { id templateSuffix descriptionHtml } userErrors { field message } } }''',
'PolicyCopy':'''mutation PolicyCopy($shopPolicy: ShopPolicyInput!) { shopPolicyUpdate(shopPolicy: $shopPolicy) { shopPolicy { id type body } userErrors { field message } } }'''}
s=Store()
def receipt(label,d):
 (P/(label+'.json')).write_text(json.dumps(d,indent=2)+'\n')
def upsert(keys,label):
 files=[]
 for k in keys:
  p=T/k;binary=p.suffix=='.png';value=base64.b64encode(p.read_bytes()).decode() if binary else p.read_text()
  files.append({'filename':k,'body':{'type':'BASE64' if binary else 'TEXT','value':value}})
 d=s.graphql(OPS['ThemeFiles'],{'files':files,'themeId':f'gid://shopify/OnlineStoreTheme/{THEME}'});receipt(label,d)
 r=d['data']['themeFilesUpsert']
 if r['userErrors']:raise RuntimeError(str(r['userErrors']))
 print(label,{'upserted':[x['filename'] for x in r['upsertedThemeFiles']],'job':r['job']})
 for k in keys:
  if k.endswith('.png'):continue
  actual=s.asset(THEME,k)
  if actual!= (T/k).read_text():
   import time
   time.sleep(1)
   actual=s.asset(THEME,k)
  if actual!= (T/k).read_text():
   try:assert json.loads(actual)==json.loads((T/k).read_text())
   except Exception:raise RuntimeError('Readback differs: '+k)

def policy_body(x):
 body=x['body']
 if x['handle']=='shipping-policy':
  body=body.replace('Standard shipping is <strong>free on all orders</strong> within the United States.', 'Standard shipping within the United States is <strong>$4.99 on orders below $45</strong> and <strong>free on orders of $45 or more</strong>.')
  body=body.replace('We currently ship to addresses within the <strong>United States only</strong>, including all 50 states. We do not ship to P.O. boxes, APO/FPO addresses, or international destinations at this time.', 'We ship within the United States and to selected international destinations shown at checkout. International rates and available delivery services are calculated at checkout. We do not ship to P.O. boxes or APO/FPO addresses.')
  body=body.replace('Effective Date: May 2026','Updated: September 12, 2026')
 return body

if __name__=='__main__':
 phase=sys.argv[1]
 if phase=='stage':
  upsert(['assets/motilli-regularity-bottle.png'],'stage-image-receipt')
  a=s.get(f'/themes/{THEME}/assets.json',{'asset[key]':'assets/motilli-regularity-bottle.png'})['asset']
  receipt('stage-image-metadata',a)
  template=T/'templates/product.motilli-regularity.json';d=json.loads(template.read_text());d['sections']['main']['settings']['hero_image_url']=a['public_url'];template.write_text(json.dumps(d,indent=2)+'\n')
  upsert(['sections/motilli-regularity-product.liquid','sections/motilli-regularity-details.liquid','sections/motilli-store-home.liquid','templates/product.motilli-regularity.json'],'stage-template-receipt')
 elif phase=='publish':
  current=s.get(f'/products/{PRODUCT}.json')['product'];receipt('product-immediately-before-publish',current)
  if current['template_suffix'] not in [None,'','motilli-regularity']:raise RuntimeError('Product template changed since inspection; reconcile first')
  for key in ['templates/index.json','sections/header-group.json','sections/footer-group.json']:
   before=(P/'before'/key).read_text();actual=s.asset(THEME,key)
   if json.loads(before)!=json.loads(actual):raise RuntimeError('Concurrent theme change: '+key)
  body='<p>Motilli Celery Juice Gummies combine FOS prebiotic fiber, celery juice powder and chlorophyllin. FOS feeds beneficial gut bacteria and can help support regular bowel movements.</p><p>Take two green-apple gummies daily with water. Each bottle contains 60 gummies: a 30-day supply.</p><p>Choose one, three or five bottles. Every option includes a 90-day money-back guarantee from delivery, even on opened bottles.</p>'
  d=s.graphql(OPS['ProductCopy'],{'product':{'id':f'gid://shopify/Product/{PRODUCT}','templateSuffix':'motilli-regularity','descriptionHtml':body,'seo':{'title':'Motilli Celery Juice Gummies | Daily FOS Fiber Support','description':'FOS prebiotic fiber for daily regularity support. Two green-apple gummies a day. Choose your bottle pack with a 90-day money-back guarantee.'}}});receipt('publish-product-receipt',d)
  if d['data']['productUpdate']['userErrors']:raise RuntimeError(str(d))
  upsert(['templates/index.json','sections/header-group.json','sections/footer-group.json'],'publish-storefront-receipt')
  mapping={'refund-policy':'REFUND_POLICY','shipping-policy':'SHIPPING_POLICY','contact-information':'CONTACT_INFORMATION'}
  for x in json.loads((P/'policies-before.json').read_text())['policies']:
   if x['handle'] not in mapping:continue
   body=policy_body(x);(P/(x['handle']+'-after.html')).write_text(body)
   if body==x['body']:continue
   d=s.graphql(OPS['PolicyCopy'],{'shopPolicy':{'type':mapping[x['handle']],'body':body}});receipt('publish-'+x['handle']+'-receipt',d)
   if d['data']['shopPolicyUpdate']['userErrors']:raise RuntimeError(str(d['data']['shopPolicyUpdate']['userErrors']))
   print('Updated policy',x['handle'])
  receipt('published-at',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'theme_id':THEME,'product_id':PRODUCT,'url':'https://getmotilli.com/products/motilli-3-bottle-90day-reset','template':'motilli-regularity'})
