"""Three interchangeable solution-aware hooks and one future-paced shared body.

Planning artifacts only. Keep v1 intact; do not generate or approve media here.
"""
import copy
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SLUG = 'mot-vid-013-three-hooks-v2'
WPM = 190


def wc(text):
    return len(re.findall(r"\b[\w]+(?:[’'-][\w]+)*\b", text))


def clock(seconds):
    return f'{int(seconds)//60:02}:{seconds%60:04.1f}'


LOOKS = {
    'LIFE': 'Vertical 9:16 candid domestic photograph. Same woman about 55–60, shoulder-length salt-and-pepper hair, grey cotton tee and charcoal lounge trousers. Ordinary skin texture and body proportions; modest lived-in bathroom and kitchen. Use the approved woman/home anchor for every subsequent shot. Restrained expression; no staged testimonial, beauty filter or exaggerated distension.',
    'SCIENCE': 'Vertical 9:16 educational 3D illustration on deep navy. Anatomically coherent stomach, small intestine and colon, continuous tract and correct relative placement. Match one approved anatomy anchor. Amber locator highlight only; no blockage, repaired nerves, cure glow or product packages inside organs.',
    'INGREDIENT': 'Vertical 9:16 tactile macro still life on warm cream stone, clear glass dish, soft natural light. Use verified ingredient reference for actual appearance; no fabricated molecules or implied laboratory proof.',
    'PRODUCT': 'Vertical 9:16 product photography. Use approved current front/back bottle and gummy photos as identity references. Preserve exact label, transparent jar, cap, dark-green heart shape and relative scale. No invented label numbers. Current packaging reference is required before generation.',
    'OBJECT': 'Vertical 9:16 close photographic detail in the same home. Use verified package reference images for every recognizable remedy; no invented label text, distorted packaging or medication disposal.',
    'GRAPHIC': 'Vertical 9:16 clean cream background with space for three ingredient callouts. Add all readable typography and numbered labels later in the internal editor.',
}

# Same spoken hook in all three; only the visual treatment and approved hook overlay change.
HOOKS = [
    ('A', 'Remedy cabinet', 'Tried all of these?', [
        ('Eye-level view from just outside the open bathroom cabinet. Woman opens the door onto crowded shelves of MiraLAX, magnesium, stool softeners and fiber; packages face the viewer.', 'Her hand opens the cabinet; hard cut to a closer shelf view at the next cue.'),
        ('Close view of her hand hovering between the familiar remedy packages; her tired face remains visible at the frame edge. No product is falling or being thrown away.', 'Her hand pauses, then lowers without selecting anything. End on a brief, restrained exhale.'),
    ], 'Recognition: I have already bought all of these. Accumulated frustration.'),
    ('B', 'Reference-style remedies → anatomy', 'Still backed up?', [
        ('Recognizable MiraLAX, magnesium and fiber packages dominate the foreground against a dark navy anatomical backdrop. The connected digestive tract is visible behind them, not inside a product package.', 'Start with remedies clearly readable; hard cut from packages to the anatomy at the next cue.'),
        ('Same coherent digestive-tract illustration, framed to include both colon and stomach. A restrained locator highlights the colon; the stomach remains visible above it.', 'Move the camera upward from colon toward stomach. Use locator emphasis only, not a causal demonstration of treatment failure.'),
    ], 'Curiosity: familiar solutions create a reason to watch the location explanation.'),
    ('C', 'Another morning, same products', 'Another remedy. Still waiting?', [
        ('Tight bathroom-counter photograph: woman stirring fiber into a clear water glass beside recognizable magnesium and laxative packages. Modest cool morning light.', 'One restrained stir; hard cut to the woman at the next cue. Do not show a dose or imply an unsafe combination.'),
        ('Same woman fully clothed on the bathtub edge, elbows on thighs, looking tired. The same remedy packages and glass remain visible on a nearby counter.', 'She sets her hands on her knees and exhales. This is the same unresolved morning, not a measured before/after test.'),
    ], 'Recognition: repeated effort without the normal morning she wants.'),
]

# Accepted future-pacing direction. Aspirational narration, not invented customer testimony.
CLOSE = [
    ('For women on a GLP-1,', 'LIFE', 'Warm eye-level portrait of the same woman at the kitchen counter, now looking ahead rather than down.', 'Identification: make the intended audience explicit.'),
    ('the goal isn’t just another trip to the bathroom.', 'LIFE', 'Wide doorway view of her ordinary bathroom; she is in the adjacent hall, fully clothed. Do not show a bowel movement or imply verified relief.', 'Reframe: establish that the desired life is bigger than bathroom frequency.'),
    ('It’s feeling regular again—and getting on with your day.', 'LIFE', 'Close view of her picking up her bag and house keys from the hall table.', 'Desire: translate regularity into freedom to get on with life.'),
    ('Imagine waking up, going comfortably,', 'LIFE', 'Morning light on the same woman sitting up in bed; cut to a neutral bathroom-door detail. Editor label: IMAGINE YOUR MORNING.', 'Future pacing: explicitly introduce an imagined outcome, not a customer result.'),
    ('and getting dressed without wondering how long it’s been.', 'LIFE', 'She puts on a light cardigan over her usual tee and takes her bag. No altered waist size, flatter-stomach comparison or jeans transformation.', 'Restored routine: getting ready without the mental tally.'),
    ('Making plans without your stomach being the first thing you think about.', 'LIFE', 'Over-shoulder view of her choosing a time for coffee with a friend; hard cut to her picking up keys. Any phone text is added in the editor, not generated.', 'Freedom: social plans replace symptom monitoring.'),
    ('You want to feel like yourself again,', 'LIFE', 'Eye-level exterior portrait just outside the same home; natural small smile, relaxed shoulders and warm daylight.', 'Identity: connect the desire to an ordinary version of herself.'),
    ('without giving up the progress you’ve worked for.', 'LIFE', 'She walks out toward her day carrying her bag. No scale, body-size before/after or claims that medication effects are unchanged.', 'Progress protection: voice the viewer’s desire without promising medication compatibility.'),
    ('Motilli. 90-day money-back guarantee. Tap below.', 'PRODUCT', 'Verified current bottle and exactly two dark-green heart-shaped gummies on cream stone. Editor-set brand, 90-DAY MONEY-BACK GUARANTEE and SHOP MOTILLI. Add a two-second silent tail.', 'Risk reversal: make the next action clear.'),
]


def main():
    old = json.loads((HERE / 'storyboard-spec.json').read_text())
    old_beats = json.loads((HERE / 'production-plan.json').read_text())['shots']
    # Retain the shared explanation and product introduction, not the old feature-recap close.
    shared = copy.deepcopy(old_beats[2:28])
    for b in shared:
        b['status'] = 'planning_only'
    t = shared[-1]['end_s']
    for index, (vo, kind, visual, emotion) in enumerate(CLOSE, 29):
        end = t + wc(vo) / WPM * 60 + (2 if index == 37 else 0)
        shared.append({'id': f'S{index:02}', 'start_s': round(t, 3), 'end_s': round(end, 3),
            't': f'S{index:02} · {clock(t)}–{clock(end)}', 'script': vo,
            'kind': kind, 'visual': visual, 'emotion': emotion, 'status': 'planning_only',
            'continuity_group': 'woman-home' if kind == 'LIFE' else 'product',
            'note': 'Imagined desired-outcome scene, not testimonial evidence or a guaranteed product result. Keep identity and body size constant. Verify offer terms before launch.' if kind == 'LIFE' else 'Current bottle and guarantee verification required. Hold end card through two-second silent tail.'})
        t = end

    hook_lanes = []
    variants = []
    for code, name, overlay, directions, emotion in HOOKS:
        beats = []
        for idx, (visual, motion) in enumerate(directions):
            base = old_beats[idx]
            b = {'id': f'H{code}{idx+1}', 'start_s': base['start_s'], 'end_s': base['end_s'],
                 't': f'H{code}{idx+1} · {clock(base["start_s"])}–{clock(base["end_s"])}',
                 'script': base['script'], 'kind': 'SCIENCE' if code == 'B' else 'LIFE',
                 'visual': visual, 'emotion': emotion, 'overlay': overlay,
                 'status': 'planning_only', 'motion': motion,
                 'note': f'{motion} Overlay: {overlay} Add text in editor. No Motilli in the hook. At 00:06.0 join shared S03. Remedy references required; current comparative VO remains in claim review.'}
            beats.append(b)
        hook_lanes.append({'label': f'HOOK {code} — {name.upper()}', 'source': 'Choose ONE hook; do not play A, B and C consecutively.', 'beats': beats})
        variants.append({'id': f'MOT-VID-013-{code}', 'hook': [b['id'] for b in beats], 'shared_body': [b['id'] for b in shared], 'estimated_duration_s': round(t, 3)})

    all_beats = [b for lane in hook_lanes for b in lane['beats']] + shared
    for b in all_beats:
        visual = b['visual'].replace('PRIOR-CONCEPT REFERENCE ONLY. Planned shot: ', '')
        b['keyframe_prompt'] = f'{LOOKS[b["kind"]]} Shot: {visual} Capture the opening pose, not multiple panels or a motion collage. No embedded captions, watermark or fabricated evidence. Leave lower-middle safe space for editor-set captions.'
        b.setdefault('motion', 'Follow the stated visual action with restrained movement; hard cut at the next narration cue. Never depict an unsupported causal treatment result.')

    words = sum(wc(b['script']) for b in hook_lanes[0]['beats'] + shared)
    notes = copy.deepcopy(old['notes'])
    notes[0]['text'] = f'V2: three interchangeable 6-second visual hooks, one shared body and an aspirational future-pacing close. {words} words per version; approximately {t:.1f}s including 2s tail at {WPM} wpm. {len(all_beats)} unique planned shots. No new keyframes, voiceover or video generated.'
    notes.insert(1, {'title': 'ASSEMBLY — CHOOSE ONE', 'text': 'A or B or C (00:00–00:06) → shared S03–S28 → future pacing S29–S36 → S37 end card. All three use identical spoken narration, shared footage, music, offer and pacing. Only hook imagery and its approved overlay vary.', 'color': '#dff2e1'})
    notes.insert(2, {'title': 'FUTURE PACING, NOT BORROWED PROOF', 'text': 'Name women explicitly, then picture getting dressed, making plans and getting on with the day. Do not use “Women say they’re regular for the first time in years” without genuine substantiated Motilli customer evidence. No review stars, quotation marks, fake customer names or testimonial styling.'})
    spec = {'title': 'MOT-VID-013 V2 — Three Failed-Solution Hooks + Future Pacing', 'project': 'motilli',
            'summary': f'Solution-aware audience. Remedy cabinet / reference-style remedies and anatomy / another morning with the same products. Choose one opening, then the identical mechanism-first body, all three ingredients before Motilli, and a women-specific imagined normal-day close. {words} words; ~{t:.0f}s per version. GPT Image 2.5 stills → Google Omni video → internal editor. Planning only.',
            'timelines': hook_lanes + [
                {'label': 'SHARED BODY 1 — WHY THE OLD TOOLS LEAVE A GAP', 'beats': shared[:14]},
                {'label': 'SHARED BODY 2 — THREE REQUIREMENTS BEFORE MOTILLI', 'beats': shared[14:24]},
                {'label': 'SHARED BODY 3 — REVEAL → NORMAL DAY → CTA', 'beats': shared[24:]},
                old['timelines'][0]],
            'notes': notes, 'moodboard': old.get('moodboard', [])}
    (HERE / 'storyboard-v2-spec.json').write_text(json.dumps(spec, ensure_ascii=False, indent=2)+'\n')
    plan = {'concept_id': 'MOT-VID-013', 'revision': 2, 'status': 'planning_only', 'board_slug': SLUG,
            'image_model': 'GPT Image 2.5', 'video_model': 'Google Omni', 'editor': 'Internal adengine timeline editor',
            'width': 1080, 'height': 1920, 'fps': 30, 'planning_wpm': WPM,
            'spoken_word_count_per_variant': words, 'estimated_duration_s': round(t, 3),
            'timing_source': 'word-count estimate; replace with recorded VO alignment',
            'not_an_executable_edit_plan': True, 'variants': variants, 'shots': all_beats}
    (HERE / 'production-plan-v2.json').write_text(json.dumps(plan, ensure_ascii=False, indent=2)+'\n')
    (HERE / 'script-v2.txt').write_text('\n\n'.join(b['script'] for b in hook_lanes[0]['beats'] + shared)+'\n')
    prompt_set = [{'shot': b['id'], 'model_requested': 'GPT Image 2.5', 'status': 'not_generated', 'prompt': b['keyframe_prompt'], 'motion_direction_for_later': b['motion']} for b in all_beats]
    (HERE / 'keyframe-prompts-v2.json').write_text(json.dumps(prompt_set, ensure_ascii=False, indent=2)+'\n')
    brief = [f'# MOT-VID-013 V2 — Three hooks + future pacing\n\n{spec["summary"]}\n',
             '## Assembly\n\nChoose exactly one hook. All join S03 at approximately 00:06.0. The first Motilli reveal remains S27 at approximately 01:05.1. Future pacing starts S29. Timings are estimates, not recorded audio. Prior board and artifacts remain intact.\n',
             '## Production\n\nGenerate one woman/home anchor, one neutral anatomy anchor and verified remedy stills with GPT Image 2.5. Match all subsequent frames to those anchors. Review keyframes before Google Omni animation. Assemble and add typography in the internal editor. Product frames wait for a current approved label. No new media has been generated.\n']
    for note in notes[:4]:
        brief.append(f'### {note["title"]}\n\n{note["text"]}\n')
    for lane in spec['timelines'][:-1]:
        brief.append(f'## {lane["label"]}\n')
        for b in lane['beats']:
            brief.append(f'### {b["t"]}\n\nVO: {b["script"]}\n\nPicture: {b["visual"]}\n\nMotion: {b["motion"]}\n\nPurpose: {b["emotion"]}\n\nDirection: {b["note"]}\n')
    brief.append('## Launch holds\n\nExisting mechanism/comparison claims remain unsubstantiated in this planning draft. Resolve these before final VO or causal medical animation. Confirm current bottle label, actual formula and guarantee. Aspirational language and illustrative scenes are not evidence of efficacy. Do not manufacture customer quotes or copy the competitor’s results.\n')
    (HERE / 'MOT-VID-013-v2-brief.md').write_text('\n'.join(brief))
    assert len(variants) == 3
    assert all(' '.join(b['script'] for b in lane['beats']) == ' '.join(b['script'] for b in hook_lanes[0]['beats']) for lane in hook_lanes)
    assert all(abs(lane['beats'][-1]['end_s'] - shared[0]['start_s']) < .002 for lane in hook_lanes)
    assert len({b['id'] for b in all_beats}) == len(all_beats)
    for variant in variants:
        lookup = {b['id']: b for b in all_beats}
        seq = [lookup[k] for k in variant['hook'] + variant['shared_body']]
        assert all(abs(a['end_s'] - b['start_s']) < .002 for a, b in zip(seq, seq[1:]))
    print(json.dumps({'slug': SLUG, 'variants': 3, 'unique_shots': len(all_beats), 'shots_per_version': len(shared)+2, 'words': words, 'estimated_seconds': round(t, 2), 'first_product_s': shared[24]['start_s'], 'future_pacing_s': shared[26]['start_s']}))


if __name__ == '__main__':
    main()
