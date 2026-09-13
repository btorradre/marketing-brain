from pathlib import Path
import json,re
P=Path(__file__).resolve().parents[1]
theme=P/'theme'
section=theme/'sections/wk-editorial-product.liquid'
s=section.read_text().split('{% stylesheet %}')[0]
s=re.sub(r'"quantity":\{\{.*?\}\},', '', s)
s=s.replace('cart.currency.iso_code | default: shop.currency','localization.country.currency.iso_code | default: shop.currency').replace(',"labels":{{ \'wk_editorial\' | t | json }}','').replace('"remove":','"quantity":{{ \'wk_editorial.quantity\' | t | json }},"remove":')
def setting(type,id,label,**kwargs):return {'type':type,'id':id,'label':'t:wk_editorial.'+label,**kwargs}
def option(value,label):return {'value':value,'label':'t:wk_editorial.'+label}
schema={'name':'t:wk_editorial.schema_name','max_blocks':50,'settings':[
setting('select','audience','schema_audience',options=[option('women','schema_women'),option('men','schema_men')],default='women'),
*[setting('text' if k in ['eyebrow','offer_heading','closing_heading'] else 'textarea',k,label) for k,label in [('eyebrow','schema_eyebrow'),('intro','schema_intro'),('details','schema_details'),('fit_copy','schema_fit'),('offer_heading','schema_offer_heading'),('offer_caption','schema_offer_caption'),('closing_heading','schema_closing_heading'),('closing_body','schema_closing_body')]],
setting('range','dispatch_days','schema_dispatch',min=0,max=30,step=1,default=10),setting('range','transit_min','schema_transit_min',min=1,max=30,step=1,default=7),setting('range','transit_max','schema_transit_max',min=1,max=30,step=1,default=10),setting('checkbox','black_preorder','schema_preorder',default=True),setting('collection','recommendation_collection','schema_recommendations')],
'blocks':[{'type':'image','name':'t:wk_editorial.schema_image','settings':[setting('url','url','schema_image_url'),setting('select','color','schema_color',options=[{'value':x,'label':x} for x in ['Cognac','Army Green','Espresso','Black']],default='Cognac'),setting('text','caption','schema_caption'),setting('select','kind','schema_kind',options=[option('hero','schema_hero'),option('packshot','schema_packshot'),option('detail','schema_detail')],default='detail'),setting('range','focus_y','schema_focus',min=0,max=100,step=1,default=50)]},
{'type':'review','name':'t:wk_editorial.schema_review','settings':[setting('text','author','schema_author'),setting('range','rating','schema_rating',min=1,max=5,step=1,default=5),setting('text','title','schema_review_title'),setting('textarea','body','schema_review_body'),setting('checkbox','verified','schema_verified',default=False)]}]}
section.write_text(s+'\n{% stylesheet %}\n'+(P/'edit/page.css').read_text()+'\n{% endstylesheet %}\n{% javascript %}\n'+(P/'edit/page.js').read_text()+'\n{% endjavascript %}\n{% schema %}\n'+json.dumps(schema,indent=2)+'\n{% endschema %}\n')
translations=json.loads((P/'edit/translations.json').read_text())
locale=json.loads((P/'shopify/staging-backup/locales/en.default.json').read_text())
locale['wk_editorial']=translations
(theme/'locales/en.default.json').write_text(json.dumps(locale,ensure_ascii=False,indent=2)+'\n')
schema_locale={'wk_editorial':{k:v for k,v in translations.items() if k.startswith('schema_')}}
(theme/'locales/en.default.schema.json').write_text(json.dumps(schema_locale,ensure_ascii=False,indent=2)+'\n')
print('Assembled section, CSS, JS, translations and schema')
