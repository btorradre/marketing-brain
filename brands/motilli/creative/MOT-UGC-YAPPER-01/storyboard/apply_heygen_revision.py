"""Apply the user's HeyGen/overlay and candid B-roll corrections."""
from pathlib import Path
import json, re, hashlib, urllib.request

ROOT=Path(__file__).resolve().parents[1]
V1=ROOT/'assets/images-v1'
V2=ROOT/'assets/images-v2'
SPEC=ROOT/'storyboard/cutroom-spec.json'
old=json.loads(SPEC.read_text())
with urllib.request.urlopen('http://localhost:8765/api/boards/mot-ugc-yapper-01') as f:
    live=json.load(f)
assert live==json.loads((ROOT/'versions/v3-before-heygen-revision/live-board.json').read_text()),'Board changed during revision; merge current edits first.'

# Exact spoken copy stays in the 27 original script cards.
changes={
'B05':('B05-support-group-overlay','overlay','Support-group screenshot overlay','Show the discussion screenshot on “scrolling through a GLP-1 support group.” This is a static card overlay, not a phone video. Keep the HeyGen avatar visible; remove before the explanation. Keep its recreation label visible.'),
'B07':('B07-fiber-water-overlay','overlay','Fiber / stool-water explanatory overlay','Reveal the matching panel on “fiber helps with regularity” and “MiraLAX moves water into the stool.” Remove at “I had completely missed that.” Keep the same avatar underneath. No generic bottles or efficacy scorecard.'),
'B10':('B10-member-response-overlay','overlay','Woman’s reply · screenshot overlay','Show the woman’s portrait and response on “this woman…replied.” Same group design as B05; keep the recreation label visible. Same HeyGen avatar continues under this card.'),
'B14':('B14-low-bulk-fiber-overlay','overlay','Low-bulk soluble fiber · ingredient overlay','Show on “soluble prebiotic fiber”; remove so the qualifier lands on her face. This represents the ingredient category. Same avatar, no new presenter scene.'),
'B15':('B15-diy-ingredients-overlay','overlay','Three named ingredients · DIY overlay','Show the three named samples while she lists separate ingredients; return to the avatar for the ratios statement. Separate source image from B12/B13/B14; no random bottles.'),
'B17':('B17-Motilli-product-overlay','overlay','Motilli product cutout · over same avatar','Show the exact supplied transparent product PNG on “Motilli.” Place independently from HeyGen below/right of the face; never ask the avatar to hold it. No new presenter setup.'),
'B18':('B18-iphone-gummies-water','broll','iPhone-style routine · two gummies and water','Short candid insert on “two before bed.” Exactly two dark-green heart gummies in her palm. Return to the same avatar for the capsule preference; no product-handling HeyGen scene.'),
'B21':('B21-mirror-smile','broll','Morning · smiling at her reflection','Use the mirror image on “my mornings felt different.” She looks at her own reflected eyes, not at the viewer. Return to the avatar for the rest of the thought.'),
'B22':('B22-candid-plate-clearing','broll','Candid action · clearing her plate','Use a short side/rear-angle cleanup insert during the practical meal test. Gaze stays on her task, never the lens. Return to the avatar for “Just fine.”'),
'B24':('B24-candid-heading-out','broll','Candid action · picking up keys and leaving','Short insert in the everyday-life callback: rear three-quarter view, keys and a step toward the open door. Her attention stays on leaving, never on the camera.'),
}
spec=json.loads(json.dumps(old))
coverage=[]
base_path=str(V1/'P01-presenter-base.png')
for lane in spec['timelines'][:3]:
    for beat in lane['beats']:
        bid=beat['t'].split(' · ')[0]
        if bid in changes:
            aid,kind,visual,direction=changes[bid]
            path=V2/(aid+'.png')
            assert path.is_file(),path
            beat['frame']=str(path);beat['visual']=visual
            beat['note']=direction+'\nUnderlying performance: one continuous HeyGen avatar from P01. Cue timing stays provisional until actual voice alignment.'
        elif Path(beat['frame']).name.startswith('P'):
            aid='P01-presenter-base';kind='presenter';path=Path(base_path)
            beat['frame']=base_path;beat['visual']='Same HeyGen avatar · continuous performance'
            beat['note']='Keep the same P01 avatar, wardrobe, car setup and framing. Use voice and natural performance to carry this thought; no regenerated pose or product handling. Timing remains provisional.'
        else:
            path=Path(beat['frame']);aid=path.stem;kind='broll'
            # Retain distinct approved inserts, remove obsolete staged-avatar language.
            if bid=='B26':
                beat['note']='Optional short spare-jar drawer insert during the spare-bottle line, then return to the same HeyGen avatar. Presenter never holds a bottle. No stock counter. Timing remains provisional.'
            else:
                beat['note']+='\nBase performance is the one P01 HeyGen avatar; returns do not require a new presenter image.'
        if bid=='B27':
            beat['note']='Same HeyGen avatar through the close. Add the exact separate Motilli product PNG and editor-set “Link below” text as overlays; no product holding or forced downward hand gesture. Hold final composition three seconds after speech. Align to final HeyGen narration.'
        if bid=='B19':
            beat['note']='Same HeyGen avatar. Express disappointment in the read; do not animate lowering a bottle or switch reference images.'
        coverage.append({'beat':bid,'asset_id':aid,'path':str(path),'type':kind,'base_presenter':base_path,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'additional_overlays':['B17-Motilli-product-overlay'] if bid=='B27' else []})

spec['summary']='Exact approved Motilli narration: 27 thought beats, H1 working opening, H2/H3 alternatives, approximately 4:34 pending voice alignment. ONE P01 HeyGen avatar drives the entire performance. Static screenshot, explanation, ingredient and product overlays are separate assets. Candid action B-roll covers selected lines. B17 and the close use the actual product cutout; the avatar never handles a product. Current replacement images are selected below; competitor frames stay in a separate reference lane.'
# Keep only the original three target lanes and untouched source lane; remove obsolete presenter pose library.
spec['timelines']=spec['timelines'][:4]
spec['timelines'].append({'label':'HEYGEN BASE · ONE AVATAR FOR ALL NARRATION','beats':[{'t':'P01 · SHARED BASE','frame':base_path,'visual':'Single avatar reference · no product handling','emotion':'One continuous account; continuity is intentional. All overlay and B-roll audio remains this same performance.'}]})
spec['timelines'].append({'label':'PRODUCT OVERLAY · REVEAL & CLOSE','beats':[{'t':'B17 / B27 / FINAL HOLD','frame':str(V2/'B17-Motilli-product-overlay.png'),'visual':'Exact source PNG · transparent background','emotion':'Layer over the same avatar. Preserve label, alpha and proportions; keep mouth clear. The close uses editor-set CTA, not a new HeyGen scene.'}]})
alts=[]
for n in old['notes']:
    if n['title'].startswith(('H2 ·','H3 ·')):
        alts.append({'t':n['title'],'script':n['text'],'frame':base_path,'visual':'Alternate opening · same HeyGen avatar','emotion':'Replace H1 only. Retain the same avatar source and re-align narration after generation.'})
alts.append({'t':'04:31–04:34 · FINAL HOLD','frame':base_path,'visual':'Same avatar + separate product / CTA overlay','emotion':'Three seconds without added speech. Use the exact product PNG from the overlay lane. No bottle in the avatar’s hands.'})
spec['timelines'].append({'label':'ALTERNATE OPENINGS & END HOLD','beats':alts})
keep_titles={'TIMING & SCRIPT','CAPTIONS & CUTS','COPY DEPENDENCIES','REFERENCE SCOPE','H2 · ALTERNATE OPENING','H3 · ALTERNATE OPENING','SOURCE REFERENCE'}
spec['notes']=[n for n in old['notes'] if n['title'] in keep_titles]
spec['notes'] += [
{'title':'HEYGEN PERFORMANCE','text':'One base avatar (P01), same face, outfit, car and framing throughout. No separate product-holding, reflective or CTA image inputs. Product, screenshots and ingredients are editor overlays; the voice stays continuous.'},
{'title':'REPLACEMENTS SELECTED','text':'B05 group screenshot; B07 fiber/water explanation; B10 woman’s reply; B14 low-bulk soluble fiber; B15 named DIY ingredients; B17 exact product cutout; B18 candid gummies; B21 mirror smile; B22 plate action; B24 heading-out action; B27 same avatar plus overlay.'},
{'title':'OVERLAY PLACEMENT','text':'Preserve card aspect ratios and readable text. Place screenshot/diagram cards below the mouth with captions beneath, using final 9:16 safe areas. Product cutout sits separately below/right of face. Leave raw overlay files intact; set placement in Resolve after voice alignment.'},
{'title':'CANDID B-ROLL','text':'Lifestyle inserts show actions, not portraits posed for camera. B21 looks at her own reflection, B22 at the plate, B24 toward the door. B18 keeps natural hand/gummy texture and ordinary phone lighting. Every insert uses a distinct scene.'},
{'title':'EDITOR & DELIVERY','text':'HeyGen generates the presenter. Google Omni is reserved for later moving B-roll. Assemble and caption in DaVinci Resolve. This revision delivers stills and overlays in Cut Room; no new voice or video has been generated.'},
{'title':'SCREENSHOT RECREATIONS','text':'B05 and B10 are generated illustrative group screenshots, visibly labeled within the image. The member is fictional; these are not captured clinical advice or customer proof. Preserve the labels when placing overlays.'},
]
now_copy=[b['script'] for t in spec['timelines'][:3] for b in t['beats']]
before_copy=[b['script'] for t in old['timelines'][:3] for b in t['beats']]
assert now_copy==before_copy
assert spec['timelines'][3]==old['timelines'][3]
SPEC.write_text(json.dumps(spec,indent=2))
(ROOT/'storyboard/asset-coverage.json').write_text(json.dumps(coverage,indent=2))
cards_path=ROOT/'storyboard/beat-cards.json';cards=json.loads(cards_path.read_text());cards['version']=4;cards['presenter_provider']='HeyGen';cards['base_presenter']=base_path;cards['status']='HeyGen avatar + separate overlays and candid B-roll; still asset revision'
for c,co,beat in zip(cards['cards'],coverage,[b for t in spec['timelines'][:3] for b in t['beats']]):
    assert c['id']==co['beat'];c['selected_asset']=co['asset_id'];c['frame']=co['path'];c['visual']=beat['visual'];c['edit_direction']=beat['note'];c['asset_type']=co['type'];c['base_presenter']=base_path
cards_path.write_text(json.dumps(cards,indent=2))
print('Updated 27 beats; one avatar, 9 generated replacements and exact source product overlay. Narration unchanged.')
