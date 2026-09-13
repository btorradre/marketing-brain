from pathlib import Path
from PIL import Image
import json
P=Path(__file__).resolve().parents[1]
shared=['cognac-front','cognac-quarter','cognac-handle-detail','cognac-clasp-detail','cognac-interior','cognac-architecture','army-front','espresso-front','black-front']
keys=shared+[f'{sex}-{scene}' for sex in ['women','men'] for scene in ['hero-v2','touch-v2','outdoor-v2','car']]
keys += [f'{sex}-{color}-hero' for sex in ['women','men'] for color in ['army','espresso','black']]
keys += [task['key'] for task in json.loads((P/'edit/all-colors-prompts.json').read_text())]
missing=[key for key in keys if not (P/'media'/f'{key}.png').exists()]
assert not missing, f'Missing gallery images: {missing}'
selected={}
for key in keys:
 source=P/'media'/f'{key}.png'
 clean=P/'media'/f'{key}-clean.png'
 if clean.exists():source=clean
 natural=P/'media'/f'{key}-natural.png'
 if natural.exists():source=natural
 natural2=P/'media'/f'{key}-natural2.png'
 if natural2.exists():source=natural2
 im=Image.open(source).convert('RGB');im.thumbnail((1200,1600))
 dest=P/'theme/assets'/f'wk-editorial-{key}.webp';im.save(dest,quality=88,method=6)
 selected[key]={'source':str(source),'asset':'assets/'+dest.name,'width':im.width,'height':im.height,'bytes':dest.stat().st_size}
(P/'edit/selected-media.json').write_text(json.dumps(selected,indent=2))
print('Prepared',len(selected),'selected web images;',sum(x['bytes'] for x in selected.values()),'bytes total')
