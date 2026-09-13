"""Prepare lossless source crops and auditable GPT Image 2 panel requests."""
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw

ROOT = Path(__file__).resolve().parent
SOURCES = {x['family']: x for x in json.loads((ROOT / 'selected-sources.json').read_text())}
SPECS = {
    'meridian': [
        ('material', (230, 435, 410, 615), 'the uninterrupted warm Brown pebbled leather front surface and its natural shallow fold', 'Pebbled leather', 'Close-up of the Meridian Brown leather grain and natural front-body fold.'),
        ('stitching', (130, 390, 350, 610), 'the left front edge, its single evidenced seam, tonal stitching and adjacent pebbled leather', 'Tonal stitching', 'Detail of the Meridian’s stitched front edge in Brown.'),
        ('finishing', (540, 425, 740, 625), 'the lower right curved gusset, layered edge finish and adjacent leather; retain the exact visible edge layers', 'Finished edges', 'Close-up of the Meridian’s curved side gusset and finished leather edge.'),
        ('hardware', (315, 315, 500, 500), 'the exact small silver center plate with its post and the two separate silver slotted belt ends; preserve their count, shapes and overlap', 'Silver details', 'Detail of the Meridian’s silver center fitting and slotted belt ends.'),
    ],
    'camille': [
        ('material', (610, 820, 820, 1030), 'only the cream canvas front, its tiny natural woven texture and soft fabric undulation', 'Canvas texture', 'Close-up of the Camille Navy tote’s cream canvas weave.'),
        ('stitching', (430, 855, 690, 1115), 'the flat Navy front strip, two fine cream stitch lines along its edges, and the cream canvas either side', 'Contrast stitching', 'Close-up of the Camille’s Navy front strip and contrasting edge stitching.'),
        ('finishing', (920, 1020, 1240, 1340), 'the lower right cream canvas pleat and narrow Navy bottom border with the source edge and contact shadow; preserve only the visible construction', 'Shaped corners', 'Detail of the Camille’s soft lower-corner pleat and Navy base trim.'),
        ('hardware', (555, 535, 905, 885), 'the narrow Navy stitched front belt and exact small gold center closure against cream canvas; preserve the closure outline and mechanism state exactly', 'Gold details', 'Close-up of the Camille’s gold center fitting on its Navy front belt.'),
    ],
    'colette': [
        ('material', (420, 1150, 690, 1420), 'only the pale oatmeal felt-like body, short matte fibers and soft heathered texture', 'Soft texture', 'Close-up of the Colette’s pale felt-like surface and short matte fibers.'),
        ('stitching', (250, 825, 820, 1395), 'the narrow Caramel leather belt, its fine tonal edge stitch lines, the broad pale felt keeper and adjacent felt body; retain exact layer order', 'Tonal stitching', 'Detail of the Colette’s stitched Caramel belt passing through a felt keeper.'),
        ('finishing', (920, 1250, 1260, 1590), 'the lower right felt gusset and its curved seam, thick felt edge and soft contact shadow, exactly as cropped', 'Shaped edges', 'Close-up of the Colette’s felt side gusset and curved lower edge.'),
        ('hardware', (710, 1050, 1170, 1510), 'the single curved Caramel belt end and its one round gold-tone cap over the pale felt body, with the exact cap profile and tonal stitching', 'Gold details', 'Detail of the Colette’s curved Caramel belt end and round gold-tone cap.'),
    ],
    'delphine': [
        ('material', (570, 1500, 940, 1870), 'only the cream diagonal canvas twill and its slightly curved lower body edge; keep the substantial diagonal weave and no extra seam', 'Canvas texture', 'Close-up of the Delphine Light Chocolate bag’s diagonal canvas twill.'),
        ('stitching', (310, 505, 710, 905), 'the burnished Light Chocolate leather flap and curved upper stitched edge with the existing small gold corner rivet; preserve exact stitching, grain and edge thickness', 'Tonal stitching', 'Detail of the Delphine’s curved leather flap edge and tonal stitching.'),
        ('finishing', (110, 1420, 630, 1940), 'the lower left burnished leather corner cap, its curved seam, adjacent diagonal canvas and only the existing visible gold foot', 'Finished corners', 'Close-up of the Delphine’s leather corner reinforcement and curved seam.'),
        ('hardware', (580, 1130, 1020, 1570), 'the single diagonal slotted gold belt-end plate and its two round rivets, warm leather belt and underlying cream diagonal canvas; preserve the exact outline and slot proportions', 'Gold details', 'Detail of the Delphine’s slotted gold belt end against cream canvas.'),
    ],
    'juliette': [
        ('material', (285, 1330, 725, 1770), 'only the matte warm Camel suede body with visible directional nap and natural soft folds', 'Suede texture', 'Close-up of the Juliette Camel suede nap and soft natural folds.'),
        ('stitching', (135, 740, 635, 1240), 'the dark cool-brown leather collar edge, its tonal seam, the narrow visible strap and the adjacent Camel suede exactly as in the crop', 'Tonal stitching', 'Detail of the Juliette’s dark leather collar seam against Camel suede.'),
        ('finishing', (80, 1690, 510, 2120), 'the lower left dark leather corner cap, its curved tonal seam and single small antique-brass stud, with the adjacent Camel suede and neutral floor', 'Finished corners', 'Close-up of the Juliette’s leather corner cap, curved seam and brass stud.'),
        ('hardware', (1190, 850, 1570, 1230), 'the one flat antique-brass bar on the dark decorative front strap, adjacent vertical leather keeper and collar edge; preserve the actual tab count visible in the crop', 'Brass details', 'Detail of the Juliette’s antique-brass bar and dark leather front strap.'),
    ],
    'weekender': [
        ('material', (350, 2250, 1100, 3000), 'only the real Army Green Weekender’s dark olive canvas, its tiny woven texture and soft body undulation; clean only loose incidental lint without changing the weave', 'Canvas texture', 'Close-up of the Eleanor Weekender’s Army Green canvas weave.'),
        ('stitching', (130, 1420, 1030, 2320), 'the actual softly contoured warm brown flap edge, its fine tonal stitching and the adjacent brown leather band; preserve the visible horizontal oval plate exactly', 'Tonal stitching', 'Detail of the Eleanor Weekender’s contoured leather flap and tonal edge stitching.'),
        ('finishing', (380, 2550, 1380, 3550), 'the lower left warm brown leather corner reinforcement, curved edge seam, adjacent Army Green canvas and only a little floor; preserve the actual source crop', 'Finished corners', 'Close-up of the Eleanor Weekender’s leather corner reinforcement and Army Green canvas.'),
        ('hardware', (340, 1260, 1290, 2210), 'the exact HORIZONTAL oval gold plate with its open shaped slot and two tiny side rivets on the warm brown flap; preserve horizontal orientation and the source closure state, nearby curved flap edge and handle-root fragment', 'Gold details', 'Close-up of the Eleanor Weekender’s horizontal oval gold fitting on its leather flap.'),
    ],
}

COMMON = '''Use case: lighting-weather. Product craftsmanship editorial photograph for a Shopify PDP. The single input image is an EXACT CROP of the selected product reference and is the sole authority for visible construction. Keep this same tight macro crop and camera angle: do not reconstruct a whole bag, invent an unseen angle, or add product parts outside the crop. Restage only the light into a consistent warm-neutral luxury editorial look: soft broad diffuse key light, gentle raking highlights, natural material texture, soft shadows, restrained color and realistic depth of field. If background is visible, make only that area a quiet warm ivory studio surface. If material fills the crop, keep the entire frame filled by that material; do not add a white margin. Keep the product's exact color, shapes, seams, layer order, hardware count and scale-relative details. Do not embellish stitching, add surface features or move closure parts. Composition: square 1:1, retain the crop's primary detail in the middle 70 percent height so a 341:272 center crop remains clear. Photography only, no text, labels, hands, tools, logos, watermark, collage, workshop, certificate, dimensions or process demonstration. This is an illustrative macro of a finished product, not a documentary of manufacturing. Subject: '''

def main():
    path = ROOT / 'prompts-and-provenance.json'
    if path.exists():
        raise RuntimeError('Manifest already exists; do not overwrite job state')
    cropdir = ROOT / 'source-crops'; cropdir.mkdir(exist_ok=True)
    panels = []
    sheet = Image.new('RGB', (1400, 6 * 380), '#eeeae5'); draw = ImageDraw.Draw(sheet)
    for ri, (family, specs) in enumerate(SPECS.items()):
        source = SOURCES[family]
        for ci, (kind, box, subject, label, alt) in enumerate(specs):
            ident = family + '-craft-' + kind
            source_path = source['source']
            if family == 'weekender' and kind == 'finishing':
                source_path = str(Path(source_path).with_name('AG-closed-three-quarter.jpg'))
            im = Image.open(source_path).convert('RGB')
            crop = im.crop(box)
            dest = cropdir / (ident + '.png'); crop.save(dest)
            row = {'id': ident, 'family': family, 'color': source['color'], 'panel': kind,
                   'source': source_path, 'source_sha256': hashlib.sha256(Path(source_path).read_bytes()).hexdigest(),
                   'source_crop': {'path': str(dest), 'box_xyxy': box, 'size': crop.size, 'processing': 'Lossless rectangular input crop only; original product pixels retained.', 'sha256': hashlib.sha256(dest.read_bytes()).hexdigest()},
                   'prompt': COMMON + subject + '.', 'label': label, 'alt': alt, 'status': 'planned'}
            panels.append(row)
            tile = ImageOps.contain(crop, (340, 340)); x = ci*350; y = ri*380
            sheet.paste(tile, (x+(350-tile.width)//2, y)); draw.text((x+7,y+345), ident, fill='black')
    manifest = {'provider': 'Kie existing ad-engine GPT Image 2 route', 'model': 'gpt-image-2-image-to-image', 'aspect_ratio': '1:1', 'resolution': '2K', 'panels': panels,
                'scope': 'Six active handbag families; Vivienne set delivered separately. No live catalog/theme writes.', 'metric_scale': 'Not independently verifiable. Crops preserve source-relative detail only.',
                'source_authority': 'Weekender is real-product video-still lineage; Delphine corrected generated creative master; Colette/Juliette generated current creative targets; Camille/Meridian current catalog supplier-photo lineage, no independent material certification.'}
    path.write_text(json.dumps(manifest, indent=2)+'\n'); sheet.save(ROOT/'source-crop-contact.jpg',quality=94)
    print(f'Prepared {len(panels)} panels')

if __name__ == '__main__':
    main()
