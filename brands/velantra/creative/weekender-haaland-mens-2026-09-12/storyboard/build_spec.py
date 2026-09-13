import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
A = ROOT / 'assets'
R = ROOT / 'reference-frames'

scenes = [
    ('S01-hook-lounge', '0.00–0.80', 'Nobody does it', 'Haaland seated beside a private jet; black designer bag immediately visible. Large hook presenter and red/white title.', 'Recognition and desire: the bag already belongs to an aspirational full outfit.', 'Start on the photo without a fade. Direct cut mid-hook at “like”; the second distinct photo turns recognition into a collection impression.'),
    ('S02-hook-tarmac', '0.80–2.00', 'like Erling Haaland.', 'Haaland walking across the tarmac with an orange/navy bag. Same opening title; presenter moved clear of bag.', 'Reinforcement: a second real styling example supports the emphatic opening.', 'Direct cut in and out. Hold title across the cut so only the underlying photograph changes. No added pan or whoosh.'),
    ('S03-hook-training', '2.00–7.33', 'The guy turns up carrying a Birkin, and the bag is the first thing you notice.', 'Third distinct Haaland photo: black training vest, white shorts and a black bag. Compact caption and chest-cropped presenter.', 'Style attention: let the viewer find the bag within a simple outfit before introducing the buying option.', 'Direct cut on “The guy.” Hold the outfit through the sentence; complete picture change at “If you want” separates Haaland from Velantra.'),
    ('S04-product-reveal', '7.33–13.33', 'If you want a travel bag with that kind of presence, take a look at the Velantra Weekender.', 'Unrelated male model at an airport entrance, navy overshirt and light trousers, holding the Cognac Weekender.', 'Product discovery: connect the desired presence to the actual named product and an attainable outfit.', 'Direct cut at the buying bridge. Show the Weekender name on its spoken cue. Later motion: small natural handle lift, no dramatic zoom. Cut to construction at “It’s got.”'),
    ('S05-construction', '13.33–19.33', 'It’s got a broad, rectangular shape, rolled leather handles, and a leather flap over canvas.', 'Stacked product front and handle close-up; warm canvas, leather flap and horizontal oval hardware visible.', 'Visual evidence: the front demonstrates shape while the separate detail makes the rolled handle construction legible.', 'Direct cut to the split layout. Hold front on “shape,” favor detail on “handles,” then leather/canvas boundary on “flap over canvas.” These are detail views of one product, not three new sourced scenes.'),
    ('S06-tee-jeans', '19.33–23.00', 'So even with a plain T-shirt and jeans, it gives you a sharper look.', 'Full casual outfit: white T-shirt and jeans with the Weekender hand-carried in a city setting.', 'Visible payoff: show how the bag changes a familiar outfit immediately after explaining its construction.', 'Direct cut on “So even.” Let the complete silhouette stay readable. Natural stance or one small step later; no artificial distress or before/after comparison.'),
    ('S07-material-hardware', '23.00–27.67', 'The Cognac version has brown leather against a lighter canvas body, with gold-tone hardware.', 'Close view of the actual Cognac leather/canvas boundary, oval plate and a hand touching the materials.', 'Tactile desire: make the color contrast and finishing visible before showing wardrobe combinations.', 'Direct cut on “The Cognac version.” Hold through the named materials; favor the gold plate at “hardware.” Keep captions and presenter clear of the features.'),
    ('S08-navy-jacket', '27.67–29.00', 'Easy to wear with a navy jacket,', 'A man in a navy blazer and grey trousers steps from a stone doorway carrying the Weekender.', 'Outfit compatibility: make the first named pairing concrete rather than leaving “easy to wear” as an abstract claim.', 'Direct cut on “Easy to wear.” Quick wardrobe cadence begins here; no transition animation. Cut at the next named outfit.'),
    ('S09-denim', '29.00–30.33', 'denim,', 'A younger man in a dark denim jacket sets the Weekender on a station bench.', 'Range: a different age, setting, action and composition make the casual pairing a distinct scene.', 'Direct cut at “denim.” Preserve a readable bag and outfit; later motion is the small set-down only. Cut on “or.”'),
    ('S10-black-coat', '30.33–31.67', 'or a black coat.', 'A dark-haired man in a black overcoat and grey trousers walks beside a modern building with the Weekender.', 'Range completed: the lighter canvas stands out against the dark outfit, closing the three-pairing sequence.', 'Direct cut on “or a black coat.” End the faster wardrobe run at the end of the sentence, then slow for the interior demonstration.'),
    ('S11-interior-pocket', '31.67–36.67', 'Inside, there’s a wide slip pocket to keep smaller things separate from the main compartment.', 'Top-down open Cognac Weekender with caramel interior; hand holds the opening and the wide slip pocket stays unobstructed.', 'Supporting utility: show the one evidenced organization detail after the style-led argument.', 'Direct cut on “Inside.” Continuous gentle hand indication later; hold until the pocket is understood. No invented laptop, shoe or garment compartments. Caption and presenter must not overlap the opening.'),
    ('S12-hotel-arrival', '36.67–42.67', 'So you’ve got a bag for the weekend that looks right when you walk into the hotel, too.', 'Complete outfit at a hotel entrance: tan jacket, white shirt, navy trousers and the Weekender.', 'Imagined use: finish on arriving well dressed, making weekend function support the appearance payoff.', 'Direct cut on “So you’ve got.” Later action should move into the entrance; the selected still establishes the setting. Hold the look through “hotel, too,” then cut to the product.'),
    ('S13-product-cta', '42.67–48.00', 'The Velantra Weekender. Check it out at the link below.', 'Distinct clear product hero with the Weekender name, link instruction and the same presenter.', 'Buying clarity: leave the exact product and a simple next step in view after the outfit examples.', 'Direct cut on the final product name. Narration ends around46s; hold the product and CTA for2seconds. Timing remains provisional until voice alignment.'),
]

beats = []
for ident, t, script, visual, emotion, note in scenes:
    suffix = '' if ident.startswith(('S01-', 'S02-', 'S05-')) else '-layout-v2'
    beats.append(dict(t=f'{ident[:3]} · {t}s · provisional', script=script, frame=str(A / f'{ident}{suffix}.png'), visual=visual, emotion=emotion, note=note))

expected = ' '.join((ROOT / 'narration.txt').read_text().split())
actual = ' '.join(' '.join(b['script'] for b in beats).split())
assert actual == expected, 'Narration changed during card split'

ref = [
    ('R01-athlete.jpg','0.00s sample','Athlete-photo opening; red ATHLETE tag, white title panel, large bottom presenter.','Recognition hook; fast photograph changes keep the same title. Purpose inferred.'),
    ('R02-split-product.jpg','5.00s sample','Stacked product imagery during the early smart-bag claim.','Early product comprehension. Split layout contrasts views; purpose inferred.'),
    ('R03-intro.jpg','7.00s sample','Athlete photo with compact black-bar phrase caption and floating chest-cropped presenter.','Product naming remains visible while celebrity recognition continues. Purpose inferred.'),
    ('R04-overhead.jpg','10.00s sample','Overhead bag demonstration, presenter repositioned above the central caption.','Hand action explains a feature; position avoids the action. Purpose inferred.'),
    ('R05-detail.jpg','21.67s sample','Detail demonstration from the source feature stack.','A named feature receives its own picture. Feature itself does not transfer to Weekender.'),
    ('R06-laptop.jpg','25.67s sample','Source laptop-use demonstration.','Use benefit follows feature; only the editing pattern transfers. No Weekender laptop-fit claim.'),
    ('R07-arrival.jpg','31.00s sample','Arrival/use-case image after the feature stack.','Return from detail to imagined use. Purpose inferred.'),
    ('R08-cta.jpg','41.00s sample','Final source product frame and compact phrase caption.','Product recall at the close. Purpose inferred.'),
]
spec = dict(
    title='Weekender — Haaland / reference-style storyboard', project='velantra',
    summary='Men’s aspirational Weekender ad. Three Haaland photos lead into an early Cognac product reveal, construction, distinct outfit pairings, one supported pocket detail and a hotel payoff. Draft4 narration is preserved exactly. 13 selected first frames plus an original presenter and overlay kit. Approximately48seconds including end hold; voice alignment pending.',
    timelines=[
        dict(label='VELANTRA — PROPOSED AD / SELECTED FIRST FRAMES',source='Draft4 · GPT Image2 storyboard frames · Cognac Weekender · timing provisional',beats=beats),
        dict(label='REFERENCE ONLY — ALEC GRAWE / FTL PRO',source='Instagram DbdW5anAxg5 · actual source screenshots ·41.77s',beats=[dict(t=t,script='Visual reference only; not target narration.',frame=str(R/f),visual=v,emotion=e,note='Observed source frame. Source product and creator are not target assets. Section analysis is sampled; candidate cut boundaries separately checked on consecutive frames.') for f,t,v,e in ref]),
    ],
    notes=[
        dict(title='VOICE — PERMISSION PENDING',text='Reference voice requested. Clone has not been submitted: reference speaker permission and lawful-use confirmation remain unanswered. Preserve exact card narration. Delivery: casual, direct male explanation, clear feature emphasis and natural cadence. No substitute voice selected.',color='#fdf3c9'),
        dict(title='EDIT LANGUAGE',text='Direct picture cuts on ideas; fast athlete opening and three-item wardrobe run, longer product and pocket holds. Continuous microphone presenter. Compact uppercase white phrase captions on black bars. Red/white hook title; occasional stacked detail and blur fill when source framing needs it. No universal zoom or whoosh.',color='#dff2e1'),
        dict(title='AUDIO / ALIGNMENT',text='Voice leads. Proposed restrained rhythmic music under speech, with no masking and no SFX on every cut. Source sound settings remain unverified. Final narration sets cuts and caption timings; do not force48seconds or speed up speech silently. Hold CTA2seconds after the last word.',color='#f7f5ee'),
        dict(title='PRODUCT / SOURCE PROVENANCE',text='Cognac canvas body, brown leather upper/flap/rolled handles/corners, horizontal oval gold-tone plate and caramel interior with wide slip pocket. Product construction checked against actual references. Generated lifestyle scale is illustrative, not measured. Haaland photos came from the existing concept’s sourced plates; no endorsement or commercial rights verification is implied.',color='#f7f5ee'),
        dict(title='STORYBOARD QA / NEXT PRODUCTION',text='Inspect every selected image for bag geometry, hardware, pocket visibility, typography and composition variety. Keep reference lane separate. Generated stills establish proposed scenes; motion and voice are not rendered. Use Google Omni for later motion and an isolated DaVinci Resolve timeline for assembly, final caption alignment and playback QA.',color='#dff2e1'),
    ],
    moodboard=[dict(image=str(A/'presenter.png'),caption='Selected original presenter · oatmeal T-shirt and handheld microphone · same identity throughout'),dict(image=str(A/'overlay-kit.png'),caption='Overlay design sheet · hook, phrase bar and CTA · opaque mockup; rebuild clean type in Resolve')]
)
(ROOT/'spec.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n')
print(f'Wrote spec: {len(beats)} target cards; exact narration match; {len(ref)} reference frames')
