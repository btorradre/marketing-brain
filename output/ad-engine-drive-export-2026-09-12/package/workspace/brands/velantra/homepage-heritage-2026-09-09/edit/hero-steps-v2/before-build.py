import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
urls = json.loads((ROOT / 'media/asset-urls.json').read_text())

def campaign(name, heading, asset, **kwargs):
    settings = {
        'eyebrow': name, 'heading': heading,
        'image_url': urls['heritage-' + asset],
        'alignment': 'center', 'shade': 45,
        'desktop_height': 90, 'mobile_height': 90,
        'image_position': '50% 50%', 'mobile_position': '50% 50%',
    }
    settings.update(kwargs)
    return {'type': 'heritage-campaign', 'settings': settings}

sections = {
    'opening': campaign('VELANTRA', 'A Life Well Carried', 'vivienne-heritage-hero',
        is_hero=True, image_alt='A woman carrying the Chocolate Vivienne outside a stone country house',
        copy='<p>Distinctive bags for the places, people, and moments that make a life.</p>',
        link='/collections/handbags', link_label='Shop Handbags',
        second_link='/products/velantra-vivienne?variant=44462686830657', second_label='Discover the Vivienne',
        alignment='left',mobile_position='50% 50%',mobile_image_url=urls['heritage-vivienne-heritage-mobile'],shade=55),
    'autumn': campaign('THE COLETTE', 'The Autumn Edit', 'colette-autumn',
        image_alt='The Caramel Colette wool tote beside an ivory knit in a warm paneled room',
        copy='<p>Soft textures. Warm tones. A new season of familiar pleasures.</p>',
        link='/products/the-colette-wool-tote?variant=44263482425409', link_label='Discover the Colette',
        alignment='right', image_position='36% 50%', mobile_position='36% 50%', shade=45),
    'world': {
        'type':'heritage-world',
        'settings':{'heading':'The World of Velantra','copy':'<p>Explore the collection, from everyday signatures to weekends away.</p>'},
        'blocks': {
            'signature':{'type':'world','settings':{
                'image_url':urls['heritage-vivienne-signature'],
                'image_alt':'Chocolate Vivienne leather, braided trim and warm gold fittings',
                'image_position':'50% 45%', 'eyebrow':'THE VIVIENNE', 'heading':'The Signature',
                'link':'/products/velantra-vivienne?variant=44462686830657','link_label':'Explore the Vivienne'}},
            'weekend':{'type':'world','settings':{
                'image_url':urls['heritage-eleanor-weekend'],
                'image_alt':'The Black Eleanor Weekender carried at a country-house doorway',
                'image_position':'50% 50%', 'eyebrow':'THE ELEANOR', 'heading':'The Weekend Away',
                'link':'/products/velantra-weekender?variant=44355431596097','link_label':'Explore the Eleanor'}},
        },
        'block_order':['signature','weekend'],
    },
    'accessories':campaign('THE ACCESSORIES COLLECTION', 'The Finishing Touch', 'horse-finishing-touch',
        image_alt='The Brown Horse Charm with its pale loop, resting on herringbone wool and walnut',
        copy='<p>A little character. Entirely your own.</p>',
        link='/collections/accessories',link_label='Shop Accessories',
        alignment='right',mobile_position='42% 50%',shade=45,desktop_height=80,mobile_height=85),
    'closing':{'type':'heritage-closing','settings':{
        'eyebrow':'VELANTRA','heading':'Collected for the Everyday',
        'copy':'<p>A favorite bag becomes part of your days. The morning you linger over. The weekend you look forward to. The places that feel like you.</p>',
        'link':'/collections/handbags','link_label':'Explore the Collection'}},
}
path=ROOT/'theme/templates/index.json';path.parent.mkdir(parents=True,exist_ok=True)
path.write_text(json.dumps({'sections':sections,'order':list(sections)},ensure_ascii=False,indent=2)+'\n')
locale=json.loads((ROOT/'before/locales/en.default.json').read_text())
locale['heritage']={'shipping':'Free shipping over $75','signature':'Luxury, without the logo'}
path=ROOT/'theme/locales/en.default.json';path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(locale,ensure_ascii=False,indent=2)+'\n')
validation=ROOT/'validation-theme'
shutil.copytree(ROOT.parent/'site-rebuild-r40-2026-09-04/theme',validation,symlinks=True,dirs_exist_ok=True)
for path in (ROOT/'theme').rglob('*'):
    if path.is_file():
        target=validation/path.relative_to(ROOT/'theme');target.parent.mkdir(parents=True,exist_ok=True)
        if target.is_symlink():target.unlink()
        shutil.copy2(path,target)
print('Built homepage template, localization and validation tree')
