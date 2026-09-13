# Removes compare-at (strikethrough) prices from every ACTIVE Velantra product. Run only on Brooks' go.
import os,json,ssl,urllib.request,certifi,time
os.chdir('/Users/brooksorradre2/Documents/marketing brain')
env=dict(l.strip().split('=',1) for l in open('.env') if '=' in l and not l.startswith('#'))
S=env['SHOPIFY_VELANTRA_STORE'].strip().strip('"'); ctx=ssl.create_default_context(cafile=certifi.where())
tok=json.load(urllib.request.urlopen(urllib.request.Request(f'https://{S}/admin/oauth/access_token',data=json.dumps({'grant_type':'client_credentials','client_id':env['SHOPIFY_VELANTRA_CLIENT_ID'].strip().strip('"'),'client_secret':env['SHOPIFY_VELANTRA_CLIENT_SECRET'].strip().strip('"')}).encode(),headers={'Content-Type':'application/json'}),context=ctx))['access_token']
def gql(q,v=None):
    r=urllib.request.Request(f'https://{S}/admin/api/2025-07/graphql.json',data=json.dumps({'query':q,'variables':v or {}}).encode(),headers={'Content-Type':'application/json','X-Shopify-Access-Token':tok})
    return json.load(urllib.request.urlopen(r,context=ctx))
prods=gql('{products(first:50,query:"status:active"){nodes{id title variants(first:50){nodes{id compareAtPrice}}}}}')['data']['products']['nodes']
json.dump(prods,open('brands/velantra/_shared/theme-build/gmc-compliance-backup-2026-09-05/compare-at-prices-BACKUP.json','w'),indent=1)
for p in prods:
    vs=[{'id':v['id'],'compareAtPrice':None} for v in p['variants']['nodes'] if v['compareAtPrice']]
    if not vs: continue
    r=gql('mutation($pid:ID!,$vs:[ProductVariantsBulkInput!]!){productVariantsBulkUpdate(productId:$pid,variants:$vs){userErrors{message}}}',{'pid':p['id'],'vs':vs})
    print(p['title'],len(vs),r['data']['productVariantsBulkUpdate']['userErrors']); time.sleep(0.5)
