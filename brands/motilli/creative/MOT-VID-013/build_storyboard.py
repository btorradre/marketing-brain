"""Build the planning storyboard; no media generation or timeline rendering."""
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SLUG = 'mot-vid-013-upstream-three-things'
REFERENCE = 'https://app.trendtrack.io/share/ads/glp-1-sos-supplements-RUoEBJ'
PRODUCT = 'https://getmotilli.com/products/motilli-digestive-health-gummies'
SOURCE = ROOT / '_engine/mcp/ad-engine/data/downloads/job_d78559811694/source.mp4'
PREVIOUS = ROOT / 'brands/motilli/creative/MOT-VID-012/assets'
PACK = ROOT / 'brands/motilli/celery juice gummies/brand/product-references/motilli product reference.png'

# Exact approved narration, divided at picture changes. No copy revision is hidden here.
# Fields: VO, type, planned image/action, viewer emotion + persuasion job, asset candidate.
SHOTS = [
('On a GLP-1, the harder you push your colon', 'SCIENCE', 'Hook: side-view torso with stomach and colon visible together. One restrained downward pressure arrow beside the colon; stomach highlighted amber. Camera moves toward the stomach.', 'Curiosity: introduce the mismatch between effort and location.', '0985_science_the-slowdown-can-begin-upstr.jpg'),
('with laxatives and fiber, the more stuck you can feel.', 'LIFE', 'Overhead bathroom counter: real MiraLAX and Metamucil packages beside a water glass. Woman closes the cabinet with a tired hand; products remain outside the body.', 'Recognition: make the familiar remedy stack visible.', '0652_card_now-look-at-the-cabinet-agai.png'),
('Here’s the trap no one explains.', 'LIFE', 'Same woman seated on the closed toilet lid, clothed in a grey cotton tee and lounge trousers; she looks from the counter to her abdomen. Tighten framing with a hard cut.', 'Anticipation: open the explanation loop.', None),
('Your GLP-1 slows your stomach down.', 'SCIENCE', 'Whole digestive tract; amber highlight stays on the anatomically correct stomach. Slow, subtle movement rather than a frozen or sealed organ.', 'Understanding: locate the initial mechanism.', '0474_science_slow-the-rate-at-which-food.jpg'),
('So when you haven’t gone in days,', 'LIFE', 'Same woman sits on the edge of the bathtub, fully clothed, elbows resting on thighs. She exhales and looks down.', 'Empathy: connect physiology to a familiar morning.', None),
('you reach for MiraLAX, magnesium, stool softeners, or more fiber.', 'OBJECT', 'Four quick object reveals on the counter, one per named remedy. Use real package references; allow internal picture changes on each product name.', 'Recognition: identify solutions the audience already knows.', None),
('Those products work downstream. They target the colon—', 'SCIENCE', 'Torso diagram: camera travels down the continuous digestive tract and highlights the colon. Keep the stomach visible in the same diagram.', 'Reframing: explain the intended downstream comparison.', '1022_pip_aimed-at-water.png'),
('the end of your digestive system.', 'SCIENCE', 'Closer view of the colon in the same diagram. A simple editor-set COLON label lands beside it; no empty-tube claim.', 'Clarity: define the term in plain visual language.', None),
('But if the slowdown begins higher up in your stomach,', 'SCIENCE', 'Hard cut back to the upper torso. Highlight the stomach at the exact word stomach; the entire tract remains connected.', 'Realization: answer why the remedies might leave a gap.', '0886_science_is-your-stomach.jpg'),
('food is still sitting at the beginning.', 'SCIENCE', 'Stomach cross-section shows a modest meal and gradual mixing; no solid brick, stool, complete obstruction, or food packed into the esophagus.', 'Understanding: translate the location into a recognizable sensation.', None),
('That’s why the relief may last a day,', 'LIFE', 'Same woman looks briefly hopeful at her bathroom mirror, then cut to her returning to the counter the following morning.', 'Frustration: depict recurrence without inventing a measured result.', None),
('the fiber can make you feel even fuller,', 'LIFE', 'Side-on seated portrait at breakfast; woman gently loosens her waistband and leaves the bowl partly eaten. Subtle fullness, no extreme distension.', 'Recognition: connect to the bloated, too-full feeling.', '0145_ugc_midsection-is-distended.jpg'),
('and those rotten-egg burps keep coming back.', 'LIFE', 'Same woman at the dining table brings a closed hand to her mouth and turns away discreetly. Avoid a cartoon gas cloud.', 'Social discomfort: expand beyond the bathroom.', None),
('It’s not that your body is broken.', 'LIFE', 'Eye-level close portrait. She relaxes her shoulders slightly, still thoughtful. Hold long enough for the reassurance to land.', 'Absolution: remove self-blame.', None),
('And it doesn’t mean you have to quit your shot.', 'OBJECT', 'Her hand sets the correctly referenced medication pen beside its box. Do not show injection technique or throw medication away.', 'Reassurance: preserve her larger goal.', '1201_card_work-alongside-the-shot.png'),
('You’ve been trying to solve an upstream slowdown with downstream tools.', 'SCIENCE', 'One full-frame anatomy map. Two editor-set callouts read STOMACH / UPSTREAM and COLON / DOWNSTREAM. Alternate emphasis between them.', 'Belief shift: complete the problem explanation.', None),
('What you need is something designed to wake your stomach back up', 'SCIENCE', 'Stay on the neutral stomach map. A soft highlight introduces the proposed movement-support job. No switch flipping, nerve repair, or restart demonstration.', 'Hope: introduce the solution requirement before the brand.', None),
('while supporting everything below it.', 'SCIENCE', 'Camera moves down the same connected tract; a second quiet highlight joins the first. Keep the diagram visually continuous.', 'Completeness: prepare the viewer for multiple ingredient jobs.', None),
('And to do that, you need three specific things.', 'GRAPHIC', 'Three clean numbered ingredient spaces fill the frame. Show 1, 2, 3; no product bottle or Motilli mark yet.', 'Curiosity: open a finite three-part checklist.', None),
('First, apigenin—a plant compound concentrated from celery juice—', 'INGREDIENT', 'Macro of washed celery stalks and a small glass of green juice on cream stone. Editor-set APIGENIN / FROM CELERY label; first checklist dot fills.', 'Discovery: connect an unfamiliar word to a familiar ingredient.', None),
('to support your stomach’s natural wave-like movement.', 'SCIENCE', 'Neutral illustrative stomach with an external wave line indicating the intended job. No causal before/after animation showing celery restarting contractions.', 'Understanding: explain the first proposed job.', '1543_science_support-that-movement.jpg'),
('Second, a low-viscosity soluble fiber', 'INGREDIENT', 'Fine soluble fiber ingredient in a glass dish beside water. Editor-set SOLUBLE PREBIOTIC FIBER label; second checklist dot fills.', 'Differentiation: distinguish the ingredient category.', None),
('that holds water in the stool', 'SCIENCE', 'Restrained diagram of water and stool inside the colon; label this an illustrative concept. Do not show FOS behaving as a proven gel-forming osmotic agent.', 'Understanding: intended second job; claim review required.', None),
('without becoming another heavy bulk load.', 'OBJECT', 'Small measured ingredient dish beside the actual referenced full-size fiber container. No fabricated gram numbers or zero-bulk comparison graphic.', 'Objection handling: address why another fiber ingredient is included.', None),
('And third, chlorophyllin to neutralize the sulfur compounds', 'INGREDIENT', 'Deep-green chlorophyllin ingredient material in a laboratory-style glass dish, editor-set CHLOROPHYLLIN label; third checklist dot fills. No fabricated molecular binding.', 'Discovery: introduce the odor-support ingredient.', None),
('behind those burps instead of merely covering the smell.', 'LIFE', 'Return to the dining scene as the woman sets down a mint packet. Stay neutral; do not portray the ingredient producing instant relief.', 'Relevance: connect the third proposed job to the symptom.', None),
('That’s why Motilli combines all three', 'PRODUCT', 'FIRST MOTILLI REVEAL: the verified current bottle enters between the three ingredient dishes. Label faces the lens and remains readable.', 'Resolution: the brand answers the completed checklist.', '1920_product_motilli-combines-them.jpg'),
('in two heart-shaped gummies made specifically for people on GLP-1s.', 'PRODUCT', 'Macro of exactly two dark-green heart-shaped gummies beside the bottle. Preserve true gummy shape and finish from the reference.', 'Ease: turn the mechanism into a simple product format.', '1944_product_forest-green-heart-gummy.jpg'),
('No harsh stimulant laxatives.', 'PRODUCT', 'Bottle and gummies stay in frame; one editor-set callout: NO STIMULANT LAXATIVES. Only use after current formula verification.', 'Reassurance: describe a specific formulation distinction.', None),
('No cabinet full of disconnected products.', 'LIFE', 'Same bathroom shelf, tidied; Motilli and a water glass occupy the foreground. Do not discard prescribed or OTC medicines on screen.', 'Relief: show the appeal of a simpler routine.', '2084_product_the-cabinet-is-no-longer.png'),
('Just support for stomach movement, downstream softness, and sulfur-related odor.', 'PRODUCT', 'Three ingredient cards return around the bottle, one per spoken job. Keep the stomach/softness/odor labels in review status until supported.', 'Recall: compress the three-job rationale into one picture.', None),
('Take two before bed with a full glass of water.', 'LIFE', 'Evening bedside scene: exactly two gummies in the same woman’s palm, clear water glass and bottle beside her. Hand lowers toward the glass.', 'Actionability: make the routine easy to picture.', '1979_product_the-routine-is-simple.jpg'),
('You keep the shot and the progress you worked for', 'LIFE', 'Morning bedroom scene: she folds her ordinary clothes and picks up her bag. No scale number, weight-loss comparison, or medication-outcome graphic.', 'Progress protection: keep her broader life in view.', None),
('while supporting your gut where the slowdown can begin.', 'PRODUCT', 'Bottle foreground on the breakfast counter; same woman in soft focus behind, preparing breakfast. Warm natural light.', 'Hope: associate the product with an ordinary routine.', None),
('It’s not a broken gut. It’s the wrong strategy.', 'LIFE', 'Close portrait of the same woman looking composed. Two-word editor-set emphasis STRATEGY MATTERS; no claim that she has been cured.', 'Absolution and recall: land the closing reframe.', None),
('Motilli comes with a 90-day money-back guarantee. Tap below.', 'PRODUCT', 'Clear end card: verified bottle, exactly two gummies, 90-DAY MONEY-BACK GUARANTEE and SHOP MOTILLI. Hold through a two-second silent tail.', 'Risk reversal: make the next action obvious.', '2294_product_90-day-money-back-guarantee.jpg'),
]

def clock(seconds):
    return f'{int(seconds)//60:02}:{seconds%60:04.1f}'

def main():
    HERE.mkdir(parents=True, exist_ok=True)
    frames = HERE / 'reference-frames'
    frames.mkdir(exist_ok=True)
    words = sum(len(re.findall(r"\b[\w]+(?:[’'-][\w]+)*\b", s[0])) for s in SHOTS)
    # Consistent word-proportional planning only; measured VO alignment replaces this.
    t = 0.0
    beats = []
    review_shots = {1, 2, 7, 10, 11, 12, 16, 17, 21, 23, 24, 25, 26, 29, 31, 32, 33, 34}
    for i, (vo, kind, visual, emotion, candidate) in enumerate(SHOTS, 1):
        n = len(re.findall(r"\b[\w]+(?:[’'-][\w]+)*\b", vo))
        duration = n / 190 * 60
        if i == len(SHOTS):
            duration += 2.0
        end = t + duration
        beat = {'id': f'S{i:02}', 'start_s': round(t, 3), 'end_s': round(end, 3),
                't': f'S{i:02} · {clock(t)}–{clock(end)}', 'script': vo,
                'kind': kind, 'visual': visual, 'emotion': emotion,
                'status': 'planning_only', 'continuity_group': 'woman-home' if kind == 'LIFE' else 'anatomy' if kind == 'SCIENCE' else 'product' if kind == 'PRODUCT' else 'ingredients' if kind == 'INGREDIENT' else 'objects',
                'note': 'GPT Image 2.5 still → Google Omni motion. Match the picture change to the exact narration cue; times are estimates.'}
        if candidate and (PREVIOUS / candidate).exists():
            beat['frame'] = str(PREVIOUS / candidate)
            beat['visual'] = 'PRIOR-CONCEPT REFERENCE ONLY. Planned shot: ' + visual
            beat['note'] += ' Existing frame is a visual reference, not an approved final shot.'
        if i in review_shots:
            beat['note'] += ' Production hold: verify the related efficacy/comparison claim before final VO or causal animation.'
        if kind == 'PRODUCT' or i in {30, 32}:
            beat['note'] += ' Confirm current bottle label; old 5g label art is not approved production truth.'
        if duration > 4:
            beat['note'] += ' Add a hard-cut detail view within this beat so no picture holds beyond four seconds.'
        beats.append(beat)
        t = end

    # Selected frames from the exact ad, not fabricated or generated replicas.
    ref_specs = [
      (2, 'On a GLP-1, the harder you push your gut with laxatives, the more stuck you get.', 'Anatomy hook and competing products', 'Contradiction / attention'),
      (8, 'Your GLP-1 slows your gut down, so you reach for a laxative to force things through.', 'Slowed-digestion explanation', 'Recognition / mechanism'),
      (14, 'It starts leaning on that push, and its own natural rhythm gets weaker.', 'Everyday frustration montage', 'Failure explanation'),
      (20, 'Meanwhile, the fiber you’re piling in just adds bulk to a gut that already can’t move it,', 'Anatomical bulk illustration', 'Alternative disqualification'),
      (24, 'It’s not that your body is broken, and it’s not the shot.', 'Reassurance beat', 'Self-blame removal'),
      (27, 'It’s that the harder you force it, the more stuck you get.', 'Anatomy callback', 'Memorable problem reframe'),
      (29, 'GLP-1-SOS breaks the loop by working with your slowed gut instead of forcing it.', 'Product-to-mechanism transition', 'Solution reveal'),
      (34, 'Magnesium gently draws water in, so things soften and move on their own.', 'Water / digestive-system illustration', 'Ingredient job'),
      (39, 'Ginger helps your stomach actually empty, so food doesn’t sit and ferment,', 'Ginger ingredient shot', 'Second ingredient job'),
      (43, 'and it replaces the B12 and iron your shot quietly drains.', 'Internal nutrient illustration', 'Benefit extension'),
      (47, 'It’s gentle enough to take every single day, which matters,', 'Daily-use beat', 'Sustainability'),
      (52, 'Women say they’re regular for the first time in years.', 'Warm relief scene', 'Social proof claim'),
      (57, 'It’s the wrong tool, and you don’t have to quit your shot to feel normal again.', 'Remedy/medication callback', 'Progress protection'),
      (62, 'GLP-1-SOS 60-Day Money-Back Guarantee.', 'Product close', 'Risk reversal'),
    ]
    refs = []
    for index, (ts, vo, visual, emotion) in enumerate(ref_specs, 1):
        dest = frames / f'ref-{index:02}-{ts:02}s.jpg'
        if not dest.exists():
            subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-ss', str(ts), '-i', str(SOURCE), '-frames:v', '1', '-q:v', '3', str(dest)], check=True)
        refs.append({'t': f'REF · sample {clock(ts)}', 'script': vo, 'frame': str(dest),
                     'visual': visual, 'emotion': emotion,
                     'note': 'Original creative reference only. Transcript excerpt near sampled frame; source claims are not product evidence.'})
    notes = [
      {'title': 'STATUS / TIMING', 'text': f'Storyboard v1. {words} spoken words at 190 wpm = {words/190*60:.1f}s; +2s tail = {t:.1f}s. {len(beats)} narration beats. Times are planning estimates, not VO timestamps. No new keyframes, VO or video generated.', 'color': '#dff2e1'},
      {'title': 'MECHANISM BEFORE BRAND', 'text': 'All three ingredient explanations must finish before S27 reveals Motilli. Order follows the approved script: apigenin → soluble fiber → chlorophyllin → combined formula.'},
      {'title': 'VISUAL GRAMMAR', 'text': 'Full-frame pictures, hard cuts, frequent 2–4s changes. Dark blue anatomy and cool ordinary home scenes first; warmer home/product images after the reveal. Text is added in the editor.'},
      {'title': 'PRODUCTION STACK', 'text': 'GPT Image 2.5 for stills, Google Omni for video, one continuous narration take. Assemble in the internal adengine timeline editor. HyperFrames and Remotion are prohibited.'},
      {'title': 'CONTINUITY', 'text': 'One woman about 55–60, shoulder-length salt-and-pepper hair, grey cotton tee, normal skin texture. Same bathroom and kitchen. One coherent anatomy model. One verified bottle reference for every product shot.'},
      {'title': 'CLAIM REVIEW — CONCRETE ISSUE', 'text': 'Existing product-development evidence does not establish celery/apigenin as a human stomach-restart treatment. The prior script overstates colon-only remedy action and ingredient effects. Preserve the script for review, but do not render restart, nerve-repair, empty-colon or guaranteed gas-binding demonstrations from it.', 'color': '#f9d9d4'},
      {'title': 'BOTTLE REFERENCE HOLD', 'text': 'The stored photo has the historical 5g fiber label. Formula records and live-page numbers conflict. This image is provenance only; confirm current bottle/label before GPT Image 2.5 product work.', 'color': '#f9d9d4'},
      {'title': 'FIRST PRODUCTION BATCH', 'text': 'Establish the recurring woman/home anchor, neutral anatomy anchor and ingredient still life. Then create shot-specific keyframes using those anchors. Product frames depend on current label confirmation.'},
      {'title': 'AUDIO / CAPTIONS', 'text': 'One clear, calm female narrator; no invented clinician or patient identity. One uninterrupted take. Captions 2–5 words, black on white rounded backing, within the vertical safe area. Optional low-volume instrumental bed begins after the opening hook.'},
      {'title': 'SOURCE', 'text': f'Exact Facebook ad 1725854202002410. {REFERENCE}. Ad-level profitability is unknown. Watch result detected 31 beats, not an exhaustive frame audit.'},
    ]
    spec = {'title': 'MOT-VID-013 — Upstream / Three Things', 'project': 'motilli',
            'summary': f'Solution-aware GLP-1 viewer: familiar remedies → upstream explanation → three ingredient jobs → Motilli reveal → daily routine and guarantee. {words} words; approx. {t:.0f}s at 190 wpm including tail. This is a planning board with original swipe frames and explicitly labeled prior Motilli asset references. Final keyframes are not generated or approved.',
            'timelines': [{'label': 'REFERENCE — GLP-1 SOS', 'source': REFERENCE, 'beats': refs},
                          {'label': 'OUR VERSION — MOTILLI — PLANNING', 'source': 'Estimated timing / approved script preserved for review', 'beats': beats}],
            'notes': notes,
            'moodboard': [{'image': str(PACK), 'caption': 'Historical bottle photo — label verification required before generation'}]}
    (HERE / 'storyboard-spec.json').write_text(json.dumps(spec, indent=2, ensure_ascii=False)+'\n')
    (HERE / 'script-approved.txt').write_text('\n\n'.join(s[0] for s in SHOTS)+'\n')
    plan = {'concept_id': 'MOT-VID-013', 'status': 'storyboard_planning', 'board_slug': SLUG,
            'width': 1080, 'height': 1920, 'fps': 30, 'spoken_word_count': words,
            'planning_wpm': 190, 'estimated_duration_s': round(t, 3),
            'timing_source': 'word-count estimate; replace with recorded VO alignment',
            'image_model': 'GPT Image 2.5', 'video_model': 'Google Omni',
            'editor': '@adengine/timeline assembleFromBoard or validated edit-plan handoff',
            'not_an_executable_edit_plan': True,
            'shots': beats}
    (HERE / 'production-plan.json').write_text(json.dumps(plan, indent=2, ensure_ascii=False)+'\n')
    intro = f'''# MOT-VID-013 — Upstream / Three Things (VO + Anatomy + Lifestyle)

## PRODUCTION METHODS — HOW WE MAKE THIS AD

GPT Image 2.5 supplies new stills. Google Omni supplies video. One continuous original or authorized narration take drives the edit. Final assembly uses the internal adengine timeline editor. This is a planning brief; audio and video have not been produced.

Reference: {REFERENCE}
Format: estimated {t:.1f}s including a 2s end-card tail; 1080x1920, 30fps, 9:16.
Production type: narration over full-frame anatomy, ingredient, product and everyday-life footage.

## VOICE

Calm, clear female narration with the reference's brisk explanatory cadence. Use an original or authorized voice; no clinician persona or fabricated testimonial. One continuous take. {words} words ÷ 190 words/minute × 60 = {words/190*60:.1f} seconds before tail. Recorded narration will replace all estimated timestamps.

## THE ONE THING

Teach every ingredient job before revealing Motilli. The product should answer a checklist the viewer has just understood. Keep the reference's progression from discomfort and clinical diagrams toward warmer everyday scenes, with a simple product close.

## THE RULES THAT RUN THE WHOLE EDIT

1. Pictures fill the frame. Hard cuts; no PIP.
2. Each picture lands on its quoted narration cue. No hold beyond four seconds without a detail cut.
3. Motilli first appears at S27, after the three ingredient explanations.
4. Keep one woman, one home and one anatomy model consistent. Continuity overrides the differing people in old reference assets.
5. Actual product references control every bottle, gummy and medication package. Do not render invented label amounts or screenshots.
6. Do not add faux hand shake, slow zoom drift, dissolves, fake reviews, weight-loss measurements, or medical before/after demonstrations.

Captions: 2–5 words per white rounded card, black bold sans-serif, lower-middle safe area; manually check against Meta overlays. Add typography in the editor.

## STEP 1 — BUILD THE REPEATING ASSETS

First establish a woman/home anchor, neutral anatomical torso anchor and ingredient still life. Reference images on the board are planning examples, not generated keyframes. Product generation waits for the current bottle/label reference.

Woman base-frame prompt:
```
Vertical candid home photograph, woman approximately 55–60 with shoulder-length salt-and-pepper hair, ordinary skin texture and natural body proportions, grey cotton tee and charcoal lounge trousers, seated on the edge of a bathtub in a modest lived-in bathroom. Eye-level medium framing, soft cool window light. Thoughtful, tired expression, restrained pose. No embedded captions. Preserve this same identity and home in subsequent references.
```

Reject identity drift, beauty-filter skin, exaggerated abdomen, uncanny fingers, incorrect anatomy or invented packaging.

## STEP 2 — THE BUILDING BLOCKS

LOOK: candid domestic photograph, ordinary surfaces and wardrobe, natural skin and soft window light, full vertical composition. Keep movement restrained and motivated.

HER: use the same approved identity reference in every home scene; identical facial structure, hair, age and wardrobe. Time-of-day lighting may change, identity may not.

SCIENCE: anatomically coherent illustrative 3D torso on deep navy. Distinct stomach, small intestine and colon, with realistic relative placement. Amber focus for problem discussion; neutral teal for explanatory callouts. No supernatural cure glow, solid obstruction, empty colon, repaired nerves or medicine packages inside organs.

INGREDIENT: tactile macro material on warm cream stone; clear glass dish, natural light, one named ingredient at a time. Typography is composited separately. No fabricated biochemical diagrams.

PRODUCT: image-to-image using verified current front/back bottle and gummy references; preserve label, cap, transparency, scale relationships and gummy shape. Do not reconstruct the package from text. The historical stored label is not cleared for production.

Use existing Motilli assets where their identity, fidelity and rights fit. The board contains labeled candidates; their inclusion does not clear them for final use.

## SCRIPT

Approved conversation wording preserved below for review. These are planning timings, not recorded VO timings. Copy/claim issues are listed at the end and must be resolved before recording.

'''
    lines = [intro]
    for b in beats:
        lines.append(f"[{clock(b['start_s'])}] {b['script']}\n")
    lines.append(f'\n## VISUAL SCHEDULE\n\n{len(beats)} narration beats across approximately {t:.1f}s; split any longer beat with an internal detail cut. Reference thumbnails are not final keyframes. Every shot below has a defined image, emotion and production route.\n')
    for b in beats:
        lines.append(f"\n### {b['t']} — {b['kind']}\n\nNarration: {b['script']}\n\nVisual: {b['visual']}\n\nPurpose: {b['emotion']}\n\nUse: Motilli existing asset library — labeled candidate on board if supplied; otherwise no selected asset.\n\nOnly if missing — Make: {b['visual'].replace('PRIOR-CONCEPT REFERENCE ONLY. Planned shot: ', '')} + {b['kind']} building block. Animate the stated action in Google Omni after the keyframe is reviewed.\n\nDirection: {b['note']}\n")
    lines.append(f'''\n## BEFORE YOU SEND IT BACK

1. Replace estimated timing with word-aligned continuous narration; check every image and caption against its cue.
2. Resolve the claims below before narration recording and causal medical animation.
3. Confirm current bottle/label, ingredient identity and serving against verified records; remove historical label candidates from the final board.
4. Review actual GPT Image 2.5 keyframes in Cutroom before animation. No planning reference should be marked approved final media.
5. Verify identical woman/home/anatomy across shots; no medication disposal, fake credentials or testimonial evidence.
6. Ensure S27 is the first product reveal; all three ingredient explanations precede it.
7. Check Motilli pronunciation and label legibility at phone size. Count the product frames; zero is a failure.
8. Final export: 1080x1920, 30fps, H.264, approximately -14 LUFS, true peak at or below -1 dBTP. Final duration follows the recorded VO plus 2s tail, not this planning estimate.

## MATERIAL PRODUCTION ISSUES

The accepted copy contains claims that the earlier drafting pass did not substantiate. The product-development brief says human evidence does not establish celery/apigenin as a constipation or motility treatment. Existing copy and live product pages are not substitutes for evidence. The colon-only remedy explanation, stomach-restart claim, chlorophyllin neutralization claim, fiber water-holding/low-bulk comparison and unaffected medication results need support or revision. This storyboard preserves the approved words transparently but does not certify them for launch. Conceptual diagrams must not present those claims as measured results.

The historical bottle photo shows 5g fiber. Product-development records warn about prior unverified amounts; do not copy that label into new production without confirmation.

## PRODUCT LINK

{PRODUCT}
''')
    (HERE / 'MOT-VID-013-brief.md').write_text('\n'.join(lines))
    print(json.dumps({'words': words, 'estimated_seconds': round(t, 2), 'shots': len(beats), 'product_reveal_s': beats[26]['start_s'], 'prior_asset_candidates': sum('frame' in b for b in beats), 'source_samples': len(refs), 'spec': str(HERE/'storyboard-spec.json')}))

if __name__ == '__main__':
    main()
