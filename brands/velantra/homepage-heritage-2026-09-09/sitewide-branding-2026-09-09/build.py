from pathlib import Path
import json,shutil
ROOT=Path(__file__).resolve().parent
BEFORE=ROOT/'before'; AFTER=ROOT/'after'
def save(k,s):
 p=AFTER/k;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s)
s=(BEFORE/'layout/theme.liquid').read_text().replace('class="template-{{ template.name }}','class="heritage-site template-{{ template.name }}')
s=s.replace("{% if template.name == 'index' %}{% render 'heritage-shell' %}{% endif %}","{% render 'heritage-shell' %}")
s=s.replace("{% render 'commerce-styles' %}","{% render 'commerce-styles' %}\n{% render 'heritage-site-styles' %}")
save('layout/theme.liquid',s)
s=(BEFORE/'snippets/heritage-shell.liquid').read_text().replace('Homepage-only heritage','Shared heritage').replace('.template-index','.heritage-site')
save('snippets/heritage-shell.liquid',s)
d=json.loads((BEFORE/'config/settings_data.json').read_text());d['current'].update(color_background='#f7f5ef',color_text='#132039',color_line='#dedad0',color_muted='#5e6269')
save('config/settings_data.json',json.dumps(d,ensure_ascii=False,indent=2)+'\n')
for p in (BEFORE/'templates').glob('product*.json'):
 d=json.loads(p.read_text());changed=False
 for section in d['sections'].values():
  for k in ['title_override','heading']:
   v=section.get('settings',{}).get(k)
   if v and v.isupper():section['settings'][k]=v.title();changed=True
 if changed:save(str(p.relative_to(BEFORE)),json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print('Prepared shell, global colors and product display headings')
