from pathlib import Path
import json,re,sys
project=Path(__file__).resolve().parents[1]
manifest=json.loads((project/'media/production-manifest.json').read_text())
source=(project/'theme/snippets/studio-image-url.liquid').read_text()
mapping={}
for match in re.finditer(r'when\s+([\d,\s]+)\s*-%}\s*{{-\s*[\'\"]([^\'\"]+)',source):
    for key in re.findall(r'\d+',match.group(1)):
        mapping[int(key)]=match.group(2)
entries=[]
for product in manifest['products']:
    for media in product['images']:
        ids=[media.get('source_image_id'),media.get('shopify_media_id'),media.get('shopify_image_source_id')]
        mapped={mapping[mid] for mid in ids if mid in mapping}
        entries.append({'handle':product['handle'],'source_image_id':media['source_image_id'],'mapped_assets':sorted(mapped),'expected_asset':media['theme_asset'],'mapped':bool(mapped),'files_exist':bool(mapped) and all((project/'theme/assets'/a).exists() for a in mapped),'correct':mapped=={media['theme_asset']},'reviewed':media.get('visual_review',{}).get('approved') is True})
report={'source_products':manifest['source_product_count'],'source_images':manifest['source_image_count'],'mapped_images':sum(x['mapped'] for x in entries),'unmapped_images':[x for x in entries if not x['mapped']],'incorrect_maps':[x for x in entries if x['mapped'] and not x['correct']],'missing_assets':[x for x in entries if x['mapped'] and not x['files_exist']],'mapped_unapproved':[x for x in entries if x['mapped'] and not x['reviewed']],'media_id_fallback_present':'media_id' in source and 'media_id: media.id' in (project/'theme/snippets/product-gallery.liquid').read_text(),'studio_toggle_present':'settings.use_studio_catalog' in source,'mappings':entries}
report['complete']=not any(report[k] for k in ['unmapped_images','incorrect_maps','missing_assets','mapped_unapproved']) and report['media_id_fallback_present'] and report['studio_toggle_present']
(project/'research/commerce-media-linkage-audit.json').write_text(json.dumps(report,indent=2))
print(json.dumps({k:v for k,v in report.items() if k not in ['mappings','unmapped_images']},indent=2))
if '--complete' in sys.argv and not report['complete']:
    sys.exit(1)
