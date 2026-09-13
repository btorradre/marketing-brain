from pathlib import Path
import json,shutil
P=Path(__file__).resolve().parents[1]
selected=json.loads((P/'edit/selected-media.json').read_text())
assert len(selected)==56
prompts=json.loads((P/'delivery/PROMPTS.json').read_text())
by_key={r['selected_asset']:r for r in prompts}
catalog={}
for filename in ['all-colors-prompts.json','all-colors-correction-prompts.json','all-colors-skin-correction-prompts.json','all-colors-sleeve-correction-prompts.json']:
 for row in json.loads((P/'edit'/filename).read_text()):catalog[row['key']]={**row,'prompt_file':'../edit/'+filename}
for key,row in selected.items():
 shutil.copy2(P/'theme'/row['asset'],P/'delivery/images'/Path(row['asset']).name)
 source_key=Path(row['source']).stem
 if source_key in catalog:by_key[key]={'selected_asset':key,'source_png':row['source'],**catalog[source_key]}
 elif key in catalog:by_key[key]={'selected_asset':key,'source_png':row['source'],**catalog[key]}
 assert key in by_key,key
(P/'delivery/PROMPTS.json').write_text(json.dumps([by_key[k] for k in selected],indent=2))
manifest=[]
for sex in ['women','men']:
 main=json.loads((P/f'theme/templates/product.wk-editorial-{sex}.json').read_text())['sections']['main']
 assert len(main['block_order'])==40
 for i,block in enumerate(main['block_order'],1):
  settings=main['blocks'][block]['settings']
  manifest.append({'audience':sex,'position':i,**{k:settings[k] for k in ['color','kind','caption','url']}})
(P/'delivery/gallery-manifest.json').write_text(json.dumps(manifest,indent=2))
print('Packaged',len(selected),'selected images and',len(manifest),'placements')
