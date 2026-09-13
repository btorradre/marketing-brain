from pathlib import Path
import json
r=Path(__file__).resolve().parents[1];t=r/'theme'
for p in t.rglob('*.liquid'):
 if p.name in ['header.liquid','footer.liquid']:
  x=p.read_text().replace('{{ routes.root_url }}products/','{{ routes.root_url | append: "/products/" | replace: "//", "/" }}');p.write_text(x)
p=t/'snippets/theme-script.liquid';x=p.read_text();x=x.replace('const root={{ routes.root_url | json }};',"const rawRoot=window.Shopify?.routes?.root || {{ routes.root_url | json }};const root=rawRoot.endsWith('/')?rawRoot:rawRoot+'/';")
x=x.replace("play:{{ 'general.play' | t | json }}", "play:{{ 'general.play' | t | json }},preorderOctober:{{ 'commerce.product.preorder_october' | t | json }},preorderEarlyOctober:{{ 'commerce.product.preorder_early_october' | t | json }},preorderSeptember:{{ 'commerce.product.preorder_black_september' | t | json }}")
x=x.replace('function renderCart(cart)',"function preorderNote(i){if(i.handle==='velantra-vivienne')return labels.preorderOctober;if(i.handle==='the-colette-wool-tote')return labels.preorderEarlyOctober;if(['velantra-weekender','the-eleanor-weekender'].includes(i.handle)&&i.variant_title==='Black')return labels.preorderSeptember;return '';}\nfunction renderCart(cart)")
x=x.replace('<p>${money(i.final_line_price)}</p>','<p>${money(i.final_line_price)}</p>${preorderNote(i)?`<p class="drawer-preorder">${esc(preorderNote(i))}</p>`:\'\'}')
x=x.replace("renderCart(data);document.dispatchEvent", "renderCart(data);const nextButtons=[...document.querySelectorAll('[data-cart-key]')];const nextFocus=nextButtons.find(n=>n.dataset.cartKey===b.dataset.cartKey&&n.className===b.className)||document.querySelector('#CartDrawer [data-dialog-close]');nextFocus?.focus();document.dispatchEvent")
x=x.replace("scope.querySelectorAll('.hero-video')", "scope.querySelectorAll('.hero-video,.detail-video')")
x=x.replace("document.querySelectorAll('.hero-video').forEach(v=>v.pause())", "document.querySelectorAll('.hero-video,.detail-video').forEach(v=>v.pause())")
p.write_text(x)
p=t/'sections/header.liquid';x=p.read_text().replace('id="NavigationDrawer"','id="NavigationDrawer" aria-label="{{ \'general.menu\' | t }}"').replace('id="SearchDialog"','id="SearchDialog" aria-label="{{ \'general.search\' | t }}"').replace('id="LocaleDialog"','id="LocaleDialog" aria-label="{{ \'general.region\' | t }}"')
x=x.replace('@media(max-width:1100px){.header-right','@media(max-width:1100px){.desktop-nav{display:none}.mobile-menu{display:block}.header-right')
x=x.replace('<a href="mailto:{{ shop.email }}">{{ \'general.client_services\' | t }}</a></nav>', '<a href="mailto:{{ shop.email }}">{{ \'general.client_services\' | t }}</a>{% if localization.available_countries.size > 1 %}<button class="micro" data-dialog-open="LocaleDialog">{{ localization.country.name }} / {{ localization.country.currency.iso_code }}</button>{% endif %}</nav>')
p.write_text(x)
p=t/'snippets/cart-drawer.liquid';x=p.read_text().replace('id="CartDrawer"','id="CartDrawer" aria-label="{{ \'cart.selection\' | t }}"');p.write_text(x)
print('Root interaction refinements applied')
