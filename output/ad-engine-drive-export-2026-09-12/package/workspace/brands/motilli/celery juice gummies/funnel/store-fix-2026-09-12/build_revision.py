import copy,json,re,shutil
from pathlib import Path
P=Path(__file__).resolve().parent
T=P/'theme'
for f in (P/'before').rglob('*'):
 if f.is_file():
  q=T/f.relative_to(P/'before');q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,q)

def write(k,s):
 p=T/k;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s)
def dump(k,d):write(k,json.dumps(d,indent=2,ensure_ascii=False)+'\n')

tpl=json.loads((P/'before/templates/product.json').read_text())
main=copy.deepcopy(tpl['sections']['main']);main['type']='motilli-regularity-product'
main['settings'].update({'mobile_padding_top':12,'desktop_padding_top':24,'enable_sticky_info':False})
blocks=main['blocks']
for bid in list(blocks):
 if bid not in ['custom_liquid_4hPfWk','buy_buttons','custom_liquid_mbg90','custom_liquid_AfY7jH']:
  del blocks[bid]
blocks['buy_buttons']['settings'].update({'margin_top':12,'margin_bottom':8,'uppercase_text':False})
blocks['custom_liquid_4hPfWk']['settings']['custom_liquid']='''<div class="motilli-buy-intro">
<p class="motilli-eyebrow">DAILY REGULARITY SUPPORT</p>
<h1>Motilli Celery Juice Gummies</h1>
<p class="motilli-benefit">Support more regular mornings.</p>
<p class="motilli-intro">FOS prebiotic fiber feeds the good bacteria in your gut and can help support regular bowel movements. So you can add daily fiber without another powder to mix.</p>
<p class="motilli-serving">2 gummies daily <span aria-hidden="true">·</span> 30 days per bottle <span aria-hidden="true">·</span> Green apple</p>
<a class="motilli-facts-link" href="#motilli-ingredients">See what's inside ↓</a>
</div>'''
blocks['custom_liquid_mbg90']['settings']['custom_liquid']='''<div class="motilli-purchase-details"><p class="motilli-shipping" data-motilli-shipping>US standard shipping: $4.99. Free on orders $45+.</p><p><strong>90 days to decide. Opened bottles count.</strong><br>If you're not satisfied, request a full refund within 90 days of delivery.</p><p class="motilli-delivery">Usually ships in 1–2 business days. US delivery: 5–10 business days after dispatch.</p></div>'''
main['block_order']=['custom_liquid_4hPfWk','buy_buttons','custom_liquid_mbg90','custom_liquid_AfY7jH']

ing=copy.deepcopy(tpl['sections']['motilli-ingredients'])
ing['settings']['heading']="The fiber from the ad, explained simply."
ing['blocks']['i3']['settings'].update({'name':'FOS prebiotic fiber','description':"FOS is short for fructooligosaccharides. It feeds the good bacteria already living in your gut and can help support more regular bowel movements."})
ing['blocks']['i1']['settings'].update({'name':'Celery juice powder','description':"Celery juice powder is part of the Motilli formula, alongside FOS prebiotic fiber and chlorophyllin."})
ing['blocks']['i2']['settings'].update({'name':'Chlorophyllin','description':"The formula contains sodium copper chlorophyllin, a chlorophyll-derived ingredient. FOS is the fiber we explain in the ad for regularity support."})
ing['block_order']=['i3','i1','i2']
usage=copy.deepcopy(tpl['sections']['motilli-usage'])
usage['settings'].update({'heading':'Two gummies. One simple daily routine.','subtext':"You don't need a blender or another powder to mix. Motilli comes in green-apple gummies, so it's easy to make it part of your day."})
vals=[('s1','Take 2 gummies daily','One serving a day, with a glass of water.'),('s2','Keep it simple','Choose a time that fits your routine and follow the directions on your bottle.'),('s3','Know your supply','Each bottle contains 60 gummies: 30 daily servings.'),('s4','Try it with confidence','You have 90 days from delivery to request a refund, even on opened bottles.')]
for k,title,body in vals:usage['blocks'][k]['settings'].update({'title':title,'body':body})
guarantee=copy.deepcopy(tpl['sections']['motilli-bf-09'])
guarantee['settings'].update({'heading':'90 days to decide. Opened bottles count.','body':"If you try Motilli and don't notice a difference, email support@getmotilli.com within 90 days of delivery to request a full refund. You can contact us at any point during those 90 days. See our refund policy for the full process.",'cta_text':'Choose your bottles','cta_link':'#MainProduct'})
faq=copy.deepcopy(tpl['sections']['motilli-bf-08'])
faq['settings']['heading']='A few things you may be wondering.'
qa=[
('What does the FOS fiber do?',"FOS is a prebiotic fiber. It feeds beneficial bacteria already in your gut and can help support regular bowel movements. It is one part of a daily fiber routine."),
("I've already tried fiber. How is this different?","Different products contain different fibers. Motilli contains FOS, also called fructooligosaccharides. Check the ingredient in the product you've tried so you can compare like for like. We don't claim Motilli will work for everyone who has tried another fiber."),
('Can I use Motilli while taking a GLP-1?',"Ask your prescriber or pharmacist whether this supplement fits your medication and health needs. Motilli provides daily fiber support; it is not a treatment for delayed stomach emptying or a replacement for prescribed care."),
('How do I take it?',"Take two gummies daily with water and follow the directions on your bottle. Each bottle contains 60 gummies, so it lasts 30 days."),
('How quickly will I notice a difference?',"People respond differently to fiber supplements. We don't promise a particular result by a particular week. If you're not satisfied, you have 90 days from delivery to request a refund, even on opened bottles."),
('Do I have to buy three bottles?',"No. You can choose one bottle, three bottles, or five bottles. One bottle is a 30-day supply, and the 90-day money-back guarantee applies to that option too."),
('Is this a subscription?',"The bottle options on this page are one-time purchases. There is no recurring order attached to these options."),
('How much is shipping?',"US standard shipping is $4.99, or free on orders of $45 or more. Orders usually process in 1–2 business days, followed by an estimated 5–10 business days for US delivery. Any available international or expedited options and their rates appear at checkout."),
('How do I request a refund?',"Email <a href=\"mailto:support@getmotilli.com\">support@getmotilli.com</a> with your order number within 90 days of delivery. Opened bottles are eligible. See our <a href=\"/policies/refund-policy\">refund policy</a> for the return and refund process.")]
faq['blocks']={f'q{i}':{'type':'qa','settings':{'question':q,'answer':'<p>'+a+'</p>'}} for i,(q,a) in enumerate(qa,1)}
faq['block_order']=list(faq['blocks'])
sections={'main':main,'motilli-explainer':{'type':'motilli-regularity-details','settings':{}},'motilli-ingredients':ing,'motilli-usage':usage,'motilli-faq':faq,'motilli-guarantee':guarantee}
dump('templates/product.motilli-regularity.json',{'sections':sections,'order':list(sections)})

src=(P/'before/sections/main-product.liquid').read_text()
src=src.replace('class="color-{{ section.settings.color_scheme }} gradient section-{{ section.id }}-padding"','class="motilli-regularity color-{{ section.settings.color_scheme }} gradient section-{{ section.id }}-padding"',1)
src=src.replace("{% render 'product-media-gallery', variant_images: variant_images, has_filtering: has_filtering, section %}",'''<figure class="motilli-product-figure">
<img src="{{ section.settings.hero_image_url }}" alt="{{ product.title | escape }} — 60 green-apple gummies" width="379" height="769" fetchpriority="high" loading="eager">
<figcaption>FOS prebiotic fiber<br><strong>2 gummies a day</strong></figcaption>
</figure>''',1)
src=src.replace("{% render 'product-media-modal', variant_images: variant_images %}",'')
src=src.replace('''          <a href="{{ product.url }}" class="link product__view-details animate-arrow">
            {{ 'products.product.view_full_details' | t }}
            {% render 'icon-arrow' %}
          </a>''','')
sm=re.search(r'{% schema %}(.*?){% endschema %}',src,re.S);schema=json.loads(sm.group(1))
schema['name']='Motilli regularity product'
schema['settings'].insert(0,{'type':'url','id':'hero_image_url','label':'Product image URL'})
src=src[:sm.start(1)]+'\n'+json.dumps(schema,indent=2)+'\n'+src[sm.end(1):]
write('sections/motilli-regularity-product.liquid',src)

# Preserve source product photography exactly; fiber amount remains a pending user confirmation.
(T/'assets').mkdir(exist_ok=True)
shutil.copy2(P.parents[1]/'product-images/v3-signal-2026-08-10/bottle_cut.png',T/'assets/motilli-regularity-bottle.png')

# Current homepage is a product page. Send visitors to the same canonical PDP, preserving attribution parameters.
dump('templates/index.json',{'sections':{'main':{'type':'motilli-store-home','settings':{}}},'order':['main']})
write('sections/motilli-store-home.liquid','''<div class="page-width" style="padding:48px 24px;text-align:center"><h1>{{ shop.name | escape }}</h1><p><a href="/products/motilli-3-bottle-90day-reset">Shop Motilli Celery Juice Gummies</a></p></div>
<script>location.replace('/products/motilli-3-bottle-90day-reset'+location.search+location.hash);</script>
{% schema %}{"name":"Motilli store home","settings":[]}{% endschema %}
''')
header=json.loads((P/'before/sections/header-group.json').read_text())
for section in header['sections'].values():
 if section['type']=='announcement-bar':
  for b in section.get('blocks',{}).values():
   b['settings'].update({'text':'90-day money-back guarantee · Free US shipping $45+','mobile_text_size':12})
dump('sections/header-group.json',header)
footer=json.loads((P/'before/sections/footer-group.json').read_text());footer['sections']['footer']['settings']['show_policy']=True;dump('sections/footer-group.json',footer)
print('Built template and related page files')
