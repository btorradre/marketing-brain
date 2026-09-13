"""Prepare reference-conditioned prompts, without making generation calls."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BRAND = ROOT / 'brands/motilli/celery juice gummies/brand'
REFS = HERE / 'reference-frames'
PLAN = json.loads((HERE / 'production-plan-v2.json').read_text())

STYLES = {
    'problem_life': ('ref-03-14s.jpg', 'Match the supplied style reference’s direct smartphone-video still aesthetic: close eye-level framing, beige bathroom walls, ordinary overhead/available light, moderate depth of field, real skin and fabric texture, subdued neutral colors. Subject fills most of the vertical frame. No cinematic cool-window grade, dreamy bokeh, editorial wellness staging or theatrical misery. Create a new woman aged about 58, shoulder-length brown-and-grey hair, ordinary fuller build, grey tee and lounge trousers; preserve her identity and body size across the set. Reference person is a mood/framing reference, not an identity to copy.'),
    'relief_life': ('ref-12-52s.jpg', 'Match the supplied style reference’s warm yellow-beige domestic lighting, close eye-level framing, approachable smile and immediate human warmth. Use the same new Motilli woman as the problem scenes, with unchanged face and body size. Keep the scene a natural phone-video still, not a fashion campaign. This is an imagined normal-day scene, not a verified customer testimonial. Retain the planned fully clothed activity; do not copy the reference’s toilet-use pose.'),
    'anatomy_macro': ('ref-04-20s.jpg', 'Match the supplied reference’s highly dimensional educational CGI: salmon-pink tissue, pronounced folds, glossy moist highlights, soft subsurface scattering, tight macro crop and dark charcoal/navy background. Preserve anatomically coherent structure. Match rendering material, contrast and camera distance, not the reference’s exaggerated obstruction or medical proposition. No bottles inside organs, invented blockage, cure transformation or illegible scientific text.'),
    'anatomy_map': ('ref-10-43s.jpg', 'Match the supplied reference’s semi-transparent pearlescent torso, dimensional digestive organs, pale illuminated rims and dark slate background. Use a coherent stomach-to-small-intestine-to-colon layout. Locator emphasis may identify a structure; do not copy the floating vitamin letters, glowing treatment particles or invented scientific annotations. Educational CGI, not a flat infographic or evidence of an ingredient effect.'),
    'ingredient': ('ref-09-39s.jpg', 'Match the supplied reference’s tactile handheld ingredient close-up: ingredient occupies most of the vertical frame, real hand for scale where appropriate, direct natural light, visible texture, ordinary dark kitchen counter in the background. Replace ginger with the planned Motilli ingredient. No ginger in the finished frame, no staged laboratory or decorative spa still life. Powder/liquid appearance is illustrative ingredient styling, not a measured sample of the finished formulation.'),
    'product_reveal': ('ref-07-29s.jpg', 'Match the supplied reference’s close three-quarter product framing, bright clean white surface, strong directional daylight, defined diagonal cast shadow and crisp package detail. Replace the competitor bottle/capsules with the supplied Motilli bottle and green heart gummies. Preserve Motilli’s clear jar, white cap, vivid green label, typography, proportions and gummy finish; do not borrow amber glass, a dark lid, capsule shapes, logo or competitor label.'),
    'product_close': ('ref-14-62s.jpg', 'Match the supplied reference’s centered upright pack shot, pale ivory seamless background, grounded soft shadow and generous upper/lower space for headline and CTA. Use the supplied Motilli package and exactly two dark-green heart gummies, not competitor capsules. Keep the exact Motilli identity. No text outside the packaging; guarantee and CTA are added later in the editor.'),
}


def family(shot):
    sid, kind = shot['id'], shot['kind']
    if sid == 'S37':
        return 'product_close'
    if kind == 'PRODUCT':
        return 'product_reveal'
    if sid in {'HB1', 'S08', 'S10', 'S23'}:
        return 'anatomy_macro'
    if kind == 'SCIENCE':
        return 'anatomy_map'
    if kind in {'INGREDIENT', 'GRAPHIC'}:
        return 'ingredient'
    if sid.startswith('S') and int(sid[1:]) >= 29:
        return 'relief_life'
    return 'problem_life'


OVERRIDES = {
    'S19': 'Three simple ingredient spaces on an ordinary dark kitchen counter, sized for celery, soluble fiber and chlorophyllin. Leave room for editor-set 1, 2, 3. No bottle or brand reveal.',
    'S20': 'Tight handheld close-up of freshly washed celery stalks, crisp ribs and leafy tips sharply visible; a small glass of green celery juice sits on the dark counter behind. This replaces the reference’s ginger ingredient.',
    'S22': 'Close-up of a hand holding a small clear dish of fine soluble fiber powder above an ordinary kitchen counter, beside a clear water glass. No gelatinous demonstration or dosage text.',
    'S25': 'Close-up of a small clear dish containing deep-green chlorophyllin-colored ingredient material, held above the same ordinary kitchen counter. No molecules, binding animation or invented formula amount.',
    'S27': 'First Motilli reveal: tightly framed three-quarter bottle on a clean bright surface with a defined diagonal shadow, celery and two small ingredient dishes secondary at the frame edge. The supplied Motilli bottle dominates, label facing camera. No competitor bottle.',
    'S28': 'Macro photograph of exactly two dark-green heart-shaped gummies in the foreground, matching the supplied gummy reference; the supplied Motilli bottle remains recognizable behind. White surface and directional daylight.',
}


prompts = []
for shot in PLAN['shots']:
    style_key = family(shot)
    ref_name, style = STYLES[style_key]
    scene = OVERRIDES.get(shot['id'], shot['visual'].replace('PRIOR-CONCEPT REFERENCE ONLY. Planned shot: ', ''))
    scene = scene.replace('Modest cool morning light.', 'Ordinary neutral-beige available bathroom light.')
    refs = [{'path': str(REFS / ref_name), 'role': 'Style reference only: lighting, material, framing, mood; not identity, brand, claim or text.'}]
    if shot['kind'] == 'PRODUCT':
        refs.extend([
            {'path': str(BRAND / 'product-references/motilli product reference.png'), 'role': 'User-selected product identity reference; preserve packaging.'},
            {'path': str(BRAND / 'website-assets/gummy.png'), 'role': 'Gummy identity reference; preserve dark-green heart shape and finish.'},
        ])
    if shot['id'] in {'HA1', 'HA2', 'HB1', 'HC1', 'HC2', 'S06', 'S24'}:
        refs.extend([
            {'path': str(BRAND / 'website-assets/refs/miralax.jpg'), 'role': 'MiraLAX packaging identity reference.'},
            {'path': str(BRAND / 'website-assets/refs/metamucil.png'), 'role': 'Metamucil packaging identity reference.'},
        ])
    prompt = f'Create ONE standalone vertical 9:16 scene keyframe, not a collage. Input 1 is the supplied competitor STYLE reference. Other supplied inputs have their individually stated identity roles.\nSTYLE: {style}\nSHOT: {scene}\nKeep the accepted scene purpose; do not copy the source frame literally. Do not generate captions, UI, scientific labels or competitor wordmarks outside explicitly requested remedy packages. Add all ad typography later in the editor. Match the opening pose only. No fabricated reviews or testimonial attribution.'
    prompts.append({'shot': shot['id'], 'model_requested': 'GPT Image 2.5', 'status': 'pending_model_access', 'style_family': style_key,
        'reference_inputs': refs, 'additional_identity_anchor_required': style_key in {'problem_life', 'relief_life'},
        'prompt': prompt, 'motion_direction_for_later': shot['motion']})

assert len(prompts) == 41
assert all(Path(ref['path']).is_file() for p in prompts for ref in p['reference_inputs'])
(HERE / 'keyframe-prompts-v3-reference-matched.json').write_text(json.dumps(prompts, ensure_ascii=False, indent=2)+'\n')
guide = ['# Motilli — reference-matched visual direction\n',
    'This supersedes the generic visual-style paragraphs in the v2 generation prompts. Keep the accepted three hooks, shared narration, timing, future-pacing activities and Motilli identity. The exact source frames listed below were visually inspected. Match the aesthetic; do not copy erroneous anatomy, medical assertions, customer identity or competitor branding.\n',
    '## Scene style references\n']
for key, (ref, style) in STYLES.items():
    guide.append(f'### {key}\n\nReference: {ref}\n\n{style}\n')
guide.extend(['## Continuity and production\n\nGenerate a new recurring woman using the source’s closer, direct domestic framing and available beige light. The earlier cool-window S05 test is not the final style anchor. Use one coherent anatomy geometry across macro and translucent views. User-selected Motilli packaging controls all product details. Ingredient close-ups use the source’s tactile kitchen framing with Motilli ingredients.\n',
    '## Captions\n\nReference body captions: bold black sans-serif on compact white rounded rectangles, lower-middle. Reference hook also uses white uppercase on a dark-green banner. For Motilli, apply the approved hook overlays in this treatment; add typography in the internal editor, not into raw images. No copied competitor slogan or logo.\n',
    '## Generation status\n\n41 shot-specific prompts have source-frame and identity-reference mappings. No new images generated in this style pass. GPT Image 2.5 remains blocked by organization verification; no model substitution is authorized. Exact visual matching must be inspected on the generated output, not certified from a prompt.\n'])
(HERE / 'reference-style-direction.md').write_text('\n'.join(guide))
print(json.dumps({'prompts': len(prompts), 'style_families': len(STYLES), 'references_valid': True, 'generation_started': False}))
