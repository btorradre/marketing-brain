"""Apply draft-only PDP stories using documented catalog/product evidence."""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
THEME = ROOT / 'theme'
def read(path):
    return json.loads(re.sub(r'^/\*.*?\*/\s*', '', path.read_text(), flags=re.S))
def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')
def p(text): return '<p>'+text+'</p>'

stories = {
 'vivienne': ('Vegetable-tanned leather', 'Braided upper edge', 'Expected to ship October',
  'The Vivienne begins with vegetable-tanned leather: a softly grained body framed by smoother trim, with a relaxed silhouette that settles into natural folds. A braided upper edge gives the bag its distinctive outline, while rolled handles, a hanging key bell and warm gold-tone fittings draw the eye to the finishing. The inward-falling leather belts and curved corner panels bring definition to the slouch. A bag with presence, made to become part of your everyday rhythm.',
  'Approximate dimensions: 38 × 27 × 20 cm (W × H × D). Rolled top handles and a detachable shoulder strap. Braided upper edge, inward-falling belt details, key bell and curved corner panels.',
  'Vegetable-tanned leather with a grained body and smoother trim; gold-tone fittings. Wipe gently with a soft, dry cloth. Avoid soaking, direct heat and prolonged sunlight. Store lightly filled in a cool, dry place.'),
 'weekender': ('Canvas with leather trim', 'Structured carryall', 'Expected to ship mid September 2026',
  'The Weekender brings the ease of canvas together with the definition of leather. Cognac, Espresso and Army Green pair a canvas body with a smooth leather flap, rolled handles and reinforced corners; Black is made entirely in leather. The generous, structured silhouette gives the bag its composed shape, with a belted front and contrast stitching to finish the outline. From the first packing list to the journey home, every detail belongs to a bag made for getting away.',
  'Approximate dimensions: 18 × 14.5 × 7 in (W × H × D). Structured body, rolled top handles, a fold-over flap and reinforced leather corners. Cognac, Espresso and Army Green have canvas bodies; Black is all leather.',
  'Black: leather throughout. Cognac, Espresso and Army Green: canvas body with leather flap, handles and trim. Spot-clean canvas carefully with a barely damp cloth; wipe leather with a soft, dry cloth. Air-dry away from heat and store in a cool, dry place.'),
 'meridian-tote': ('Grained leather', 'Polished silver-tone fittings', '',
  'Grained leather gives the Meridian its depth and gently structured shape. The wide body is framed by short, flat handles and folded side panels, with polished silver-tone fittings providing a quiet point of contrast. A narrow belted front keeps the design precise, while the open top and central zipped compartment bring order to the day. Carried in the hand or worn with its detachable strap, the Meridian moves easily between the practical and the considered.',
  'Approximate dimensions: 37 × 24 × 15 cm (W × H × D). Short, flat top handles and a detachable adjustable strap. Open top, folded side panels and a central zipped compartment between two open sections.',
  'Grained leather with silver-tone fittings. Wipe with a soft, dry cloth. Keep away from prolonged moisture, direct heat and sunlight. Test any suitable leather conditioner on a discreet area first and store lightly filled.'),
 'colette': ('Brushed wool with leather trim', 'Belted, softly structured form', 'Expected to ship early October',
  'Brushed wool gives the Colette a soft, tactile surface, balanced by smooth leather at the handles and across the belted front. The pale body has a gently structured, east-west shape, with broad side panels and softly rounded corners. Two curved leather belt ends, finished with warm gold-tone caps, add movement to the clean silhouette. Open at the top and comfortable in the hand, it brings the texture of a favorite coat to the bag you carry through the day.',
  'Approximate dimensions: 50 × 26 × 18 cm (W × H × D). Approximate handle drop: 16 cm. Open top, broad side panels, felt handle legs with leather-wrapped upper arcs and two separate curved belt ends with gold-tone caps.',
  'Brushed wool body with leather trim and gold-tone fittings. Gently lift the nap with a soft garment brush. Spot-clean with a barely damp cloth and let air-dry. Wipe leather with a dry cloth; store upright, away from direct heat and sunlight.'),
 'delphine': ('Woven canvas with leather trim', 'Gold-tone turn-lock', '',
  'The Delphine pairs tightly woven canvas with a smooth leather flap, rolled top handles and curved leather corners. The contrast gives its compact silhouette both texture and definition. Gold-tone fittings, a small key bell and belted front straps complete the composition, with visible stitching tracing the leather edges. A lined interior and zipped pocket keep the essentials together. Considered in proportion and rich in detail, it is a bag for the day that continues into evening.',
  'Approximate dimensions: 25 × 22 × 14 cm (W × H × D). Rolled top handles and a detachable long strap. Lined interior with a zipped pocket, leather corner panels, gold-tone turn-lock and metal feet.',
  'Woven canvas body with leather flap, handles and trim; gold-tone fittings. Spot-clean canvas with a soft, barely damp cloth. Wipe leather with a dry cloth. Allow to air-dry away from heat and store lightly filled, out of direct sunlight.'),
 'juliette': ('Suede with leather trim', 'Soft, open-top silhouette', '',
  'Soft suede gives the Juliette its warm, matte depth, while a smooth leather collar draws a clear line around the open top. Rolled leather handles and matching corner panels frame the relaxed body, allowing the suede to fall into broad, natural folds. A slim front belt, narrow hanging ties and warm metal fittings keep the finishing understated. The result is an easy, tactile tote whose character comes from the meeting of materials and the way it is carried.',
  'Approximate dimensions: 18.5 × 18.5 × 8 in (W × H × D). Short rolled handles for hand or forearm carry. Open top, leather collar, reinforced leather corners, slim front belt and hanging ties.',
  'Suede body with smooth leather collar, handles and corners. Brush suede gently with a soft, dry suede brush, following the nap. Wipe leather with a dry cloth. Avoid moisture, heat and direct sun; store lightly filled.'),
 'boat-tote-2': ('Woven canvas', 'Belted front', '',
  'Canvas sets the tone for the Camille: tactile, relaxed and ready to become part of the day. Its open-top shape is defined by long handles, vertical front strips and a slim belt with a small gold-tone fitting. The two-tone colorways bring crisp contrast to the canvas body, while the solid editions give the silhouette a different expression. With a broad base and an easy carryall shape, the Camille feels equally at home on a morning errand or a weekend away.',
  'Approximate dimensions: 20 × 14 × 8 in (W × H × D), approximately 51 × 36 × 20 cm. Approximate handle drop: 10 in. Open-top carryall with a belted front and a defined base. Handle and upper-panel construction vary between two-tone and solid colorways.',
  'Woven canvas with contrasting or tonal trim and gold-tone fittings. Spot-clean with a soft, barely damp cloth. Do not soak; air-dry fully before storage. Keep out of prolonged direct sunlight.'),
 'bag-scarf': ('Lightweight silk-blend fabric', 'Soft drape', '',
  'A soft silk-blend fabric gives the Bag Scarf its lightness and fluid drape. Color, print and a gentle sheen turn a simple knot into a considered finishing touch, whether wound around a handle or left with the tails falling loosely. Each pattern brings a different mood to the bag beside it. It is a small way to make a familiar piece feel personal again.',
  'Lightweight printed scarf with softly finished edges. Tie around a bag handle or style as a hair or neck accessory.',
  'Silk-blend fabric. Spot-clean gently or dry-clean; avoid wringing. Store flat or loosely rolled and keep out of prolonged sunlight.'),
 'bag-organizer': ('Structured felt', 'Removable dividers', '',
  'Structured felt gives the Bag Organizer a soft touch and a shape that sits neatly inside a tote. Interior pockets and removable dividers create a place for the small things that tend to disappear, while the open top keeps them easy to find. The quiet neutral finish sits comfortably beside different bag interiors. A practical detail that brings a little more order to the everyday, and moves with you when it is time to change bags.',
  'Choose a size to suit your bag’s interior. Approximate L × D × H: Small 8.66 × 4.5 × 5.3 in; Medium 9.25 × 5.1 × 5.9 in; Large 11.4 × 5.5 × 7.1 in. Multiple pockets and removable dividers. Pictured contents are not included.',
  'Structured felt. Spot-clean gently with a barely damp cloth and air-dry completely. Reshape before storing.'),
 'horse-charm': ('Smooth leather', 'Horse silhouette', '',
  'Smooth leather gives the Horse Charm its soft shape and clear silhouette. The small profile, layered details and considered color combinations bring a playful equestrian note to an everyday bag. Its character lies in the outline and the finishing, with each version offering its own arrangement of color and detail. Attach it to a favorite handle for a personal touch that feels easy to change with the day.',
  'Decorative horse-shaped bag charm. Colorways have their own attachment and finishing details; refer to the selected color’s photographs.',
  'Smooth leather with color-specific trims and fittings. Wipe with a soft, dry cloth. Keep away from prolonged moisture and store without crushing.'),
 'cherry-charm': ('Decorative finish with metal fittings', 'Cherry-shaped accent', '',
  'Two cherries and a small leaf bring a bright, playful detail to the Cherry Charm. The rounded forms and considered color combinations create a lively contrast beside a simple tote or top-handle bag. Each colorway has its own surface finish and construction, with metal fittings completing the attachment. A small accent for making an everyday bag feel more like your own.',
  'Decorative cherry-shaped charm with a leaf detail and bag attachment. Construction and finish vary by colorway; use the selected color’s photographs as your guide.',
  'Decorative body with metal fittings; surface finish varies by colorway. Wipe gently with a soft, dry cloth. Avoid soaking, abrasive cleaners and prolonged direct sunlight.'),
 'boat-tote-keychain': ('Textured body with contrast trim', 'Miniature tote silhouette', '',
  'The Boat Tote Keychain brings the familiar lines of a carryall into a miniature accessory. A textured pale body, contrasting handles and tiny belted front give it definition, while a short chain and gold-tone ring complete the piece. The appeal is in the small details: the trim, the stitching and the neatly framed silhouette. Add it to your keys or a favorite bag for a quiet echo of the full-size tote.',
  'Miniature decorative tote with a short linked chain and gold-tone key ring. Contrast handles, vertical front strips and a tiny belted front.',
  'Textured fabric-look body with smooth trim and gold-tone fittings. Wipe gently with a soft, dry cloth. Keep away from prolonged moisture and abrasive cleaners.'),
 'ingrid': ('Burnished leather finish', 'Belted top-handle silhouette', '',
  'The Ingrid’s burnished surface gives the bag depth, with tonal variation and natural-looking folds playing across its broad silhouette. Rolled handles, pinched side panels and curved corner reinforcements define the shape. A slender belt and warm gold-tone fittings bring focus to the front, with finishing details that vary between colorways. It is an expressive take on the top-handle bag, balancing a generous body with a composed outline.',
  'Approximate dimensions: 15 × 12 × 6.3 in (L × H × D). Rolled handles, folded upper panel, pinched side panels and reinforced corners. Front fitting design varies by colorway.',
  'Burnished leather-look surface with gold-tone fittings. Wipe with a soft, dry cloth. Avoid soaking, abrasive cleaners, direct heat and prolonged sunlight. Store lightly filled.'),
 'portico-bucket-bag': ('Grained finish', 'Compact bucket silhouette', '',
  'The Portico takes its character from a compact bucket shape and a richly grained surface. A gently flared opening sits above a rounded base, while two flat handles keep the outline simple. The vertical front strap, hanging gold-tone padlock and separate key cover form the finishing details. With its sculpted proportions and understated hardware, it brings a considered point of interest to an everyday look.',
  'Compact bucket shape with two flat handles, a flared opening and rounded base. Vertical front strap, hanging padlock and separate key cover.',
  'Grained surface with gold-tone fittings. Wipe gently with a soft, dry cloth. Avoid soaking and abrasive cleaners. Store lightly filled, away from heat and sunlight.'),
 'bow-tote': ('Ivory canvas with woven ribbon', 'Hand-tied bow', '',
  'Ivory canvas gives the Rosalie its crisp, gently structured shape. A woven ribbon passes through warm gold-tone grommets and ties into a generous bow, letting color become the focal point of the design. Flat canvas handles and a defined base keep the little tote composed, while floral lining adds a softer detail inside. From the ribbon’s drape to the rounded corners, the Rosalie brings a light, personal touch to everyday dressing.',
  'Mini tote with flat canvas handles, an open top, woven ribbon bow and floral fabric lining. Sand, Denim and Pink refer to the ribbon and lining treatment; the canvas body remains ivory.',
  'Ivory canvas, woven ribbon and floral fabric lining with gold-tone fittings. Spot-clean gently with a barely damp cloth and air-dry. Store without crushing the ribbon.'),
 'straw-birkin': ('Woven straw with smooth trim', 'Crossed front straps', '',
  'Woven straw gives the Sofia its warm texture and gently structured shape. Smooth handles and a folded upper panel frame the basket-like body, while crossed front straps and visible stitching keep the finishing precise. The contrast between the woven surface and smooth trim gives the design its character. An easy companion for lighter days, with a silhouette that feels considered from the market morning to a long afternoon outside.',
  'Approximate dimensions: 12 × 9.5 × 6 in (W × H × D). Approximate handle drop: 4 in. Woven body, folded upper panel, short handles and crossed front straps.',
  'Woven straw body with smooth trim. Dust gently with a soft, dry brush and wipe trim with a dry cloth. Avoid soaking and excessive heat. Store upright without crushing the weave.'),
 'boat-tote-legacy': ('Canvas with contrast trim', 'Everyday carryall', '',
  'Canvas gives the Boat Tote its relaxed character, framed by contrasting handles and a belted front. The textured body and visible stitching keep the construction part of the design, with a broad carryall shape that feels easy to reach for. Its appeal is in that meeting of practical form and considered detail: a familiar silhouette with enough personality to make the everyday feel a little more your own.',
  'Canvas carryall with contrast handles, trim and a belted front. Construction varies by listing and colorway; refer to the selected product’s photographs.',
  'Canvas body with contrasting trim. Spot-clean gently with a barely damp cloth and air-dry fully. Avoid soaking, direct heat and prolonged sunlight.')
}

changed=[]
for suffix, (material, detail, lead, story, details, care) in stories.items():
    path=THEME/'templates'/f'product.{suffix}.json'; data=read(path); main=data['sections']['main']
    main['settings'].update(description_override=p(story),fact_material=material,fact_detail=detail,
        preorder_lead_time=lead,show_facts=True,show_policies=False,show_shipping_summary=True)
    if suffix=='weekender': main['settings']['fact_material_black']='All leather'
    oldblocks=main.get('blocks',{})
    retained={k:v for k,v in oldblocks.items() if v['type']!='accordion'}
    main['blocks']={
      'story_details':{'type':'accordion','settings':{'heading':'Details','content':p(details),'open':False}},
      'story_care':{'type':'accordion','settings':{'heading':'Materials and Care','content':p(care),'open':False}},
      **retained}
    main['block_order']=['story_details','story_care']+list(retained)
    save(path,data);changed.append(str(path.relative_to(THEME)))

default=THEME/'templates/product.json';data=read(default);data['sections']['main']['settings'].update(show_shipping_summary=True,show_policies=False);save(default,data);changed.append(str(default.relative_to(THEME)))
(Path(__file__).parent/'qa/revision-2/story-template-files.json').write_text(json.dumps(changed,indent=2))
print('Updated',len(changed),'product templates; preserved other sections and app blocks.')
