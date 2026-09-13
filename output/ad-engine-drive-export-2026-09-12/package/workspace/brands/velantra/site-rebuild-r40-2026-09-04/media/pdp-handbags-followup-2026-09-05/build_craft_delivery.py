"""Generate comparison sheets and export only visually accepted provider images."""
import hashlib, json
from pathlib import Path
from PIL import Image, ImageDraw, ImageOps, ImageEnhance

ROOT = Path(__file__).resolve().parent

def main():
    data = json.loads((ROOT/'prompts-and-provenance.json').read_text())
    qa_path = ROOT/'qa.json'
    qa = json.loads(qa_path.read_text()) if qa_path.exists() else {'panels':{}}
    by_family = {}
    for row in data['panels']: by_family.setdefault(row['family'],[]).append(row)
    (ROOT/'qa').mkdir(exist_ok=True)
    (ROOT/'web').mkdir(exist_ok=True)
    deliveries = []
    for family, rows in by_family.items():
        sheet = Image.new('RGB',(1400,1130),'#eeeae5'); d = ImageDraw.Draw(sheet)
        for c,row in enumerate(rows):
            for r in range(3):
                path = row['source_crop']['path'] if r == 0 else row.get('output')
                if not path or not Path(path).exists(): continue
                im = Image.open(path).convert('RGB')
                if r == 2:
                    side = im.width; height = int(side*272/341)
                    im = im.crop((0,(im.height-height)//2,side,(im.height+height)//2))
                    im = ImageEnhance.Color(im).enhance(.8)
                tile = ImageOps.contain(im,(340,340))
                x=c*350;y=r*375
                sheet.paste(tile,(x+(350-tile.width)//2,y+(340-tile.height)//2))
                label=['SOURCE','GENERATED','341:272 / CSS saturation .8'][r]
                d.text((x+7,y+345),row['panel']+' | '+label,fill='black')
            verdict = qa['panels'].get(row['id'],{})
            if verdict.get('status') != 'accepted': continue
            out = Path(row['output'])
            digest = hashlib.sha256(out.read_bytes()).hexdigest()
            if verdict.get('sha256') != digest: raise RuntimeError('QA hash mismatch: '+row['id'])
            im=Image.open(out).convert('RGB');im.thumbnail((1024,1024),Image.Resampling.LANCZOS)
            dest=ROOT/'web'/(row['id']+'.jpg');im.save(dest,'JPEG',quality=90,subsampling=0,optimize=True)
            deliveries.append({'id':row['id'],'family':family,'color':row['color'],'panel':row['panel'],'heading':row['label'],'alt':row['alt'], 'theme_asset':dest.name,'path':str(dest),'dimensions':list(im.size),'bytes':dest.stat().st_size,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(), 'provider_png':row['output'],'provider_url':row['provider_asset']['source_url'],'provider_sha256':digest,'source':row['source'],'source_crop':row['source_crop'],'qa':verdict})
        sheet.save(ROOT/'qa'/(family+'-source-generated-crop.jpg'),quality=93)
    manifest={'date':'2026-09-05','scope':'Six active handbag families, four craft detail macros each','accepted_count':len(deliveries),'requested_count':24,'complete':len(deliveries)==24,'files':deliveries,'processing':'Provider PNG retained. Web export is uniform downscale to 1024x1024 JPEG only. Center crop/desaturation is QA preview only.','claims':'Illustrative finished-product macros. No certification of physical dimensions, material composition or manufacturing process.'}
    (ROOT/'delivery-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(f'{len(deliveries)}/24 approved JPG exports; comparison sheets refreshed.')

if __name__ == '__main__': main()
